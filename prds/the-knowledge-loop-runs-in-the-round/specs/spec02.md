---
goal: The analyst brief queries the knowledge base before it reads the PRD, and every worker writes outside findings back to it
complexity: 5
footprint: references/parts/workers.md
---

# spec02 — the analyst and every-worker briefs reach for the record

## What already stands

Applied directly in the tree, uncommitted, per `probe/workers-md-patch.md`:
- `<!-- brief:analyst -->` now opens with "Query the record first:
  `python3 resources/knowledge.py query "<the PRD's question>"` from
  `<repo>`..." before the existing "Read `.pearde/prds/<prd>/prd.md`..."
  line — the gap-auto-enqueue behaviour is `knowledge.py query`'s own, cited
  not reimplemented.
- `<!-- brief:every -->` now carries "A fact learned outside this repo... is
  written back with `python3 resources/knowledge.py remember`..." — the
  first draft used a literal `<title>` placeholder, which `brief.py`'s
  `TOKEN_RE` does match (unlike `<the PRD's question>`, which has a space
  and an apostrophe) — fixed to name the verb without a bracketed argument
  so no new placeholder-table row is needed.
- `python3 resources/board/brief.py --check` exits 0.

## What is left to finish

Nothing — closed; verified below. (Earlier note, now stale: a pre-existing,
unrelated bug — `brief_prd()` calling `collectlib.repo_of(prd, board_root)`
with 2 args against a `repo_of(prd, board, board_root)` signature, `TypeError`
on any real render — was fixed by commit `0849795`, PRD
`collect-commits-the-code-repo-not-the-board-repo-twice`. Nothing left on
this spec's side; see report.md.)

## Acceptance

- [x] `<!-- brief:analyst -->` opens with the `Query the record first`
      sentence, before `Read \`.pearde/prds/<prd>/prd.md\``
- [x] `<!-- brief:every -->` carries the `A fact learned outside this repo`
      sentence, with no new unnamed placeholder
- [x] `python3 resources/board/brief.py --check` exits 0

## Verify and Proof

```sh
set -e
python3 resources/board/brief.py --check
grep -q "Query the record first" references/parts/workers.md
grep -q "A fact learned outside this repo" references/parts/workers.md
echo "spec02: workers.md queries first, writes findings back — ok"
```
Run 2026-08-31 (analyst pass): `brief.py --check` exit 0, both greps hit,
echo printed. Re-run 2026-08-31, implementer, against the files now on disk:
`brief.py --check` exit 0 again, both greps hit again, echo printed, exit 0.
Box 1 additionally proven ordered (the block's `Query the record first` line
is 133, the `Read .pearde/prds/<prd>/prd.md` line 139); box 2 additionally
proven by token dump — both blocks hold only table placeholders
(`every`: `<language>`, `<prd>`), nothing for `--check` to flag.
