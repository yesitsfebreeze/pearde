---

kind: work
level: 10
status: done
description: "`just run` still opens with `pkill -x memory`, killing every daemon, hub and `memory mcp` adapter on the machine — the exact line `stop-is-a-verb` and `clean-is-a-verb` deleted from the two recipes beside it, and redundant with the hot reload `just install` already triggers"
read_when: "running a justfile recipe, or stopping a daemon"
---

# the-machine-wide-kill-survives-in-just-run

## Do

The `run:` recipe in `justfile` is:

```
run:
    -pkill -x memory
    just install
    rm -f .memory/data/app.port
    (nohup memory daemon > .memory/daemon-run.log 2>&1 &)
    until [ -f .memory/data/app.port ] && nc -z 127.0.0.1 "$(cat .memory/data/app.port)"; do sleep 1; done
```

Every clause of it is something the record already ruled on, for the two
recipes on either side. [[stop-is-a-verb]] deleted `just kill` because a daemon
is stopped "over that root's own socket, never by signalling every process on
the machine whose name is memory"; [[clean-is-a-verb]] deleted `just clean`'s path
list because "memory computes those paths" and `MEMORY_DIR` relocates them.
[[@prd/work/memory--just-kill-matches-the-repo-path-and-a-system-daemon.md]] is the work part that
measured the selector — and `-x memory` is the narrowed selector it landed, kept
here after the recipe it was landed for was removed. Three copies of one line;
two were deleted and the third was not revisited.

What it costs is not theoretical on this machine. Read 2026-09-06: two
`memory daemon` processes serving different roots, one `memory hub`, and one
`memory mcp` adapter per live agent session. `just run` in any lane takes all of
them — and an agent's relay does not come back, because it resolves its
endpoint once and only `attach` can ask the hub to spawn a node
([[the-mcp-relay-resolves-its-endpoint-once]]).

The kill is also redundant with the step after it. `[reload] enabled` defaults
true at a 3-second poll (`src/config/src/config.rs:860-866`), so `just install`
alone hands every running daemon over to the new binary — which is the whole
mechanism [[hot-reload-fingerprints-mtime-not-content]] describes. The `pkill`
buys a cold start of one root at the price of every other root's process.

Two lines are the same guess `clean` was deleted for: `rm -f
.memory/data/app.port` and the `until` that reads it hardcode the default layout,
and the recipe's own comment admits it — "Assumes the default `.memory/data`
layout for the port file the wait reads." The comment above it also says the
killed processes are "none of them flushed", which stopped being true when
SIGTERM was wired to the guarded shutdown ([[a-signal-runs-the-guarded-flush]]).

Replace the first line with `just stop` — this root's socket, this root's
daemon — and take the port from the loaded config rather than
`.memory/data/app.port`, the same move `clean-is-a-verb` made.

## Check

`rg -n 'pkill' justfile` returns nothing; `just run` with a peer daemon serving
another root leaves that daemon alive and its `memory mcp` adapters answering;
`just run` works in a root whose `data_dir` is not `.memory/data`.

Landed 2026-09-07 in the `quality` lane: the recipe is a `#!/usr/bin/env bash`
body opening with `just stop`, and the port file is
`$(memory status | sed -n 's/^data dir  *//p')/app.port` — one read of the loaded
config, used by the `rm` and the `until`, with
`${dir:?…}` failing loudly rather than spinning on `/app.port` if the read
comes back empty. `rg -n 'pkill' justfile` returns nothing and no `.memory/data`
literal is left in the recipe; the stale "none of them flushed" comment is
gone. The peer-daemon half of the Check was not executed here — running
`just run` stops a daemon the parallel sessions on this tree share
([[lanes-not-a-shared-tree]]) — and rests on
`tests/e2e/lifecycle.rs`, which already holds that `memory stop` reaches exactly
one root's socket.
