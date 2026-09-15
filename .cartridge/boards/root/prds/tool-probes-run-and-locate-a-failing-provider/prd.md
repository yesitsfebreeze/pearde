---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: tool-probes-run-and-locate-a-failing-provider
needs:
- "@root/every-enabled-tool-ships-a-contract-probe"
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

## From the retired work memo

Folded 2026-09-15 from `work/tool-probes-run-and-locate-a-failing-provider.md` (status open, estimate 2d). The PRD state above is authoritative.

> Contract probes run against disposable fixtures, and an injected failure is traced to its provider and failing check

### Outcome

Discovered probes actually execute, and their results are strong enough to
diagnose with.

The end-to-end fixture exercises the two tools the default profile enables:
`tool.shell` command submission, interactive input and screen readback, and
`tool.memo` resolve, read and write against a temporary record. Every
state-changing probe runs against a disposable fixture, never the user's record
or the user's shell session. A probe passes only on observed behaviour — the
command's output, the memo read back — never on a successful dispatch.

Then the loop closes: with a service or tool deliberately made to fail, the
agent inspects the evidence, names the provider and the failing check, and
reruns the probe after the fix to see it pass on the same binary. The recorded
report separates **passed**, **failed** and **unverified** capabilities rather
than reducing them to one status.

Two facts the analyst probe established that this work has to handle. Calling an
agent tool over the socket is refused today — `zirkle call tool.shell …` answers
`invocation context required` and `zirkle call memo …` answers `trusted memo cwd
required` — so a probe has to supply the invocation context and a trusted record
path the way the agent's own dispatch does. And the loop should be provable
without a model: use a deterministic local provider, as the audit
[[runtime-audit-2026-09-12]] and the existing offline profile smoke
(`just agent-smoke`) already do.

Scope: running probes and reporting them. Discovering what to run is
[every-enabled-tool-ships-a-contract-probe](../every-enabled-tool-ships-a-contract-probe/prd.md); the evidence channel the report
cites is [a-turn-carries-one-id-through-host-lua-and-bun](../a-turn-carries-one-id-through-host-lua-and-bun/prd.md).
