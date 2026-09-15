# Root board progress

Snapshot: 2026-09-15, coordinator pass 1.

- open: 19 (16 leaves, 3 milestones); deferred 236; done 483; claimed 0
- active claims: none recorded through `prd claim`; the coordinator is working
  `the-gates-run-from-the-root-justfile` in place and has dispatched
  `the-record-has-one-vocabulary-and-no-shadowed-copies` to a worker
- lanes: none

## In flight

- `@root/the-gates-run-from-the-root-justfile` — coordinator. The gate layer is
  written: `.cartridge/justfile` now owns `check`, `test`, `smoke`, `verify` and
  `isolation`, each naming its toolchain first, running its whole target list,
  printing one line per target and exiting non-zero on any failure. `root` is
  derived from `source_directory()`, so `just --justfile .cartridge/justfile`
  resolves the same paths as `just` from the composed root. Observed:
  `just isolation` and `just --justfile .cartridge/justfile isolation` both pass;
  `just check` reported 5 of 18 targets failed and exited 1. `just test` and
  `just smoke` are running.
- `@root/the-record-has-one-vocabulary-and-no-shadowed-copies` — worker,
  probing and specifying.

## Known blockers

- The root repository cannot pass `prd collect` today. `collect` rejects any
  working-tree change outside the PRD footprint, and fifteen submodules carry
  another session's uncommitted work (`agent`, `cartridge`, `docs`, `fs`,
  `gitfs`, `harness`, `live`, `mcp`, `memo`, `policy`, `proxy`, `pty`, `router`,
  `sessions`, `tools`), plus untracked `.obsidian/` and `.yolo-test/`.
- Footprints written as `.cartridge/memos/**` never match: `feet()` resolves the
  literal path and `collect` compares by prefix, so a `**` segment authorises
  nothing. Specs must name real paths.
- `just verify` is red because a host from another session already serves
  `/tmp/cartridge-501/69a3b8e0c7a1/host.sock`. That host was not started here and
  is not being stopped.

## Next action

Finish the gate evidence from the running `just test` and `just smoke`, then
write the Result block and attempt `prd specced` for the gates PRD.
