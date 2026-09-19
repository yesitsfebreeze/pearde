---
complexity: 3
footprint:
  - web.ctg/.cartridge/.gitignore
  - web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md
  - .cartridge/tests/integration/web-tool-policy.test.ts
---

# spec01 — the agent picks the tool up for free, a system memo tells it to cite the source, and a real per-operation policy rule refuses it

Round 2, revising round 1 (reviewer score 78/100, B1–B3 blocking; see
`review.md`). No code changes. `agent.ctg`'s `needs: [..., "tool.*"]` already
resolves to every event with that prefix another enabled cartridge listens to
(`cartridge.ctg/docs/creating-cartridges.txt`, MANIFEST FIELDS), and
`web.ctg/cartridge.json` already `listen`s `tool.web` — so the tool is already
on the agent's list with zero edit to `agent.ctg`, `mcp.ctg` or `harness.ctg`.
`policy.ctg/init.lua`'s `evaluate()` already reads `request.input.op` and
applies `operations[tool][op]` ahead of the tool-level rule, so
`policy.operations.web = {fetch = "deny"}` already refuses only the fetch —
proven live below, composing the real `policy.ctg` with the real `web.ctg` in
a scratch fixture, never the live project's `.cartridge/config.lua`. What was
missing: one system memo, one test that proves the composition, and (round 1's
finding) the `.gitignore` line that lets the memo actually land.

## Round 1 findings addressed

- **B1 (blocking): the memo was gitignored.** `web.ctg/.cartridge/.gitignore`
  is a whitelist (`/*`, `!/.gitignore`, `!/docs/`, `!/help.md`, `!/tests/`) —
  measured: `git check-ignore -v web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md`
  → `web.ctg/.cartridge/.gitignore:5:/*`. Collect stages from `git status
  --porcelain --untracked-files=all -- <footprint>`, which omits ignored
  files, so the lane commit dropped the memo and pass 2 then failed block 1's
  first `test -f`. Fixed: `.gitignore` is now in the footprint, with `!/memos/`
  and `/memos/.lock` added in the same form as `docs.ctg/.cartridge/.gitignore`
  (below). Block 1 now also asserts `! git check-ignore -q <memo path>`
  directly, not just the allow-list line, so a wrong pattern still fails it.
- **B2 (blocking): block 2's binary lookup failed in every lane.**
  `cartridge.ctg` is itself a real git submodule and is empty in a lane
  worktree, so `$PWD/cartridge.ctg/target/debug/cartridge` never exists there
  and the collector sets no `CARGO_TARGET_DIR`. Fixed: block 2 derives the
  main checkout from `git rev-parse --path-format=absolute --git-common-dir`
  (the shared `.git` a linked worktree still points at) and exports
  `CARTRIDGE_BIN` from it, per the spec template's own naming for this exact
  case ("name absolute tools (e.g. `CARTRIDGE_BIN`) with an env default"). The
  test reads `process.env.CARTRIDGE_BIN` first. Measured: lane exit 0 now with
  no external env needed at all.
- **B3 (blocking): a skip could hide an unproven pass 2.** `total=pass+skip=2,
  pass>=1` accepted a skip in the live checkout too. Fixed: block 2's last
  line compares `git rev-parse --git-dir` against `--git-common-dir` — equal
  only in the main checkout, never in a linked worktree — and requires
  `skip -eq 0` there. Measured on a standalone local clone (a genuine main
  checkout, git-dir == git-common-dir, unlike every worktree used elsewhere in
  this spec): `policy.ctg` empty → exit 1; `policy.ctg` real → exit 0, 2 pass.
  In a lane worktree the guard does not fire (git-dir != git-common-dir), so
  skipping there stays honest.
- **N1: dropped the tautological assertion.** The test no longer builds
  `{content:"permission denied",error:true}` from its own `decision` value and
  asserts it equals itself. `agent.ctg`/`mcp.ctg`'s conversion of a deny into
  that reported result is cited, unchanged source, not reproduced by this
  test (comment in the test explains why); the fact this test owns is the
  real policy decision plus that the gated fetch never dispatches.
