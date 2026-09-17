# Assessment Lessons — Judgment Rules for Data Analyst Interviews

This file accumulates judgment rules learned from real Data Analyst / Analytics
Engineer interview assessments at Qubika. Each entry started as a specific
correction on a specific candidate's draft; the candidate's identity and any
identifying detail have been stripped, but the underlying mechanism — what
went wrong in the reasoning, and the rule that fixes it — is kept intact,
because that mechanism is what generalizes to the next interview.

Treat this as a living document. When an assessment draft needs a correction
that would recur on a different candidate, add a dated entry here following
the existing format: **what went wrong** → **rule going forward**. Keep
entries short and actionable — a rule to follow next time, not a transcript of
the conversation.

This file is loaded by the `assess-DA-interview` skill and should govern every
assessment produced with this kit, on top of `interview_template.md`.

---

## Keep every block in an assessment brief and concise

**Pattern observed:** without an explicit length rule, Detailed Assessment
bullets tend to grow unchecked across edit rounds — one review found bullets
running 90+ words each, several times longer than needed to make the point.

**Rule going forward:**

- Every block is brief by default: the Overall Assessment, the follow-up
  focus section, and each Detailed Assessment bullet. A bullet is two to four
  sentences (the judgment, the evidence for it, the gap if there is one).
- Cite the one or two most telling specifics rather than every instance of
  the same signal. If a candidate showed the same weakness four times, that's
  one example plus "repeatedly," not four examples.
- Take more room only when fairness requires it (a genuinely mixed picture,
  an error whose mechanism needs explaining). Expand a block beyond that only
  when the hiring lead explicitly asks for more depth on it.
- Brevity is not vagueness: cut redundant examples, never the concrete
  evidence that makes a bullet verifiable. A short bullet with a named tool
  and a specific moment beats a long one full of impressions.
- Re-check length on every edit pass, same as the em-dash check. Rounds of
  "add this detail too" are exactly what make blocks creep.

## Judge a concept explanation by the candidate's whole trajectory, not just their final phrasing

**Pattern observed:** a draft credited a candidate with correctly explaining
a technical concept (e.g. fact/dimension tables, a layered architecture
pattern) because by the end of the exchange the candidate had produced
roughly accurate content. On closer review of the transcript, the candidate
had visibly not known the answer when first asked, and only arrived at
something coherent after a long, hesitant back-and-forth — in one case,
explicitly declining to answer a concept by name ("I'd rather not say
something that could be wrong"), then describing the same concept minutes
later while discussing an unrelated topic, without ever recognizing it was
the same thing until it was pointed out. Grading only the eventual output
missed that the concept was shaky and disorganized in the candidate's head,
not solid.

**Rule going forward:**

- When a candidate eventually lands on a correct answer, trace how they got
  there before calling it "correctly explained": did they answer promptly and
  directly, or only after visible searching, hedging, or multiple prompts?
  Did a later, disconnected part of the transcript happen to contain the
  right content without the candidate tying it back to the original
  question?
- A candidate declining to answer by name, then unknowingly describing the
  same concept elsewhere without noticing the connection, is a stronger
  signal of disorganized/shaky knowledge than either "knows it" or "doesn't
  know it" alone — name that pattern explicitly rather than just scoring the
  final content as correct.
- This is a variant of the SQL-weighting lesson below: don't let the
  presence of eventually-correct content overshadow how weak or disorganized
  the process of getting there actually was.

## Weight live SQL exercise errors correctly — don't let conceptual/verbal strength overshadow them

**Pattern observed:** a draft leaned on a "Yes, move forward" verdict built
mostly on strong conceptual answers (pipeline mechanics, dimensional
modeling), while the live SQL exercise was summarized generically as "ran out
of time on the last exercise." Reviewing the actual screen-share showed the
candidate had joined two tables on a plausible-looking but wrong key (e.g.
`o.id = c.id` instead of the real foreign key) in every exercise requiring
it, without ever noticing, and could not construct a basic multi-value filter
(`IN (...)`), cycling through a self-contradicting `AND` condition and then a
misplaced `HAVING` before running out of time. These are fundamentals-level
SQL errors, not edge-case gaps, and they should have been the central driver
of the verdict, not a secondary note.

**Rule going forward:**

- When summarizing a live SQL exercise, don't default to describing outcomes
  only in terms of "which exercises were completed / ran out of time."
  Actively check for: wrong join keys (even if the query runs and returns
  rows), incorrect or abandoned filter logic, and any fundamental construct
  (basic filtering, `GROUP BY`/`HAVING` ordering, join conditions) the
  candidate struggled with, then weigh those explicitly in the Overall
  Assessment and the SQL bullet, not just completion count.
- A candidate joining on a plausible-looking but wrong key without noticing
  is a more serious signal than simply not finishing later exercises — flag
  it prominently.
- Don't let strong conceptual/verbal answers on adjacent topics (a tool's
  mechanics, data modeling theory) offset a weak hands-on SQL result when
  forming the overall recommendation; SQL fundamentals demonstrated live
  carry more weight than talking about SQL/data pipelines in the abstract.

