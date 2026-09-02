---
complexity: 7
footprint:
  - README.md
---

# spec04 — `README.md` rewritten dense

The opening, the "Three rings" prose (Core, Advisors, Tools) and two closing
sentences are cut for density — one idea per sentence, no unbound pronoun,
no redundant clause. Every table (sixty seconds, disk layout, the pass,
mid-pass lookups, scopes, Glossary), the state diagram and every command
line are untouched. Already stands, done in the lane.

## Acceptance

- [x] `python3 resources/prose.py check README.md` exits `0`
- [x] every Glossary row present at `HEAD` is still present
- [x] every fenced code block's content is byte-identical to `HEAD`

## Verify and Proof

```sh
OUT=$(python3 resources/prose.py check README.md 2>&1) && RC=0 || RC=$?
[ "$RC" = "0" ]
printf '%s\n' "$OUT"

BEFORE_GLOSS=$(git show HEAD:README.md | grep -c '^| [a-z]* | ')
AFTER_GLOSS=$(grep -c '^| [a-z]* | ' README.md)
[ "$AFTER_GLOSS" = "$BEFORE_GLOSS" ]

git show HEAD:README.md | awk '/^```/{f=!f;next} f' > /tmp/readme-code-before.$$
awk '/^```/{f=!f;next} f' README.md > /tmp/readme-code-after.$$
cmp /tmp/readme-code-before.$$ /tmp/readme-code-after.$$
rm -f /tmp/readme-code-before.$$ /tmp/readme-code-after.$$

echo "spec04: glossary rows before $BEFORE_GLOSS after $AFTER_GLOSS"
```
