# Score and note format

## The score is out of 10, and the bar is 8

Every session starts at **10**. Each defect costs points. The floor is **1**.
**8 or more clears the screener**; below 8 does not.

Score only the **last result of each exercise**, and score the **data returned**,
never the SQL style.

| Defect | Cost |
| --- | --- |
| Right rows, wrong or missing sort in Exercise 2 (`ORDER BY` absent, or ascending when the statement asked for most recent first) | −0.5 |
| Wrong data on one exercise — Ex 1 returning 40, 0 or one row per stage; Ex 2 returning a cartesian product, unfiltered rows, 0 rows, or the wrong grain | −3 |
| An exercise never attempted, or nothing runnable written for it | −5 |

Deductions land on half points. Do not invent costs that are not in this table,
and do not soften one because the candidate seemed capable.

### What costs nothing

Mention it in the note if it is worth mentioning, but do not deduct:

- keyword casing, indentation, aliases, `SELECT *`-style sloppiness;
- extra columns beyond the three asked for, as long as the rows and their order
  are right;
- a clumsy path that lands on the right data: `GROUP BY stage HAVING stage =
  'hired'` that returns 6, a subquery instead of a join, a comma join with the
  condition in `WHERE`, `LEFT JOIN`, `LIKE 'Data'`;
- failed attempts and error messages along the way — including a case slip the
  candidate diagnosed and fixed themselves. Debugging your own error is the
  behaviour this screener most wants to see, not a defect.

Right, for the record: **6** in Exercise 1; the **12 rows** of the Data area in
Exercise 2, the three requested columns, most recent first.

### What the scale looks like in practice

| Session | Score | |
| --- | --- | --- |
| Both exercises right | 10 | above the bar |
| Right data, but Exercise 2 was never sorted | 9.5 | above the bar |
| Exercise 1 right, Exercise 2 a cartesian product | 7 | below |
| Exercise 1 returned 40, Exercise 2 right but unsorted | 6.5 | below |
| Time ran out with Exercise 2 untouched | 5 | below |
| Both exercises returned the wrong data | 4 | below |

The scale is deliberately sparse — two five-minute exercises cannot support
finer gradations, and nothing lands at 8 or 8.5. What the number buys is the
difference between *missed a detail* and *cannot write a join*, which a single
verdict word could not carry.

**Below 8 does not advance to the technical interview.** The score is what a
human reads if they want to argue the case; there is no separate conversation to
open, and no different number to negotiate.

## Time

The whole thing is **5 minutes**, explanation included. At five minutes the
recruiter stops the exercise wherever it is. A candidate still fighting
Exercise 1 at three minutes is not going to clear the bar; let them finish the
attempt anyway, it costs nothing and it is fairer.

Record the total time and the per-exercise time from the transcript. Someone who
scores 10 in 90 seconds and someone who scores 10 at 4:50 both scored 10 — time
is context for the technical interviewer, never part of the score.

## Note format

Short. It goes into Manatal as it is.

```
SQL screener — <Candidate name> — <date>
Score: <n> / 10 — above the bar (8) | below the bar (8)
Time: <mm:ss> total (Exercise 1 <mm:ss>, Exercise 2 <mm:ss>)

Exercise 1 (count with a filter): OK / not OK — <one line, plain language>
Exercise 2 (join two tables, filter by text, sort): OK / not OK — <one line>
What cost points: <one plain line per deduction, or "nothing" on a 10>

Their queries
Ex 1: <verbatim SQL>
Ex 2: <verbatim SQL>

Flag: <only if something warrants it — otherwise leave this line out>
```

The outcome is a plain lowercase clause with the bar printed next to it, so
anyone reading the record can act on it without judging SQL and without a word
in capitals deciding for them.

`What cost points` is what makes a 9.5 legible as different from a 7. One line
per deduction, in plain language a recruiter can defend in a conversation:
"joined the two tables but never filtered by area, so it returned all 40
candidates" — not "missing predicate on the dimension". On a 10, write
`nothing`.

Quote their SQL verbatim and nowhere else. Never rewrite it, never correct it
silently, and never put the right answer in the note — the note travels, and the
answer key does not. Name the defect, never the correction.

## Flags worth raising (and how)

A flag records a fact about how the session ran, so the technical interviewer
knows how to read the note. It is never a theory about the candidate. One line
each, plain and literal, and only when the transcript shows it:

- no queries run at all for an exercise, with something left in the editor
  (usually: ran out of time);
- the candidate said they had never used SQL;
- the session was dictated over screen share because the link would not open —
  then typing and typos are not theirs;
- the transcript had to be pasted by hand because it did not arrive by itself.

Nothing else goes on that line. In particular:

- never compare this session with another candidate's, from today or any other
  day, and never mention that two queries look alike;
- never comment on where a query might have come from, how fast it arrived,
  how it is formatted, or what the pauses between queries might mean;
- never write a flag that the recruiter could not read out loud to the
  candidate as a plain statement of fact.

If something in the transcript looks odd to you, the transcript itself is what
travels: pass it to the technical interviewer and let them read it. Suspicion
written into a record follows a person around, and this screener is not the
place where it gets decided.

## After the note

Paste it into the candidate's record in Manatal. At 8 or above, pass the raw
transcript along with it to the technical interviewer — they want the original
queries, not the summary.
