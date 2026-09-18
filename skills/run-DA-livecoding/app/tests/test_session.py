"""Session extras: the candidate's name and the slug it contributes to the
session folder."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from session import Session, compact_name, safe_dirname, slugify


class TestSlugify(unittest.TestCase):
    def test_accents_are_folded_to_ascii(self):
        self.assertEqual(slugify("María Pérez"), "maria-perez")
        self.assertEqual(slugify("Ana María Pérez-López"), "ana-maria-perez-lopez")

    def test_only_lowercase_letters_digits_and_dashes_survive(self):
        self.assertEqual(slugify("Jane Doe (candidate #2)"), "jane-doe-candidate-2")

    def test_path_separators_cannot_escape_the_sessions_folder(self):
        for name in ("../../etc", "/etc/passwd", "..", "./.."):
            slug = slugify(name)
            self.assertNotIn("/", slug)
            self.assertNotIn("..", slug)

    def test_a_name_with_no_ascii_letters_yields_nothing(self):
        for name in ("李雷", "", "   ", None, "!!!"):
            self.assertEqual(slugify(name), "")

    def test_length_is_capped_without_a_trailing_dash(self):
        slug = slugify("Alexandra Bartholomew Christopherson Delacroix Everett")
        self.assertLessEqual(len(slug), 40)
        self.assertFalse(slug.endswith("-"))


class TestSessionCandidate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def _session(self, **kwargs):
        return Session(["ex1"], ttl_min=60, log_path=os.path.join(self.tmp.name, "session.jsonl"), **kwargs)

    def test_no_candidate_by_default(self):
        self.assertIsNone(self._session().candidate)

    def test_candidate_is_kept_verbatim(self):
        self.assertEqual(self._session(candidate="María Pérez").candidate,
                         "María Pérez")


class TestSafeDirname(unittest.TestCase):
    """The candidate folder keeps the name readable but cannot escape itself."""

    def test_readable_name_survives_intact(self):
        self.assertEqual(safe_dirname("Ana María Pérez"), "Ana María Pérez")

    def test_no_traversal_escapes(self):
        for name in ("../../etc", "..", "../..", "a/../../b", "x\\..\\y"):
            out = safe_dirname(name)
            self.assertNotIn("/", out)
            self.assertNotIn("\\", out)
            self.assertFalse(out.startswith("."), out)
            self.assertNotEqual(out, "..")

    def test_separators_and_nul_are_dropped(self):
        self.assertEqual(safe_dirname("/etc/passwd"), "etc passwd")
        self.assertNotIn("\0", safe_dirname("Ana\0Test"))

    def test_falls_back_when_nothing_readable_is_left(self):
        for name in ("", "   ", "..", None):
            self.assertEqual(safe_dirname(name), "unnamed-candidate")

    def test_length_is_capped(self):
        out = safe_dirname("Alexandra Bartholomew Christopherson Delacroix "
                           "Everett Fitzgerald Harrington")
        self.assertLessEqual(len(out), 60)


class TestCompactName(unittest.TestCase):
    """The log filename matches the FirstnameLastname the other files use."""

    def test_spaces_collapse_into_camel_case(self):
        self.assertEqual(compact_name("Alejandro Almeida"), "AlejandroAlmeida")

    def test_accents_are_folded_to_ascii(self):
        self.assertEqual(compact_name("María Pérez"), "MariaPerez")

    def test_punctuation_is_dropped(self):
        self.assertEqual(compact_name("Jean-Luc De La Cruz"), "JeanLucDeLaCruz")

    def test_falls_back_when_nothing_is_left(self):
        for name in ("", "   ", None, "!!!"):
            self.assertEqual(compact_name(name), "Candidate")

    def test_result_is_filename_safe(self):
        for name in ("../../etc", "a/b\\c", "Ana\0Test"):
            out = compact_name(name)
            self.assertTrue(out.isalnum(), out)


class TestDiscardKeepsTheCandidateFolder(unittest.TestCase):
    """discard() removes the log and nothing else.

    The log now lives directly in the candidate's folder, alongside their CV,
    transcript and assessment, so a discard that removed the containing
    directory would destroy the interview record.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.neighbour = os.path.join(self.tmp.name, "X_Assessment.md")
        with open(self.neighbour, "w") as f:
            f.write("the assessment")
        self.log = os.path.join(self.tmp.name, "X_SQL_2026-01-01_00-00-00.jsonl")

    def tearDown(self):
        self.tmp.cleanup()

    def test_discard_deletes_only_the_log(self):
        s = Session(["ex1"], ttl_min=60, log_path=self.log)
        self.assertTrue(os.path.exists(self.log))
        s.discard()
        self.assertFalse(os.path.exists(self.log))
        self.assertTrue(os.path.isdir(self.tmp.name))
        self.assertTrue(os.path.exists(self.neighbour))
        with open(self.neighbour) as f:
            self.assertEqual(f.read(), "the assessment")

    def test_discard_clears_an_empty_containing_directory(self):
        os.remove(self.neighbour)  # nothing else in the folder
        sub = os.path.join(self.tmp.name, "2026-01-01_00-00-00")
        s = Session(["ex1"], ttl_min=60,
                    log_path=os.path.join(sub, "session.jsonl"))
        s.discard()
        self.assertFalse(os.path.exists(sub), "empty dir left behind")
        self.assertTrue(os.path.isdir(self.tmp.name))

    def test_discard_survives_a_log_that_is_already_gone(self):
        s = Session(["ex1"], ttl_min=60, log_path=self.log)
        os.remove(self.log)
        s.discard()  # must not raise
        self.assertTrue(os.path.exists(self.neighbour))

    def test_ending_normally_leaves_the_log_in_place(self):
        s = Session(["ex1"], ttl_min=60, log_path=self.log)
        s.end("ctrl_c")
        self.assertTrue(os.path.exists(self.log))
        self.assertTrue(os.path.exists(self.neighbour))


if __name__ == "__main__":
    unittest.main()
