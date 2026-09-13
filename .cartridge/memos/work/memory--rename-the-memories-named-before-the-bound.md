---
kind: work
level: 10
status: done
description: one memory in this store is named with an entire Obsidian workspace JSON, so every `health` call prints about 200 lines of it — the bound landed in the code and never touched the names already written
read_when: "reading health, or after landing a write-time bound"
---

# rename-the-memories-named-before-the-bound

## Do

[[@prd/work/memory--a-graviton-name-is-bounded.md]] is done: a name is one line under 80 characters
or the memory stays unnamed. The names written before it are still in the store.
`memory health` on 2026-09-06 printed, among 27 memories, one whose name is a
complete Obsidian `workspace.json` — layout, leaf ids, `lastOpenFiles` — about
200 lines inside the memory list, on every call, on the surface an agent reads
first to learn the store's shape.

The bound is a write-time guard with no pass over what exists. Apply it once to
the stored names: any memory whose name fails the bound returns to unnamed and is
renamed by the next naming pass, which is what the guard would have done. The
naming write itself must route to the daemon
(`unnamed-promote-is-clobbered` and [[@prd/work/memory--unnamed-promote-routes-to-the-daemon.md]])
or the next flush restores what was cleared.

The pass is the doctor's, landed 2026-09-06: `is_name_shaped` and
`GRAVITON_NAME_MAX_CHARS` are public out of `tick_loop::tick_tasks`, so the
diagnosis asks the write-time guard itself rather than retyping 80. The
`misshapen_memory_names` finding lists every named memory the guard would refuse
and carries one `UnnameMisshapenMemory` repair each; `apply_repairs` re-verifies
the name is still misshapen and clears `graviton_text` and `graviton_vec`.
`memory repair` already refuses while the writer lock is held, so the clear
cannot land under a live daemon and be flushed back over.

What is left is the run: the daemon holds the writer lock on the store that
carries the workspace.json name, so `memory doctor --json` then `memory repair`
needs it stopped first.

Landed `6839761d`: the doctor half alone — `is_name_shaped` and
`GRAVITON_NAME_MAX_CHARS` public, the finding, the repair. The run itself has
not happened, and the store still shows it: `memory health` on 2026-09-07 prints
one 81-character name, "Core Theme: The parts protocol and membrane's .mb
contract are the same system.", which the guard refuses on its length and on
its trailing period. The Check failed, so the part stayed open
([[landed-work-still-says-open]]).

Landed 2026-09-07, the run: daemon stopped, `memory doctor` found 7 misshapen
names, `memory repair` unnamed them — `memory health` now prints no memory name
over 80 characters and doctor lists no `misshapen_memory_names` finding. The
run was first recorded as `status: closed`, a fourth lifecycle word the
vocabulary refuses ([[blocked-does-not-say-who-unblocks]]), which turned the
fields gate red on the record; the word is `done`, what a passing Check buys.

## Check

`memory health` prints no memory name over 80 characters or containing a newline,
and the count of `[unnamed]` memories rises by exactly the number of names the
bound rejects.
