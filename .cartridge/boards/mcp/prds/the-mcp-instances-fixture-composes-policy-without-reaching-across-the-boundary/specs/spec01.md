---
complexity: small
footprint:
  - .cartridge/tests/integration/instances.test.ts
---

# spec01 — the fixture composes a policy of its own

Base: `mcp.ctg` `HEAD` on `main` (clean at dispatch, `git status --porcelain`
empty). Repo is `mcp.ctg`; the footprint is the one file.

## What the fixture actually needs from `policy.ctg`

Measured, at `policy.ctg/cartridge.json` and `policy.ctg/init.lua`:

- The fixture composes `policy` for exactly one reason: `mcp.ctg/cartridge.json`
  declares `needs: ["sessions","policy","policy.*","tool.*"]`, and the host holds
  a waiting cartridge until every need it waits for has an **active listener**
  (`cartridge.ctg/src/host/mod.rs:444`). With no cartridge listening on `policy`,
  the `mcp` node never starts and the fixture's `initialize` retry loop runs out.
- At call time `mcp.ctg/src/service.rs:574-605` emits one `policy` event per
  `tools/call` and proceeds only on `decision == "allow"`; anything else is a
  refusal and `_ =>` is "invalid policy decision". So the fixture needs a
  decision of `allow` to reach any of its session assertions.
- Nothing else. The fixture never sends `cartridge/policy`, so
  `policy.explain` is never reached: `mcp.ctg/src/lib.rs:29` enables explanations only when
  `needs()` contains the literal `"policy.explain"`, and mcp declares the glob
  `policy.*`, not that key. No assertion in the fixture reads a `reason`, a
  `revision`, a `rule`, or any refusal. The real evaluator's 122 lines — rule
  precedence, operation rules, the revision identity, the explain authorization
  shape — are dead weight in this profile.

The need is therefore "a cartridge that answers the `policy` event", not
"`policy.ctg`". Of the isolation memo's three ways out — declare the need, make
it an event, or ship an own copy — the need is **already declared** (`needs`
carries `policy`) and the integration **already is an event**; only the file
copy is illegal. So: **ship an own copy**, which here means the fixture writes
its own policy cartridge with the same `cartridge(profile, id, manifest, init)`
helper it already uses for `sessions` and `echo`, both of which are already own
copies of a sibling's wire shape ("as the real sessions cartridge answers",
line 64). This is one more of the same, not a new mechanism.

## Steps

1. `.cartridge/tests/integration/instances.test.ts`: delete lines 62-63 (the
   `mkdirSync(profile/policy)` and the `copyFileSync` from `../policy.ctg`) and
   put a `cartridge(profile, 'policy', …)` call in their place:

   ```ts
   // Its own policy, not the sibling checkout's: mcp waits for a `policy`
   // listener before its node starts and refuses every call the decision does
   // not allow, so the composed daemon still applies a configured decision. The
   // declared default is `ask`; the composition's `default="allow"` is what lets
   // these calls through.
   cartridge(profile, 'policy', { name: 'policy', entry: 'init.lua', settings: { default: { type: 'string', default: 'ask' } }, events: { policy: { description: 'Decide a tool call: {tool, op?} -> {decision, reason, revision}.', schema: { type: 'object', required: ['tool'] } } }, listen: ['policy'] }, `
   cartridge.listen("policy", function(request)
     return { decision = cartridge.config.default, reason = "fixture policy", revision = "fixture-policy:1" }
   end)`);
   ```

   `cartridge()` already `mkdirSync`s recursively, so the separate `mkdirSync`
   goes. Nothing else in the file changes: `runtime` stays (line 8 still uses it
   for the `CARTRIDGE_BIN` fallback), and the composition's
   `config.lua` keeps `policy={default="allow"}`.

2. Nothing else. No source, manifest or unit-test change; `needs` already
   declares `policy`.

Why the declared default is `ask` and not `allow`: it makes the composition's
own `policy={default="allow"}` load-bearing. The daemon really evaluates a
configured decision for every `tools/call`; drop the configuration and every
call is refused and the session assertions fail. A stub returning a hardcoded
`"allow"` would pass the same assertions while proving nothing about the policy
round — that is cheat (c) below, and block 3 rejects it.

## Acceptance

- [x] No file in `mcp.ctg` names `../policy.ctg` or any other `../<sibling>.ctg`
      path, and the isolation gate passes for the whole composition with this
      tree standing in for `mcp.ctg` (block 1).
