---
state: open
origin: derived
priority: 85
complexity: 0
blast-radius:
---

# the-file-index-is-green-so-a-spec-can-assert-it

`python3 resources/index.py check` **exits 1 on `main`** and has for some
time. Measured 2026-09-04 03:20 at `676ce01`: 17 problem rows.

That would be housekeeping if the command were not in **136 spec files'
`## Verify and Proof` blocks**. A verify block is `set -e`-ish: the red exit
fails the whole block, so a PRD whose own work is perfect still collects as
`spec01 exit 1`. Two collects were blocked by exactly this on 2026-09-04 —
`pending-gets-an-expiry-not-a-decree` and
`the-tree-holds-only-what-a-board-uses/the-template-twins-fold-into-the-reference` —
and the count is only what one pass happened to reach. **This is the wall in
front of the collect queue, not a lint.**

## What is red, and why it is not one fix

Three different causes, and only the first is mechanical:

**1. Three tracked files with no row in `references/files.md`** — `.gitattributes`
(added by `7bfe99a` for the union merge), `resources/board/obsidian_register.py`
(added by `one-register-writer`), and `resources/board-name.sh` (still
untracked, see 3). Add the rows.

**2. A whole `docs/` tree that `references/files.md` documents and git does not
track.** `docs/` exists on disk — `app/ components/ content/ lib/
node_modules/` — but `git ls-files docs` is **empty** and `.gitignore` says
nothing about it. `index.py check` reads tracked files, so all 18 `@docs/…`
rows and the `@@docs` keyword read as "not on disk". **A person decides this
one**: either the fumadocs app is committed, or it is ignored and the rows and
the `@@docs` keyword come out of `references/files.md` and `index.md`. It
touches `pearde-ships-as-a-product/docs-are-densified-after-they-are-checked`.

**3. Rows for files that were planned and never built.**
`@resources/board/purge.py` is named by `references/files.md:177` and
`references/parts/handles.md:74` — its PRD,
`the-lifecycle-contract-and-purge-reclaims-it`, is `failed`.
`@resources/board/hotreload-test.js` is named by `index.md:63` under `@@view`.
Either the row goes or the file does.

**4. Probe residue committed into a product file.** `capabilities.md:58` holds
`| `zzdead` | not a real verb | — | — | python |`. A fixture row got committed.
Separately, `be` is a real verb with no row.

## Must not change

- `resources/index.py`'s own rules. The index is right and the tree is wrong;
  loosening the check to go green is the failure mode this PRD exists to
  prevent.
- The 136 verify blocks. They are correct to assert the invariant.

## Pointers

- `resources/index.py` — `check`
- `references/files.md`, `index.md`, `capabilities.md`, `references/parts/handles.md`
- sibling: `pearde-ships-as-a-product/docs-are-densified-after-they-are-checked`
- sibling: `the-lifecycle-contract-and-purge-reclaims-it` (`failed`)

## Questions

### Q1: Is the `docs/` fumadocs app committed to this repo, or ignored?

It is on disk, untracked, and fully documented in `references/files.md`. The
answer decides whether 18 rows and the `@@docs` keyword stay or go.
