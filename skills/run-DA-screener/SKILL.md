---
name: run-DA-screener
description: >
  This skill should be used when a recruiter runs the short SQL screener with a
  candidate, before the technical interview — e.g. "run the SQL screener",
  "start the SQL test for this candidate", "give me the SQL exercises link",
  "the candidate finished, here is the transcript", "how did they do in the SQL
  test", "write the screener note", "kill the screener link", "corré el
  screener de SQL", "pasame el link de los ejercicios de SQL", "ya terminó, acá
  está el resultado", "roda o screener de SQL". It writes a link for that one
  candidate that expires by itself, hands over the exact words to say, and
  turns the session transcript into a PASS / NOT PASS note for the ATS.
  Everything happens in this chat — no terminal, no installs.
metadata:
  version: "0.5.0"
---

# Qubika SQL Screener

A **5-minute** SQL check the **recruiting team** runs during their screening
call, before the candidate reaches a technical interview. Two exercises: a
count with a filter, and a join between two tables filtered by a text value.
It answers one question — *can this person write basic SQL themselves?* — and
the answer is binary.

The people using this skill are not technical. Give them words they can say and
paste, never SQL to type or judge. You do the judging.

**Keep your replies short.** A recruiter is reading you mid-call with a
candidate waiting: hand over the link and the one-line message, not a briefing.
Everything below is what you need to know, not what you need to say.

## One candidate, one link, and it expires

The exercises live at one address that is always up. What is per-candidate is
the **link**: it carries their name and the moment it dies. Past that moment the
page refuses to open, and if the time runs out mid-exercise it closes itself.
Nothing is published, shared or deleted per session — you write a URL, and the
URL stops working by itself.

That is also why two recruiters can screen two people at the same time: two
links, two expiries, no shared state.

Rules that are not negotiable:

- **Never** send a link without an expiry, and never reuse an expiry from an
  earlier session. Every candidate gets a freshly written link.
- **Never** send the practice link
  (`https://qubika-sql-screener.screener-site.workers.dev/?demo=1`) to a
  candidate — it is for rehearsing, and its transcript is stamped PRACTICE.
- Keep the window short: **45 minutes** from when you write the link. It is a
  5-minute exercise inside a 30-minute call.

## 1. Write the session link

The exercises live at:

```
SCREENER_HOST = https://qubika-sql-screener.screener-site.workers.dev
```

That address never changes and is the only one to use. Never invent a URL: if
the page does not load for the candidate, run the call on screen share (see
*When something goes wrong*) rather than sending them somewhere else.

1. Ask for the **candidate's full name** if it has not been given.
2. Work out the expiry: **the current time in UTC, plus 45 minutes**, written
   ISO 8601 with the trailing `Z` (`2026-09-22T18:15:00Z`). Getting the
   timezone wrong is the one mistake that matters here, so also tell the
   recruiter the expiry in their own local time — "this link stops working at
   15:15 your time" — which is how they will notice if it is off.
3. Build the link:

   ```
   https://qubika-sql-screener.screener-site.workers.dev/?c=Maria%20Clara%20Zordan&id=mcz-0922-1530&x=2026-09-22T18:15:00Z
   ```

   `c` is the name with spaces encoded as `%20`, `id` is any short unique
   string (initials plus the date and time works), `x` is the expiry. The name
   is shown in the page header and stamped into the transcript, so the recruiter
   never has to ask the candidate to type it.
4. Hand it over with the chat message below, and say when it dies.

## 2. Hand it over

Give the recruiter the message to paste in the meeting chat — one line, in the
language of the call, nothing else around it:

> **EN** — Two short SQL exercises, 5 minutes: [link] — share your screen while
> you work.

> **ES** — Dos ejercicios cortos de SQL, 5 minutos: [link] — compartí pantalla
> mientras los hacés.

> **PT** — Dois exercícios curtos de SQL, 5 minutos: [link] — compartilhe a tela
> enquanto trabalha.

Add one line of your own, not more: when the link expires, in their local time.

## 3. During the call

Only say these if the recruiter asks how to run it:

- Ask for screen sharing before the first query — it is what makes the result
  mean something.
- Explain in two sentences and start: statement and tables on the left, query on
  the right, press Run, five minutes for both. The page shows the elapsed time.
- Stay quiet while they type. Let wrong queries run; the candidate reading their
  own error is what this measures.
- Allowed nudges: "take your time", "read the statement again", "what does that
  error say?", "what would you try next?". Never a SQL keyword the statement
  does not already contain, never a hint from the answer key, and never a
  verdict during the call.
- At ~2 minutes on Exercise 1, move to Exercise 2 anyway. At 5 minutes, stop.
- Google for syntax is fine; an AI writing the query is not.

