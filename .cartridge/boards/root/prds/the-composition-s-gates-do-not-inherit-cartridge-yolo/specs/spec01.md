---
complexity: small
footprint:
  - .cartridge/justfile
  - .cartridge/memos/routine/cartridge-development.md
---

# spec01 — the gate recipes strip CARTRIDGE_YOLO before they spawn anything

Base: superproject `80a6b0913893354f1cac6ccfef54017d191f9e27`. Revision 1 was
re-proved at `c84b3a4`, where both footprint files and the two pins are
unchanged. Pins: agent.ctg `620857d`, cartridge.ctg `324f36e`.

The live `.cartridge/justfile` has an uncommitted hunk in `_fan` from another
session (an isolation run beside `check`). Another row lands that hunk first.
This diff touches only `_one` and `build`, and it applies cleanly both to
HEAD's file and to the dirty file (`patch --dry-run` exits 0). Implement in a
lane cut from HEAD. Before collect, run
`git -C /Users/feb/dev/cartridge status --porcelain -- .cartridge/justfile`,
as the PRD's landing note says.

## Mechanism

Two changes to `.cartridge/justfile`:

- One bash `unset` in `_one`.
- `env -u` on `build`.

Why these two recipes:

- Every gate (`check`, `test`, `smoke`, `verify`, `isolation`) enters through
  `_fan`. `_fan` itself only spawns `tools` (which runs `command -v` only) and
  `_one`.
- `_one` is the one recipe that spawns memo-run, which then runs cargo,
  nextest, bun or the built host. `_one` can also be called on its own. So the
  single `unset` in `_one` covers both the gate path and a direct `_one` call,
  and an `unset` in `_fan` would add nothing. Verify block 2 proves each path
  separately.
- `build` spawns cargo through memo-run without going through `_fan`.

Rejected: just's global `unexport`. It would also strip the variable from the
operational recipes, and `cartridge.ctg/src/cli/host.rs:157` correctly passes it
on to a daemon those recipes start.

## Scope of PRD box 1, narrowed on purpose

PRD box 1 asks for every recipe that spawns cargo *or a nested `just`*. This
spec deliberately narrows that to the recipes that reach cargo, a test runner
or the built host: `_one` for every gate, and `build`.

Every memo-run recipe spawns a nested `just`:

- `run`, `launch`, `daemon`, `process`, `invoke`, `call`, `status`, `tail`,
  `ledger`, `sweep`, `mcp` and `live` run the operational memos, which start
  or talk to the host. There the variable is a real capability: host.rs:157
  turns an inherited `CARTRIDGE_YOLO=1` into `--yolo` on the daemon it spawns.
  Stripping it there would make that capability unreachable, which PRD box 4
  forbids.
- `help`, `tools`, `links`, `install`, `audit`, `proxy`, `prompt`, `recall`
  and `availability` spawn no cargo and give no gate verdict.

A gate verdict is produced only below `_one` or `build`, so that is where the
strip goes.

## Steps

1. Apply this diff to `.cartridge/justfile`. It is also saved as
   `justfile.patch` in
   `prd.ctg/.cartridge/boards/root/.state/loop/the-composition-s-gates-do-not-inherit-cartridge-yolo/`.

```diff
--- a/.cartridge/justfile
+++ b/.cartridge/justfile
@@ -124,6 +124,11 @@
 _one gate target *args:
     #!/usr/bin/env bash
     set -euo pipefail
+    # `--yolo` exports CARTRIDGE_YOLO=1 into the terminal, and the host then
+    # merges `yolo: true` into every cartridge declaring it: files are trusted
+    # and the agent skips policy. A verdict is about the code, so no target
+    # inherits it; a test that needs yolo sets it in its own child environment.
+    unset CARTRIDGE_YOLO
     gate=$1; target=$2; shift 2
     case "$gate" in
         # The composed repository's own layout test is a target of the test
@@ -147,7 +152,7 @@
     esac
 
 build target="all" *args:
-    @"{{memo_runner}}" "{{development}}" build "$@"
+    @env -u CARTRIDGE_YOLO "{{memo_runner}}" "{{development}}" build "$@"
 
 links:
     @"{{memo_runner}}" "{{development}}" links
```

2. Apply this diff to `.cartridge/memos/routine/cartridge-development.md`,
   saved as `memo.patch` in the same directory. It adds one body paragraph and
   leaves the frontmatter and the just block untouched.

