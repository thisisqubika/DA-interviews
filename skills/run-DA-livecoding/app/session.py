"""Session state: token, TTL, per-exercise editor text, run history, JSONL log."""
import hmac
import json
import os
import re
import secrets
import threading
import time
import unicodedata


def slugify(name, max_len=40):
    """Filesystem-safe ASCII slug of a candidate name; "" if nothing survives.

    'Ana María Pérez-López' -> 'ana-maria-perez-lopez'; '../../etc' -> 'etc'.
    Only [a-z0-9-] can come out, so the result is safe as a directory suffix.
    """
    ascii_text = (unicodedata.normalize("NFKD", name or "")
                  .encode("ascii", "ignore").decode("ascii"))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:max_len].rstrip("-")


def safe_dirname(name, max_len=60):
    """Candidate name as a directory name: readable, but unable to escape.

    The session log lives in the candidate's own workspace folder, which
    assess-DA-interview later reads as "Candidates/<Candidate Name>/", so the
    name is kept as typed rather than slugified. Path separators, NUL and any
    leading dot come out, which is what stops "../.." from being a directory.
    Falls back to the slug, then to a placeholder, if nothing readable is left.
    """
    cleaned = "".join(" " if c in "/\\\0" else c for c in (name or ""))
    cleaned = " ".join(cleaned.split()).strip(". ")
    return cleaned[:max_len].strip(". ") or slugify(name) or "unnamed-candidate"


def compact_name(name, max_len=40):
    """'Alejandro Almeida' -> 'AlejandroAlmeida'; 'María Pérez' -> 'MariaPerez'.

    The FirstnameLastname form the other per-candidate files already use
    (FirstnameLastname_Assessment.md, FirstnameLastname_InterviewPrep.md), so
    the SQL log sorts next to them. ASCII only, so it is safe in a filename.
    """
    ascii_text = (unicodedata.normalize("NFKD", name or "")
                  .encode("ascii", "ignore").decode("ascii"))
    parts = [p for p in re.split(r"[^A-Za-z0-9]+", ascii_text) if p]
    return "".join(p[:1].upper() + p[1:] for p in parts)[:max_len] or "Candidate"


class Session:
    def __init__(self, exercise_names, ttl_min, log_path, candidate=None):
        self.candidate = candidate  # interviewer-only; never sent to the browser
        self.token = secrets.token_urlsafe(16)
        self.created_at = time.time()
        self.expires_at = self.created_at + ttl_min * 60
        self.ttl_min = ttl_min
        self.shutdown = threading.Event()
        self.shutdown_reason = None  # set by whoever requests the shutdown
        self.exercise_names = list(exercise_names)
        self.editor_texts = {name: "" for name in exercise_names}
        self.runs = []
        self.run_lock = threading.Lock()
        self.last_run_ts = 0.0
        # A path, not a directory: the log lands straight in the candidate's
        # folder, beside their CV, transcript and assessment. Nothing here may
        # ever remove that directory — see discard().
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
        self._lock = threading.Lock()
        self._log_file = open(self.log_path, "a", encoding="utf-8")
        self._ended = False

    def check_token(self, token):
        # Compare as bytes: str compare_digest raises TypeError on non-ASCII
        # input, and the token arrives percent-decoded from the URL.
        if not isinstance(token, str) or not token:
            return False
        return hmac.compare_digest(token.encode("utf-8"),
                                   self.token.encode("utf-8"))

    def expired(self):
        return time.time() >= self.expires_at

    def active(self):
        return not self.expired() and not self.shutdown.is_set()

    def set_editor_text(self, exercise, text):
        with self._lock:
            if exercise not in self.editor_texts:
                return False
            self.editor_texts[exercise] = text
            return True

    def editor_snapshot(self):
        with self._lock:
            return dict(self.editor_texts)

    def record_run(self, entry):
        with self._lock:
            self.runs.append(entry)
        self.log(dict(entry, type="run"))

    def log(self, obj):
        line = json.dumps(obj, ensure_ascii=False)
        with self._lock:
            if self._log_file.closed:
                return
            self._log_file.write(line + "\n")
            self._log_file.flush()

    def discard(self):
        """Drop a session that never started: close the log, delete just it.

        Only the log file. The directory holding it is the candidate's own
        folder, with their CV, transcript and assessment in it, so removing
        the directory here would destroy the interview record.
        """
        with self._lock:
            self._ended = True
            if not self._log_file.closed:
                self._log_file.close()
        try:
            os.remove(self.log_path)
        except OSError:
            pass
        # Then the containing directory, but only if this left it empty --
        # rmdir refuses a non-empty one, which is exactly the guarantee
        # wanted: a candidate folder holding a CV, transcript or assessment
        # can never be removed here. It only ever clears a timestamp folder
        # under the legacy layout, or a candidate folder this aborted run
        # created and never put anything else in.
        try:
            os.rmdir(os.path.dirname(self.log_path))
        except OSError:
            pass
        self.shutdown.set()

    def end(self, reason):
        with self._lock:
            if self._ended:
                return
            self._ended = True
        self.log({"type": "editor_final", "ts": time.time(),
                  "exercises": self.editor_snapshot()})
        self.log({"type": "session_end", "ts": time.time(), "reason": reason})
        with self._lock:
            self._log_file.close()
        self.shutdown.set()
