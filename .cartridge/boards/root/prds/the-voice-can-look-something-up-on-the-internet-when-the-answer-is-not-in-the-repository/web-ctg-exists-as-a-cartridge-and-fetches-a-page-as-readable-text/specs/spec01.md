---
complexity: 3
footprint:
  - web.ctg
  - .cartridge/init.lua
---

# spec02 — web.ctg exists as a cartridge and fetches a page as readable text

A new TypeScript cartridge in `auth.ctg`'s shape, owning one capability:
reaching the network on purpose. `{op:"fetch", url}` returns
`{url, title, text, bytes, truncated}`. A URL whose host is outside the declared
allowlist, or whose scheme is not `http`/`https`, is refused **before any
request leaves the process**, and the refusal is returned to the caller.

Supersedes spec01, whose block 3 was inert (two AND-OR census guards that
`sh -eu` never enforced) and whose host filter rejected a case the spec itself
requires. Blocks 1 and 2 carry over; block 3 is rewritten; every row of the
evidence table was re-measured.

## Files

Exactly these paths are created or changed. Nothing else.

| Path | What it is |
| --- | --- |
| `web.ctg/cartridge.json` | manifest: events `web` and `tool.web`, settings `allow_hosts` and `max_bytes`, `commands` (`check`, `test`), `grant`, `listen` |
| `web.ctg/init.lua` | copy of `auth.ctg/init.lua` with the event list `{ "web", "tool.web" }` |
| `web.ctg/package.json` | copy of `auth.ctg/package.json` with `name: "@cartridge/web"` |
| `web.ctg/tsconfig.json` | byte copy of `auth.ctg/tsconfig.json` |
| `web.ctg/.gitignore` | byte copy of `auth.ctg/.gitignore` |
| `web.ctg/.cartridge/.gitignore` | byte copy of `auth.ctg/.cartridge/.gitignore` (the whitelist) |
| `web.ctg/README.md` | at least ten non-blank lines |
| `web.ctg/.cartridge/help.md` | the help page, non-empty |
| `web.ctg/src/wire.ts` | byte copy of `auth.ctg/src/wire.ts` |
| `web.ctg/src/web.ts` | the capability: allowlist guard, fetch, HTML → text |
| `web.ctg/src/main.ts` | `serve(wire, make)` — the `auth.ctg/src/main.ts:5` seam |
| `web.ctg/.cartridge/tests/integration/node.ts` | byte copy of `auth.ctg/.cartridge/tests/integration/node.ts` |
| `web.ctg/.cartridge/tests/integration/fetch.test.ts` | the suite, against `Bun.serve` on loopback |
| `.cartridge/init.lua` | one added line: `\t{ id = "web", path = "web.ctg" },` |

Submodule or plain directory: follow the PRD's "Open decision that does not
block this child", which records the recommendation and the reason. This spec
does not re-decide it; it only requires that whatever lands adds no
`.gitmodules` entry inside this footprint, no Cargo path dependency, no symlink
and no `../<sibling>.ctg` reference. `needs` is absent, and that is what makes
`just isolation` pass.

No runtime dependency and no `bun install`: Bun 1.3.14 on this machine ships
`fetch` and `HTMLRewriter` (`bun -e 'typeof HTMLRewriter'` → `function`), and
`HTMLRewriter.transform(string)` returns a `string` **synchronously** with the
handlers already run. `devDependencies` stay dev-only (`@types/bun`,
`typescript`) and there is no `bun.lock`, so `commands` declares `check` and
`test` and no `build`. Block 1 gates this: a `commands.build` carrying
`--frozen-lockfile` with no `web.ctg/bun.lock` beside it fails.

## The module contract the Verify blocks depend on

`web.ctg/src/web.ts` exports, by these exact names:

