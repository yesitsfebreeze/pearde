# @memory/the-cold-tier-scales-past-a-linear-scan/the-memory-cartridge-integration-tests-trust-the-project-they-boot review history

Plan: @memory/the-cold-tier-scales-past-a-linear-scan/the-memory-cartridge-integration-tests-trust-the-project-they-boot (prd.md, specs/spec01.md).
Scope: leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: none (split 2026-09-16 with none used).

## Round 1 — 2026-09-19

Plan: @memory/the-cold-tier-scales-past-a-linear-scan/the-memory-cartridge-integration-tests-trust-the-project-they-boot
Reviewer: fresh reviewer agent, coordinator-5c-7 (independent; did not write the plan).
Inherited rounds: none.

Presented revision:

| Input | SHA-256 |
| --- | --- |
| prd.md | 7b2056cd01d0d17b04f954038b4162c2148e2b719fbc7c9a84487ea735cee2ec |
| specs/spec01.md | 31810c843d0d9e4b0b93dab27aa57a84638f1746dda53a847b19464cbbd9a3cc |
| .state/loop/integration-trust/attempt-2.patch | a5cd553d5d5487d17979ba75595b6bac18b69d3ce8ac5d0ebd2f3370195178b2 |
| Code | memory.ctg 3432b13; cartridge.ctg HEAD 804a08b, release binary 2026-09-19 13:12 |

### Validation (executed by this reviewer)

Scratch copy: `git archive 3432b13` of memory.ctg in `scratchpad/it-r1/memory.ctg`, with sibling
symlinks `cartridge.ctg` and `memo.ctg` pointing at the live checkouts. The test block ran
exactly as `runTestBlock` runs it (`sh -eu -c 'PRD_TEST_REPORT=…; exec >log 2>&1; set --\n<run>'`),
with `env -u CARGO_TARGET_DIR CARTRIDGE_YOLO=1` to mimic a YOLO collector. Nothing was built in
memory.ctg/target. The live memory.ctg is unchanged at 3432b13.

1. Base, cold target: exit 0 in 49 s. 3 PASS lines; `an_inherited_yolo_…` absent, so
   `runTestBlock` reports "no pass for" it and the block **fails at base**. It cannot pass vacuously
   because the name is pinned. This also confirms the PRD's premise: under YOLO the 3 existing
   tests pass.
2. attempt-2.patch (`git apply` clean), warm: exit 0 in 5 s, 4 PASS lines. The nextest format
   `PASS [ 0.069s] (1/4) memory::cartridge <name>` matches `passedTests`' regex.
3. Mutant: `.env_remove("CARTRIDGE_YOLO")` removed. Exit 100, and the new test FAILs at 10.04 s.
   **The box-2 claim is reproduced.**
4. Extra mutant: the daemon spawn in `Base::boot` bypasses `base_command` (so it inherits YOLO),
   and `trust` targets the wrong directory. The 3 existing tests FAIL ("profile did not come up")
   because the `cli` spawn, which still strips YOLO, refuses the untrusted project. The new test
   stays green, so the "every spawn goes through base_command" property is guarded only
   indirectly. See N2.
5. Isolation: the scratch `target/` holds only `integration-trust-verify`. The nested
   `cargo build -p memory_cartridge` in `module()` inherits `CARGO_TARGET_DIR`, so pass 2 does not
   write `target/debug` of the live memory.ctg.
6. Engine: `testBlock` takes the `run:` value verbatim and splices it after `set --` into
   `sh -eu -c`. A leading `VAR="${…:-$PWD/…}"` prefix assignment with expansion is valid, and `PWD`
   is set, so `-u` is safe. `verify()` runs only the spec's blocks, so the PRD body's copy is
   informational.
7. Precondition: `.lanes/cartridge.ctg` is a symlink to the live checkout, and
   `../cartridge.ctg/target/release/cartridge` exists (-x). The path is the same one the fixture's
   `base()` reads through `CARGO_MANIFEST_DIR` (the root package is at the repo root), so it holds
   from both the lane and the repo.
