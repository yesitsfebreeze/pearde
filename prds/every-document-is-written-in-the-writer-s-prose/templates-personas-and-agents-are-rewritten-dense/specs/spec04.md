---
complexity: 11
footprint:
  - references/templates/grammar.md
  - references/templates/health.md
  - references/templates/prd.md
  - references/templates/spec.md
  - references/templates/memo.md
  - references/templates/report.md
  - references/templates/workflow.md
  - references/templates/atomic.md
  - references/templates/vision.md
---

# spec04 — the nine shapes code copies are rewritten dense, and still round-trip

The seven bare templates plus `grammar.md` and `health.md` carry the same facts
in fewer words. Unlike the `.doc.md` companions, code copies these: a rewrite
lands in every board written from here on, so each writer is re-run afterwards.

The cuttable surface is small and unevenly spread, measured by
`probe/surface.py`:

| file | words | cuttable | who copies it |
|---|---|---|---|
| `grammar.md` | 4,122 | 309 (7%) | `grammar.py init`, whole, `<board>` and `<today>` substituted |
| `health.md` | 377 | 145 (38%) | nothing — `health.py` writes notes in this shape |
| `memo.md` | 83 | 50 (60%) | `memos.py add` |
| `report.md` | 85 | 67 (79%) | nothing — a person writes from it |
| `prd.md` | 65 | 47 (72%) | `pearde add`, `pearde refine` |
| `atomic.md` | 60 | 24 (40%) | existence-checked by `workflows.py add`, never read |
| `spec.md` | 48 | 19 (40%) | the analyst, by hand |
| `workflow.md` | 83 | 23 (28%) | existence-checked by `workflows.py add`, never read |
| `vision.md` | 36 | 13 (36%) | `pearde init` |

`grammar.md` is 3,740 of its 4,122 words in table rows — the shipped vocabulary
of every board, and every row a fact that survives as a row. Its rewritable
share is 309 words of prose and headings, so it takes the smallest cut of any
file in this PRD and carries the largest risk.

`health.md`'s frontmatter is 224 of its 377 words, comments holding the
threshold constants that `health.py` implements. Those numbers are facts.

One collision the probe hit: `prose.py check` does not strip frontmatter, so it
reads `health.md`'s key comments as prose and flags `the day it was scored` for
its `it was`. Reword the comment; the key set, its order and its constants stay.

## Acceptance

- [x] `python3 resources/prose.py check references/templates/grammar.md references/templates/health.md references/templates/prd.md references/templates/spec.md references/templates/memo.md references/templates/report.md references/templates/workflow.md references/templates/atomic.md references/templates/vision.md` exits 0.
- [x] The group's words, `prose.py`'s own count, fall from 4690 to **4646 or fewer** — `prose.py stat <base>` summed over the group's lines. 0.9% off, the measured floor, and the check fails on the count itself.
- [x] `grammar.md` keeps every table row: its count of lines beginning `|` is unchanged, and every `**<term>**` of the base revision is still present, spelled identically.
- [x] `grammar.md` keeps its group headings in order, ending on `## This repo`, and still carries `<board>` and `<today>` for `grammar.py init` to substitute.
- [x] `health.md` keeps its frontmatter keys, in order, with every threshold number of the base revision — 150, 1500, 300, 3000, 10, 50, 4, 40, 400, 80, 800, 3, 20, 2, 25, 0.10, 0.50 — present.
- [x] Every bare template keeps its frontmatter keys and its headings unchanged; only placeholder prose inside angle brackets is rewritten.
- [x] The round-trip in `## Verify and Proof` exits 0 on a fresh temp board — `grammar.py init` then `check`, `memos.py add` then `check`, `workflows.py add` for both kinds then `check`. `probe/roundtrip.sh` is the same script standalone.
- [x] `python3 resources/index.py check` names no `@` in `references/templates/`.

## Verify and Proof

```sh
BASE=${BASE:-$(git merge-base HEAD main)}
set -e
python3 resources/prose.py check references/templates/grammar.md references/templates/health.md references/templates/prd.md \
  references/templates/spec.md references/templates/memo.md references/templates/report.md references/templates/workflow.md references/templates/atomic.md \
  references/templates/vision.md

# grammar.md keeps every row and every term
a=$(git show "$BASE:references/templates/grammar.md" | grep -c '^|')
b=$(grep -c '^|' references/templates/grammar.md)
[ "$a" = "$b" ] || { echo "grammar.md: $a rows -> $b"; exit 1; }
git show "$BASE:references/templates/grammar.md" | grep -o '\*\*[^*]*\*\*' | sort -u > /tmp/t.old
grep -o '\*\*[^*]*\*\*' references/templates/grammar.md | sort -u > /tmp/t.new
if comm -23 /tmp/t.old /tmp/t.new | grep -q .; then
  comm -23 /tmp/t.old /tmp/t.new; echo "grammar.md lost a term"; exit 1
fi
grep -q '<board>' references/templates/grammar.md
grep -q '<today>' references/templates/grammar.md
grep -q '^## This repo' references/templates/grammar.md

# health.md keeps its ordered key set and every threshold
git show "$BASE:references/templates/health.md" | sed -n '2,/^---$/p' | cut -d: -f1 > /tmp/k.old
sed -n '2,/^---$/p' references/templates/health.md | cut -d: -f1 > /tmp/k.new
diff /tmp/k.old /tmp/k.new
for n in 150 1500 300 3000 10 50 4 40 400 80 800 3 20 2 25 0.10 0.50; do
  grep -q -- "$n" references/templates/health.md || { echo "health.md lost $n"; exit 1; }
done

# every writer that copies a template still round-trips, on a fresh board
R=$(mktemp -d)/repo
mkdir -p "$R/pearde/prds" "$R/pearde/memos" "$R/pearde/workflows"
printf -- '---\nname: probe\n---\n' > "$R/pearde/settings.md"
python3 resources/grammar.py init "$R/pearde" >/dev/null
python3 resources/grammar.py check "$R/pearde"
grep -q '^## This repo' "$R/pearde/grammar.md"
python3 resources/memos.py add "a probe subject" "$R/pearde" >/dev/null
python3 resources/memos.py check "$R/pearde"
printf '# a-probe-step — the unit in a phrase\n\n## Do\n\n1. Run the probe.\n\n## Done when\n\n- The probe exits 0.\n\n## Fails when\n\n| seen | means | do |\n|------|-------|----|\n' \
  | python3 resources/workflows.py add a-probe-step atomic "a probe step" "$R/pearde" >/dev/null
printf '# a-probe-job — the job in a phrase\n\n## Use when\n\n- A probe job.\n- Not a real job; use `probe-then-spec`.\n\n## Steps\n\n| # | atomic | why | on failure |\n|---|--------|-----|------------|\n| 1 | `a-probe-step` | proves the copy | `stop` |\n' \
  | python3 resources/workflows.py add a-probe-job workflow "a probe job" "$R/pearde" >/dev/null
python3 resources/workflows.py check "$R/pearde"
rm -rf "$(dirname "$R")"

if python3 resources/index.py check | grep -q '^references/templates/'; then
  echo "a dangling @ under references/templates/"; exit 1
fi
# the ceiling, on prose.py's own count
python3 resources/prose.py stat "$BASE" | grep -E 'templates/(grammar|health|prd|spec|memo|report|workflow|atomic|vision)\.md:' \
  | awk -F'[ >]+' '{b+=$2; a+=$4} END {
      printf "group: %d -> %d (%.1f%% off)\n", b, a, 100*(b-a)/b;
      if (a > 4646) { printf "over the %d ceiling\n", 4646; exit 1 } }'
```
