---
state: specced
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
footprint:
  - "proxy.ctg/src/service.rs"
  - "proxy.ctg/.cartridge/docs/README.md"
  - "proxy.ctg/.cartridge/tests/unit/tests.rs"
---

# the proxy never teaches one tool twice

## Outcome

A caller that already carries one of the harness tools under a server
namespace of its own — an MCP client's `mcp__cartridge__memo` for `memo` —
owns that tool's surface for the request: the proxy injects no second copy.
Each cartridge tool appears to the model exactly once.

## Acceptance

- [x] A request whose caller tools include `mcp__cartridge__<name>` gets no
  injected `cartridge__<name>` for that tool; tools without a namespaced
  caller copy are still injected (unit test:
  `namespaced_copies_of_injected_tools_are_skipped_not_duplicated`,
  proxy.ctg unit suite).
- [x] An exact `cartridge__<name>` caller tool still fails the collision
  check in `wire::inject` before any side effects (same test, second half).
- [x] The namespaced copy's calls are caller-owned: no internal dispatch,
  no policy round, no observation journaling for them.
- [x] `proxy.ctg/.cartridge/docs/README.md` documents skip-vs-collision.
- [x] The proxy unit suite passes (51 tests).

## Notes

Implemented in `proxy.ctg/src/service.rs::run`: caller tool names are
collected per wire (`t["name"]` for Anthropic/Responses,
`t["function"]["name"]` for Chat) before descriptor assembly; a descriptor
whose public name `cartridge__{name}` is the suffix of a strictly longer
caller tool name is skipped. The strict-suffix condition keeps exact-name
collisions authoritative in `wire::inject`, where they fail before
forwarding as before.