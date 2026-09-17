---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
footprint:
- "src/transport/cartridge.rs"
needs:
- "a-cartridge-call-can-be-cancelled"
---

# A wedged call reports its late answer

## Outcome

When a call outlives its bound and the provider answers afterwards, that answer
reaches the session as a result or a failure instead of vanishing. A caller is
never left with neither.

## Evidence

Established 2026-09-17 by the analyst of `@mcp/a-cartridge-call-is-cancellable-and-bounded`
against `cartridge.ctg` HEAD `63ff234`: `Ctx::bail` (`src/transport/cartridge.rs:416-425`)
discards a late answer entirely. Combined with the caller-side timeout that
tells the provider nothing (`:389-393`), a wedged call spends its work and then
throws the result away, which is why a worker sees `<id> did not answer in time`
and nothing ever explains what happened.

## Acceptance

- [ ] An answer that arrives after its bound expired is reported to the session
      rather than dropped.
- [ ] The report distinguishes a late success from a late failure.
- [ ] A test drives a provider that answers after the bound and asserts the
      session observes the outcome, failing in the world it denies.

## Needs

`a-cartridge-call-can-be-cancelled`, and not only for ordering: both change
`src/transport/cartridge.rs`, so they must land serially, and the cancellation
path decides what "late" even means.
