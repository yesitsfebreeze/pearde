# Weight and order

Three axes decide what runs next. No axis is a clock.

1. **Dependency** — `needs:` all `done`, every child `done` — a parked
   child holds its parent. A hard gate: an unready PRD is no candidate at all. The
   gates are one function, `plan.dispatchable`, read by `scan`'s ready band and
   by `claim`. A footprint overlap with a `claimed` PRD is **not** a gate —
   each worker has a git worktree of its own, so the pair is ordered below (an
   `after … (footprint)` edge) and resolved at the merge.
2. **The vision axis** — asap lanes first, then depth, then `priority`. A PRD
   declaring `axis: asap` in its frontmatter is a deliberate exception, the
   "see it working" ask, and dispatches before everything else by priority.
   On-axis PRDs dispatch deepest-first: the longest serial chain leads, because
   every hour of waiting is an hour added to the finish. `priority` breaks ties
   within a depth. A PRD off the axis dispatches after all on-axis work, by
   priority. The axis is `.pearde/vision.md`: `terminals:` names the PRDs whose
   completion is the vision, and a PRD's depth is the longest serial chain from
   the PRD to one terminal, over `needs:` alone — a `done` PRD on the
   chain costs no hop, and a parent lands after its children, so a parent named
   as a terminal puts its subtree on the axis. A live PRD reaching no terminal
   is off-axis. `edges:` orders nothing: an edge is a check on `needs:`, and an
   edge whose two ends resolve while neither PRD declares the hop is reported
   as `the vision says X needs Y; X does not` — one line in X's frontmatter
   closes it. `scan`'s first line carries `axis: <on> on · <off> off`, a line
   off the axis carries `· off-axis`, and `pearde vision` prints the whole
   axis. A board with no `terminals:` prints none of the above and orders as
   described.
3. **Complexity and blast-radius** — `complexity` 1-100 is the weight the
   progress line and `plan` use. `blast-radius` breaks ties and decides what a
   pass leads with: a `high` PRD gone wrong costs more than a late `low` one.

The analyst scores `complexity` and `blast-radius` at spec time from the specs
just written — how many units, how much is unknown, how much of the tree they
touch. The orchestrator writes both on the SPECCED transition.

### The pressure order — what a pass touches first, across the whole board

The three axes above order the PRDs that *can* run. The pressure order answers
the wider question, in one ranking written here once and read from here by both
ends:

| # | band | is |
|---|------|----|
| 0 | **to collect** | every acceptance box closed, a worker still holding the PRD. One commit, and a whole frontier can open — no dispatch is cheaper |
| 1 | **waiting on you** | `question`, `blocked`, `refine`, `failed` — the four that move only when a person moves them |
| 2 | **in flight** | a worker holds the PRD and its boxes are ticking |
| 3 | **ready now** | dispatchable this second. Inside the band, biggest door first — that ordering IS the dispatch order |
| 4 | **gated** | the rest of the plan, in schedule order |
| 5 | **parked** | `deferred` and the board's own states — weighed, scheduled by nothing |
| 6 | **landed** | `done`, laid out to the left of now |

**The cut falls between 1 and 2.** Above the cut lies what this pass can act
on; below lies what somebody already holds. Every band boundary follows from
the cut.

`plan.py scan` prints its five sections in pressure order, so a pass reads the
board already sorted, and the timeline stacks its rows the same way, so the top
of the chart and the top of the scan make the same claim. Inside a band the
three axes above break the tie — earliest start, then critical, then the weight
unblocked. Progress is a key nowhere: a bar filling as its checks land would
drag its own row up the page, and a row moving under the reader is what the
banding prevents. A PRD changes band when a state or a claim changes.

### No axis is a clock

`actual:` is a record the plan never schedules by. `est:` is a fallback: a PRD
with no `complexity` is weighed by its `est` rather than dropping to the board
average. Nothing asks an analyst to produce one, and no pass reports hours left
— wall-clock is a function of token throughput, tool latency and contention,
never a property of the work.

`workers` is no axis either. `0`, the default, is unlimited: the plan
dispatches every ready PRD the moment its edges clear, and the wall printed is
the critical path, the one bound agents cannot argue with. A number is a cap a
person set, and the plan then prints the wall that cap costs beside the peak
the fastest path asked for.

The one clock the board does show is fitted, not estimated. `plan.py
calibrate` reads every done PRD carrying an `actual:` across every registered
board and fits one machine-wide constant — hours per unit of weight, as a ratio
of sums so a five-minute PRD cannot outvote a three-day one, with a P20–P80
band from the per-PRD spread. Once fitted, every weight on the board prints as
tuned real hours: weight × the fit × `TUNE`, a hand-set margin hard-coded in
`mapfile.py` (1.618). Raise `TUNE` when the board keeps finishing late, lower it
when the board keeps beating the number.

A bad fit can mislabel an axis and can never re-order the work — precisely
because `est` and `actual` stay out of the schedule, nobody ever had reason to
game them, which is what makes them honest calibration data. Refit as `actual:`
records accumulate; the fit is dated, is per board, and lives at
`<board>/.state/calibration.json`.

The weight of one PRD, first answer wins:

1. its specs — each spec's `complexity`, or that spec's `est`, summed
2. its own `complexity`
3. its own `est`
4. the average weight of every scored PRD on the board
5. `weight-default` from `.pearde/settings.md`, when nothing is scored

A parent with live children weighs zero — the work sits in the children, and
weighing the parent too counts the same work twice. A held PRD weighs what is
LEFT of the work, floored at a twentieth.

**Compute cost belongs in the spec that spends it.** GPU seconds, API calls, a
sweep priced from cached timings: real, predictable, and a legitimate reason to
scope a spec down or refuse a cell. Such a call is a *scope* decision inside a
spec, never a *schedule* decision on a board.
