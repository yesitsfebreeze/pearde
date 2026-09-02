---
complexity: 3
footprint:
  - references/parts/statusline.md
---

# spec05 — `references/parts/statusline.md` rewritten dense

The seven-term bullet run becomes a table, and the three long bullets — the
derived remainder, the persona channel, the vault URI — each become a section
whose heading states its claim. Already stands, done in the lane: `check`
green, 8 unbound pronouns to none.

**This file ends longer than it started: 430 → 437 words.** The Density rule
"a fact set is a table" turns a seven-term bullet list into a table, and the
row scaffolding costs more characters than the prose it replaces. Every other
cut in this PRD is real; here the gain is structural, not volumetric, and the
box below bounds the growth rather than pretending it away.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/statusline.md` exits `0`
- [x] the word count is within 2% of the count at `HEAD` — the table's cost, bounded
- [x] the term table carries a row for each of the seven terms the two rows render
- [x] the two-row format block is unchanged
- [x] every `@reference` present at `HEAD` is still present

## Verify and Proof

```sh
M=references/parts/statusline.md

python3 resources/prose.py check "$M"

python3 resources/prose.py stat HEAD | grep "^$M:" \
  | awk '{ exit ($4+0 <= $2*1.02) ? 0 : 1 }'

python3 - "$M" <<'PY'
import sys
t = open(sys.argv[1]).read()
for term in ["`<rd>/<rn> <rp>%`", "`+<dr>d`", "`*<dirty>`",
             "`↑<ahead> ↓<behind>`", "`<persona>`", "`▸board`", "`▸vault`"]:
    assert any(l.startswith("|") and term in l for l in t.splitlines()), \
        f"no table row for {term}"
assert "<dir> <branch> *<dirty> ↑<ahead> ↓<behind> · <model>" in t
assert "▸pearde <rd>/<rn> <rp>% · +<dr>d · open <o> <q>% · <persona> · ▸board" in t
print("spec05: 7 term rows, format block intact")
PY

git show "HEAD:$M" | grep -o '@[A-Za-z0-9_/.]*[A-Za-z0-9_]' | sort -u > /tmp/s_b.txt
grep -o '@[A-Za-z0-9_/.]*[A-Za-z0-9_]' "$M" | sort -u > /tmp/s_a.txt
comm -23 /tmp/s_b.txt /tmp/s_a.txt > /tmp/s_lost.txt
[ ! -s /tmp/s_lost.txt ]

echo "spec05: check green, growth bounded, refs kept"
```
