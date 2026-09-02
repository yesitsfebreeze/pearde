---
complexity: 9
footprint:
  - resources/doctor.sh
  - resources/invariants/every-artifact-lands-inside-the-board.sh
  - .pearde/prds/leaked-background-services-outlive-their-fixtures/probe
---

# spec03 — the run that starts them is the run that stops them

The PRD's contract is "each run stops what it started". Fifty-three harnesses
cannot each be trusted to, and most of them belong to other PRDs that this one
must not edit — so the teardown goes where the run is: the sweep in
`resources/doctor.sh`. After `wait`, the sweep calls `serve.py reap` and puts
what it stopped on the `harnesses` row. `reap` keeps every daemon watching a
board still on disk, so this is safe beside another session's sweep and safe
beside the machine's own service.

**What stands.** The `reap` call after `wait`, `HLEAK`, and the
`· <n> leaked service(s) reaped` suffix on `HDET` in `resources/doctor.sh`;
`doctor.sh` parses under `bash -n` and the row renders `1 of 1 green · 1s` on
a one-harness fixture board.

**What is left.** `resources/invariants/every-artifact-lands-inside-the-board.sh`
still drives its whole `mktemp -d` fixture with **no** `PEARDE_PORT`, so
`py init` runs `serve.py ensure` against the machine's real daemon on 8443 and
registers a throwaway board into it. It then tries to undo that with
`serve.py forget pearde-invariant-probe` — a repair after the fact, on a line
with no trap behind it, and one that misses whenever the board keys under a
different name. `.pearde/workflows/attempt-the-build.md` already names this
exact failure and its remedy: point the fixture at a dead port
(`PEARDE_PORT=1`) so no repair can connect. Measured during the probe pass,
the live daemon on 8443 was watching `rampdemo` and `manola` — two fixture
boards registered by exactly this route.

The PRD's own harness is
`.pearde/prds/leaked-background-services-outlive-their-fixtures/probe/verify.sh`
— every check scoped to a pid it started, and it is picked up by the sweep
because `doctor.sh` globs `verify.sh` and nothing else. Six when spec03 was
written; sixteen now. Section 4 reaps right after a session start and asserts
the daemon and its board survive it; section 5 asserts `--pid` refuses a value
it cannot read rather than widening to the whole machine; section 6 asserts
the grace genuinely expires, and that its shipped default is a wait a session
can outlive rather than one nothing is ever reaped under. The box below reads
the tally the probe prints, never a total written into it.

## Acceptance

- [x] `resources/doctor.sh` runs `serve.py reap` after the sweep's `wait`, and the count it stopped reaches the `harnesses` row
- [x] the `harnesses` row keeps its shape — `<n> of <total> green · <s>s` — when nothing leaked, so `.pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe/verify.sh` stays at `16 checks · 16 pass · 0 fail · 0 skip`
- [x] `resources/invariants/every-artifact-lands-inside-the-board.sh` exports `PEARDE_PORT=1` before it drives the fixture, so no command in it can reach the machine's daemon
- [x] that harness still prints seven `PASS` lines and no `FAIL` with the port dead
- [x] running that harness leaves the machine's daemon watching exactly the boards it watched before — checked by diffing `serve.py status` around the run, never by counting processes
- [x] `bash .pearde/prds/leaked-background-services-outlive-their-fixtures/probe/verify.sh` exits 0, and its own final tally parses to `checks == pass` with `fail` at zero — never a pinned total, because this probe gains checks as the contract does

## Verify and Proof

Run under `bash -e -o pipefail` — that is how `pearde collect` runs it
(`collect.py:1057`). The `status` diff is the honest scoping here: a count of
`serve.py run` on this machine is a number a neighbouring session moves, and
last pass a check that read one was red for exactly that reason.

```sh
cd /Users/feb/dev/infra/pearde
bash -n resources/doctor.sh
grep -q 'serve.py" reap' resources/doctor.sh
grep -q 'HLEAK' resources/doctor.sh
grep -qE '^export PEARDE_PORT=1|PEARDE_PORT=1' resources/invariants/every-artifact-lands-inside-the-board.sh

BEFORE="$( { python3 resources/board/serve.py status || true; } | sed -n 's/^  \([a-z0-9-]*\) .*/\1/p' | sort )"

INV="$( { bash resources/invariants/every-artifact-lands-inside-the-board.sh; } 2>&1 )"
printf '%s\n' "$INV"
[ "$(printf '%s\n' "$INV" | grep -c '^PASS')" = 7 ]
if printf '%s\n' "$INV" | grep -q '^FAIL'; then echo "the invariant harness went red"; false; fi

# an assignment inside `if` is the one form `set -e` does not abort on, so a
# red probe still prints its tally instead of vanishing at the assignment
if PROBE="$(bash .pearde/prds/leaked-background-services-outlive-their-fixtures/probe/verify.sh 2>&1)"
then PRC=0; else PRC=$?; fi
printf '%s\n' "$PROBE" | grep -E '^  FAIL|^[0-9]+ checks · ' || true
# the tally, parsed — never a literal total. This probe gains checks as the
# contract does, and a box pinned to today's number reddens on tomorrow's.
TALLY="$(printf '%s\n' "$PROBE" | grep -E '^[0-9]+ checks · ' | tail -1)"
PN=$(printf '%s' "$TALLY" | awk '{print $1}')
PP=$(printf '%s' "$TALLY" | awk '{print $4}')
PF=$(printf '%s' "$TALLY" | awk '{print $7}')
echo "probe tally: $PN checks · $PP pass · $PF fail"
[ "$PRC" = 0 ] && [ -n "$PN" ] && [ "$PN" = "$PP" ] && [ "$PF" = 0 ]

AFTER="$( { python3 resources/board/serve.py status || true; } | sed -n 's/^  \([a-z0-9-]*\) .*/\1/p' | sort )"
echo "watched before: $(printf '%s' "$BEFORE" | tr '\n' ' ')"
echo "watched after:  $(printf '%s' "$AFTER"  | tr '\n' ' ')"
[ "$BEFORE" = "$AFTER" ]
```
