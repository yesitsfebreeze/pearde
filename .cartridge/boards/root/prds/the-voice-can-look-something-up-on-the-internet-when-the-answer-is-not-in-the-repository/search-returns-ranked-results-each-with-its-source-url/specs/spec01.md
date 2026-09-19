---
complexity: 2
footprint:
  - web.ctg/cartridge.json
  - web.ctg/src/web.ts
  - web.ctg/src/main.ts
  - web.ctg/README.md
  - web.ctg/.cartridge/help.md
  - web.ctg/.cartridge/tests/integration/search.test.ts
---

# spec01 — search returns ranked results, each with its source URL

`web.ctg` gains a second operation on the same tool. `{op:"search", query,
limit?}` calls the Brave Search API (`api.search.brave.com`) and returns
`{query, results:[{rank, title, url, snippet}]}`, Brave's ranked JSON used as
returned — no re-ranking, no scraping. The credential is one declared,
optional setting, `brave_api_key_env`, naming the environment variable that
holds the key; it arrives `null` when unset, and a search then reports an
error naming that setting rather than crashing, hanging, or answering with an
empty `results` list. A key Brave itself rejects (HTTP 401/403) is reported
the same way. `fetch` is untouched and keeps working with no key at all.

**`web.ctg` is a plain directory tracked in the superproject, not a git
submodule** (`git log -1 -- web.ctg`, `git ls-files web.ctg` both resolve
against the superproject's own history; there is no `.gitmodules` entry for
it). The footprint above lands as an ordinary commit in `repo`, with no
submodule pointer bump and no separate submodule commit.

## Files

Exactly these paths are changed. Nothing else.

| Path | What changes |
| --- | --- |
| `web.ctg/cartridge.json` | `web`'s schema gains `op:"search"`, `query`, `limit`; `tool.web`'s description gains search; a new setting `brave_api_key_env`; `grant.net` gains `api.search.brave.com`; a new `grant.env: ["WEB_*"]` |
| `web.ctg/src/web.ts` | `Web.search()`, `NO_SEARCH_KEY`, `SEARCH_KEY_REJECTED`, `KEY_NOT_GRANTED`, `BRAVE_SEARCH_URL`, `SearchResult`, `SearchResponse`; `Web`'s constructor gains `deps.env` and `deps.searchUrl`; `Web`'s injected-fetch type gains an `init` parameter so `search()` can send a header |
| `web.ctg/src/main.ts` | `DESCRIPTOR` and `run()` accept `op:"search"` alongside `op:"fetch"` |
| `web.ctg/README.md` | names the backend, the key setup, the new setting; stays ≥ 10 non-blank lines |
| `web.ctg/.cartridge/help.md` | names the backend, the setting, the new refusals; stays non-empty |
| `web.ctg/.cartridge/tests/integration/search.test.ts` | the new suite, against a `Bun.serve` standing in for Brave |

## Why the credential is a fixed `grant.env` prefix, not `${config.brave_api_key_env}`

**Correction (round 2, N1):** round 1 said `sessions.ctg`/`harness.ctg`
"already use that exact mechanism" (`${config.X}` in a grant) "for their own
per-operator env names." That is false, and self-contradicting one sentence
later where it calls the static prefix "the `sessions.ctg`/`harness.ctg`
shape" — no cartridge in this composition puts `${config.…}` in `grant.env`.
`harness.ctg` declares `grant.env: ["HARNESS_ROSTER_*"]` and its `roster`
setting must name a variable starting with that literal prefix;
`sessions.ctg` declares `grant.env: ["SESSIONS_MAILBOX_*"]` the same way; and
`live.ctg` grants a fixed exact name, `OPENAI_API_KEY`. `HARNESS_ROSTER_*` is
this spec's direct precedent, copied exactly: an optional, defaultable
setting names a variable that must start with a static `grant.env` prefix.

The host *can* expand a grant field from the setting that names it
(`cartridge.ctg/src/host/plan.rs`, `expand_grant`/`configured`), and that
mechanism is what was wrongly attributed to the two sibling cartridges above.
It does not fit here regardless: `configured()` resolves `${config.X}` by
calling `.as_str()` on the settled value and **errors the whole plan** when
that is not a string — `Err(Descriptor("need `${config.X}` names no string
setting"))` (`plan.rs:78-96`). `settings.txt` promises that an
`optional: true` key with `default: null` "arrives as null when unset", so a
`grant.env: ["${config.brave_api_key_env}"]` would make `web.ctg` **fail to
load at all** the moment the key is unset — the opposite of Acceptance box 2
("absent, ... `web.ctg` still loads and still fetches"). The one variant that
would technically work is `default: ""` plus
`grant.env: ["${config.brave_api_key_env}"]`, since `configured()` silently
skips an empty string (`plan.rs:91`) rather than erroring; it is rejected
because the user's answer on 2026-09-17 fixes `null`, not `""`, as the unset
value, and because it would grant exactly the one variable name the operator
chose, with no prefix discipline, unlike every existing precedent in this
composition.

