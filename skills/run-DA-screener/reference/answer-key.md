# Answer key — Qubika SQL Screener

Interviewer-only. Never paste any of this into the meeting chat, never read a
solution out loud, and never share this file with a candidate. The platform
page itself contains no solutions, so nothing here can leak through it.

## The dataset (identical in every session)

```sql
CREATE TABLE job_openings (id INTEGER, title VARCHAR, area VARCHAR, opened_date DATE);
CREATE TABLE candidates  (id INTEGER, opening_id INTEGER, full_name VARCHAR,
                          applied_date DATE, stage VARCHAR, expected_salary_usd INTEGER);
```

- 8 openings, 40 candidates, no orphan `opening_id`.
- `area` values: `Data` (3 openings), `Engineering` (2), `Design`, `QA`,
  `Marketing` (1 each).
- `stage` values and counts: `applied` 11, `screening` 7, `rejected` 7,
  `interview` 6, `hired` 6, `offer` 3.
- Two candidates have `expected_salary_usd` NULL (ids 9 and 30). Id 9 is in the
  Data area, so a NULL shows up in the Exercise 2 result — that is expected,
  not a mistake by the candidate.
- The engine is SQLite (sql.js) running in the candidate's browser. String
  comparison with `=` is case-sensitive; `LIKE` is not.

## Exercise 1 — count with a filter

**Statement given to the candidate:** how many candidates are in `hired` stage.
Return a single number.

**Reference solution**

```sql
SELECT COUNT(*) AS hired_candidates
FROM candidates
WHERE stage = 'hired';
```

**Correct answer: 6.**

Accept as fully correct: `COUNT(1)`, `COUNT(id)`, with or without an alias, any
keyword casing, `stage IN ('hired')`, `stage LIKE 'hired'`, or a `GROUP BY
stage HAVING stage = 'hired'` that returns the single row `6` (clumsy, still
right — mention the clumsiness in the note, do not fail it).

Diagnostic wrong results:

| Result | What they wrote | How to read it | Cost |
| --- | --- | --- | --- |
| `40` | `HAVING stage = 'hired'` with no `GROUP BY`, or no filter at all | The HAVING/WHERE confusion. SQLite does not error here — it silently ignores the condition, so they may believe they are right. The strongest signal to capture. | −3 |
| 6 rows, one per stage | `GROUP BY stage` with no filter | Knows aggregation, did not read "in hired stage". | −3 |
| `0` | `stage = 'Hired'` or `'HIRED'` | Case. Small slip, but the number is wrong. | −3 |
| error `no such column` | typo, or quoting `hired` with double quotes (`"hired"` is an identifier in SQLite) | Normal; what matters is whether they read the error and fixed it. | 0 if they fixed it — otherwise the last result is what costs |

## Exercise 2 — join + string filter + sort

**Statement given to the candidate:** `full_name`, `applied_date` and
`expected_salary_usd` of every candidate who applied to an opening in the
`Data` area, sorted by application date, most recent first.

**Reference solution**

```sql
SELECT c.full_name, c.applied_date, c.expected_salary_usd
FROM candidates c
JOIN job_openings o ON o.id = c.opening_id
WHERE o.area = 'Data'
ORDER BY c.applied_date DESC;
```

**Correct answer: exactly these 12 rows, in this order.**

```
Tomás Ibáñez        2026-04-10  3500
Ana Beatriz Souza   2026-04-02  3800
Renata Lima         2026-03-21  NULL
Diego Castro        2026-03-18  3600
Nicolás Vieira      2026-03-09  3000
Valentina Rossi     2026-03-05  2900
Sofía Martínez      2026-02-20  3200
Joaquín Pereira     2026-02-11  2300
Pablo Almeida       2026-02-06  3400
Camila Duarte       2026-02-02  2750
Mateo Rodríguez     2026-01-18  2400
Lucía Fernández     2026-01-15  2600
```

Accept as fully correct: `INNER JOIN`, `LEFT JOIN` (same 12 rows here), a comma
join with the join condition in `WHERE` (`FROM candidates c, job_openings o
WHERE o.id = c.opening_id AND o.area = 'Data'`), `JOIN ... USING (…)` variants
that work, a subquery (`WHERE opening_id IN (SELECT id FROM job_openings WHERE
area = 'Data')`), any table aliasing, `LIKE 'Data'`, and extra columns beyond
the three asked for (note it as sloppiness, not an error).

Diagnostic wrong results:

| Result | What they wrote | How to read it | Cost |
| --- | --- | --- | --- |
| 120 or 320 rows | comma join with no join condition, or `CROSS JOIN` | Cartesian product. The most serious miss on this exercise — they do not have the join model. | −3 |
| 40 rows | joined but never filtered | Did not apply the `Data` filter. | −3 |
| 0 rows | `area = 'data'` / `'DATA'`, or filtered on `title = 'Data'` | Case, or filtered the wrong column. Watch whether they diagnose it. | −3 |
| 12 rows, oldest first | `ORDER BY applied_date` (no `DESC`) | Read the sort direction wrong. The rows are right. | −0.5 |
| 12 rows, unsorted | no `ORDER BY` | Ignored the last line of the statement. The rows are right. | −0.5 |
| error `a GROUP BY clause is required before HAVING` | filtered with `HAVING` | The confusion this screener is built to surface. Record it verbatim. | 0 if they fixed it — otherwise the last result is what costs |
| 3 rows / opening-level rows | grouped by opening | Misread the grain of the question. | −3 |

## Turning this into the score

The screener tests whether someone can write a filter and a join at all, not
whether they write elegant SQL. Right data by a clumsy path scores full marks;
wrong data with beautiful syntax does not. Style, aliasing and readability are
colour for the note, never a reason to take points off — and never a reason to
give them back to someone whose numbers are wrong.

Only the **last result of each exercise** counts. The attempts before it are
what the note describes, not what it scores: the `Cost` columns above apply to
where the candidate ended up, not to every wrong turn on the way. A candidate
who returned 40, saw it, and fixed it to 6 scored on the 6.

Start at 10, subtract the costs above, and the bar is 8 — so a detail slip still
clears and a wrong result does not. `reference/screener-note.md` has the full
rubric, the sanity checks and the note format.
