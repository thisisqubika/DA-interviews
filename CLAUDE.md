# CLAUDE.md — Qubika Data Analyst Interview Kit

## What this repo is

This is the `qubika-livecoding` Claude Code plugin: a standardized kit for
running Data Analyst / Analytics Engineer interviews across the team. It
covers the whole interviewer workflow — preparing before the call, running
the live SQL exercise, writing the post-call assessment, and tracking the
candidate pipeline — as one installable plugin so every interviewer works
from the same process, template, and judgment criteria.

## Hard constraint: this repo holds no candidate data, ever

This is the single most important rule in this project. The repo is
distributed to every interviewer on the team via a shared plugin
marketplace. It must contain **zero** candidate-identifying information: no
CVs, no transcripts, no assessments, no session logs, no names, in any
commit, past or present.

- Candidate data lives in each interviewer's **own workspace**, outside this
  repo, resolved via the `DA_INTERVIEWS_DIR` environment variable (default
  `~/qubika-da-interviews/`). See each skill's "Where the workspace lives"
  section.
- SQL livecoding session logs go to `~/qubika-sql-interviews/sessions/`
  (overridable via `DATA_ANALYTICS_LIVECODING_DATA_DIR`), same principle.
- Before any commit, check `git status`/`git diff` for anything that looks
  like a real name, a pasted transcript, or CV content. If something slips
  in, it needs to be scrubbed from history, not just deleted in a follow-up
  commit — flag it instead of pushing.
- Test fixtures and example data must be synthetic. This mirrors the
  existing hard rule for `run-DA-livecoding`'s SQL exercise data.

## Layout

```
qubika-livecoding/
├── skills/
│   ├── run-DA-livecoding/       SQL livecoding app (server, tunnel, exercises)
│   ├── prepare-DA-interview/    Workflow A — pre-call, CV-driven prep
│   ├── assess-DA-interview/     Workflow B — post-call, transcript-driven assessment
│   └── candidate-status/        Pipeline dashboard over an interviewer's workspace
└── standards/
    ├── interview_template.md    Canonical assessment template (single source of truth)
    ├── assessment-lessons.md    Judgment rules distilled from real assessments
    └── roles/
        ├── DASRI.md             QCPF Data Analyst Senior I definition
        └── DASRII.md            QCPF Data Analyst Senior II definition
```

`standards/` is the team's shared source of truth for *what a good
assessment looks like and how to judge one*. The skills in `skills/` are the
executable procedures that apply those standards; they don't duplicate the
content, they read it. If the process needs to change, edit `standards/`
first — skills should reference it, not restate it.

## The two interview workflows

- **Workflow A (`prepare-DA-interview`)** — before the call. CV-driven,
  since no transcript exists yet. Produces a prep guide: CV analysis,
  CV-vs-JD contrast, what to focus on, per-category questions.
- **Workflow B (`assess-DA-interview`)** — after the call. Transcript-driven,
  with the CV demoted to cross-check-only material. Produces the final
  hiring assessment against `standards/interview_template.md`.

They invert which source is primary (CV vs. transcript) on purpose — don't
conflate them. `run-DA-livecoding` is a separate, self-contained skill
(SQL exercise server) that either workflow can reference but doesn't depend
on programmatically.

## Updating `standards/`

`standards/assessment-lessons.md` is meant to grow. When an interviewer's
correction to an assessment draft reveals a durable judgment rule (not a
one-off), add a dated entry there following the existing format: what went
wrong → rule going forward. **Strip every candidate-identifying detail**
before it's written — no real names, no verbatim quotes that could identify
someone, no client names. Generalize the situation just enough to keep the
mechanism (what a reviewer should watch for) intact; see the existing
entries for the level of abstraction expected.

Changes to `standards/interview_template.md` are structural (section list,
category list) — treat them as team-wide decisions, not something to edit
unilaterally on a single assessment.

## Working conventions

- Everything written to disk by these skills (assessments, prep docs) is in
  English, regardless of the transcript's, the CV's, or the conversation's
  language. Conversation with the interviewer matches their language.
- Don't assume a candidate's pronouns from their name; default to they/them
  unless confirmed.
- See `skills/run-DA-livecoding/SKILL.md` for the SQL app's own rules (the
  interviewer owns the server process, never Claude — a server started from
  a chat session dies with that session and would drop the candidate's link
  mid-interview).
