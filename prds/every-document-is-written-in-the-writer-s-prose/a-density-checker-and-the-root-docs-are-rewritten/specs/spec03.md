---
complexity: 5
footprint:
  - index.md
---

# spec03 — `index.md` rewritten dense, and `@@language` gains the checker

The prose around the Keywords and Files tables is cut for density (no
unbound pronoun, no redundant clause); every `@@keyword` row and its anchors
are untouched. `@@language`'s row gains `@resources/prose.py`. Already
stands, done in the lane.

## Acceptance

- [x] `python3 resources/prose.py check index.md` exits `0`
- [x] `@@language`'s row lists `@resources/prose.py`
- [x] every `@@keyword` row present at `HEAD` is still present

## Verify and Proof

```sh
OUT=$(python3 resources/prose.py check index.md 2>&1) && RC=0 || RC=$?
[ "$RC" = "0" ]
printf '%s\n' "$OUT"

grep '@@language' index.md | grep -q '@resources/prose.py'

BEFORE=$(git show HEAD:index.md | grep -c '^| `@@')
AFTER=$(grep -c '^| `@@' index.md)
[ "$AFTER" = "$BEFORE" ]

echo "spec03: keywords before $BEFORE after $AFTER"
```