So `grant.env` is `["WEB_*"]`, the `HARNESS_ROSTER_*`/`SESSIONS_MAILBOX_*`
shape, pinned exactly (round 2, B1 — see Block 1). `brave_api_key_env` is the
auth.ctg-shaped optional setting (`type: "string"`, `default: null`,
`optional: true`, one `doc` line) that names the variable, which must start
with `WEB_` or the base's environment-clearing spawn never hands it through.
This is read from the repository, not probed: `plan.rs`'s `configured` and
`expand_grant`, `process.rs`'s `granted_env`, `harness.ctg/cartridge.json`'s
`roster`/`HARNESS_ROSTER_*`, `sessions.ctg/cartridge.json`'s
`SESSIONS_MAILBOX_*`, `live.ctg/cartridge.json`'s `OPENAI_API_KEY`, and the
three settings on `auth.ctg/cartridge.json` (`credentials_dir`,
`router_data_dir`, `codex_home`), all as they stand on this HEAD.

`allow_hosts` is not touched by `search`: it is the fetch operation's gate on
a *caller-supplied* URL. Brave's endpoint is fixed by this cartridge, not by
a caller, so it does not go through `destination()`; its trust boundary is the
credential, not a host allowlist. This is a deliberate asymmetry, not an
oversight — noted so a reviewer does not look for `api.search.brave.com` in
`allow_hosts`'s default list and call it missing.

## The module contract the Verify blocks depend on

`web.ctg/src/web.ts` exports, in addition to the existing `NOT_HTTP`,
`OFF_ALLOWLIST`, `Web`, `Page`, `readable`:

```ts
export const NO_SEARCH_KEY: string;        // names `brave_api_key_env` in the string itself
export const SEARCH_KEY_REJECTED: string;  // names `brave_api_key_env` in the string itself
export const KEY_NOT_GRANTED: string;      // "does not start with `WEB_`..."; the caller prepends `brave_api_key_env` and the offending name
export const BRAVE_SEARCH_URL: string;     // "https://api.search.brave.com/res/v1/web/search"
export type SearchResult = { rank: number; title: string; url: string; snippet: string };
export type SearchResponse = { query: string; results: SearchResult[] };
export type WebConfig = { allow_hosts?: string[] | null; max_bytes?: number | null; brave_api_key_env?: string | null };

export class Web {
  constructor(config?: WebConfig, deps?: { fetch?: typeof fetch; env?: Record<string, string | undefined>; searchUrl?: string });
  search(query: string, limit?: number): Promise<SearchResponse>;
}
```

- `search` throws `NO_SEARCH_KEY` **before any request is made** when
  `brave_api_key_env` is null/absent, or when it names a variable not present
  in `deps.env` (default `process.env`) — zero requests reach `deps.fetch` in
  either case. When it names a variable **not starting with `WEB_`**, it
  throws `KEY_NOT_GRANTED`'s text instead (naming both `brave_api_key_env` and
  the offending name), also before any request — the base would never hand
  that value through regardless of whether the operator exported it (round 2,
  N3).
- Otherwise it calls `deps.fetch(url, { headers: { Accept: "application/json",
  "X-Subscription-Token": key } })` against `deps.searchUrl` (default
  `BRAVE_SEARCH_URL`), with `q` and, if given, a clamped `count` as query
  parameters.
- HTTP 401 or 403 throws `` `${SEARCH_KEY_REJECTED}: HTTP ${status}` `` —
  never a returned `{query, results: []}`.
- Any other non-`ok` status throws `` `web got HTTP ${status} from ${url}` ``,
  matching `fetch`'s own wording.