- **N2: reworded "carrying the reason."** `agent.ctg` returns
  `{"content":"permission denied","error":true}` with no reason attached; only
  the policy decision itself carries one (`"Policy denies web.fetch"`, which
  the test does assert). Acceptance box 3 below is reworded to say this
  precisely instead of implying the reason reaches the model unconditionally.
- **N3: restored PRD/spec box 1's `just prompt` clause and recorded the
  measurement.** See the measured table below: `cartridge run memo
  {"op":"system",cwd}` against a scratch composition that has `memo.ctg` and
  `web.ctg` real, with the reference memo in place, composed the memo's own
  line into the returned template. Not added as a Verify block: `cartridge
  run` against `repo` would start a real process reading/writing that
  checkout's own `.cartridge/` state, which this spec must not do; the
  measurement is recorded as evidence, not automated.
- **N4: named the exact memo-tool call.** See "The memo, exact content"
  below.
- **N6: tightened the glob-resolution check.** The test now asserts
  `toContain("tool.web -> web")` (the literal `cartridge list` line), and
  block 1 greps that same literal, instead of a regex/OR-fallback pair.
- **N5 (box 4 ceiling):** unchanged; recorded again below.

## Landing note: `.cartridge/config.lua` is out of this footprint

`.cartridge/config.lua` and `.cartridge/justfile` carry uncommitted edits that
belong to someone else (`git diff -- .cartridge/config.lua` on this HEAD shows
an unrelated `router.listen`/`skip` change). `prd collect` commits every dirty
path inside the union of the PRD's and the spec's footprints (`planner.ts`), so
any footprint naming `.cartridge/config.lua` would sweep that foreign edit into
this change, or abort the second verification pass after the fast-forward.
Neither footprint names it; the PRD's was narrowed on 2026-09-19 (review round 2,
B4). The spec does not touch it: the integration test composes `policy.ctg` and `web.ctg` into a
scratch project with its **own** `config.lua`, which proves the per-operation
refusal more directly than editing the live composition ever would (it drives
`policy` with the exact request shape `agent.ctg`/`mcp.ctg` send, and reads
`web.ctg`'s real dispatch on either side of the rule).

## Files

| Path | What it is |
| --- | --- |
| `web.ctg/.cartridge/.gitignore` | add `!/memos/` and `/memos/.lock`, matching `docs.ctg/.cartridge/.gitignore` exactly |
| `web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md` | a `kind: system` memo, written through the memo tool, `docs.ctg/.cartridge/memos/system/docs-entry.md` as the model |
| `.cartridge/tests/integration/web-tool-policy.test.ts` | the composition proof: real `policy.ctg` + real `web.ctg`, plus the generic `tool.*` glob proof against real `web.ctg` |

### The `.gitignore`, exact content

```
# Whitelist: a fresh checkout gets only what is listed here. Everything
# else a cartridge writes into .cartridge (sessions, credentials, caches,
# logs, live data) stays on this machine. A cartridge that keeps local
# state inside a tracked folder adds its rule below the list.
/*
!/.gitignore
!/docs/
!/help.md
!/memos/
!/tests/

# memo: the record writer lock.
/memos/.lock
```

### The memo, exact content

```markdown
---
kind: system
description: "When the answer is not on this disk, use the web tool to search or fetch it, and name the source URL in the answer you give."
order: 0
---

# Naming a source, not just having one

`web` is the one tool this composition grants network reach on purpose: `{op:
"search", query}` returns ranked results, each with its own `url`; `{op:
"fetch", url}` returns a page as readable text with its `url`. Neither is a
substitute for `read`/`grep`/`glob` against this repository -- reach for
`web` only once the question is about something outside it (current external
facts, a library's own docs, whether something still works the way it used
to), not as a first resort.

An answer built from a search or a fetch names the URL it came from, in the
answer itself, the same way a citation would: the person asking can follow
it. A refusal (an unconfigured search, a host outside the allowlist, a denied
policy rule) is reported back as a tool result, not silently retried or
hidden -- say what was refused and why, rather than guessing.

See `@root/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/the-agent-calls-it-cites-its-sources-and-policy-can-refuse-it`
for why this line exists: the tool already reaches the agent for free through
the `tool.*` need glob, and policy already refuses it per-operation; what was
missing was telling the model when to reach for it and to cite what it found.
```

`description` is 141 characters, under the 200-character rule in
`memo.ctg`'s `type/system.md`. Written through the memo tool, not by hand
(N4), with the exact call:

```
cartridge run memo '{"op":"write","cwd":"<abs>/web.ctg","path":"system/reach-the-web-and-name-the-source.md","body":"<the markdown above>"}'
```

against a project where `web.ctg/.cartridge/` already exists (it does). A
Verify block cannot distinguish a tool write from a hand write with identical
bytes; that stays a ceiling, not re-litigated by a stronger block.

### The test, exact content

```ts
// Composes the REAL policy.ctg and REAL web.ctg into a scratch fixture this
// test owns -- never the live project's `.cartridge/config.lua`. policy.ctg
// and web.ctg are the only two cartridges this proof needs; both ship no
// build step, so this stays lane-fast wherever their source is checked out.
import { test, expect } from "bun:test";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const runtime = path.resolve(import.meta.dir, "../../..");
// `cartridge.ctg` is itself a real git submodule and is empty in a lane
// worktree, so the binary cannot always be found under `runtime`. Block 2
// exports CARTRIDGE_BIN, resolved from the main checkout's shared `.git`
// (`git rev-parse --git-common-dir`), which exists even when this lane's own
// `cartridge.ctg` does not. CARGO_TARGET_DIR stays the fallback for a bare
// `bun test` run outside that block, from a real checkout.
const binary =
  process.env.CARTRIDGE_BIN ||
  path.join(process.env.CARGO_TARGET_DIR || path.join(runtime, "cartridge.ctg/target"), "debug/cartridge");
if (!fs.existsSync(binary)) throw Error(`Build the runtime first: ${binary}`);

// policy.ctg and agent.ctg are real git submodules; a lane worktree of the
// superproject checks every submodule out empty (no network there -- measured
// directly: a fresh `git worktree add --detach` leaves policy.ctg, agent.ctg,
// mcp.ctg empty, and `git submodule update --init` needs the network and, for
// at least one of those three, fails even with it). web.ctg is a plain
// tracked directory and is always present. This suite therefore composes only
// policy.ctg + web.ctg (never agent.ctg/mcp.ctg), and still skips cleanly
// where policy.ctg itself carries no source.
const hasPolicy = fs.existsSync(path.join(runtime, "policy.ctg/init.lua"));
const hasWeb = fs.existsSync(path.join(runtime, "web.ctg/init.lua"));

function scratchRoot(prefix: string) {
  return fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), prefix)));
}

/** A scratch composition of the real `policy.ctg` and real `web.ctg`, with a
 *  policy rule and an `allow_hosts` this test owns. */
function policyWebProfile(deny: boolean, allowHost: string) {
  const root = scratchRoot("cartridge-web-policy-");
  const builtin = path.join(root, "builtin");
  const inner = path.join(root, ".cartridge");
  fs.mkdirSync(builtin, { recursive: true });
  fs.mkdirSync(inner, { recursive: true });
  fs.symlinkSync(fs.realpathSync(path.join(runtime, "policy.ctg")), path.join(builtin, "policy.ctg"));
  fs.symlinkSync(fs.realpathSync(path.join(runtime, "web.ctg")), path.join(builtin, "web.ctg"));
  fs.writeFileSync(path.join(inner, "init.lua"), 'return {{id="policy",path="policy.ctg"},{id="web",path="web.ctg"}}\n');
  const rule = deny ? ',operations={web={fetch="deny"}}' : "";
  fs.writeFileSync(
    path.join(inner, "config.lua"),
    `return {policy={default="allow"${rule}},web={allow_hosts={${JSON.stringify(allowHost)}}}}\n`,
  );
  return { root, builtin };
}

// Bun.spawnSync blocks the JS thread, starving the event loop the loopback
// `Bun.serve` below needs to answer the child's request -- measured directly:
// the child hangs until spawnSync's own timeout kills it, every time, with
// "socket connection closed unexpectedly". Bun.spawn (async), awaited, does not.
async function runEvent(builtin: string, root: string, event: string, input: unknown, env: Record<string, string | undefined>, killAfter = 20_000) {
  const child = Bun.spawn([binary, "--dir", builtin, "run", event, JSON.stringify(input)], { cwd: root, env, stdout: "pipe", stderr: "pipe" });
  const timer = setTimeout(() => child.kill("SIGKILL"), killAfter);
  try {
    const [stdout, stderr, code] = await Promise.all([new Response(child.stdout).text(), new Response(child.stderr).text(), child.exited]);
    return { code, stdout, stderr };
  } finally {
    clearTimeout(timer);
  }
}

(hasPolicy && hasWeb ? test : test.skip)(
  "a real per-operation policy rule refuses web.fetch before any request is made, and lets it through once removed",
  async () => {
    let hits = 0;
    const server = Bun.serve({
      port: 0,
      hostname: "127.0.0.1",
      fetch: () => {
        hits++;
        return new Response("<html><body><p>secret-marker</p></body></html>", { headers: { "content-type": "text/html" } });
      },
    });
    const host = `127.0.0.1`;
    const url = `http://127.0.0.1:${server.port}/page`;
    const context = { session: "s", run: "r", call: "c", cwd: "." };
    const home = scratchRoot("cartridge-web-policy-home-");
    const env = { ...process.env, CARTRIDGE_HOME: home };
    const roots: string[] = [];
    try {
      // A symlinked cartridge is trusted by the project its real files live
      // under, not by the fixture root that links to it.
      Bun.spawnSync([binary, "trust", runtime], { cwd: runtime, env, timeout: 5_000 });
      // deny
      const deny = policyWebProfile(true, host);
      roots.push(deny.root);
      Bun.spawnSync([binary, "trust", deny.root], { cwd: deny.root, env, timeout: 5_000 });
      const decision = await runEvent(deny.builtin, deny.root, "policy", { tool: "web", input: { op: "fetch", url }, context }, env);
      expect(decision.code, decision.stderr).toBe(0);
      const value = JSON.parse(decision.stdout);
      expect(value.decision).toBe("deny");
      expect(value.reason).toContain("web.fetch");
      // What agent.ctg/mcp.ctg do with a "deny" decision -- turn it into
      // {content:"permission denied",error:true} without ever calling the
      // tool -- is cited, unchanged source (agent.ctg/src/lib.rs,
      // mcp.ctg/src/service.rs's refusal()), not reproduced here: a test
      // asserting a literal this test itself constructs would prove nothing
      // about that code. What this proof owns is the one fact upstream of
      // it -- the real policy decision -- and that the fetch it gates never
      // dispatches while denied.
      expect(hits).toBe(0);

      // allow
      const allow = policyWebProfile(false, host);
      roots.push(allow.root);
      Bun.spawnSync([binary, "trust", allow.root], { cwd: allow.root, env, timeout: 5_000 });
      const allowed = await runEvent(allow.builtin, allow.root, "policy", { tool: "web", input: { op: "fetch", url }, context }, env);
      expect(JSON.parse(allowed.stdout).decision).toBe("allow");
      const fetched = await runEvent(allow.builtin, allow.root, "web", { op: "fetch", url }, env);
      expect(fetched.code, fetched.stderr).toBe(0);
      const page = JSON.parse(fetched.stdout);
      expect(page.text).toContain("secret-marker");
      expect(hits).toBe(1);
    } finally {
      server.stop(true);
      fs.rmSync(home, { recursive: true, force: true });
      for (const root of roots) fs.rmSync(root, { recursive: true, force: true });
    }
  },
  60_000,
);

