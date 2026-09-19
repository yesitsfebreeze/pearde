---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge"
capability-owner: runtime
needs:
  - '@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/the-host-answers-policy-and-policy-explain-with-the-evaluator-policy-ctg-had'
footprint:
  - /Users/feb/dev/cartridge/.gitmodules
  - /Users/feb/dev/cartridge/policy.ctg
  - /Users/feb/dev/cartridge/.cartridge/init.lua
  - /Users/feb/dev/cartridge/.cartridge/justfile
  - /Users/feb/dev/cartridge/.cartridge/tests/integration/smoke.test.ts
  - /Users/feb/dev/cartridge/.cartridge/memos/routine/cartridge-smoke.md
---

# policy.ctg leaves the composition and the repository

## Outcome

the submodule and its `init.lua` row (`.cartridge/init.lua:30`) are removed, and `policy` is dropped from the `check`/`test`/`smoke` owner lists (`.cartridge/justfile:100-102`). The smoke fixture's policy profile becomes a host with no cartridges (`init.lua` `return {}`) that is still answered by `cartridge run policy`. The pointer moves to child 1's commit, all in one superproject commit.

## Acceptance

- [ ] `just smoke policy` passes against a profile that composes no `policy.ctg`, with the same four decisions and the `null` rejection.
- [ ] `git submodule status` lists no `policy.ctg`, and no file outside `prd.ctg` names `policy.ctg`.
- [ ] `just test runtime`, `just isolation` and a live `env -u CARTRIDGE_YOLO cartridge call policy '{"tool":"read","input":{},"context":{}}'` all exit 0.

## Provenance

Child 2 of 7 of @runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow, split 2026-09-19 by coordinator cartridge-4b from its analyst report (base cartridge.ctg 324f36e). Review rounds used: 0 of 5 (the parent had no review.md). Evidence: the parent `## Split` section and `.state/loop/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/analyst-1.md`.

## Landing notes (2026-09-19, from cartridge-f4 and cartridge-cc)

- The footprint no longer lists `cartridge.ctg`. As a whole directory it reserved the entire host repository and would have clashed with every cartridge.ctg lane on the board. If this row really must move the `cartridge.ctg` pointer, name that in a re-reviewed spec. Otherwise child 1 bumps the pointer when it lands.
- `policy` is active in the live daemon. Source: the manifests, read 2026-09-19. `mcp.ctg/cartridge.json` needs `policy` and `policy.*`; `agent.ctg` and `proxy.ctg` need `policy`. The live daemon could not confirm this, because mcp was `failed` on a trust refusal at the time. Once child 1 lands, the host must answer every key that `policy.*` matches, `policy.explain` included. Confirm this with a live `cartridge call` through mcp before and after the removal, because a failure would surface at mcp, not at policy.
- Removing a submodule changes `.gitmodules` and the superproject index while other sessions hold lanes that reach live submodules through sibling symlinks. Whoever dispatches this row announces it to every coordinator first, the way host swaps are announced, and picks a window when no lane is building.
- Order of landings in `.cartridge/justfile`, agreed with cartridge-f4: first `@root/an-owner-check-runs-the-isolation-gate-and-says-so` (the uncommitted `_fan` isolation hunk), then `@root/the-composition-s-gates-do-not-inherit-cartridge-yolo`, then this row.
