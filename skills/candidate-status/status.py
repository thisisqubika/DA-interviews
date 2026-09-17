#!/usr/bin/env python3
"""Scan the interviewer's Candidates/ workspace and report each candidate's pipeline state."""
import os
import re
import sys
from pathlib import Path

DEFAULT_WORKSPACE = os.path.join(os.path.expanduser("~"), "qubika-da-interviews")
WORKSPACE = Path(os.environ.get("DA_INTERVIEWS_DIR", DEFAULT_WORKSPACE))
CANDIDATES = WORKSPACE / "Candidates"

# (label, predicate on lowercased filename)
ARTIFACTS = [
    ("CV",         lambda n: n.endswith((".pdf", ".docx")) and "assessment" not in n),
    ("transcript", lambda n: n.endswith(".txt")),
    ("prep",       lambda n: n.endswith("_interviewprep.md")),
    ("questions",  lambda n: n.endswith("_interviewquestions.md")),
    ("assessment", lambda n: n.endswith("_assessment.md")),
]


def verdict_of(path):
    """Pull the Yes/No verdict and seniority out of an assessment file.

    Some files carry an extra title/metadata header before the template's
    first question, so scan the whole file rather than a fixed prefix.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None
    # Some files bold the template questions, so strip markdown emphasis.
    lines = [l.strip().strip("*").strip() for l in text.splitlines()]
    verdict = seniority = None
    for i, line in enumerate(lines):
        if line.lower().startswith("should the candidate move"):
            for nxt in lines[i + 1:i + 3]:
                if re.fullmatch(r"(yes|no)\b.*", nxt, re.I):
                    verdict = nxt.split()[0].capitalize()
                    break
        if line.lower().startswith("what is the candidate's perceived seniority"):
            for nxt in lines[i + 1:i + 3]:
                if nxt:
                    seniority = nxt
                    break
    return verdict, seniority


def main():
    if not CANDIDATES.is_dir():
        sys.exit(
            f"No Candidates/ directory at {CANDIDATES}\n"
            f"Set DA_INTERVIEWS_DIR to point at your interview workspace, "
            f"or create {CANDIDATES} to start one."
        )

    rows, issues = [], []
    for folder in sorted(CANDIDATES.iterdir()):
        if not folder.is_dir():
            continue
        files = [f for f in folder.iterdir() if f.is_file() and not f.name.startswith(".")]
        names = [f.name.lower() for f in files]

        have = {}
        for label, pred in ARTIFACTS:
            have[label] = any(pred(n) for n in names)

        assessment = next((f for f in files if f.name.lower().endswith("_assessment.md")), None)
        verdict, seniority = verdict_of(assessment) if assessment else (None, None)

        if verdict:
            stage = f"done ({verdict}{', ' + seniority if seniority and seniority != '-' else ''})"
        elif have["assessment"]:
            stage = "assessment drafted"
        elif have["transcript"]:
            stage = "interviewed, needs assessment"
        elif have["prep"] or have["questions"]:
            stage = "prepped, awaiting call"
        elif have["CV"]:
            stage = "CV only, needs prep"
        else:
            stage = "empty"

        rows.append((folder.name, stage, have))

        # Gaps worth flagging
        if have["assessment"] and not have["transcript"]:
            issues.append(f"{folder.name}: assessment exists but no transcript in the folder")
        if have["assessment"] and not have["CV"]:
            issues.append(f"{folder.name}: assessment exists but no CV in the folder")
        if not files:
            issues.append(f"{folder.name}: folder is empty")

    width = max(len(r[0]) for r in rows) if rows else 10
    print(f"{'CANDIDATE'.ljust(width)}  {'STAGE'.ljust(30)}  ARTIFACTS")
    print(f"{'-' * width}  {'-' * 30}  {'-' * 40}")
    for name, stage, have in rows:
        marks = " ".join(
            f"{'+' if have[label] else '-'}{label}" for label, _ in ARTIFACTS
        )
        print(f"{name.ljust(width)}  {stage.ljust(30)}  {marks}")

    print(f"\n{len(rows)} candidates.")
    if issues:
        print("\nGaps:")
        for i in issues:
            print(f"  ! {i}")


if __name__ == "__main__":
    main()
