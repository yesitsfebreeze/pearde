---
atomic: read-the-contract
subject: read the PRD, its answers and everything it cites, before the first edit
date: 2026-08-28
updated: 2026-09-01
runs: 50
---

# read-the-contract — the whole contract in the window before anything moves

## Do

1. `cat prds/<prd>/prd.md`. Read the body, and `## Answers`, `## Questions`
   and `## Failure` if they are there — an answer already on the file closes
   a fork you would otherwise ask again.
2. `ls prds/<prd>/specs/` and read every file it lists. A spec's own
   `workflow:` and `footprint:` override the PRD's for that unit, and its
   `## Verify and Proof` block is the command set for it.
3. Resolve every `@<path>` and `@@<keyword>` the body cites and open it. `@`
   is a path from the skill root; `@@` is a row in `index.md`, and the first
   anchor in that row is the file that answers the question.
4. `git status --short`. Write down which paths are already modified — that
   list is the only thing that later tells your hunks from someone else's.
5. Write down the `footprint:` paths and, for each, whether it exists yet.

## Done when

- Every `@` and `@@` in the body resolved to a file that exists, or the
  dangling one is named in the report.
- Every path in `footprint:` has been opened, or is stated as not yet on disk.
- The `git status --short` list is recorded before the first edit, not after.

## Fails when

| seen | means | do |
|------|-------|----|
| the coordinator reports the PRD body changed while you were building | the contract moved; the build stands on the old text | re-run this step on the new text, keep the build, name both reads in the report |
| `git status --short` lists paths the brief did not | the tree is live; other sessions wrote since the brief | record what you see now — that list, not the brief's, tells your hunks from theirs |
| a `footprint:` path is absent under the `repo:` root | the board is a `.pearde/` inside a code repo, and the footprint spans both | resolve each entry against the board root and the checkout above it, take whichever holds it, and record `git status --short` **in both** — one root's clean tree says nothing about the other's |
| a `footprint:` path does not exist and no sibling is writing it | a layout change moved the file after the specs were written | `find <board> -name '<basename>'`; if exactly one match, take it as the same file, do the contracted work there, and name both spellings in the report — a missing footprint path is a stale spelling far more often than a file to create |
| an edit aimed at `specs/spec01.md` does not find its anchor | every PRD numbers its specs from 01, so a footprint that names another PRD's files puts two identically-named `spec01.md` one directory apart — and this PRD's footprint is entirely inside another PRD's folder | anchor every spec edit on the box's own text and `assert` it before writing; then `git status --short -- prds/<other-prd>/specs/` to prove nothing landed in the neighbour. Never address a spec by number alone |