(hasWeb ? test : test.skip)(
  "the tool.* need resolves the real web cartridge with no edit to any existing cartridge",
  async () => {
    const root = scratchRoot("cartridge-web-toolglob-");
    const builtin = path.join(root, "builtin");
    const inner = path.join(root, ".cartridge");
    const caller = path.join(builtin, "caller.ctg");
    fs.mkdirSync(caller, { recursive: true });
    fs.mkdirSync(inner, { recursive: true });
    fs.symlinkSync(fs.realpathSync(path.join(runtime, "web.ctg")), path.join(builtin, "web.ctg"));
    // A fixture stand-in for "some enabled cartridge needing `tool.*`" -- this
    // is the generic mechanism the real agent.ctg relies on
    // (agent.ctg/cartridge.json's own `needs` already names it), proven here
    // with zero edit to agent.ctg, mcp.ctg or harness.ctg.
    fs.writeFileSync(
      path.join(caller, "cartridge.json"),
      JSON.stringify({ name: "caller", entry: "init.lua", events: { caller: { description: "x" } }, listen: ["caller"], needs: ["tool.*"] }),
    );
    fs.writeFileSync(path.join(caller, "init.lua"), 'cartridge.listen("caller", function() return {} end)\n');
    fs.writeFileSync(path.join(inner, "init.lua"), 'return {{id="caller",path="caller.ctg"},{id="web",path="web.ctg"}}\n');
    fs.writeFileSync(path.join(inner, "config.lua"), 'return {web={allow_hosts={"127.0.0.1"}}}\n');
    const env = { ...process.env, CARTRIDGE_HOME: scratchRoot("cartridge-web-toolglob-home-") };
    try {
      Bun.spawnSync([binary, "trust", runtime], { cwd: runtime, env, timeout: 5_000 });
      Bun.spawnSync([binary, "trust", root], { cwd: root, env, timeout: 5_000 });
      const list = Bun.spawnSync([binary, "--dir", builtin, "list"], { cwd: root, env, timeout: 10_000 });
      expect(list.exitCode, list.stderr.toString()).toBe(0);
      expect(list.stdout.toString()).toContain("tool.web -> web");
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
      fs.rmSync(env.CARTRIDGE_HOME!, { recursive: true, force: true });
    }
  },
  30_000,
);
```

## Acceptance

- [x] `web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md` exists, `kind: system`, its `description` tells the model to use `web` when the answer is not on this disk and to name the source URL, was written through the memo tool, and is not gitignored; `just prompt` includes its line (measured below, not a Verify block).
- [x] The tool appears to the agent with no edit to `agent.ctg`, `mcp.ctg` or `harness.ctg` — proven live: a fixture cartridge declaring `needs: ["tool.*"]`, composed with the real `web.ctg` and nothing else, resolves `tool.web -> web` in `cartridge list`, with zero bytes changed in any real cartridge.
- [x] A real per-operation policy rule (`policy.operations.web = {fetch = "deny"}`, in a fixture project's own config, never the live `.cartridge/config.lua`) refuses `web.fetch` before any request leaves the process; the policy decision itself carries the reason (`"Policy denies web.fetch"`). `agent.ctg`/`mcp.ctg` already convert any deny into a reported result (`{content:"permission denied",error:true}`, no reason attached) rather than a silent drop — cited, unchanged source, not re-tested here. With the rule absent, the same fetch dispatches and the caller gets the page. Proven live by `.cartridge/tests/integration/web-tool-policy.test.ts`, composing the real `policy.ctg` and real `web.ctg`, and guaranteed to actually run (not silently skip) whenever this Verify block executes in the main checkout.
- [x] An answer built from a search can name its sources: every search result and every fetched page carries its `url`, and the system memo tells the model to name it. Whether a given model turn does so is a recorded ceiling, not a mechanism (see spec01 "Ceiling: box 4").

### Ceiling: box 4 is a model behaviour, not a mechanism

`web.ctg` already returns `url` on every search result and every fetched
page (`web.ctg/src/web.ts`'s `SearchResult` and `Page` types both carry
`url`; both sibling specs' Verify blocks already assert it). Whether a given
model turn actually *writes* the URL into its spoken answer is a property of
that turn, not of any file in this footprint — no Verify block run over
source or a fixture can execute "the model composed an answer" without
either running a real model (non-deterministic, not reproducible under
`sh -eu` in 120 s) or asserting on the memo's own text, which would only
prove the instruction exists, not that it was followed. Per [[review-plan]]
step 4: the judge and the judged would run in the same process family with
no independent signal. This spec's Acceptance box for model behaviour is
therefore the instruction's presence and correctness (the memo, checked
below) plus the mechanical fact that `url` is always available to compose
with; a transcript-level check that the model actually cited a URL on a live
search turn is out of this spec's footprint and belongs to product QA on
`agent.ctg`/`live.ctg`, not to a Verify block here. (Round 1, N5: accepted as
recorded, no further gate round.)

## Verify and Proof

<!--
Engine facts (prd.ctg/.cartridge/templates/spec.md): each block runs as
`sh -eu -c`, 120 s, twice -- first with cwd = the lane (a worktree of `repo`
with every real cartridge submodule checked out empty, measured directly:
`git worktree add --detach` leaves policy.ctg, agent.ctg, mcp.ctg, and
cartridge.ctg itself all empty, and only `web.ctg`, a plain tracked
directory, has real content), then with cwd = `repo` (the live checkout,
where every submodule has its real content and is never a linked worktree).
Paths are relative to the repo root; no `cd` to an absolute checkout.

No Rust is compiled by this spec's own footprint. Block 2 only *runs* the
pre-built host binary, located via `git rev-parse --path-format=absolute
--git-common-dir` (the shared `.git` of the main checkout, reachable from a
linked worktree even when that worktree's own `cartridge.ctg` is empty) with
`CARTRIDGE_BIN` as the override, the same naming the spec template itself
gives for this exact case.

Measured directly, both blocks, via `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`,
with the round-2 reference memo, `.gitignore` and test file in place:
- **lane** (a fresh detached superproject worktree -- policy.ctg/mcp.ctg/
  agent.ctg/cartridge.ctg all empty, web.ctg real): block 1 exit 0; block 2
  finds `CARTRIDGE_BIN` via the main checkout automatically (no external env
  needed) and reports `1 pass, 1 skip, 0 fail`, exit 0. The B3 guard does not
  fire here (git-dir != git-common-dir in a linked worktree), so the skip is
  honest, not hidden.
- **"repo" shape, policy present** (a second linked worktree with
  `policy.ctg`'s real content restored, standing in for a lane whose
  submodule happens to be checked out): block 1 exit 0; block 2:
  `2 pass, 0 fail, 10 expect() calls`, exit 0, ~3.4 s.
- **true main checkout, policy absent** (a standalone local `git clone`,
  where `git rev-parse --git-dir` equals `--git-common-dir`, unlike every
  worktree above -- the shape B3 has to catch): block 2 exit **1** even
  though `1 pass, 1 skip, 0 fail` on its own would otherwise look green; the
  guard's `test "$skip" -eq 0` is what fails it.
- **true main checkout, policy present** (the same clone, `policy.ctg`
  restored): block 2 exit 0, `2 pass, 0 fail, 10 expect() calls`.
- **base** (the three footprint files absent -- the actual live checkout,
  read-only): block 1 exit 1 (the first `test -f` fails).

Every census line is one statement per the `sh -eu` AND-list trap already
recorded in the sibling specs (`test -n "$n" && test "$n" -ge 1` never fails
under `set -e` when `$n` is empty).
-->

### Block 1 — the memo lands, is well-formed and not gitignored, and the test file exists

```sh
test -f web.ctg/.cartridge/.gitignore
test -f web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md
test -f .cartridge/tests/integration/web-tool-policy.test.ts
grep -qF '!/memos/' web.ctg/.cartridge/.gitignore
! git check-ignore -q web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md
grep -qn '^kind: system$' web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md
grep -qn 'description:' web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md
description=$(sed -n 's/^description: *"\(.*\)"$/\1/p' web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md | head -1)
test -n "$description"
length=$(printf '%s' "$description" | wc -c | tr -d ' ')
test "$length" -le 200
printf '%s' "$description" | grep -qi 'web'
printf '%s' "$description" | grep -qi 'source\|cite\|url'
grep -qn 'source URL' web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md
grep -qF 'tool.web -> web' .cartridge/tests/integration/web-tool-policy.test.ts
grep -qn 'policyWebProfile' .cartridge/tests/integration/web-tool-policy.test.ts
grep -qn 'operations={web={fetch="deny"}}' .cartridge/tests/integration/web-tool-policy.test.ts
grep -qn 'CARTRIDGE_BIN' .cartridge/tests/integration/web-tool-policy.test.ts
for title in \
  "a real per-operation policy rule refuses web.fetch before any request is made, and lets it through once removed" \
  "the tool.* need resolves the real web cartridge with no edit to any existing cartridge"
