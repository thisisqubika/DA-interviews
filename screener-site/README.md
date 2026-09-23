# Qubika SQL Screener — the deployed site

The page the recruiting team's candidates open. One static folder, deployed
**once**; every candidate gets their own link to the same page, and the link
carries who the session is for and when it dies.

**Live at https://qubika-sql-screener.screener-site.workers.dev** — a
Cloudflare Worker that serves these files, plus two routes that carry a finished
session back to the interviewer.

```
screener-site/
├── wrangler.jsonc        deploy config (static assets + KV binding)
├── src/
│   └── index.js          the /s/<id> routes; everything else is the page
└── public/
    ├── index.html        the whole app (statements, data, editor, engine glue)
    └── vendor/
        ├── sql-wasm.js   SQLite compiled to WebAssembly (sql.js 1.14.2)
        └── sql-wasm.wasm
```

No database, no build step, and all the SQL still runs in the candidate's own
browser. Exactly one thing leaves it: when the candidate clicks Finish, the page
POSTs the transcript to `/s/<id>`, where it sits in Cloudflare KV for 30 days
so the interviewer can fetch it with `GET /s/<id>`. Nobody copies or pastes
anything unless that send fails.

## The transcript routes

| | |
| --- | --- |
| `POST /s/<id>` | Called by the page on Finish. Stores the transcript with a 30-day TTL. First write wins — a second POST to the same id returns 409 and the stored session is kept, so real evidence cannot be overwritten. Bodies over 64 KB are refused. |
| `GET /s/<id>` | Returns the transcript as `text/plain`, or 404 if nothing was stored. This is what the `run-DA-screener` skill fetches. |

Ids must be 16–64 lowercase letters and digits; anything else is refused with a
400. **The id is the entire access control** — there is no auth header to add,
because the retrieval has to work as a plain URL fetch. That is why the skill
mints it at random and why a readable id like `mcz-0922-1530` is not acceptable:
a guessable id is a transcript anyone can read for a day.

## The session link

```
https://qubika-sql-screener.screener-site.workers.dev/?c=Maria%20Clara%20Zordan&id=k7m2pq9x4vb1nz8t9wc3&x=2026-09-22T18:15:00Z
```

| Parameter | Meaning |
| --- | --- |
| `c` | Candidate's full name. Shown in the page header, stamped into the transcript. URL-encode the spaces (`%20` or `+`). |
| `id` | **Required in practice.** 16–64 random lowercase letters and digits. It keys the "already finished" lock in that browser, appears in the transcript, and is the address the finished session is stored at and fetched from. A link without one still works as an exercise, but the transcript has nowhere to go and the candidate is asked to paste it by hand. |
| `x` | **Required.** When the link dies, as ISO 8601 **UTC** (the trailing `Z` matters). Recommended: 45 minutes from when the link is written. |

Without a valid `x` in the future the page refuses to open at all, so a
forgotten expiry fails loudly instead of leaving an exercise open forever.

`…workers.dev/?demo=1` is a practice link: 30 minutes from opening, marked
*practice* in the header and in the transcript so a rehearsal can never be
mistaken for a candidate's session.

## How a session dies

- **The candidate clicks Finish** — the exercises close immediately, the
  transcript is sent, and that browser comes back to the ended screen on reload.
- **The clock runs out** — at `x` the page closes itself mid-exercise and sends
  the session as it stands, so time running out never costs the evidence.

Either way, if the send fails the page falls back to showing the candidate their
transcript and asking them to paste it in the meeting chat. That path is the
exception, not the normal flow, and the skill says so when it hits a 404.
- Expiry is checked against **the host's clock**, read from the `Date` response
  header of a `HEAD` on the page itself, not the candidate's device. Winding the
  laptop clock back does not reopen a session.

What this design deliberately cannot do: revoke a live link before its expiry.
If a link leaks and it matters, redeploy the site under a different path — every
link in flight points at the old one and stops working. Keep expiries short
(45 minutes) and that is a once-a-year problem.

## Deploying

Once, to create the store the transcripts live in:

```bash
npx wrangler kv namespace create SESSIONS
```

Put the id it prints into `kv_namespaces[0].id` in `wrangler.jsonc`, replacing
the placeholder. Until you do, the deploy fails — which is deliberate, because a
Worker deployed without its KV binding would accept sessions and lose them.

Then, for this deploy and every one after it:

```bash
cd screener-site && npx wrangler deploy
```

`wrangler.jsonc` points at `public/` for the static files and `src/index.js` for
the two routes; assets are matched first, so the Worker only ever sees `/s/<id>`.

Two things worth knowing if this ever moves:

- **`wrangler pages deploy` no longer works.** Current wrangler delegates Pages
  commands to Workers and fails without a config, printing a wall of output
  that looks like progress while creating nothing. This project is on Workers
  static assets, which is the supported path.
- **The hostname comes from the account's `workers.dev` subdomain**
  (`screener-site`), which is account-wide. Renaming it, or moving to a custom
  domain, changes the address in every link in flight — so it also means
  updating `SCREENER_HOST` in `skills/run-DA-screener/SKILL.md` and waiting a
  few minutes for a new certificate.

Cloudflare gets the three things right that a static host has to get right, and
they are worth re-checking on any other host: `.wasm` served as
`application/wasm` (S3 guesses wrong, and the engine then fails to start),
`index.html` served with `max-age=0, must-revalidate` so a redeploy reaches
people, and the `Date` response header left intact — it is the clock the expiry
trusts.

After deploying, open `https://qubika-sql-screener.screener-site.workers.dev/?demo=1`
once and check the engine starts and the tables show sample rows.

## Changing the exercises

`public/index.html` holds everything: the two statements in `EXERCISES`, the
seed rows in `OPENINGS` and `CANDIDATES`, the schema in `SCHEMA_SQL`. Edit,
redeploy (`npx wrangler deploy`), and
update `skills/run-DA-screener/reference/answer-key.md` in the same change — its
expected results are what every verdict is measured against. Sessions already
running keep the version they loaded.

The page contains no solutions, on purpose: a candidate can read its source.