## 4. Close the session

1. The candidate clicks **Finish & copy session** (top right), confirms, and
   pastes the text into the meeting chat. That click closes the exercises on
   their side: Run stops working and a reload comes back to the same "Session
   ended" screen.
2. The recruiter pastes that text here.
3. Nothing has to be shut down. The link dies at its expiry whether or not
   anyone remembers it, and a candidate who kept the URL finds a dead page.
4. If the recruiter has no transcript to paste (the candidate closed the tab,
   the copy failed), write the note from what they saw and say in it that the
   evidence was partial.

A link cannot be revoked early — that is the trade for having no server. If one
leaks to somewhere it should not be, or a candidate is caught passing it
around, tell the Data Studio: redeploying the site at a different path kills
every link in flight at once.

The transcript starts with `=== QUBIKA SQL SCREENER — SESSION TRANSCRIPT v1 ===`
and contains every query they ran, the result summary, the errors and the
timings. Nothing in it is private to the candidate beyond what they typed.

## 5. Write the verdict

1. Read `reference/answer-key.md` — the dataset, both reference solutions, the
   correct results, the variants that are equally correct, and what each wrong
   result tells you. Judge the **data returned**, not the SQL style, and only
   the **last result of each exercise**.
2. Read `reference/screener-note.md` — the PASS / NOT PASS rule and the note
   format. Both exercises right is a PASS; anything else is a NOT PASS. Do not
   invent middle grades, percentages or "almost".
3. Write the note in the recruiter's language (English by default; Spanish or
   Portuguese if they are writing in one of those). Short: the verdict, the
   times, one plain-language line per exercise, their queries verbatim.
4. Tell them where it goes: the candidate's record in Manatal, and — on a PASS
   — the raw transcript in the handoff to the technical interviewer.

If the recruiter asks what the right answer was, tell **them** — the answer key
is theirs to read. Add one line reminding them it never goes to a candidate,
and never into the meeting chat.

## When something goes wrong

- **"This link is not valid any more"** — the expiry has passed (or the link
  lost part of itself on the way through the chat, which drops the `x=`).
  Write a new link and resend it; never reuse the old one.
- **The time ran out mid-exercise** — the page closes but the candidate can
  still copy their session text from the ended screen. Take the transcript,
  then decide with the recruiter whether the interruption was theirs or ours: a
  link written with too short a window is our mistake, and they get a new one.
- **"The page is stuck loading" / "the SQL engine could not start"** — the
  exercise engine is served with the page. Reload once; if it still fails, try
  another browser (Chrome or Edge), or a network without a corporate proxy.
  Their typed SQL is lost on reload, which at that point is one query.
- **The candidate clicked Finish by accident** — their session is closed for
  good. Write them a new link and note in the write-up that they restarted.
- **"Copy to clipboard" did nothing** — the box is selectable: select all, copy
  manually. Some browsers block clipboard access on a page they consider
  untrusted.
- **The candidate closed the tab before copying** — reopening the same link
  still offers **Show my session text again** for 90 minutes in that browser,
  as long as the link has not expired. Otherwise the text is gone: the page
  keeps nothing anywhere else, and neither does anyone else.
- **Only SELECT queries can be run here** — the page refuses anything that
  would change the data. That message means the candidate wrote something that
  is not a `SELECT`; it is not a fault of the page.

## Maintaining the platform (Data Studio, not recruiters)

The site is `screener-site/` in the qubika-livecoding repo: `public/index.html`
plus the SQLite engine in `public/vendor/`, served as static assets by a
Cloudflare Worker (`wrangler.jsonc`). Redeploying is one command from that
folder, `npx wrangler deploy`; `screener-site/README.md` has the details. SQL
runs in the candidate's own browser; there is no server code, no database and
nothing to keep running.

- The exercises, the seed data and the schema all live in `public/index.html`.
  Edit, redeploy, and update `reference/answer-key.md` in the same change — its
  expected results are what every verdict is measured against. Sessions already
  open keep the version they loaded.
- Keep the page free of solutions. The candidate can read its source.
- Expiry is enforced against the host's `Date` response header, so a candidate
  cannot reopen a session by changing their laptop clock. Finishing is also
  recorded in that browser's `localStorage` for 90 minutes, keyed by the link's
  session id, so a reload cannot resume a sent session; practice links are
  exempt, so a rehearsal can be repeated.
- There is no way to revoke a live link early; redeploying the site at a
  different path is the blunt instrument, and it invalidates every link in
  flight.
- This screener is deliberately a different dataset from the technical
  interview's exercises (`run-DA-livecoding`), so that passing it here does not
  preview that session.
