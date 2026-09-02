---
complexity: 5
footprint:
  - references/skills/
---

# spec01 — the nineteen skill files read dense, frontmatter included

All 19 tracked `.md` files under `references/skills/` rewritten against
`## Density` in @references/language.md. Six `description:` lines are rewritten
with them, which the PRD's answered question authorises: *rewrite the
summaries too — every phrase that makes a tool fire is kept word for word*.
Every `name:`, every quoted trigger phrase and every backticked span in a
description survives character-identical, so an agent harness fires the same
skill on the same words.

Every box below is measured on the **merged tree**, never on the lane and
never on `main`. `collect` commits the lane's uncommitted files and then
merges, and `main` has moved under this lane. `probe/verify.sh` builds that
tree from a temp index and moves no branch.

## What already stands

- 18 of 19 bodies rewritten and green; `pearde-graph.md` was already dense.
- Six `description:` lines rewritten: `pearde-all`, `pearde-drill`,
  `pearde-machine`, `pearde-persona-ask`, `pearde-scout`, `pearde-workflow`.
  The other thirteen are untouched.
- `python3 resources/prose.py check references/skills/*.md` exits 0.
- 4,583 words to 4,445, and `pearde-all`'s description from 1,038 characters
  to 980 — under the 1,024-character skill-description cap it broke on `main`.
- Boxes 1 to 5 below are green on the merged tree today, and `REF=main bash
  probe/verify.sh` reddens 1, 3 and 5, so the set can still fail.

## What is left

- Land the lane and re-run `probe/verify.sh` against whatever `main` is then.
  Nothing in this spec has writing left in it.

## Acceptance

- [x] on the merged tree, `python3 resources/prose.py check references/skills/*.md` exits 0
- [x] every `name:` line in `references/skills/*.md` is byte-identical to `main`'s
- [x] in every `description:`, the ordered list of `"quoted"` phrases and of backticked spans is byte-identical to `main`'s
- [x] no `description:` value exceeds 1,024 characters
- [x] `bash resources/doctor.sh` reports `skills ok 19 well-formed`
- [x] `git diff --name-status main <merged-tree> -- references/skills/ resources/scout/` names 18 or more files and every line is `M` — no add, no rename, no delete

## Verify and Proof

```sh
bash pearde/prds/every-document-is-written-in-the-writer-s-prose/\
skills-and-scout-docs-are-rewritten-dense/probe/verify.sh
```

One `PASS`/`FAIL` line per box and `boxes N/14` at the end; spec01's six are
the lines prefixed `spec01.`. `REF=main bash …` is the negative control.
