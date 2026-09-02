---
complexity: 8
footprint:
  - references/parts/loop.md
---

# spec04 — loop.md, rewritten dense

1,713 words, the seven-step table every session works from and one of the two
files the guard exempts from its third-read refusal, because a compacted pass
has to be able to re-read the steps. A step, a command or a decision lost here
is lost from every pass on every board.

**Already standing.** Nothing; the analyst's build measured this file and
rewrote none of it. It fails `prose.py check` on 8 unbound waste words (`it`,
`that`, `this`). Mean sentence length is inside the limit.

**Left to finish.** The rewrite. 73% of the file is paragraph prose. The seven
step rows are the file's spine and stay rows; the prose around them is where
the cut is. Every command name, step number and cross-reference survives, and
the file still reads as the whole loop to a session that has just been
compacted and holds nothing else.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/loop.md` prints nothing and exits 0
- [x] the fact check prints nothing for `loop.md` against the lane's base commit and exits 0
- [x] `loop.md` holds fewer words at `prose.py stat` than at the base commit
- [x] the seven step rows survive as seven rows, each naming the same step number and command as at the base commit
- [x] `git diff --name-status <base> -- references/parts/loop.md` prints exactly one row, beginning `M`
- [x] `python3 resources/index.py check` prints no line naming `loop.md`

## Verify and Proof

```sh
BASE=$(git merge-base HEAD main)   # fc75bcf at the lane cut
ROOT=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
PRD=$ROOT/.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-parts-reference-is-rewritten-dense/the-loop-parts-are-rewritten-dense
python3 resources/prose.py check references/parts/loop.md         # silent, exit 0
python3 "$PRD/probe/facts.py" "$BASE" references/parts/loop.md    # silent, exit 0
python3 resources/prose.py stat "$BASE" | grep 'parts/loop.md'
git diff --name-status "$BASE" -- references/parts/loop.md
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
case "$rc" in 0|1) ;; *) echo "index.py check crashed: $rc"; exit 1;; esac
if printf '%s\n' "$out" | grep 'parts/loop.md'; then exit 1; fi
was=$(git show "${BASE}:references/parts/loop.md" | grep '^| [1-7] ') && rc=0 || rc=$?
now=$(grep '^| [1-7] ' references/parts/loop.md) && rc=0 || rc=$?
printf '%s\n' "$was" | wc -l          # seven step rows before
[ "$was" = "$now" ]                   # and the same seven, unchanged, after
```
