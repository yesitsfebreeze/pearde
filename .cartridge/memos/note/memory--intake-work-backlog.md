---
kind: documentation
description: Navigation snapshot of unfinished intake work, separating recorded statuses, design questions, and older prose backlogs
read_when: picking the next drive item beyond the completed working-with-memory plan
---

# Intake work backlog

Snapshot: 2026-09-07. Intake is a location, not a kind. The first drive
scan looked only in `memos/work/` and missed the intake work already exposed
by [[memo-index]]. This index restores that route; it does not create duplicate
work items, change their statuses, or assert that an old defect still exists.

Recounted 2026-09-09, the record holds 205 `kind: work` memos, 16 of them
still in `intake/`, every one `status: open`. These are frontmatter counts,
not 16 independent implementation tasks: parents include children, and some
open items need verification rather than new code.
The generated `memos/work/index.json` remains the exhaustive kind-to-source
lookup, including completed items. Do not hand-edit generated indexes.

## Recorded open work in intake

### Lifecycle and diagnostics

- [[@prd/work/memory--reaping-a-node-whose-root-vanished-forgets-it-rather-than-stopping-it.md]] — gracefully stop the owned node before dropping its handle.
- [[@prd/work/memory--the-e2e-harness-writes-the-real-machine-registry.md]] — isolate test registry writes.
- [[@prd/work/memory--the-machine-wide-embed-lane-has-a-candidate-object.md]] — bound hub search invokes; this does not promise machine-wide serialization of every embed caller.
- [[@prd/work/memory--the-number-that-names-the-stall-is-computed-and-unread.md]] — expose in-flight crossings; also referenced by [[@prd/work/memory--memory-integration-fast-readiness.md]], not a second implementation task.
- [[@prd/work/memory--the-reflex-ledger-discards-every-write-error.md]] — surface failed ledger persistence.
- [[@prd/work/memory--the-root-pin-is-logged-before-it-is-attempted.md]] — **done since this snapshot**: landed `f4f901e1`; full gate passed 1,388 tests plus doctests. Do not select again.

### Ingest, record access, and provenance

- [[@prd/work/memory--the-json-span-turns-a-transient-failure-into-a-permanent-one.md]] — parse a complete claims array despite surrounding brackets and prose.
- [[@prd/work/memory--part-list-answers-the-whole-record-uncapped.md]] — bound the record-list response.
- [[@prd/work/memory--part-write-indexes-a-new-part.md]] — stale open design: [[the-index-is-derived]] supersedes its manual append mechanism. Reconcile the memo before executing it; do not reintroduce index-row writes.
- [[@prd/work/memory--a-routine-call-walks-the-whole-record-to-find-one-file.md]] — narrow routine resolution.
- [[@prd/work/memory--setup-sorts-every-access-count-to-render-a-greeting.md]] — avoid the full health calculation for setup.
- [[@prd/work/memory--the-de-link-leaves-no-mark-a-reader-can-act-on.md]] — retain an actionable trace when a link is removed.
- [[@prd/work/memory--the-citation-gate-reads-code-and-not-the-record.md]] — check the record's code citations.

### Build, tests, and documentation

- [[@prd/work/memory--the-vector-decoder-passes-the-current-lint.md]] — satisfy the installed compiler's decoder lint.
- [[@prd/work/memory--the-scale-tier-has-a-runner.md]] — give the ignored measurement tier an explicit runner.
- [[@prd/work/memory--the-graviton-tests-stayed-in-the-accept-test-file.md]] — place graviton tests with their subject.
- [[@prd/work/memory--the-store-readme-describes-store-core.md]] — correct the store crate's documentation boundary.

### Command-admin split

[[@prd/work/memory--the-commands-admin-split.md]] is the parent, not a ninth independent change.
Its eight open children are listed below. The parent's prose says health moves
last while its list places health first; reconcile the ordering before dispatch.
The requested re-export shim also conflicts with [[code-laws]]; resolve that
scope conflict rather than implementing the old split literally:


