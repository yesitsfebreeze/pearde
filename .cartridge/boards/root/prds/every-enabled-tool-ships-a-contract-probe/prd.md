---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: every-enabled-tool-ships-a-contract-probe
---

# `cartridge verify` names every enabled cartridge that declares no contract

The host already runs declared contracts: a manifest's `selftest` and `integration` keys name events the cartridge listens to, and `cartridge verify [cartridge]` (`just verify`) sends each one and names the failing entry. Only harness.ctg and tools.ctg declare `selftest` today, and verify says nothing about enabled cartridges without a contract, so they pass silently. Outcome: verify reports coverage. Owner: the host in cartridge.ctg; adding contracts to individual cartridges is follow-up work in their owner boards.

## Acceptance

- [ ] `verify` on a disposable profile with one covered and one uncovered cartridge names the uncovered entry id as `no contract`, derived from the loaded entries rather than a handwritten list; disabled entries are not listed.
- [ ] Coverage lines are informational: an all-passing profile still exits 0, while a `selftest` returning `false` or erroring still exits non-zero naming `<id> selftest <key>`.
- [ ] A manifest whose `selftest` names an event it does not listen to is still refused at load, before any contract runs (existing test `a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to`).

## Proof and recovery

Start at `cartridge.ctg/src/host/run.rs` (`contracts`, `run_contracts`), `cartridge.ctg/src/cli/host.rs` (`verify`) and `cartridge.ctg/src/loader/document.rs` (`selftest`). Add the fixture beside `verify_sends_every_declared_contract` in `cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs`, reusing its tempdir helpers. Gates from `/Users/feb/dev/cartridge`: `just test cartridge`, `just check cartridge`; not run for this plan. Manifests without contracts keep loading unchanged; making `no contract` fatal is a later opt-in. The former prerequisite on the blocked debug-mode memo is dropped: it cites pre-rename `builtin/memory/.zirkle` paths and gates nothing here. Shares `host.rs` tests with `tool-probes-run-and-locate-a-failing-provider`; land them in sequence.

## Review

[Review history](review.md). 3 of 5 rounds used.
