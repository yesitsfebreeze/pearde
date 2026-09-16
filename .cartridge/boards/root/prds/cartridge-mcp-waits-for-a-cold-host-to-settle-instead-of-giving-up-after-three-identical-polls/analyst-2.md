# analyst-2 — bounded revision after review round 1 (84/100)

Verdict: **SPECCED** (revision). `specs/spec01.md` revised in place; `prd.md` body
edited in two places; **`attempt-1.patch` is unchanged** — the fix, the deadline
argument and the prototype were upheld, so there is no `attempt-2.patch`. The
patch still applies clean to a `63ff234` archive (`1 file changed, 41 insertions(+),
19 deletions(-)`). Footprint unchanged.

Revision base: root `b4c3dfd`, `cartridge.ctg` `63ff234`.

## The blocking finding — how it is closed

**Cause.** The round-1 fixture built one temp project root *before* the loop and
reaped only the daemon between runs. Runs 2-5 were page-warm and could not fail,
so the whole box rested on run 1, and an unpatched binary passed it in 2 of 3
attempts.

**Fix, in two parts.**

1. **A fresh project root inside the loop.** The fixture's setup is now a
   `makeRoot()` function called at the top of each iteration: it mints its own
   `mktemp -d`, writes `init.lua`/`config.lua`, re-copies the snapshot cartridges
   with their dylibs, and the iteration's `finally` reaps that root's daemon *and*
   `rm -rf`s the root. No run inherits another's page cache, dylib residency or
   daemon state. Observable proof that this changed the fixture's behaviour:
   unpatched failures now land on runs 1, 2, 3, 4 and 5 across attempts, where
   before they only ever landed on run 1.
2. **Fifteen cold runs, split 8 + 7 across two blocks.** Measured per-run failure
   rate on an unpatched binary: **31 of 108 cold runs (29 %)**. Five independent
   cold runs would still let an unpatched tree through at 0.71⁵ ≈ 18 % — and did,
   once in five attempts, measured. Fifteen give 0.71¹⁵ ≈ 0.6 %, under the 1 %
   the reviewer asked for. They are split because the engine kills a block at
   120 s and 8 runs measure 31-41 s here; one 15-run block would leave no
   headroom. Box 1 is green only when **both** blocks exit 0.

Spec Acceptance box 1 now reads "15 of 15 … each run in its own freshly built
project root". The PRD's own box 1 ("5 of 5") is left untouched — the spec
strengthens it, and Acceptance boxes are the coordinator's.

### Every observed exit code, fixed blocks against an unpatched binary

Blocks extracted verbatim from the revised `spec01.md` and run as `sh -eu <file>`
with cwd = repo root, each bounded by a 150 s `perl` alarm (no `timeout(1)` on
this machine).

Binary A = built from a clean `git archive 63ff234` in an isolated
`CARGO_TARGET_DIR`. Binary B = built by Verify block 2 itself from the live
checkout (see "Observation" below — a parallel session had edited that checkout
outside `settle_remote`, so A is the authoritative baseline; B is reported for
completeness and is unpatched with respect to this fix either way).

| binary | attempt | block 4 (8 runs) | block 5 (7 runs) | box 1 |
| --- | --- | --- | --- | --- |
| A | 1 | **exit 1** — `1 of 8 runs wrong` | **exit 1** — `1 of 7 runs wrong` | RED |
| A | 2 | **exit 1** — `2 of 8 runs wrong` | **exit 1** — `2 of 7 runs wrong` | RED |
| A | 3 | **exit 1** — `3 of 8 runs wrong` | **exit 1** — `1 of 7 runs wrong` | RED |
| B | 1 | **exit 1** — `2 of 8 runs wrong` | **exit 1** — `2 of 7 runs wrong` | RED |
| B | 2 | **exit 1** — `6 of 8 runs wrong` | **exit 1** — `3 of 7 runs wrong` | RED |
| B | 3 | **exit 1** — `3 of 8 runs wrong` | **exit 0** — `7/7 ok` | RED |
| B | 4 | **exit 1** | **exit 1** | RED |
| B | 5 | **exit 1** | **exit 1** | RED |

**Box 1 is RED in 8 of 8 attempts against an unpatched binary.** Block 4 exited 1
in 8 of 8; block 5 exited 1 in 7 of 8 — the single `7/7 ok` is the measured
reason the box needs both blocks (a 7-run block alone passes ≈ 9 % of the time).

Against the **patched** binary (same archive, patch applied, isolated target dir):
block 4 **exit 0** `8/8 ok` in 31 s, block 5 **exit 0** `7/7 ok` in 26 s, block 6
(untrusted) **exit 0**, both runs failing in 2.0 s naming `mcp`. 0 failures of 35
cold runs.

