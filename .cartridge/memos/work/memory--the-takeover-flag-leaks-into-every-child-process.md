---

kind: work
level: 10
status: done
description: "`MEMORY_TAKEOVER` is set in the successor's environment and never removed, so a hot-reloaded daemon passes it to the hub it auto-starts and the hub passes it to every node it spawns — where fd 0 is `/dev/null` and listener adoption fails"
read_when: "touching a spawn, the handover, or a node that will not bind"
---

# the-takeover-flag-leaks-into-every-child-process

## Do

`spawn_successor` sets `.env(TAKEOVER_ENV, "1")`
(`src/identity/src/lib.rs:159-171`) to tell the successor that fd 0 is the bound
listener. Nothing ever removes it, so it stays in that process's environment for
its whole life — and both of the other spawn sites use `Command::new` without
clearing the environment.

The chain, all in the tree:

1. Any `cargo install` triggers a handover
   ([[hot-reload-fingerprints-mtime-not-content]]), so the running daemon is a
   successor carrying `MEMORY_TAKEOVER=1`.
2. 500 ms into its boot it runs `register_with_hub`
   (`commands/src/lib.rs:1211`, `src/commands/src/commands_hub.rs:369-397`),
   which calls
   `connect_hub_or_start` and, with `hub.auto_start` on and no hub running,
   spawns one through `spawn_detached` — inheriting the variable.
3. The hub spawns a node for a root with `Command::new(exe).arg("--daemon")`
   and `.stdin(Stdio::null())` (`hub/src/lib.rs:99-105`) — inheriting it again.
4. That node's `is_takeover_boot()` is true. It skips `maybe_self_heal_store`
   (`lib.rs:953`) and `evict_predecessor` (`:1094`), then takes the adoption
   branch at `:1149` and calls `adopt_memory_listener` on fd 0, which is
   `/dev/null`. On `Err` it logs "takeover adoption failed" and **returns** —
   the node never binds and never serves, and the hub's readiness probe reports
   the spawn as failed.

Remove it where it does not belong: `.env_remove(identity::TAKEOVER_ENV)` on
the hub's node spawn and on `spawn_detached`. Belt and braces, `is_takeover_boot`
could also require fd 0 to actually be a socket, which would make the flag
self-checking rather than trusted.

This is an argument from the code, not an observed failure — the last two steps
have not been run. What would settle it is step 5 of the Check.

**Done 2026-09-06 — three changes, and the third is the one that matters.**
Both `.env_remove(identity::TAKEOVER_ENV)` calls are in, on the hub's node spawn
(`hub/src/lib.rs:99`) and on `spawn_detached`
(`src/commands/src/commands_hub.rs:310`), each
with the reason beside it.

The third was not in the `Do`. Step 4 of the chain ends at `lib.rs:1161`, where
adoption failure was `tracing::error!` followed by `return` — the node exits
having served nothing and the hub's readiness probe reports a spawn that never
came up. That is unrecoverable by construction: **any** future leak of the flag,
not just the two closed here, produces a daemon that dies silently. It now
returns `None` and falls through to `bind_memory_listener`, which the surrounding
code already handles — `Bound` serves, `AlreadyRunning` stands down with a
message, `Err` names the refusal. A spurious flag costs a warn line instead of a
dead process, and a genuine takeover whose adoption fails recovers by binding.
Downgraded to `warn` because it is no longer fatal.

The `Do`'s alternative — making `is_takeover_boot` require fd 0 to be a socket —
was **not** done. It needs `libc`, which this tree avoids on purpose
(`spawn_successor` goes out of its way), and the fallback makes the flag
self-correcting without a dependency: believing it wrongly now costs nothing, so
the check has little left to buy.

**The Check is not claimed.** Its step 5 is a live sequence — install, force a
handover, stop the hub, ask the successor's hub for a node from a second root —
and it was not run. The part is honest that the last two steps of its chain were
never observed, and a green suite does not exercise them, so converting an
argument from the code into a claim of proof would be the thing this record
keeps catching. What holds: the three paths are what the part says they should
be, and a node reaching the adoption branch spuriously no longer dies.

## Check

`.env_remove` on both spawns, and: start a daemon, `cargo install --force` to
force a handover, stop any running hub, then from a second root ask the
successor's hub for a node — the node binds and serves rather than logging
"takeover adoption failed". `just test` green — the suite half holds at 1,255
passed; the live sequence was not run.
