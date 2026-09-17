---
name: prepare-DA-interview
description: >
  Use when the interviewer wants to prepare for an upcoming Data Analyst /
  Analytics Engineer interview, before the call happens, from whatever the
  funnel has produced so far: recruiter screening notes, a CV, or both, plus
  one or more job descriptions (pasted, or Atlassian/Jira tickets). Triggers
  include "necesito preparar la entrevista del candidato X", "I need to prep
  the interview for candidate X", "help me prep for tomorrow's interview",
  "assess this candidate against the opening", "what should I probe with X",
  "where should I focus with this candidate". Produces a prep guide with a
  must-have coverage table, gap questions, two interview scenarios, logistics
  and risk flags, and a seniority pre-read. Do NOT use this to process a
  finished interview into a post-call assessment, or to run
  the live SQL livecoding app (use run-DA-livecoding).
metadata:
  version: "0.2.0"
---

# Interview Prep (Workflow A)

Pre-call. There is no transcript yet, so nothing here is a finding about the
candidate: **everything in a prep doc is a hypothesis to test on the call.**
Write it as questions to probe and things to watch, never as conclusions
about what the candidate can do. This is the inverse of the post-call
assessment, where the transcript is the only evidence and the CV is demoted
to a cross-check.

The interview is happening either way; that is not the interviewer's call.
What this decides is how to run it: where to spend the time, which gaps to
close, which scenarios to use, and what to flag about the fit going in.

## Inputs

Accept any combination of these. At least one candidate document and at
least one opening are required.

**Candidate side** (need at least one):
- **Recruiter screening notes.** The recruiter's template: name, location,
  academic background, motivation for change, English level, work experience
  summary, tech stack, key strengths, area of improvement, recruiter
  recommendation, notice period, planned time off, contract or structure
  expectations. Usually pasted into the chat.
- **CV.** Pasted, attached, or in `<workspace>/Candidates/<Candidate Name>/`.

When both are present, use both: the CV carries trajectory and tenure, the
notes carry motivation, logistics and the recruiter's read. They also
cross-check each other, and any contradiction between them is itself a
finding worth probing.

**Opening side** (need at least one):
- A **pasted JD**, or
- An **Atlassian/Jira ticket** (e.g. `ODS-xxx`).

If a candidate document or an opening is missing, **ask for it and stop.**
Do not proceed on one of the two.

### Sourcing rule

Only read what the interviewer actually hands over. Never go looking through
Jira, Drive, Gmail, Slack or the web for a candidate or an opening that
wasn't given to you.

The one automated fetch: **when a Jira ticket is shared**, pull it via the
Atlassian MCP (`getJiraIssue`, passing `qubika.atlassian.net` as `cloudId`)
before drafting, if that MCP is available. If a JD is mentioned but no link
or text is given, ask for it; never guess which opening is in play.

### Extracting a CV file

PDFs extract cleanly via `pypdf`/`PyPDF2` in a short Python one-liner; the
`Read` tool's PDF path needs poppler, which may not be installed. Collapse
whitespace after extracting, since CVs can come out with spaces between
every character:

```
python3 -c "import pypdf,sys,re;print(re.sub(r'\s+',' ','\n'.join(p.extract_text() for p in pypdf.PdfReader(sys.argv[1]).pages)))" "path/to/CV.pdf"
```

`.docx`:

```
python3 -c "import docx,sys;print('\n'.join(p.text for p in docx.Document(sys.argv[1]).paragraphs))" file.docx
```

## Where the workspace lives

This kit never stores candidate data (CVs, notes, transcripts, assessments)
inside the plugin itself. That data is personal and confidential and must
never be committed to this repo. Each interviewer keeps their own workspace,
resolved as `$DA_INTERVIEWS_DIR` if set, else `~/qubika-da-interviews/`, with
candidate folders under `<workspace>/Candidates/<Candidate Name>/`.

The role definitions this skill reads (`roles/DASRI.md`, `roles/DASRII.md`)
live in this plugin's own `standards/` directory, one level up from
`skills/`. Resolve that path relative to this skill's own location, not
relative to the interviewer's workspace.

## Output: file, chat, or both

Match the environment rather than forcing one shape:

- **Filesystem available** (Claude Code, or any session that can write):
  write `<workspace>/Candidates/<Candidate Name>/FirstnameLastname_InterviewPrep.md`,
  creating the candidate folder if needed. Then report in chat: where the
  file is, the fit read in one or two lines, and the two or three things most
  worth the interviewer's attention. This is the preferred path: the file is
  what the rest of this kit reads from the same candidate folder later, and
  it survives the chat session.
