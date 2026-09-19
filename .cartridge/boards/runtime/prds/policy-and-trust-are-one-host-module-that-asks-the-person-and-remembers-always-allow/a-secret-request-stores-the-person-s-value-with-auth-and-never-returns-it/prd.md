---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
needs:
  - '@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/a-consumer-raises-an-approve-or-input-request-and-a-person-answers-it-from-the-command-line'
  - '@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values'
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/secret.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/request.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/policy/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/request.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/policy
  - /Users/feb/dev/cartridge/cartridge.ctg/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/help.md
---

# a secret request stores the person's value with auth and never returns it

## Outcome

`kind: "secret"` names `{provider, field}`. The person's value goes from the CLI (read without echo) to the host and on to auth's store key only. The requester receives `{stored: true}`.

## Acceptance

- [ ] Named test with a fake store listener: the requester's result is exactly `{stored:true}`, and the value appears in no channel entry, pending summary, log line (captured tracing) or reply other than the store call.
- [ ] Named test: `always` on a secret is refused, and the CLI never takes a secret from argv, only from stdin with no echo.

## Provenance

Child 7 of 7 of @runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow, split 2026-09-19 by coordinator cartridge-4b from its analyst report (base cartridge.ctg 324f36e). Review rounds used: 0 of 5 (the parent had no review.md). Evidence: the parent `## Split` section and `.state/loop/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/analyst-1.md`.

## Contract note (2026-09-19, from cartridge-b0, which owns the auth board)

`@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values` does not provide a store key and will not grow one. It ships auth's own store under `~/.cartridge/auth` (pass layout `cartridge/<provider>/<field>`), the events `auth {op:"status"|"list"}` that return names and states only, and one value door: `bun <auth.ctg>/src/insert.ts <provider> [field]`, which reads stdin, runs outside the daemon and creates the key and store on first use. The recorded auth decision is "no event carries a value, in or out", because the transport keeps 1024 envelopes per channel in memory (`cartridge.ctg/src/transport/cartridge.rs:474-486`) and the ASP ring will persist every published envelope.

So "on to auth's store key" in the Outcome cannot be built as written. Two options:

- (a) Recommended by b0: the host CLI that answers the secret request runs the insert door itself, spawning `bun <auth root>/src/insert.ts <provider> <field>` with the value piped to stdin, so the value is never an envelope. It needs nothing new from auth and keeps auth's rule.
- (b) A new @auth PRD adds a store key. It must first show the value never enters a retained channel or the ring, and it needs a write grant on the store.

The analyst for this child must resolve the Outcome against (a) before speccing, or raise a question if (b) is wanted.

Update (2026-09-19, cartridge-b0): the prerequisite is done at auth.ctg `c5e8871`. The door is `bun /Users/feb/dev/cartridge/auth.ctg/src/insert.ts <provider> [field]`, with the value on stdin. It prints `pass:cartridge/<provider>/<field>` and refuses an empty value with "A secret value is required on stdin". The store is `~/.cartridge/auth/store`. `auth {op:"status",provider,field?}` reports `available_unverified` once the entry exists.
