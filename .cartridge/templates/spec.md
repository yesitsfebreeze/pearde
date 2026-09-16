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
- Paths are relative to the repo root. Never `cd` to an absolute checkout, or
  pass 1 tests the wrong tree. `../<sibling>.ctg` does not resolve from the
  lane either; name absolute tools (e.g. CARTRIDGE_BIN) with an env default.
- Pass 2 runs in the live checkout. The host hot-restarts a cartridge when its
  target/debug dylib changes, so every cargo block first sets
  `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/<slug>-verify}"`.
- A block must not write inside the footprint. In the lane pass, collect
  commits such writes; in pass 2 they abort collection with "source footprint
  changed during integrated verification". Write scratch output elsewhere.
-->

```sh
<Probed commands, relative to the repo root, with failure propagation.>
```
