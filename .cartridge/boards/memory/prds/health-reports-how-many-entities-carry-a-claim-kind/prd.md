---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge/memory.ctg"
footprint:
  - "src/graph/src/heat.rs"
  - "src/cartridge/src/lib.rs"
---

# Health reports how many entities carry a claim kind

## Outcome

`kind_decay` in `src/graph/src/heat.rs` only slows decay for an entity whose
`claim_kind` is one of the seven built-in labels. Raw ingests, `tool.memory` ingests
and anything the background classifier has not reached fall to the default curve. If
most of a live bank is unlabelled, the per-kind table is decorative and the whole
bank forgets at one rate, which is the collapse the test-model-thing issue tracker
documented for a single decay initialisation. Before anyone tunes curves, the bank
must say how much of it the curves reach.

`health` gains a `claim_kind_coverage` block: total entities, the count with a
non-empty `claim_kind`, and a count per label. The same block reports the count in
each storage tier. No policy change ships with this item; it is the number the next
decision reads.

## Acceptance

- [ ] `memory health` and the cartridge `health` op return `claim_kind_coverage` with `total`, `labelled` and a per-label map.
- [ ] A test ingests three entities, labels one, and asserts labelled equals one.
- [ ] The README health section names the block and what an unlabelled majority means.
