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
  candidate that expires by itself, hands over the exact words to say, collects
  the finished session on its own, and scores it out of 10 as a note for the
  ATS. Everything happens in this chat — no terminal, no installs, and nothing
  for the recruiter to copy or paste.
metadata:
  version: "0.6.0"
---

# Qubika SQL Screener

A **5-minute** SQL check the **recruiting team** runs during their screening
call, before the candidate reaches a technical interview. Two exercises: a
count with a filter, and a join between two tables filtered by a text value.
It answers one question — *can this person write basic SQL themselves?* — as a
score out of 10, where 8 clears the bar.

The people using this skill are not technical. Give them words they can say and
paste, never SQL to type or judge. You do the judging.

**Keep your replies short.** A recruiter is reading you mid-call with a
candidate waiting. Everything below is what you need to know, not what you need
to say: hand over the link, and later the note, with nothing wrapped around
them. Do not explain what you just did, do not restate what the recruiter is
about to do, and never close with a summary of a thing they can already read.

## One candidate, one link, and it expires

The exercises live at one address that is always up. What is per-candidate is
the **link**: it carries their name and the moment it dies. Past that moment the
page refuses to open, and if the time runs out mid-exercise it closes itself.
Nothing is published or deleted per session — you write a URL, and the URL stops
working by itself.

That is also why two recruiters can screen two people at the same time: two
links, two expiries, two session ids, nothing shared between them.

Rules that are not negotiable:

- **Never** send a link without an expiry, and never reuse an expiry or a
  session id from an earlier session. Every candidate gets a freshly written
  link with a freshly minted random id.
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
   https://qubika-sql-screener.screener-site.workers.dev/?c=Maria%20Clara%20Zordan&id=k7m2pq9x4vb1nz8t9wc3&x=2026-09-22T18:15:00Z
   ```

   `c` is the name with spaces encoded as `%20`, `x` is the expiry, and `id` is
   the session id. The name is shown in the page header and stamped into the
   transcript, so the recruiter never has to ask the candidate to type it.

   **The id must be random, and it is built by a recipe, not by counting.**
   Write **five blocks of four** lowercase letters and digits, then join them:

   ```
   k7m2  pq9x  4vb1  nz8t  9wc3   →   k7m2pq9x4vb1nz8t9wc3
   ```

   Five blocks of four is twenty characters, which is comfortably inside the
   16–64 the site accepts. Never count the characters to check — counting is how
   this goes wrong. If a block comes out short or long, write the five blocks
   again from scratch. A short id is refused by the site at the moment the
   candidate finishes, when it is far too late to fix.

   The id carries no name, no initials and no date: it is what you fetch the
   finished session with in step 4, so a guessable id is a transcript anyone can
   read for a day.

   **Do all of this silently.** Never show the id to the recruiter, never
   mention that you are generating one, and never tell them you are writing it
   again — they are mid-call with a candidate waiting, and a message about an id
   being too short is noise about a thing they cannot act on. Keep it in the
   conversation for step 4 and say nothing about it.
4. Hand it over with the chat message below, and say when it dies.

## 2. Hand it over

**Give the link, bare.** What goes in the meeting chat is the URL on its own —
no sentence around it, no "two short SQL exercises", no instruction to share
their screen. The recruiter explains all of that out loud; a chat message that
repeats it is noise they have to read past mid-call.

Then one short line to the recruiter, not in the chat message: when the link
stops working, in their local time. That line is the safeguard against a
timezone mistake, so it stays — but it is the only thing you add.

Nothing else. Do not confirm how you spelled the candidate's name, do not offer
to regenerate the link, do not explain what the parameters mean, do not recap
what happens next. If the name is wrong they will tell you, and writing another
link takes one message.

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
- When they are done, ask them to click **Finish**, top right, and confirm.
  That is the last thing anyone has to do — the session comes to us by itself,
  and nobody is asked to copy or paste it.
- Google for syntax is fine; an AI writing the query is not.

## 4. Collect the session

1. The candidate clicks **Finish** (top right) and confirms. That closes the
   exercises on their side — Run stops working, a reload comes back to the same
   "Session ended" screen — and sends their session to us. They are not asked to
   copy or paste anything.
2. The recruiter tells you they are done.
3. Fetch the transcript yourself, from the session id you minted in step 1:

   ```
   https://qubika-sql-screener.screener-site.workers.dev/s/<id>
   ```

   It comes back as plain text, starting with
   `=== QUBIKA SQL SCREENER — SESSION TRANSCRIPT v1 ===`. Do not ask the
   recruiter for it, and do not ask them to ask the candidate — fetching it is
   your job, and the whole point is that nobody has to handle it.
4. Nothing has to be shut down. The link dies at its expiry whether or not
   anyone remembers it, and a candidate who kept the URL finds a dead page.
5. If the fetch comes back empty, see *When something goes wrong* — there is a
   fallback, and it is the only case where anyone pastes anything.

The transcript is kept for **30 days** and then deleted — long enough for the
handoff to the technical interviewer and for a note to be revisited during the
hiring loop, not long enough to become an archive. After that the note in
Manatal, with the queries quoted in it, is the record.

A link still cannot be revoked before its expiry. If one leaks to somewhere it
should not be, or a candidate is caught passing it around, tell the Data Studio:
redeploying the site at a different path kills every link in flight at once.

The transcript contains every query they ran, the result summary, the errors and
the timings. Nothing in it is private to the candidate beyond what they typed.

## 5. Score it and write the note

1. Read `reference/answer-key.md` — the dataset, both reference solutions, the
   correct results, the variants that are equally correct, and what each wrong
   result tells you. Judge the **data returned**, not the SQL style, and only
   the **last result of each exercise**.
2. Read `reference/screener-note.md` — the scoring rubric and the note format.
   Every session starts at 10; each defect has a fixed cost in that table; 8
   clears the bar. Apply the table as written. Do not invent a cost that is not
   in it, do not round a score to feel fairer, and do not reach for a number
   before you have named the defects.
3. Write the note in the recruiter's language (English by default; Spanish or
   Portuguese if they are writing in one of those). Short: the score, the times,
   one plain-language line per exercise, their queries verbatim.

**Give the note and stop.** The note is the whole answer. Nothing before it and
nothing after it — no paragraph on how the candidate worked, no reading of their
debugging, no observation about how much time they had left, no reminder to
paste it in Manatal, no reminder that the link expires by itself. All of that is
either already in the note or something the recruiter does not need said.

The note is also the only place any of it belongs: an assessment written in chat
instead of in the note is one that never reaches the candidate's record.

If the recruiter asks what the right answer was, tell **them** — the answer key
is theirs to read. Add one line reminding them it never goes to a candidate, and
never into the meeting chat.

## When something goes wrong

- **"This link is not valid any more"** — the expiry has passed (or the link
  lost part of itself on the way through the chat, which drops the `x=`).
  Write a new link and resend it; never reuse the old one.
- **The time ran out mid-exercise** — the page closes itself and sends the
  session as it stands, so the work is not lost. Fetch it as usual, then decide
  with the recruiter whether the interruption was theirs or ours: a link written
  with too short a window is our mistake, and they get a new one.
- **"The page is stuck loading" / "the SQL engine could not start"** — the
  exercise engine is served with the page. Reload once; if it still fails, try
  another browser (Chrome or Edge), or a network without a corporate proxy.
  Their typed SQL is lost on reload, which at that point is one query.
- **The candidate clicked Finish by accident** — their session is closed for
  good. Write them a new link and note in the write-up that they restarted.
- **The fetch comes back "No transcript for this session"** — either the
  candidate never clicked Finish, or the send was blocked on their network. In
  that case the page shows them the text and asks them to paste it in the
  meeting chat, so ask the recruiter for it. Check the id in the URL you are
  fetching matches the one you minted before concluding anything is wrong.
- **There is no text to paste either** — the candidate closed the tab before
  finishing. Reopening the same link still offers **Show my session text again**
  for 90 minutes in that browser, as long as the link has not expired.
  Otherwise the session is gone: write the note from what the recruiter saw and
  say in it that the evidence was partial.
- **"Copy to clipboard" did nothing** — only comes up on that fallback path.
  The box is selectable: select all, copy manually. Some browsers block
  clipboard access on a page they consider untrusted.
- **Only SELECT queries can be run here** — the page refuses anything that
  would change the data. That message means the candidate wrote something that
  is not a `SELECT`; it is not a fault of the page.

## Maintaining the platform (Data Studio, not recruiters)

The site is `screener-site/` in the qubika-livecoding repo: `public/index.html`
plus the SQLite engine in `public/vendor/`, served as static assets, and
`src/index.js`, a Worker that does one job. Redeploying is one command from that
folder, `npx wrangler deploy`; `screener-site/README.md` has the details. SQL
still runs entirely in the candidate's own browser — there is no database and
nothing to keep running.

- The exercises, the seed data and the schema all live in `public/index.html`.
  Edit, redeploy, and update `reference/answer-key.md` in the same change — its
  expected results are what every verdict is measured against. Sessions already
  open keep the version they loaded.
- Keep the page free of solutions. The candidate can read its source.
- The Worker has two routes, both under `/s/<id>`: the page POSTs the finished
  transcript to it, and a GET reads it back. Transcripts live in a Cloudflare KV
  namespace (`SESSIONS`) for 30 days and then delete themselves. A POST to an
  id that already has a transcript is refused, so a stored session can never be
  overwritten — which is also why a candidate who restarts needs a new link with
  a new id.
- The session id is the only thing protecting a transcript: the Worker refuses
  anything shorter than 16 characters, but it cannot tell a random id from a
  predictable one. That part is step 1's job, every time.
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
