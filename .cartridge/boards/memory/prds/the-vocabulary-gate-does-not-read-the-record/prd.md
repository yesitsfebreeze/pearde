---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# the banned synonym for the intake is gated in `src/` and `tests/` and nowhere else, so the record carries it 25 times across 13 parts including one part's own name

## Do

`tests/vocabulary.rs` bans one word — the print-queue synonym the 2026-07-17
rename scrubbed — and its own header says the rename kept "no alias anywhere".
The gate walks `root/src`, `root/tests` and `README.md`
(`tests/vocabulary.rs:33-37`) and stops there. `memos/` is never read, so the
record was never held to the rule it states.

Measured 2026-09-06: 40 occurrences across 14 part files, cut to **25 across
13** the same hour by renaming the two parts written that night that had
already added to it — which is what an unenforced rule does, and how quickly.
What remains includes `open-work.md`, `working-with-memory.md`,
`ingest-says-when-a-fact-lands.md`, `the-intake-drain-runs-a-batch.md` and a
part whose *name* was the banned word: `drain-the-intake.md`, a `status: done`
work item from the dashboard plan. So a cold agent reading the record learns the
word the code forbids, which is the exact failure the gate was written to stop;
it caught the tree and missed the memory.

Point the gate at `memos/` as well, then rename what it finds — the part file,
its index row and every inbound link in one change, since a rename that leaves
a link behind is `the-index-gate-scans-three-places`'s other failure. Do the
rename in one operation for the reason
`the-parts-gate-is-red-in-both-directions` gives.

## Acceptance
`cargo test --test vocabulary` walks `memos/` and passes, and `grep -ri` for the
word across `memos/` returns nothing but this part's own description of what it
removed.

Done 2026-09-06. The gate walks `memos/` (`313be131`) and its red-on-purpose
selftest gained a fixture that writes a part carrying the word and requires the
failure to name that path, so the root cannot be dropped later unnoticed. The
sweep rewrote 57 occurrences across 26 record files plus one in
`src/commands/src/lib.rs`: the queue is the intake, what sits in it is parked.
Both parts whose names carried the word are renamed with their rows and inbound
links — `drain-the-intake` and `the-direct-intake-has-already-replayed-most-of-itself`.
`cargo test --test vocabulary` is green and a case-insensitive grep over
`memos/` returns nothing. Four record files and the one code line were left
uncommitted because another session's in-flight work sits in the same files;
the content is correct on disk and rides into their commit.
