---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/sessions.ctg"
capability-owner: sessions
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/lib.rs"
---

# Sessions runs once in the daemon with one buffer-id space

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies sessions as
must-exist-once: it loads its store into memory once (`lib.rs:261`), so under
two compositions the last rename wins and buffer ids come from a counter
local to each process.

## Outcome

Sessions is composed exactly once in the daemon. Buffer ids come from one
counter in that one node, so ids from different attached instances never
collide, and store renames land on the single in-memory copy.

## What changes

- With the host-attach contract in force there is one sessions node; this
  child verifies that and removes any per-process assumption left in the
  code (the in-process buffer-id counter must be the daemon's, not an
  instance's).
- If any sessions API is per-instance by design (a client's own buffer list),
  key it by attached instance inside the one node, the way the parent's
  audit prescribes.

## Acceptance

- [ ] Two attached instances calling sessions do not see each other's buffers
      unless they ask for them, and both get ids from one space (no id reused
      across instances).
- [ ] A rename made through one instance is visible through the other.
- [ ] Exactly one sessions node exists with the daemon running (covered again
      by the composed acceptance test).