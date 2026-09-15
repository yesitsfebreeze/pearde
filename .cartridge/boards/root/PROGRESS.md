# Root board progress

Snapshot: 2026-09-15 11:15, coordinator pass 3 (session cartridge-ctg-22).

- done this pass: 1 — `the-record-has-one-vocabulary-and-no-shadowed-copies`
- open: 16 on root; 3 analyzing, 13 waiting on a `needs`
- claims, all by cartridge-ctg-22:
  - `host-tests-hold-under-suite-contention` — analyst reported (spec01
    draft, not published). Red at `f8a2c00`: 3 of 14 main-binary tests, one
    `host.sock is already served` collision in `cli::setup` that poisons the
    `trust_home()` mutex for two more. Held again: a live session began editing
    five host files (`src/host/socket.rs`, `src/host/mod.rs`, `src/cli/args.rs`,
    `src/cli/client.rs`, `src/transport/typed.rs`) at 11:01, on exactly that
    collision. Waiting for it to commit; the draft does not yet meet "never
    process-global" and gets revised against the committed tree.
  - `pty-router-harness-mcp-tests-are-green` and
    `sessions-and-gitfs-tests-are-green` — analysts probing the owners with
    the orphaned 07:13 attempt left in place
- hosts: none started by this session. A `cartridge launch claude` host from
  another session runs from `cartridge.ctg/target/debug`; it is not touched.

## Landed

| item | where |
|---|---|
| `the-gates-run-from-the-root-justfile` | root `585a767` |
| `the-composition-comes-up-without-memory` | root `2cb8cb4`, prd.ctg `a2ece4fb` |
| `collect-checks-the-footprint-not-the-whole-working-tree` | prd.ctg `c0226fe0` |
| `the-profile-is-the-orchestration-service` | root `6ee17d9` and earlier |
| `the-record-has-one-vocabulary-and-no-shadowed-copies` | collected at root `714c088`, prd.ctg `e50d14b0` |

## What changed since pass 2

cartridge.ctg is clean: the two sessions holding it committed (`f8a2c00`), so
the host-tests item is no longer held and is claimed.

The untracked principle memo that held the record item belonged to session
cartridge-ctg-0b, which committed it at root `714c088`; collect then verified
the item.

## Still held, and by what

`pty-router-harness-mcp-tests-are-green` and `sessions-and-gitfs-tests-are-green`:
their footprints carry 22 uncommitted changes written 07:13–07:41 today (two doc
edits at 09:14 and 09:17). They are exactly this work: `CARTRIDGE_HOME` set per
spawned test host in pty, harness, sessions and mcp; rustfmt reflows; gitfs cap
tests pinned to the cap in force instead of a hard-coded 8 MiB; `grant.env`
prefixes in harness and sessions. Three live peer sessions answered "not mine";
the fourth (cartridge-e0) has not answered yet. If no session owns them they
are an abandoned earlier attempt, and the analysts continue from them rather
than starting over.

## Worth deciding, all outside every footprint here

- Two acceptance boxes name `cartridge call memo '{"op":"index"}'`, which
  cannot work: a native memo request must carry `cwd`, or the service answers
  `trusted memo cwd required`.
- `.cartridge/justfile` still has a `sweep` recipe; `cartridge sweep` is gone.
- `.cartridge/config.lua` carries a `memory` block that settles nothing.
- `memo.ctg`'s docs still tell a reader to run `cartridge --yolo run tui`.
- Twelve cartridges each ship an identical `type/note.md` and `type/type.md`,
  so `memo index` reports no single declaration for either kind.
- `.obsidian/` and `.yolo-test/` are untracked in the composed root.
- The composed repository's `source-layout` test is red, on a `cargo metadata`
  lookup for the memory package.

## Next action

Take the host-tests analyst report, spec and implement it. Once cartridge-e0
answers (or stays silent through this item), claim the two remaining suite
items and continue from the orphaned attempts.
