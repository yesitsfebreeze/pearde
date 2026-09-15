# Root board progress

Snapshot: 2026-09-15, coordinator pass 2.

- open: 20 on root (16 leaves, 3 milestones, 1 child added this pass)
- every box of three items is now observed green; none is collected
- claims: none through `prd claim`; the coordinator worked the gates item and
  the new child in place, and dispatched the other two to workers
- lanes: none. No host is running that this session started.

## What moved this pass

`the-gates-run-from-the-root-justfile` — specced, implemented, verified. All
five gates run from the composed root, name their toolchain first, run the whole
target list, print one verdict line per target and exit non-zero on any failure.
`just --justfile .cartridge/justfile check` works. A verifier caught that the
first version silently dropped the composed repository's own `source-layout`
test, which used to ride at the tail of an owner loop; it is a `test` target
named `layout` now, and red for a reason of its own. `verify` honours
`CARGO_TARGET_DIR` again. Not yet committed: the two justfiles are the only
uncommitted work this session holds.

`the-record-has-one-vocabulary-and-no-shadowed-copies` — all three boxes green.
Committed as `f6a4668d` in prd.ctg and `bc4f5b5` in the root.

`the-profile-is-the-orchestration-service/the-composition-comes-up-without-memory`
— new, found by starting a host. Specced, fixed, all boxes green. Committed as
`a2ece4fb` in prd.ctg and `2cb8cb4` in the root.

`the-profile-is-the-orchestration-service` — all four boxes green. Its
`supersedes:` frontmatter named one of three decisions and now names all three;
`live.ctg/src/launch.ts` called `spawnSync` without importing it, fixed in
live.ctg `939dddb`.

## The composition runs again

It had been down. `prd.ctg/cartridge.json` still declared `needs: ["memory"]`
after the profile stopped composing memory, so the host refused to start `prd`
and memo, harness, agent, live, mcp and proxy all stalled behind it. The
`unknown token` and `already served` errors earlier in the day were a separate
and smaller thing: a dead runtime had left its socket file behind. Clearing the
stale file and starting a host exposed the real cause. With the declaration
gone, `cartridge status` reports 19 cartridges and none failed or waiting,
`live` answers `running` and harness `ring` answers `disabled`.

## The one blocker that needs a human

Nothing on this board can be collected. `prd collect` refuses when the composed
root's working tree holds any change outside the PRD's footprint, and the tree
holds fourteen submodules carrying other sessions' uncommitted work plus two
untracked directories:

```
$ just prd collect the-composition-comes-up-without-memory --board root
changed path is outside the PRD footprint: .cartridge/justfile

$ git status --porcelain=v1 -z --untracked-files=all | tr '\0' '\n'
 M .cartridge/justfile
 M agent.ctg
 M cartridge.ctg
 M docs.ctg
 M fs.ctg
 M gitfs.ctg
 M harness.ctg
 M justfile
 M mcp.ctg
 M memo.ctg
 M policy.ctg
 M proxy.ctg
 M pty.ctg
 M router.ctg
 M sessions.ctg
 M tools.ctg
?? .obsidian/...
?? .yolo-test/...
```

Three ways out, and the choice is the board owner's. The other sessions commit
their submodule work. Or `.gitignore` gains `.obsidian/` and `.yolo-test/`.
Or `collect` stops conflating two different things: that the commit touches
only the footprint, which is right, and that the whole working tree is clean,
which no repository of eighteen submodules with concurrent sessions will ever
be. Only the third is a lasting fix, and it is a change to prd.ctg's own
engine, outside every footprint on this board.

## Two acceptance boxes are written against a call that does not exist

`cartridge call memo '{"op":"index"}'` cannot work on any host:
`memo.ctg/src/service.rs:455` requires a native memo request to carry `cwd` and
answers `trusted memo cwd required` without it. The working call adds
`"cwd":"/Users/feb/dev/cartridge"`. Both boxes that name it should be reworded.

## Smaller things found and left alone, each outside every footprint

- `.cartridge/justfile` still has a `sweep` recipe; `cartridge sweep` was removed.
- `.cartridge/config.lua` carries a `memory` block that settles nothing.
- `memo.ctg`'s docs still tell a reader to run `cartridge --yolo run tui`.
- Each of twelve cartridges ships its own identical `type/note.md` and
  `type/type.md`, so `memo index` reports no single declaration for either kind.
- `just test prd` is red on six pre-existing cases: the board's own `deferred`
  state missing from an allowed-state list, a migration manifest count, and four
  statusline cases.

## Where the pass ended

The two justfiles landed as `53b25f2` in the composed root, with the gate
evidence at that revision: `check` 3 of 18 red, `test` 7 of 19 red, `smoke` 3
of 3 red, `verify` 1 of 1 red, `isolation` green, each printing one verdict
line per target and exiting non-zero. `check live` and `check runtime` turned
green during the session and the gate reported it without being asked.

All three worked items then refused to collect at the same line:

```
$ just prd collect the-gates-run-from-the-root-justfile --board root
changed path is outside the PRD footprint: agent.ctg
$ just prd collect the-record-has-one-vocabulary-and-no-shadowed-copies --board root
changed path is outside the PRD footprint: agent.ctg
$ just prd collect the-profile-is-the-orchestration-service/the-composition-comes-up-without-memory --board root
changed path is outside the PRD footprint: agent.ctg
```

That is now its own item,
`@root/collect-checks-the-footprint-not-the-whole-working-tree`, which names the
one line in `prd.ctg/src/lifecycle.ts` and why narrowing the scan is the only
lasting fix. It is dispatchable, but it changes the engine that decides whether
work may land, so it is the board owner's call rather than a coordinator's.

## Next action

The board owner decides on the collect item. Until then nothing lands, and
four items sit dispatchable with green boxes and committed work.
