# Root board progress

Snapshot: 2026-09-15, end of coordinator pass 2.

- done this pass: 4 — the gate layer, the workspace record, the composition
  coming up without memory, and the profile itself
- open: 17 on root; 1 specced and held, 3 dispatchable but footprint-held,
  13 waiting on a `needs`
- claims: none. No lane. No host running that this session started.

## Landed

| item | where |
|---|---|
| `the-gates-run-from-the-root-justfile` | root `585a767` |
| `the-composition-comes-up-without-memory` | root `2cb8cb4`, prd.ctg `a2ece4fb` |
| `collect-checks-the-footprint-not-the-whole-working-tree` | prd.ctg `c0226fe0` |
| `the-profile-is-the-orchestration-service` | root `6ee17d9` and earlier |

## The two things that mattered

The composition was down and nobody had said so. Taking `memory` out of the
profile left `prd.ctg/cartridge.json` still declaring it a hard need, so the
host refused to start `prd` and memo, harness, agent, live, mcp and proxy all
stalled behind it. Every host error recorded earlier in the day was downstream
of that; the `unknown token` and `already served` messages were a dead
runtime's leftover socket, not authentication. With the declaration gone,
`cartridge status` reports 19 cartridges with none failed or waiting, `live`
answers `running` and harness `ring` answers `disabled`.

Nothing could be collected, and that was the tooling, not the work. `collect`
asked git for the status of the whole repository and refused on the first entry
outside the footprint, which in a composed repository of eighteen submodules
worked by concurrent sessions is never satisfiable. The question carries a
pathspec now. What may enter a commit did not change: only footprint paths were
ever staged, the committed revision is still checked in full by
`assertFootprint`, and a dirty path inside the footprint still refuses. Three
collections that had been refusing went through immediately against a tree
carrying 23 unrelated dirty entries, and those entries were untouched
afterwards.

## Still open, and why

`the-record-has-one-vocabulary-and-no-shadowed-copies` — specced, every box
green, committed as `f6a4668d` and `bc4f5b5`. It refuses to collect for the
right reason now: `.cartridge/memos/principle/no-redundant-comments.md`, written
at 10:47 today, sits untracked inside its footprint. It is not this session's
and the review-and-fix session has confirmed it is not theirs either; the
owning session has been asked to commit it. That one file is the whole
remaining distance.

`host-tests-hold-under-suite-contention`, `pty-router-harness-mcp-tests-are-green`
and `sessions-and-gitfs-tests-are-green` — dispatchable, not started. Their
footprints hold 30, 9 and 13 uncommitted changes belonging to other sessions.

cartridge.ctg is held by two of them. One is running a review-and-fix pass and
reports its own work finished and green: formatting and clippy clean, 152
library tests passing, and 15 of 15 binaries green when its files alone are
applied to `891a2c2` in a separate worktree. It is holding its commit on
purpose, because four CLI tests are red from the other session's host work and
committing would put that red on main. The other session holds the host files
and is working those four with the diagnosis in hand. This is a queue, not a
stall, and it resolves without anyone here intervening.

Judging whether a suite is green at a revision that does not exist yet is not
possible, and dispatching into those trees would either build on moving work
or overwrite it.

Everything else waits on those.

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
  lookup for the memory package. It is a `test` gate target now, so it is
  visible rather than skipped.

## Next action

Wait for the other sessions to commit, then collect the record item and take
the three suite items.