```ts
export const NOT_HTTP = "web reaches http and https only, not";
export const OFF_ALLOWLIST = "web may not reach the host";
export type WebConfig = { allow_hosts?: string[] | null; max_bytes?: number | null };
export type Page = { url: string; title: string; text: string; bytes: number; truncated: boolean };
export class Web {
  constructor(config?: WebConfig, deps?: { fetch?: typeof fetch });
  destination(url: string): URL;          // throws; the only gate
  fetch(url: string): Promise<Page>;      // calls destination() before this.f()
}
export function readable(html: string): { title: string; text: string };
```

- `destination` parses the URL, throws `` `web cannot read the URL: ${url}` `` on
  a parse failure, throws `` `${NOT_HTTP} ${scheme}: ${url}` `` when the protocol
  is neither `http:` nor `https:`, and throws
  `` `${OFF_ALLOWLIST} ${host}; allowed: ${list}` `` when the lowercased hostname
  is not an exact member of `allow_hosts`. Absent or empty `allow_hosts` reaches
  nothing. Match the host **exactly**: `sub.allowed.example` is not
  `allowed.example`, and block 2 drives that case.
- `fetch` calls `destination(url)` as its **first statement** and passes only
  `target.href` to the injected client, so no request can be made for a
  destination that was refused. A non-`ok` response throws
  `` `web got HTTP ${status} from ${href}` ``.
- `readable` drops `script`, `style`, `noscript`, `template` and `title`
  content, collects the title separately, inserts a newline at block elements,
  and returns collapsed text. `max_bytes` (default `2000000`) cuts `text` and
  sets `truncated`.

  One spelling trap, worth naming because it is easy to get wrong and block 2
  catches it: a `text(t) { t.remove(); }` handler on `script`/`style` does not
  keep that text out of a broad `*` text handler. Use an element-scoped drop
  counter (`element(e) { drop++; e.onEndTag(() => { drop--; }); }`) and skip
  text while `drop > 0`.

`web.ctg/src/main.ts` exports `serve(wire, make = config => new Web(config))`
and registers **only through `wire.on(name, handler)`** for `"apply"`, `"web"`
and `"tool.web"`. `apply` must call `make(config)` with the config the host
passed — block 2 re-applies a different `allow_hosts` and requires the change to
take effect, so a `serve` that ignores its argument fails. `tool.web` answers
`describe` with `{name, description, input_schema}`, `cancel` with
`{cancelled:false}`, and `call` by returning `{content: JSON.stringify(page)}` on
success and `{content: <the error message>, error: true}` on a refusal — a
refusal is a tool result the model sees, never a dropped call.

## Acceptance

- [x] `web.ctg/cartridge.json` declares `web` and `tool.web`, each with a `description` and a `schema` and each in `listen`; every setting has a `type` and a `doc`; `commands` declares `check` and `test`; `grant.exec` names `bun` and `grant.net` is a non-empty list that does not contain `*`.
- [x] `.cartridge/init.lua` has `{ id = "web", path = "web.ctg" }`, `web.ctg/README.md` has at least ten non-blank lines and `web.ctg/.cartridge/help.md` is non-empty — together the three things that make `cartridge help web` print a page and exit zero in a trusted checkout.
- [x] `{op:"fetch", url}` on an allowed `http`/`https` host returns the page as readable text with its URL, its title, a byte count and `truncated`, with script and style content and markup removed; `max_bytes` cuts the text and says so.
- [x] A host outside `allow_hosts`, a sub-domain of an allowed host, `file:`, `data:` and `ftp:` are each refused with an error naming the offending host or scheme, **and no request is made for any of them**; the refusal reaches the caller through `tool.web` as `{error: true}` carrying the reason; a re-applied `allow_hosts` takes effect.
- [x] `bun test ./web.ctg/.cartridge/tests/integration/fetch.test.ts` proves fetch and every refusal against a `Bun.serve` server on `127.0.0.1`, with at least six passing tests, no failures and at least twenty-five assertions, and no test names a host that is not loopback or a reserved documentation name.
- [x] `just audit web` and `just isolation` report nothing hard. (`just isolation` is composition-wide, so it covers the siblings; an all-cartridge `just audit` cannot run in a lane and is a post-merge check — see the block comment.)

