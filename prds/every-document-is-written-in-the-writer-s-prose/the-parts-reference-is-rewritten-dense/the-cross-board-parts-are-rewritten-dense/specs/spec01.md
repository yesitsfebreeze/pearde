---
complexity: 12
footprint:
  - references/parts/handles.md
---

# spec01 — `handles.md` rewritten dense, its 419 facts intact

`references/parts/handles.md` is the largest fact set in this PRD — 419 facts
in 1,898 words at `fc75bcf`, most of them table cells naming a handle and its
meaning. The rewrite therefore works almost entirely in the paragraph lines
between the tables; the tables are the fact set and are copied through
unchanged.

Two unbound waste words stood at `fc75bcf`, both bound relative clauses the
checker reads as vague subjects: `before it is filed` and `left in it is
blocked on the user`. Both cleared by naming the subject, not by deleting the
clause.

The file is shared. Three handle rows — `session`, `refuse`, `share` — landed
from other PRDs after the lane was cut, and the lane carries them verbatim, so
the count a box compares against is the text the rewrite replaced, never a
fixed commit. `fc75bcf` stays the fact baseline: a fact set may gain, never
lose.

A fourth row landed after the rewrite itself: `31620bb` widened the `session`
row by 64 prose words, so the file on disk now weighs more than the rewrite
left it. The word box therefore reads the rewrite commit and its parent, found
by this PRD's slug in the log, never `git log -1` on the file — the last commit
to touch a shared file is whichever PRD landed most recently, and anchoring
there measures a neighbour's paragraph instead of this unit's cut.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/handles.md` is silent and exits 0
- [x] the fact probe reports `0 lost` against `fc75bcf` — the three rows landed since are counted as new, never as a loss
- [x] no table row present at `fc75bcf` was removed or reworded — the tables carry the facts and the rewrite touches no row
- [x] the rewrite carries fewer words than the text it replaced — 2,113 against 2,122, read at the rewrite commit and its parent, an anchor a later row in this shared file cannot move
- [x] `python3 resources/index.py check` names no dangling reference in `references/parts/handles.md`

## Verify and Proof

```sh
BASE=fc75bcf   # the lane cut — the fact baseline, never the word baseline
M=references/parts/handles.md
PRD="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)/.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-parts-reference-is-rewritten-dense/the-cross-board-parts-are-rewritten-dense"
python3 resources/prose.py check "$M"
python3 "$PRD/probe/facts.py" diff "$BASE" "$M"
R=$(git log --format=%H --reverse --grep=the-cross-board-parts-are-rewritten-dense -- "$M")
set -- $R; R=$1
[ -n "$R" ]
was=$(python3 resources/prose.py stat "$R^" | awk -v m="$M: " '$0 ~ "^"m {print $2}')
now=$(python3 resources/prose.py stat "$R" | awk -v m="$M: " '$0 ~ "^"m {print $2}')
echo "$M: $was -> $now at the rewrite"
[ "$now" -lt "$was" ]
rows=$({ git diff "$BASE" -- "$M" | grep -c '^-|'; } || true)
[ "$rows" = 0 ]
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
[ -n "$out" ] || [ "$rc" = 0 ]
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -q "$M"; then exit 1; fi
```