Earlier, before the 8+7 split, the same fresh-root fixture at 5 runs was run 5
times against binary A: exit **1, 1, 1, 1, 0** (`3/5`, `1/5`, `1/5`, `1/5` wrong,
then `5/5 ok`). That 1-in-5 false green is what sized the box at 15.

## The four non-blocking findings

| # | finding | where it now lives |
| --- | --- | --- |
| 2 | baseline restated as probabilistic | `spec01.md` → Context, new paragraph "**The baseline is probabilistic, not deterministic — corrected in round 2**" (round-1 reviewer's 5 of 8 plus this round's 31 of 108 = 29 %, and the correction that what decides a run is whether any ~300 ms window passes with no state change, not the 300 ms/1.6 s margin); `spec01.md` → "Why box 1 discriminates", which replaces "Why box 1 is not a coin flip" and drops its two wrong bullets; `prd.md` body → Outcome ("3 of 3 as first reported, and about one cold run in three on independent re-measurement") and a "**Round 2 correction**" paragraph appended to the Planning note. Frontmatter and Acceptance boxes untouched. |
| 3 | `ok = out.includes('"tools"')` passes on an empty list | `spec01.md` → the fixture now parses the `id: 2` JSON-RPC response, requires a non-empty `result.tools`, **and** requires its length to equal the same call made against the now-settled daemon in the same root. Acceptance box 1 states this. Measured: 19 tools cold and 19 settled on every passing run; a failing cold run prints `cold=-1 settled=19`. |
| 4 | 60 s worst-case cost of the new wait | `spec01.md` → "Option chosen", new paragraph "**Accepted cost of deleting the shortcut**": an unserved key plus a cartridge stuck `starting`/`waiting` now waits to `host.startup_timeout_secs` (60 s) where it returned in ~300 ms. Named as bounded and accepted, with the reason it did not appear in either degraded composition measured (trust-refused cartridges go `failed`, so `!starting && !empty` still returns at once; 1.6-2.8 s). Also summarised in the PRD's round-2 correction paragraph. |
| 5 | `kache` build-cache assumption behind the 120 s budget | `spec01.md` → the comment above the Verify blocks now lists every block's measured time and states that the 8.9 s/11.5 s build numbers assume `rustc-wrapper = "kache"`, **which lives in `~/.cargo/config.toml` and not in this repo** (verified), so a host or CI without it needs `$C` pre-warmed outside the block. The same comment names why blocks 2-3 set `CARGO_TARGET_DIR` unconditionally rather than in the template's `${CARGO_TARGET_DIR:-…}` form (the fixture must run the binary those blocks just built). Finding 5's second half — `Cargo.lock` inside the footprint — is fixed rather than merely named: block 2 now passes `cargo build --locked`, which fails loudly instead of refreshing the lock and aborting pass 2 with "source footprint changed". |

Free extras taken while in the file: the reviewer's −1 for never naming
`Host::settled` is closed in "Option chosen" (one sentence naming
`src/host/run.rs:12` as the reason `verify_timeout()`'s three callers are right
to keep their budget), and the Proof section gained a round-2 measurement table
beside the round-1 prototype table.

## What did not change

- `attempt-1.patch` — byte-identical, still the whole implementation.
- The footprint (`cartridge.ctg`, `cartridge.ctg/src/cli/host.rs`).
- Verify block 1 (source guards). Re-checked this round: **exit 1** on the
  unpatched tree naming the shortcut, **exit 0** on the patched tree. Round 1
  already proved all eight patterns discriminate individually; none were touched.
- Verify block 3 and blocks 7-9 (`just check cartridge`, `just test cartridge`,
  `just test lifecycle`), which round 1 ran green and this revision did not edit.
- The no-lane landing shape, the overlap section and the remaining-work section.

## Commands, with cwd and exit code

