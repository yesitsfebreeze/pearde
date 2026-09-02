---
complexity: 6
footprint:
  - references/files.md
---

# spec02 — `references/files.md` rewritten dense, and the `prose.py` row

The manifest's opening paragraphs are cut for density (lead with the
answer, no unbound pronoun) and the `resources/board/knowledge/` section is
tightened the same way — every row and fact intact. `resources/prose.py`
gains its row beside `resources/index.py`. Already stands, done in the lane.

## Acceptance

- [x] `python3 resources/prose.py check references/files.md` exits `0`
- [x] `references/files.md` holds a row for `@resources/prose.py`
- [x] every anchor row present at `HEAD` is still present — no row deleted

## Verify and Proof

```sh
OUT=$(python3 resources/prose.py check references/files.md 2>&1) && RC=0 || RC=$?
[ "$RC" = "0" ]
printf '%s\n' "$OUT"

grep -q '@resources/prose.py' references/files.md

BEFORE=$(git show HEAD:references/files.md | grep -c '^| @')
AFTER=$(grep -c '^| @' references/files.md)
[ "$AFTER" -ge "$BEFORE" ]

echo "spec02: rows before $BEFORE after $AFTER"
```
