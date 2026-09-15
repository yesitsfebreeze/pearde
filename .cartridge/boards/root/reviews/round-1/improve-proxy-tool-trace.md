---
kind: work
description: "Inspect internal proxy tool work by request identity"
status: open
priority: P1
size: M
needs:
  - "[improve-tool-result-contract](../../prds/improve-tool-result-contract/prd.md)"
  - "[improve-policy-explain](../../../policy/prds/improve-policy-explain/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["inspect internal proxy tool work by request identity", "implementing proxy cartridge improvements"]
---

# Inspect internal proxy tool work by request identity

## Outcome

An optional bounded trace identifies internal rounds, tools, policy decisions, timings and outcomes while caller-owned history stays in the client.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

## Footprint

Proxy; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `proxy.ctg/service.rs`
- `proxy.ctg/streaming.rs`
- `proxy.ctg/wire.rs`
- `proxy.ctg/tests.rs`
- `proxy.ctg/README.md`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] A mixed internal/caller tool batch has one trace per executed internal call with correct policy/outcome identity.
- [ ] Another client cannot read the trace; retention expiry is explicit and secret values do not appear in default traces.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Correlate with session/run/call and descriptor revisions. Redact sensitive payloads by default, define retention and require the same authorized request scope for trace access; do not expose internal tool calls as caller tool calls.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test proxy
just check proxy
just smoke proxy
```


## Compatibility and recovery

Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-tool-result-contract](../../prds/improve-tool-result-contract/prd.md), [improve-policy-explain](../../../policy/prds/improve-policy-explain/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
