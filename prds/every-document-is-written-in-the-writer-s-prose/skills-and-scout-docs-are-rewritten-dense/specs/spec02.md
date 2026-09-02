---
complexity: 4
footprint:
  - resources/scout/README.md
  - resources/scout/findings.md
  - resources/scout/reading-list.md
  - resources/scout/routes.md
---

# spec02 — the four scout documents read dense, every route id intact

`README.md`, `findings.md`, `reading-list.md` and `routes.md` rewritten
against `## Density` in @references/language.md. These four carry the scout
layer's addressable data: 45 route ids `route.sh` resolves by name, the
finding table's verdict rows, and the reading list's mechanism rows. Every
table row survives as a row and every id resolves to the same page.

Every box below is measured on the **merged tree**, for the reason spec01
gives, and here it is not a formality: `main` added a 70-line finding to
`findings.md` after this lane's base, and the lane alone cannot show it.

## What already stands

- All four rewritten; `python3 resources/prose.py check resources/scout/*.md`
  exits 0 on the lane.
- 7,876 words to 7,829. `findings.md` keeps every `**Why**`,
  `**Overturned by**` and `**Route gotcha**` paragraph as a paragraph.
- `bash resources/scout/route.sh list` returns 45 on the merged tree, and the
  route id set diffs clean against `main`.
- The lane merges into `main` without a conflict: `git merge-tree
  --write-tree` exits 0 and `main`'s new finding and its summary row both
  survive — 84 table rows on both sides.
- Boxes 2 to 6 are green on the merged tree today.

## What is left

- One sentence, in the section `main` added under this lane. On the merged
  tree `prose.py` reports `resources/scout/findings.md: 1 unbound waste word
  (it)` at *"(2.4.0, 2025-12-18), and it is a kernel extension: a reboot,
  redu…"*. Rewrite that clause after `collect` merges — it does not exist in
  the lane, and adding it there by hand turns a clean merge into a conflict.
- Then re-run `probe/verify.sh`; box 1 is the only red one and it closes on
  that edit.

## Acceptance

- [x] on the merged tree, `python3 resources/prose.py check resources/scout/*.md` exits 0
- [x] `bash resources/scout/route.sh list` returns 45 lines
- [x] the set of route ids in `routes.md` is unchanged against `main`
- [x] each of the four files has the same count of table rows as on `main` — `findings.md` 84 included
- [x] `python3 resources/index.py check` prints exactly what it prints on `main`, line for line
- [x] the scope's word count, code stripped, is below `main`'s across `references/skills/` and `resources/scout/` together

## Verify and Proof

```sh
bash pearde/prds/every-document-is-written-in-the-writer-s-prose/\
skills-and-scout-docs-are-rewritten-dense/probe/verify.sh
```

The lines prefixed `spec02.` are this spec's six boxes, `spec02.4` counted
once per file. `REF=main bash …` is the negative control: it reddens
`spec02.1` and `spec02.6`.