do
  grep -qnF "$title" .cartridge/tests/integration/web-tool-policy.test.ts
done
```

A `git diff --quiet HEAD -- agent.ctg mcp.ctg harness.ctg policy.ctg
.cartridge/config.lua` guard was tried and dropped in round 1:
`.cartridge/config.lua`/`.cartridge/justfile` are already dirty on this HEAD
from someone else's unrelated edit, so that guard fails today independent of
this spec. The guarantee that nothing outside this spec's footprint lands
belongs to `prd collect` itself (it commits only footprint paths).

### Block 2 — the composed proof runs, is guaranteed to run for real in the main checkout, and is honest elsewhere

```sh
main="$(git rev-parse --path-format=absolute --git-common-dir)"
main="${main%/.git}"
export CARTRIDGE_BIN="${CARTRIDGE_BIN:-$main/cartridge.ctg/target/debug/cartridge}"
test -x "$CARTRIDGE_BIN" || { echo "Build the runtime first: $CARTRIDGE_BIN" >&2; exit 1; }
log="${TMPDIR:-/tmp}/web-tool-policy-test.$$.log"
bun test ./.cartridge/tests/integration/web-tool-policy.test.ts >"$log" 2>&1 || { cat "$log"; rm -f "$log"; exit 1; }
cat "$log"
pass=$(sed -n 's/^ *\([0-9][0-9]*\) pass$/\1/p' "$log" | head -1)
fail=$(sed -n 's/^ *\([0-9][0-9]*\) fail$/\1/p' "$log" | head -1)
skip=$(sed -n 's/^ *\([0-9][0-9]*\) skip$/\1/p' "$log" | head -1)
test -n "$skip" || skip=0
rm -f "$log"
test -n "$pass"
test -n "$fail"
test "$fail" -eq 0
total=$((pass + skip))
test "$total" -eq 2
test "$pass" -ge 1
# Pass 2 (the main checkout itself, never a linked worktree) must run the
# composed proof for real: a skip is only honest where the lane's own
# policy.ctg genuinely carries no source.
if test "$(git rev-parse --path-format=absolute --git-dir)" = "$(git rev-parse --path-format=absolute --git-common-dir)"; then
  test "$skip" -eq 0
