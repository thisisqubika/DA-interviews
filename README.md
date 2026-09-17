# Qubika Data Analyst Interview Kit (plugin `qubika-livecoding`)

A standardized kit for running **Data Analyst / Analytics Engineer
interviews** the same way across the whole team — no third-party product, no
per-seat cost, one shared process. It covers the full interviewer workflow:

1. **Prep** the interview from the candidate's CV (and JD, if any).
2. **Run** a live SQL exercise from your own laptop, behind an ephemeral
   public link, with every query and its verdict streaming to your terminal.
3. **Assess** the finished interview into a structured, template-driven
   hiring recommendation, calibrated against Qubika's official DASRI/DASRII
   seniority criteria and a set of judgment rules distilled from real
   assessments.
4. **Track** the candidate pipeline at a glance.

Candidate data (CVs, transcripts, assessments) never lives in this repo —
see [Where your candidate data lives](#where-your-candidate-data-lives).

## Components

| Component | Purpose |
| --- | --- |
| Skill: `run-DA-livecoding` | Preflight + hands you the one-line command to start a live SQL interview in your terminal; also lists exercises, shows solutions, reads session logs, helps add exercises and troubleshoot. Invoke it as `/qubika-livecoding:run-DA-livecoding` or in natural language. The full app ships inside the skill (`skills/run-DA-livecoding/app/`). |
| Skill: `prepare-DA-interview` | Pre-call prep from the candidate's CV and JD: trajectory analysis, CV-vs-JD contrast, what to focus on, per-category questions. Invoke as `/qubika-livecoding:prepare-DA-interview` or "prep the interview for candidate X". |
| Skill: `assess-DA-interview` | Post-call structured assessment from the interview transcript, following `standards/interview_template.md` and the judgment rules in `standards/assessment-lessons.md`. Invoke as `/qubika-livecoding:assess-DA-interview` or "process the interview for candidate X". |
| Skill: `candidate-status` | Scans your interview workspace and reports each candidate's stage, artifacts, and recorded verdict. Invoke as `/qubika-livecoding:candidate-status` or "what's the status of my candidates". |
| `standards/` | The team's shared source of truth: the assessment template, the DASRI/DASRII role definitions, and the accumulated judgment rules. Skills read this; it isn't duplicated per-skill. |

## Install (as a Claude Code plugin)

The archive doubles as a single-plugin local marketplace
(`.claude-plugin/marketplace.json` is included). From the directory you
unzipped it into:

```bash
claude plugin marketplace add <install-dir> --scope project
```

then install `qubika-livecoding` from that marketplace. If the `claude
plugin` CLI is unavailable (e.g. managed-settings auth errors), declare it
directly in the project's `.claude/settings.json` instead — this is
equivalent and fully supported:

```json
{
  "extraKnownMarketplaces": {
    "qubika-livecoding-local": {
      "source": { "source": "directory", "path": "<install-dir>" }
    }
  },
  "enabledPlugins": { "qubika-livecoding@qubika-livecoding-local": true }
}
```

Restart the Claude Code session afterwards — plugins load at startup. Verify
with `/qubika-livecoding:run-DA-livecoding` or by asking "list the SQL exercises".

## Where your candidate data lives

This repo is shared across the team, so it never stores candidate data — no
CVs, transcripts, assessments, prep docs, or session logs, in any commit.
Each interviewer keeps their own workspace, outside the plugin:

- **Interview prep/assessment workspace**: `$DA_INTERVIEWS_DIR` if set, else
  `~/qubika-da-interviews/`, with each candidate in
  `Candidates/<Candidate Name>/`. The `prepare-DA-interview`,
  `assess-DA-interview`, and `candidate-status` skills read and write there.
- **SQL livecoding session logs**: `$DATA_ANALYTICS_LIVECODING_DATA_DIR` if
  set, else `~/qubika-sql-interviews/sessions/`. The `run-DA-livecoding`
  skill writes there.

Nothing needs to be created manually — the skills create the folders they
need on first use.

## Setup (one time)

```bash
brew install cloudflared   # optional — without it the link comes from localhost.run
```

```bash
python3 -m pip install --break-system-packages duckdb
```

## Usage

**The interview runs in your own terminal, and you stop it there.** Run
**`/qubika-livecoding:run-DA-livecoding`** (or just ask: *"run a SQL interview"*) and you
get a one-line command to paste into your terminal. Claude asks for the
candidate's name first and passes it as `--candidate`, so the log and the
session folder carry it. From that point on, that window is the interview: it
prints the candidate link, the steps, and every query the candidate runs, each
with a **result** verdict against the reference solution (`PASS`, `NEAR:*`,
`FAIL:*` with the reason) and **style** flags. **Ctrl+C in that window ends the
interview** — the link dies instantly.

Claude never launches the server itself, on purpose: a server started from a
chat session dies with that session and would drop the candidate's link
mid-interview.

Other things to ask Claude, any time:

- **"List the SQL exercises"** — the difficulty ladder with the technique each
  one tests (interviewer-only info).
- **"Show me the solutions"** — reference answers with expected outputs.
- **"What has the candidate run?"** — reads the live session log (queries,
  the result verdict and style flags per run).
- **"Add an exercise about window functions"** — scaffolds it in the right
  format.

## Usage — prep, assessment, and pipeline status

These three skills don't need a terminal window kept open; ask Claude
directly, any time:

- **`/qubika-livecoding:prepare-DA-interview`** or *"prep the interview for
  candidate X"* — before the call. Reads the candidate's CV (and JD, if
  given) from your workspace and writes
  `Candidates/<Name>/FirstnameLastname_InterviewPrep.md`: trajectory
  analysis, CV-vs-JD contrast, what to focus on, and per-category questions.
