---
state: "done"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 1
date: "2026-09-15"
footprint:
- "justfile"
- ".cartridge/justfile"
- ".cartridge/tools/memo-run"
- ".cartridge/memos/routine/cartridge-development.md"
- ".cartridge/memos/routine/cartridge-smoke.md"
commit: "585a7677d6714a9c15d6fe92a2e6db13538c5ae4"
---

# The gates run from the root justfile

## Outcome

Every gate is one recipe from the composed root that names each target's result and fails loudly.

## Acceptance

- [x] `just check`, `just test`, `just smoke`, `just verify`, `just isolation` run from `/Users/feb/dev/cartridge`, print one line per target with pass or fail, and exit non-zero on any failure.
- [x] `just --justfile .cartridge/justfile check` works or refuses with the reason (2026-09-15: `.cartridge/.cartridge/tools/memo-run: No such file or directory`).
- [x] A missing toolchain (cargo, cargo-nextest, bun, tmux) is reported by name before any target runs.

## Result

2026-09-15, worked by the coordinator and checked by an independent verifier
that reran every line itself.

### The change

`.cartridge/justfile` owns all five gates now, and they share one shape:
`tools` names the toolchain, `_fan` expands `all` into that gate's target list
and runs every target without stopping at a failure, `_one` dispatches one
target to the owner that implements it. The root justfile keeps only `prd` and
the import. `root` comes from `source_directory()` rather than
`justfile_directory()`, which is what makes the second box work.

### Box 1 — every gate reports per target and fails loudly

```
$ just check
check     memo       FAIL        ... 18 verdict lines ...
check: 3 of 18 targets failed            exit 1

$ just test
test      runtime    FAIL        ... 19 verdict lines ...
test: 7 of 19 targets failed             exit 1

$ just smoke
smoke     policy     FAIL
smoke     proxy      FAIL
smoke     mcp        FAIL
smoke: 3 of 3 targets failed             exit 1

$ just verify
verify    composition FAIL
verify: 1 of 1 targets failed            exit 1

$ just isolation
isolation composition pass               exit 0
```

Each begins with `toolchain: cargo cargo-nextest bun tmux`. None stops at its
first failing target: `test` fails on `runtime`, the first in its list, and
still runs the eighteen after it. The red targets belong to other PRDs on this
board, not to the gate work. Two of them went green during the session and the
gate reported the change without being asked: `check live`, once
`live.ctg/src/launch.ts` imported the `spawnSync` it calls, and `check runtime`,
from another session's work in cartridge.ctg.

### Box 2 — the file names itself

```
$ just --justfile .cartridge/justfile check prd
toolchain: cargo cargo-nextest bun tmux
check     prd        pass

$ just --justfile .cartridge/justfile isolation
isolation composition pass
```

Neither output contains `.cartridge/.cartridge/tools/memo-run`, which was the
recorded failure.

### Box 3 — a missing toolchain is named first

```
$ just tools
toolchain: cargo cargo-nextest bun tmux                 exit 0

$ PATH="<only just>" just tools
toolchain: missing cargo cargo-nextest bun tmux         exit 2

$ PATH="<only just>" just isolation
toolchain: missing cargo cargo-nextest bun tmux         exit 2
```

The third refuses before the target: no isolation output and no verdict line
appear.

### A regression the verifier caught, and the fix

The first version of the gate layer silently stopped running the composed
repository's own `source-layout` integration test. That test rode at the tail
of the development memo's `all` loop, and the gate hands that memo one owner at
a time, so the tail was never reached. It is a `test` target named `layout`
now, which is why `test` has 19 targets and not 18. It is red, on a `cargo
metadata` lookup for the memory package, and it was already never running
before this change, because the old loop aborted on the first failing owner
and never got that far. The gate is what made it visible. The spec's
verification block fails if the target disappears again.

`verify` also lost `CARGO_TARGET_DIR`, which the runtime memo honours; it
resolves the host the same way again.

### Not collected

`prd collect` refuses while the composed root's working tree carries changes
outside this footprint, and it carries fourteen submodules of other sessions'
uncommitted work plus two untracked directories. That blocker is recorded on
the board and needs a human.

### Left alone, outside this footprint

`.cartridge/justfile` still carries a `sweep` recipe, and `cartridge sweep` no
longer exists: `error: unrecognized subcommand 'sweep'`. The owner list in
`_fan` duplicates the one in the development memo; they agree today and nothing
keeps them in step.