- On success it maps `body.web.results` (Brave's shape) to
  `{rank: index+1, title, url, snippet: description}`, in order, with no
  further parsing.

`web.ctg/src/main.ts`'s `run()` accepts `{op:"search", query, limit?}`
alongside `{op:"fetch", url}`, and its `DESCRIPTOR.input_schema` names both.
`tool.web`'s existing refusal envelope (`{content, error:true}`) is
unchanged and carries a search refusal the same way it already carries a
fetch refusal.

## Acceptance

- [x] `{op:"search", query}` returns `{query, results:[{rank,title,url,snippet}]}`, ranked in the order Brave returned them, each result carrying its `url`; the `web` event schema requires `query` for `op:"search"` and `url` for `op:"fetch"`, never both for every op, so the host does not refuse a well-formed search at the sender.
- [x] `brave_api_key_env` is one declared, optional setting (`type:"string"`, `default:null`, `optional:true`, a `doc` line); `grant.env` is exactly `["WEB_*"]`. With the setting null, naming a variable this process was not handed, or naming a variable outside the `WEB_` prefix, a search is refused **before any request is made**, with an error naming `brave_api_key_env`, and `web.ctg` still loads and `fetch` still works.
- [x] A rejected key (HTTP 401 or 403 from the backend) is reported as an error naming `brave_api_key_env`, never as a returned empty `results` list.
- [x] `bun test` (`fetch.test.ts` and the new `search.test.ts`) proves a recorded backend response, a backend rejection and both missing-credential paths against a `Bun.serve` standing in for Brave — no live network and no real key anywhere in the suite.
- [x] `README.md` and `.cartridge/help.md` name Brave as the backend, `api.search.brave.com` in `grant.net`, and how to supply the key (`brave_api_key_env`, a `WEB_`-prefixed variable).
- [x] `just audit web` and `just isolation` report nothing hard for it.

## Verify and Proof

<!--
Engine facts (prd.ctg/.cartridge/templates/spec.md): each block runs as
`sh -eu -c`, 120 s, twice — first with cwd = the lane
(`prd.ctg/.cartridge/boards/root/.lanes/<slug>`, a worktree of `repo`), then
with cwd = `repo`. Paths are relative to the repo root; no `cd` to an
absolute checkout. No Rust is compiled here, so no block needs
CARGO_TARGET_DIR. No block writes inside the footprint: block 3's only write
is a log under TMPDIR, removed on both the success and the failure path.

Since `web.ctg` is a plain tracked directory rather than a submodule, both
passes see the same, real content for every path this spec touches; only
*sibling* cartridges (real submodules) can be empty in the lane, which
affects only the two composition-wide commands at the end of block 1.
Measured directly, in a superproject worktree with the sibling submodule
directories empty (`git worktree add --detach`, matching how the
`web-ctg-exists-...` sibling spec measured its own lane): `just audit web`
exits 0 (`audit: 1 of 1 cartridges pass the hard checks`) and `just
isolation` exits 0 (`isolation composition pass`), both with the sibling
directories empty. Neither command is affected by this change; re-measured
current in round 2 (see "What was measured").

`bun test` TRAP, measured directly and not documented in the sibling spec: a
file argument that does not exist is **silently dropped**, not an error —
`bun test a.test.ts missing.test.ts` with `missing.test.ts` absent exits 0 and
runs only `a.test.ts`. Block 3 therefore asserts `test -f` on the new suite
file before running `bun test`, and separately pins the combined pass/expect
counts, so a tree that never adds the file cannot pass by omission.

Same `sh -eu` trap as the sibling spec's own note: every census line below is
one statement, because `test -n "$n" && test "$n" -ge 6` never fails under
`set -e` when `$n` is empty (the AND-list short-circuits and the shell
continues). No block here uses `! grep`; every alternation uses `grep -E`.
-->

### Block 1 — the declaration, the grants, the documentation

```sh
test -f web.ctg/cartridge.json
test -f web.ctg/src/web.ts
test -f web.ctg/src/main.ts
test -f web.ctg/.cartridge/tests/integration/search.test.ts
test -s web.ctg/.cartridge/help.md
test "$(awk 'NF' web.ctg/README.md | wc -l | tr -d ' ')" -ge 10
grep -qn 'api.search.brave.com' web.ctg/README.md
grep -qn 'brave_api_key_env' web.ctg/README.md
grep -qn 'brave_api_key_env' web.ctg/.cartridge/help.md
bun -e '
  const m = JSON.parse(require("node:fs").readFileSync("web.ctg/cartridge.json", "utf8"));
  const bad = (why) => { console.error("manifest: " + why); process.exit(1); };
  const web = (m.events || {}).web;
  if (!web || !web.description || !web.schema) bad("web event lacks a description or a schema");
  const op = ((web.schema.properties || {}).op || {});
  if (!(op.enum || []).includes("search")) bad("the web event op enum does not include search");
  if (!(op.enum || []).includes("fetch")) bad("the web event op enum does not include fetch");
  if ((web.schema.required || []).includes("url") || (web.schema.required || []).includes("query")) {
    bad("the web schema requires url or query for every op, so the host would refuse a search that has no url");
  }
  const when = (name) => (web.schema.allOf || []).find((b) => ((((b.if || {}).properties || {}).op || {}).const) === name);
  if (!((when("search") || {}).then || {}).required?.includes("query")) bad("op search does not require query");
  if (!((when("fetch") || {}).then || {}).required?.includes("url")) bad("op fetch does not require url");
  const settings = m.settings || {};
  for (const [name, s] of Object.entries(settings)) if (!s || !s.type || !s.doc) bad("setting " + name + " lacks a type or a doc");
  const key = settings.brave_api_key_env;
  if (!key) bad("no brave_api_key_env setting");
  if (key.type !== "string") bad("brave_api_key_env is not type string");
  if (key.default !== null) bad("brave_api_key_env does not default to null");
  if (key.optional !== true) bad("brave_api_key_env is not optional");
  const net = (m.grant || {}).net;
  if (!Array.isArray(net) || net.length === 0) bad("grant.net is empty");
  if (net.includes("*")) bad("grant.net contains *");
  if (!net.includes("api.search.brave.com")) bad("grant.net does not name api.search.brave.com");
  const env = (m.grant || {}).env || [];
  if (JSON.stringify(env) !== JSON.stringify(["WEB_*"])) bad("grant.env is not exactly [\"WEB_*\"]: " + JSON.stringify(env));
  if (!((m.grant || {}).exec || []).includes("bun")) bad("grant.exec does not name bun");
'
just audit web
just isolation
```

### Block 2 — the behaviour: ranked results with source URLs, and every credential path

This block runs no `grep`; it checks the error text itself, to bind the
messages to the credential's own vocabulary (`brave_api_key_env`, the
offending variable name) rather than to any exported constant a hollow
rewrite could keep by coincidence. It imports `Web` directly and injects
`env` and `searchUrl`, so no key and no network are real.

