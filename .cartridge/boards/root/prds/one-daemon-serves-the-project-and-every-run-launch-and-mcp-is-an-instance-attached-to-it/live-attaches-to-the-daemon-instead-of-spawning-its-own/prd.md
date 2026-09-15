---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/live.ctg"
capability-owner: live
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/launch.ts"
- "src/coordinator.ts"
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
- `coordinator.ts` start-up marking of in-flight tasks as `interrupted`
  applies only to the node's own startup (first composition), not to an
  attach onto a running daemon that owns live work.
- `live/main.ts:9` hardcodes credential paths under cartridge.ctg — note it
  here; fix only if it blocks attach.

## Open question carried from the parent

Does `launch` keep its agent process and tmux window while its proxy listener
stays in the daemon, with the agent pointed at the daemon's proxy address?
The answer belongs here.

## Acceptance

- [ ] `cartridge launch claude` with a daemon running starts no `cartridge
      daemon` process and no second composition; the agent talks through the
      daemon's proxy (parent Acceptance box 2 covers the process count).
- [ ] Work in flight on the daemon is not marked `interrupted` by a new
      `launch` attaching.
- [ ] With no daemon, `launch` results in exactly one daemon being started
      (concurrent launches included).