---
complexity: 7
footprint:
  - references/parts/commits.md
---

# spec03 — commits.md, rewritten dense

1,568 words, 85% of them paragraph prose — the highest cuttable share of the
eleven loop parts, and the file where the rewrite has the most room. Every
commit-message rule, path, flag and refusal string survives verbatim.

**Already standing.** Nothing; the analyst's build measured this file and
rewrote none of it. It fails `prose.py check` on 12 unbound waste words
(`it`, `that`, `there`) — the most of any of the eleven. Mean sentence length
is inside the limit.

**Left to finish.** The rewrite. Clear the twelve vague-subject hits, then the
judgement pass. Because 85% of the file is prose, this is the one loop part
where a cut approaching the tree-wide target is plausible; take it as far as
the fact check allows and no further.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/commits.md` prints nothing and exits 0
- [x] the fact check prints nothing for `commits.md` against the lane's base commit and exits 0
- [x] `commits.md` holds fewer words at `prose.py stat` than at the base commit
- [x] `git diff --name-status <base> -- references/parts/commits.md` prints exactly one row, beginning `M`
- [x] `python3 resources/index.py check` prints no line naming `commits.md`

## Verify and Proof

```sh
BASE=$(git merge-base HEAD main)   # fc75bcf at the lane cut
ROOT=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
PRD=$ROOT/.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-parts-reference-is-rewritten-dense/the-loop-parts-are-rewritten-dense
python3 resources/prose.py check references/parts/commits.md         # silent, exit 0
python3 "$PRD/probe/facts.py" "$BASE" references/parts/commits.md    # silent, exit 0
python3 resources/prose.py stat "$BASE" | grep 'parts/commits.md'
git diff --name-status "$BASE" -- references/parts/commits.md
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
case "$rc" in 0|1) ;; *) echo "index.py check crashed: $rc"; exit 1;; esac
if printf '%s\n' "$out" | grep 'parts/commits.md'; then exit 1; fi
```
