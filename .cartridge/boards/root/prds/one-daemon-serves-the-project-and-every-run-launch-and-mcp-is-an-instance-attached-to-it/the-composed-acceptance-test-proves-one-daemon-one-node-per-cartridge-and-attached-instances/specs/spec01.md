---
complexity: medium
footprint:
  - .cartridge/tests/unit/src/tests/mod.rs
  - .cartridge/tests/unit/src/tests/composed/mod.rs
  - .cartridge/tests/unit/src/tests/composed/fixture.rs
---

# spec06 — one composed test proves one daemon, one node per cartridge and attached instances

Base: cartridge.ctg `d169293`. `repo` is `cartridge.ctg`; nothing outside it
changes. All three footprint paths are inside the PRD's declared
`.cartridge/tests/`, so no widening is needed.

The implementation is preserved at this PRD's `.state/loop/…/reference/`,
updated this round, `rustfmt`-clean, and it passes all four Verify blocks.

## Where the test lives, and why it is Rust and not bun

*(Verified independently in review round 1; unchanged.)*
`cartridge.ctg/justfile:5-7` is exactly `cargo nextest run --workspace`, reached
by `just test runtime` through `cartridge-development.md:71-72`. The bun
`lifecycle` target is hard-wired to the **superproject's**
`.cartridge/tests/integration/takeover.test.ts`, so a `.test.ts` under
`cartridge.ctg/.cartridge/tests/` would be run by no gate. `Cargo.toml:8` sets
`autotests = false`; every test file is reached by a `#[cfg(test)] #[path]` mod
attribute from `src/`, and the only attachment point inside the footprint is
`.cartridge/tests/unit/src/tests/mod.rs:1-4` (included by `src/lib.rs:15-17`).
Adding `mod composed;` needs **no `src/` edit**.

## What changed this round

**B16 — the mutant was detectable in-band, and is not any more.** Two fixes, and
the second is the structural one:

1. Block 4 now runs in the **same path shape and the same environment** as
   block 1 — the same `/tmp/cxv$$` root, the same variables, the same
   `--test-threads=1`. The reviewer's cheat H keyed on `XDG_RUNTIME_DIR`
   containing `cxv`; that string is now true of both runs.
2. **The receipt moved into `Drop`, and takes no argument at all.** It is
   written on the panic path, so a *failing* run still leaves one — and block 4
   judges the mutant by **the mutant's own receipts**, not by its exit code:

   ```
   compositions=1 nodes=3   — the composition was whole
   probe_node=differs       — and what broke is the one thing the mutation broke
   run_node=differs
   ```

   Cheat H panics at its detector before any `Lab` exists, so no `Drop` runs
   and **no receipt directory is created at all** — measured; that is where
   block 4 rejects it.

   The receipt's fields are the fixture's alone: a body cannot author
   `compositions`, `nodes`, `probe`/`probe_node`, `run`/`run_node`, `launched`
   or `live`, or forge one under mutation — it supplies only its own label.
   That is what "the body chooses nothing" means, and only that. It does not
   mean the gate can tell *why* a body went red: because `Drop` writes
   unconditionally, a body that panics for a reason unconnected to any of the
   four claims still leaves this exact receipt (cheat I, below). The reddening
   under the mutant shows the fixture's own measurements differed; it is not
   attributed to, and does not prove, that the failing assertion named one of
   the claims.

   **Ceiling (B18, cheat I).** Five earlier attempts to beat block 4 in-band —
   cheats A, D, F, G and H, preserved beside this spec's reference at
   `.state/loop/…/cheats/` — are all rejected by block 1 or block 4. Cheat I is
   not: built at the mutant's own path (`"$work/tree"`), it asserts
   `!env!("CARGO_MANIFEST_DIR").contains("/tmp/")` once the `Lab` exists,
   panics there on every one of the four bodies, and still produces all four
   receipts block 4 demands, because `Drop` runs on any panic. One round was
   spent designing a same-path, same-environment gate (`review-plan.md:58-69`);
   it closed the environment discriminator (B16) but not the path one, and
   that is recorded as the ceiling of this gate rather than spent again. The
   backstop is not block 4: it is reading `reference/mod.rs` directly — four
   exact `assert_eq!`s, one per claim, no bound and no detector — and checking
   that the assertions shipped are the assertions this spec's receipt table
   describes.

