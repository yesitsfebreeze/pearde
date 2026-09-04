---
state: specced
origin: requested
priority: 40
complexity: 32
blast-radius: mid
workflow: probe-then-spec
---

# tags are derived when the vault is written

The `tags:`/`retag` machinery in `memos.py` and `workflows.py` exists to colour Obsidian's graph. Tags are computed when the vault or wiki is written instead of stored in every memo's frontmatter; the `retag` verbs go; the memo and invariant `no-colour-group-in-the-vault-preset-is-a-path-query` are updated to the new mechanism.

## Questions

### Q1: Where a memo's tags live

Every memo today stores four redundant tag lines that exist only to colour the graph in Obsidian, and a repair command rewrites them when they drift. Are the tags kept inside each memo file, or computed from the memo's kind at the moment the vault is written?

1. **Derive at write** — the vault writer computes the tags from each memo's kind; no memo stores tags, and the repair command goes. (recommended)
2. **Keep stored tags** — the status quo: the four lines per memo and the repair command stay, and nothing else changes.
3. **Store one tag** — each memo keeps a single tag line naming its kind; the vault writer adds the rest, and the repair command goes.

or write your own

## Done means

No memo carries `tags:`; the graph still colours by kind.

## Needs

No gate.

## Answers

**Q1** *(answered 2026-09-03 11:42)* — Derive at write — the vault writer computes the tags from each memo's kind; no memo stores tags, and the repair command goes.

## Blocked

**2026-09-03 21:57 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-tags-are-derived-when-the-vault-is-written` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-tags-are-derived-when-the-vault-is-written` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/tags-are-derived-when-the-vault-is-written`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-tags-are-derived-when-the-vault-is-written` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-tags-are-derived-when-the-vault-is-written` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/tags-are-derived-when-the-vault-is-written`.

**2026-09-04 04:12 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-tags-are-derived-when-the-vault-is-written` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-tags-are-derived-when-the-vault-is-written` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/tags-are-derived-when-the-vault-is-written`.

**2026-09-04 04:21 — the lane will not rebase**

`lane/the-tree-holds-only-what-a-board-uses-tags-are-derived-when-the-vault-is-written` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-tree-holds-only-what-a-board-uses-tags-are-derived-when-the-vault-is-written` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-tree-holds-only-what-a-board-uses/tags-are-derived-when-the-vault-is-written`.
