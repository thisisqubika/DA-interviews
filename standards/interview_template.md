# Interview Assessment Template

Skeleton for the deliverable produced at the end of every Data Analyst /
Analytics Engineer interview process run with this kit. Copy everything
below the line into `Candidates/<Candidate Name>/FirstnameLastname_Assessment.md`
in the interviewer's own workspace and fill it in.

**Before writing:** read the full transcript, plus `assessment-lessons.md` in
this `standards/` folder. The rules it carries (language split, CV usage,
seniority criteria, em-dash restraint) govern this document and are
summarized in the notes at the bottom.

**Do not add sections or reorder them.** Sub-bullets can be added inside an
existing category when the transcript supports it.

---

**Should the candidate move to the next step in the hiring process?**
 Yes / No

**What is the candidate's perceived seniority?**
DASRI / DASRII — or `-` when the verdict above is No.

**What actual client/job is fit for this candidate?**
[Always ask; never assume. When several openings are in play, evaluate each
one separately: a Yes overall is not a yes for every role. **One verdict per
opening plus one or two sentences of reasoning, no more.** Name the deciding
factor, not the argument for it; the evidence already sits in the Detailed
Assessment and does not get restated here. Distinguish a capability gap from
an engagement-shape mismatch (a short fixed-scope engagement affords no
ramp-up; a longer build seat with onboarding can absorb a gap that an audit
cannot).]

**Overall Assessment:** [One short paragraph, roughly 4-6 sentences. Lead
with the overall shape and fit judgment, then the one or two most important
strengths and gaps. State the years of experience, the industries and the
current role, and **always say whether the candidate has Databricks
experience or not**, even when the answer is no — that one fact drives
staffing decisions and must never be left implicit. Faithful to what was
actually said, neither inflated nor unfairly harsh. If something wasn't
explored, say so rather than filling it in. Keep supporting detail and quotes
for the Detailed Assessment below. If the transcript is incomplete or has
inaudible parts, flag that here.]

**Should the next interviews focus more deeply on specific aspects?**
[What a follow-up round should probe, and why. Include topics that got too
little clock relative to their weight for the role in play, questions that
went unasked, and anything left genuinely uncertain. "Nothing to add" is a
valid answer.]

**Detailed Assessment:**

* **Warehouse technologies:** [...]
* **Data Modeling:** [...]
* **ETL Tools:** [...]
* **BI Tools:** [...]
* **Dashboarding & Design:** [...]
* **Project / Stake Holder Management:** [...]
* **SQL:** [...]
* **Python:** [...]
* **AI Usage:** [...]
* **Cultural fit:** [Soft signals: collaboration, initiative, honesty about
  gaps, verbosity vs. conciseness, hedging. Whether they look aligned with how
  the team works.]
