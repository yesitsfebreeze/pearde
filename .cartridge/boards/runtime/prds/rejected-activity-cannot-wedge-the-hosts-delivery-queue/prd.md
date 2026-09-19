---
state: open
origin: requested
priority: 99
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
needs:
  - "@memory/memory-experience-becomes-reliable-and-useful/memory-classifies-activity-acceptance-and-refusal"
footprint:
  - "src/trace/activity.rs"
  - "src/host/trace.rs"
  - "src/transport/cartridge.rs"
  - ".cartridge/tests/unit/src/trace/activity.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Rejected activity cannot wedge the hosts delivery queue

Define a bounded generic activity delivery contract that distinguishes accepted, retryable and permanent rejection. Keep schema normalization, semantics and storage in memory. Preserve visible loss accounting without retaining a second host ledger.

## Evidence

The host retries every delivery error forever before dequeuing the next item. Its queue holds 1,024 entries and reports dropped_before on a later record. Memory rejects oversized and expired input, and currently discards dropped_before during normalization. The permanent-error stall is a source finding, not yet a live loss measurement. See [investigation](../../../memory/prds/memory-experience-becomes-reliable-and-useful/investigation.md).

## Acceptance

- [ ] An oversized or expired record followed by a valid one receives a visible permanent refusal; the valid record proceeds.
- [ ] Temporary unavailability retries with stable identity, bounded backoff and cancellation; acknowledged records are not duplicated.
- [ ] Queue saturation and shutdown expose accepted, pending, rejected and dropped counts; no silent data-loss claim is made.
- [ ] Producer/consumer contract tests run against a disposable memory endpoint and preserve redaction without exporting secrets.

## Proof and recovery

Add a deterministic permanently-reject-first fixture to the existing delivery tests. Run cargo test --locked trace::activity --lib from cartridge.ctg, then the declared host integration test with a disposable bank. Add the real-endpoint contract fixture to the declared launch integration target and run `cargo test --locked --test launch activity_delivery_contract` (new test required). Consume the memory-owned negotiated contract; never parse error strings. Deploy opt-in endpoint support first, then migrate host and all configured trace senders, then remove superseded handling. Unknown or old responses remain explicitly unsupported/retryable, never silently acknowledged.

No runtime code imports memory crates. A rejection must not be treated as successful recording. Roll back negotiated response handling compatibly; never unblock by bypassing trust. Scope M.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
