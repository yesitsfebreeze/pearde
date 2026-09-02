---
complexity: 4
footprint:
  - references/parts/progress.md
---

# spec04 — `references/parts/progress.md` rewritten dense

The opening drops its label and leads on the rule, the reading notes gather
under a heading that states them, and the persona and status-line paragraphs
each get a heading naming their claim. The twelve-row term table is untouched.
Already stands, done in the lane: 591 → 580 words, `check` green, 4 unbound
pronouns to none.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/progress.md` exits `0`
- [x] the word count is at or below the count at `HEAD`
- [x] every row of the term table at `HEAD` is still present
- [x] the rendered progress-line format string is unchanged

## Verify and Proof

```sh
M=references/parts/progress.md

python3 resources/prose.py check "$M"

python3 resources/prose.py stat HEAD | grep "^$M:" \
  | awk '{ exit ($4+0 <= $2+0) ? 0 : 1 }'

BR=$(git show "HEAD:$M" | grep -c '^|'); AR=$(grep -c '^|' "$M")
[ "$AR" -ge "$BR" ]

grep -qF 'done <rd>/<rn> · <rp>% · derived <dd>/<dn> · open <o>/<n>' "$M"
grep -qF 'ready <r> · blocked <b> · collect <c> @<w> workers · as <persona>' "$M"

echo "spec04: table rows $BR->$AR, format string intact, check green"
```