- [x] The fixture still passes, with the same session, cancel, survival,
      `status` and socket assertions, against a policy cartridge it writes
      itself (block 2).
- [x] No assertion is weakened: the `expect()` census does not fall, each named
      property is still asserted by name, and the test is not skipped, `.only`d
      or made conditional (block 3).

## Verify and Proof

Engine facts, per `prd.ctg/.cartridge/templates/spec.md`: each block is
`sh -eu -c`, 120 s, run first in the lane (a worktree of `mcp.ctg` at
`prd.ctg/.cartridge/boards/mcp/.lanes/<slug>`) and then in `repo` (`mcp.ctg`).
Paths are relative to the repo root; no block `cd`s to an absolute checkout and
no block writes inside the footprint.

**Before the fix, block 1 is red and blocks 2 and 3 are red; after it all three
are green.** Block 1 is red today in the live repo for exactly the defect this
PRD names — that is correct and expected, and it is why the block exists: no
gate on the path that landed the defect ran it.

Neither pass has a composition root as its cwd, and the isolation gate is
composition-wide, so blocks 1 and 2 find the composition by walking up from the
cwd to the first directory holding `.cartridge/tools/memo-run` (the composed
repository; `mcp.ctg` has no such directory and neither does a lane's parent).
Block 1 then builds a **shadow root** in `TMPDIR`: a symlink per sibling `*.ctg`
from the composition, plus `mcp.ctg -> $PWD`, so the gate reads the tree under
test in both passes and the live checkout in neither. Measured in both
directions: with `mcp.ctg` symlinked to the live tree the gate exits 1 naming
`instances.test.ts:63`; with it symlinked to the fixed tree it exits 0,
`Isolation passed for 17 cartridges.`

```sh
# Block 1 — the gate this PRD exists for, over the tree under test.
composition=$PWD
until [ -x "$composition/.cartridge/tools/memo-run" ]; do
  if [ "$composition" = / ]; then echo 'no composed repository above this tree' >&2; exit 1; fi
  composition=$(dirname "$composition")
done
shadow=$(mktemp -d "${TMPDIR:-/tmp}/mcp-isolation-XXXXXX")
trap 'rm -rf "$shadow"' EXIT
for sibling in "$composition"/*.ctg; do
  case $(basename "$sibling") in mcp.ctg) continue ;; esac
  ln -s "$sibling" "$shadow/$(basename "$sibling")"
done
ln -s "$PWD" "$shadow/mcp.ctg"
# The gate builds its sibling alternation from the `*.ctg` directories it finds,
# so a shadow missing one passes an unfixed tree. Assert the set it was built from.
test "$(ls -d "$shadow"/*.ctg | wc -l)" -eq "$(ls -d "$composition"/*.ctg | wc -l)"
mkdir -p "$shadow/.cartridge/memos/routine"
cp "$composition/.cartridge/memos/routine/check-cartridge-isolation.md" "$shadow/.cartridge/memos/routine/"
"$composition/.cartridge/tools/memo-run" "$shadow/.cartridge/memos/routine/check-cartridge-isolation.md" check
```

```sh
# Block 2 — the fixture itself, against binaries built outside both repos.
# The host is the composition's, because it is the platform and not the tree
# under test; the module is this tree's own crate.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/mcp-policy-fixture-verify}"
composition=$PWD
until [ -x "$composition/.cartridge/tools/memo-run" ]; do
  if [ "$composition" = / ]; then echo 'no composed repository above this tree' >&2; exit 1; fi
  composition=$(dirname "$composition")
done
cargo build --manifest-path "$composition/cartridge.ctg/Cargo.toml" --bin cartridge
cargo build --manifest-path Cargo.toml
CARTRIDGE_BIN="$CARGO_TARGET_DIR/debug/cartridge"
MCP_MODULE="$CARGO_TARGET_DIR/debug/libmcp.dylib"
if [ ! -f "$MCP_MODULE" ]; then MCP_MODULE="$CARGO_TARGET_DIR/debug/libmcp.so"; fi
export CARTRIDGE_BIN MCP_MODULE
bun test ./.cartridge/tests/integration/instances.test.ts
```

```sh
# Block 3 — nothing was weakened to make block 1 pass. Single-statement guards:
# `! grep` is ignored by `sh -e`, BSD grep has no `\|` alternation, and a
# `test -n "$x" && test …` list only gates on its last command.
fixture=.cartridge/tests/integration/instances.test.ts
test -f "$fixture"
# The profile carries a policy cartridge the fixture writes itself.
grep -q "cartridge(profile, 'policy'" "$fixture"
# Its answer comes from the composition's configuration, not from a constant,
# so the daemon still applies a decision that the composition could change.
grep -q 'cartridge.config.default' "$fixture"
grep -q 'policy={default="allow"}' "$fixture"
# The test is run, whole, every time.
if grep -nE 'skip|\.todo|\.only|\.failing' "$fixture"; then exit 1; fi
# The census of proved properties has not fallen.
count=$(grep -c 'expect(' "$fixture")
test "$count" -ge 11
# Each property the PRD names is still asserted.
grep -q 'expect(initialized.result?.serverInfo?.name' "$fixture"
grep -q 'expect(two).not.toBe(one)' "$fixture"
grep -q 'expect(await session(a)).toBe(one)' "$fixture"
grep -q 'expect(await session(b)).toBe(two)' "$fixture"
grep -q "method: 'notifications/cancelled'" "$fixture"
grep -q "node.state === 'active'" "$fixture"
grep -q "entry === 'mcp.sock'" "$fixture"
```

None of block 3's failure messages prints the token it wanted: a failing
`grep -q` is silent and the block exits on the property, not on a cure.

`just audit`, named in the PRD's acceptance, is covered by no block and cannot
be. `audit` reports every cartridge against the vision axes — surface, README,
help page — and none of those is reachable from a change confined to one
integration test file, so no block over this footprint can move it either way.
It stands as an owner gate at collect, not as a Verify block here.

### Cheats built and measured against these blocks

Seven trees, each a shadow composition root with `mcp.ctg` carrying one variant
of the fixture. `isolation` is block 1's gate; `guards` is block 3 verbatim.

| tree | what it is | isolation | guards |
|---|---|---|---|
| `base` | the live fixture, unchanged | **1** | 1 |
| `ref` | step 1 applied | **0** | **0** |
| `cheat-a` | isolation by deleting the assertions that needed policy | 0 | 1 |
| `cheat-a2` | `ref` plus the same deletions (stub kept) | 0 | 1 (census 5 < 11) |
| `cheat-b` | isolation by skipping the test when `../policy.ctg` is absent | 0 | 1 |
| `cheat-b2` | `ref` plus an unconditional `skipIf` | 0 | 1 |
| `cheat-c` | a stub that hardcodes `allow`, no settings, composition policy config dropped | 0 | 1 |

The bar is reachable (`ref` is 0/0) and no cheat clears both.

## Remaining risk

- Block 2 **is** measured green, on both sides. Review round 1 built the host
  and the module into a target dir outside every repository, exactly as block 2
  does, and ran block 2 verbatim: the `ref` tree (step 1 applied) exits **0**
  with 1 pass, 0 fail and 13 `expect()` calls in 2.88 s, and the live `mcp.ctg`
  composing the real `policy.ctg` exits **0** the same way, 1 pass and 13
  `expect()` calls in 2.77 s — identical pass and identical census on both
  sides. An earlier red in the analyst's harness was the stale checked-in host
  binary (`cartridge.ctg/target/{debug,release}/cartridge`, both Sep 16 23:40,
  predating `ec4de01`, the commit that makes the bridge mint an instance id):
  it fails at `expect(two).not.toBe(one)` with `session-1` on both bridges for
  `base` and `ref` alike. That is why block 2 builds the host itself, and why
  the checked-in binaries must not be used to run it.
- Block 2 builds `cartridge.ctg` cold into a target dir outside both repos on
  the lane pass, within the collector's 120 s. If it times out, the target dir
  survives and the `repo` pass is warm; if the lane pass times out repeatedly,
  collect from `claimed` with no lane, as the sibling
  `mcp-keys-sessions-and-inflight-calls-by-attached-instance` did.
- `mcp.ctg/Cargo.toml` has no path dependency into a sibling, so a lone lane
  worktree builds without sibling symlinks beside it (checked; the only `path =`
  is `src/lib.rs`). Block 2's host build reaches the composition by absolute
  path, which is the "name absolute tools with an env default" case, not a `cd`
  into another checkout.
- The guard `grep -nE 'skip|…'` would also fire on the word "skip" in a comment.
  That is deliberate: the fixture has no such word today, and a comment about
  skipping is worth a second look.
