---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: root
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: capabilities-live-with-their-owners
needs:
- '@memo/memo-write-document'
- '@fs/direct-fs-document'
- '@gitfs/gitfs-document'
- '@pty/pty-document'
- '@sessions/sessions-document'
- '@router/router-document'
---

# Each capability ships its own executable documentation

Roll-up only. Under [a-cartridge-brings-its-own-surface](../../../../../../.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md) (2026-09-14) every cartridge already ships `.cartridge/help.md` and `cartridge help` builds the manual from what is present. What remains is that each capability's executable contract memo lives with its owner and is reached only through a declared need or event. The six owner leaves below carry that work; this parent adds no implementation.

## Acceptance

- [ ] Each linked leaf is `done`, with a passed review of its current revision and its own gate evidence.
- [ ] At one recorded set of submodule revisions, from `/Users/feb/dev/cartridge`: `just check` and `just test` exit 0, and `just isolation` reports no undeclared cross-cartridge reference.
- [ ] A leaf that is retired, superseded or exhausts its five rounds keeps this parent open with the gap named in Result; it is never dropped silently.

## Work items

- [A document invokes validated memo writes](../../../memo/prds/memo-write-document/prd.md)
- [A document preserves guarded direct file edits](../../../fs/prds/direct-fs-document/prd.md)
- [A document preserves session overlay semantics](../../../gitfs/prds/gitfs-document/prd.md)
- [A shell document uses the owned persistent terminal](../../../pty/prds/pty-document/prd.md)
- [A document reads bounded session history](../../../sessions/prds/sessions-document/prd.md)
- [A document explains routing without exposing secrets](../../../router/prds/router-document/prd.md)

## Integration and recovery

Run the three commands above after the last leaf lands and record each owner's submodule SHA beside the exit status. These gates have not run for this plan. Baseline ([release-status](../../../../../../.cartridge/memos/note/release-status.md)): `just test` is currently red in gitfs, harness, mcp, pty, router and sessions, so the gate cannot pass before those owners are green. Leaves land independently; on an integration failure reopen the leaf whose pinned revision changed and keep the previous pinned revisions as the usable composition. Several leaves still name pre-rewrite starting files (for example pty-document links `tool.rs` and `input.rs`) and must be rebased in their owner boards before they are claimed.

## Review

[Review history](review.md). Rounds inherited from `capabilities-live-with-their-owners` and `the-tool-surface-is-search-and-shell`; 3 of 5 used.
