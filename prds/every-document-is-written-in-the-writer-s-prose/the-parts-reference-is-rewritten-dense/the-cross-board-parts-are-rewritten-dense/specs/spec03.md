---
complexity: 3
footprint:
  - references/parts/machine.md
  - references/parts/all.md
  - references/parts/master.md
---

# spec03 — the three rewritten files held green and committed

`machine.md`, `all.md` and `master.md` are rewritten dense in the lane and
green: `prose.py check` exits 0 on each and the fact probe reports zero losses
against `fc75bcf`. Nothing is left to write. This unit exists so the work
sitting uncommitted in the lane has a box of its own, and so a later edit to
the other two files cannot redden these three without a check catching it.

| file | words at `fc75bcf` | words now | cut | hits cleared |
|---|---|---|---|---|
| `references/parts/machine.md` | 2412 | 2385 | 1.1% | 20 |
| `references/parts/all.md` | 996 | 1071 | see below | 7 |
| `references/parts/master.md` | 653 | 637 | 2.4% | 1 |

`all.md` grew against `fc75bcf` because another PRD landed a paragraph in it
after the lane was cut — *a pass is rendered here as what it asks* — and the
lane carries that paragraph verbatim. Measured against the text the rewrite
actually replaced the file went 1,085 to 1,071 words, the same 1.4% cut.

One file under `references/parts/` still violates the density rule:
`commits.md`, three unbound waste words, owned by no PRD in this set. The
count was 2 when the specs were written; a sibling closed the other between
that pass and this one.

## Acceptance

- [x] `python3 resources/prose.py check` is silent and exits 0 on all three files named in the footprint
- [x] the fact probe reports `0 lost` on all three against `fc75bcf`
- [x] the three files' rewrite is committed, not left standing — `git status --short` names none of them in the tree `collect` measures, `collect` step 1b having committed the lane (@references/parts/commits.md: the worker never commits)
- [x] `python3 resources/prose.py check references/parts/*.md` names none of this PRD's five files, and prints how many files under `references/parts/` still violate — 1, `references/parts/commits.md`, not one of this PRD's

## Verify and Proof

```sh
BASE=fc75bcf   # the lane cut — the fact baseline
PRD="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)/.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-parts-reference-is-rewritten-dense/the-cross-board-parts-are-rewritten-dense"
F="references/parts/machine.md references/parts/all.md references/parts/master.md"
python3 resources/prose.py check $F
python3 "$PRD/probe/facts.py" diff "$BASE" $F
[ -z "$(git status --short -- $F)" ]
hits=$({ python3 resources/prose.py check references/parts/*.md || true; })
n=$({ printf '%s' "$hits" | grep -c . ; } || true)
echo "violating files under references/parts/: $n"
if printf '%s\n' "$hits" | grep -E 'parts/(machine|all|master|handles|ramp)\.md'; then exit 1; fi
```
