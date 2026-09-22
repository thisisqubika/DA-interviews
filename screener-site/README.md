# Qubika SQL Screener — the deployed site

The page the recruiting team's candidates open. One static folder, deployed
**once**; every candidate gets their own link to the same page, and the link
carries who the session is for and when it dies.

**Live at https://qubika-sql-screener.screener-site.workers.dev** — a
Cloudflare Worker that serves these files and nothing else.

```
screener-site/
├── wrangler.jsonc        deploy config (static assets, no Worker code)
└── public/
    ├── index.html        the whole app (statements, data, editor, engine glue)
    └── vendor/
        ├── sql-wasm.js   SQLite compiled to WebAssembly (sql.js 1.14.2)
        └── sql-wasm.wasm
```

No server, no database, no build step. SQL runs in the candidate's browser; the
site is plain files behind a CDN, and nothing about a session is ever sent
anywhere — the candidate copies their own transcript into the meeting chat.

## The session link

```
https://qubika-sql-screener.screener-site.workers.dev/?c=Maria%20Clara%20Zordan&id=mcz-0922-1530&x=2026-09-22T18:15:00Z
```

| Parameter | Meaning |
| --- | --- |
| `c` | Candidate's full name. Shown in the page header, stamped into the transcript. URL-encode the spaces (`%20` or `+`). |
| `id` | Session id — anything unique; it keys the "already finished" lock in that browser and appears in the transcript. Optional. |
| `x` | **Required.** When the link dies, as ISO 8601 **UTC** (the trailing `Z` matters). Recommended: 45 minutes from when the link is written. |

Without a valid `x` in the future the page refuses to open at all, so a
forgotten expiry fails loudly instead of leaving an exercise open forever.

`…workers.dev/?demo=1` is a practice link: 30 minutes from opening, marked
*practice* in the header and in the transcript so a rehearsal can never be
mistaken for a candidate's session.

## How a session dies

- **The candidate clicks Finish & copy session** — the exercises close
  immediately, and that browser comes back to the ended screen on reload.
- **The clock runs out** — at `x` the page closes itself mid-exercise. The
  transcript they already have stays copyable from the ended screen, so time
  running out never costs the evidence.
- Expiry is checked against **the host's clock**, read from the `Date` response
  header of a `HEAD` on the page itself, not the candidate's device. Winding the
  laptop clock back does not reopen a session.

What this design deliberately cannot do: revoke a live link before its expiry.
If a link leaks and it matters, redeploy the site under a different path — every
link in flight points at the old one and stops working. Keep expiries short
(45 minutes) and that is a once-a-year problem.

## Deploying

```bash
cd screener-site && npx wrangler deploy
```

That is the whole procedure, for the first deploy and every one after it. The
Worker has no code — `wrangler.jsonc` points at `public/` and Cloudflare serves
those files directly.

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
