---
state: open
origin: requested
priority: 99
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
footprint:
  - "src/rpc/src/experience/mod.rs"
  - "src/rpc/src/experience/input.rs"
  - "src/store/core/src/experience.rs"
  - "src/cartridge/src/lib.rs"
  - "cartridge.json"
  - ".cartridge/tests/unit/src/rpc/src/experience_test.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Memory classifies activity acceptance and refusal

Publish a declared activity-delivery response contract that lets generic callers distinguish durable acceptance, duplicate acceptance, temporary refusal and permanent rejection. Memory owns classification; the host consumes the contract without parsing memory-specific error strings.

## Evidence

The current append endpoint returns queued/duplicate values or plain string errors. The host discards response bodies and retries all errors. The independent runtime-plan review identified the missing producer ownership. See [investigation](../investigation.md).

## Acceptance

- [ ] A negotiated contract returns stable dispositions for accepted, duplicate, retryable and rejected inputs, plus a bounded reason code; acceptance means committed durable intake.
- [ ] Oversized or expired inputs receive permanent rejection, while capacity exhaustion and temporary storage unavailability remain retryable; neither refusal creates an acceptance receipt.
- [ ] Old callers retain the existing behavior until migrated; unsupported versions and unknown responses cannot be mistaken for acknowledgement or silently discarded.
- [ ] Offline public append tests cover each disposition, duplicate retries and restart. The host's follow-up contract test can consume these responses without memory imports.

## Proof and recovery

First add table-driven experience_delivery_contract tests in the RPC experience suite, including storage fault injection and declared schema validation. From memory.ctg run `cargo test --locked -p rpc experience --lib` and `cargo test --locked -p memory_cartridge --lib`.

Deploy additive opt-in support first, then migrate host and configured trace senders using the runtime leaf. Keep old handling until every caller is migrated; remove it in the coordinated integration change, with rollback supported by the prior caller/endpoint pair. Inventory proxy and native senders during specification. No transport failure becomes success. Scope S; no graph matching or batch scheduling changes.

## Dependencies and review

This leaf supplies the hard prerequisite for @runtime/rejected-activity-cannot-wedge-the-hosts-delivery-queue. It is split from that plan after its failed first review, so it inherits one used round and enters review round 2. [Review](review.md) must score at least 90 without blockers. Update README/help and run composition audit/isolation before collection. Implementation remains open and unclaimed.
