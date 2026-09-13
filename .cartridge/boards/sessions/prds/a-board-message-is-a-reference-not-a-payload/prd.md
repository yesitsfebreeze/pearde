---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: sessions
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: a-board-message-is-a-reference-not-a-payload
needs:
- '@sessions/the-agents-chat-through-one-tool'
---

# a-board-message-is-a-reference-not-a-payload

Define board posts with explicit bounded claim text and a typed references array: memo source/revision, session/run identity, channel/sequence or owner-qualified path/range. A byte cap enforces size only; prose discipline is guidance, not an asserted semantic guarantee. Resolution uses existing scoped read APIs.

## Acceptance

- [ ] A second authorized session follows every supported reference form and gets exact identity/revision or a named stale/missing result.
- [ ] Oversized text/reference lists and malformed forms are rejected before append; a short inline payload is not falsely claimed detectable by length alone.
- [ ] Cross-scope references disclose no unauthorized content and reports measure actual posted/reference bytes without claiming an unmeasured scaling law.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-board-message-is-a-reference-not-a-payload`; maximum five rounds.
