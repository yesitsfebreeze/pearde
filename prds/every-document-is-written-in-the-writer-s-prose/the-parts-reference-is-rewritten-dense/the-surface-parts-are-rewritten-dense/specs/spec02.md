---
complexity: 7
footprint:
  - references/parts/doctor.md
---

# spec02 — `references/parts/doctor.md` rewritten dense

The fourteen-bullet run of per-part notes becomes one `##` section per part,
each heading summarising the finding beneath it, and the opening lands on the
answer rather than a label. The part table, the usage block and every
`--fix`-ability ruling stay. Already stands, done in the lane: 1,784 → 1,775
words, `check` green, 19 unbound pronouns to none.

Seven strings in this file are pinned by `the-gate-runs-the-harnesses`. All
seven survive the rewrite, and the box below holds them.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/doctor.md` exits `0`
- [x] the word count is at or below the count at `HEAD`
- [x] all fourteen part rows of the table are still present
- [x] every string `the-gate-runs-the-harnesses` pins is intact

## Verify and Proof

```sh
M=references/parts/doctor.md

python3 resources/prose.py check "$M"

python3 resources/prose.py stat HEAD | grep "^$M:" \
  | awk '{ exit ($4+0 <= $2+0) ? 0 : 1 }'

BR=$(git show "HEAD:$M" | grep -c '^| `'); AR=$(grep -c '^| `' "$M")
[ "$AR" -ge "$BR" ]

for s in '| `harnesses`' 'harnesses: on' 'exits non-zero' \
         'a gate nobody can afford to run' 'no ledger' 'unpinned' '--harnesses'; do
  grep -qF -- "$s" "$M" || { echo "lost pin: $s"; exit 1; }
done

echo "spec02: part rows $BR->$AR, 7 harness pins intact, check green"
```
