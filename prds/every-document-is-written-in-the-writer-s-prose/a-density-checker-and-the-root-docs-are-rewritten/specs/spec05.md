---
complexity: 3
footprint:
  - SKILL.md
---

# spec05 — `SKILL.md` rewritten dense

The three numbered sections are cut for density — no unbound pronoun, no
redundant clause. The frontmatter (`name:`, `description:`), both `bash`
blocks and the closing bullet list are untouched. Already stands, done in
the lane.

## Acceptance

- [x] `python3 resources/prose.py check SKILL.md` exits `0`
- [x] the frontmatter is byte-identical to `HEAD`
- [x] both fenced `bash` blocks are byte-identical to `HEAD`

## Verify and Proof

```sh
OUT=$(python3 resources/prose.py check SKILL.md 2>&1) && RC=0 || RC=$?
[ "$RC" = "0" ]
printf '%s\n' "$OUT"

git show HEAD:SKILL.md | awk 'BEGIN{n=0} /^---$/{n++; if(n<=2) print; next} n==1' > /tmp/skill-fm-before.$$
awk 'BEGIN{n=0} /^---$/{n++; if(n<=2) print; next} n==1' SKILL.md > /tmp/skill-fm-after.$$
cmp /tmp/skill-fm-before.$$ /tmp/skill-fm-after.$$
rm -f /tmp/skill-fm-before.$$ /tmp/skill-fm-after.$$

git show HEAD:SKILL.md | awk '/^```/{f=!f;next} f' > /tmp/skill-code-before.$$
awk '/^```/{f=!f;next} f' SKILL.md > /tmp/skill-code-after.$$
cmp /tmp/skill-code-before.$$ /tmp/skill-code-after.$$
rm -f /tmp/skill-code-before.$$ /tmp/skill-code-after.$$

echo "spec05: 3 assertions"
```
