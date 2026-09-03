---
complexity: 4
footprint:
  - references/parts/commits.md
  - references/parts/states.md
---

# spec02 — the written contract says a conflict is reported, not merged by hand

Two documented claims contradict spec01 and have to move with it.
`references/parts/commits.md` says of a merge conflict that "the lane branch
still holds the work; a person merges it by hand" — true of the lane, wrong
about the board, and it is the sentence that made a stranded `claimed` PRD
read as intended behaviour. Its transitions table also says `claimed →
blocked` commits, which a conflicted lane does not: nothing merged, so nothing
is staged. `references/parts/states.md` gives `blocked` as set by the
orchestrator and as always carrying `needs:`; `collect` now sets it too, and
the conflict case waits on a person rather than on a named PRD, so it carries
a `## Blocked` section and no `needs:`.

The `## Blocked` heading is deliberately not a new part: it is the wall
@references/parts/view.md already draws and `questions.py` already refuses a
`blocked` PRD for lacking, so the reason lands where every reader of this board
already looks and no renderer has to learn anything.

**What already stands.** Both files are edited in the lane, uncommitted, and
`python3 resources/board/mapfile.py check` is silent over them.

**What is left.** Commit them, and re-read the two paragraphs against spec01
once it lands, in case the implementer changed a word of the mechanism.
`references/parts/commits.md` and `references/parts/states.md` are also in the
footprint of the sibling PRD `collect-runs-the-invariants-and-red-refuses`,
which is `claimed` as this is written — the plan's `after … (footprint)` edge
orders the pair, and whichever lands second rebases onto the first.

## Acceptance

- [ ] `references/parts/commits.md` no longer says a person merges a conflicted lane by hand
- [ ] it says instead that the PRD is written `blocked` with the lane branch and the conflicting files named, and that `unblock` returns it to `specced`
- [ ] it says why `blocked` and not `failed`, in one clause a reader can act on
- [ ] its `claimed → blocked` row names the conflicted lane as the case that commits nothing
- [ ] the `blocked` row of `references/parts/states.md` names `collect` among what sets it
- [ ] `references/parts/states.md` no longer reads as though every `blocked` PRD carries `needs:`
- [ ] `python3 resources/board/mapfile.py check` prints nothing and exits 0

## Verify and Proof

```sh
set -e
! grep -q "a person merges it by hand" references/parts/commits.md
grep -q "unblock" references/parts/commits.md
grep -q "never a stranded lane" references/parts/commits.md
grep -q "A conflicted lane is the exception" references/parts/commits.md
grep -q "a lane that will not rebase" references/parts/states.md
grep -q "written by" references/parts/states.md
python3 resources/board/mapfile.py check
echo "spec02 ok"
```
