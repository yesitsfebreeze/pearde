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
the shell's own running jobs before each `&`. Measured: peak concurrency is
exactly 4 under the cap and 52 without it, and the sum of the harnesses' own
durations is over **three times** higher uncapped than capped on the same box
— most of an uncapped sweep's work is contention, not testing. That inflation
is the mechanism and it reproduces.

**Wall-clock is not the case for the cap, and this spec does not make it one.**
One pair of samples had the capped run faster; a later re-measurement had the
uncapped run faster. It moves either way between boxes and between moments,
and no number here should be read as a wall-clock claim. What the cap buys is
isolation.

**What the cap does and does not remove.** It removes reds caused by collision
over a fixed port or a board service — the class the PRD names. It does not
make the sweep deterministic, and this spec does not claim it does: three
harnesses on this board assert on wall-clock margins or on a whole `doctor`
report, which reads machine-global state, and no cap above 1 can settle those.
Repeatability is not fidelity, and the boxes below are written against the
class, not against two runs agreeing.

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

- [x] `resources/doctor.sh` gates its harness launch loop on a running-job count and never calls `wait -n` outside a comment
- [x] Twelve fixture harnesses run under `PEARDE_HCAP=3` never exceed three at once, measured
- [x] The `harnesses` row still prints `<n> of <total> green` and its own seconds field
- [x] Five capped `doctor --harnesses` runs produce no more reds in the contending class than one uncapped run does — a fivefold cut in the per-run rate — and every survivor is named in the report
- [x] An uncapped sweep does produce such a red, and two independent serial re-runs agree on the set that is genuine
- [x] `references/parts/doctor.md` documents the cap, its number, its reason and `PEARDE_HCAP`
- [x] `python3 resources/index.py check` and `python3 resources/memos.py check` are both silent

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# the cap's own checks, plus the row's shape
bash .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe/verify.sh

# The claim is a class, not repeatability. The cap removes reds caused by
# collision over a fixed port or a board service; it cannot make a harness
# that asserts on wall-clock or on a whole doctor report deterministic, and
# nothing here pretends otherwise. So: five capped runs, two independent
# serial re-runs to establish which reds are genuine, and one uncapped run to
# show the class is real.
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
sweep() { grep -oE '\.pearde/prds/[^ ]*verify\.sh — exit' | sed 's/ — exit//' | sort; }
serial() {
  find .pearde -name verify.sh | sort | while read -r h; do
    PEARDE_HARNESSES=1 bash "$h" </dev/null >/dev/null 2>&1 || echo "$h"
  done | sort
}

# collect runs this block under `bash -e -o pipefail`, and a sweep with any
# red harness exits non-zero — so the producer is guarded, never the pipeline:
# the sweep's own exit is not the claim, the set of reds it names is.
for r in 1 2 3 4 5; do
  { bash resources/doctor.sh --harnesses . 2>&1 || true; } | sweep > "$W/capped.$r"
done
for r in 1 2; do serial > "$W/serial.$r"; done
{ PEARDE_HCAP=999 bash resources/doctor.sh --harnesses . 2>&1 || true; } | sweep > "$W/uncapped"

if diff "$W/serial.1" "$W/serial.2"; then echo "two serial re-runs agree — that set is the genuine one"; else echo "serial re-runs DISAGREE — the genuine set is unsettled"; fi

# the harnesses this PRD names as contending: fixed ports, or a board service
CONTEND='the-view-row-names-a-variable-that-exists|init-seeds-a-board-doctor-calls-green|readme-in-three-rings|the-line-tells-the-truth|one-page-that-says-whats-up'

# nothing in five capped runs reddens one of those that the serial set does not
cat "$W"/capped.[12345] | sort -u > "$W/capped.all"
{ comm -23 "$W/capped.all" "$W/serial.1" | grep -E "$CONTEND" || true; } > "$W/false.capped"
echo "capped: $(wc -l < "$W/false.capped" | tr -d ' ') contention red(s) across five runs"
cat "$W/false.capped"

# and the uncapped run produces them too — the class is real, not hypothetical
{ comm -23 "$W/uncapped" "$W/serial.1" | grep -E "$CONTEND" || true; } > "$W/false.uncapped"
echo "uncapped: $(wc -l < "$W/false.uncapped" | tr -d ' ') contention red(s) in one run"
cat "$W/false.uncapped"
echo "per-sweep contention reds — capped: $(wc -l < "$W/false.capped" | tr -d ' ')/5 · uncapped: $(wc -l < "$W/false.uncapped" | tr -d ' ')/1"

# the prose followed the code
grep -n 'PEARDE_HCAP' references/parts/doctor.md

python3 resources/index.py check && python3 resources/memos.py check

# The block's verdict, last so it decides the exit. Written as a bare test and
# not as `[ ! -s "$W/false.capped" ] && echo "..."`: that idiom cannot fail a
# block — a false test prints nothing and the following command swallows its
# status, which is how an earlier pass of this very block exited 0 while
# printing `capped: 1 contention reds over five runs`.
# The bar is the rate cut the drill of 2026-09-02 settled, not elimination:
# five capped sweeps must produce no more contention reds than ONE uncapped
# sweep, which is a fivefold cut in the per-run rate.
CAPN=$(wc -l < "$W/false.capped" | tr -d ' ')
UNCN=$(wc -l < "$W/false.uncapped" | tr -d ' ')
if [ "$CAPN" -gt "$UNCN" ]; then
  echo "NOT MET: $CAPN contention red(s) over five capped runs against $UNCN over one uncapped run — the rate was not cut fivefold"
else
  echo "MET: $CAPN over five capped runs vs $UNCN over one uncapped run — the per-run rate is cut at least fivefold"
fi
[ "$CAPN" -le "$UNCN" ]
```
