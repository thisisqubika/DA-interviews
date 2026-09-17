---
name: assess-DA-interview
description: >
  Use when the interviewer wants to process a finished Data Analyst /
  Analytics Engineer interview into a structured hiring assessment (e.g.
  "procesá la entrevista de X", "armá el assessment de X", "ya terminé la
  entrevista con X", "process the interview for X", "write up the
  assessment"). This is Workflow B (post-call, transcript-driven). It gates
  on the three mandatory questions, drafts the assessment from the
  transcript, then runs a self-check pass over the file before handing it
  over. Do NOT use this to prepare an interview before the call (use
  prepare-DA-interview for that) or to run the live SQL livecoding app (use
  run-DA-livecoding).
metadata:
  version: "0.1.0"
---

# Interview Assessment (Workflow B)

Produce `Candidates/<Candidate Name>/FirstnameLastname_Assessment.md` from an
interview transcript, inside the interviewer's own interview workspace (see
"Where the workspace lives" below). The local file is the deliverable; it
gets refined in conversation afterwards. Never create the output in Drive,
Confluence, or any connected app; those are sources only.

Talk to the interviewer in **their** language. Write the **file in
English**, always, regardless of the transcript's or the conversation's
language. Never draft in another language and translate at the end.

## Where the workspace lives

This kit never stores candidate data (CVs, transcripts, assessments) inside
the plugin itself — that data is personal/confidential and must never be
committed to this repo. Each interviewer keeps their own workspace, resolved
as `$DA_INTERVIEWS_DIR` if set, else `~/qubika-da-interviews/`, with
candidate folders under `<workspace>/Candidates/<Candidate Name>/`. Create
the candidate's folder there if it doesn't exist yet.

The standards this skill applies (`interview_template.md`,
`assessment-lessons.md`, `roles/DASRI.md`, `roles/DASRII.md`) live in this
plugin's own `standards/` directory, one level up from `skills/` — resolve
that path relative to this skill's own location, not relative to the
interviewer's workspace.

## Step 1 — Gather inputs before writing anything

Do not draft a single line until this step closes.

1. **Transcript.** Required. If not pasted or attached, look in
   `<workspace>/Candidates/<Candidate Name>/` for a `Technical Interview -
   *.txt` or similar. If there's none, ask for it and stop. No transcript, no
   assessment.
2. **Read the whole transcript** before writing. Also read
   `standards/assessment-lessons.md` in this plugin, which carries judgment
   rules distilled from real assessments and overrides first instincts.
3. **CV (optional).** Read it if present, as cross-check material only. PDFs
   extract cleanly with `pypdf`; the `Read` tool's PDF path needs poppler,
   which may not be installed:
   ```
   python3 -c "import pypdf,sys,re;print(re.sub(r'\s+',' ','\n'.join(p.extract_text() for p in pypdf.PdfReader(sys.argv[1]).pages)))" "path/to/CV.pdf"
   ```
   `.docx`: `python3 -c "import docx,sys;print('\n'.join(p.text for p in docx.Document(sys.argv[1]).paragraphs))" file.docx`

## Step 2 — Ask the three mandatory questions

Ask these together in one message, in the interviewer's language, and
**wait**. Proceeding without the SQL verdict or the client field is the
single most common way this deliverable comes out wrong.

1. **SQL livecoding verdict.** "What did the candidate solve, and what
   specific errors did they make?" The transcript only captures spoken
   train-of-thought while typing, never the query that ran or its result
   (that only existed on the shared screen). **Never infer the SQL outcome
   from the transcript.** The interviewer's answer is the sole source for the
   SQL bullet and any SQL mention in the Overall Assessment.
2. **Client/project fit.** Never invent or assume a client. Ask which
   openings are in play. If several are named, each gets judged separately
   (see Step 4).
3. **JD link.** Ask whether there's an Atlassian/Jira JD (e.g. `ODS-xxx`).
   Never guess which one. Fetch each via the Atlassian MCP (`getJiraIssue`,
   `cloudId: qubika.atlassian.net`) before drafting, if that MCP is
   available. No JD is fine, proceed.

