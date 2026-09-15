---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: proxy
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-proxy-continuation-recovery
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/continuation.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/continuations.md
commit: "9ddcc08807a059579c21227ad9d3523d242ddf86"
---

# Make continuation lifetime and restart recovery explicit

Clients can distinguish valid, expired and lost-on-restart continuation IDs and recover with full conversation input.

## Acceptance

- [x] Create a continuation, evict it and restart the fixture proxy: each path returns the documented outcome with no cross-client mapping.
- [x] Full-input recovery succeeds; any optional durable mode has restart, retention and wrong-profile tests, otherwise the limitation is explicitly retained.

- [x] Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Proof and recovery

Start at owner-local `src/service.rs`, `src/streaming.rs` and `src/wire.rs`. See [bounded specification](specs/spec01.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-proxy-continuation-recovery`; maximum five rounds.

Reverify unchanged acceptance after the next integrated owner feature; earlier
0c9d4e9b receipt retained. No contract relaxation.

Reverification: recall integration at9ddcc088 changes shared proxy paths. Bind newly imported context/wire modules and dependency declarations without changing behavior acceptance or executable gates.

## From the retired work memo

Folded 2026-09-15 from `work/improve-proxy-continuation-recovery.md` (status open). The PRD state above is authoritative.

### Outcome

Clients can distinguish valid, expired and lost-on-restart continuation IDs and recover with full conversation input.

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
- [ ] Create a continuation, evict it and restart the fixture proxy: each path returns the documented outcome with no cross-client mapping.
- [ ] Full-input recovery succeeds; any optional durable mode has restart, retention and wrong-profile tests, otherwise the limitation is explicitly retained.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Document the existing bounded mapping first and expose expiry/restart semantics. Measure need before adding persistence; if durable mode is justified, bind mappings to profile/provider identity, encrypt sensitive contents where needed and define retention without storing credentials.
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

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
