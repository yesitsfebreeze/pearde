---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: blocked
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# two daemons served this root at once during a binary handover and fought over the flush epoch — the claim on the store is now a refusal, and the hour of quiet log is still unobserved

## Do

The daemon log carries the fight twice inside eleven minutes on 2026-09-06:

```
memory.persist: refused to flush a stale snapshot — disk advanced under us
 (another writer); absorbing disk rows and retrying  disk_epoch=2895 expected=2856
```

Both times a second daemon was serving `/Users/feb/dev/memory` — one started by
hand in this session, one replacing itself through a `cargo install` handover —
and each flushed a snapshot the other had already advanced. The retry loop that
follows is a candidate for the runtime stall in
[the-daemon-comes-back-after-the-watchdog](../the-daemon-comes-back-after-the-watchdog/prd.md): a flush that keeps losing its
epoch is a flush that blocks past the watchdog's five seconds.

The refusal that should have prevented it was keyed on the socket, not the
store. A daemon replaces a running daemon for the same root because the socket
tag is the canonicalized root (`socket-tag-is-canonicalized`) — but the
handover deliberately leaves the predecessor alive long enough to pass the
listener fd, and a root reached under two names widens the same window
(`uncanonical-root-gets-own-daemon`).

The claim is now the refusal, and it is keyed on the data dir: `store::lock`
was already the one lock the store needs — an flock, so two spellings of one
dir are one lock on one inode (`one_store_under_two_names_is_one_lock`) — and
what was missing was that `claim_writer_lock` in `commands_serve.rs` gave up
after ten retries and served anyway. It now refuses, naming the holder, and
`bootstrap` returns `None` so nothing binds. The claim moved ahead of
`maybe_self_heal_store`, which is what makes the exclusivity that compaction
already assumed actually true. The orderly hot reload takes the lock out of the
`EngineHandle` and drops it before it spawns its successor, so the one path
that legitimately hands the store over passes it rather than racing it; the
retries remain for the watchdog's dark handover, where the predecessor
force-exits and only the OS can release.

What is left is the observation: the second half of the Check cannot be read
from a test. Blocked until a person runs two daemons over one data dir for an
hour and reads the log.

## Acceptance
Two daemons started against different roots that both reach
`/Users/feb/dev/memory/.memory/data`: the second refuses the store with a message
naming the holding pid, and the daemon log carries no `disk advanced under us`
line over an hour of normal use.

**Check read 2026-09-07: the first clause passes, the second waits on a person.**

The first clause — "the second refuses the store with a message naming the
holding pid" — is now held by
`lifecycle::a_second_daemon_over_one_store_refuses_and_names_the_holder`
(`tests/e2e/lifecycle.rs`): two `MemoryProject`s, the second's `data_dir` pointed
at the first's `.memory/data`, its daemon spawned with piped stderr and asserted
to exit without binding a socket, its output carrying `daemon pid <first>` —
the line `store_core::lock` writes as `"{what} pid {}"`. The refusal it proves
is `claim_writer_lock` (`src/commands/src/commands_serve.rs:55`), which after
ten retries names the holder and returns `None` so `bootstrap` never serves.

An earlier read the same day recorded the opposite — "the `Do` is
unimplemented, not merely unverified" — against the documentation comment that
called the claim non-fatal. The comment and the code had already parted: the
refusal landed in c6b88899, and only the test was missing.

The second clause needs two daemons started against different roots that reach
one data dir, and an hour of normal use watched. That is a person starting
processes on a shared machine, not something a sweep should provoke, and this
memo waits on that observation rather than being re-picked every pass
([[the-eight-unread-work-checks]]). The fight it would watch for was last seen
in `.memory/daemon-run.log` at 2026-09-06 16:33:27 (`disk_epoch=9958
expected=9957`), with `memory watchdog: async runtime stalled ~30s ... guarded
flush blocked past 5s` on the very next line — the causal chain to
[the-daemon-comes-back-after-the-watchdog](../the-daemon-comes-back-after-the-watchdog/prd.md) this memo proposed as a candidate,
observed in sequence in one log.
