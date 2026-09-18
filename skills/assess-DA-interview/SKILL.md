---
name: assess-DA-interview
description: >
  Use when the interviewer wants to turn a finished Data Analyst /
  Analytics Engineer interview into a structured hiring assessment (e.g.
  "procesá la entrevista de X", "armá el assessment de X", "ya terminé la
  entrevista con X", "summarize this interview", "make the summary of the
  mock with X", "evaluate X", "process the interview for X", "write up the
  assessment", "use the format we already used"). Also use when asked to
  shorten, translate or revise an assessment this skill produced. This is
  Workflow B (post-call, transcript-driven): it reads the transcript from
  the source the interviewer named (a Tactiq link, a Google Doc, a local
  file), reads the live SQL session log, gates on the questions it cannot
  answer alone, drafts against the shared template, then runs a self-check
  pass before handing it over. Do NOT use this to prepare an interview
  before the call (use prepare-DA-interview) or to run the live SQL
  livecoding app (use run-DA-livecoding).
metadata:
  version: "0.3.0"
---

# Interview Assessment (Workflow B)

Produce `Candidates/<Candidate Name>/FirstnameLastname_Assessment.md` from an
interview transcript, inside the interviewer's own interview workspace (see
"Where the workspace lives"), and print the finished text in chat as well, so
it can be read and corrected without opening the file. The local file is the
deliverable; it gets refined in conversation afterwards. Never create the
output in Drive, Confluence, or any connected app; those are sources only.

Talk to the interviewer in **their** language. Write the **file in
English**, always, regardless of the transcript's or the conversation's
language. Never draft in another language and translate at the end.

## Where the workspace lives

This kit never stores candidate data (CVs, transcripts, assessments, SQL
session logs) inside the plugin itself — that data is personal/confidential
and must never be committed to this repo. Each interviewer keeps their own
workspace, resolved as `$DA_INTERVIEWS_DIR` if set, else
`~/qubika-da-interviews/`, with candidate folders under
`<workspace>/Candidates/<Candidate Name>/`. Create the candidate's folder
there if it doesn't exist yet.

The standards this skill applies (`interview_template.md`,
`assessment-lessons.md`, `roles/DASRI.md`, `roles/DASRII.md`) live in this
plugin's own `standards/` directory, one level up from `skills/` — resolve
that path relative to this skill's own location, not relative to the
interviewer's workspace.

## Step 1 — Get the transcript, from the named source only

Do not draft a single line until this step and Step 2 both close.

**Tactiq is the system of record for interview recordings**, so when no
source is named, look there first: `search_meetings` with the candidate's
name. Interviews are titled `Technical Interview - <Role> - <Name> - <CC>`.
Check the title, the date and the attendees against the candidate before
reading, and if more than one plausible meeting comes back, or the match is
not exact, ask which one rather than picking.

**Everywhere else, use only the source the interviewer gave.** Never search
Drive, Gmail, Slack, Confluence or the web for the interview. If the named
source fails, say so and stop rather than substituting another one: a
recording of a different session with the same candidate is worse than no
recording.