## Don't default communication weaknesses to "English fluency" — check what's actually happening

**Pattern observed:** a draft described a candidate's spoken English as
having "frequent self-corrections and false starts," framing it as a
fluency/delivery issue. The actual transcript pattern was that many answers
started short or incomplete and only became complete after the candidate
asked a follow-up question or the question was reformulated for them, plus
visible uncertainty in the content of at least one answer — a content and
confidence issue, not a language one.

**Rule going forward:**

- When a candidate's answers read as unclear, short, or hesitant, don't
  default to attributing it to language/fluency. Check the actual transcript
  pattern: was the content itself incomplete or uncertain, and did it only
  become complete after the interviewer's own follow-up/reformulation? That's
  a communication-completeness or confidence signal, which is more relevant
  to the assessment than accent or grammar.
- Before writing any Communication or "confusion" claim, trace it back to
  whose words actually created the ambiguity in the transcript (see the next
  entry).

## Don't attribute the interviewer's own phrasing mix-ups to the candidate

**Pattern observed:** a draft credited a candidate with "conceptual
fuzziness" for "initially conflating relationship cardinality with filter
direction." Re-reading the transcript showed the interviewer was the one who
used the wrong term while asking the question (mixing up two concepts in the
question itself), and the candidate actually caught it ("I believe that
should be — is it not cardinality you're asking about, right?") before
answering. The candidate didn't know the underlying answer outright, but the
"confusion" was never theirs.

**Rule going forward:**

- Before writing that a candidate was confused about or conflated two
  concepts, check the transcript for who actually introduced the ambiguity.
  If it was the interviewer's phrasing (a garbled or double-barreled
  question), don't attribute the resulting back-and-forth to the candidate's
  understanding.
- It's fine, and often more accurate, to describe the candidate not knowing
  an answer outright but reasoning their way to a correct one with a fair
  justification — that's a genuinely different (and often more favorable)
  signal than "conflated two concepts."

## Always re-check claims against the actual transcript

**Pattern observed:** across several rounds of edits to the same assessment,
small inaccuracies crept in because bullets were being refined against an
earlier summary of the transcript rather than the transcript text itself. One
example: a bullet credited a candidate with explaining a concept correctly
"once clarified," when the transcript actually showed the interviewer
explaining the concept to the candidate, with the candidate never circling
back to confirm it in their own words.

**Rule going forward:**