Also confirm **pronouns** if the transcript doesn't make them explicit. Never
infer them from the candidate's name (a name is not a reliable signal).
Default to they/them until confirmed.

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
fine when the transcript supports them.

Read `standards/assessment-lessons.md` in full before drafting — it holds
the accumulated judgment rules (SQL error weighting, hands-on vs. exposure,
DASRI/DASRII criteria, bench-hire vs. named-engagement standards, brevity,
style) that decide the content of a strong assessment. Highlights:

- **Trace the trajectory, not the landing.** A correct answer given promptly
  is a different signal than the same content assembled after visible
  searching and follow-ups.
- **Whose ambiguity was it?** Before writing that the candidate was confused
  or conflated two concepts, check who introduced it in the transcript.
- **Don't default to "English fluency."** Check whether hesitant answers
  were actually thin in content, or only became complete after a follow-up.
- **Hands-on vs. exposure.** Say explicitly which one the transcript
  supports before writing "uses" or "works with" a tool.
- **Weigh live SQL errors heavily.** Wrong join keys that still return rows,
  abandoned filter logic, `WHERE`/`GROUP BY`/`HAVING` confusion outweigh
  strong conceptual answers on adjacent topics.
- **Every block stays brief.** Two to four sentences per Detailed Assessment
  bullet; one short paragraph for the Overall Assessment.
- **Seniority.** Verdict No means `-`. For Yes, read `standards/roles/DASRI.md`
  and `DASRII.md` and check the transcript's evidence against their actual
  dimensions, not a general impression.
- **A Yes is not a yes for every opening.** Judge each JD against its
  ramp-up budget; separate "can't do this" from "can't do this on this
  engagement's timeline."
- **The CV stays out of the file.** Cross-check only; flag CV/transcript
  discrepancies in chat, never in the document.
- **Voice.** First person for the interviewer's own words ("I asked...", "I
  explained..."), never third-person by name.
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
echo "— names in third person (expect 0 interviewer self-references):"; grep -n '\bI \|\bmy\b' "$F" >/dev/null; echo "(spot-check manually: no 'the interviewer said/asked' by name)"
echo "— CV cited inline (expect 0):"; grep -niE 'CV (corroborat|adds|confirm|shows)|per (his|her|their) CV|on paper' "$F"
echo "— categories present:"; grep -cE '^\* (Warehouse technologies|Data Modeling|ETL Tools|BI Tools|Dashboarding & Design|Project / Stake ?Holder Management|SQL|AI Usage|Communication):' "$F"
echo "— empty bullets (expect none):"; grep -nE '^\* [A-Za-z /&]+: *$' "$F"
echo "— seniority line:"; sed -n '1,6p' "$F"
echo "— long bullets (>90 words: review for trimming):"
awk '/^\* /{n=split($0,w," "); if(n>90){split($0,c,":"); printf "  %s (%d words)\n", c[1], n}}' "$F"
echo "— Overall Assessment length (target 4-6 sentences):"
awk '/^Overall Assessment:/{n=split($0,w," "); print "  "n" words"}' "$F"
```

Then verify by reading, not by grep alone:

- Category count is 9 (10 with the optional `English` bullet). Every one
  either carries transcript evidence or explicitly says it wasn't assessed.
- Seniority is coherent with the verdict: `-` for No, `DASRI`/`DASRII` for
  Yes, nothing else.
- No claim rests on a paraphrase of an earlier draft. After several edit
  rounds, small drifts from the transcript compound, so go back to the
  transcript text for each specific moment.
- The SQL bullet reflects **the interviewer's live verdict**, not the
  transcript.

Report to the interviewer in their language: where the file is, the verdict
and seniority with the reasoning in one or two lines, any CV-vs-transcript
discrepancy found (chat only), and anything the interview left untested.

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
