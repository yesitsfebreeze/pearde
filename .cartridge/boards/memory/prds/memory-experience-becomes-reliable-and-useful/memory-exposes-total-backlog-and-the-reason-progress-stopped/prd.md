---
state: "claimed"
origin: requested
priority: 99
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
footprint:
  - "src/store/core/src/lib.rs"
  - "src/store/core/src/experience.rs"
  - "src/rpc/Cargo.toml"
  - "src/rpc/src/server.rs"
  - "src/rpc/src/experience/mod.rs"
  - "src/rpc/src/experience/drain.rs"
  - "src/rpc/src/crystallization_cycles.rs"
  - "src/commands/src/memory.rs"
  - "src/cartridge/src/status.rs"
  - "src/cartridge/src/asp/mod.rs"
  - "src/rpc/src/experience/view.rs"
  - "src/cartridge/build.rs"
  - "src/cartridge/build_identity.rs"
  - "src/cartridge/Cargo.toml"
  - "Cargo.lock"
  - "cartridge.json"
  - ".cartridge/tests/unit/src/store/core/src/experience_test.rs"
  - ".cartridge/tests/unit/src/rpc/src/experience_test.rs"
  - ".cartridge/tests/unit/src/cartridge/status_test.rs"
  - ".cartridge/tests/unit/src/cartridge/build_identity_test.rs"
  - ".cartridge/tests/unit/src/commands/src/memory_test.rs"
  - ".cartridge/tests/integration/asp.rs"
  - "README.md"
  - ".cartridge/help.md"
claim: "memory-status-implementer 2026-09-19T18:55:33.590Z"
---

# Memory exposes total backlog and the reason progress stopped

Expose cheap, authoritative intake and migration progress through memory status and ASP. Separate serving retrieval, accepting input and advancing crystallization. Include live generation/build identity so inspected source cannot be confused with the loaded implementation.

## Evidence

A historical row is returned by experience_pending while experience_stats reports zero pending. Live stale-commit failures appear in process-local cycles, separately from readiness. A successful semantic query does not establish writer progress. See [investigation](../investigation.md).

## Acceptance

- [ ] An otherwise empty inbox with historical rows reports a nonzero total backlog, with live and historical counts separately.
- [ ] Last successful commit, oldest pending age, retry state and last error identify a stale writer even while queries work.
- [ ] Counters and totals reconcile after commit, failure and restart; process-local cycle history is labelled with its retention and generation.
- [ ] Repeated status reads do not scan full payload history, call models, heat knowledge or generate recursive activity.

## Proof and recovery

Promote historical_work_is_absent_from_pending_statistics; add transaction/restart and stale-worker status tests. Run cargo test --locked -p store_core experience --lib, cargo test --locked -p rpc experience --lib and cargo test --locked -p memory_cartridge status --lib from memory.ctg. Measure polling cost at 1,000 and 100,000 fixture rows.

Maintain counters transactionally and initialize migration totals once. Explicit unavailable is preferable to a fabricated zero. No Scope-specific policy enters memory. Scope M.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
