# Qubika SQL Interview (plugin `qubika-livecoding`)

Run **live SQL interviews** from your own laptop — no third-party product, no
per-seat cost. One command starts a small local web app with 5 SQL exercises
(statement + schemas + editor + Run button + results) on an embedded DuckDB
engine, and exposes it through an **ephemeral public link** (a Cloudflare
quick tunnel or localhost.run — both free, no account — whichever proves
reachable first) that you paste in the Google Meet chat. The
candidate shares their screen; your terminal shows every query they run,
whether its result matches the reference answer, and short SQL style flags.
**Stopping the process kills the link instantly**, and a JSONL log of the full
session is saved for later review.

## Components

| Component | Purpose |
| --- | --- |
| Skill: `run-DA-livecoding` | Preflight + hands you the one-line command to start an interview in your terminal; also lists exercises, shows solutions, reads session logs, helps add exercises and troubleshoot. Invoke it as `/qubika-livecoding:run-DA-livecoding` or in natural language. The full app ships inside the skill (`skills/run-DA-livecoding/app/`). |
| Skill: `prepare-DA-interview` | Pre-call prep from recruiter screening notes and/or a CV, against one or more job descriptions (pasted, or Jira tickets): must-have coverage table, gap questions, two ready-to-run interview scenarios, logistics and risk flags, and a DASRI/DASRII seniority pre-read. Invoke as `/qubika-livecoding:prepare-DA-interview` or "prep the interview for candidate X". |
| Skill: `assess-DA-interview` | Post-call write-up from the interview transcript (a Tactiq link, a Google Doc, a local file) plus the live SQL session log: verdict, DASRI/DASRII seniority, client fit per opening, and eleven evidence-backed categories against the shared template. Invoke as `/qubika-livecoding:assess-DA-interview` or "process the interview for candidate X". |
| `standards/` | The team's shared source of truth for what a good assessment looks like: `interview_template.md` (the canonical structure), `assessment-lessons.md` (judgment rules distilled from real assessments), and `roles/` (the DASRI / DASRII career-path definitions both skills check evidence against). |
| `workspace-template/` | Empty skeleton for your own interview workspace. Candidate files never live in this repo. |

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
| `--candidate "Full Name"` | **Required.** Names the candidate folder the session log is written to, and appears in the log, the banner and the farewell. Leave it out and it asks at the prompt. |
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

**Afterwards.** Each session is one folder in the candidate's own workspace
folder as
`<workspace>/Candidates/<Candidate Name>/<FirstnameLastname>_SQL_<timestamp>.jsonl`
(never inside the plugin), with every query, its verdict and reason, its
style flags, and the final text of each editor. It sits beside that
candidate's prep doc, transcript and assessment, and sorts with them. That
puts the SQL log next to the CV, the transcript and the assessment for the
same person, which is where `assess-DA-interview` reads it from. Setting
`DATA_ANALYTICS_LIVECODING_DATA_DIR` opts back into the old flat layout,
`<that dir>/sessions/<timestamp>_<candidate-slug>/`, at the cost of that
link.

## Interview prep (`prepare-DA-interview`)

Before the call, ask *"prep the interview for candidate X"* (or run
`/qubika-livecoding:prepare-DA-interview`) and hand over whatever the funnel has
produced: the recruiter's screening notes, a CV, or both, plus the opening.
Job descriptions can be pasted, or given as Atlassian/Jira tickets, which the
skill fetches for you. Several openings at once is fine; it compares them side
by side and says which is the more plausible fit.

You get a must-have coverage table (one row per requirement, none skipped),
questions grouped by the gaps they close, two scenarios ready to read out
loud with what a strong and a weak answer sound like, logistics and risk flags
(notice period, contract type, English against how client-facing the seat is),
and a read on where the evidence points for DASRI vs DASRII. Nothing in it is
a verdict on the candidate: there is no transcript yet, so it is written as
hypotheses to test on the call.

**Candidate data never lives in this repo.** The skill reads and writes a
workspace outside it, resolved as `$DA_INTERVIEWS_DIR` if set, else
`~/qubika-da-interviews/`. Copy the skeleton once:

```bash
cp -R workspace-template ~/qubika-da-interviews
```

See `workspace-template/README.md` for the per-candidate layout. In a chat
client with no filesystem, the prep is delivered inline instead.

## Interview assessment (`assess-DA-interview`)

After the call, ask *"process the interview for candidate X"* (or run
`/qubika-livecoding:assess-DA-interview`) and give it the transcript: a Tactiq
link, a Google Doc link, or a local file. It reads only the source you name,
never going looking for the recording elsewhere, and it reads the SQL session
log from the candidate's folder so the SQL judgment rests on the queries that
actually ran rather than on what anyone remembers. Then it asks the handful of
things it cannot know — your own read of the live exercise, which openings are
in play and what they are for, whether there is a Jira JD — and drafts against
`standards/interview_template.md`.

You get the verdict, a DASRI/DASRII seniority read checked against the
career-path definitions, fit judged per opening (a Yes overall is not a yes
for every seat), and eleven categories each carrying evidence from the call or
an explicit "not covered". It lands as
`Candidates/<Name>/FirstnameLastname_Assessment.md` in your workspace and is
printed in chat as well, so you can correct it in place. Corrections that
would recur on the next candidate get logged to
`standards/assessment-lessons.md` rather than lost.

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
