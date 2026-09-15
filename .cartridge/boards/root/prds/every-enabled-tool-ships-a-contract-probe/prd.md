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
canonical-scope: every-enabled-tool-ships-a-contract-probe
needs:
- "@root/debug-mode-opens-and-closes-from-the-shell"
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

## From the retired work memo

Folded 2026-09-15 from `work/every-enabled-tool-ships-a-contract-probe.md` (status open, estimate 2d). The PRD state above is authoritative.

> Debug discovery lists every enabled tool with its backing service and a runnable contract probe its cartridge ships

### Outcome

Debug discovery answers one question completely: what can this agent do, who
provides it, and how is that claim checked. It enumerates every enabled agent
tool with the service backing it, and for each one a runnable contract probe
shipped by the providing cartridge. A tool with no probe, and a capability that
is skipped or unavailable in this environment, is reported as **unverified** —
never as passed, never silently omitted.

Half the enumeration already exists and should be reused, not rebuilt: `zirkle
list` resolves every injected key to its provider, printing `tool.shell <- pty`
and `tool.memo <- memo` for the default profile, and the effective tool set is
one explicit table in `.zirkle/default/init.lua` that feeds both the agent's
injections and its dispatch list. `zirkle status` adds the live per-fiber state.

The missing half is the probe itself. No cartridge ships one today: of
`builtin/{agent,fs,harness,memo,policy,sessions,shell,ui}` with a `.zirkle/memos/`
record, none holds a probe memo, and there is no declared kind for one. A probe
travels with the cartridge that makes the claim, so adding a tool adds its probe
in the same folder — discovery must not carry a central list of what to check.
The program map from [the-agent-can-discover-its-own-program](../the-agent-can-discover-its-own-program/prd.md)
(`builtin/memo/.zirkle/memos/note/program-map.md`,
`program-cartridge-contracts.md`, `program-checks.md`) is the description to
attach probes to.

Scope: declaring and discovering probes, and reporting what is unverified.
Executing them against fixtures is
[tool-probes-run-and-locate-a-failing-provider](../tool-probes-run-and-locate-a-failing-provider/prd.md).