- **Chat-only** (Claude chat app, no filesystem): deliver the full prep
  inline, same structure, nothing truncated.
- If the interviewer asks for one shape explicitly, follow that.

Never create the output in Google Drive, Confluence or any connected app.
Those are sources only.

## Steps

1. **Read every input in full before writing a line.** Both candidate
   documents if both exist, and every JD.
2. **Parse the opening(s) first.** Extract every must-have as its own line,
   keeping the JD's exact strictness words ("at depth", "in production", "or
   clear evidence you will get there fast"). Strictness decides weight: a
   Missing on a strict must-have is the headline of the whole prep, and goes
   in the opening paragraphs, never buried in the table. Also extract the
   "what you own" items, since the scenarios and the extra questions come
   from those.
3. **Parse the candidate documents into evidence, marking provenance.** For
   each claim, mark whether it is recruiter-reported, self-reported, CV
   claim, or backed by a concrete example (a named project, a metric like
   "reduced storage 40%"). Separately, check every tool claim for **hands-on
   work vs exposure or oversight**: CV language like "familiar with",
   "supported", "collaborated on" is exposure until something shows
   otherwise. Say which one the document supports before writing that
   someone "uses" a tool. Then flag internal contradictions: years that do
   not add up, tool tenure longer than the role tenure, certifications on a
   different track than the stated direction, anything that reads as
   templated or padded, a motivation statement pointing at a different stack
   than the opening, or a CV that disagrees with the recruiter's notes.
4. **Map each must-have to evidence**, one of five statuses: **Strong**,
   **Partial**, **Likely (verify)**, **Not evidenced** (documents are
   silent), **Missing** (documents say the candidate lacks it). Every
   must-have from the JD gets a row. None skipped.
   - **With several JDs**, run them side by side in one table, a column per
     opening, and then say which is the more plausible fit and why. Openings
     on the same program often want different profiles, and a strong fit for
     one is not a fit for another.
5. **Write the fit read.** Cover: the shape of the profile against the shape
   of the seat (a data engineer profile in an analytics engineer seat is a
   headline, not a detail); where the JD is strict vs flexible relative to
   this candidate's strengths and weaknesses; whether the recruiter's
   recommendation holds against the JD, disagreeing openly when it does not;
   the framing that would make the candidate presentable to the client and
   whether the client has to accept that framing first; and, when the fit is
   poor for this seat, which other kind of seat would fit better, since
   there are often several openings on the same program.
6. **Pre-read the seniority question.** Check the evidence against
   `standards/roles/DASRI.md` and `DASRII.md` and their actual dimensions
   (Teamwork, Communication, Delivery, Leadership, Studio/Company Impact,
   Technical Expertise, AI Adoption), not a general impression. DASRI is
   strong autonomous ownership of a bounded scope; DASRII additionally
   requires scaling through others, coaching analysts, cross-team KPI or
   semantic governance, advising business or data leadership. Strong
   individual technical depth alone does not reach DASRII. Frame all of this
   as **where the evidence points and what is missing to confirm it**, never
   as a verdict. There is no transcript yet.
7. **Write the gap questions, grouped by gap.** Not by assessment category:
   the interviewer is going in to close specific gaps, so the grouping
   follows the gaps. Each question must test the underlying concept even
   when the candidate lacks the named tool (incremental strategies without
   dbt vocabulary, dialect migration without Snowflake, macros as "how did
   you reuse SQL logic"). Add one line per question on what a strong vs a
   weak answer sounds like. When a tool gap looks bridgeable, include one
   "what have you read or tried about X since you saw this description"
   question, which tests the learning-velocity claim directly. When the
   candidate has done an analogous thing (migrated SQL Server to Spark SQL,
   say), build the question on that so the transferable skill can show.
8. **Design the two scenarios** (rules below).
9. **Write the logistics and risk flags** (rules below).
10. **List what is still unresolved** and needs a decision or confirmation
    from the interviewer before the call: which JD to interview against,
    ambiguous JD details, whether a stated requirement is a hard filter,
    a missing document that would change the read.
11. **Deliver** per the output rules above, and close with a note that this
    is a prep guide only, and that the post-call assessment must be built
    from the interview transcript, not from this document.

## Scenario rules

- Exactly two: **easy** and **hard**. Easy tests the core daily task of the
  role, the bulk of the first months. Hard tests the part the JD calls most
  valuable or most ambiguous, usually stakeholder-facing or definitional.
- Each must be statable out loud in under a minute with no screen. Give the
  exact script in quotes.
- For each scenario include: **Script**, **Why it matters** (tied to a
  specific JD line), **Strong answer**, **Weak answer**, **What to expect
  from this candidate** given their background, and one **Follow-up** if
  they do well.
- Build clues into the scenario (the shape of the error, who is waiting,
  what already matches) so a strong candidate can reason from them and a
  weak one has to guess. A good scenario also rewards asking clarifying
  questions before answering.
- Put a business person in the scenario (an analyst waiting, two teams
  disagreeing) so communication can be scored, not just the technical path.
  If the candidate never addresses that person, tell the interviewer to ask
  "and what does she hear from you today?" and score that separately.

## Logistics and risk flags

These kill hires late, so they are a standing section, not an afterthought:

- Start date against notice period and planned time off, checked against the
  role's heaviest period.
- Contract type or structure expectations against what Qubika can actually
  offer in the candidate's country.
- Stated English level against how stakeholder-facing the role really is.
- The self-declared weakness against the role's actual shape (parallel
  streams, interruptions, ambiguity).
