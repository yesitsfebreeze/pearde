---
complexity: 8
footprint:
  - resources/board/lanes.py
  - resources/board/collect.py
---

# spec01 — a conflicted lane writes the PRD `blocked` with git's own file list

`lanes.merge` stops raising a bare `LaneError` on a conflict and raises a new
`lanes.Conflict` instead, carrying the lane branch, the branch it would not
land on, and the files git named as data rather than only inside a sentence.
`collect.land_lane` lets that one class through — every other `LaneError` is
still a `Stop`, because a lane git cannot read is a broken board — and
`collect.collect_one` catches it and writes the PRD `blocked`: `claim:`
dropped, a `## Blocked` section appended naming the branch, the target and one
bullet per conflicting file, and a transition row recorded. Nothing else
moves: the checkout is where `lanes.merge` left it and the worker's commits
are still on the lane branch, which is why the reason can say so.

`blocked` and not `failed`. A `failed` PRD is work that did not do what it
said; this work may be perfect and merely disagree with what landed while it
ran, and `failed` routes to `retry`, which would dispatch a second worker onto
a lane that already holds the answer. `unblock` is the edge out and it lands
on `specced` — specced work with a lane standing, exactly what it was before
the collect.

**What already stands.** All of it, uncommitted in the lane: `lanes.Conflict`,
the re-raise in `land_lane`, `collect.block_conflict`, and the `except
LaneConflict` in `collect_one`. The probe at
`.pearde/prds/no-work-is-lost-on-the-board/a-conflicted-lane-is-reported-not-stranded/probe/verify.sh`
is 21 of 21 green against this tree and 12 of 21 against the same tree without
the change, so the boxes below are checks that can and do fail.

**What is left.** Commit it inside this footprint and re-run the probe. Two
things the build deliberately did not do, each a judgement the implementer
should keep rather than reverse: `block_conflict` is unconditional and not
behind `--fail`, because without the write the PRD stays `claimed` with no
worker, which is the defect the contract names; and its `--dry` arm is
unreachable today, because `land_lane` returns before it merges under `--dry`.

## Acceptance

- [x] `lanes.Conflict` subclasses `LaneError` and carries `branch`, `onto` and `files`, the file list taken from git's conflict output and not re-parsed out of the message
- [x] `lanes.merge` raises `Conflict` on both paths that can conflict — the rebase of the lane and the `--ff-only` merge into the checkout
- [x] `collect.land_lane` re-raises `Conflict` and still turns every other `LaneError` into a `Stop`
- [x] a conflicting collect leaves the PRD `state: blocked` with no `claim:` key
- [x] the PRD body gains a `## Blocked` section naming the lane branch and every conflicting file, one per bullet
- [x] the checkout is on the commit it started on and the lane branch still holds the worker's commits, and the lane's own tree is clean
- [x] `pearde scan` names the PRD `blocked` and says it is waiting on a person
- [x] `pearde unblock <prd>` takes it from `blocked` to `specced`
- [x] a collect with no conflict is untouched — the PRD reaches `done`, the worker's code lands, and nothing is written about a block

## Verify and Proof

```sh
set -e
B="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)"
python3 -m py_compile resources/board/lanes.py resources/board/collect.py
python3 -c "import sys; sys.path.insert(0, 'resources/board'); import lanes; assert issubclass(lanes.Conflict, lanes.LaneError)"
PEARDE_ROOT="$PWD" bash "$B/.pearde/prds/no-work-is-lost-on-the-board/a-conflicted-lane-is-reported-not-stranded/probe/verify.sh"
```