```sh
bun -e '
  const { Web } = await import("./web.ctg/src/web.ts");
  const bad = (why) => { console.error("web search: " + why); process.exit(1); };

  const BODY = { web: { results: [
    { title: "Kestrel", url: "https://source.example/kestrel", description: "A small falcon." },
    { title: "Common kestrel", url: "https://source.example/common-kestrel", description: "The most common kestrel." },
  ] } };
  const reached = [];
  let status = 200;
  const client = async (url, init) => {
    reached.push({ url: String(url), token: init && init.headers && init.headers["X-Subscription-Token"] });
    return new Response(JSON.stringify(BODY), { status, headers: { "content-type": "application/json" } });
  };

  const noKey = new Web({}, { fetch: client, env: {} });
  let message = null;
  try { await noKey.search("kestrel"); } catch (error) { message = String(error && error.message || error); }
  if (message === null) bad("a search with no brave_api_key_env setting was not refused");
  if (!message.includes("brave_api_key_env")) bad("the no-key refusal does not name brave_api_key_env: " + message);
  if (reached.length !== 0) bad("a request left the process with no key configured");

  const unset = new Web({ brave_api_key_env: "WEB_BRAVE_API_KEY" }, { fetch: client, env: {} });
  message = null;
  try { await unset.search("kestrel"); } catch (error) { message = String(error && error.message || error); }
  if (message === null) bad("a search whose named variable is unset was not refused");
  if (!message.includes("brave_api_key_env")) bad("the unset-variable refusal does not name brave_api_key_env: " + message);
  if (reached.length !== 0) bad("a request left the process with the key variable unset");

  const wrongPrefix = new Web({ brave_api_key_env: "BRAVE_API_KEY" }, { fetch: client, env: { BRAVE_API_KEY: "s3cr3t" } });
  message = null;
  try { await wrongPrefix.search("kestrel"); } catch (error) { message = String(error && error.message || error); }
  if (message === null) bad("a variable name outside WEB_ was not refused, though the base never grants it");
  if (!message.includes("brave_api_key_env")) bad("the wrong-prefix refusal does not name brave_api_key_env: " + message);
  if (!message.includes("BRAVE_API_KEY")) bad("the wrong-prefix refusal does not name the offending variable: " + message);
  if (reached.length !== 0) bad("a request left the process for a key the base would never have granted");

  const web = new Web({ brave_api_key_env: "WEB_BRAVE_API_KEY" }, { fetch: client, env: { WEB_BRAVE_API_KEY: "s3cr3t" } });
  const found = await web.search("kestrel", 5);
  if (found.query !== "kestrel") bad("the response does not carry the query back");
  if (!Array.isArray(found.results) || found.results.length !== 2) bad("the ranked results were not returned");
  if (found.results[0].rank !== 1 || found.results[1].rank !== 2) bad("results are not ranked in order");
  if (found.results[0].url !== "https://source.example/kestrel") bad("a result is missing its source URL");
  if (!found.results[0].title || !found.results[0].snippet) bad("a result is missing its title or snippet");
  if (reached.length !== 1) bad("a working search made " + reached.length + " requests, not one");
  if (reached[0].token !== "s3cr3t") bad("the key from the named variable was not sent as the credential");

  status = 401;
  const before = reached.length;
  let rejected = null, empty;
  try { empty = await web.search("kestrel"); } catch (error) { rejected = String(error && error.message || error); }
  if (empty !== undefined) bad("a rejected key came back as a result instead of an error: " + JSON.stringify(empty));
  if (rejected === null) bad("a 401 from the backend was not reported");
  if (!rejected.includes("brave_api_key_env")) bad("the rejected-key error does not name brave_api_key_env: " + rejected);
  if (reached.length !== before + 1) bad("the rejected-key case made an unexpected number of requests");
  status = 403;
  try { await web.search("kestrel"); bad("a 403 from the backend was not reported"); }
  catch (error) { if (!String(error.message).includes("brave_api_key_env")) bad("the 403 refusal does not name brave_api_key_env"); }

  console.log("web search: ranked results, source URLs, and every credential path behave as specified");
'
```

