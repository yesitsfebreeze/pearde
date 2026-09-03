---
memo: a-master-need-is-the-union-of-its-members
kind: invariant    # decision | note | invariant
status: decided    # open | decided | superseded
tags:
  - memo
  - kind/invariant
  - status/decided
subject: a master board's ramp need is the union over its members, never its own repo alone
date: 2026-09-02
verify: bash resources/invariants/a-master-need-is-the-union-of-its-members.sh
# updated:         # only on a substantive revision; never for a path fix
# prds:            # board-relative PRD dirs this memo governs
#   - <prd-dir>
# supersedes:      # the slug this replaces
# superseded_by:   # the slug that replaced this
---
<!-- Unlike a prd.md, a memo's keys are a CLOSED set: an undeclared key is a
     typo and @resources/doctor.sh fails on it. @references/memo.md is the
     format. -->

# a-master-need-is-the-union-of-its-members — the ramp measures every tree the board plans over

## Decision

`ramp need` on a master board is the **union over `members:`**, to any depth,
with the master's own tree counted as one more member of that union rather
than the whole of it. Three things follow, and each is an assertion in
`verify:`:

- **The sum, not the maximum and not the master's own.** A job's count is the
  per-member counts added. A member reached by two routes, or by a cycle, is
  counted once — the walk is keyed by `os.path.realpath`.
- **The floor lands on the sum.** `writing`'s floor is 25; two members holding
  fifteen markdown files each raise `writing` together and neither raises it
  alone. A floor applied per member would be a floor on the smallest tree.
- **A row credits the members it came from.** On a union the marker list is
  the sum of five trees and says nothing, so `why` becomes `mitosys 14769,
  model 353, realm 99, …`, loudest first. The fork `write_ask` puts to a
  person carries the same subject: *`mitosys 14,769, model 353 and 3 more
  members ask for rust`*, never *`The tree asks for rust`*.

A **plain** board is untouched by all of it. `scan_roots` returns one unnamed
row, `needs` runs the same body it always ran, the `why` is still the marker
list, and the fork still says *the tree*. That is not a courtesy: it is the
first check in `verify:`, and it is the one row that stays green through the
regression the others catch.

`have` is **not** part of this. It reads one machine's installed skills and
always did. So a master's `gap` is a union `need` measured against a single
machine's `have` — the asymmetry is deliberate, because a skill is installed
for a person, not for a repo. @references/parts/ramp.md says so in the same
words, so a reader does not infer a symmetry that is not there.

## Why

Measured on `/Users/feb/dev/infra/.pearde`, a master of four, on 2026-09-02:

```
$ pearde ramp need
writing        104  *.md×104
docker           2  1 PRD
rust             1  *.rs×1
```

That `rust 1` was one file — `.pearde/prds/a-shared-name-is-not-a-shared-function/probe/main.rs`,
a probe, inside the board's own directory. The four member trees the board
plans over hold **14,562 tracked `.rs` files**. Every member is a Rust
workspace; the `infra` directory the master lives in is not a Rust repo at
all.

The number was not merely small. It was measured against the one tree that by
construction holds the least code, and it still reached a person as a
question: a `GAP rust` that cost two passes. The gap happened to be real, and
it was real by accident — had that one probe file not existed, the same
arithmetic would have printed nothing and the board would have gone on
planning Rust work with no Rust skill and no question asked.

The ramp is loop step 0. It is the one gate that runs before any PRD is
touched, and its whole job is to say whether this machine is tooled for the
work. A gate whose signal is measured against the wrong tree is worse than no
gate, because its silence is believed.

## What makes it hold

Not a sentence. `resources/board/ramp.py` is arranged so the union is the only
thing `needs` can compute:

- `scan_roots(board)` is the single place the member walk lives — breadth
  first, keyed by realpath, names taken from `members:` and suffixed on a
  collision. A plain board returns `[("", board)]` and nothing downstream
  changes shape.
- `_measure(board)` is one board's raw signal with **no floor applied**. The
  floor cannot be applied per member because the function that would apply it
  does not know the members exist.
- `_union(board)` sums those, `needs` floors the sum, `contributors` reads the
  same measurement back as `{job: [(member, hits)]}` so a sentence can name a
  member without re-parsing a string it built.

And `verify:` is seventeen assertions over three to seven git repos built in a
`mktemp -d`, so every count is known by construction rather than read off
whichever trees this machine holds. A check that read the real boards would
have printed `rust 1` as happily as the gate did.

## Alternatives considered

**Leaving `repo_of(board)` and telling people to scan members individually.**
It is what the tool did, and it makes the master board's own `need` a number
that is never right and never obviously wrong. The master exists to plan over
the union; the gate that runs before that planning has to measure the same
union or it is answering a different question than the board is asking.

**Measuring the union but keeping the marker list as `why`.** `*.rs×15245`
summed over five trees is a true sentence that helps nobody: a person reading
a gap needs to know *which repo* is asking so they can judge whether the skill
is worth installing. The marker list survives on a plain board, where there is
one tree and naming it says nothing.

**A floor per member, then summing what cleared it.** Cheaper to reason about
and wrong in the direction that matters: a monorepo split into six services,
each with four markdown files, would raise `writing` at zero. The floor exists
to stop one stray file asking for a toolchain, and a union of stray files
across six trees is not stray.

**One level of `members:`, not a walk.** The contract's own words are that a
member is measured *the way its own board would measure it* — and a member
that is itself a master measures a union. A one-level walk returns the middle
repo's own directory and calls it the answer, which is the original fault
moved down a level. `verify:` asserts the grandchildren.

**Unioning `have` as well, for symmetry.** A skill is installed on a machine
for a person; it is not a property of a repo. Unioning `have` over members
would say a job is answered because some other project's checkout carries a
project-level skill directory this session cannot reach. The asymmetry is
named in the reference instead of papered over.

## Consequences

- `need` on a master runs `git ls-files` once per member. On the four-member
  board here that is five invocations and about a second — a gate cost, once
  a pass, not a per-call one.
- `board_words()` is the public union accessor and **nothing inside `needs`
  calls it**: `_measure` needs the per-board split, so it reaches for
  `_words_of`. Its docstring says so and `verify:` calls it. A pass reading it
  as a leftover and deleting it would take a contract item with it.
- `contributors(board)` walks the members a second time. Cheap next to
  `git ls-files`, and it is what keeps `write_ask` from re-parsing the `why`
  string to guess where a member's name ends.
- **`have` still has the fault on its own axis.** `skill_dirs()` does
  `repo_of(board)` and reads only the master's own project-level
  `.claude/skills/`; a member's are invisible. That is outside this
  invariant's words and worth its own contract — recorded here so the next
  reader does not take this memo as covering it.
