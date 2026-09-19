---
complexity:
footprint:
  - <actual canonical path>
---

# specNN — <one implementable goal>

## Acceptance

- [ ] <Observable behavior with an independent check.>

## Verify and Proof

<!--
How collect runs these blocks (engine facts, src/lifecycle.ts collect/verify):
- Each sh/bash/shell block runs as `sh -eu -c`, 120 s limit, empty stdin, the
  collector's environment.
- It runs twice: first with cwd = the lane, a worktree of the PRD's `repo` at
  `prd.ctg/.cartridge/boards/<board>/.lanes/<slug>`; then, after the
  fast-forward, with cwd = `repo` itself. With no lane it runs once, in `repo`.
- A lane of a superproject holds each submodule as a detached worktree of the
  live submodule at the commit HEAD pins, so pass 1 reads and builds the
  pinned siblings, never their dirty working trees.
- Paths are relative to the repo root. Never `cd` to an absolute checkout, or
  pass 1 tests the wrong tree. `../<sibling>.ctg` does not resolve from the
  lane either; name absolute tools (e.g. CARTRIDGE_BIN) with an env default.
- Pass 2 runs in the live checkout. The host hot-restarts a cartridge when its
  target/debug dylib changes, so every cargo block first sets
  `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/<slug>-verify}"`.
- A block must not write inside the footprint. In the lane pass, collect
  commits such writes; in pass 2 they abort collection with "source footprint
  changed during integrated verification". Write scratch output elsewhere.
- Gate behaviour with a `test` block, not a hand-rolled census: one `run:`
  line, then one `pass:` line per test that must pass. Collect requires exit 0
  AND the runner reporting each name as passed. It reads cargo
  (`test a::b::name ... ok`) and nextest `PASS` lines from the output, and a
  JUnit report written to `$PRD_TEST_REPORT` (bun: `--reporter=junit
  --reporter-outfile="$PRD_TEST_REPORT"`). A name matches exactly or as the
  last `::` segment. It pins the name, not the body; the diff reviewer is the
  backstop for the body.
-->

```sh
<Probed commands, relative to the repo root, with failure propagation.>
```

```test
run: <test command, e.g. cargo test -p <crate> --lib>
pass: <test name>
```
