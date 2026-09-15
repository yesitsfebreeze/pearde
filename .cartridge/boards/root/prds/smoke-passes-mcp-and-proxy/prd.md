---
state: open
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
- "mcp.ctg"
- "proxy.ctg"
- "memo.ctg"
- ".cartridge/memos/routine/cartridge-smoke.md"
needs:
- sessions-and-gitfs-tests-are-green
- pty-router-harness-mcp-tests-are-green
---

# Smoke passes mcp and proxy

## Outcome

The two doors a worker uses (MCP tools, proxied model requests) pass the composed smoke.

## Acceptance

- [ ] `just smoke` exits 0: mcp lists tools with memo active (2026-09-14: `memo inactive`); proxy answers an authenticated request inside its deadline with harness context injected (2026-09-14: timeout).

## Result

Attempt 2026-09-15 14:40 (coordinator pass 4, worker dispatched at need's
collect): blocked, nothing implemented.

- Claim refused: footprint overlaps the live proxy-ledger claim
  (@proxy/the-proxy-hands-each-finished-exchange-to-the-memory-ledger,
  handed to the Track C collector, pending its collect).
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
