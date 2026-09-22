# Verdict and note format

## The verdict is binary: PASS or NOT PASS

Both exercises returned the right data → **PASS**. Anything else → **NOT PASS**.
There is no middle grade, no percentage and no "almost": these two exercises are
deliberately easy, so someone who writes SQL at all clears them inside the five
minutes, and someone who does not is not a borderline case.

Right means the data, not the SQL:

- **Exercise 1** — the single number **6**.
- **Exercise 2** — the **12 rows** of the Data area, the three requested
  columns, most recent application first.

Does **not** affect the verdict (these still PASS):

- keyword casing, indentation, aliases, `SELECT *`-style sloppiness;
- failed attempts and error messages along the way — only the last result of
  each exercise counts;
- a clumsy but correct path: `GROUP BY stage HAVING stage = 'hired'` that ends
  up returning 6, a subquery instead of a join, a comma join with the condition
  in `WHERE`, `LEFT JOIN`, `LIKE 'Data'`;
- extra columns beyond the three asked for, as long as the rows and their order
  are right. This is the only tolerance — mention it in the note.

NOT PASS, no matter how good the SQL looked:

- a wrong number in Exercise 1 (40 is the usual one — see the answer key);
- a wrong row set in Exercise 2: cartesian product, no `Data` filter, empty
  result from a case mismatch;
- the right rows in the wrong order, or unsorted — the statement asks for the
  order;
- only one of the two solved, or time ran out with an exercise unfinished;
- nothing runnable was written.

**A NOT PASS does not advance to the technical interview.** If the recruiter
thinks the circumstances warrant an exception (a broken connection, an obvious
language barrier, a candidate who has never touched SQL but is being considered
for something else), they say so to the hiring lead — that is a human decision,
not a different verdict.

## Time

The whole thing is **5 minutes**, explanation included. At five minutes the
recruiter stops the exercise wherever it is. A candidate still fighting
Exercise 1 at three minutes is already a NOT PASS in practice; let them finish
the attempt anyway, it costs nothing and it is fairer.

Record the total time and the per-exercise time from the transcript. Someone who
passes in 90 seconds and someone who passes at 4:50 are both a PASS — the time
is context for the technical interviewer, never part of the verdict.

## Note format

Short. It goes into Manatal as it is.

```
SQL screener — <Candidate name> — <date>
Result: PASS | NOT PASS
Time: <mm:ss> total (Exercise 1 <mm:ss>, Exercise 2 <mm:ss>)

Exercise 1 (count with a filter): OK / not OK — <one line, plain language>
Exercise 2 (join two tables, filter by text, sort): OK / not OK — <one line>

Their queries
Ex 1: <verbatim SQL>
Ex 2: <verbatim SQL>

Flag: <only if something warrants it — otherwise leave this line out>
```

Plain language in those two lines, no SQL vocabulary the recruiter cannot
defend in a conversation: "joined the two tables but never filtered by area, so
it returned all 40 candidates" — not "missing predicate on the dimension".

Quote their SQL verbatim and nowhere else. Never rewrite it, never correct it
silently, never add the right answer to the note — the note travels, and the
answer key does not.

## Flags worth raising (and how)

State the observation, not the accusation. One line each, and only when the
transcript shows it:

- a first query that arrives perfect after a long silence, formatted unlike
  anything else they typed;
- no queries run at all for an exercise, with something left in the editor
  (usually: ran out of time);
- the candidate said they had never used SQL;
- the session was dictated over screen share because the link would not open —
  then typing and typos are not theirs.

## After the note

Paste it into the candidate's record in Manatal. On a PASS, pass the raw
transcript along with it to the technical interviewer — they want the original
queries, not the summary.