- [[@prd/work/memory--split-admin-claim-kind.md]]
- [[@prd/work/memory--split-admin-compact.md]]
- [[@prd/work/memory--split-admin-compress.md]]
- [[@prd/work/memory--split-admin-focus.md]]
- [[@prd/work/memory--split-admin-gc.md]]
- [[@prd/work/memory--split-admin-health.md]]
- [[@prd/work/memory--split-admin-hub-register.md]]
- [[@prd/work/memory--split-admin-unnamed.md]]

Read each block and its question before treating it as a missing implementation.
[[the-eight-unread-work-checks]] and [[landed-work-still-says-open]] explain
why a commit title or a status alone cannot establish completion.

## Questions and approval boundaries

The 13 intake question memos are not 13 unmade decisions: nine remain
unresolved, three have recorded resolutions, and one needs reconciliation
with implementation reported in another lane. Recommendations are not answers.

### Nine unresolved question memos

- [[approve-self-improve-inventory-scope]] — explicit approval for a proposed instruction change; [[@prd/work/memory--self-improve-inventory-includes-ignored-entrypoints.md]] remains blocked.
- [[does-a-removal-need-a-tombstone]] — persisted removals versus a single-writer boundary.
- [[does-the-record-keep-line-anchors]] — five unanswered blocks; reconcile the answered `path#symbol` direction with [[@prd/work/memory--the-citation-gate-reads-code-and-not-the-record.md]] before executing its older range-check design.
- [[is-the-machine-inventory-a-surface]] — four open surface/policy questions; the existing CLI inventory is already acknowledged.
- [[memory-run-named-by-the-decision-not-by-the-binary]] — planned verb versus shipped surface; check current launch work before implementing another verb.
- [[should-the-reasoner-be-seeded-by-default]] — default policy is distinct from the completed sampling wiring in [[@prd/work/memory--the-reasoner-is-seeded.md]].
- [[the-vision-names-env-vars-the-proxy-never-honoured]] — establish the contract/history rather than revive variables from prose.
- [[what-should-the-hygiene-gate-default-to]] — default and false-refusal policy, not permission to enable a proposed mode.
- [[which-side-of-the-unload-resolve-seam-moves]] — residency/index boundary, also tracked by [[@prd/note/memory--open-work.md]].

### Resolved or reconciliation-only question memos

- [[recall-floor-canary-set]] — the recorded user answer supersedes the old canary fork.
- [[where-does-a-declaration-carry-its-payload]] — all answers settled by [[a-declaration-carries-its-payload-in-a-toml-block]].
- [[how-does-a-part-quote-a-wikilink]] — stale unanswered blocks: the quote convention is settled by [[a-body-citation-is-backticked]] and [[a-code-citation-is-backticked]], with [[@prd/work/memory--the-gate-reads-body-links.md]] and [[@prd/work/memory--the-record-citation-breaks-rustdoc.md]] done.
- [[memory-provider-recovery]] — reconcile its unanswered authority question with [[memory-native-model-service]], which reports bounded recovery implemented in an unlanded lane. Do not build that service again or infer permission for broader autonomous repair.

## Other routes, not duplicate work queues

[[working-with-memory]] is the older dashboard plan, not the whole current
backlog. [[@prd/note/memory--open-work.md]] carries ranked and unranked prose findings;
[[@prd/insight/memory--the-record-plans-work-in-two-places.md]] documents the split between that list
and atomic work memos. Its ordering is historical evidence, not a fresh
validation of every defect. [[the-unranked-half-was-never-read]] records why
copying finding titles without reading their closing notes recreates dead work.

[[@prd/work/memory--memory-integration-assessment.md]] is another existing work root; indexing
intake does not silently choose it or authorize its approval-gated parts.

## How drive consumes this index

1. Resolve the source through the generated kind index, even when its path is
   in intake. Read its full `Do`, `Check`, dependencies, and closing notes.
2. Distinguish new implementation, unrun verification, answered-but-stale
   blockers, and human approval. Do not change a work status on this census.
3. For execution, revalidate the selected item against the current tree,
   use its own lane, and run its literal Check through [[@prd/routine/run-board.md]]. For a design
   gap, use [[drill]] first; do not infer the user's answer.
4. Regenerate the canonical indexes with `just memos-check` after memo edits.
   This navigation snapshot is not a replacement for those generated indexes.
