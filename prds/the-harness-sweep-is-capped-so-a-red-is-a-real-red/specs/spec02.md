---
complexity: 6
footprint:
  - .pearde/prds/the-view-row-names-a-variable-that-exists/probe
  - .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe
---

# spec02 — the view-row harness stands down on a busy port instead of leaking one

The harness that binds 8477, 8478 and 8479 was the sweep's main source of false
reds, and it made its own collisions permanent. This unit guards the three
ports and closes the leak, so the harness reports `skip` where it cannot assert
and leaves nothing listening when it exits early.

**What already stands** — all three edits are written and demonstrated.

1. **The leak.** `cleanup()` reads `SRVPID3` under `set -u` with `trap … EXIT`,
   but `SRVPID3` was first assigned two thirds of the way down the file. Any
   exit before that line died inside `cleanup`, skipped the `rm -rf` on the
   line below, and left 8477 and 8478 listening for the rest of the session —
   turning one collision into a permanent one. All three pids are now
   initialised together, before the trap is armed. Demonstrated: a truncated
   copy of the harness that exits before the third server now leaves no
   listener.
2. **The guard.** Each of the three port-bound checks is now preceded by
   `port_busy` — the same one-liner as
   `the-doctor-completes-without-a-home/probe/verify.sh:244`, not a second
   spelling — and stands down to `skip` rather than asserting against somebody
   else's socket. A stood-down check is never counted as a pass: in that mode
   it cannot fail, so counting it green would be manufactured evidence.
   Demonstrated: with 8477 held, the harness reports two skips and exits 0.
3. **The summary.** The line gained a skip count, placed *before* the fail
   count. `the-doctor-completes-without-a-home/probe/verify.sh:250` parses this
   harness's summary with a regex anchored on `· 0 fail` at end of line;
   appending the skip count would have broken that reader silently.

**What is left** — nothing functional. Confirm the three behaviours against the
boxes below, and leave the harness unpinned as its siblings are (see the
finding in the report: `doctor`'s unpinned-detector only recognises the literal
`$((PASS+FAIL))`, which no harness carrying skips can write).

## Acceptance

- [ ] All three server pids are initialised before the `EXIT` trap is armed
- [ ] An exit before the third server starts leaves no listener on 8477 or 8478
- [ ] With 8477 held by another process, the harness reports at least one skip and exits 0
- [ ] No skip is counted as a pass in the summary line
- [ ] The summary line still ends in the fail count, so `the-doctor-completes-without-a-home` still parses it
- [ ] Exactly one spelling of `port_busy` exists across the three harnesses that use it
- [ ] The harness reads green end to end on a clean box

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# the leak, the guard, the summary anchor and the single spelling are all
# asserted by this PRD's own harness
bash .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe/verify.sh

# the harness itself, on a clean box
bash .pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh

# its reader still agrees with it
bash .pearde/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh

# nothing was left listening by any of the above
for p in 8477 8478 8479; do
  (: < /dev/tcp/127.0.0.1/$p) 2>/dev/null && echo "LEAK on $p" || echo "$p free"
done
```