## Verify and Proof

<!--
Engine facts (prd.ctg/.cartridge/templates/spec.md): each block runs as
`sh -eu -c`, 120 s, twice — first in the lane
`prd.ctg/.cartridge/boards/root/.lanes/<slug>`, then in `repo`. Paths are
relative to the repo root; no `cd` to an absolute checkout. No Rust is
compiled here, so no block needs CARGO_TARGET_DIR. No block writes inside
the footprint: block 3's only write is a log under TMPDIR, removed on both
the success and the failure path.

`sh -eu` TRAP, and the reason spec01's block 3 was inert: `set -e` is not
applied to any command of an AND-OR list except the last. So
`test -n "$n" && test "$n" -ge 6` NEVER fails the block — when `$n` is
empty the list short-circuits and the shell carries on. Measured:
`sh -eu -c 'n=""; test -n "$n" && test "$n" -ge 25; echo after=$?'` prints
`after=1` and the shell exits 0. Every census guard below is therefore one
statement per line. Same family as the recorded
`negated-grep-guards-are-inert-under-set-e` trap; no block here uses
`! grep`, and every alternation uses `grep -E`, never a BRE `\|`.

Measured in a superproject worktree of e8fc2ba with the submodule
directories empty (which is what a superproject lane looks like):
`just audit web` exits 0 (`audit: 1 of 1 cartridges pass the hard checks`,
the superproject's dirty files appearing only as soft `find:` lines) and
`just isolation` exits 0 (`isolation composition pass`). Both are safe here.

Three things are deliberately NOT in a block:
- `cartridge help web`. Measured in that same worktree: it exits 1 with
  "is in no trusted project; review it, then run `cartridge trust ...`",
  and the trust prompt never waits in a non-tty. Editing a manifest also
  untrusts the live project, so pass 2 is no safer. Acceptance box 2 gates
  the three facts that make the page exist instead. Run `cartridge help web`
  by hand in a trusted checkout after the merge.
- an all-cartridge `just audit`. In a lane every sibling directory is empty,
  so only `web.ctg` can be audited. `just isolation` IS composition-wide and
  does run here. Run `just audit` across all cartridges by hand after the
  merge; the pre-change baseline is 17 of 17.
- `just check web` / `just test web`. `.cartridge/justfile:100-101` hold
  hardcoded target lists that do not include `web`, and that file is outside
  this footprint. Block 3 calls `bun test` directly.

`bun test` path forms, measured on bun 1.3.14 in the live repo (spec01
asserted both of these wrongly, from piped output whose exit code was never
read): `bun test auth.ctg/.cartridge/tests/` — no leading `./` — matches
nothing and exits **1**, printing "Tests need \".test\"... in the filename".
`bun test ./auth.ctg/.cartridge/tests/` — leading `./`, a directory, no file
named — DOES descend the dotdir: 15 pass across 3 files, exit 0. Block 3
names the file, which is narrower and also gates that this file exists.
-->

### Block 1 — the declaration, the profile, the documentation and the gates

```sh
test -f web.ctg/cartridge.json
test -f web.ctg/init.lua
test -f web.ctg/src/main.ts
test -f web.ctg/src/web.ts
test -s web.ctg/.cartridge/help.md
test "$(awk 'NF' web.ctg/README.md | wc -l | tr -d ' ')" -ge 10
grep -qn 'id = "web", path = "web.ctg"' .cartridge/init.lua
bun -e '
  const m = JSON.parse(require("node:fs").readFileSync("web.ctg/cartridge.json", "utf8"));
  const bad = (why) => { console.error("manifest: " + why); process.exit(1); };
  if (!m.description) bad("no description");
  for (const name of ["web", "tool.web"]) {
    const e = (m.events || {})[name];
    if (!e) bad("no event " + name);
    if (!e.description || !e.schema) bad(name + " lacks a description or a schema");
    if (!(m.listen || []).includes(name)) bad(name + " is declared but not listened to");
  }
  const settings = m.settings || {};
  for (const [name, s] of Object.entries(settings)) if (!s || !s.type || !s.doc) bad("setting " + name + " lacks a type or a doc");
  if (!settings.allow_hosts) bad("no allow_hosts setting");
  const net = (m.grant || {}).net;
  if (!Array.isArray(net) || net.length === 0) bad("grant.net is empty");
  if (net.includes("*")) bad("grant.net contains *");
  if (!((m.grant || {}).exec || []).includes("bun")) bad("grant.exec does not name bun");
  const build = (m.commands || {}).build;
  const frozen = build && JSON.stringify(build.argv || []).includes("--frozen-lockfile");
  if (frozen && !require("node:fs").existsSync("web.ctg/bun.lock")) bad("commands.build installs --frozen-lockfile but the cartridge ships no bun.lock");
  for (const name of ["check", "test"]) if (!(m.commands || {})[name]) bad("commands declares no " + name);
'
just audit web
just isolation
```

### Block 2 — the behaviour: a page comes back readable, and nothing else is ever reached

This block greps for nothing. It imports the module, injects a client that
records every URL it is handed, and counts. A cartridge that declares
`allow_hosts` and never consults it is caught by the count; one that fetches but
drops the refusal path is caught by the refusals; one whose `apply` ignores the
host's config is caught by the re-apply at the end.

```sh
bun -e '
  const { Web } = await import("./web.ctg/src/web.ts");
  const bad = (why) => { console.error("web: " + why); process.exit(1); };
  const PAGE = "<!doctype html><html><head><title>PAGETITLE</title><style>b{color:red}STYLETEXT</style></head><body><h1>Heading</h1><p>BODYTEXT one</p><script>SCRIPTTEXT()</script><p>BODYTEXT two</p></body></html>";
  const reached = [];
  const client = async (url) => { reached.push(String(url)); return new Response(PAGE, { headers: { "content-type": "text/html" } }); };

  const web = new Web({ allow_hosts: ["allowed.example"] }, { fetch: client });
  const page = await web.fetch("https://allowed.example/p");
  if (reached.length !== 1) bad("one allowed fetch made " + reached.length + " requests");
  if (!String(page.url).includes("allowed.example")) bad("the returned url does not name the page fetched");
  if (page.title !== "PAGETITLE") bad("the title was not read: " + JSON.stringify(page.title));
  if (!page.text.includes("BODYTEXT one") || !page.text.includes("BODYTEXT two")) bad("the body text is missing from the readable text");
  if (page.text.includes("SCRIPTTEXT")) bad("script contents reached the caller");
  if (page.text.includes("STYLETEXT")) bad("style contents reached the caller");
  if (page.text.includes("<p>") || page.text.includes("</body>")) bad("markup reached the caller instead of readable text");
  if (typeof page.bytes !== "number" || page.bytes <= 0) bad("bytes is not a positive number");
  if (page.truncated !== false) bad("a short page reported itself truncated");

  const cut = new Web({ allow_hosts: ["allowed.example"], max_bytes: 12 }, { fetch: client });
  const short = await cut.fetch("https://allowed.example/p");
  if (short.truncated !== true || short.text.length !== 12) bad("max_bytes is declared but does not cut the text");

  const before = reached.length;
  const refusals = [
    ["https://denied.example/p", "denied.example"],
    ["http://sub.allowed.example/p", "sub.allowed.example"],
    ["file:///etc/passwd", "file"],
    ["data:text/html,<p>x</p>", "data"],
    ["ftp://allowed.example/p", "ftp"],
  ];
  for (const [url, named] of refusals) {
    let message = null;
    try { await web.fetch(url); } catch (error) { message = String(error && error.message || error); }
    if (message === null) bad("fetching " + url + " was not refused");
    if (!message.includes(named)) bad("the refusal of " + url + " does not name " + named + ": " + message);
  }
  if (reached.length !== before) bad((reached.length - before) + " request(s) left the process for a destination that had to be refused: " + JSON.stringify(reached.slice(before)));

  const nowhere = new Web({}, { fetch: client });
  let empty = null;
  try { await nowhere.fetch("https://allowed.example/p"); } catch (error) { empty = String(error.message); }
  if (empty === null) bad("a cartridge with no allow_hosts still reached the network");
  if (reached.length !== before) bad("a request left the process with no allow_hosts configured");

  const { serve } = await import("./web.ctg/src/main.ts");
  const handlers = new Map();
  let built = 0;
  serve({ on: (n, h) => handlers.set(n, h) }, (config) => { built++; return new Web(config, { fetch: client }); });
  await handlers.get("apply")({ allow_hosts: ["allowed.example"] });
  if (built !== 1) bad("apply did not build the capability from the config the host passed");
  const ctx = { session: "s", run: "r", call: "c", cwd: "." };
  const ok = await handlers.get("tool.web")({ op: "call", context: ctx, input: { op: "fetch", url: "https://allowed.example/p" } });
  if (ok.error) bad("an allowed fetch came back as a tool error: " + ok.content);
  if (!String(ok.content).includes("BODYTEXT one")) bad("the tool result does not carry the page text");
  const no = await handlers.get("tool.web")({ op: "call", context: ctx, input: { op: "fetch", url: "https://denied.example/p" } });
  if (no.error !== true) bad("a refused fetch did not come back to the caller as an error result");
  if (!String(no.content).includes("denied.example")) bad("the refusal returned to the caller does not name the host: " + no.content);
  await handlers.get("apply")({ allow_hosts: ["second.example"] });
  const moved = await handlers.get("tool.web")({ op: "call", context: ctx, input: { op: "fetch", url: "https://allowed.example/p" } });
  if (moved.error !== true) bad("a re-applied allow_hosts did not take effect: the old host is still reachable");
  const now = await handlers.get("tool.web")({ op: "call", context: ctx, input: { op: "fetch", url: "https://second.example/p" } });
  if (now.error) bad("a re-applied allow_hosts did not take effect: the new host is refused: " + now.content);
  console.log("web: fetch and every refusal behave as specified");
'
```

### Block 3 — the cartridge's own suite runs against a local server and asserts something

The pass census, the failure census and the assertion census are each pinned on
their own line, because `bun test` prints no test names on success and omits the
`expect() calls` line entirely when there are no assertions — six empty bodies
would otherwise walk straight through.

```sh
log="${TMPDIR:-/tmp}/web-ctg-bun-test.$$.log"
bun test ./web.ctg/.cartridge/tests/integration/fetch.test.ts >"$log" 2>&1 || { cat "$log"; rm -f "$log"; exit 1; }
cat "$log"
pass=$(sed -n 's/^ *\([0-9][0-9]*\) pass$/\1/p' "$log" | head -1)
fail=$(sed -n 's/^ *\([0-9][0-9]*\) fail$/\1/p' "$log" | head -1)
checks=$(sed -n 's/^ *\([0-9][0-9]*\) expect() calls$/\1/p' "$log" | head -1)
rm -f "$log"
test -n "$pass"
test "$pass" -ge 6
test -n "$fail"
test "$fail" -eq 0
test -n "$checks"
test "$checks" -ge 25
grep -qn 'Bun.serve' web.ctg/.cartridge/tests/integration/fetch.test.ts
grep -qn '127.0.0.1' web.ctg/.cartridge/tests/integration/fetch.test.ts
grep -qn 'OFF_ALLOWLIST' web.ctg/.cartridge/tests/integration/fetch.test.ts
grep -qn 'NOT_HTTP' web.ctg/.cartridge/tests/integration/fetch.test.ts
for title in \
  "a page from an allowed host comes back as readable text" \
  "a host outside the allowlist is refused before any request is made" \
  "a scheme that is not http or https is refused before any request is made" \
  "the tool envelope returns a refusal to the caller instead of throwing it away"
do
  grep -qnF "$title" web.ctg/.cartridge/tests/integration/fetch.test.ts
done
if grep -rhoE 'https?://[a-zA-Z0-9.-]+' web.ctg/.cartridge/tests/ \
   | grep -vE '://(127\.0\.0\.1|localhost|([a-z0-9-]+\.)+(example|test|invalid)|(.+\.)?example\.(com|org|net))$' \
   | grep -q .; then
  echo "a test names a host that is neither loopback nor a reserved documentation name" >&2
  exit 1
fi
```

The reserved-host alternative is `([a-z0-9-]+\.)+(example|test|invalid)$`, with
the `+` on the label group. spec01 had a single `[a-z0-9-]+\.`, which admits one
label only and so flagged `sub.allowed.example` — the very sub-domain case
Acceptance box 4 requires and block 2 drives. A correct implementation could not
pass it.

## The suite block 3 requires

`web.ctg/.cartridge/tests/integration/fetch.test.ts` holds at least these six
tests, with exactly these titles (block 3 pins four of them), and at least
twenty-five `expect()` calls across them:

1. `a page from an allowed host comes back as readable text` — a `Bun.serve` on
   `127.0.0.1:0`, a real `Web` with `allow_hosts: ["127.0.0.1"]`, asserting the
   title, both paragraphs, the absence of the script and style text and of
   `<p>`, and that the server saw exactly one request.
2. `a host outside the allowlist is refused before any request is made` — an
   injected client that counts calls; the error names the host and the count is
   zero.
3. `a scheme that is not http or https is refused before any request is made` —
   `file:`, `data:` and `ftp:`, the count still zero.
4. `an empty allowlist reaches nothing at all`.
5. `an upstream status is reported, and a long page is cut and says so` — a 404
   path on the local server and a `max_bytes` of 10.
6. `the tool envelope returns a refusal to the caller instead of throwing it away`
   — a real `Wire` over a `PassThrough` pair driven by the copied `node.ts`,
   proving `describe`, an allowed `call`, and a refused `call` coming back as
   `{error: true}` naming the host.

The reference suite for this spec scores `6 pass, 0 fail, 29 expect() calls`.

## What was measured, on HEAD e8fc2ba

A reference implementation of this spec was built in a detached superproject
worktree with the submodule directories empty, alongside six wrong versions.
Every one of the three blocks was run as `sh -eu` in each tree — 21 block runs,
every cell below observed, none inferred:

| Tree | Block 1 | Block 2 | Block 3 |
| --- | --- | --- | --- |
| the change absent (clean worktree) | 1 | 1 | 1 |
| (a) declares `allow_hosts`, never checks it | 0 | **1** | **1** |
| (b) fetches, refusal path removed | 0 | **1** | **1** |
| (c) `Web.fetch` a stub, six empty test bodies | 0 | **1** | **1** |
| (d) reference `src/`, hollow suite (6 empty tests, 0 assertions) | 0 | 0 | **1** |
| (e) `serve`'s `apply` ignores the host's config | 0 | **1** | 0 |
| (f) `commands.build` with `--frozen-lockfile`, no `bun.lock` | **1** | 0 | 0 |
| the reference implementation | 0 | 0 | 0 |

Every wrong version is caught by at least one block, and the reference passes
all three. Rows (a)–(d) were reproduced by the round-1 reviewer from its own
independently built trees; (e) and (f) are this round's additions for the two
gaps the review named.

Block 1 is a declaration gate: it fails the absent change and (f), and passes a
stub by design. Block 2 is the behaviour gate — it caught every `src/` cheat
tried by both the analyst and the reviewer, including a genuine `HTMLRewriter`
defect the reviewer wrote by accident. Block 3 is the suite gate, and (d) is the
row it exists for. Do not weaken block 2 into greps: every wrong version above
contains the strings `allow_hosts`, `NOT_HTTP` and `OFF_ALLOWLIST`, so every
grep for them passes.
