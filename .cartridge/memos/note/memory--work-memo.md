---
kind: type
type: work
description: "one unit of planned work — `level: 1-10`, `status: open | done | blocked`, a `## Do` that says what, a `## Spec` an analyst writes that says how, and a `## Check` of boxes that can fail; done when every box is ticked"
read_when: "writing a work memo, speccing one, or asking why a memo sits in the spec band"
---

# work

One unit of planned work — pearde's PRD on the record
([[@prd/decision/memory--the-pearde-workflow-is-the-work-record.md]]). Frontmatter carries `level: 1-10`
and `status: open | done | blocked`; the body carries three sections, each with
one author:

- `## Do` — **the contract, what not how.** What exists when this is done, why
  it matters, what must not change, pointers to memos and prior work. No
  file names, no verbs of change: a Do that names the files has already
  decided the how, and the analyst's probe is where that is decided. Written
  by whoever asks — a person, [[@prd/routine/plan-cartridge-work.md]], a finding.
- `## Spec` — **the how, from a probe.** The files it touches, the steps as
  commands, the routine or tool path the hand runs. Written by the analyst
  after it tried to build the thing, never from reading. A memo with no Spec
  sits in the `spec` band and is dispatched to an analyst, not a hand.
- `## Check` — **the proof.** `- [ ]` boxes, each a behaviour that can fail,
  and one `sh` block that exercises them. Written with the Spec; ticked by the
  implementer as each closes, never in a batch. `status: done` only when every
  box is `[x]`.

One memo is one spec. Level bounds the split: a level-10 item is one focused
change a hand finishes from its Spec alone; an analyst that finds two units
returns a split — children at level 10, `subwork:` naming them on the parent, the parent's Check becoming "every child done".
Five optional typed lines place it in time on the plan ([[@prd/decision/memory--the-plan-is-a-gantt.md]]):
`estimate`, `actual`, `claim`, `due`, `needs`; the nonvisual `plan` operation
parses these fields in `src/rpc/src/plan.rs`, whose tests cover scheduling.
[[@prd/routine/run-board.md]] runs one, and runs a plan's worth at once.
