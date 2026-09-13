---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: tool-probes-run-and-locate-a-failing-provider
needs:
- every-enabled-tool-ships-a-contract-probe
---

# Tool probes run and locate a failing provider

Drive the actual exposed capability census, not the old two-tool default. Execute owner-declared probes through a disposable real host with trusted invocation context and fixture roots. Integrate this evidence into the owner-capability and composed-system gates.

## Acceptance

- [ ] Every enabled capability is passed, failed or explicitly unverified with its exact source/recipe revision and expected assertion.
- [ ] A fixture provider deliberately fails, is correctly attributed from its output, then passes after repair without changing the expected result to bless it.
- [ ] State-changing probes cannot reach user stores, repositories or the live PTY; unknown/malformed probe declarations cause no execution.

## Proof and recovery

Start at [settings.md](../../settings.md), [justfile](../../../../../../justfile).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `tool-probes-run-and-locate-a-failing-provider`; maximum five rounds.