- **`/qubika-livecoding:assess-DA-interview`** or *"process the interview for
  candidate X"* — after the call. Asks the three mandatory questions (your
  live SQL verdict, the client/project fit, the JD link), then drafts
  `Candidates/<Name>/FirstnameLastname_Assessment.md` against
  `standards/interview_template.md`, calibrated with
  `standards/assessment-lessons.md` and the DASRI/DASRII definitions in
  `standards/roles/`. Runs a self-check pass (brevity, style, category
  coverage, verdict/seniority coherence) after the first draft and every
  edit.
- **`/qubika-livecoding:candidate-status`** or *"what's the status of my
  candidates"* — scans your workspace and reports each candidate's stage
  (needs prep, awaiting call, needs assessment, done) with the recorded
  verdict and any gaps.

See [Where your candidate data lives](#where-your-candidate-data-lives) for
where these skills read and write.

## Commands

The app is `skills/run-DA-livecoding/app/serve.py` inside the plugin. Every
command below is `python3 "<install-dir>/skills/run-DA-livecoding/app/serve.py"`
plus options; the skill hands it to you with the real path filled in. Run it in
**your own terminal** and leave that window open — it *is* the interview
console.

**Start an interview:**

```bash
python3 "<install-dir>/skills/run-DA-livecoding/app/serve.py" --candidate "Full Name"
```

Within about 30 seconds the banner prints the link to paste in the Meet chat,
checked and reachable before it is shown. **Ctrl+C in that window ends the
interview** and kills the link.

**Options** (all combinable):

| Option | Effect |
| --- | --- |
| `--candidate "Full Name"` | Puts the name in the log, the banner, the farewell and the session folder name. Optional, but you will want it. |
| `--exercise exercise_01,exercise_03` | Serve a subset. Default: all five. |
| `--tunnel cloudflare` / `--tunnel localhost.run` | Force one link provider. Default: start both and keep the first one that proves reachable. |
| `--no-tunnel` | Localhost only, no public link. The fallback when no provider works: share your own screen and the candidate dictates the SQL. |
| `--ttl 120` | Session lifetime in minutes (default 180) — a backstop in case you forget Ctrl+C. |
| `--port 8766` | Port (default 8765). Only needed when a previous session is still running. |
| `--list` | Print the exercises with the technique each one tests, then exit. |

**Before an interview**, to see what each exercise tests:

```bash
python3 "<install-dir>/skills/run-DA-livecoding/app/serve.py" --list
```

**Reading the console.** One line per query the candidate runs:

- `result` — `PASS` (same data as the reference solution) · `NEAR:cols` /
  `NEAR:order` (right data, other column or row order) · `FAIL:cols` /
  `FAIL:rows` / `FAIL:vals` (wrong, with the reason on the next line) · `n/a`
  (no reference for this exercise) · blank (the query failed, or it was an
  `EXPLAIN`/`DESCRIBE`, not an answer). Results are compared as **data**, never
  as SQL text, so CTEs, subqueries and different aliases all pass.
- `style` — `ok`, or flags: `T` tabs · `I` sloppy indentation · `L` layout (a
  long line, or a whole multi-clause query on one line) · `S` missing spaces
  around an operator or comma · `*` `SELECT *` · `A` expression column with no
  alias. Keyword casing is not judged.

The banner repeats this legend. Both columns are for you only; the candidate
never sees them.

**Afterwards.** Each session is one folder under
`~/qubika-sql-interviews/sessions/<timestamp>_<candidate-slug>/` (just
`<timestamp>/` when no name was given, and never inside the plugin), holding a
`session.jsonl` with every query, its verdict and reason, its style flags, and
the final text of each editor.

## Security model (short version)

Every route requires a 128-bit session token; anything else is a 404. The
candidate's SQL runs on a read-only DuckDB connection with external access
disabled — no local file reads, no writes, no config changes — plus a 30s
query timeout, 200-row result cap and rate limiting. Result verdicts, style
flags and the candidate's name are interviewer-only: they go to the terminal
and the log, never to any HTTP response. Exercise data is 100% synthetic (hard
rule for any exercise you add). The tunnel link dies with the process and
subdomains are never reused.

## Notes

- The link is checked before it is shown: Cloudflare and localhost.run are
  started together and the first one the server answers through wins, so a
  Cloudflare outage costs a few seconds instead of a dead link. The subdomain
  is random either way; off-putting Cloudflare names are auto-discarded. A
  fixed branded URL (e.g. `sql-livecoding.qubika.com`) would need a Cloudflare
  named tunnel — see the app README's "Future evolution".
- Plan B if the candidate's network blocks one provider: `--tunnel` the other
  one; if both, run with `--no-tunnel` and share your own screen.
