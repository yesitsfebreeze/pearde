---
complexity: 4
footprint:
  - .pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe
  - .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe
---

# spec03 — the spare port is re-checked between picking it and using it

`init-seeds-a-board-doctor-calls-green`'s harness picked a free port by binding
port 0 and closing the socket before use. That is a TOCTOU, not a stale check:
the port is free at the moment it is printed and anyone may take it before the
board service binds it, which is exactly what a parallel sweep arranges. The
PRD names this as the same class as the other three and explicitly excludes it
from the stale-checks PRD.

**What already stands** — the pick is now a loop. `port_busy` (the one shared
spelling) re-checks the port immediately before it is used, and the pick is
retried up to five times; a port that answers a connect belongs to somebody
else. If five tries find nothing free the harness fails loudly rather than
proceeding with an empty `SPARE`, and because the `EXIT` trap is not armed at
that point in the file, that arm removes its own scratch directory first.

**What is left** — nothing functional. Confirm the two behaviours against the
boxes below.

Note for whoever picks this up: the window is narrowed, not closed. Nothing
short of holding the socket open until the service inherits it can close it
entirely, and the board's service takes a port number rather than a file
descriptor. Narrowing is the whole of what this spec claims, and the retry
makes a collision require two races in a row rather than one.

## Acceptance

- [x] The harness re-checks the picked port with `port_busy` before using it
- [x] A port found busy is discarded and another is picked, up to five tries
- [x] Exhausting the tries fails loudly rather than proceeding with an empty port value
- [x] That failure arm removes its own scratch directory, since the `EXIT` trap is not yet armed — the arm run, not the `rm -rf` grepped for
- [x] The harness reads green end to end, standing down where it is designed to
- [x] The harness uses the same `port_busy` spelling as its two siblings, not a second one

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# the re-check, the loud failure and the single spelling are asserted here
bash .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe/verify.sh

# the harness itself
bash .pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe/verify.sh

# and under the sweep's own environment, where it stands down
PEARDE_HARNESSES=1 bash .pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe/verify.sh

# The exhausted-tries arm's own cleanup is asserted behaviourally by the
# probe above ("...and removes its own scratch directory"), which runs the
# arm under a TMPDIR of its own and checks that directory is still empty.
# An earlier line here looked in /tmp, where `mktemp -d` on this box does not
# put anything — $TMPDIR is /var/folders/…/T — so it printed 0 whether or not
# the arm leaked, and compared that 0 to nothing. This is the leak check that
# does compare something: the harness's real TMPDIR, before against after.
# The count is taken in a TMPDIR of this block's own, so a neighbour session
# running mktemp at the same moment cannot move it — the machine-wide
# $TMPDIR count did exactly that at collect (2461 -> 2471 with nothing of
# the harness's among the ten), which is a check decided by scheduling.
LEAK="$(mktemp -d)"
BEFORE="$( { ls -d "$LEAK"/tmp.* 2>/dev/null || true; } | wc -l | tr -d ' ' )"
TMPDIR="$LEAK" bash .pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe/verify.sh >/dev/null 2>&1 || true
AFTER="$( { ls -d "$LEAK"/tmp.* 2>/dev/null || true; } | wc -l | tr -d ' ' )"
echo "scratch dirs under the harness's own TMPDIR: $BEFORE -> $AFTER"
if [ "$AFTER" -le "$BEFORE" ]; then
  echo "the harness left no scratch directory behind"
fi
rm -rf "$LEAK"
[ "$AFTER" -le "$BEFORE" ]
```
