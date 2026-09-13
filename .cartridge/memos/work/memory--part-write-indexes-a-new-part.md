---
kind: work
level: 10
description: a `part write` whose path is new and whose row is absent appends the index row to `memos/SYSTEM.md` from the part's own front matter — kind, description, a `read when` the caller passes — so creating a task is one call and the gate is never red between two edits
read_when: "writing a part from an agent"
status: done
estimate: 4h
---

# part-write-indexes-a-new-part

[[@prd/work/memory--part-is-a-verb.md]] made the write one call; the row is still a second edit
by hand, and [[the-parts-gate-is-red-in-both-directions]] says the gate is red
until it lands.

## Do

- `src/rpc/src/server.rs` `part write`: an optional `read_when` argument.
  When the path does not yet exist under the watched root and `SYSTEM.md`
  holds no row whose link is the part's leaf, append
  `| [[<leaf>]] | <kind> | <description> | <read_when> |` after the last
  row of the repo table — the row before the blank line that precedes the
  condensed rows. A missing `read_when` uses the description's first
  clause. An existing path or an existing row writes only the file.
- The same walk the gate uses finds the table; the gate's own fixture
  gains a case where a write lands the row and a second write does not
  double it.
- `tests/memos_index.rs`'s `the_gate_can_go_red` keeps its red case, so
  a part written by any other means still fails without its row.

## Check

`cargo test --test memos_index` green with the two new cases; from an
agent, one `part {action: write, path: memos/intake/x.md, text: …,
read_when: …}` leaves `just memos-check` green with no second call, and
the row reads the front matter's `kind` and `description` verbatim.

Done 2026-09-09, with no code written: the outcome landed on 2026-09-06 in
`fd80fd98`, "the index is generated from the parts, never typed". There is no
row to append. `tests/memos_index.rs` builds `_index_.md` and `index.json`
per kind by walking the folders, so `memos/SYSTEM.md` carries no index table
and the gate never asks for a row. Checked literally in the lane: one
`memo {op: write, path: work/…}` through the daemon, then
`cargo test --test memos_index` green with no second call, the new leaf
already in `memos/work/_index_.md` and `index.json` with its own front
matter's kind, description and `read_when` verbatim, and `memos/SYSTEM.md`
untouched. The `read_when` argument the Do asks for has no consumer left, so
it was not added.
