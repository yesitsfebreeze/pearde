---
state: "open"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/harness.ctg"
work-kind: leaf
canonical-scope: reflex-tool-audit-loop
needs:
- "@mcp/deferred-tool-band"
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

## Decision

2026-09-16, coordinator (analyst-1 report under `.state/loop/reflex-tool-audit-loop/`). Settled from existing records, not a user question:

- Box 3 has nothing to outrank until `@mcp/deferred-tool-band` lands a disposition (`harness.ctg/src/lib.rs` `convert_tools` passes descriptors straight through), so this PRD needs the band.
- Counting (box 1) already exists as `sessions reflex_report` (`sessions.ctg/src/lib.rs`, over `src/observations.rs`). `@sessions/reflex-reports-attributed-tool-outcomes` (done) rules that the session observation boundary owns tool-use attribution. Harness reads it and keeps no second ledger.
- So the draw, verdict and trigger records belong in sessions, next to the observation journal. The next analysis splits into a sessions child (store, draw, rate, disable) and a harness child (applies verdicts over the band's disposition, reports which input decided, injects trigger lines, scripted offline test).
- The band's disposition is a descriptor contract, not an mcp internal: `summary`, `defer` and a `hot` set (canonical statement: the `## Deferred tools` section of `mcp.ctg/.cartridge/docs/README.md`, specified by `@mcp/deferred-tool-band` spec01). The harness child must apply the same rule in `convert_tools`, reading its own `hot` setting, before verdicts can outrank it.
- Gate timings were not measured, because a detached harness worktree cannot build without the sibling `memo.ctg`. The next analysis must measure them with the sibling submodules present.
