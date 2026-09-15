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

# the distill prompt marks turns `[0]`-based while telling the model they are 1-based, and the parser drops any cited turn below 1 — so every stored turn number is one low and a claim drawn from a transcript's first turn loses its provenance entirely

## Do

Three pieces disagree, in one file.

**The markers are 0-based.** `distill_claims`
(`src/ingest/src/ingest_distill.rs:83-87`) builds them as

```
.map(|(i, t)| format!("[{}] {t}", start + i))
```

with `start = batch_idx * DISTILL_CHUNK_TURNS` and `i` from `enumerate()`, so
the first turn of the first batch is marked `[0]`.

**The prompt says they are 1-based**, twice: "The transcript below is marked
with 1-based turn numbers in [brackets]" and `"turns": [<1-based turn numbers
the claim is drawn from, **as marked**>]` (`:92`, `:99`). A model following the
instruction copies what it sees, which is the 0-based number.

**The parser drops anything below 1, deliberately.** `parse_claims` (`:192`)
filters `|n| *n >= 1`, and a test pins it:
`turns_absent_or_malformed_leaves_empty`
(`src/ingest/src/tests/ingest_distill_test.rs:52-62`) asserts
`turns: [2.0, 0, "oops"]` yields `vec![2]` under the comment "floats accepted,
zeros/negatives dropped". That is the fourth voice saying the numbering starts
at 1, against one marker generator that starts at 0. So a claim correctly citing
the transcript's first turn arrives
with an empty `turns` vec, and `ingest_intake.rs:192-199` then writes an empty
`Source::Session.section` — the uncited case. One turn per transcript can never
be cited, and it is the first one, which is usually where the request is stated.

Every other citation is stored one lower than the convention the prompt, the
`Claim.turns` doc ("1-based turn numbers in the transcript") and
`split_turns`' comment ("a 1-based turn number here maps to the same turn the
caller indexed") all assert.

Fix the markers: `start + i + 1`. That is the one change that makes all three
agree, and it leaves the `>= 1` filter meaningful as a guard against a model
inventing a zero.

Name the consequence rather than solving it here: sections already in the store
were written under the 0-based scheme, and intake turn numbers are the only
non-empty sections there ([[section-dedup-keys-on-the-section-alone]]), so old
rows will sit one below new ones.

**Done 2026-09-06.** The markers are `start + i + 1`, with the four things they
now agree with named in the comment beside them: the prompt's two 1-based
statements, `Claim.turns`' doc, `split_turns`' mapping, and the `>= 1` filter
that gave the mismatch its teeth. One character, four disagreeing assertions
resolved.

`distill_chunk_markers_carry_global_turn_index` moved with it — it pinned the
batch-2 marker at `DISTILL_CHUNK_TURNS` and now pins `DISTILL_CHUNK_TURNS + 1`,
still asserting the offset is global rather than per-batch, which was its
subject.

New: `the_first_turn_is_marked_one_and_can_be_cited` pins the case the defect
made unreachable. It asserts three things rather than one — that the opening
turn is marked `[1]`, that **no** marker is `[0]`, and that a claim citing turn 1
keeps its `turns` vec. The middle assertion is the one that would catch a
regression to 0-based numbering even if the parser's filter were later
loosened, since the filter is what turned a numbering slip into lost
provenance.

The consequence the `Do` names stands and is not solved here: sections written
under the 0-based scheme sit one below new ones, and intake turn numbers are the
only non-empty sections in the store.

## Acceptance
A transcript whose first turn carries the only citable fact produces a claim
with `turns == [1]` and a `Source::Session.section` of `"1"`. `just test`
green — suite 1,255 passed. The claim half is held by the new test; the
`section` half follows from `ingest_intake.rs:192-199` writing the joined turn
numbers, which the same test's `turns == [1]` feeds.