### Block 3 — the cartridge's own suite runs against a local server and asserts something

```sh
test -f web.ctg/.cartridge/tests/integration/search.test.ts
log="${TMPDIR:-/tmp}/web-ctg-search-test.$$.log"
bun test ./web.ctg/.cartridge/tests/integration/fetch.test.ts ./web.ctg/.cartridge/tests/integration/search.test.ts >"$log" 2>&1 || { cat "$log"; rm -f "$log"; exit 1; }
cat "$log"
pass=$(sed -n 's/^ *\([0-9][0-9]*\) pass$/\1/p' "$log" | head -1)
fail=$(sed -n 's/^ *\([0-9][0-9]*\) fail$/\1/p' "$log" | head -1)
checks=$(sed -n 's/^ *\([0-9][0-9]*\) expect() calls$/\1/p' "$log" | head -1)
rm -f "$log"
test -n "$pass"
test "$pass" -ge 12
test -n "$fail"
test "$fail" -eq 0
test -n "$checks"
test "$checks" -ge 60
grep -qn 'searchUrl' web.ctg/.cartridge/tests/integration/search.test.ts
grep -qn 'NO_SEARCH_KEY' web.ctg/.cartridge/tests/integration/search.test.ts
grep -qn 'SEARCH_KEY_REJECTED' web.ctg/.cartridge/tests/integration/search.test.ts
grep -qn 'KEY_NOT_GRANTED' web.ctg/.cartridge/tests/integration/search.test.ts
grep -qn 'Bun.serve' web.ctg/.cartridge/tests/integration/search.test.ts
for title in \
  "search returns ranked results, each carrying its source URL" \
  "no key configured is refused before any request is made" \
  "a rejected key is reported by name, and never as an empty result pretending success" \
  "a variable name outside the WEB_ prefix is refused with a sharper reason"
do
  grep -qnF "$title" web.ctg/.cartridge/tests/integration/search.test.ts
done
if grep -rhoE 'https?://[a-zA-Z0-9.-]+' web.ctg/.cartridge/tests/ \
   | grep -vE '://(127\.0\.0\.1|localhost|([a-z0-9-]+\.)+(example|test|invalid)|(.+\.)?example\.(com|org|net))$' \
   | grep -q .; then
  echo "a test names a host that is neither loopback nor a reserved documentation name" >&2
  exit 1
fi
```

## What was measured

