---
complexity: 10
footprint:
  - references/parts/ramp.md
---

# spec02 — `ramp.md` rewritten dense, its 69 facts intact

`references/parts/ramp.md` was 1,157 words over only 69 facts — the loosest of
the five, and the one with the most paragraph prose a rewrite may shorten. It
carried 12 unbound waste words, the highest density in this PRD.

Most of the 12 were bound relative clauses (`a member that is itself a master`,
`the smallest tree it can see`) and cleared by naming the subject. Three were
the genuine vague-subject shape the rule targets — `That is the whole loop`,
`it is not a property of a repo`, `That is not a failure` — and those are the
sentences where the cut is real.

No other PRD has touched this file since the lane was cut, but the word box is
written against the text the rewrite replaced rather than against a fixed
commit, so a row landing here later cannot redden it. It finds that text by
this PRD's slug in the log, not by `git log -1` on the file: the last commit to
touch a file is whichever PRD landed most recently, and `handles.md` in spec01
shows what anchoring there costs once a neighbour lands.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/ramp.md` is silent and exits 0
- [x] the fact probe reports `69 -> 69 facts, 0 lost` against `fc75bcf`
- [x] the rewrite carries fewer words than the text it replaced — 1,140 against 1,157, read at the rewrite commit and its parent
- [x] the fenced blocks are byte-identical to their text at `fc75bcf` — the `happiness: 0` yaml and the `ramp: happy 1` output line are quoted behaviour, not prose
- [x] `python3 resources/index.py check` names no dangling reference in `references/parts/ramp.md`

## Verify and Proof

```sh
BASE=fc75bcf   # the lane cut — the fact baseline, never the word baseline
M=references/parts/ramp.md
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
F=$(printf '\140\140\140')          # the fence marker, spelled in octal
diff <(git show "$BASE":"$M" | awk -v m="$F" '$0 ~ "^"m {f=!f;next} f') \
     <(awk -v m="$F" '$0 ~ "^"m {f=!f;next} f' "$M")
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
[ -n "$out" ] || [ "$rc" = 0 ]
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -q "$M"; then exit 1; fi
```
