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

# the watcher's fail-open comment argues from "there is no startup scan", 99 lines above the boot scan that landed six weeks after it was written

## Do

`MemoryFileWatcherSink::ingest` (`src/ingest/src/ingest_file_watcher.rs:119-125`)
justifies its durable-first ordering like this:

```
// Durable first, RAM second — `tool_ingest`'s shape. `notify` installs
// watches and replays nothing, and there is no startup scan, so a record
// still in the channel when the daemon dies is gone and nothing re-offers
// it.
```

There is a startup scan. `scan` sits 99 lines below in the same file
(`:221`), and `commands_serve` spawns it on every boot alongside the watcher
(`src/commands/src/commands_serve.rs:540`, imported as `scan as scan_roots`,
spawned at `:587`) under its own comment saying so: "The boot scan reads and embeds every file it finds". A
record lost in the channel *is* re-offered at the next boot for any file still
on disk under the roots — which is the whole point of
`the-watcher-walks-its-roots-at-start`. Only a file deleted before that boot
is gone.

The comment was written on 2026-07-22 (`8c13e7c9`); `scan` landed on 2026-09-05
(`9b0862e9`, [watcher-scans-at-boot](../watcher-scans-at-boot/prd.md)) without it being revisited. Correct the
middle sentence to name the boot scan and the case that survives it — a file
deleted before the next boot — and leave the fail-open conclusion, which the
durable intake and the scan both support and neither weakens.

This is a rot class `tests/cited_paths.rs` cannot see. The fourteen in
`a-citation-rots-quietly` were coordinates — a path or a line that moved, and
a walker can resolve those. This comment cites nothing; it asserts a behaviour,
and only reading the crate it lives in falsifies it
(`a-gate-can-see-half-of-citation-rot`).

**Done 2026-09-06, and the part's coordinates were incomplete.** The site named
above is corrected: a record lost from the RAM queue is gone *from the queue*,
the boot `scan` re-offers every file still on disk under the roots, and the case
the durable write actually saves is a file deleted before that boot — which no
scan can find. The fail-open conclusion stands untouched, supported by both.

**There was a second copy.** `rg -n "no startup scan" src` — the claim's own
wording rather than this part's line numbers — answered twice, the second at
`src/ingest/src/tests/ingest_file_watcher_test.rs:448`, same assertion in a test
comment nobody would have opened. Both are fixed and the phrase now returns
nothing across `src` and `tests`. Trusting the coordinates would have left half
the rot in place, which is `read-twice-by-different-means` applied to a part
rather than to a tool.

Both shas check out: `8c13e7c9` is "park watched files in the durable intake"
(2026-07-22) and `9b0862e9` is "the watcher walks its roots at start"
(2026-09-05).

This is `a-copied-fact-has-no-dissent` with an assertion in place of a number,
and it behaved identically — two statements of one fact, both true when written,
both falsified at the same instant by the same commit, neither able to
contradict the other. The difference is where the falsification comes from: a
measurement is overtaken by the *world* moving, which no test can watch, while
an assertion like "there is no startup scan" is overtaken by the *tree* moving,
and the tree is exactly what a test can read. Nothing checks it today.

## Acceptance
The comment no longer says the tree has no startup scan, and names
`scan`/`scan_roots` so the next reader can reach it. `just check` green, suite
1,243 passed, and `rg -n "no startup scan" src tests` returns nothing.
