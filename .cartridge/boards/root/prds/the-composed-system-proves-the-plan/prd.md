---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
superseded-by: "@root/the-gates-are-green-at-one-pinned-set-of-shas"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: root
work-kind: milestone
review-round: 3
review-status: failed
canonical-scope: the-composed-system-proves-the-plan
needs:
- '@runtime/the-sandbox'
- '@memo/memo-board-template'
- '@harness/harness-consumes-landscape'
- '@mcp/clients-share-document-execution'
- capabilities-live-with-their-owners
- '@runtime/documents-own-live-processes'
- '@ui/human-context-is-the-same-document'
- '@tools/development-tooling-has-one-home'
- '@landscape/context-quality-is-measured'
- '@landscape/recursive-development-graph'
---

# The composed system passes its release gates at one pinned set of revisions

Milestone: release the composition only when its named integration prerequisites and the root gates pass together. The host now runs on the transport protocol and every cartridge was ported (2026-09-14), so the gates below replace the pre-rewrite "document execution" wording; the old 159-plan source map is history, not acceptance.

## Acceptance

- [ ] From `/Users/feb/dev/cartridge` at one recorded set of submodule SHAs: `just check`, `just test`, `just smoke` and `just verify` exit 0, and `just isolation` reports nothing.
- [ ] Each `needs` item is `done` with current proof, or retired or rehomed by its owner-board review with the reason in Result; unsupported platforms are named as excluded.
- [ ] A wrapper is retired only after its consumer census and parity check pass; its source history and store bytes are retained.

## Proof and recovery

Baseline ([release-status](../../../../../../.cartridge/memos/note/release-status.md)): host lib tests pass, but `just smoke` mcp and proxy fail (`memo inactive`, proxy timeout) and `just test` is red in gitfs (6), harness (1), mcp (1), pty (2), router (2) and sessions (8). These gates have not run for this plan. On a red gate, attribute it to the owner whose pinned SHA changed, reopen that item and keep the last green set of SHAs as the release candidate; nothing is replayed automatically.

## Dependencies and review

`@runtime/the-sandbox` is added, closing the round-1 finding that sandbox prerequisites were missing. Unresolved: `@landscape/context-quality-is-measured` and `@landscape/recursive-development-graph` sit on the dissolved landscape board (no landscape.ctg; fabric work is owned by memo, `memo.ctg/src/fabric_graph.rs` and `memo.ctg/evidence`, gate `just test memo`); `@tools/development-tooling-has-one-home` is marked superseded by its own review; `@runtime/documents-own-live-processes` still describes pre-rewrite lifetimes. The owning boards must rehome or retire these before this gate can pass. [Review history](review.md); 3 of 5 rounds used.
