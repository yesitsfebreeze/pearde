---
complexity: 4
footprint:
  - docs/content/docs/improvements/lifecycle-contract.mdx
---

# spec03 — the improvement page the PRD cites as its own source

The page this PRD's own `## Why now` and `## Done when` are copied from —
`title`/`description` frontmatter, the same `Why now` → `The change` →
`Done when` → `Fails when` → `What stays out` shape every other page in
`docs/content/docs/improvements/` carries, plus the participant table this
PRD's `## The change` only names in prose.

What already stands: the page's content, drafted in the same pass that
built `purge.py` and reproduced whole into this lane's footprint at
`docs/content/docs/improvements/lifecycle-contract.mdx`.

What is left, and why it is not this spec's to finish: `docs/` itself —
the fumadocs app (`docs/package.json`, `docs/app/`, `docs/lib/`, thirty-odd
sibling pages under this same directory) — carries no git history on this
machine; `git ls-files docs/` returns nothing on the branch this lane was
cut from, and the copy on disk in the checkout this lane's board lives
under is itself uncommitted. Linking this page into
`docs/content/docs/improvements/meta.json`'s `pages` array and
`index.mdx`'s summary table means editing two files a much larger,
separate effort (the docs axis of `pearde-ships-as-a-product`) is also
mid-write on, uncommitted, in that same checkout — see `## Findings` in
the report. This spec's footprint is the one file that is unambiguously
this PRD's alone; the two shared files are named here as not-yet-safe to
touch rather than left unmentioned.

## Acceptance

- [x] The page exists at `docs/content/docs/improvements/lifecycle-contract.mdx`,
  with `title`/`description` frontmatter and the five sections every
  improvement page carries
  - proof: `test -f docs/content/docs/improvements/lifecycle-contract.mdx` on the lane; `grep -c '^## ' …` → 5 (`Why now`, `The change`, `Done when`, `Fails when`, `What stays out`)
- [ ] `docs/content/docs/improvements/meta.json`'s `pages` array and
  `index.mdx`'s table both name `lifecycle-contract` — left open: both
  files are mid-write by the sibling docs effort in the checkout this
  board lives under, uncommitted; adding a row here races that write
  rather than joining it. Whichever of the two commits first should carry
  this one entry, and the other rebase onto it.

## Verify and Proof

```sh
LANE="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"
test -f "$LANE/docs/content/docs/improvements/lifecycle-contract.mdx"
grep -c '^## ' "$LANE/docs/content/docs/improvements/lifecycle-contract.mdx"   # 5
head -4 "$LANE/docs/content/docs/improvements/lifecycle-contract.mdx" | grep -q '^title:'
```
