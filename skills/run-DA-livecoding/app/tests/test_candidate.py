"""The candidate's name is mandatory, and it decides where the log is written.

An unnamed session log is one nobody can match back to an interview, so
serve.py refuses to start without a name — from the flag, or from the prompt.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import serve


class TestResolveCandidate(unittest.TestCase):
    def test_flag_wins_and_is_sanitized(self):
        self.assertEqual(serve._resolve_candidate("  María   Pérez  "),
                         "María Pérez")

    def test_empty_flag_is_rejected_without_prompting(self):
        with self.assertRaises(serve._MissingCandidate):
            serve._resolve_candidate("   ")

    def test_missing_flag_is_rejected_when_there_is_no_terminal(self):
        with mock.patch.object(sys, "stdin") as stdin:
            stdin.isatty.return_value = False
            with self.assertRaises(serve._MissingCandidate) as cm:
                serve._resolve_candidate(None)
        self.assertIn("--candidate", str(cm.exception))

    def test_missing_flag_is_asked_for_at_the_prompt(self):
        with mock.patch.object(sys, "stdin") as stdin, \
                mock.patch("builtins.input", side_effect=["", "  Ana Test "]):
            stdin.isatty.return_value = True
            self.assertEqual(serve._resolve_candidate(None), "Ana Test")

    def test_prompting_gives_up_rather_than_looping_forever(self):
        with mock.patch.object(sys, "stdin") as stdin, \
                mock.patch("builtins.input", return_value="") as asked:
            stdin.isatty.return_value = True
            with self.assertRaises(serve._MissingCandidate):
                serve._resolve_candidate(None, prompts=3)
        self.assertEqual(asked.call_count, 3)

    def test_ctrl_c_at_the_prompt_stops_instead_of_starting_unnamed(self):
        with mock.patch.object(sys, "stdin") as stdin, \
                mock.patch("builtins.input", side_effect=KeyboardInterrupt):
            stdin.isatty.return_value = True
            with self.assertRaises(serve._MissingCandidate):
                serve._resolve_candidate(None)


class TestLogPath(unittest.TestCase):
    STAMP = "2026-09-18_10-00-00"

    def test_log_lands_in_the_candidates_workspace_folder(self):
        with mock.patch.object(serve, "LEGACY_DATA_DIR", None), \
                mock.patch.dict(os.environ,
                                {"DA_INTERVIEWS_DIR": "/tmp/ws"}, clear=False):
            self.assertEqual(
                serve.log_path_for("María Pérez", self.STAMP),
                "/tmp/ws/Candidates/María Pérez/MariaPerez_SQL_"
                + self.STAMP + ".jsonl")

    def test_name_matches_the_other_per_candidate_files(self):
        with mock.patch.object(serve, "LEGACY_DATA_DIR", None), \
                mock.patch.dict(os.environ,
                                {"DA_INTERVIEWS_DIR": "/tmp/ws"}, clear=False):
            path = serve.log_path_for("Alejandro Almeida", self.STAMP)
        self.assertEqual(os.path.basename(path),
                         "AlejandroAlmeida_SQL_" + self.STAMP + ".jsonl")
        # same folder as AlejandroAlmeida_Assessment.md, not a subfolder
        self.assertEqual(os.path.dirname(path),
                         "/tmp/ws/Candidates/Alejandro Almeida")

    def test_a_retake_does_not_overwrite_the_first_attempt(self):
        with mock.patch.object(serve, "LEGACY_DATA_DIR", None):
            a = serve.log_path_for("Ana Test", "2026-09-18_11-00-00")
            b = serve.log_path_for("Ana Test", "2026-09-18_14-00-00")
        self.assertNotEqual(a, b)

    def test_workspace_defaults_to_the_home_directory(self):
        env = {k: v for k, v in os.environ.items() if k != "DA_INTERVIEWS_DIR"}
        with mock.patch.object(serve, "LEGACY_DATA_DIR", None), \
                mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(
                serve.log_path_for("Ana Test", self.STAMP),
                os.path.join(os.path.expanduser("~"), "qubika-da-interviews",
                             "Candidates", "Ana Test",
                             "AnaTest_SQL_" + self.STAMP + ".jsonl"))

    def test_a_name_cannot_write_outside_the_candidates_folder(self):
        with mock.patch.object(serve, "LEGACY_DATA_DIR", None), \
                mock.patch.dict(os.environ,
                                {"DA_INTERVIEWS_DIR": "/tmp/ws"}, clear=False):
            path = serve.log_path_for("../../etc", self.STAMP)
        self.assertTrue(
            os.path.normpath(path).startswith("/tmp/ws/Candidates/"), path)

    def test_the_env_var_still_buys_the_old_flat_layout(self):
        with mock.patch.object(serve, "LEGACY_DATA_DIR", "/tmp/legacy"):
            self.assertEqual(
                serve.log_path_for("María Pérez", self.STAMP),
                "/tmp/legacy/sessions/" + self.STAMP
                + "_maria-perez/session.jsonl")


if __name__ == "__main__":
    unittest.main()
