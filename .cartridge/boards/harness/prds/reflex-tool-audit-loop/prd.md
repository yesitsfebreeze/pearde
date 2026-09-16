---
state: "analyzing"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/harness.ctg"
work-kind: leaf
canonical-scope: reflex-tool-audit-loop
claim: "coordinator-c4-2 2026-09-16T08:15:00.031Z"
---

# The tool surface is audited by use, not by declaration

Every enabled tool costs its schema on every request, and the composition decides which tools are worth that cost from what they declare about themselves. A declaration cannot confirm itself: a tool nobody calls looks the same as one that is essential but rarely needed.

Count every tool call into a per-session ledger, and let the measurement outrank the declaration. Because a tool that is never surfaced can never be called, the audit draws one cold tool per session, surfaces it, and records whether it was useful — so a tool the composition has quietly stopped offering gets a chance to prove itself rather than decaying by default. A recorded verdict of useful carries a trigger line into later sessions saying when the tool applies.

## Acceptance

- [ ] Every tool call is counted into a session ledger naming the tool and the call count, readable after the session.
- [ ] One cold tool is drawn per session, surfaced, and its outcome recorded as a verdict; a session where the drawn tool was not reachable records that instead of a verdict.
- [ ] A recorded verdict and fire count outrank the tool's declared disposition when the surface is composed, and the composed surface reports which input decided each tool.
- [ ] A useful verdict contributes one trigger line naming when the tool applies, present in later sessions' composed context.
- [ ] The audit is disableable, and disabled it records nothing and changes no composed surface.
- [ ] Counting, drawing, verdicts and their effect on composition are tested offline in `just test harness` with a scripted session.

## Proof and recovery

Mechanism from `/Users/feb/dev/pi/packages/coding-agent/src/core/reflex/` (461 lines at survey, verified present), the measured half of upstream's tool-surface economy: it counts calls into a ledger so a rarity flag cannot confirm itself, draws one cold tool per session for rating, and lets verdicts and fire counts override the static policy.

Pairs with `@mcp/deferred-tool-band`, which is the withholding half: this child measures, that one defers. Land the band first or the audit has nothing to correct. Reconcile with `@sessions/reflex-reports-attributed-tool-outcomes`, which already exists on the sessions board and covers attribution of the same observations.

Gates, cwd `/Users/feb/dev/cartridge`: `just test harness`, `just check harness`. Not run for this plan.