```diff
--- a/.cartridge/memos/routine/cartridge-development.md
+++ b/.cartridge/memos/routine/cartridge-development.md
@@ -24,6 +24,16 @@
 worktrees is not guaranteed. Ordinary checkouts keep the caller's wrapper
 configuration.
 
+A gate result is evidence only when the environment it was taken in is named.
+`--yolo` exports `CARTRIDGE_YOLO=1` into the terminal; the host then merges
+`yolo: true` into every cartridge that declares it, so files are trusted and the
+agent skips policy, and the same tree gives another verdict. The composed gates
+(`just check`, `test`, `smoke`, `verify`, `isolation`, and `build`) therefore
+strip that variable themselves before they spawn anything; a test that needs
+yolo sets it in its own child environment, as the lifecycle test does. A
+hand-run `cargo` or `memo-run` bypasses that: run it as
+`env -u CARTRIDGE_YOLO ...` and name that form in the report.
+
 Model evaluations remain explicit opt-in
 operations in their own memos.
```

   The source for that wording: the merge is at
   `cartridge.ctg/src/settings/mod.rs:15-16`, and the policy skip is the
   agent's own `yolo` branch at `agent.ctg/src/lib.rs:634`.

3. Run the Verify blocks below from the lane root.

## Runs that need the variable (PRD box 4)

`rg CARTRIDGE_YOLO` over the tree, excluding `target/` and the boards, finds
only three places:

- `cartridge.ctg/src/transport/settings.rs:188`, the constant.
- `cartridge.ctg/.cartridge/tests/unit/src/tests/settings.rs:34`, a comment.
- `.cartridge/tests/integration/takeover.test.ts:17`, the `lifecycle` target.
  It sets `CARTRIDGE_YOLO: "1"` in the environment it builds for its own
  children, so the `unset` does not affect it.

No gate run needs to inherit the variable. `--yolo` on `run`, `launch` or
`daemon` still sets it inside the process (`cartridge.ctg/src/cli/mod.rs:87-88`),
and the operational recipes are unchanged.

## Lane dependency

The agent loop test needs a release host. `base_binary()` in
`agent.ctg/.cartridge/tests/integration/loop.rs:52-63` uses `CARTRIDGE_BIN`,
or else `../cartridge.ctg/target/release/cartridge`. A lane's cartridge.ctg is
a fresh `seedSubmodules` worktree with no `target/`, so without that variable
all 13 loop tests panic with "the base is not built".

- The agent `test` blocks therefore default `CARTRIDGE_BIN` to the live release
  host.
- Block 1 fails first, and names the release build, if that host is missing.
  Recovery: `cd cartridge.ctg && cargo build --release` in the live checkout,
  or set `CARTRIDGE_BIN`.

The cartridge `each_file…` test does not have this problem. It is a unit test
of cartridge.ctg itself and compiles from the lane's own checkout (measured
below).

## Acceptance

- [ ] `_one` and `build` in `.cartridge/justfile` remove `CARTRIDGE_YOLO`
      before they spawn anything. Under `CARTRIDGE_YOLO=1`, a stand-in cargo
      and a stand-in host record the variable as unset when reached through
      each of these: `just test agent`, `just _one test agent` called on its
      own, `just verify composition` and `just build agent` (Verify block 2).
- [ ] `CARTRIDGE_YOLO=1 just test agent` passes
      `multiple_tool_calls_execute_and_persist_in_response_order` with no
      change to agent.ctg, and `env -u CARTRIDGE_YOLO just test agent` passes
      it too (the first two `test` blocks).
- [ ] `CARTRIDGE_YOLO=1 just test cartridge each_file_is_evaluated_in_a_state_of_its_own`
      passes `lua::tests::each_file_is_evaluated_in_a_state_of_its_own` (the
      third `test` block).
- [ ] No gate run needs to inherit the variable (evidence above). The
      operational recipes and `--yolo` are unchanged, and the nested-`just`
      narrowing is deliberate (see "Scope of PRD box 1"). The diff reviewer
      checks that the diff touches only `_one` and `build`.
- [ ] `cartridge-development.md` says a gate result is evidence only when its
      environment is named, and that the gate strips `CARTRIDGE_YOLO` itself
      (block 2 checks that the memo names the variable; the diff reviewer
      checks the wording).

## Verify and Proof

Discrimination, measured in a tree built the way `seedSubmodules` builds a lane:

