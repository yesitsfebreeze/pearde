---
state: "analyzing"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 2
date: "2026-09-15"
footprint:
- ".cartridge/tests/integration/smoke.test.ts"
needs:
- sessions-and-gitfs-tests-are-green
- pty-router-harness-mcp-tests-are-green
claim: "coordinator-c4-9 2026-09-16T08:34:16.147Z"
---

# Smoke passes mcp and proxy

## Outcome

The two doors a worker uses (MCP tools, proxied model requests) pass the composed smoke.

## Acceptance

- [ ] `just smoke` exits 0: mcp lists tools with memo active (2026-09-14: `memo inactive`); proxy answers its key check inside its deadline (2026-09-14: timeout); the gate runs only on clean mcp.ctg, proxy.ctg, router.ctg and cartridge.ctg trees, with artifacts rebuilt from them and HEAD shas logged, so a pass proves committed HEAD.

## Result

Attempt 2026-09-15 14:40 (coordinator pass 4, worker dispatched at need's
collect): blocked, nothing implemented.

- Claim refused: footprint overlaps the live proxy-ledger claim
  (@proxy/the-proxy-hands-each-finished-exchange-to-the-memory-ledger,
  handed to the Track C collector, pending its collect).
- Superseded 2026-09-16 by the Planning note: causes 2-3 and "add cartridge.ctg" were fixture bugs (the router EPERM is config dirs outside its write grant), not cartridge.ctg.
- `just smoke all` fails all three targets; diagnosis, three stacked causes:
  1. Fixture ENOENT: `smoke.test.ts:38` symlinks `<root>/builtin/<module>`
     but the composed root has no `builtin/` — predates the restructure
     (root `495fc86`). Fix: symlink `<root>/<module>` directly.
  2. Scratch profiles fail trust (`is in no trusted project`) — needs the
     per-spawn `CARTRIDGE_HOME` + pre-trust pattern just landed in
     pty/harness/sessions/mcp tests.
  3. Router node sandbox_apply dies (`exit 71: sandbox-exec: Operation not
     permitted`) in every scratch composition; a policy-only composition
     works and the real project works; the trigger is the exact profile the
     host generates for the router node from a scratch profile (likely
     `$PROJECT`/`$HOME` grant substitution against the scratch root). The
     fix lives in cartridge.ctg (sandbox/profile.rs or host/plan.rs), the
     host-tests item's repo.
- Next: claim when the proxy collect releases the footprint; the sandbox
  fix belongs with host-tests' isolation work or its follow-up, and the
  fixture + footprint probably need `prd refine` (add cartridge.ctg,
  drop the builtin/ assumption).

## Planning note

2026-09-16, coordinator cartridge-c4, from analyst-1 (`.state/loop/smoke-passes-mcp-and-proxy/`). At committed HEAD every smoke failure comes from the stale fixture `.cartridge/tests/integration/smoke.test.ts`: a missing `builtin/` root, a policy path, config dirs outside the router's write grant, no `CARTRIDGE_HOME`, and a daemon that is never stopped. None of them is in mcp or proxy. The footprint adds that file. The smoke memo sends no model request, so "harness context injected" can't be proven here. That clause is dropped from the box, and the live proof belongs to `@root/every-exchange-reaches-the-memory-ledger-and-condenses-on-the-one-daemon`.

analyst-1 (`.state/loop/smoke-passes-mcp-and-proxy/analyst-1.md`) predates review round 2. Its clean-tree and dylib-freshness observations are stale. spec01 now requires the four trees to be clean and rebuilds them in the gate.
