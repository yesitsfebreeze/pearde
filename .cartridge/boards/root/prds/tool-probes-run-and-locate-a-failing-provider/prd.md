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
canonical-scope: tool-probes-run-and-locate-a-failing-provider
---

# A failing contract names its cartridge, and a solo verify isolates it

`run_contracts` in `cartridge.ctg/src/host/run.rs` already reports ``<id> <obligation> `<key>` returned false`` or the error, and `verify_one` runs one cartridge with only the providers its needs resolve to. Neither failure path has a regression test: the only verify test, `verify_sends_every_declared_contract`, covers a passing contract. Outcome: fixtures prove that a failing provider is located from verify output alone. Owner: the host in cartridge.ctg.

## Acceptance

- [ ] In a tempdir profile where `b` needs `a` and `a`'s `selftest` returns `false`, `verify()` runs both contracts and returns exactly one failure line, naming `a selftest`.
- [ ] Changing `a`'s listener to return `true` in the same fixture yields no failures, with the expected assertion unchanged.
- [ ] `verify_one("b")` starts only `b` and its resolved provider, so a third cartridge that would fail to start is not reported; a need that binds to nothing fails with the `binds to nothing` profile error before any contract runs.

## Proof and recovery

Add the fixtures beside `verify_sends_every_declared_contract` in `cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs`, reusing its `cartridge` and `profile` helpers and tempdirs, so no user store, repository or live PTY is reachable. Gates from `/Users/feb/dev/cartridge`: `just test cartridge`, `just check cartridge`; not run for this plan. If a fixture shows wrong attribution, fix `run_contracts`, never the expectation. The unsettled-profile report (`profile did not settle`) is left out: `verify_timeout` comes from the process-wide `settings::host()` and cannot be shortened per test without a separate change.

## Dependencies and review

No hard prerequisite: the former need on `every-enabled-tool-ships-a-contract-probe` only adds coverage lines. Both items edit `host.rs` tests; land them in sequence. [Review history](review.md); 3 of 5 rounds used.
