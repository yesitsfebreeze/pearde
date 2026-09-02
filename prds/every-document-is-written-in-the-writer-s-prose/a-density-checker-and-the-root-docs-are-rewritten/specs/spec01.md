---
complexity: 14
footprint:
  - resources/prose.py
  - references/language.md
---

# spec01 — the density checker, and the rules it checks

`resources/prose.py` reads `references/language.md`'s `## Density` section
and checks the four rules a regex can hold: mean sentence length, unbound
waste words (`it`, `this`, `that`, `there` in their vague-subject shape —
`it is`, `this means`, `there are` — never the bound `this file` or `read
it`), and banned openers/closers (a preamble or a recap phrase). `stat`
prints a word count per tracked `.md` file and the tree total, and diffs
against a `ref` when one is given. Both already stand, built and run against
the real tree at `probe/prose.py` — this spec is the move into the footprint
and the `## Density` section, both already written in the lane.

## Acceptance

- [x] `python3 resources/prose.py check <clean-fixture>` exits `0`
- [x] `python3 resources/prose.py check <fixture-with-a-planted-preamble>`
      exits `1`
- [x] `python3 resources/prose.py stat` prints a `total:` line
- [x] `references/language.md` holds a `## Density` heading, and its table
      carries all nine rules from `@references/personas/writer.md`

## Verify and Proof

```sh
test -x resources/prose.py || python3 -c "import ast; ast.parse(open('resources/prose.py').read())"

D=$(mktemp -d)
cat > "$D/clean.md" <<'EOF2'
# Clean

Read `@resources/prose.py`. The checker enforces four density rules.
EOF2
cat > "$D/preamble.md" <<'EOF2'
# Preamble

This document explains the checker. Read `@resources/prose.py` for the rules.
EOF2

CLEAN=0
python3 resources/prose.py check "$D/clean.md" >/dev/null 2>&1 || CLEAN=$?
PREAMBLE=0
python3 resources/prose.py check "$D/preamble.md" >/dev/null 2>&1 || PREAMBLE=$?
rm -rf "$D"

[ "$CLEAN" = "0" ]
[ "$PREAMBLE" = "1" ]

STAT_OUT=$(python3 resources/prose.py stat 2>&1) && STAT_RC=0 || STAT_RC=$?
[ "$STAT_RC" = "0" ]
printf '%s\n' "$STAT_OUT" | grep -q '^total: [0-9]'

grep -q '^## Density$' references/language.md

RULE_ROWS=$(awk '/^## Density$/{f=1;next} /^## /{f=0} f && /^\|/' references/language.md | grep -vc -- '---')
[ "$RULE_ROWS" -ge "10" ]
grep -q 'Lead with the answer' references/language.md
grep -q 'Cut twice' references/language.md
grep -q 'No unbound' references/language.md
grep -q 'Emphasis earns its place' references/language.md

echo "spec01: 8 assertions"
```
