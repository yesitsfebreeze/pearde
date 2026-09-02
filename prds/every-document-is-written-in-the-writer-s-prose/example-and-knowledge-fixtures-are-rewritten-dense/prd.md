---
state: done
origin: requested
priority: 55
complexity: 16
blast-radius:
needs:
  - a-density-checker-and-the-root-docs-are-rewritten
actual: 1.19h
commit: 9889e78 1614faa
---


# example-and-knowledge-fixtures-are-rewritten-dense — resources/board/example/**` and `resources/board/knowledge/**` rewritten dense, checked against any harness reading them verbatim

resources/board/example/**` and `resources/board/knowledge/**` rewritten dense, checked against any harness reading them verbatim

## History

**failed, retried 2026-09-02 20:42**

The worker reported DONE, 17/17. The orchestrator does not believe it, on two
independent pieces of evidence. The work itself is largely sound — sixteen of
the seventeen boxes reproduce — so this is one short pass, not a redo. The
lane keeps the work; do not redo the eighteen fixture files.

**1 · `pearde collect` refused the merge.** The lane branched at `d240590`;
main is now `fc75bcf`, four commits ahead. `collect` reported
`merge conflict: lane/…-example-and-knowledge-fixtures-are-rewritten-dense
into main`, wrote nothing, and left the work on the lane. The tree is clean —
no conflict markers, no partial merge.

**2 · Two boxes go red on the merged tree.** Commit `8f6ccfa
the-map-is-a-note-per-file-not-a-flat-table` appended a "File index" section
to `resources/board/knowledge/Dashboard.md` after the lane left:

    python3 resources/prose.py check $(git ls-files \
      'resources/board/example/*.md' 'resources/board/knowledge/*.md')
    resources/board/knowledge/Dashboard.md: 4 unbound waste word(s) (it, that, this)
    exit 1

That fails **spec02 box 1** (`names no file under resources/board/knowledge/`)
and **spec03 box 5** (`names no file under example/ or knowledge/`). The lane
version alone is clean; main's version alone is red; the merge keeps main's
undense paragraphs. Every gate in the worker's report was run against a base
four commits stale, and `collect` runs on the merged tree.

**3 · spec03 box 3 is closed against a state that has already reverted.**
`pearde/memos/README.md` is untracked — `git ls-files pearde` returns 0. It is
machine-local, shared by every lane, carried by no merge. The worker
regenerated it at 18:37 with the new banner; another session's `memo add`
overwrote it at 19:56:59 with the old-banner generator. `memos.py check` from
the repo root — the exact call spec03's own Verify block makes — now returns
`README.md: the kind index is stale — run memo index`, exit 1. The report's
load-bearing claim that it "needs no follow-up once the lane lands" is false.

### What the retry owes

1. **Rebase the lane onto `fc75bcf`**, resolve the conflict, and re-run
   spec02 box 1 and spec03 box 5. Either rewrite the appended `Dashboard.md`
   section dense inside this lane — it is four words — or split it out and
   amend both boxes to name the exclusion explicitly. A box that only passes
   on a stale base is not closed.
2. **Strike or replace spec03 box 3.** It asserts a property of an untracked,
   shared, machine-local directory that no merge carries and any concurrent
   session overwrites. Replace it with something the generator owns end to
   end — `memos.py check` on a fresh `pearde init` board — and add
   `python3 resources/memos.py index pearde` as a named landing step.

### What is not the reason

"Verified rather than redone" is not a gap. All seventeen boxes are
outcome-shaped — checker exit codes and byte-comparisons — and were re-run
independently against the lane tree. Who typed the prose has no bearing on
whether `prose.py` exits 0 or whether `plan.py scan` comes back
byte-identical. Re-deriving the analyst's rewrite would produce different
words and the identical green.

Two stale claims in the worker's own report, so the retry does not act on
them: "nothing committed" is wrong — `b513b01` was committed and rebased to
`ad01d84` at 18:37:58, thirty-six seconds after the report was written; and
its `find_board` defect is already fixed on main by `b150992` / `6085233`.

Disclosed and not disqualifying: the analyst wrote eighteen files of
implementation and then wrote the acceptance boxes for its own work, as each
spec states under "What already stands". It does not make the runs wrong, but
`prose.py` counts words, sentence length and waste words — passing a word
counter is not the same claim as "reads dense", and this PRD never made the
second one.

## Report

spec01: exit 0
merged tree 99d55648936f8f4e59838c54aa88e50d2828fb28  (9a98fae + 9889e78 + uncommitted)
PASS  spec01.0 prose.py ran over 22 fixture files
PASS  spec01.1 prose names no example/ file
PASS  spec01.2 scan prints 8 PRDs, boxes 3/5 and 3/3
PASS  spec01.2 band order unchanged
PASS  spec01.3 memos.py check silent
PASS  spec01.3 workflows.py check silent
PASS  spec01.3 questions.py check silent
PASS  spec01.4 13+ example/ files changed and every line is M
PASS  spec01.5 box text unchanged in prds/building/specs/spec01.md
PASS  spec01.5 box text unchanged in prds/finished/specs/spec01.md
PASS  spec01.6 asking/prd.md keeps three answers, one recommended
PASS  spec02.1 prose names no knowledge/ file
PASS  spec02.2 WORKFLOW.md frontmatter byte-identical
PASS  spec02.3 the legacy name is gone
PASS  spec02.4 all four workflow ids present
PASS  spec02.4 the Routing table rows are unchanged
PASS  spec02.5 dataview fences byte-identical in Dashboard.md
PASS  spec02.5 dataview fences byte-identical in conclusions/_index.md
PASS  spec02.5 dataview fences byte-identical in sources/_index.md
PASS  spec02.6 pearde init plants all five knowledge files
PASS  spec02.6 knowledge.py doctor is clean on the planted vault
PASS  spec03.1 the generated index reads dense
PASS  spec03.2 the example fixture equals what render_index() emits
PASS  spec03.3 a board this generator made checks clean
PASS  spec03.4 every content line of the index survives
PASS  spec03.5 prose names no fixture file at all

boxes 26/26

spec02: exit 0
merged tree 99d55648936f8f4e59838c54aa88e50d2828fb28  (9a98fae + 9889e78 + uncommitted)
PASS  spec01.0 prose.py ran over 22 fixture files
PASS  spec01.1 prose names no example/ file
PASS  spec01.2 scan prints 8 PRDs, boxes 3/5 and 3/3
PASS  spec01.2 band order unchanged
PASS  spec01.3 memos.py check silent
PASS  spec01.3 workflows.py check silent
PASS  spec01.3 questions.py check silent
PASS  spec01.4 13+ example/ files changed and every line is M
PASS  spec01.5 box text unchanged in prds/building/specs/spec01.md
PASS  spec01.5 box text unchanged in prds/finished/specs/spec01.md
PASS  spec01.6 asking/prd.md keeps three answers, one recommended
PASS  spec02.1 prose names no knowledge/ file
PASS  spec02.2 WORKFLOW.md frontmatter byte-identical
PASS  spec02.3 the legacy name is gone
PASS  spec02.4 all four workflow ids present
PASS  spec02.4 the Routing table rows are unchanged
PASS  spec02.5 dataview fences byte-identical in Dashboard.md
PASS  spec02.5 dataview fences byte-identical in conclusions/_index.md
PASS  spec02.5 dataview fences byte-identical in sources/_index.md
PASS  spec02.6 pearde init plants all five knowledge files
PASS  spec02.6 knowledge.py doctor is clean on the planted vault
PASS  spec03.1 the generated index reads dense
PASS  spec03.2 the example fixture equals what render_index() emits
PASS  spec03.3 a board this generator made checks clean
PASS  spec03.4 every content line of the index survives
PASS  spec03.5 prose names no fixture file at all

boxes 26/26

spec03: exit 0
merged tree 99d55648936f8f4e59838c54aa88e50d2828fb28  (9a98fae + 9889e78 + uncommitted)
PASS  spec01.0 prose.py ran over 22 fixture files
PASS  spec01.1 prose names no example/ file
PASS  spec01.2 scan prints 8 PRDs, boxes 3/5 and 3/3
PASS  spec01.2 band order unchanged
PASS  spec01.3 memos.py check silent
PASS  spec01.3 workflows.py check silent
PASS  spec01.3 questions.py check silent
PASS  spec01.4 13+ example/ files changed and every line is M
PASS  spec01.5 box text unchanged in prds/building/specs/spec01.md
PASS  spec01.5 box text unchanged in prds/finished/specs/spec01.md
PASS  spec01.6 asking/prd.md keeps three answers, one recommended
PASS  spec02.1 prose names no knowledge/ file
PASS  spec02.2 WORKFLOW.md frontmatter byte-identical
PASS  spec02.3 the legacy name is gone
PASS  spec02.4 all four workflow ids present
PASS  spec02.4 the Routing table rows are unchanged
PASS  spec02.5 dataview fences byte-identical in Dashboard.md
PASS  spec02.5 dataview fences byte-identical in conclusions/_index.md
PASS  spec02.5 dataview fences byte-identical in sources/_index.md
PASS  spec02.6 pearde init plants all five knowledge files
PASS  spec02.6 knowledge.py doctor is clean on the planted vault
PASS  spec03.1 the generated index reads dense
PASS  spec03.2 the example fixture equals what render_index() emits
PASS  spec03.3 a board this generator made checks clean
PASS  spec03.4 every content line of the index survives
PASS  spec03.5 prose names no fixture file at all

boxes 26/26
/Users/feb/dev/infra/pearde/pearde/memos/README.md