**B17 — contention is handled, not disclaimed.** Blocks 1 and 4 pass
`--test-threads=1`. The suite is its own heaviest neighbour — four bodies, five
hosts — and serialising it removes that. Measured: block 1 goes from ~3.9 s
parallel to **7.5 s** serial, block 4 to **28.8 s**; both well inside 120 s, and
the "rerun the target alone" sentence that contradicted the PRD's third
acceptance box is gone. The PRD's box stands as written.

**The stronger-assertion cell, re-measured.** The reviewer was right: my
archived tree was not `rustfmt`-clean, so block 3 rejected it — correctly, since
that block exists to reject unformatted code. Formatted, the same tree now
measures **0/0/0/0**. It is preserved beside the reference so the cell can be
checked rather than taken on trust.

**F13** — blocks 1, 3 and 4 default `CARGO_TARGET_DIR` to
`/tmp/cxbuild-composed`, outside every repository. This departs from the
template's `$PWD/target/<slug>-verify` deliberately: pass 2 runs in the live
checkout, and build output under `repo` is something the collector then has to
ignore.

**Block 4 no longer pins the deliverable's exact Lua text.** Each mutation is a
regex whose match count is asserted — including the second, which must match
**twice** (both of the store's answers). A mutation that silently failed to apply
aborts the block instead of letting it pass for the wrong reason.

**`kache`.** It is in `~/.cargo/config.toml`, not `cartridge.ctg/.cargo/config.toml`
as spec05 claimed. Block 4's cost rests on it: **28.8 s with kache**; without it
the mutant's build is an ordinary cold build of this crate and its 188 lock
packages, which should be budgeted at minutes — over the 120 s limit. If the gate
is ever run where kache is absent, block 4 needs a shared build cache.

## The gate: four questions

| block | question | what it kills |
|---|---|---|
| 1 | Was the world real, and were the claims' **actions** performed? | cheat D (a minted run directory reports `compositions=0`), cheat F (a daemon and the right arithmetic reports `run=0 launch=0 mcp=0 cold=0`) |
| 2 | Is the instrument the instrument? | shape only; no cheat dies here, by design |
| 3 | Is it formatted? | unformatted deliverables |
| 4 | **Would the test object?** | cheat G (no assertions — the mutant stays green), cheat H (a mutant detector — no receipts) |

## The fixture (`composed/fixture.rs`)

- `Lab::new(name)` builds a disposable project of three toy Lua cartridges
  (`store`, `proxy`, `mcp`), records it with `crate::trust`, and exports a
  **short** `XDG_RUNTIME_DIR`.
- **Short is load-bearing.** `socket::base()` (`src/host/socket.rs:49-53`) joins
  `XDG_RUNTIME_DIR` with `cartridge` then `.filter(|dir| dir.as_os_str().len() < 48)`
  — silently. The fixture **asserts** the length, and `run_dir` **asserts**
  `dir.starts_with(&self.base)` before counting or stopping anything.
- **A node socket must be a socket** (`FileTypeExt::is_socket`).
- `impl Drop for Lab` writes the receipt, then issues `cartridge stop` for every
  root, kills and reaps every spawned child, and removes the roots and its own
  runtime directory.
- Spawned clients get `Stdio::null()`: piped, a host-launched program reparented
  to init keeps the harness's pipes open and nextest reports a leaky pass.
- One receipt file per test; two processes appending to one file interleaved
  into a corrupt line during analysis and the gate's count lied.
- `Lab::command()` is the single place every client process is built, so the
  verbs are tallied there, before the command runs.

### The receipt, all of it fixture-measured

```
test=<name> label=<name> roots=<n> live=<n> compositions=<n> nodes=<n> daemon=<pid>
            probe=<hit|miss|unanswered> probe_node=<same|differs|none>
            run=<n> launch=<n> mcp=<n> call=<n> cold=<n> peak=<n>
            run_node=<same|differs|none> launched=<n|none>
```

`probe` is claim 3's linkage, `run_node` claim 1's, `launched` claim 2's; `cold`
counts attaching verbs issued while `compositions(root) == 0`, evaluated before
the command runs, which is claim 4's subject.

### Measured engine facts

`--yolo` is refused by every subcommand but `run`, `launch` and `daemon`;
`call` and `status` never start a host — only `run`, `launch` and `mcp` attach;
`settled` must require `state == "active"`, because a cartridge left out of the
composition is still listed as `disabled`; `warnings = "deny"`
(`Cargo.toml:74-75`) denies an unused **fixture** method; and nextest is
fail-fast by default, so block 4 passes `--no-fail-fast` or it never sees the
other three objections.

## The four bodies (`composed/mod.rs`)

| test | claim | asserts, beyond `compositions == 1` and `nodes == 3` |
|---|---|---|
| `a_run_against_a_live_daemon_starts_no_node` | 1 | the `run` reply carries the **same `node`** a prior `call` got; daemon pid unchanged |
| `two_launches_and_one_mcp_leave_one_daemon_and_one_node_per_cartridge` | 2 | two `launch` and one `mcp` alive at once, pids ≠ daemon's; the one `proxy` node counted **exactly 2**; a second real project makes the same helpers report `1 + 1 = 2` |
| `one_instance_writes_what_another_reads_off_one_node` | 3 | a separate process ingests `cedar`, another queries it back `hit = true` off the **same node**; a never-ingested word is `hit = false` |
| `two_instances_started_cold_and_concurrently_share_one_daemon` | 4 | starts cold (`compositions == 0` first), two concurrent `run`s, both later calls answered by the same node, one composition after |

Every count is `assert_eq!` against a non-zero expectation. No `<=`, no `>=`.

## Steps

1. Copy `reference/fixture.rs` and `reference/mod.rs` (this PRD's `.state/loop`
   directory) to `.cartridge/tests/unit/src/tests/composed/`. They are
   `rustfmt`-clean at this base; after any edit run `cargo fmt --all`.
2. Add `mod composed;` as the first line of
   `.cartridge/tests/unit/src/tests/mod.rs`.
3. Nothing else. No change under `src/`.

## Acceptance

- [ ] `cargo nextest run --workspace -E 'test(tests::composed::)' --test-threads=1`
      runs exactly 4 tests, all pass, none leaky.
- [ ] Every receipt — written by the fixture in `Drop`, so the body chooses
      nothing — reports `compositions=1 nodes=3`, a non-zero daemon pid,
      `probe=hit probe_node=same` and `run_node=same`; `instances` also
      `launched=2` and `roots=2 live=2`.
- [ ] The receipts name the four claims as actions: `run=2 … cold=0`;
      `launch=2 mcp=1` with `peak ≥ 4`; `call ≥ 7`; `run=3 … cold=2 peak=2`.
- [ ] A mutant of the tree, run in the same path shape and environment, fails
      all four tests AND leaves four receipts reporting `compositions=1 nodes=3`
      with `probe_node=differs run_node=differs` — the fixture's own
      measurements of the mutated world, unforgeable by the body. This is not
      attributed to the four claims' own assertions: block 4 is defeated by a
      body that panics on the mutant tree's own path once the `Lab` exists
      (cheat I, ceiling B18) and still leaves this receipt, because `Drop`
      writes it unconditionally. The backstop for the claims themselves is the
      diff reading of `reference/mod.rs`'s four bodies — one `assert_eq!` per
      claim, no bound, no detector.
- [ ] The fixture asserts its runtime directory survives `socket::base()`'s
      silent 48-character filter, refuses a run directory outside its own base,
      counts only real sockets, and tears down with `cartridge stop` on the panic
      path — no `pkill`, no `killall`.
- [ ] `cargo fmt --all --check` exits 0.

## Verify and Proof

```sh
set -eu
# Outside the repository: a target directory under `repo` is build output the
# collector would have to ignore, and pass 2 runs in the live checkout.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cxbuild-composed}"
# Everything this block writes beyond the build lives under one short scratch
# root that goes away on every exit path. Short is load-bearing: socket::base()
# joins XDG_RUNTIME_DIR with `cartridge` and silently discards the result at 48
# characters, falling back to /tmp/cartridge-<uid>, where this machine's live
# hosts are. A path under CARGO_TARGET_DIR is already too long.
work="/tmp/cxv$$"
rm -rf "$work"
mkdir -p "$work/rt"
trap 'rm -rf "$work"' EXIT
report="$work/receipts"
log="$work/plain.txt"
CARTRIDGE_COMPOSED_REPORT="$report" XDG_RUNTIME_DIR="$work/rt" \
  cargo nextest run --workspace -E 'test(tests::composed::)' --test-threads=1 \
  > "$log" 2>&1 || true

# A filter naming a missing or renamed module exits 0 with "0 tests run"; a
# compile failure prints no census at all. A leaky test left a process holding
# the harness's pipes, which is the opposite of what this PRD proves.
grep -q 'Starting 4 tests' "$log"
grep -q '4 tests run: 4 passed' "$log"
if grep -qn 'leaky' "$log"; then exit 1; fi

# The receipts. Every field is measured by the fixture — the world it walked and
# the verbs it was asked to perform. The body supplies only the label, so it can
# neither author a number nor name an action it did not take.
test -d "$report"
test "$(find "$report" -type f | wc -l | tr -d ' ')" = 4
cat "$report"/* > "$work/receipts.txt"
report="$work/receipts.txt"
test "$(wc -l < "$report" | tr -d ' ')" = 4

# The world: one composition, three nodes, a live daemon, and one node answering
# two separate client processes.
test "$(grep -c 'compositions=1 nodes=3' "$report")" = 4
test "$(grep -c 'probe=hit probe_node=same' "$report")" = 4
test "$(grep -c 'daemon=0 ' "$report")" = 0

# The four claims, as ACTIONS the fixture mediated. A body that never ran the
# verb cannot produce the line.
# Claim 1 — a `run` against a live daemon (cold=0: the daemon was already up).
grep -q 'label=run .* run=2 launch=0 mcp=0 call=[1-9][0-9]* cold=0 ' "$report"
# Claim 2 — two launches and one mcp, against a live daemon, all alive at once.
grep -q 'label=instances .* run=1 launch=2 mcp=1 call=[1-9][0-9]* cold=0 ' "$report"
test "$(sed -n 's/.*label=instances .*peak=\([0-9]*\).*/\1/p' "$report")" -ge 4
# Claim 3 — the cross-process round trip, more than the fixture's own probe.
test "$(sed -n 's/.*label=shared .*call=\([0-9]*\).*/\1/p' "$report")" -ge 7
# Claim 4 — two attaching clients issued against a project with NO composition,
# alive together, ending on one daemon.
grep -q 'label=cold .* run=3 launch=0 mcp=0 call=[1-9][0-9]* cold=2 peak=2' "$report"
# The claim LINKAGES, measured by the fixture: a `run` lands on the node a
# plain `call` already reached, and the ONE proxy node saw both launches.
test "$(grep -c 'run_node=same' "$report")" = 4
grep -q 'label=instances .* launched=2' "$report"
# The negative control: a second real project, measured by the same helpers.
grep -q 'label=instances roots=2 live=2' "$report"
test "$(grep -c 'roots=1 live=1' "$report")" = 3
```

```sh
set -eu
bodies=.cartridge/tests/unit/src/tests/composed/mod.rs
fix=.cartridge/tests/unit/src/tests/composed/fixture.rs
test -f "$bodies"
test -f "$fix"
grep -q '^mod composed;' .cartridge/tests/unit/src/tests/mod.rs
test "$(grep -c '#\[test\]' "$bodies")" = 4

# No bound may stand in for a count, and nothing may be counted in the project's
# own `.cartridge` — the sibling defect this board started from.
if grep -qn '<=' "$bodies"; then exit 1; fi
if grep -qn '>=' "$bodies"; then exit 1; fi
if grep -qn 'join(".cartridge")' "$bodies"; then exit 1; fi

# The body names a label; it never authors a number or a verb the gate reads.
# What the body DID is gated by block 1's receipt, not by a grep here.
if grep -qn 'compositions=' "$bodies"; then exit 1; fi
if grep -qn 'probe=' "$bodies"; then exit 1; fi

# The fixture is the measuring instrument, and its guarantees are effects:
# it asserts the base it actually got, refuses a run directory outside it,
# counts only real sockets, and stops what it started on the panic path.
test "$(grep -c 'CARTRIDGE_COMPOSED_REPORT' "$fix")" = 1
grep -q 'impl Drop for Lab' "$fix"
grep -q '"stop"' "$fix"
grep -q 'as_os_str().len() < 48' "$fix"
grep -q 'dir.starts_with(&self.base)' "$fix"
grep -q 't.is_socket()' "$fix"
# The receipt is the fixture's: it takes a label, never a caller's numbers.
# The receipt is the fixture's alone: it takes no argument, and Drop writes it,
# so no body authors a field; it supplies the label and decides whether a
# `Lab` (and so a receipt) exists.
grep -q 'fn receipt(&mut self)' "$fix"
grep -q 'self.receipt();' "$fix"
if grep -qn 'lab.receipt' "$bodies"; then exit 1; fi
if grep -qn 'tempfile::tempdir()' "$fix"; then exit 1; fi
if grep -qn 'pkill' "$fix"; then exit 1; fi
if grep -qn 'killall' "$fix"; then exit 1; fi
if grep -qn 'pkill' "$bodies"; then exit 1; fi
if grep -qn 'killall' "$bodies"; then exit 1; fi
```

```sh
set -eu
# Outside the repository: a target directory under `repo` is build output the
# collector would have to ignore, and pass 2 runs in the live checkout.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cxbuild-composed}"
cargo fmt --all --check
```

```sh
set -eu
# Block 4 — execute a mutant. The receipt proves the world was real; this proves
# the test would object to a world that is not.
#
# The mutant runs in the SAME path shape and the SAME environment as block 1 —
# the same `/tmp/cxv$$` root, the same variables, the same `--test-threads=1` —
# because a mutant whose run is distinguishable from the real run is just
# another in-band signal for a body to detect.
#
# And it is judged by the MUTANT'S OWN RECEIPTS, not by the exit code: the
# fixture measured a whole composition whose node identity the mutation broke;
# why the body went red is not recorded (B18). `Drop` writes receipts
# unconditionally, so a failing body still leaves one.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cxbuild-composed}"
work="/tmp/cxv$$"
rm -rf "$work"
mkdir -p "$work/rt"
trap 'rm -rf "$work"' EXIT
mutant="$work/tree"
mkdir -p "$mutant"
tar -cf - --exclude ./target --exclude ./.git . | (cd "$mutant" && tar -xf -)
fix="$mutant/.cartridge/tests/unit/src/tests/composed/fixture.rs"
test -f "$fix"

# The toy store stops being ONE node: every call answers with a fresh identity.
# Claims 1, 3 and 4 each assert that two client processes were served by the
# same node, and the fixture's own probe and run_node must report `differs`.
# The one proxy node also miscounts, so claim 2's exact `assert_eq!(launches, 2)`
# goes red — fast, because the body's wait loop breaks on `launches > 1`.
# Each edit is anchored and each anchor is checked: a mutation that silently did
# not apply would make this block pass for the wrong reason.
python3 - "$fix" <<'PY'
import re, sys
path = sys.argv[1]
body = open(path).read()

def edit(text, pattern, replacement, what, expected=1):
    new, n = re.subn(pattern, replacement, text)
    assert n == expected, f"{what}: matched {n} times, expected {expected}"
    return new

# One node identity per node -> one per call.
body = edit(body, r'local node = tostring\(\{\}\)\nlocal seen = \{\}',
            'local seen = {}\nlocal function node() return tostring({}) end',
            "store: per-call identity")
body = edit(body, r'return \{ node = node, hit =',
            'return { node = node(), hit =',
            "store: every answer carries the per-call identity", expected=2)
# The one proxy node miscounts the launches it saw.
body = edit(body, r'count = #launches \}',
            'count = #launches + 2 }',
            "proxy: launch miscount")
open(path, 'w').write(body)
PY

log="$work/mutant.txt"
report="$work/receipts"
CARTRIDGE_COMPOSED_REPORT="$report" XDG_RUNTIME_DIR="$work/rt" \
  CARGO_TARGET_DIR="$work/target" \
  cargo nextest run --manifest-path "$mutant/Cargo.toml" \
  -E 'test(tests::composed::)' --test-threads=1 --no-fail-fast > "$log" 2>&1 || true

# The mutant built and ran, and every one of the four objected.
grep -q 'Starting 4 tests' "$log"
grep -q '4 tests run: 0 passed, 4 failed' "$log"
# The fixture measured a whole composition whose node identity the mutation
# broke; why the body went red is not recorded (B18). Four receipts, every one
# of them.
test -d "$report"
test "$(find "$report" -type f | wc -l | tr -d ' ')" = 4
cat "$report"/* > "$work/receipts.txt"
report="$work/receipts.txt"
test "$(grep -c 'compositions=1 nodes=3' "$report")" = 4
test "$(grep -c 'probe_node=differs' "$report")" = 4
test "$(grep -c 'run_node=differs' "$report")" = 4
test "$(grep -c 'daemon=0 ' "$report")" = 0
```

## Measured evidence

Scratch worktree of `d169293` at `/tmp/cxw`. Every cheat was ported to this
round's fixture and made to compile before being measured. Trees were measured
one at a time; with `--test-threads=1` the back-to-back reddening seen in round 4
did not recur.

| tree | b1 | b2 | b3 | b4 | where it was rejected |
|---|---:|---:|---:|---:|---|
| clean tree (no `composed/`) | **1** | **1** | 0 | **1** | census absent; `test -f bodies` |
| **reference** | **0** | **0** | **0** | **0** | — 4 passed in 7.5 s serial; block 4 28.8 s |
| **reference + stronger assertions** (correct) | **0** | **0** | **0** | **0** | — no false red, re-measured after formatting |
| cheat A — four titles, empty bodies | **1** | 0 | 0 | **1** | b1 `test -d receipts` |
| cheat D — no host; run directory minted through `run_dir` | **1** | 0 | 0 | **1** | b1 `compositions=1 nodes=3` count `0 = 4` |
| cheat F — daemon, one `call`, the arithmetic | **1** | 0 | 0 | **1** | b1 claim-1 verb line |
| cheat G — every verb real, no assertion anywhere | **0** | 0 | 0 | **1** | **b4** — the mutant stays green |
| **cheat H — cheat G plus a mutant detector** | 1\* | 0 | 0 | **1** | **b4 `test -d receipts`** — it panicked before any `Lab` existed, so no `Drop` wrote one |

\* Cheat H's **b1 = 1 is an artefact of my scratch worktree living under
`/tmp/cxw`**: the detector I strengthened also tests `CARGO_MANIFEST_DIR` for
`/tmp/`, true of the worktree and false of a real checkout. In a real checkout
cheat H passes block 1, exactly as the reviewer measured. **Block 4 is its only
genuine rejection**, and it is the one that matters.

Reference receipts:

```
test=run       label=run       roots=1 live=1 compositions=1 nodes=3 daemon=53924 probe=hit probe_node=same run=2 launch=0 mcp=0 call=5 cold=0 peak=1 run_node=same launched=0
test=instances label=instances roots=2 live=2 compositions=1 nodes=3 daemon=54047 probe=hit probe_node=same run=1 launch=2 mcp=1 call=6 cold=0 peak=5 run_node=same launched=2
test=shared    label=shared    roots=1 live=1 compositions=1 nodes=3 daemon=53942 probe=hit probe_node=same run=1 launch=0 mcp=0 call=7 cold=0 peak=1 run_node=same launched=0
test=cold      label=cold      roots=1 live=1 compositions=1 nodes=3 daemon=54029 probe=hit probe_node=same run=3 launch=0 mcp=0 call=6 cold=2 peak=2 run_node=same launched=0
```

The mutant's own receipt for `run`, which is what block 4 reads:

```
test=run label=run roots=1 live=1 compositions=1 nodes=3 daemon=59462 probe=hit probe_node=differs run=2 launch=0 mcp=0 call=5 cold=0 peak=1 run_node=differs launched=2
```

The composition is whole — `compositions=1 nodes=3` — and the only thing that
changed is the thing the mutation broke.

## Remaining risk

- **Block 4's budget depends on `kache`** (`~/.cargo/config.toml`). 28.8 s with
  it; a cold full build without it exceeds 120 s. Stated rather than assumed.
- **The toy profile is not the real 20-cartridge composition** and cannot be from
  a cartridge.ctg lane (`.lanes/` holds sibling symlinks for `auth.ctg`,
  `cartridge.ctg`, `memo.ctg` only, so `../memory.ctg` does not resolve). Every
  per-cartridge sibling disclaimed the composed shape and handed it here.
- **Block 4 does not gate the claims' own assertions (B18).** It rejects a body
  that panics before a `Lab` exists or fails the tree's own
  `0 passed, 4 failed` census; it does not record which assertion inside a
  body went red. The diff reading of `reference/mod.rs`'s four bodies is the
  backstop for the claims themselves.
- `peak` for `instances` is `≥ 4` rather than exact: it counts daemon children
  too, and a fast-exiting client can shift it by one.
- `/bin/sleep` orphans are bounded, not eliminated: `Drop` reaps the
  `cartridge launch` client, not the program the *host* launched, which is
  reparented to init. 20 s, and `Stdio::null()` keeps them out of the leak
  detector.
