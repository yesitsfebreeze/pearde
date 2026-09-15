---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: proxy
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-proxy-total-usage
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/usage.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/usage.md
commit: "9ddcc08807a059579c21227ad9d3523d242ddf86"
needs:
- "@gitfs/tool-results-interoperate"
- "@root/improve-tool-result-contract"
---

# Account for every internal model round consistently

JSON and streaming responses provide consistent total usage across internal tool rounds, with final-round usage separately identified.

## Acceptance

- [x] A three-round fixture reports matching cumulative totals for JSON and SSE and no double counting of final events.
- [x] Missing usage, partial stream failure and cancellation preserve known totals and label incomplete accounting.

- [x] Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Proof and recovery

Source: `proxy.ctg/src/service.rs`, `src/streaming.rs`, `src/wire.rs` and `src/usage.rs`.

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. The public proxy tests/check and GitFS/policy consumer gates now pass; see verification.json.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Review history](review.md): round 3 passed at 96/100; acceptance evidence is separate from the plan score.

Reverify unchanged usage accounting at0c9d4e9 after scoped continuation changes;
prior480a093f receipt retained. Router integration is0a216cb.

Reverify unchanged acceptance after the next integrated owner feature; earlier
0c9d4e9b receipt retained. No contract relaxation.

Reverification: recall integration at9ddcc088 changes shared proxy paths. Bind newly imported context/wire modules and dependency declarations without changing behavior acceptance or executable gates.

## From the retired work memo

Folded 2026-09-15 from `work/improve-proxy-total-usage.md` (status open). The PRD state above is authoritative.

### Outcome

JSON and streaming responses provide consistent total usage across internal tool rounds, with final-round usage separately identified.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

### Footprint

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

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] A three-round fixture reports matching cumulative totals for JSON and SSE and no double counting of final events.
- [ ] Missing usage, partial stream failure and cancellation preserve known totals and label incomplete accounting.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Normalize provider-supplied usage, distinguish unavailable fields from zero, and account for failed/cancelled attempts when known. Preserve wire compatibility through documented metadata rather than changing standard meanings silently.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test proxy
just check proxy
just smoke proxy
```


### Compatibility and recovery

Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-tool-result-contract](../../../root/prds/improve-tool-result-contract/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
