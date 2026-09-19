---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
needs:
  - '@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/the-host-answers-policy-and-policy-explain-with-the-evaluator-policy-ctg-had'
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/request.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/pending.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/channel.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/plan.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/socket.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/request.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/args.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/policy
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/host/socket.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/transport.txt
---

# a consumer raises an approve or input request and a person answers it from the command line

## Outcome

`policy.request` is a host-owned event with a declared `timeout_ms`. It takes `{kind: approve|input, operation, summary, schema?, timeout_ms}` and resolves to `allowed | denied | timed_out`, plus `value` for `input`. The requester is stamped from the connection's token. Today `Caller::Cartridge` drops the id (`socket.rs`: `host.caller(token).map(|_| Caller::Cartridge)`), so it must carry it. `answer` and `requests` are socket methods, never events and never `tool.*`, granted only to the host token. The empty token no longer passes as `Caller::Host` (`socket.rs`, the `ponytail:` comment). Every pending request's summary is published on a host channel, `policy`, that clients `subscribe` to like `lifecycle`. The command line gets `cartridge request [list|follow|answer <id> allow|deny|--value <json>]`.

## Acceptance

- [ ] Named tests: a timeout answers `timed_out` and counts as a denial; a second answer to an id is refused; the wait is bounded by `timeout_ms`.
- [ ] Named tests: a `requester` field supplied in the data is ignored or refused, and the stamped id is the calling cartridge. A cartridge token, and the empty token, get `UNAUTHORIZED` on `answer`, including for the cartridge's own request.
- [ ] Named test: a channel subscriber receives each pending summary with its originator. An `input` value appears in no channel entry and in no log line, which the test checks by capturing the tracing output.
- [ ] `cartridge request answer` from a terminal resolves a request raised with `cartridge call policy.request`, shown by a transcript in the evidence.

## Provenance

Child 3 of 7 of @runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow, split 2026-09-19 by coordinator cartridge-4b from its analyst report (base cartridge.ctg 324f36e). Review rounds used: 0 of 5 (the parent had no review.md). Evidence: the parent `## Split` section and `.state/loop/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/analyst-1.md`.
