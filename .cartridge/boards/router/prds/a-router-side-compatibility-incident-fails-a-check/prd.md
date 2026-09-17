---
state: open
origin: requested
priority: 40
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/service.rs"
- "justfile"
- ".cartridge/tests"
---

# a router-side compatibility incident fails a check

## Outcome

The standard the other six PRDs meet is enforced by something that runs, not by
a person reading the health view. A route shelved for a shape the router could
have adapted fails a check; a route shelved because an account has no balance
does not.

## Evidence

The seven causes in [[@router/system/vision.md]] were found by reading 91
incidents by hand on 2026-09-16. Nothing in the repository would have reported
them, and several had been failing for long enough to spend 14 to 20 attempts
each. A rule that matters becomes a check that runs; a standard nobody can run
is a standard nobody keeps.

The distinction the check must draw already exists in the data. `payment`,
`quota` and `auth` incidents are the operator's — an empty balance, a missing
login, a spent quota — and must never fail a check, or the check fails on every
machine that has not logged into every provider. `compatibility` is the
router's own, and after the other six PRDs land there should be none.

## Acceptance

- [ ] A check reports every open `compatibility` incident, with its route, its
      attempt count and the provider's own message.
- [ ] It exits non-zero when one is open and zero when none is, and it says
      which of the seven known causes each one matches, or that it matches none.
- [ ] It passes on a machine with no credentials at all: absent providers
      contribute no routes and therefore no incidents.
- [ ] `payment`, `quota`, `auth` and `transport` incidents are reported as
      context and never fail the check.
- [ ] It is reachable the same way the other gates are, beside `just check
      router` and `just test router`, and named in `.cartridge/help.md`.
- [ ] A test drives a synthetic health store with one compatibility incident
      and one payment incident, and asserts the check fails on the first and
      not the second.

## Needs

- a-tool-schema-the-provider-rejects-is-rewritten-to-its-dialect
- a-parameter-a-route-renames-is-renamed-rather-than-dropped
- a-deprecated-model-leaves-the-catalog-instead-of-being-retried
- a-route-that-refuses-reasoning-keeps-answering-without-it
- a-route-that-refuses-the-developer-role-is-sent-system
- a-model-that-names-another-endpoint-is-routed-to-that-endpoint

## Planning note

2026-09-16. Last of the set by dependency, not by importance: it is the part
that keeps the other six from silently regressing. Filed from
[[@router/system/vision.md]], whose "what done looks like" section this check
makes executable.
