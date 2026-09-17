---
name: prepare-DA-interview
description: >
  Use when the interviewer wants to prepare for an upcoming Data Analyst /
  Analytics Engineer interview, before the call happens — e.g. "necesito
  preparar la entrevista del candidato X", "I need to prep the interview for
  candidate X", "help me prep for tomorrow's interview". This is Workflow A
  (pre-call, CV-driven — there is no transcript yet). Produces a prep guide
  with CV analysis, CV-vs-JD contrast, what to focus on, and per-category
  questions. Do NOT use this to process a finished interview into an
  assessment (use assess-DA-interview for that) or to run the live SQL
  livecoding app (use run-DA-livecoding).
metadata:
  version: "0.1.0"
---

# Interview Prep (Workflow A)

Produce `Candidates/<Candidate Name>/FirstnameLastname_InterviewPrep.md`
inside the interviewer's own interview workspace (see "Where the workspace
lives" below), from the candidate's CV and, optionally, a job description.
There's no transcript yet, so don't ask for one; this workflow inverts the
weighting of `assess-DA-interview`, where the CV is demoted to a cross-check
role. Here the CV is the primary source and is cited freely.

## Where the workspace lives

This kit never stores candidate data (CVs, transcripts, assessments) inside
the plugin itself — that data is personal/confidential and must never be
committed to this repo. Each interviewer keeps their own workspace, resolved
as `$DA_INTERVIEWS_DIR` if set, else `~/qubika-da-interviews/`, with
candidate folders under `<workspace>/Candidates/<Candidate Name>/`.

The role definitions this skill reads (`roles/DASRI.md`, `roles/DASRII.md`)
live in this plugin's own `standards/` directory, one level up from
`skills/` — resolve that path relative to this skill's own location.

## Steps

1. **Locate the CV.** It should be in
   `<workspace>/Candidates/<Candidate Name>/`. Read it before writing
   anything. If there's no CV in that folder, **ask for it and stop** (this
   workflow can't run without it, unlike the JD, which is optional).
   - PDFs extract cleanly via `pypdf`/`PyPDF2` in a short Python one-liner;
     the `Read` tool's PDF path needs poppler, which may not be installed.
     Collapse whitespace after extracting — CVs can come out with spaces
     between every character:
     ```
     python3 -c "import pypdf,sys,re;print(re.sub(r'\s+',' ','\n'.join(p.extract_text() for p in pypdf.PdfReader(sys.argv[1]).pages)))" "path/to/CV.pdf"
     ```
2. **Fetch the JD(s) if given.** Job descriptions are usually Atlassian/Jira
   links (e.g. `ODS-xxx`). Fetch each one via the Atlassian MCP
   (`getJiraIssue`, passing `qubika.atlassian.net` as `cloudId`) before
   drafting, if that MCP is available. If a JD is mentioned but no link is
   given, ask for it. If there's no JD, proceed on the CV alone and say so in
   the doc.
3. **Analyze the CV.** This is the core of the deliverable, not a summary of
   it. Cover: career trajectory and tenure at each role, which claims are
   hands-on vs. exposure language ("familiar with," "supported,"
   "collaborated on"), certifications and what track they're actually on,
   and anything that reads as templated or padded. Apply the same
   hands-on-vs-oversight discipline that `assess-DA-interview` applies to
   transcripts.
4. **Contrast the CV against the JD(s) explicitly.** Where the candidate
   clears the bar, where they don't, and where it's unclear. If there are
   multiple JDs, compare them side by side (a table works well) and say
   which is the more plausible fit and why, since they often want different
   profiles.
5. **Flag what to focus on beyond the standard question set.** This is the
   part interviewers care about most: the two or three things genuinely
   uncertain or risky about *this* candidate, that the usual questions
   wouldn't surface. Lead with them rather than burying them under the
   per-category questions.
6. **Then the per-category questions**, using the same categories as
   `standards/interview_template.md`'s Detailed Assessment. Flag which
   categories are low-stakes for the JD in play so interview time isn't
   burned on them.
7. **Pre-read the seniority question.** Check the CV evidence against
   `standards/roles/DASRI.md` and `DASRII.md` and say where it points and
   what evidence is missing, framed as what to probe rather than as a
   verdict (there's no transcript yet).
8. **List what's still unresolved** and needs a decision or confirmation
   from the interviewer (which JD to interview against, ambiguous JD
   details, whether a stated requirement is a hard filter).
9. **Write it to**
   `<workspace>/Candidates/<Candidate Name>/FirstnameLastname_InterviewPrep.md`.
   Close the file with a note that it's a prep guide only and that the
   eventual assessment must be built from the transcript via
   `assess-DA-interview`.

## Content rules

The content rules in `standards/assessment-lessons.md` and
`standards/interview_template.md` (language split, sparing em-dashes, first
person for the interviewer's own words, don't assume pronouns from a name,
don't inflate exposure into hands-on use, bold every heading) all still
apply here. The one exception is the CV-usage restriction: in a prep doc the
CV is the primary source and is cited freely, unlike in an assessment where
it's cross-check-only.

**Language.** The written deliverable and the conversation around it follow
different languages: files are always in English regardless of the
conversation's language; talk to the interviewer in their own language.

Since there's no transcript, everything in a prep doc is a hypothesis to
test on the call — write it that way (questions and things to probe), not as
findings about the candidate.