- Motivation for change against the actual stack of the opening.

Then, in the same section: the best STAR story available in the documents
and how to push on it, what to emphasize in the live SQL test given this JD,
and 4 to 6 additional questions. Always include one **failure question** ("a
change you shipped produced wrong numbers: how was it caught, what happened
in the first hour, what changed afterwards") and one about **documentation
others actually used**.

## Output structure

Same order whether it lands in a file or in chat. Bold headings, tight
bullets.

1. Title line: `Pre-interview prep: <Candidate> vs <Role> (<program or client if known>)`
2. **Overall.** 2 to 3 short paragraphs, fit read first, leading with any
   Missing on a strict must-have and with the two or three things genuinely
   uncertain or risky about *this* candidate that the standard question set
   would not surface.
3. **Profile read.** Trajectory and tenure, provenance of the main claims,
   hands-on vs exposure, contradictions and padding.
4. **Must-have coverage.** Table, `Must-have | What the documents show | Status`.
   One row per must-have, none skipped. With several JDs, a column each,
   plus the call on which fits better.
5. **Seniority pre-read.** Where the evidence points against DASRI/DASRII,
   and what is missing to confirm it. Framed as what to probe.
6. **Questions to probe the gaps.** Grouped by gap, numbered, each with its
   strong vs weak line.
7. **Scenarios.** Scenario 1 (easy) and Scenario 2 (hard), each with
   Script, Why it matters, Strong answer, Weak answer, What to expect from
   this candidate, Follow-up.
8. **Logistics and risks**, then **More questions worth asking**.
9. **Unresolved, needs your decision.**

## Content rules

**Language.** The written file is always in English, regardless of the
conversation's or the documents' language. Talk to the interviewer in their
own language. Never draft in another language and translate at the end.

**Everything ties back to the documents or the JD.** No generic interview
advice, no question that could have been copied from a bank. Reference the
candidate's real companies, projects and metrics so the questions are built
for this person.

**Distinguish demonstrated from claimed** everywhere: "recruiter says",
"self-reported", "CV claim, no example given", "backed by a metric".

**Be direct about the fit read.** Say plainly when a required item is
missing. Assertive and action-oriented beats hedged.

**Short over long.** No padding. Cutting length means dropping redundant
examples, never dropping the concrete evidence that makes a line verifiable.

**Never use em dashes or double hyphens** anywhere in the deliverable. Use
commas, colons, semicolons or periods.

**Bold every heading and subheading**, including each numbered section above
and each scenario's field labels. Re-check this after every edit pass, since
rewriting a block is where the bold gets dropped.

**Do not assume pronouns from a candidate's name.** A name is not a reliable
signal. Default to they/them until the documents or the interviewer confirm
otherwise.

**No CV restriction here.** Unlike a post-call assessment, where the CV is
cross-check-only and stays out of the file, in a prep doc the candidate
documents are the primary source and are cited freely. That is the whole
point of the deliverable.

This workflow is self-contained: every rule it needs is in this file. If a
post-call assessment rulebook ships alongside it in `standards/`, do not read
it here. Those rules presuppose a transcript (SQL sourced from the
interviewer, the trajectory of a spoken explanation, whose ambiguity it was,
the CV kept out of the file) and do not apply before the call. The handful
that do carry over are already restated above: hands-on vs exposure,
seniority against the real DASRI/DASRII dimensions, brevity, pronouns, bold
headings.
