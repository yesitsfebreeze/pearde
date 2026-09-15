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
  `just check` reported 5 of 18 targets failed and exited 1; `just test` 6 of 18
  and exited 1; `just smoke` 3 of 3 and exited 1; `just verify` 1 of 1 and
  exited 1. All five gates print one verdict line per target and none stops at
  its first failure. Spec published (`prd specced`); an independent verifier is
  rerunning every acceptance line.
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

## Red targets the gates now name

These belong to later PRDs, not to the gate work. `check`: runtime, memo,
memory, policy, live. `test`: the same five plus prd. `smoke`: policy, proxy,
mcp. `live` is red because of an uncommitted half-edit in
`live.ctg/src/launch.ts` (`Cannot find name 'spawnSync'`), which is inside the
footprint of `@root/the-profile-is-the-orchestration-service`.

## Correction from the verifier, and the fix

The first gate layer silently dropped the composed repository's own
`source-layout` integration test: the development memo ran it at the tail of
its own `all` loop, and the gate now hands that memo one owner at a time. It is
now a `test` target of its own, named `layout`, and it is red on a `cargo
metadata` lookup for the memory package, which belongs to another PRD. `verify`
also lost `CARGO_TARGET_DIR`; it resolves the host the way the runtime memo does
again. Both fixes are inside the footprint, and the spec now guards the layout
target.

## The stale daemon is a human's call

The peer session working in cartridge.ctg confirmed the diagnosis: pid 92897
serves this project from a build older than the uncommitted work in the tree,
its socket no longer writes the token file the command line used to read, and
its authentication path predates the current one. A `cartridge call` built from
this tree therefore speaks a protocol that host does not implement, and
`cartridge run` then finds the address taken. Whoever owns pid 92897 restarting
it against a fresh build clears both. No session here will stop it. That blocks
one box on `the-record-has-one-vocabulary-and-no-shadowed-copies`, one on
`the-profile-is-the-orchestration-service`, and it is why `just verify` is red.

## The record item is worked, verified and committed, and still open

Boxes 1 and 2 are observed green and ticked; box 3 stays open because its named
command cannot be run against the stale daemon. Committed as `f6a4668d` in
prd.ctg and `bc4f5b5` in the composed root. Not collected.

The verifier caught one real defect and it is repaired. The two shadowing
`type/` leaves were deleted on the premise that the shipped copies are
byte-identical; they are not. The workspace `type/type.md` carried the memo file
contract and the qualified-versus-bare wikilink rule, and two grammars cited it
as authority for exactly that. The contract now lives in
`grammar/memo-grammar.md` and `record-grammar.md` cites the grammar. The spec
grew a fifth check that fails if either regresses.

## Next action

Take the re-run gate evidence, write the gate PRD's Result, commit the two
justfiles and attempt `prd collect`. Then dispatch
`@root/the-profile-is-the-orchestration-service`, which overlaps the gate
footprint on `.cartridge/justfile` and the record footprint on
`.cartridge/memos`, so it runs only after both land.
