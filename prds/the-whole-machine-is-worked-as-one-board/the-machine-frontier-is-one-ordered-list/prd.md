---
state: done
origin: requested
priority: 80
complexity: 28
blast-radius:
actual: 0.33h
---

# the-machine-frontier-is-one-ordered-list — Run from any directory, one command prints every watched board's PRDs as a single dependency-ordered frontier, with the concurrency it would use and the reading that produced it, and moves nothing

Run from any directory, one command prints every watched board's PRDs as a single dependency-ordered frontier, with the concurrency it would use and the reading that produced it, and moves nothing

## Report

spec01: exit 0
ok   runs from / with no board above the cwd
ok   prints a board count over the watch set
ok   prints the slot count and its reading
ok   the reading names the cpu term
ok   the reading names the memory term
ok   every row is addressed @<board>/<rel>
ok   prints at least one wave
ok   a row marked ready is in a wave
ok   no row marked ready carries a non-dispatchable state
ok   the merged progress line is one line
ok   --json parses and carries slots, rows, waves
ok   it moved nothing in this repo
ok   machine-ceiling: 0 lifts the ceiling
ok   an unlimited ceiling prints ∞, never 0
ok   an unlimited ceiling keeps the floor of 1
ok   a set machine-ceiling is honoured
ok   an absent machine-ceiling still gives 12
ok   an unparseable machine-ceiling gives 12
PASS
ok discovered
ok cold cwd
ok moved nothing

spec02: exit 0
5 slots (cpu-bound, ceiling 12) · cpu 6.15 of 10 loaded, 1.9 cores under 80% → 5 · mem 18.2 of 32 GiB used, 7.4 GiB under 80% → 72
5 | 5 slots (cpu-bound, ceiling 12) · cpu 6.15 of 10 loaded, 1.9 cores under 80% → 5 · mem 18.2 of 32 GiB used, 7.4 GiB under 80% → 72
ok band and reading
slots took 0.01s
56:| `machine-ceiling` | 12        | the highest concurrency `pearde machine` will name across every watched board. Not a limit that was found — the highest that was **measured** to cost nothing on this machine (12 at once, +4% mean latency, no knee), so it is a number to move rather than a law. `0` — like `workers` and `pipeline` — is **unlimited**: the load-derived count with the floor of 1 under it and nothing above it, printed `ceiling ∞`, never a bare `0`. `1`-`64` is that number. Absent, unparseable or out of that band leaves 12 standing, so an untouched board keeps the measured composite and only an explicit `0` lifts the cap. The floor is always 1 and load only ever lowers the count. Read by @resources/board/machine.py alone, off the board at the cwd — the command spans every board and writes to none, so the board a person is standing in is the one they addressed, and away from any board the default stands. @references/parts/machine.md |

spec03: exit 0
  skills      ok      18 well-formed · pearde-doctor pearde-drill pearde-grammar pearde-graph pearde-health pearde-knowledge pearde-machine pearde-master pearde-memo pearde-persona-ask pearde-persona-create pearde-persona pearde-report pearde-scout pearde-update pearde-view pearde-workflow pearde 
  index       ok      149 files · 36 keywords · every anchor resolves
SKILL.md:1
index.md:2
references/files.md:1
ok neither line touched
  pearde-machine missing  --dry/pearde-machine — 5 of 5 links
dirname: illegal option -- -
usage: dirname string [...]