| cwd | command | exit |
| --- | --- | --- |
| repo | `git rev-parse HEAD` → `b4c3dfd`, `git -C cartridge.ctg rev-parse HEAD` → `63ff234` | 0 |
| repo | `git -C cartridge.ctg status --porcelain` (at start) — empty | 0 |
| scratch | `git -C cartridge.ctg archive 63ff234 \| tar -x` ×2, sibling `*.ctg` symlinks | 0 |
| scratch/patched/cartridge.ctg | `patch -p1 < attempt-1.patch` | 0, "1 file changed, 41 insertions(+), 19 deletions(-)" |
| scratch/head | `cargo build --bin cartridge --manifest-path cartridge.ctg/Cargo.toml`, `CARGO_TARGET_DIR=scratch/target-head` | 0, 9.2 s |
| scratch/patched | same, `CARGO_TARGET_DIR=scratch/target-patched` | 0, 5.1 s |
| scratch/head | Verify block 1 (source guards) | **1** — "settle_remote still ends the wait on three identical polls" |
| scratch/patched | Verify block 1 | **0** — `source guards ok` |
| scratch (no `cartridge.ctg`) | Verify block 1 | **1** — `test -f` (round 1; unchanged block) |
| repo | Verify block 1 (live checkout, unpatched) | **1** — names the shortcut |
| scratch/patched | `cargo build --locked --bin cartridge --manifest-path cartridge.ctg/Cargo.toml` | 0, 9.4 s |
| repo | `cargo build --locked --quiet --bin cartridge --manifest-path cartridge.ctg/Cargo.toml`, isolated target dir | 0 |
| repo | Verify block 2 (with `--locked`) | 0, 1.0 s and 3.1 s |
| repo | Verify block 3 (mcp/memo dylibs) | 0, 0.1 s (cache warm) |
| repo | draft fixture, 5 runs, binary A ×5 | **1, 1, 1, 1, 0** |
| repo | draft fixture, 8 runs, binary A ×3 | **1, 1, 1** (`3/8`, `2/8`, `2/8` wrong) |
| repo | draft fixture, 7 runs, binary A ×2 | **1, 1** (`5/7`, `2/7` wrong) |
| repo | draft fixture, 8 runs then 7 runs, patched | **0, 0** (`8/8 ok` 30 s, `7/7 ok` 32 s) |
| repo | Verify block 4 verbatim, binary B ×5 | **1, 1, 1, 1, 1** |
| repo | Verify block 5 verbatim, binary B ×5 | **1, 1, 0, 1, 1** |
| repo | Verify block 4 verbatim, binary A ×3 | **1, 1, 1** |
| repo | Verify block 5 verbatim, binary A ×3 | **1, 1, 1** |
| repo | Verify block 4 verbatim, patched | **0** — `8/8 ok`, 31 s |
| repo | Verify block 5 verbatim, patched | **0** — `7/7 ok`, 26 s |
| repo | Verify block 6 verbatim (untrusted), patched | **0** — 2.0 s and 2.0 s, naming `mcp`, 6 s |
| repo | `grep -rn 'rustc-wrapper\|kache' .cargo/config.toml cartridge.ctg/.cargo/config.toml ~/.cargo/config.toml` | 0 — only `~/.cargo/config.toml:4` |
| repo | re-extract the 9 `sh` blocks from the revised spec; 0 ticked boxes | 0 |

Every `cargo` command used a `CARGO_TARGET_DIR` under the session scratchpad or
`$HOME/.cache/cartridge-cold-mcp`; no live `target/` was written. Every cold probe
used a scratch `CARTRIDGE_HOME`, a `mktemp -d` project root and a binary outside
the live tree. Block scripts, probe files and the two scratch trees live in
`…/scratchpad/revise-cold-mcp-settle/`. No `prd` state operation, no `git add`, no
commit, no push.

## Observation for the coordinator — not caused by this revision

Partway through this revision the live `cartridge.ctg` checkout went **dirty**
and the live project daemon **disappeared**:

- `git -C cartridge.ctg status --porcelain` was empty at the start and at
  15:40-ish, then showed 8 modified files at ~15:56:
  `.cartridge/settings.json`, `docs/architecture.txt`, `src/cli/args.rs`,
  `src/cli/host.rs`, `src/cli/mod.rs`, `src/host/mod.rs`, `src/host/socket.rs`,
  `src/settings/host.rs` (+115/−3). File mtimes 15:54-15:56.
- `pgrep -f 'cartridge --dir /Users/feb/dev/cartridge'` now returns nothing; the
  pid 8772 that round 1 recorded is gone.

This is not mine: my only writes were to `prd.ctg` markdown and to scratch
directories, and every build used an isolated `CARGO_TARGET_DIR`. The changes
look like another session's daemon/socket work — `src/cli/host.rs` still contains
`stable >= 3`, so they are not this PRD's fix. I did not act on it. Two
consequences worth knowing:

1. **`src/cli/host.rs` is in this PRD's footprint and is currently dirty in the
   live checkout from work that is not this PRD.** The implementer will collide
   unless that is resolved first.
2. Five of my eight verbatim block attempts used binary B, built by Verify block 2
   from that checkout. Binary A (clean `63ff234` archive) reproduces the same
   verdict — box 1 RED 3 of 3 — so the conclusion does not rest on B.

## Remaining uncertainty

- The 29 % per-run rate is this machine, this composition. On a much faster or
  much slower host the rate moves and so does the false-green probability; the
  spec states the rate and the arithmetic so a re-reviewer can re-derive it.
- Blocks 4 and 5 take ~31 s and ~26 s of a 120 s budget here. A host ~3× slower
  would exceed it; that is named in the block-budget comment together with the
  `kache` assumption, and the split into two blocks is what buys the margin.