- `git worktree add --detach` of superproject HEAD `c84b3a4`.
- agent.ctg and cartridge.ctg added as detached worktrees at their pinned
  shas, with no `target/`.
- Cold `target/prd-yolo-verify`; `CARTRIDGE_BIN` and `CARGO_TARGET_DIR` unset;
  cwd is the worktree root.

| Block | HEAD files | With both diffs |
|---|---|---|
| 1 (release host present) | exit 0 | exit 0, 0 s |
| 2 (probe) | exit 1: "a gate handed CARTRIDGE_YOLO to cargo-test: 1 1" | exit 0, 15 s |
| test agent, `CARTRIDGE_YOLO=1` | exit 1, 50 s: `multiple_tool_calls_execute_and_persist_in_response_order ... FAILED` at loop.rs:798 | exit 0, 48 s, 13 passed |
| test agent, variable unset | exit 0, 74 s | exit 0, 60 s |
| test cartridge `each_file…` | exit 1, 29 s: nextest FAIL | exit 0, 11 s: nextest PASS |

Mutants of block 2 against the patched tree:

- `_one`'s `unset` removed: exit 1, "... cargo-test: 1 1". Both the gate path
  and the direct `_one` call leak.
- The `build` edit reverted: exit 1, "... cargo-build: 1".

Block 1 with `CARTRIDGE_BIN=/nonexistent`: exit 1, and the message names the
release build.

```sh
base="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}"
if ! test -x "$base"; then
    printf 'no base host at %s: the agent loop test needs a release host; run `cd cartridge.ctg && cargo build --release` in the live checkout, or set CARTRIDGE_BIN\n' "$base" >&2
    exit 1
fi
```

```sh
probe=$(mktemp -d)
mkdir -p "$probe/bin" "$probe/target/debug"
# A stand-in cargo and host that record whether the gate handed them the variable.
# The stand-in cargo fails `build`, so build stops before links/install touch anything.
printf '#!/bin/sh\nprintf "%%s\\n" "${CARTRIDGE_YOLO-unset}" >> "%s/cargo-$1"\n[ "$1" != build ]\n' "$probe" > "$probe/bin/cargo"
printf '#!/bin/sh\nprintf "%%s\\n" "${CARTRIDGE_YOLO-unset}" >> "%s/host"\n' "$probe" > "$probe/target/debug/cartridge"
chmod +x "$probe/bin/cargo" "$probe/target/debug/cartridge"
CARTRIDGE_YOLO=1 PATH="$probe/bin:$PATH" just --justfile .cartridge/justfile test agent
CARTRIDGE_YOLO=1 PATH="$probe/bin:$PATH" just --justfile .cartridge/justfile _one test agent
CARTRIDGE_YOLO=1 CARGO_TARGET_DIR="$probe/target" just --justfile .cartridge/justfile verify composition
CARTRIDGE_YOLO=1 PATH="$probe/bin:$PATH" CARTRIDGE_BIN_DIR="$probe/installed" just --justfile .cartridge/justfile build agent || true
# Two test records: one through the gate, one from `_one` called on its own.
test "$(grep -c . "$probe/cargo-test")" -eq 2
for seen in cargo-test host cargo-build; do
    test -f "$probe/$seen"
    if grep -qv '^unset$' "$probe/$seen"; then
        printf 'a gate handed CARTRIDGE_YOLO to %s: %s\n' "$seen" "$(tr '\n' ' ' < "$probe/$seen")" >&2
        exit 1
    fi
done
if ! grep -q 'CARTRIDGE_YOLO' .cartridge/memos/routine/cartridge-development.md; then
    echo 'cartridge-development.md does not name the variable the gate strips' >&2
    exit 1
fi
```

```test
run: CARTRIDGE_YOLO=1 CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}" CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/prd-yolo-verify}" just --justfile .cartridge/justfile test agent
pass: multiple_tool_calls_execute_and_persist_in_response_order
```

```test
run: env -u CARTRIDGE_YOLO CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}" CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/prd-yolo-verify}" just --justfile .cartridge/justfile test agent
pass: multiple_tool_calls_execute_and_persist_in_response_order
```

```test
run: CARTRIDGE_YOLO=1 CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/prd-yolo-verify}" just --justfile .cartridge/justfile test cartridge each_file_is_evaluated_in_a_state_of_its_own
pass: lua::tests::each_file_is_evaluated_in_a_state_of_its_own
```