**Round 1**, on HEAD `ccb4348`: a reference implementation was built in a
detached superproject worktree, alongside three deliberately wrong versions
of `src/web.ts`. Base failed all three blocks; the reference passed all
three (`11 pass, 0 fail, 71 expect() calls`); the three mutants passed block
1 (a declaration gate) and were each caught by blocks 2 and 3. Full detail
in round 1 of `review.md`. Round 1 review (independent agent, Opus 5) scored
84/100 and found two blocking gaps in block 1 itself, both in the manifest
half: **B1**, block 1's `grant.env` check accepted `["WEB"]`, `[""]` and
`["W*"]` — none of which the base's `granted_env` actually treats as
admitting `WEB_BRAVE_API_KEY` — and **B2**, nothing checked that the `web`
event schema's `required` still demanded `url` for every op, which would
make the host refuse `{op:"search", query}` at the sender before this
cartridge ever saw it. The review also found the round 1 rationale
misattributed the `${config.X}`-in-`grant.env` mechanism to `sessions.ctg`/
`harness.ctg` (corrected above), a `help.md`/`README.md` contradiction about
which of `allow_hosts`/`grant.net` is the subset, and two cheap gaps: no
sharper message when a named variable is outside the `WEB_` prefix, and a
stale HEAD in this section.

**Round 2**, re-measured on HEAD `ec2b1d6`
(`git diff --stat ccb4348 ec2b1d6 -- web.ctg` and `-- cartridge.ctg/src/host/plan.rs
cartridge.ctg/src/host/process.rs` are both empty, so nothing this spec
depends on moved): block 1 now pins `grant.env` to exactly `["WEB_*"]`
(the reviewer's measured line, used as given) and checks the `web` schema's
`required`/`allOf` shape directly; the reference gained the `KEY_NOT_GRANTED`
path (round 2, N3) and its own test; `help.md`/`README.md` were reconciled
(round 2, N2). Every block was re-run as `sh -eu` in fresh detached
superproject worktrees (sibling directories empty) against: the untouched
base, the reference, the same three `src/web.ts` mutants, and the reviewer's
four manifest-only mutants of the reference (M1–M4). 24 runs, all observed
directly, none inferred:

| Tree | Block 1 | Block 2 | Block 3 |
| --- | --- | --- | --- |
| base (the change absent) | 1 | 1 | 1 |
| (a) declares the setting, `search()` never checks it | 0 | **1** | **1** |
| (b) a rejected key returns `{results: []}` instead of throwing | 0 | **1** | **1** |
| (c) refusal messages exist but never name `brave_api_key_env` | 0 | **1** | **1** |
| M1: `events.web.schema.required = ["op", "url"]` | **1** | 0 | 0 |
| M2: `grant.env = ["WEB"]` | **1** | 0 | 0 |
| M3: `grant.env = [""]` | **1** | 0 | 0 |
| M4: `grant.env = ["W*"]` | **1** | 0 | 0 |
| the reference implementation | 0 | 0 | 0 |

(Exit codes; 0 = pass, bold = the wrong tree wrongly passed that block —
none does, now.) Block 1 is a declaration gate and does not run `Web.search`
at all, so (a)–(c) still pass it by design; M1–M4 are manifest-only and now
correctly **fail** it, closing B1 and B2. Block 2 is the behaviour gate: it
catches (a)–(c) by driving `Web.search` directly, and correctly passes
M1–M4, whose underlying `src/web.ts` is the untouched reference. Block 3 (the
cartridge's own suite) independently catches (a)–(c) the same way it did in
round 1, and also passes M1–M4 for the same reason as block 2 — a schema or
grant defect that the host would act on is invisible to a suite that never
goes through the host's own schema check, which is exactly why block 1 has
to be the one that catches it.

The reference suite for this spec: `12 pass, 0 fail, 75 expect() calls`
across `fetch.test.ts` (6/0/47, unchanged) and `search.test.ts` (6/0/28, one
test added for the `WEB_`-prefix check). Wall time for every block measured
under 1 s; `just audit`/`just isolation` together under 1 s. All comfortably
inside the 120 s per-block limit.

## Known ceiling of the gate

Per [[review-plan]]: a Verify block can prove a named test exists, runs, and
turns red on a deliberate mutation — it cannot prove the test died of the
behaviour rather than of something the test itself supplied, because the
judge (block 3's census) and the judged (the suite) run in the same process
family. Block 2 is this spec's answer to that: it drives `Web.search`
directly, independent of whatever `search.test.ts` happens to assert, so a
hollow suite padded with true assertions still fails block 2. That is the
same ceiling the `web-ctg-exists-...` sibling spec recorded and the same
answer it gave (an independent behaviour block), re-verified here rather than
re-argued. The diff reading remains the backstop for whether `search.test.ts`
itself is a good suite, not merely a passing one.
