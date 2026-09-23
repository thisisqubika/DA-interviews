// The only server code in the screener. Everything else — the exercises, the
// data, the SQLite engine — runs in the candidate's browser and is served as
// static assets by the binding below.
//
// Two routes, one job: when a candidate finishes, their transcript lands here
// so the recruiter never has to ask them for it. The session id is the whole
// security model — it is minted at random by the skill that writes the link,
// and it is the only thing standing between a transcript and anyone who guesses
// a URL. Ids shorter than 16 characters are refused for that reason.

const MAX_BYTES = 64 * 1024;   // a real session is a few KB; this is a ceiling
const TTL_SECONDS = 30 * 24 * 60 * 60;
const ID = /^[a-z0-9]{16,64}$/;

const text = (body, status, extra) => new Response(body, {
  status,
  headers: { "content-type": "text/plain; charset=utf-8", ...extra },
});

async function store(id, request, env){
  // Cheap rejection first, so an oversized body is never read into memory.
  if (Number(request.headers.get("content-length") || 0) > MAX_BYTES)
    return text("Transcript too large\n", 413);

  const body = await request.text();
  if (!body.trim()) return text("Empty transcript\n", 400);
  if (body.length > MAX_BYTES) return text("Transcript too large\n", 413);

  // First write wins. A session is finished once, so a second POST to the same
  // id is either a retry or someone trying to overwrite real evidence — and in
  // both cases the stored transcript is the one to keep.
  if (await env.SESSIONS.get(id) !== null)
    return text("A transcript is already stored for this session\n", 409);

  await env.SESSIONS.put(id, body, { expirationTtl: TTL_SECONDS });
  return text("Stored\n", 201);
}

async function read(id, env){
  const body = await env.SESSIONS.get(id);
  if (body === null)
    return text("No transcript for this session\n", 404);
  return text(body, 200, { "cache-control": "no-store" });
}

export default {
  async fetch(request, env){
    const { pathname } = new URL(request.url);
    const match = pathname.match(/^\/s\/([^/]+)\/?$/);

    if (match){
      const id = match[1];
      if (!ID.test(id)) return text("Not a valid session id\n", 400);
      if (request.method === "POST") return store(id, request, env);
      if (request.method === "GET")  return read(id, env);
      return text("Method not allowed\n", 405, { allow: "GET, POST" });
    }

    // Everything else is the page itself, served exactly as it was before this
    // Worker existed.
    return env.ASSETS.fetch(request);
  },
};
