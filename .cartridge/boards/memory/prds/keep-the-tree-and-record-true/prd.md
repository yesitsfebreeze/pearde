---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: keep-the-tree-and-record-true
needs:
- '@memory/memory-002'
- '@memory/memory-004'
- '@memory/the-graph-converges'
---

# What memory reports about its store stays true

This is a finite parent for three memory outcomes: status counts use one vocabulary, ranking on a spilled store is measured and decided, and repeated ingest converges to stable counts. It replaces the historical standing maintenance terminal, which was never meant to finish and which the small-PRD rule retired. Later hygiene findings get their own leaves.

## Acceptance

- [ ] Each linked leaf is done, with its own evidence, at one memory.ctg revision.
- [ ] Integration gate: at that revision, run `just all` from /Users/feb/dev/cartridge/memory.ctg. On the graph-converges fixture store, `memory health` and the `health` RPC must report equal counts under the terms memory-002 defines, and `memory check --json` must report no `dangling_reasons`.
- [ ] If a leaf or the gate fails, record it here and leave the parent open.

## Work items

- [CLI and RPC name the same memory counts](../memory-002/prd.md)
- [Decide how ranking treats cold rows on a spilled store](../memory-004/prd.md)
- [Repeating a multi-document ingest converges to stable counts](../the-graph-converges/prd.md)

## Review

[Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--keep-the-tree-and-record-true.md` (status open). The PRD state above is authoritative.

> the standing terminal for maintenance — every open memo that fixes a lie, a gate gap, a leftover lane or a rotten memo hangs here, so the plan counts it toward the vision without inventing a product it advances

The vision names a product; the tree and the record decay under it, and the
work that stops the decay — [[hygiene]], [[quality]], [[legible]] and
[[@prd/routine/plan-cartridge-work.md]] findings — advances no single terminal. Off the axis it is
drawn grey and never dispatched first; on a product terminal it lies about
what that terminal needs. So it hangs here, a terminal of [the-vision](../../../root/prds/the-vision/prd.md) that
is never done and whose Check is the gates ([[@prd/routine/plan-cartridge-work.md]] step 4).

### Do

`subwork:` [a-baked-manifest-dir-names-a-lane-that-may-be-gone](../a-baked-manifest-dir-names-a-lane-that-may-be-gone/prd.md), [a-killed-daemon-pays-a-full-index-rebuild](../a-killed-daemon-pays-a-full-index-rebuild/prd.md), [a-root-search-cannot-see-the-record](../a-root-search-cannot-see-the-record/prd.md), [an-assessments-memos-are-left-uncommitted](../an-assessments-memos-are-left-uncommitted/prd.md), [claude-md-links-resolve-nowhere](../claude-md-links-resolve-nowhere/prd.md), [compact-writes-a-twin-instead-of-replacing-its-source](../compact-writes-a-twin-instead-of-replacing-its-source/prd.md), [finish-the-store-the-doctor-found](../finish-the-store-the-doctor-found/prd.md), [four-production-sites-mint-an-edge-nothing-can-find](../four-production-sites-mint-an-edge-nothing-can-find/prd.md), [just-list-describes-half-its-recipes-with-a-sentence-fragment](../just-list-describes-half-its-recipes-with-a-sentence-fragment/prd.md), [memory-mcp-never-answers-initialize](../memory-mcp-never-answers-initialize/prd.md), [landed-lanes-are-never-closed](../landed-lanes-are-never-closed/prd.md), [lane-gates-run-a-stale-cached-test-binary](../lane-gates-run-a-stale-cached-test-binary/prd.md), [mine-backed-intake-compaction](../mine-backed-intake-compaction/prd.md), [part-list-answers-the-whole-record-uncapped](../part-list-answers-the-whole-record-uncapped/prd.md), [the-build-cache-is-off-while-its-store-sits-over-limit](../the-build-cache-is-off-while-its-store-sits-over-limit/prd.md), [the-citation-gate-reads-code-and-not-the-record](../the-citation-gate-reads-code-and-not-the-record/prd.md), [the-commands-admin-split](../the-commands-admin-split/prd.md), [the-de-link-leaves-no-mark-a-reader-can-act-on](../the-de-link-leaves-no-mark-a-reader-can-act-on/prd.md), [the-e2e-harness-writes-the-real-machine-registry](../the-e2e-harness-writes-the-real-machine-registry/prd.md), [the-graviton-tests-stayed-in-the-accept-test-file](../the-graviton-tests-stayed-in-the-accept-test-file/prd.md), [the-intake-status-scan-cannot-see-the-direct-queue](../the-intake-status-scan-cannot-see-the-direct-queue/prd.md), [the-json-span-turns-a-transient-failure-into-a-permanent-one](../the-json-span-turns-a-transient-failure-into-a-permanent-one/prd.md), [the-machine-wide-embed-lane-has-a-candidate-object](../the-machine-wide-embed-lane-has-a-candidate-object/prd.md), [the-number-that-names-the-stall-is-computed-and-unread](../the-number-that-names-the-stall-is-computed-and-unread/prd.md), [the-root-memory-needs-one-authority](../the-root-memory-needs-one-authority/prd.md), [the-store-readme-describes-store-core](../the-store-readme-describes-store-core/prd.md), [the-vector-decoder-passes-the-current-lint](../the-vector-decoder-passes-the-current-lint/prd.md), [the-verdicts-bundles-are-nine-claims-not-four](../the-verdicts-bundles-are-nine-claims-not-four/prd.md), [the-warm-lsp-times-out](../the-warm-lsp-times-out/prd.md), [the-extension-catalogue-row-has-no-member](../the-extension-catalogue-row-has-no-member/prd.md), [the-plan-crate-cites-an-untracked-file](../the-plan-crate-cites-an-untracked-file/prd.md), [the-exit-flag-tests-race-each-other](../the-exit-flag-tests-race-each-other/prd.md), [the-admin-split-left-rotted-citations](../the-admin-split-left-rotted-citations/prd.md), [twenty-bare-name-anchors-point-into-a-dead-commands-admin](../twenty-bare-name-anchors-point-into-a-dead-commands-admin/prd.md), [the-lsp-answer-asks-a-positive-control](../the-lsp-answer-asks-a-positive-control/prd.md), [an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one](../../../runtime/prds/an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one/prd.md), [lane-rm-cannot-address-an-agent-worktree](../lane-rm-cannot-address-an-agent-worktree/prd.md), [the-alias-lock-test-races-its-own-global](../the-alias-lock-test-races-its-own-global/prd.md), [a-lane-daemon-pays-twelve-minutes-to-open-its-eyes](../a-lane-daemon-pays-twelve-minutes-to-open-its-eyes/prd.md), [the-installed-binary-answers-for-a-memory-that-is-gone](../the-installed-binary-answers-for-a-memory-that-is-gone/prd.md), [a-lanes-build-can-hand-back-a-siblings-binary](../../../runtime/prds/a-lanes-build-can-hand-back-a-siblings-binary/prd.md), [memory-health-loads-its-own-graph-beside-the-daemon](../memory-health-loads-its-own-graph-beside-the-daemon/prd.md)

The list is the open maintenance memos, appended by [[@prd/routine/plan-cartridge-work.md]] and the
attach step of [[@prd/routine/run-board.md]] as they are written.

### Check

Every child `status: done`, and `just all` green on the trunk.