* **Communication:** [...]
* **English:** [Level plus a sentence on what was observed. Optional; include
  when it's relevant to the role, e.g. a client-facing or US-facing seat.]

---

## Short form: a disqualifying observation

When the interviewer reports conduct that ends the process on its own (the
candidate consulting an outside source or another person during the live
exercise, someone else answering for them, a misrepresented identity or
history), the assessment stops at the headers. No Detailed Assessment, no
technical verification, no JD reading: none of it can change the
recommendation, so none of it is written.

```
**Should the candidate move to the next step in the hiring process?**
 No

**What is the candidate's perceived seniority?**
-

**What actual client/job is fit for this candidate?**
None. The process ended on conduct rather than fit.

**Overall Assessment:** [The approved conduct line, in the interviewer's first
person, stating what they observed and when. Then one sentence recording that
the rest of the interview was not evaluated, because no level of technical
performance would change the recommendation.]

**Should the next interviews focus more deeply on specific aspects?**
Not applicable.
```

The conduct line is **shown to the interviewer and approved before it is
written to the file.** It is an allegation about a named person that outlives
the conversation, so it is recorded as their observation ("During the live SQL
exercise I observed…") rather than as established fact, unless they ask for it
stated flatly. Never upgrade their "I think" into a finding, and never soften
their finding into a suspicion.

---

## Notes for filling this in

**Keep every block brief and concise.** This applies to the Overall
Assessment, the follow-up focus section and each Detailed Assessment bullet.
A bullet is two to four sentences: the judgment, the evidence that supports
it, and the gap if there is one. Cite the one or two most telling specifics,
not every instance of the same signal. If a category needs more room to be
fair (a genuinely mixed picture, an error that needs its mechanism
explained), take it, but the default is short. Only expand a block when the
hiring lead asks for more depth on it.

Brevity is not vagueness: cutting length means dropping redundant examples,
not dropping the concrete evidence that makes a bullet verifiable. Re-check
this on every edit pass, since rounds of added detail are what make blocks
creep.

**Weigh what was volunteered over what had to be pulled out.** What the
candidate raised on their own counts for far more than what only surfaced
after a probe. If a core practice (mocking a dashboard before building it,
running a stakeholder feedback loop, sanity-checking a query's result) never
came up until asked, say so explicitly: it signals the practice isn't part of
how they naturally work.

**Uncovered categories say so.** If the interview never touched a category,
write "Not covered during the interview." rather than leaving it blank,
padding it, or inferring content from an adjacent answer.

**Every bullet needs concrete evidence from the transcript** — examples,
tools named, how they handled a specific question — not generic impressions.
If a category wasn't covered, say so explicitly instead of leaving it blank
or inventing content.

**SQL is never sourced from the transcript.** The transcript only captures
spoken train-of-thought while typing, never the query that ran or its result.
The bullet is written from the session log `run-DA-livecoding` leaves at
`<workspace>/Candidates/<Candidate Name>/<FirstnameLastname>_SQL_<ts>.jsonl`
(every query's SQL, status, row count, `check` verdict and `style` flags),
plus the interviewer's own read of how it was arrived at. With neither, the
bullet stays empty rather than guessed at. Never read the SQL from the
console feed: it truncates at about 100 characters, cutting off exactly the
clauses that decide whether an answer was right. Watch
for: joining on the wrong key without noticing even when the query returns
rows, abandoned or self-contradicting filter logic, `WHERE`/`GROUP
BY`/`HAVING` ordering confusion, and whether they sanity-checked the result.
Weigh these fundamentals-level errors heavily; strong conceptual answers on
adjacent topics don't offset a weak hands-on result.

**Seniority.** No verdict means `-`, never a level. For a Yes, read
`standards/roles/DASRI.md` and `DASRII.md` and check the evidence against
their actual dimensions (Teamwork, Communication, Delivery, Leadership,
Studio/Company Impact, Technical Expertise, AI Adoption). DASRI is strong
autonomous ownership of a bounded scope; DASRII additionally requires scaling
through others — coaching analysts, cross-team KPI or semantic governance,
advising business/data leadership. Strong individual technical depth alone
doesn't reach DASRII, and absence of that evidence is itself informative.

**Hands-on vs. exposure.** Before writing that someone "uses" or "works
with" a tool, check whether the transcript shows hands-on work or
oversight/exposure. Say which it is. This matters most for PM/DPM-type
profiles where conceptual knowledge outpaces current practice. The same
discipline applies to AI Usage: don't inflate a course or a trial into
production use.

**Verify technical explanations.** For every concept the candidate explains,
check it against an authoritative source (dbt Labs, Databricks, Microsoft
Learn, Snowflake, Kimball) before writing the bullet. Don't repeat their
explanation as correct without checking. This doesn't apply to purely
experiential claims (what they built, team size, timelines).

**Trace how they got there, not just where they landed.** A correct answer
given promptly is a different signal than the same content assembled after
visible searching and several follow-ups. If a later, disconnected part of
the transcript happened to contain the right content without the candidate
tying it back, name that pattern.

**Whose ambiguity was it?** Before writing that a candidate was confused or
conflated two concepts, check who introduced the ambiguity. If the
interviewer's phrasing was garbled, don't attribute the resulting
back-and-forth to the candidate's understanding. Likewise, when answers come
out short or incomplete, don't default to blaming English fluency — check
whether the content itself was thin, or only became complete after a
follow-up.

**The CV, the screening notes and the prep doc all stay out of the file.**
This document is written from the interview. Recruiter screening notes
(`manatal.md`), the prep guide produced before the call, and the CV are
cross-check material only: use them to test what was said, never as a source
to recite. Facts that only these carry do not belong in the assessment, and
the prep doc's framing of an opening is a hypothesis it was written to test,
not a finding to repeat. Where the interview contradicts them, raise it in
conversation with the hiring lead, never inside the document.

Watch for this in the Overall Assessment specifically, which is where
pre-call material leaks in most easily: every claim in it should be traceable
to something the candidate actually said or did on the call.

**Voice and language.** Written in the interviewer's own first person ("I
asked...", "I explained..."), never third person by name. The file is always
in English regardless of the transcript's or the conversation's language.
Don't assume pronouns from a name; default to they/them unless confirmed.

**Style.** Use em-dashes sparingly; prefer parentheses or a comma
restructure. Re-scan the whole file for them after every edit pass, not just
the first draft.

**Bold every heading and subheading.** The four question headings,
`**Overall Assessment:**`, `**Detailed Assessment:**` and each Detailed
Assessment category name (`* **Category:** content`, colon inside the
markers). Re-check this on every edit pass too, since rewriting a bullet is
where the bold gets dropped.

**Delivery.** Save as `Candidates/<Candidate Name>/FirstnameLastname_Assessment.md`
in the interviewer's own workspace, and print the finished text in chat as
well so it can be read and corrected without opening the file. The local file
is the deliverable, refined in conversation until final. Never create the
output in Google Drive, Confluence, or any connected app.
