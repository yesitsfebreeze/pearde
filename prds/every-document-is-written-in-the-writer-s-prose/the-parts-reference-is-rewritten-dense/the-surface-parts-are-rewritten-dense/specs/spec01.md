---
complexity: 12
footprint:
  - references/parts/view.md
---

# spec01 — `references/parts/view.md` rewritten dense

The largest file under `references/parts/` (4,380 words). Its prose paragraphs
are cut for density — lead with the answer, no unbound pronoun, long
paragraphs split at their seams — while every table, fenced block, deep link
and `@`-reference stays verbatim. Already stands, done in the lane: 4,380 →
4,317 words, `check` green, 27 unbound pronouns to none.

One string in this file is pinned by a harness: `one-page-that-says-whats-up`
greps for `Nothing that is git-ignored is rendered for a person`. The line is
untouched, and the box below holds it that way.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/view.md` exits `0`
- [x] the word count is at or below the count at `HEAD`
- [x] every table row and fenced block at `HEAD` is still present — none dropped
- [x] every `@reference` present at `HEAD` is still present
- [x] the string `Nothing that is git-ignored is rendered for a person` is intact

## Verify and Proof

```sh
M=references/parts/view.md

python3 resources/prose.py check "$M"

python3 resources/prose.py stat HEAD | grep "^$M:" \
  | awk '{ exit ($4+0 <= $2+0) ? 0 : 1 }'

BR=$(git show "HEAD:$M" | grep -c '^|'); AR=$(grep -c '^|' "$M")
[ "$AR" -ge "$BR" ]
BF=$(git show "HEAD:$M" | grep -c '^```'); AF=$(grep -c '^```' "$M")
[ "$AF" = "$BF" ]

git show "HEAD:$M" | grep -o '@[A-Za-z0-9_/.]*[A-Za-z0-9_]' | sort -u > /tmp/v_b.txt
grep -o '@[A-Za-z0-9_/.]*[A-Za-z0-9_]' "$M" | sort -u > /tmp/v_a.txt
comm -23 /tmp/v_b.txt /tmp/v_a.txt > /tmp/v_lost.txt
[ ! -s /tmp/v_lost.txt ]

grep -q 'Nothing that is git-ignored is rendered for a person' "$M"

echo "spec01: rows $BR->$AR fences $BF->$AF refs kept, check green"
```
