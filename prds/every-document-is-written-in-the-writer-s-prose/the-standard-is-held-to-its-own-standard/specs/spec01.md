---
complexity: 8
footprint:
  - references/language.md
---

# spec01 — the standard passes the checker it defines

`python3 resources/prose.py check references/language.md` exits `0`. The
standard was the one file the density rules never ran against: its own body
carried the bare counter-example `"This is important for correctness"`, and
the checker read the quote as the file's own vague-subject prose. Every
quoted example of banned prose is now backticked, the `## Density` table
carries the convention as a rule, and the rule bullets are cut without losing
one. Built and standing in the lane, uncommitted — this spec is the check
that it stays true.

## Acceptance

- [x] `python3 resources/prose.py check references/language.md` exits `0`
- [x] The `## Density` table carries a row naming the backticked-example
      convention, and still carries all nine rules it held before
- [x] All eleven `## Rules` bullets survive, each by its lead phrase
- [x] `## Where prose stays` and the seven-row `## Shape per document` table
      survive, README exemption included
- [x] `python3 resources/prose.py stat` reports `references/language.md` at
      `611` words or fewer — its count before the rewrite
- [x] `python3 resources/index.py check` prints no line about
      `references/language.md` other than the pre-existing
      `@references/personas/writer.md` one, which closes on the merge

## Verify and Proof

```sh
python3 resources/prose.py check references/language.md

ROWS=$(awk '/^## Density$/{f=1;next} /^## /{f=0} f && /^\|/' references/language.md | grep -vc -- '---')
[ "$ROWS" -ge "11" ]
grep -q 'A quoted example of banned prose is backticked' references/language.md
for r in 'Lead with the answer' 'Every heading summarises what is beneath it' \
         'Cut twice' 'A fact set is a table, a sequence a numbered list' \
         'About twenty words a sentence, on average' 'No unbound' \
         'Reference describes, never teaches' 'No preamble, no recap, no closer' \
         'Emphasis earns its place'; do
  grep -q "$r" references/language.md || { echo "density rule lost: $r"; exit 1; }
done

for r in 'Structure over prose' 'One idea per sentence' 'Imperative' \
         'Name the thing' 'Address, do not describe a path' \
         'where the reader needs the scope' 'No hedging' 'No meta' 'No legacy' \
         'Rationale only where it changes a decision' 'Delete, do not deprecate'; do
  grep -q "$r" references/language.md || { echo "rule lost: $r"; exit 1; }
done

grep -q '^## Where prose stays$' references/language.md
grep -q 'Alternatives considered' references/language.md
SHAPE=$(awk '/^## Shape per document$/{f=1;next} /^## /{f=0} f && /^\|/' references/language.md | grep -vc -- '---')
[ "$SHAPE" -ge "8" ]
grep -q '| README        | a person, first time | quickstart, then rings |' references/language.md
grep -q 'a sentence there may' references/language.md

WORDS=$(python3 resources/prose.py stat | awk -F': ' '$1=="references/language.md"{print $2}')
[ -n "$WORDS" ] && [ "$WORDS" -le "611" ]

IDX=$(python3 resources/index.py check 2>&1 | grep -c 'references/language.md' || true)
[ "$IDX" -le "1" ]
python3 resources/index.py check 2>&1 | grep 'references/language.md' \
  | grep -qv 'personas/writer.md' && { echo "new dangling address in language.md"; exit 1; } || true

echo "spec01: 6 boxes, $ROWS density rows, $WORDS words"
```
