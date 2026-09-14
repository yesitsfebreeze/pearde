---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: root
work-kind: rollup
review-round: 3
review-status: failed
canonical-scope: cartridge-improvement-programme
needs:
- '@gitfs/tool-results-interoperate'
- '@memo/improve-memo-programme'
- '@memory/improve-memory-programme'
- '@memory/improve-memory-tool-programme'
- '@gitfs/improve-gitfs-programme'
- '@pty/improve-pty-programme'
- '@mcp/improve-mcp-programme'
- '@policy/improve-policy-programme'
- '@sessions/improve-sessions-programme'
- '@harness/improve-harness-programme'
- '@router/improve-router-programme'
- '@proxy/improve-proxy-programme'
- '@agent/improve-agent-programme'
- '@fs/improve-fs-programme'
- '@runtime/improve-tools-programme'
- '@ui/improve-ui-programme'
---

# Cartridge improvement programme

Roll-up only: index the per-owner improvement programmes and record their combined evidence. Claim a leaf in its owner board; this parent adds no implementation.

## Acceptance

- [ ] Every linked child is `done` with its own recorded evidence, or retired by its owner-board review with the reason copied into Result.
- [ ] After the last child lands, `just check` and `just test` exit 0 from `/Users/feb/dev/cartridge` at one recorded set of submodule revisions, and Result lists tested mitigations and remaining limitations per owner.
- [ ] No child leaves `needs` without its owner-board disposition.

## Work items

- [Every currently exposed tool completes through its real consumers](../../../gitfs/prds/tool-results-interoperate/prd.md)
- [Memo improvement plan](../../../memo/prds/improve-memo-programme/prd.md)
- [Memory improvement plan](../../../memory/prds/improve-memory-programme/prd.md)
- [Memory tool adapter improvement plan](../../../memory/prds/improve-memory-tool-programme/prd.md)
- [GitFS and ship improvement plan](../../../gitfs/prds/improve-gitfs-programme/prd.md)
- [PTY and shared shell improvement plan](../../../pty/prds/improve-pty-programme/prd.md)
- [MCP bridge improvement plan](../../../mcp/prds/improve-mcp-programme/prd.md)
- [Policy improvement plan](../../../policy/prds/improve-policy-programme/prd.md)
- [Sessions improvement plan](../../../sessions/prds/improve-sessions-programme/prd.md)
- [Harness improvement plan](../../../harness/prds/improve-harness-programme/prd.md)
- [Router improvement plan](../../../router/prds/improve-router-programme/prd.md)
- [Proxy improvement plan](../../../proxy/prds/improve-proxy-programme/prd.md)
- [Agent loop improvement plan](../../../agent/prds/improve-agent-programme/prd.md)
- [Filesystem tools improvement plan](../../../fs/prds/improve-fs-programme/prd.md)
- [Workspace tools improvement plan](../../../runtime/prds/improve-tools-programme/prd.md)
- [Terminal UI improvement plan](../../../ui/prds/improve-ui-programme/prd.md)

## Reconciliation and recovery

The host now runs on the transport protocol and every cartridge was ported (2026-09-14). Children written before that must be reconciled in their owner boards before this parent can close:

- `@memory/improve-memory-tool-programme`: the memory-tool submodule was dropped; memory.ctg serves `tool.memory` itself ([help](../../../../../../memory.ctg/.cartridge/help.md)).
- `@runtime/improve-tools-programme`: "workspace tools" targets the dropped workspace; tools.ctg has its own `tools` board.
- `@policy/improve-policy-programme`: under [a-cartridge-brings-its-own-surface](../../../../../../.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md) the policy keeps no per-tool catalog; per-tool rules belong to `config.lua`.
- `@ui/improve-ui-programme`: the board name is historical; it already targets tui.ctg.

Six children are already `done`. Baseline ([release-status](../../../../../../.cartridge/memos/note/release-status.md)): `just test` is red in gitfs, harness, mcp, pty, router and sessions. These gates have not run for this plan. On an integration failure reopen the child whose pinned revision changed and keep the previous pinned revisions.

## Review

[Review history](review.md). Inherits round 1 from `cartridge-improvement-programme`; 3 of 5 used.