fi
```

## What was measured, on HEAD 7446db2 (spec written against 4104d36; no footprint path changed in between)

In addition to the block-by-block table above:

| Case | Command | Result |
| --- | --- | --- |
| deny rule present | `cartridge run policy {tool:"web",input:{op:"fetch",url}}` | `{"decision":"deny","reason":"Policy denies web.fetch",...}` |
| deny rule present | (never dispatched) | loopback server saw 0 requests |
| deny rule absent | `cartridge run policy {tool:"web",input:{op:"fetch",url}}` | `{"decision":"allow",...}` |
| deny rule absent | `cartridge run web {op:"fetch",url}` | `{"url":...,"text":"secret-marker",...}`, loopback server saw 1 request |
| fixture `needs:["tool.*"]` + real `web.ctg` | `cartridge list` | `tool.web -> web`, zero cartridges edited |
| memo composed (reviewer's round-1 measurement, cited here per N3, not re-run this round) | `cartridge run memo {"op":"system","cwd":"."}` against a scratch composition with real `memo.ctg` + real `web.ctg` and the reference memo in place | the returned template includes `- When the answer is not on this disk, use the web tool ... name the source URL in the answer you give. Body: @web/system/reach-the-web-and-name-the-source.md` |

All scratch worktrees and the standalone clone used for measurement were
removed after; `git worktree prune` was run; nothing was written in the live
checkout.
