---
complexity: 8
footprint:
  - resources/doctor.sh
  - references/parts/doctor.md
  - .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe
---

# spec01 — the sweep runs a few at a time, and says so in prose

`doctor --harnesses` launched every harness at once with a bare `&` per
iteration and one bulk `wait`. This unit caps the number running at any moment
so a red from the sweep is a fault rather than a collision, keeping the row's
existing shape and its printed line.

**What already stands** — the code is written and demonstrated. `resources/doctor.sh`
now sets `HCAP="${PEARDE_HCAP:-4}"` and gates the launch loop on the count of
the shell's own running jobs before each `&`. Measured: two consecutive sweeps
returned identical failure sets, that set equalled a full serial re-run, and
wall-clock was 80s against the 84s uncapped baseline — the cap costs nothing.
Failures fell from 8 to 1, and the 1 is genuine.

**Why the cap is polled and not `wait -n`.** The comment this replaced promised
a `wait -n` cap. `wait -n` arrived in bash 4.3; `/bin/bash` on macOS is 3.2.57
and this script's shebang is `#!/bin/bash`, so `wait -n` exits 2 with
`invalid option` here. Polling `jobs -r` is the portable equivalent and holds
the cap exactly — recorded as `[[260902-e933]]` in the knowledge base.

**Why 4.** Above the number of harnesses that contend for a fixed port or a
board service at any one moment, and far below the box's core count, so no
harness waiting on a socket with a timeout is starved of CPU. Raising it trades
trust for wall-clock; lowering it buys no more trust, only time.

**What is left** — `references/parts/doctor.md`'s `harnesses` bullets (around
lines 79-92) describe the row without mentioning that it now runs a few at a
time or why. Add one bullet: the cap, the number, the reason a red from an
uncapped sweep was not evidence, and `PEARDE_HCAP` as the override for an
experiment. No `settings.md` key is added — the PRD asks for a number, not a
new contract surface.

## Acceptance

- [ ] `resources/doctor.sh` gates its harness launch loop on a running-job count and never calls `wait -n` outside a comment
- [ ] Twelve fixture harnesses run under `PEARDE_HCAP=3` never exceed three at once, measured
- [ ] The `harnesses` row still prints `<n> of <total> green` and its own seconds field
- [ ] Two consecutive `doctor --harnesses` runs return the same set of failing harnesses
- [ ] That set equals the set a serial re-run of every harness returns
- [ ] `references/parts/doctor.md` documents the cap, its number, its reason and `PEARDE_HCAP`
- [ ] `python3 resources/index.py check` and `python3 resources/memos.py check` are both silent

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# the cap's own checks, plus the row's shape
bash .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe/verify.sh

# determinism: two sweeps in a row must name the same failures
for r in A B; do
  bash resources/doctor.sh --harnesses . 2>&1 \
    | grep -oE '\.pearde/prds/[^ ]*verify\.sh — exit' | sed 's/ — exit//' | sort > "/tmp/sweep.$r"
done
diff /tmp/sweep.A /tmp/sweep.B && echo "capped sweep is deterministic"

# and that set must equal a serial re-run's
find .pearde -name verify.sh | sort | while read -r h; do
  PEARDE_HARNESSES=1 bash "$h" </dev/null >/dev/null 2>&1 || echo "$h"
done | sort > /tmp/sweep.serial
diff /tmp/sweep.A /tmp/sweep.serial && echo "capped sweep == serial re-run"

# the prose followed the code
grep -n 'PEARDE_HCAP' references/parts/doctor.md

python3 resources/index.py check && python3 resources/memos.py check
```
