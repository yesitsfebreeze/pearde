---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 95
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
capability-owner: runtime
canonical-scope: second-harness-composition-proof
review-round: 3
review-status: passed
needs:
  - '@harness/concise-writer-cartridge'
---

# A second harness works by composing existing cartridges

Verify that an author can build a concise writing harness by adding one
[writer cartridge](../../../harness/prds/concise-writer-cartridge/prd.md) and a
composition profile, reusing the transport host and the shipped cartridges
unchanged. **Base** means that foundation plus the default composition. On
2026-09-14 that composition is the root `.cartridge/init.lua` and `config.lua`,
which are uncommitted; cartridge.ctg no longer carries one (b1494bb). Owner: runtime.

## Acceptance

- [ ] From a clean disposable checkout, a short author guide composes the writer. Its real-model corpus shows shorter replies and readable memos with required meaning kept. Record setup time, commands and diff, with zero edits to host, transport or capability source.
- [ ] With a deterministic model endpoint, exercise real memory, gitfs, pty, policy, router and sessions events: call each and read back its effect. A profile-only swap restores the default harness, which passes the same checks.
- [ ] Missing or undeclared needs, denied grants, malformed replies, deadlines, cancellation, restart and failed reload give attributable outcomes. Committed data survives, with no uncertain-mutation replay, duplicate writer, orphan process or widened grant.
- [ ] Three clean repetitions produce a pass/fail matrix with revisions, platform, timings and every manual workaround.
- [ ] Each failure reuses a matching open PRD or files one owner-local repair PRD; close only after repairs and a complete rerun.

## Proof and recovery

First commit or pin the root composition profile, then record the current
baseline. The release-status note already lists failures: smoke mcp/proxy, and
harness, gitfs, pty, router and sessions tests. Start at
`cartridge.ctg/src/transport`, `.cartridge/tests/unit/src/tests/host.rs`,
`docs/creating-cartridges.txt` and `harness.ctg/.cartridge/help.md`. From
`/Users/feb/dev/cartridge` run `just test runtime`, `just test harness` and
`just smoke`. Use disposable stores; teardown touches only fixture resources.

## Dependencies and review

The baseline probe can start now; the full trial needs the writer. Reuse
[composition work](../cartridges-compose-recursively/prd.md). [Review](review.md): round 3/5.
