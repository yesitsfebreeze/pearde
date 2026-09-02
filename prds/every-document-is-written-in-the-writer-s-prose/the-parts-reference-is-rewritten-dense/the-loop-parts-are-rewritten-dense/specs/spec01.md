---
complexity: 4
footprint:
  - references/parts/roles.md
  - references/parts/solo.md
  - references/parts/derived.md
  - references/parts/contract.md
  - references/parts/board.md
---

# spec01 — the five small loop parts, rewritten dense

The five files under 700 words: `roles`, `solo`, `derived`, `contract` and
`board`. Each opens on its finding, states each rule once, and carries every
backtick span, table cell, heading and `@path` present at the lane's base
commit.

**Already standing.** The analyst's build rewrote all five in the lane;
`prose.py check` and the fact check are green on each, and the five total
1,753 words against 1,816 at the base. `board.md`'s four-way rationale for
the un-named board directory — a setting, a marker file, an environment
variable, a `.claude/settings.json` key — became a four-row table rather than
being deleted, and no memo carries that rationale, so the table is the only
copy.

**Left to finish.** Review the five against the nine rules in
@references/language.md's `## Density` that no checker holds — lead with the
answer, headings summarise, cut twice, a fact set is a table, reference
describes never teaches, emphasis earns its place — and cut further wherever a
fact survives the cut. `contract.md` is 13% prose and was already green; a
word cut there would be a fact cut, so it is held, not reduced.

## Acceptance

- [x] `python3 resources/prose.py check` prints nothing for each of the five files and exits 0
- [x] the fact check prints nothing for the five files against the lane's base commit and exits 0
- [x] the five files together hold fewer words at `prose.py stat` than at the base commit
- [x] `git diff --name-status <base> -- references/parts` shows no row beginning `R` or `D` — none of the five renamed, none deleted
- [x] `python3 resources/index.py check` prints no line naming any of the five files
- [x] `board.md` holds one table row for each of the four rejected alternatives to a configurable board directory

## Verify and Proof

```sh
BASE=$(git merge-base HEAD main)   # fc75bcf at the lane cut
ROOT=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
PRD=$ROOT/.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-parts-reference-is-rewritten-dense/the-loop-parts-are-rewritten-dense
F="references/parts/roles.md references/parts/solo.md references/parts/derived.md references/parts/contract.md references/parts/board.md"
python3 resources/prose.py check $F              # silent, exit 0
python3 "$PRD/probe/facts.py" "$BASE" $F         # silent, exit 0
python3 resources/prose.py stat "$BASE" | grep -E 'parts/(roles|solo|derived|contract|board)\.md'
git diff --name-status "$BASE" -- references/parts
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
case "$rc" in 0|1) ;; *) echo "index.py check crashed: $rc"; exit 1;; esac
if printf '%s\n' "$out" | grep -E 'parts/(roles|solo|derived|contract|board)\.md'; then exit 1; fi
grep -c '^| a' references/parts/board.md        # 4 rejected alternatives, one row each
```
