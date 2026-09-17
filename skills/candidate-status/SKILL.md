---
name: candidate-status
description: >
  Use when the interviewer wants an overview of their Data Analyst interview
  pipeline — e.g. "cómo viene el pipeline", "qué candidatos tengo
  pendientes", "estado de los candidatos", "what's the status of the
  candidates", "quién falta procesar", "which assessments are missing".
  Scans the interviewer's Candidates/ workspace and reports each candidate's
  stage, artifacts, recorded verdict and any gaps.
metadata:
  version: "0.1.0"
---

# Candidate Pipeline Status

Run the scanner:

```bash
python3 "<SKILL_DIR>/status.py"
```

`<SKILL_DIR>` is the absolute path of this skill's own directory. It reads
`Candidates/*/` inside the interviewer's interview workspace and prints one
row per candidate: stage, artifact presence (`+`/`-` per artifact), and the
verdict plus seniority parsed out of the assessment file when there is one.
Below the table it lists gaps.

## Where the workspace lives

This kit never stores candidate data (CVs, transcripts, assessments) inside
the plugin itself — that data is personal/confidential and must never be
committed to this repo. Each interviewer keeps their own workspace, resolved
as:

- `$DA_INTERVIEWS_DIR` if set, else
- `~/qubika-da-interviews/`

with candidate folders under `<workspace>/Candidates/<Candidate Name>/`. If
that directory doesn't exist yet, the script exits with a message explaining
how to point `DA_INTERVIEWS_DIR` at the right place or create one — help the
user do that rather than guessing a path.

## Stages

Derived from which artifacts exist, most advanced first:

| Stage | Meaning |
|---|---|
| `done (Yes/No[, DASRI\|DASRII])` | Assessment carries a parsed verdict |
| `assessment drafted` | Assessment file exists but no verdict parsed yet |
| `interviewed, needs assessment` | Transcript present, no assessment — run `assess-DA-interview` |
| `prepped, awaiting call` | Prep or question doc exists, call hasn't happened |
| `CV only, needs prep` | Just a CV — run `prepare-DA-interview` |
| `empty` | Folder with nothing usable |

## Reporting to the interviewer

Summarize in their language. Lead with what needs action (candidates
awaiting an assessment, or a CV sitting unprepped), then the gaps. Don't just
dump the table — say what they should do next.

Two caveats when interpreting gaps:

- **"assessment exists but no transcript"** is usually benign for older
  candidates: the transcript was pasted into the conversation rather than
  saved to the folder. It only matters if the assessment needs to be revised
  later, since the source would be gone. Mention it as housekeeping, not as
  an error.
- **A missing CV** is likewise often just a file that was never downloaded.

## If the parse looks wrong

The verdict parser tolerates an extra title/metadata header above the
template's first question and markdown-bolded question lines (both occur in
practice). If a candidate shows `assessment drafted` when the file clearly
has a verdict, the file's question wording probably drifted from
`standards/interview_template.md` — check it with:

```bash
grep -niE 'move to the next|seniority' "Candidates/<Name>/<File>_Assessment.md"
```

Fix the file to match the template rather than loosening the parser: the
template wording is the contract.
