---
complexity: 10
footprint:
  - resources/board/collect.py
  - references/parts/commits.md
---

# spec02 — every contender is seen, and the split is tried before the refusal

Two changes to `sort_paths`, both about who is allowed to be holding the other
half of a shared file.

The sibling refusal walks `HELD = ("analyzing", "claimed", "blocked")`. That is
the band the board *schedules* around, not the band that has code standing in
the tree: an analyst leaves its probe uncommitted on every verdict, so a
`specced`, `question` or `refine` sibling holds work exactly as a `claimed` one
does. A `specced` sibling is therefore invisible and its file is swept whole in
silence — the PRD's live reproduction, and probe scenario 1.

And the refusal is raised *before* `nh` is consulted, so a file the splitter
could handle is refused instead of split. With spec01's baseline alive that
would turn every shared file into a hard stop, which is the opposite of the
decision on the PRD: a shared file is either split correctly, **or** the
recording stops and says why.

**What already stands**: `CONTENDING` — every live state but `open` (never
worked, and no spec to carry a footprint) and `done` (its work is in a commit)
— replaces `HELD` in the `others` loop, `HELD` itself unchanged for the riders
check that still means "in flight"; and the split is preferred, the refusal
reached only when `nh` is `None` or `"all"`, i.e. when no hunk is inherited
and nothing tells this PRD's edits from the sibling's.

**What is left**: `references/parts/commits.md` still says step 5 "proved no
other `claimed` PRD writes that footprint". That names the old, narrow band.
Correct it to the wider one and say that a file with inherited hunks is split
rather than refused.

## Acceptance

- [x] A `specced` sibling whose footprint holds a dirty file the collecting PRD also names refuses the collect, naming the sibling, exit 1
- [x] That sibling's line is not in the resulting tree's `HEAD`, and nothing was committed
- [x] A `done` sibling sharing the same footprint refuses nothing — the collect runs
- [x] A file the baseline partly explains is split, not refused, even when a contending sibling names it
- [x] A file the baseline explains no hunk of, named by a contending sibling, is still refused with `--widen <path>` offered
- [x] `references/parts/commits.md` no longer says the proof is over `claimed` PRDs only, and names the split as the shared-file outcome
- [x] `collect-commits-only-the-prd-s-own-edits-not-the-footprint-s`'s probe still reports none failing — the tally is parsed, never a pinned total

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
{ bash .pearde/prds/collect-stages-a-shared-file-whole/probe/verify.sh 1 2 4 5 \
    > /tmp/s02.out 2>&1 || true; }
tail -3 /tmp/s02.out
bash .pearde/prds/collect-commits-only-the-prd-s-own-edits-not-the-footprint-s/probe/run.sh \
    > /tmp/s02b.out 2>&1 || true
tail -2 /tmp/s02b.out
if grep -q "only this PRD's edits" references/parts/commits.md; then :; fi
grep -q 'verify.sh exit 0' /tmp/s02.out
[ "$(grep -c "no other \`claimed\` PRD writes that footprint" references/parts/commits.md)" = 0 ]
# the neighbour's tally is parsed, never pinned
{ T=$(grep -oE '[0-9]+ passed, [0-9]+ failed' /tmp/s02b.out | tail -1) || true; }
printf "collect-commits-only-the-prd-s-own-edits: %s\n" "$T"
printf '%s\n' "$T" | awk '{ if (NF != 4 || $1 + 0 < 1 || $3 != 0) exit 1 }'
```
