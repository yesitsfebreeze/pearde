---
state: "claimed"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/live.ctg"
capability-owner: live
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/launch.ts"
- ".cartridge/tests/integration/launch.test.ts"
claim: "coordinator-cartridge-1b-3 2026-09-16T10:59:26.143Z"
---

# Live attaches to the daemon instead of spawning its own

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. Two findings from the parent:

- `live.ctg/src/launch.ts:46-52` spawns `--yolo daemon` undetached when
  `status` fails — the only place outside cartridge.ctg that starts a daemon,
  and it defeats the one-daemon shape.
- live marks in-flight tasks `interrupted` at start
  (`live.ctg/src/coordinator.ts:30-38`), which kills the other host's work
  when two compositions run; under one daemon this becomes harmless, but the
  marking must not fire on attach.

## Outcome

`launch` attaches to the project daemon (starting it through the host-attach
contract when none answers) and never spawns its own daemon. Attaching does
not mark existing in-flight work `interrupted`.

## What changes

- `launch.ts` drops its `--yolo daemon` spawn; it uses the attach path from
  the host-attach child.
- `coordinator.ts` needs no change (analyst-1, 2026-09-16). The `interrupted`
  marking lives in `Coordinator`'s constructor, reachable only from
  `startServer` ← `wire.on("apply")`, and the host sends `apply` exactly once
  per node start (`cartridge.ctg/src/host/process.rs:207-224`). An attach
  constructs nothing itself — except where `settle_remote`'s single
  trust-refusal `reload` (`cli/host.rs:152-165` → `Host::reconcile`,
  `host/mod.rs:294-327`) starts a `waiting`/failed node, and a node start is
  exactly when the marking is meant to fire. The marking was destructive only
  because a *second live node* shared the on-disk store; deleting the spawn
  removes that. Same shape
  as the done sibling `agent-runs-key-per-attached-instance-not-per-process`,
  whose audit premise also dissolved once one daemon was the rule. The path was
  dropped from the footprint in round 1 (F1): `feet()` unions the PRD's and the
  spec's footprints, and `collect` commits every changed path in that union, so
  keeping an untouched file there would have swept a peer's 60 uncommitted lines
  into this PRD's receipt. A later slice brings its own spec and its own
  footprint.
- `live/main.ts:9` hardcodes credential paths under cartridge.ctg — note it
  here; fix only if it blocks attach.

## Open question carried from the parent

Does `launch` keep its agent process and tmux window while its proxy listener
stays in the daemon, with the agent pointed at the daemon's proxy address?
The answer belongs here.

**Answered 2026-09-16 (analyst-1): yes, and it is already the shipped
behaviour.** `host::launch` attaches, asks the daemon's `proxy` cartridge for
`{"op":"launch",…}`, and proxy answers from its own bound listener —
`let (base, key) = proxy.front…; args["base"] = json!(base)`
(`proxy.ctg/src/lib.rs:394-403`) — which router renders the agent command
around. The CLI then runs that command in the launching process, foreground,
`kill_on_drop`, after `ignore_interrupt` so the terminal's Ctrl-C reaches the
agent (`cartridge.ctg/src/cli/host.rs:231-282`). The proxy port is bound once,
in the daemon, by composition (`.cartridge/init.lua:41-51`), so no second
design is open. Nothing in this PRD's footprint decides it; the live launcher
is the same shape one level up — Live's HTTP server stays in the daemon's live
node and `launch.ts` prints the session URL.

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1. The footprint gained
`.cartridge/tests/integration/launch.test.ts`: it is the only runnable proof
from inside live.ctg, and without it the spec has no executable Verify block.

That test is **already red at HEAD**, for a reason outside this PRD — it still
expects the `tui`/`pty` handoff that `the-profile-is-the-orchestration-service`
removed, and `just test live` runs it. The spec rewrites it rather than leaving
a second red suite behind, which also fixes a hole in the old test: its fake
`status` exited 0, so it never reached the spawn it claimed to forbid. Whoever
reviews this must confirm the rewritten test fails against unpatched
`launch.ts` — the analyst observed exit 1 with 2 failures there.

## Acceptance

- [ ] `cartridge launch claude` with a daemon running starts no `cartridge
      daemon` process and no second composition; the agent talks through the
      daemon's proxy (parent Acceptance box 2 covers the process count).
- [ ] Work in flight on the daemon is not marked `interrupted` by a new
      `launch` attaching.
- [ ] With no daemon, `launch` results in exactly one daemon being started
      (concurrent launches included).