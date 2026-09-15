---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# the fourteen daemons a handover left behind ignored SIGTERM and SIGINT and needed SIGKILL, so their graceful shutdown never ran — a freshly started daemon exits on SIGTERM normally

## Do

Measured 2026-09-06 on the fourteen daemons a `cargo install` handover left
behind ([a-successor-inherits-every-descriptor](../a-successor-inherits-every-descriptor/prd.md)): `kill -TERM` on all
fourteen, all fourteen alive five minutes later at 0% CPU; `kill -INT`, all
fourteen still alive; `kill -KILL`, gone. A daemon started fresh in the same
session exits on `kill -TERM` within six seconds. So the difference is the
spawn, not the code.

The mechanism is now measured too, on a spawned child rather than assumed from
the standard: `identity_tests::stop_signal_tests` sets SIGINT (then SIGTERM) to
ignore between fork and exec — exactly what a backgrounded parent hands down —
and has the child signal itself. It survives, so an ignored disposition does
cross `exec`; with `reset_stop_signals` in the same `pre_exec` it dies of the
signal, so the reset lands. That reset is now the first thing
`spawn_successor` does before exec (`src/identity/src/lib.rs`), beside the
close-on-exec sweep.

The other half is already landed: `util::lifecycle::terminate()` selects on
SIGTERM beside `ctrl_c`, and the daemon stops through it
(`src/commands/src/commands_serve.rs:258`), so the ordinary way to stop a
process is the way that flushes.

Landed `73681460`: the reset in `spawn_successor` and, in `identity_test.rs`,
`the_successor_spawn_restores_both_dispositions` — the test half of the Check.

The live half is now `lifecycle::a_handover_generation_stops_on_a_signal`
(`tests/e2e/lifecycle.rs`), and it runs in about eight seconds. A copy of the
binary is started under `sh -c "trap '' INT TERM; exec ..."` — a backgrounded
parent's dispositions, handed to memory by the `exec` — then a second copy is
`touch`ed and renamed onto that path so `cfg.reload`'s self-watch hands over.
`touch` is load-bearing: on macOS `fs::copy` clones the source's mtime with
the bytes, and the fingerprint is (len, mtime), so two copies of one file are
the same binary to the watch. The successor's pid comes out of `writer.lock`,
the one place a daemon publishes it — the successor is nobody's child once the
predecessor exits — and its `shutting down... / done` out of the stderr pipe it
inherited, read past the predecessor's `handing over to new binary`.

The reading the run added: the reset cannot be seen from the outside. Remove it
from `spawn_successor` and the e2e stays green, because the predecessor
registers handlers for both signals the moment it awaits
`util::lifecycle::terminate()`, which replaces the inherited `SIG_IGN` before
it ever forks — and `exec` resets a *handled* signal to default in the child
for free. The reset covers the generation whose predecessor installed no
handler, which is exactly the fourteen daemons that took only SIGKILL. So the
mechanism's red proof stays the unit test; the e2e holds the behaviour the
`Check` names.

## Acceptance
A daemon spawned through a handover from a backgrounded parent exits on
`kill -TERM` within ten seconds and its log carries the shutdown flush, and a
test asserts both signals are at their default disposition in the successor.
