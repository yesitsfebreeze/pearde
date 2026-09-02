---
complexity: 8
footprint:
  - resources/board/knowledge/
---

# spec02 — the knowledge seed reads dense, and drops the legacy name

The five tracked `.md` files under `resources/board/knowledge/` rewritten
against `## Density` in @references/language.md. `WORKFLOW.md`'s title read
`# Vicky Workflow` — a former product name, which `## Rules` in
@references/language.md bans outright; the rewrite retitles it. Every
frontmatter key `resources/knowledge.py` reads, and every Dataview block,
survives character-identical.

`Dashboard.md` is the file this retry turns on. Commit `8f6ccfa
the-map-is-a-note-per-file-not-a-flat-table` appended a "File index" section
to it after the lane branched, in three undense paragraphs. The lane's own
rewrite is clean and main's own file is clean of everything but that section,
so **only the merge is red** — which is where `collect` runs the gate.

## What already stands

- `WORKFLOW.md` retitled `# Knowledge workflow — the loop's configuration`,
  its preamble and its trailing `## Notes for agents` folded into the lead and
  `## Rules`, and `### crystalize` moved under `## Workflows` where the other
  three workflows live.
- `Dashboard.md`, `conclusions/_index.md`, `sources/_index.md` and
  `sources/.absorbed/_index.md` rewritten; every Dataview and DataviewJS
  fence untouched.
- The three paragraphs `8f6ccfa` appended to `Dashboard.md` rewritten dense,
  uncommitted in the lane — four words, exactly the repair the retry asked
  for, and no section was split out. Both directions are proven: the merged
  tree with main's paragraphs reports `Dashboard.md: 4 unbound waste word(s)
  (it, that, this)` and exits 1; with the lane's, `prose.py check` exits 0.
- `pearde init` plants all five, and `knowledge.py doctor` prints
  `doctor: clean` on the planted vault.

## What is left

- Land the lane, the uncommitted `Dashboard.md` with it, and re-run the boxes
  on the merged tree. Box 1 is the one that was red; nothing else in this
  spec has work in it.
- If main appends to `Dashboard.md` again before this lands, the same repair
  is owed again — the section belongs to whoever writes it, and box 1 names
  no exclusion.

## Acceptance

- [x] on the merged tree, `python3 resources/prose.py check` names no file under `resources/board/knowledge/` — the "File index" sections `8f6ccfa` appended included, with no exclusion carved for them
- [x] `WORKFLOW.md` frontmatter still carries `type`, `active_focus`, `priority_tags`, `research_depth`, `auto_enqueue`, `min_sources_per_conclusion` and `default_workflow`, with the same values
- [x] no `.md` file under `resources/board/knowledge/` contains the string `Vicky`
- [x] the four workflow ids `default`, `deep-dive`, `triage` and `crystalize` each keep their numbered steps, and the four `## Routing` table rows are unchanged
- [x] every Dataview and DataviewJS fence in `Dashboard.md`, `conclusions/_index.md` and `sources/_index.md` is byte-identical to main's
- [x] `pearde init` into an empty dir plants all five files and `knowledge.py doctor` on the planted vault prints `doctor: clean`

## Verify and Proof

```sh
bash .pearde/prds/every-document-is-written-in-the-writer-s-prose/\
example-and-knowledge-fixtures-are-rewritten-dense/probe/verify_merged.sh
```

Box 1 alone, if the merged tree is already unpacked at `$M`:

```sh
python3 resources/prose.py check $(cd "$M" && find resources/board/knowledge -name '*.md')
```
