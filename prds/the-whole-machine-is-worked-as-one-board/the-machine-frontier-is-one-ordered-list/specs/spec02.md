---
complexity: 8
footprint:
  - resources/board/machine.py
  - references/settings.md
---

# spec02 — the slot count is derived from load, and prints its reading

How many jobs the machine would run at once is computed from what the machine
is actually doing, and the count is never printed without the numbers that
produced it. Floor 1, ceiling 12, and a load-derived value between — the answer
to the PRD's Q1, *"dynamically by load, so we use 80% power of the machine"*.
Load only ever lowers the count; the ceiling is what protects the user.

## What already stands

Built and proven live in the probe, at all three ends on one afternoon:

```
free machine   12 slots (at the ceiling, ceiling 12) · cpu 1.78 of 10 loaded …
saturated       1 slots (at the floor, ceiling 12)   · cpu 18.14 of 10 loaded, idle 0.0%
load1 stale    10 slots (load1 stale, ceiling 12)    · cpu 11.78 of 10 loaded … · busy 47% now (1.5s sample)
```

The two measured gotchas are already coded and commented: `vm_stat`'s
*"Pages free"* is not available memory — counting it alone reported 31.2 of
32 GiB used on an idle machine and pinned the meter to its floor, so free,
inactive, speculative and purgeable are summed; and `load1` lags in both
directions, which the third line above is the fix for.

## The `load1` lag, and the mitigation this build proves

`load1` is a one-minute average. Measured 2026-09-02: six busy cores moved it
2.14 → 3.31 in 20 s, so it under-reports a machine filling up; after a 12-core
burn ended it read 20.58 and stayed high for minutes, so it over-reports a
machine that is already free. Metering on it alone throttles late and recovers
late.

The mitigation built here is a **second opinion, asked only on the throttle
path**: when the load-derived count would fall to the floor and CPU is the
binding term, take a one-second instantaneous sample — `top -l 2 -n 0 -s 1`
on darwin, two reads of `/proc/stat` elsewhere — and, if the machine is
genuinely free, use that instead and say `load1 stale` in the reading. It cost
1.5 s in the run above and is not paid on a quiet machine, where the count is
already at the ceiling and nothing needs confirming.

The residual weakness stays, and belongs in the file as a comment: the
confirming sample is a one-second window, so a machine that is bursty rather
than busy can be read either way. The floor of 1 is what makes that safe —
the worst reading still makes progress.

## What is left

The linux `/proc` branch is written but has run on darwin only; it needs one
run on linux, or the fallback to the ceiling proven when both readings are
`None`. `machine-ceiling` becomes a key in `references/settings.md`.

## Acceptance

- [x] `slots()` returns `(n, reading)` and every caller prints the reading beside the count
- [x] `1 <= n <= machine-ceiling` for every reading, including one that computes negative free cores
- [x] The reading names the cpu term and the memory term with their raw numbers, not just the verdict
- [x] Available memory counts free, inactive, speculative and purgeable pages — a machine with 19 GiB of 32 in use reports about 19, never 31
- [x] When the load-derived count is at the floor and cpu is the binding term, an instantaneous sample is taken and the reading gains `busy <p>% now (<t>s sample)`
- [x] A machine whose `load1` is stale but which is measurably free returns a count above the floor and the reading says `load1 stale`
- [x] A machine that is genuinely saturated stays at the floor, and the instantaneous sample confirms it rather than lifting it
- [x] The instantaneous sample is taken only on that path — a quiet machine's `slots()` call spawns no `top` and returns in well under a second
- [x] On a non-darwin posix the numbers come from `/proc/loadavg`, `/proc/meminfo` `MemAvailable` and `/proc/stat`; `vm_stat` and `sysctl` are never called
- [x] When neither cpu nor memory can be read, the count is the ceiling and the reading says `machine unreadable, holding at the ceiling`
- [x] `machine-ceiling` is a row in `references/settings.md` with default `12`, read by `machine.py` and by nothing else; an absent or unreadable value leaves 12 standing
- [x] The `load1` lag and the one-second window of its mitigation are written as comments in the file, with the measured numbers

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 resources/board/machine.py machine slots
# the count is inside the band, on whatever the machine is doing right now
python3 -c "
import sys; sys.path.insert(0,'resources/board'); import machine as m
n,r = m.slots(); print(n, '|', r)
assert 1 <= n <= m.SLOT_CEILING, n
assert 'cpu ' in r and 'mem ' in r, r
print('ok band and reading')"
# the quiet path spawns no sampler
python3 -c "
import sys,time; sys.path.insert(0,'resources/board'); import machine as m
t=time.time(); m.slots(); print('slots took %.2fs' % (time.time()-t))"
grep -n 'machine-ceiling' references/settings.md
```
