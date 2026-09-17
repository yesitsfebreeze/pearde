---
state: "done"
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
commit: "ac71b3b6ee892449afb8d8c1b6df00ed80b8488c"
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

- [x] In an isolated project with no running daemon, `cartridge mcp` answers `initialize` and `tools/list` on 5 of 5 cold starts.
- [x] If the listener never becomes active, `cartridge mcp` fails within the documented startup deadline with a message naming the missing listener.
- [x] `just check cartridge`, `just test cartridge` and `just test lifecycle` exit 0.

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

**Round 3 (2026-09-17, analyst-1): the defect is still present and the gate
changed shape.** Re-read from the shared dirty checkout (`cartridge.ctg`
`63ff234` plus unrelated uncommitted idle-timeout work): `attach` still takes no
key (`src/cli/host.rs:59`), the settle still runs on `verify_timeout()` (`:74`)
and `if stable >= 3 && !empty { return; }` is intact (`:215`). The fix is
unchanged. What changed is spec01's Verify: the round-2 15-cold-start `bun`
fixture — which builds the host binary and two dylibs inside 120 s blocks, spawns
fifteen daemons and assumes a `rustc-wrapper` cache that is not in this repo — is
demoted to the implementer's one-off probe, and the gate becomes a source-pinned
grep plus four unit cases over a new **pure** `settled(status, key)` predicate.
With no `stable`/`last` state left, a repeated identical picture cannot end the
wait by construction rather than by measurement. Footprint narrowed to
`src/cli/host.rs` and `.cartridge/tests/unit/stdio.rs`. The three repository
gates were observed to exit 0 on the dirty tree in 4 s, 18 s and 47 s.

## The staged-index precondition is cleared (2026-09-17, coordinator cartridge-24)

Round 4's review and the implementer both carry a standing precondition: that
`prd collect` would refuse repository-wide while the superproject index held
another session's staged rename `R100 .cartridge/tools/pi-voice ->
.cartridge/tools/live`. The implementer flagged it as unchecked.

It is cleared. `git diff --cached --name-only` in the superproject prints
nothing — the rename was authorised by its owner and committed as `89522e3`
earlier today, and the same precondition was observed cleared when the sibling
`@root/one-daemon/.../mcp-keys-sessions-and-inflight-calls` collected at
`805efec` this afternoon. The superproject's working tree still carries
unrelated dirt (`.cartridge/config.lua` and four submodule pointers), but none
of it is staged and none of it is in this footprint.

## Evidence for the ticked boxes (2026-09-17, coordinator cartridge-24)

Implemented at `cartridge.ctg` `d169293` (parent `4b607ea`), which touches
exactly two in-footprint files: `src/cli/host.rs` and
`.cartridge/tests/unit/stdio.rs`. A verifier that neither wrote nor implemented
the plan re-ran everything and reproduced the decisive measurement itself.

All six Verify blocks exit 0 — block 2 runs all four named `settled` cases,
block 4 is `just test cartridge` at 180 run / 180 passed / 0 skipped, block 5
answers `` `mcp` is not provided `` in 2 s, block 6 is `just test lifecycle` at
13 pass / 0 fail in 47 s. The three owner gates exit 0.

Box 1 is the one that mattered, and it was measured rather than argued. The
round-2 cold-start fixture was recovered from this board's own history
(`git -C prd.ctg show 20d140de`), both binaries were built from `git archive`
extractions into scratch target directories outside every repository, and every
run used a fresh project root and its own `XDG_RUNTIME_DIR`:

- unpatched `4b607ea`: 1 of 8, then 4 of 16 — **5 of 24 cold runs failed (21%)**,
  every failure carrying the PRD's exact string
  `` service `mcp` unavailable: no active listener ``;
- patched `d169293`: **0 of 15**, nineteen tools returned cold and settled on
  every run.

The verifier did not reproduce the implementer's 1-in-3 rate on its first
sample and said so: this is a race, the per-sample count moves, and its 21% sits
near the spec's own 29%. The patched side matched exactly. Box 1 asks for 5 of 5
and was met at 15 of 15.

One box is proven structurally rather than at runtime, and is ticked on that
basis because it is what the spec asks for: spec box 3, the per-call status
budget. Block 1's grep plus the committed `while let Some(left) = …` /
`tokio::time::timeout(left, …)` and the two-return guard establish the shape. No
fixture exercises a daemon that answers its socket but never its status, and the
spec does not ask for one.

`attempt-1.patch` was unusable twice over and was not used: `git apply --check`
fails at `src/cli/host.rs:55`, and it spells the predicate `fn serves(...)` with
the starting and empty cases inline, which block 1's
`grep -qF 'fn settled(status: &Value, key: &str) -> bool'` would have rejected.
The committed code implements the spec's folded pure `settled`. That is the
second attempt patch in this board found stale against its own spec today; see
also `@root/one-daemon/.../mcp-keys-sessions-and-inflight-calls`.

The live project daemon was pid 3353 before the verification and pid 3353 after.
No `*.ctg/target/debug` artefact of this composition was rebuilt.
