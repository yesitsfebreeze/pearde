---
atomic: read-the-contract
subject: read the PRD, its answers and everything it cites, before the first edit
date: 2026-08-28
updated: 2026-09-02
runs: 82
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
| the `repo:` root is a worktree under `<board>/.lanes/`, `git status --short` in it is empty, and the brief says the probe's uncommitted code is already there | `lanes.create` cuts the lane off the code repo's **HEAD**, so it carries nothing the orchestrator's checkout has not committed — and with a dirty checkout that is every uncommitted pass before yours, your own included | `git -C <checkout> status --short` and `git -C <checkout> diff -- <each footprint path>`. Read the hunks: where they are entirely this PRD's, copy those files into the lane and continue there, and say in the report that the merge will refuse until the orchestrator runs `git -C <checkout> checkout -- <path>` on each file whose lane copy is a strict superset. Where a hunk is a neighbour's, leave it in the checkout and do not carry it |
| the `repo:` root is a lane, and no `footprint:` path exists under it at any depth | the footprint is board paths, and the board is a repo of its own that the lane is not a worktree of — there is nothing to copy in and nothing to merge out | work in the board repo directly, at the path the spec's `## Verify and Proof` block `cd`s to, and say so in the report. Do not create the missing tree in the lane: a second `prds/` under a lane is a board the scan will find |
| `prd.md`'s body is the unedited template — the angle-bracketed request block, no prose | the PRD was filed from a finding rather than written, and the contract lives elsewhere: in `specs/`, in a previous pass's `report.md`, or in the `report.md` of the PRD this one answers | take those as the contract and name in your report which file you read it from. Do not ask the fork back: a placeholder body is not a missing answer, it is a PRD filed by the board rather than by a person |
| the `repo:` root is a lane and a spec's `## Verify and Proof` block spells `pearde/prds/…`, or runs a command that resolves a board | `lanes.create` gives the lane no board, so the block cannot run there and every board-rooted command in it answers about the checkout | symlink the live board in at `<lane>/pearde` (both `/pearde` and `/.pearde` are gitignored) **and read the next row before you baseline anything** |
