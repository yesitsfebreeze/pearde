---
state: "open"
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
capability-owner: runtime
work-kind: leaf
footprint:
- "cartridge.ctg"
- "cartridge.ctg/src/cli/host.rs"
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
---

# cartridge mcp waits for a cold host to settle

## Outcome

On a cold host (no daemon yet), `cartridge mcp` gives up with "service mcp unavailable:
no active listener" — 3 of 3 runs as first reported, and about one cold run in three on
independent re-measurement with a fresh project root per run (see the Planning note: the
defect is a real but probabilistic race, not a certainty). It stops waiting after three
identical status polls while cartridges are still starting
(`cartridge.ctg/src/cli/host.rs:157` at cdd3124/771e046).
The first MCP client of a fresh project therefore fails. The wait should end when the
requested listener is active or a bounded startup deadline passes, not on repeated
identical polls.

## Acceptance

- [ ] In an isolated project with no running daemon, `cartridge mcp` answers `initialize` and `tools/list` on 5 of 5 cold starts.
- [ ] If the listener never becomes active, `cartridge mcp` fails within the documented startup deadline with a message naming the missing listener.
- [ ] `just check cartridge`, `just test cartridge` and `just test lifecycle` exit 0.

## Proof and recovery

Found 2026-09-16 by the smoke analyst of `@root/smoke-passes-mcp-and-proxy` (spec01 round-4
revision). The smoke fixture works around it by starting the daemon itself. The fix lands
after the daemon-attach leaf, which rewrites the same attach path in `src/cli/host.rs`.

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1.

**The defect still reproduces at HEAD** — established before planning
any fix, because the done attach sibling (`cartridge.ctg 1aefee3`) rewrote
`attach` and three other rows on this board turned out to rest on premises that
had already dissolved. Here the premise is intact and only the line numbers
moved: at `63ff234`, `attach` is `src/cli/host.rs:59`, the settle call `:74`,
`settle_remote` `:147`, and the three-identical-poll return `:180`. Measured in
an isolated project with a scratch `CARTRIDGE_HOME`: the status picture
`{active:13, starting:2, waiting:2}` holds for ~300–400 ms while `mcp` needs
~1.6 s, so `stable >= 3` fires and the run fails in ~2.0 s with
``service `mcp` unavailable: no active listener``.

**Round 2 correction (2026-09-16, analyst-2): the baseline is probabilistic.**
The analyst's 5-of-5 and the smoke analyst's 3-of-3 both counted runs that reused
one project root, where only the first run is genuinely cold. With a *fresh*
project root per run the round-1 reviewer measured 5 failures of 8 and analyst-2
measured 31 failures of 108 (29 %). The defect and the fix are unchanged; what
changed is the acceptance test, which now runs 15 genuinely cold starts across
two Verify blocks because 5 would green-light an unpatched tree about 18 % of the
time. Accepted cost now named in spec01: an unserved key plus a cartridge stuck
`starting`/`waiting` waits to `startup_timeout_secs` (60 s) where it used to
return in ~300 ms.

The analyst's first probe was a **false** reproduction (a missing `cartridge
trust` made 15 cartridges fail on trust, a different error); it recorded and
discarded it rather than counting it.

**The real deadline is `host.startup_timeout_secs` (60 s), and today nothing
applies it.** `attach`'s own 60 s loop never binds the settle, because the
`Ok(Some(found))` arm calls `settle_remote(&found.0, settings.verify_timeout())`
and returns from inside that arm — so the only bound is `verify_timeout_secs`
(default 300), a *verify* budget misapplied to CLI startup. The fix moves the
settle to `startup_timeout()` and leaves `verify_timeout()` to its three
in-process callers.

The fix is one guard in the shared function rather than a patch at the `mcp`
call site: all four `attach` callers already know their key, so `attach` takes
`key: &str`, `settle_remote` returns when an `active` cartridge lists it, and the
`stable`/`last` shortcut is deleted — which fixes `run` and `launch` too.
Prototype measured 0 of 5 failures, and 0 of 35 with the round-2 fresh-root fixture.

**Overlap with `@root/an-attach-gives-up-on-a-daemon-that-answers-its-socket-but-never-its-status`
is real and disclosed, and the two do not fight.** `settle_remote`'s deadline
only checks *between* `Peer::call` awaits, so it does not bind against
`rpc.rs:239-257` at all; since this fix increases the poll count, the spec wraps
the status call in `tokio::time::timeout` — the in-footprint way, since `rpc.rs`
belongs to that PRD. The rpc-layer fix makes the wrapper redundant but harmless.
Ship both, this one first.

**Landing shape:** superproject PRD with a submodule footprint, so it collects
with **no lane** — a superproject lane worktree leaves submodules empty and
Verify pass 1 cannot build there.
