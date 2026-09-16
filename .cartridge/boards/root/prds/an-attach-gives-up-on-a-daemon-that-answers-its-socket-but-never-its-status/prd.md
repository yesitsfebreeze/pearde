---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge"
footprint:
- "cartridge.ctg"
- "cartridge.ctg/src/cli/host.rs"
- "cartridge.ctg/src/transport/rpc.rs"
---

# an attach gives up on a daemon that answers its socket but never its status

## Outcome

An attach to a daemon that accepts a connection but never answers fails with a
diagnosable error inside a bounded time, instead of hanging forever. Every leg
of the attach path is bounded, and the bound is one the caller can reason about.

## Evidence

Found by the round-2 reviewer of
`@root/one-daemon-.../live-attaches-to-the-daemon-instead-of-spawning-its-own`
on 2026-09-16 (finding F9), while confirming that the live launcher may safely
drop its own kill timer.

`cartridge.ctg/src/transport/rpc.rs:239-257` awaits an untimed oneshot, and
`settle_remote` (`src/cli/host.rs:144-183`) checks its deadline only *between*
calls. So a daemon holding an open socket that never answers `status` hangs the
caller indefinitely. The other legs are bounded — `startup_timeout_secs` 60,
`verify_timeout_secs` 300, `event_timeout_ms` 60000 — which is why the rest of
the attach path has a ~420 s worst case.

Until now the live launcher's own 10-second kill masked this at ~30 s for that
one caller. That timer was removed deliberately (it fired mid-settle and killed
healthy cold attaches), so the hole is now reachable. Re-adding a launcher-side
timer is the wrong fix: it would reintroduce the bug that removal solved.

## Acceptance

- [ ] An attach against a daemon socket that accepts and never answers fails
      within a bounded, documented time, with an error naming what timed out.
- [ ] The bound is enforced in the transport, not in any one caller, so every
      caller of the attach path inherits it.
- [ ] A healthy cold attach that legitimately takes longer than the old
      launcher timer still succeeds (no regression of the removed kill).

## Planning note

2026-09-16, coordinator cartridge-1b. Filed as its own PRD rather than widened
into the live-attaches PRD: the defect is in `cartridge.ctg`'s transport, which
is outside that PRD's footprint (`live.ctg/src/launch.ts` plus its test), and it
predates that change. Not a blocker for it — the reviewer passed that plan at 92
with this recorded as non-blocking.