- Before writing or editing any claim in the Detailed Assessment, go back to
  the transcript text itself for that specific moment — don't rely on a prior
  paraphrase (yours or an earlier draft's) as the source of truth.
- This matters most after several rounds of edits on the same document,
  where small drifts from the original transcript can compound.

## Don't phrase oversight/exposure as hands-on use

**Pattern observed:** a bullet stated that a candidate "uses [Tool X]," when
in fact the candidate's role was a management/oversight position and they
oversaw a team or pipeline that used the tool, rather than working in it
hands-on themselves.

**Rule going forward:**

- Before writing that a candidate "uses" or "works with" a tool/technology,
  check whether the transcript shows hands-on use or just exposure/oversight
  (managing a team that uses it, describing it accurately without doing the
  work themselves, etc.).
- If it's oversight/exposure rather than hands-on, say so explicitly (e.g.
  "their current project runs on X, but they oversee it as a manager rather
  than building it themselves" or "they can describe X accurately, but this
  is exposure, not hands-on experience").
- This distinction matters most for candidates in PM/DPM-type roles, where
  deep conceptual knowledge often outpaces current hands-on practice.

## Writing style: reduce em-dash usage

**Pattern observed:** the same style correction (reduce use of "—") recurred
across multiple assessments and multiple edit passes on the same document —
each round of "add this detail" or "trim this for concision" reintroduced
fresh em-dashes as a quick-connector crutch, and the check was only run after
the first draft, not after later edits.

**Rule going forward:**

- Use "—" sparingly. When a parenthetical aside would work just as well,
  prefer parentheses "( )" instead; a comma or period restructure often works
  too.
- This applies to assessments and any other written output produced with
  this kit, not just one document.
- Treat this as a check to run on the **whole document after every edit
  pass**, not just after the first draft: any time text is added, revised, or
  trimmed later in conversation, re-scan the full file for "—" before
  presenting it, not only the sentences just touched, since the check is easy
  to skip on iterative small edits.

## CV usage in candidate assessments

**Pattern observed:** when enriching an assessment with a candidate's CV, the
CV ended up cited throughout the Detailed Assessment bullets (e.g. "*CV
corroboration:* ...", "*CV adds:* ..."), overloading the document with
CV-sourced content. The assessment is supposed to be mainly grounded in the
interview transcript.

**Rule going forward:**

- The assessment file itself must stay **mostly transcript-based**. The CV
  is support material used to cross-check, not a source to cite inline
  throughout the document.
- Use the CV only to sanity-check what the candidate said (dates, employers,
  certifications, tools). Do **not** weave CV-derived facts and figures into
  the assessment's prose or bullets.
- **If something in the CV doesn't match what the candidate said in the
  interview** (different years of experience, a skill/tool claimed on paper
  but not demonstrated live, a certification level that doesn't match how
  they came across, etc.), **flag it in conversation with the hiring lead —
  never inside the assessment file.** The assessment stays clean;
  discrepancies are a conversation, not a document section.
- When in doubt about how much CV content to include, default to leaving it
  out of the file and raising it in conversation instead.

## Keep the Overall Assessment brief

**Pattern observed:** a first draft of the Overall Assessment ran three
paragraphs long. It should be a fraction of that.

**Rule going forward:**

- The Overall Assessment should be a single short paragraph (roughly 4-6
  sentences), not multiple paragraphs. Lead with the overall shape/fit
  judgment, then the one or two most important strengths and gaps.
- Save the supporting detail, evidence, and quotes for the Detailed
  Assessment bullets below it — don't front-load them into the Overall
  Assessment.
- This applies to any role type processed with this kit, not just Data
  Analyst assessments.

## Don't assume gender/pronouns from a candidate's name

**Pattern observed:** a draft defaulted to a gendered pronoun for a candidate
throughout an assessment, based on the candidate's first name alone — the
guess turned out to be wrong.

**Rule going forward:**

- Never infer a candidate's pronouns from their first name. Names aren't a
  reliable signal, and a wrong guess misgenders a real person.
- Default to they/them in the draft when pronouns aren't otherwise stated,
  unless the hiring lead has confirmed pronouns or the transcript makes the
  candidate's stated pronouns explicit.
- If the hiring lead corrects the pronoun for a candidate, fix it
  consistently throughout the whole document (Overall Assessment + every
  Detailed Assessment bullet), not just the first instance.

## Verify every technical concept the candidate explains against official sources

**Pattern observed:** a draft repeated a candidate's own explanation of a
tool's mechanics as if it were correct, without checking it — the candidate
had it backwards. The error would have been caught by comparing the
explanation to the tool's own official documentation.

**Rule going forward:**

- For every technical concept a candidate explains in the transcript (data
  warehousing concepts, tool-specific mechanics, SQL/dbt/BI semantics, etc.),
  verify the candidate's explanation against an official/authoritative source
  (vendor docs, e.g. dbt Labs, Databricks, Microsoft Learn, Google Cloud
  docs, or well-established references like Kimball Group for dimensional
  modeling) before writing the corresponding Detailed Assessment bullet.
- Do this systematically for the whole transcript, not just for the concept
  that happens to draw attention. Make a list of every concept touched on the
  call, then verify each one.
- If the candidate's explanation is correct, it's fine to state so plainly.
  If it's incorrect or technically vague/imprecise (right end-result, wrong
  or hand-wavy mechanism), say so explicitly in the bullet, citing what the
  accurate mechanism actually is, while still being fair (e.g. noting when a
  vague answer lines up with the candidate's own admission of limited
  hands-on exposure).
- This check applies across all Detailed Assessment categories where a
  technical concept was verbally explained, not only ETL Tools/SQL. It does
  not apply to purely experiential claims (what they built, team size,
  timelines), which stay evidence-from-transcript as before, not fact-checked
  against an external source.

## No delivery-tool step — the local .md is the deliverable, refined in conversation

**Rule going forward:**

- Once the `.md` file is written to the candidate's folder, treat it as
  already "delivered." The next steps are iterative corrections in
  conversation, not a delivery/send action.
- Don't invoke or refer to a file-delivery-style tool for this kit's output,
  even if such a tool happens to be available in a given session.
- Never use Google Drive, Confluence, or any connected app as a
  **destination** for an assessment or prep doc, even as a draft. Those
  systems may only be **sources** (to locate a transcript, JD, or CV).

## Use the QCPF DASRI/DASRII definitions to judge seniority, not general impression

**Pattern observed:** a candidate was marked DASRII based on a general
seniority impression from the transcript. Checking the transcript's evidence
against the actual QCPF dimensions showed the evidence (strong autonomous
technical ownership, no evidence of leading/coaching other analysts, no
cross-team KPI/semantic governance, no advisor-to-leadership role) matched
DASRI, not DASRII.

**Rule going forward:**

- Before assigning DASRI or DASRII in any assessment, read both
  `standards/roles/DASRI.md` and `DASRII.md` and check the transcript's
  evidence against their actual dimensions (Teamwork, Communication,
  Delivery, Leadership, Studio/Company Impact, Technical Expertise, AI
  Adoption), not just an overall gut sense of "senior."
- The key differentiator in practice: DASRI is strong autonomous
  individual-contributor ownership of a bounded scope (a dashboard, model,
  workstream); DASRII requires evidence of owning a broader domain/decision
  system AND scaling through others (coaching/leading analysts, cross-team
  KPI or semantic governance, acting as an advisor to business/data
  leadership, Studio-level impact). Strong individual technical depth alone,
  without that scaling-through-others evidence, points to DASRI even if the
  technical bar is high.
- If the transcript doesn't cover Leadership/Studio-Impact-type evidence at
  all (most technical interviews won't probe this deeply), don't default
  upward to DASRII just because the technical answers were strong. Absence of
  evidence for the DASRII-specific dimensions is itself informative.

## Detailed Assessment has nine categories

**Rule going forward:**

- The template's Detailed Assessment has **nine** required categories, in
  this order: Warehouse technologies, Data Modeling, ETL Tools, BI Tools,
  Dashboarding & Design, Project / Stake Holder Management, SQL, **AI
  Usage**, Communication. A tenth, **English**, is optional and only included
  when relevant to the role (client-facing or a specific market seat).
  `interview_template.md` is the source of truth for this list.
- **AI Usage** covers which AI tools/models the candidate mentions, what they
  actually use them for, and whether that's applied to real project work or
  just personal study. Don't inflate "took a course" or "played with it" into
  hands-on production use — same hands-on-vs-exposure distinction as
  elsewhere in this file.

## Speak in the interviewer's own voice, first person, not third person

**Pattern observed:** a Detailed Assessment bullet referred to the
interviewer by name in the third person ("when [Interviewer] explained it
with an example...").

**Rule going forward:**

- These documents are written in the interviewer's own voice. When
  describing something the interviewer said or did during the interview
  (asked a question, explained a concept, followed up on an answer), write
  it in the first person ("I explained...", "I asked...") rather than by name
  in the third person.
- This applies throughout every document produced with this kit — prep
  docs, assessments, any other output — not just one file.

## Judge role fit against the engagement's ramp-up budget, not just the skill gap

**Pattern observed:** an overall "Yes" verdict needed to become a clear "No"
for one specific opening — a short, fixed-scope engagement where the
candidate's answer to a structural/governance question described the
convention their own projects happened to use, rather than a genuine
understanding of the underlying design principles. That signals readiness to
build inside someone else's setup, not to audit or design one from scratch —
which is exactly what a short, knowledge-is-the-deliverable engagement
requires from day one.

**Rule going forward:**

- A "Yes" verdict is not automatically a yes for every open role. When
  multiple JDs are in play, evaluate each one separately against **how much
  ramp-up time that specific engagement actually affords**. A fixed-scope
  short engagement (audit, assessment, 2-4 week deliverable) has effectively
  zero ramp-up budget: the candidate must already know the platform on day
  one, because the knowledge itself is the deliverable. A longer build seat
  with onboarding can absorb a gap that a short audit cannot.
- Separate **"can't do this"** from **"can't do this in three weeks starting
  Monday."** Frame the rejection as a fit problem between candidate and
  engagement shape, not as a capability judgment, when the evidence supports
  that distinction. Say so explicitly in the client/job field.
- When a candidate answers a **structural/governance** question by
  describing the **convention their projects happened to use**, treat that as
  a distinct and informative signal: they know the platform as a user of
  someone else's setup, not as someone who designed, governed, or audited it.
  Building inside a lakehouse and judging someone else's lakehouse are
  different skills; don't let fluency in the first imply the second.
- Watch for the same wrong answer repeating across reformulations of a
  question. If the candidate gives the same off-target answer two or three
  times even after the question is cleanly restated, that's not a phrasing
  problem, it's the boundary of their mental model of that topic.

## Never serve both exercise sets in the same SQL livecoding session

**Pattern observed:** a session started without an explicit `--exercise`
flag loaded both the A and B exercise sets at once (ten exercises instead of
five), and the duplication was only noticed mid-interview when the candidate
link was opened, burning clock at the start of an already tight exercise
block.

**Rule going forward:**

- Always start the session with an explicit single set. Never let it default
  to loading everything.
  - Set A: `--exercise exercise_01,exercise_02,exercise_03,exercise_04,exercise_05`
  - Set B: `--exercise exercise_01b,exercise_02b,exercise_03b,exercise_04b,exercise_05b`
- Confirm which set is wanted before starting if it isn't obvious (e.g. a
  candidate repeating the exercise, or one set used recently with another
  candidate from the same referral source). Defaulting to A is fine when
  there's no stated preference, but the two sets must never be served
  together.
- Before handing over the candidate link, check the startup banner's
  "Exercises:" line and confirm it lists exactly five. If it lists ten, stop
  the process and restart with the flag rather than passing the link along.

## Never read the live SQL session from the truncated console log — use the JSONL

**Pattern observed:** narrating a live SQL session in real time from the
backgrounded `serve.py` console output led to misreading the outcome,
because the console truncates each query at roughly 100 characters — cutting
off exactly the clauses that mattered (the join condition, `GROUP BY`,
`HAVING`). A join key that was actually wrong (the classic
plausible-looking-but-wrong-key failure mode) was read as correct for most of
a session, and a dead end caused by a malformed `GROUP BY` was misread as a
`HAVING` threshold problem.

**Rule going forward:**

- The console log is only a heartbeat (which exercise, status, row count).
  Never quote or interpret the SQL text from it, and never draw a conclusion
  about a join key, `GROUP BY`, `HAVING`, or filter from a line that ends
  mid-clause.
- The full SQL lives in
  `~/qubika-sql-interviews/sessions/<timestamp>/session.jsonl`, appended per
  run while the session is live. Read that file (keys: `type`, `exercise`,
  `status`, `sql`, `row_count`, `duration_ms`, `error`; `type` is
  `run`/`editor_final`/`session_start`/`session_end`) instead of the console,
  including mid-interview.
- Row count alone never confirms correctness. Verify against the reference
  by loading `exercises/<name>/schema.sql` plus the `data/*.csv` into DuckDB
  and running both `solution.sql` and the candidate's query. A wrong-key join
  can return a plausible-looking row count, and can even return the right
  *shape* (e.g. one row per group) with wrong totals.
- While narrating a live session, label reads as provisional when they rest
  on partial data, and state the correction plainly once the full log is
  available. Don't let an encouraging in-flight reading stand as the
  assessment's version of events.

## A bench hire is judged on "would a client interview pass them?", not on the JD's bar

**Pattern observed:** a role's description was thin, and the actual purpose
turned out to be a proactive bench hire — meaning the real question was
whether the profile was solid enough to be fairly confident it would clear a
client interview, aligned to Qubika's classic sold stack (Databricks, Power
BI, dbt). A candidate who was strong overall but had only one of those three
tools as real hands-on practice (with the other two at minimal or stale
exposure) shouldn't get a flat "No" (their analytics ability was solid) or a
flat "Yes for anything" (the stack mismatch is real) — the correct verdict
was "Yes, but not for this position."

**Rule going forward:**

- Always establish what the opening is *for* before writing a verdict. A
  named client engagement, an internal Studio seat, and a proactive bench
  hire apply different standards to the same evidence. When a JD is terse,
  ask; don't infer the standard from the JD's requirement list alone.
- For a **bench hire**, the question is not "does this person meet the
  stated bar?" but "would we be confident putting them in front of a client
  tomorrow?" That is a higher and differently-shaped bar: it rewards
  demonstrable fluency in the stack actually being sold and gives no credit
  for adjacent-tool competence, because there is no specific engagement whose
  onboarding could absorb a gap.
- Check the candidate's stack against Qubika's **classic sold stack
  (Databricks, Power BI, dbt)** explicitly, tool by tool, and say how many of
  the three are real hands-on practice versus exposure. Strength in an
  adjacent equivalent (e.g. BigQuery for Databricks, Looker or Tableau for
  Power BI) is real skill and worth recording, but it does not substitute
  when the client is buying the named tool.
- A stack mismatch on a bench hire is a **"Yes, but not for this position,"**
  not a flat No. Reserve the flat No for candidates whose analytics ability
  itself doesn't clear the bar. When the profile is solid and the problem is
  which tools they've practiced, say so in that form, keep the seniority
  level as assessed, and name the shape of opening that *would* fit. The `-`
  seniority rule applies only to a genuine No, not to this verdict.
- This is the same distinction as the ramp-up-budget entry above (Yes
  overall, No for a specific engagement). Reach for it whenever the blocker
  is the fit between candidate and opening rather than the candidate's
  capability, and keep the document's tone matched to that: a stack-mismatch
  write-up should still read as a recommendation to keep the person in play.

## Every heading and subheading goes in bold

**Rule going forward:**

- In an assessment: bold each of the template's four question headings,
  `**Overall Assessment:**`, `**Detailed Assessment:**`, and every one of the
  Detailed Assessment category names as `* **Category:** content`. The colon
  goes inside the bold markers.
- In a prep doc (or any other file produced with this kit): the same applies
  to Markdown headings and to any inline lead-in that functions as a
  subtitle. A `#`/`##` heading already renders as a title, so bold the
  lead-in labels that aren't real headings, and keep `#` headings as headings
  rather than converting them.
- Apply this to new documents from the first draft, and re-check it on every
  edit pass alongside the em-dash and bullet-length checks. An edit that
  rewrites a bullet is the easy place to drop the bold on its category name.