8. Stale release: trust code (`src/trust`) last changed 04aae7f on Sep 16, before the 13:12 release
   build. `verify` is at trust/mod.rs:93–94, and the wording "is in no trusted project" is at :151,
   so the release binary is current for this behaviour. The host's release-over-debug dylib
   preference does not apply, because the fixture execs the binary by path.
9. `~/.cartridge`: after a mark, `find ~/.cartridge -newer mark -type f` found **2** files. Both are
   trust records for `/private/tmp/cx1807-instances-0` and `/private/tmp/cx1247-cold-0`, written by
   a concurrent process (mcp fixtures). None names `cartridges/memory` (grep exit 1). The fixture
   left nothing, but the spec's stated check method false-fails on this machine. See N1.
10. Precedent `src/hub/src/lib.rs:121` `.env_remove(identity::TAKEOVER_ENV)` exists.

### Scores

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Real remaining gap (YOLO sessions make the trust step unprovable), correctly restated after f2319c5, one outcome, one file. −2: the PRD says the test "proves the fixture's spawns do not inherit it", but it proves only `base_command` (N2). |
| Ownership and reuse | 19 | One owner, one footprint file, and it reuses the in-repo env_remove precedent. No base change. −1: none material. |
| Dependencies and implementable slices | 18 | Base binary prerequisite gated by a `test -x` that works in both passes. attempt-2 applies and is small. −2: the precondition checks existence, not that the release build contains the trust behaviour (fine today, per item 8). |
| Observable acceptance and baseline evidence | 18 | Box 1 is an executed test that fails at base. Box 2 mutant reproduced. −2: the box-3 check method ("no file newer than a mark") is unsound with concurrent base users (N1). |
| Failure, recovery and compatibility | 18 | Isolated target, no footprint writes, and the new test's failure mode is bounded (10 s). −2: both passes are cold (~50 s each, since the live repo has no `target/integration-trust-verify`), with nested-cargo lock waits, a 2.4× margin under load (N3). `set_var` would need `unsafe` on edition 2024 (N4). |
| **Total** | **91** / 100 | |

### Findings

- **N1 (non-blocking).** The box-3 check "no file under `~/.cartridge` is newer than a mark" is
  false-positive on this machine. Concurrent tests write `~/.cartridge/trust/*.json` (item 9). Fix:
  reword the spec's box 3 and its Verify note to "no trust record under `~/.cartridge/trust` names a
  path containing `cartridges/memory` or the run's tempdir, written after the mark". Keep it
  assigned to the diff reviewer. Optionally, pin it in-test: after `Base::boot`, assert that no file
  in `$HOME/.cartridge/trust` mentions `dir`.
- **N2 (non-blocking).** The new test pins `base_command`, not that `Base::boot`/`Base::cli` use it.
  Mutant 4 shows the `cli` spawn indirectly catches a daemon spawn that bypasses the helper. A
  bypass on all three spawns would pass all 4 tests under YOLO. Fix: soften the PRD's wording to
  "proves `base_command` strips it", and name spec step 2's "`Command::new(base())` only in
  `base_command`" as a diff-reviewer check.
- **N3 (non-blocking).** Timing: measured 49 s cold here and 53 s in the analyst's run, per pass.
  Pass 2 in the live repo is also cold. Record in the spec that both passes are cold, and that a
  timeout under heavy parallel cargo load should be rerun alone, not answered by loosening the gate.
- **N4 (non-blocking).** `std::env::set_var` is safe only on edition 2021 (workspace edition is
  2021 today). Add a one-line comment in the test, or note it in the spec, so an edition bump fails
  to compile loudly rather than being "fixed" by deleting the line.

No blocking findings. The Verify fails at base, the mutant is real, targets are isolated and
relative, and the precondition holds from the lane and the repo.

Disposition: keep; proceed to implementation with attempt-2.patch. N1/N2 wording can be folded in
without a new round (they change no gate).
Result: PASS. Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.

VERDICT: PASS