- **Tactiq link** (`app.tactiq.io/...`), or the meeting id a search returned:
  read it with the Tactiq MCP.
  `get_transcript` with the link as `meetingId`, from page 1 until `hasMore`
  is false. Also `get_meeting` for the title (it usually carries the role and
  the candidate's name) and the attendees; don't wait on its AI summary if it
  is still generating, since it derives from the same transcript and adds
  nothing. If a Tactiq tool returns `access_required`, call
  `get_access_options` and show the interviewer the result instead of trying
  another source.
- **Google Docs link**: take the file ID (the segment after `/d/`) and read
  it with Drive's `read_file_content`. If the output is persisted to a file
  because it is large, read that file in full.
- **Local file**: read it directly. If nothing was given, look in
  `<workspace>/Candidates/<Candidate Name>/` for a `Technical Interview -
  *.txt` or similar.

No transcript, no assessment: ask for it and stop.

**Archive it in the candidate's folder before reading on.** A fetched
transcript is written to
`<workspace>/Candidates/<Candidate Name>/<meeting title>.txt`, using the
Tactiq meeting title as the filename so it matches the
`Technical Interview - *.txt` pattern this step looks for. Head it with the
source (Tactiq meeting id and URL, or the Drive file id), the recording date,
the duration, the attendees and the retrieval date, then the entries as
`[MM:SS] Speaker: text`. Add a short note listing the garbled terms worth
knowing (`"data rigs" = Databricks`) and mark any stretch with no speech
captured, naming the file that does hold that evidence. Skip the write only
when the transcript was already a local file in that folder. This keeps the
assessment auditable after the Tactiq retention window closes, and it is why
a re-run does not need to re-fetch.

Candidate data never enters git: `.gitignore` covers `Candidates/` and
`*.txt`, which matters because the workspace may sit inside the repo
checkout.

**Read the whole transcript before writing.** The interview is not linear —
evidence for one category is scattered across the session (a dbt remark in the
intro, a soft-skill signal during the SQL exercise). Classify each passage by
topic, not by where it appeared. These transcripts are machine-generated:
expect garbled words, misheard names and mixed English/Spanish. Infer meaning
from context, never quote garbled text verbatim, and skip a passage that is
too garbled to interpret rather than guessing. When a meaningful stretch of
audio is lost (long gaps between timestamps, single-word entries), say so in
one line before the assessment and mark the affected categories as not
covered. **Expect this over the live SQL exercise specifically**: candidates
work silently while typing, so the recording routinely has a hole running from
the moment the link is handed over to the time warning near the end. That is
normal, not a fault, and it is why the SQL bullet comes from the session log.

Then read `standards/assessment-lessons.md` in this plugin, in full. It
carries the judgment rules distilled from real assessments and overrides
first instincts.

**CV (optional).** Read it if present, as cross-check material only. PDFs
extract cleanly with `pypdf`; the `Read` tool's PDF path needs poppler,
which may not be installed:

```
python3 -c "import pypdf,sys,re;print(re.sub(r'\s+',' ','\n'.join(p.extract_text() for p in pypdf.PdfReader(sys.argv[1]).pages)))" "path/to/CV.pdf"
```

`.docx`: `python3 -c "import docx,sys;print('\n'.join(p.text for p in docx.Document(sys.argv[1]).paragraphs))" file.docx`

## Step 2 — Read the SQL log, then ask what only the interviewer knows

**The SQL session log.** `run-DA-livecoding` writes every query the candidate
ran to
`<workspace>/Candidates/<Candidate Name>/<FirstnameLastname>_SQL_<timestamp>.jsonl`,
in the candidate's own folder beside their prep doc, transcript and
assessment (sessions logged before this naming sit in
`~/qubika-sql-interviews/sessions/<stamp>_<slug>/session.jsonl`). Read the
newest one for this candidate; a retake gets its own timestamp, so check the
stamp against the interview date rather than assuming there is only one. Keys: `type`
(`session_start`/`run`/`editor_final`/`session_end`), `exercise`, `status`,
`sql`, `row_count`, `duration_ms`, `error`, plus each run's `check` verdict
and `style` flags and each exercise's final editor text.

- **Never infer the SQL outcome from the transcript.** It only ever captured
  spoken train-of-thought while typing.
- **Never read the SQL from the console feed**; it truncates at about 100
  characters, cutting off exactly the join conditions and `GROUP BY`/`HAVING`
  clauses that decide whether an answer was right.
- Row count alone never confirms correctness. A join on a wrong-but-plausible
  key returns rows, sometimes even the right shape with wrong totals. Check
  the `check` verdict, and when it is missing, load
  `exercises/<name>/schema.sql` plus `data/*.csv` into DuckDB and run both
  `solution.sql` and the candidate's query.

**Then ask, in one message, in the interviewer's language, and wait.**
Proceeding without these is the single most common way this deliverable comes
out wrong.

**Ask with `AskUserQuestion`, as multiple choice, in a single call.** A free
prose question makes the interviewer compose four answers from scratch after a
long call, which is when details get dropped. Offer concrete options instead:
one call, the four questions below, two to four options each. Every question
renders an "Other" box, so nothing is lost by offering options, and the
interviewer can always write their own answer instead of picking.

Make the options carry what you already know. The SQL question is the clearest
case: having read the log, name the readings that fit it (visibly stuck on a
specific exercise, worked steadily and ran out of clock, never sanity-checked a
result, did not watch closely) rather than offering generic ones. Use
`multiSelect` where answers can combine, which is the SQL read and the openings
in play, and single-select for conduct and the JD.

The tool caps at four questions, so **pronouns are confirmed in the chat text
that accompanies the call**, not as a fifth question. Say in the same message
which pronouns you will default to and why, and use the chat text for anything
else the interviewer should have in view while answering, such as a summary of
what the session log shows or a stretch of recording that was lost.

1. **Anything disqualifying, and any notes taken during the call.** Ask this
   first and read the answer before touching anything else, because it can end
   the work: "Was there anything unusual or concerning? Anything you noted
   while they were working through the exercise? Anything that decides this on
   its own?" What this is reaching for: signs the candidate consulted an
   outside source or another person during the live exercise, someone else
   answering for them, a misrepresented identity or history, or conduct that
   would end the process regardless of skill. The interviewer watched the call
   and the shared screen; none of that reaches the transcript or the session
   log, and it is not inferable from either. If the answer is yes, go to
   Step 2b and do not draft a full assessment.

   **This question also carries the interviewer's general notes**, which are
   not only about the SQL exercise. Give it three options: nothing unusual;
   something concerning that may decide this on its own; and nothing
   disqualifying but notes to add. That third option is the place for
   everything the recording does not hold and the exercise did not produce:
   demeanor, an off-transcript remark, context on why an answer came out the
   way it did, a scheduling or logistics flag. Prompt for the free text once
   it is picked, and fold what comes back into the relevant Detailed
   Assessment categories rather than into a section of its own.
2. **Their read of the SQL exercise.** The log says what ran; only the
   interviewer saw how it was arrived at — hesitation, dead ends, whether the
   candidate sanity-checked the result. Ask for it even with the log in hand.
   If there is no log, their answer is the only source; without either, the
   SQL bullet stays empty rather than guessed at.
3. **Client/project fit.** Never invent or assume a client. Ask which
   openings are in play, and what the opening is *for* (a named engagement, a
   Studio seat, a proactive bench hire) — they apply different standards to
   the same evidence. If several are named, each gets judged separately.
4. **JD link.** Ask whether there's an Atlassian/Jira JD (e.g. `ODS-xxx`).
   Never guess which one. Fetch each via the Atlassian MCP (`getJiraIssue`,
   `cloudId: qubika.atlassian.net`) before drafting, if that MCP is
   available. No JD is fine, proceed.

Also confirm **pronouns** if the transcript doesn't make them explicit. Never
infer them from the candidate's name (a name is not a reliable signal).
Default to they/them until confirmed.

## Step 2b — When something disqualifying is reported, stop short

A disqualifying observation decides the outcome on its own, so the rest of the
evaluation does not change the recommendation and is not worth writing. Skip
Steps 3 and 4 entirely. Do not verify technical claims, do not fill the
Detailed Assessment, do not read the JDs.

**Draft the conduct line and get it approved before it reaches the file.**
Write one or two sentences in the interviewer's own first person, stating what
they observed and when, then show it in chat and wait. This is an allegation
about a named person that will outlive the conversation, so it is written as
observation attributed to them ("During the live SQL exercise I observed…"),
not as established fact, unless they tell you to state it flatly. Never
upgrade "I think" into a finding, never soften a finding into a suspicion, and
never add corroboration of your own: if the session log happens to point the
other way, say so in chat so they can weigh it, and write what they decide.

Then write the short form from `standards/interview_template.md`: verdict No,
seniority `-`, no fitting opening, the approved conduct line as the Overall
Assessment plus one sentence recording that the remainder was not evaluated,
and "Not applicable" for the follow-up question. No Detailed Assessment. Run
the self-check, print it in chat, and stop.

If they answer that nothing was disqualifying, continue at Step 3 as normal.

## Step 3 — Verify technical claims

Before writing any bullet where the candidate explained a concept, list
every technical concept touched in the call and check each against an
authoritative source (dbt Labs, Databricks, Microsoft Learn, Snowflake,
Kimball). Do not repeat the candidate's explanation as correct without
checking — see `standards/assessment-lessons.md` for a real example of this
mistake and its correction. If a concept is wrong or hand-wavy, say so and
state the actual mechanism, while staying fair (a vague answer matching the
candidate's own admission of thin exposure is worth noting as such).

This applies to explained concepts only, not to experiential claims (what
they built, team size, timelines), which stay evidence-from-transcript.

## Step 4 — Draft the file

Copy the skeleton from `standards/interview_template.md` and fill it in.
**Do not add sections or reorder them.** Sub-bullets inside a category are
fine when the transcript supports them. The eleven Detailed Assessment
categories, in order: Warehouse technologies, Data Modeling, ETL Tools, BI
Tools, Dashboarding & Design, Project / Stake Holder Management, SQL, Python,
AI Usage, Cultural fit, Communication — plus the optional English.

Read `standards/assessment-lessons.md` in full before drafting — it holds
the accumulated judgment rules (SQL error weighting, hands-on vs. exposure,
DASRI/DASRII criteria, bench-hire vs. named-engagement standards, brevity,
style) that decide the content of a strong assessment. Highlights:

- **Trace the trajectory, not the landing.** A correct answer given promptly
  is a different signal than the same content assembled after visible
  searching and follow-ups.
- **Volunteered beats extracted.** What the candidate raised on their own
  weighs far more than what surfaced only after a probe. When a practice that
  should be second nature never came up until asked, say so explicitly.
- **Whose ambiguity was it?** Before writing that the candidate was confused
  or conflated two concepts, check who introduced it in the transcript.
- **Don't default to "English fluency."** Check whether hesitant answers
  were actually thin in content, or only became complete after a follow-up.
- **Hands-on vs. exposure.** Say explicitly which one the transcript
  supports before writing "uses" or "works with" a tool.
- **Weigh live SQL errors heavily.** Wrong join keys that still return rows,
  abandoned filter logic, `WHERE`/`GROUP BY`/`HAVING` confusion outweigh
  strong conceptual answers on adjacent topics.
- **Databricks is always stated.** The Overall Assessment says whether the
  candidate has Databricks experience or not, even when the answer is no. It
  drives staffing decisions and must never be left implicit.
- **Uncovered means uncovered.** A category the interview never touched gets
  "Not covered during the interview." — never a blank, never padding, never
  content inferred from an adjacent answer.
- **Every block stays brief.** Two to four sentences per Detailed Assessment
  bullet; one short paragraph for the Overall Assessment.
- **Seniority.** Verdict No means `-`. For Yes, read `standards/roles/DASRI.md`
  and `DASRII.md` and check the transcript's evidence against their actual
  dimensions, not a general impression.
- **A Yes is not a yes for every opening.** Judge each JD against its
  ramp-up budget; separate "can't do this" from "can't do this on this
  engagement's timeline."
- **Write it from the interview.** The CV, the recruiter screening notes and
  the prep doc are cross-check material only, never sources to recite. A fact
  that only the pre-call documents carry does not go in the file, and the prep
  doc's framing of an opening is a hypothesis it was written to test, not a
  finding. Flag any discrepancy in chat, never in the document. Check the
  Overall Assessment hardest: it is where pre-call material leaks in most
  easily, and every claim in it should trace to something the candidate said
  or did on the call.
- **The client/job field is a verdict, not an argument.** One verdict per
  opening plus one or two sentences naming the deciding factor. The evidence
  is already in the Detailed Assessment and does not get restated.
- **Voice.** First person for the interviewer's own words ("I asked...", "I
  explained..."), never third-person by name. Natural full sentences, not
  telegraphic fragments — the interviewer sends this as their own evaluation.
  Refer to the person as "the candidate" or by pronoun.
- **Style.** Em-dashes sparingly. Every heading/subheading in bold.

## Step 5 — Self-check the file, then report

Run this after the first draft **and after every later edit pass**.
Iterative edits reintroduce em-dashes as a quick-connector crutch, and the
check gets skipped precisely on the small edits. Re-scan the whole file, not
just the lines just touched.

```bash
F="Candidates/<Candidate Name>/<Firstname><Lastname>_Assessment.md"
echo "— em-dashes (expect few; review each):"; grep -c '—' "$F"
grep -n '—' "$F"
echo "— CV cited inline (expect 0):"; grep -niE 'CV (corroborat|adds|confirm|shows)|per (his|her|their) CV|on paper' "$F"
echo "— categories present (expect 11, 12 with English):"
grep -cE '^\* \*\*(Warehouse technologies|Data Modeling|ETL Tools|BI Tools|Dashboarding & Design|Project / Stake ?Holder Management|SQL|Python|AI Usage|Cultural fit|Communication|English):\*\*' "$F"
echo "— unbolded category names (expect 0):"; grep -nE '^\* [A-Za-z][^*]*:' "$F"
echo "— empty bullets (expect none):"; grep -nE '^\* \*\*[A-Za-z /&]+:\*\* *$' "$F"
echo "— Databricks stated in the Overall Assessment (expect 1+):"
awk '/^\*\*Overall Assessment:\*\*/,/^\*\*Should the next/' "$F" | grep -ci databricks
echo "— seniority line:"; sed -n '1,8p' "$F"
echo "— long bullets (>90 words: review for trimming):"
awk '/^\* /{n=split($0,w," "); if(n>90){split($0,c,":"); printf "  %s (%d words)\n", c[1], n}}' "$F"
echo "— Overall Assessment length (target 4-6 sentences):"
awk '/^\*\*Overall Assessment:\*\*/{n=split($0,w," "); print "  "n" words"}' "$F"
echo "— client/job field length (target under ~100 words):"
awk '/^\*\*What actual client\/job/,/^\*\*Overall Assessment:/' "$F" | wc -w
echo "— pre-call sources cited in the file (expect 0):"
grep -niE 'screening notes|recruiter (notes|recorded|reported)|prep doc|manatal|the prep (said|pointed)' "$F"
```

On a Step 2b short-form assessment, only the em-dash, pre-call-sources and
seniority checks apply; the category and length checks do not, and a missing
Detailed Assessment is correct rather than an omission.

Then verify by reading, not by grep alone:

- Category count is 11 (12 with the optional `English` bullet). Every one
  either carries transcript evidence or explicitly says it wasn't assessed.
- Seniority is coherent with the verdict: `-` for No, `DASRI`/`DASRII` for
  Yes, nothing else.
- No claim rests on a paraphrase of an earlier draft. After several edit
  rounds, small drifts from the transcript compound, so go back to the
  transcript text for each specific moment.
- The SQL bullet reflects **the session log plus the interviewer's read**,
  never the transcript.

Then **print the full assessment text in chat** alongside the file path, so
it can be read and corrected in place. If earlier tool calls mean chat text
would not render verbatim, send it with the user-message tool so it appears
exactly as written.

Report to the interviewer in their language: where the file is, the verdict
and seniority with the reasoning in one or two lines, any CV-vs-transcript
discrepancy found (chat only), any part of the recording that was lost, and
anything the interview left untested.

## Step 6 — Log durable lessons

When the interviewer corrects something, decide whether it's a one-off (this
document) or durable (future assessments too). If durable, append a dated
entry to `standards/assessment-lessons.md` following the existing format:
what went wrong → rule going forward, short and actionable, with any
candidate-identifying detail generalized away. Don't ask permission for
small stylistic/process corrections, just log it and mention it in chat. Ask
first only if the correction would contradict `standards/interview_template.md`
or this skill's workflow.

If the correction belongs to the live SQL app's behavior rather than to
assessment writing, it belongs in the `run-DA-livecoding` skill instead —
that skill never reads `standards/assessment-lessons.md`.
