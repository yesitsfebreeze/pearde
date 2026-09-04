# the-whole-machine-is-worked-as-one-board — analyst report

Verdict: REFINE

workflow: probe-then-spec · persona: engineer (Mara Vogt) · 2026-09-02
Q1 answered on the board; the meter it asked about is now measured, built and
proven. The split below is the board's own rule, not a dodge — see Sizing.

Probe: `.pearde/prds/the-whole-machine-is-worked-as-one-board/probe/machine.py`,
uncommitted. `git status --porcelain` empty; `doctor` unchanged from the
baseline captured before the build.

## Q1 is settled, and the premise behind it was wrong

The answer was *"cant we do it dnyamically by load, so we use 80% power of the
machine"*. I measured before believing either way, because the instrument was
the whole question. Numbers in
`scratchpad/meter/RESULTS.md`, recorded as `[[260902-5c4d]]`.

| meter | measured | what "80% of the machine" then permits |
|---|---|---|
| CPU | 5 concurrent workers: mean 14.3% of 1000% available, peak 160% → **0.32 core each** | ~25 at peak cost, ~270 at mean |
| memory | session RSS 2.28 → 2.80 GiB over that burst → **104 MiB each** | ~180 |
| processes | top-level count 6 → 7, **unmoved** | no limit approached |
| latency | identical prompt: 1 concurrent **1579 ms**, 12 concurrent **mean 1646 ms** (stdev 104, spread 1482-1874) | no knee at 12 |

**+4% latency for twelve times the work.** Serial queuing would have put the
twelfth at 19.8 s; it landed at 1.9 s.

So the honest finding is that **no local meter binds at a number anyone would
choose**. A cap derived from 80% of this machine computes 25-270 workers —
the fifty-at-once the user declined, reached silently. The machine is not what
a worker consumes; the model service is, and this process cannot read it.

The caveat, stated because it bounds the claim: the latency test used trivial
agents and measures request scheduling. It does **not** prove sustained
throughput scales to twelve real pass workers running for minutes. Measuring
that means dispatching real workers across six live boards, which an analysis
may not do.

## What was built from that: a composite, and it is legible

Load's honest job is to **throttle down**, never to set the number.

```
floor    1     always make progress
ceiling  12    the highest concurrency measured to cost nothing (+4%), and the
               board's own escalation continued — 3 plain, 6 master, 12 machine
between        (0.80 × cores − load1) ÷ 0.32,  and the same against memory
```

Proven live at both ends, and graded in between:

```
idle          12 slots (at the ceiling, ceiling 12) · cpu 1.97 of 10 loaded,
              6.0 cores under 80% → 18 · mem 18.9 of 32 GiB used, 6.7 GiB → 66
12-core burn  t+20s load1=11.75 → 1 slots (at the floor)
              t+80s load1=27.21 → 1 slots (at the floor)
band          load 4.0→12 · 4.5→10 · 5.0→9 · 6.0→6 · 7.0→3 · 7.5→floor
```

Contract step 4 is met: the slot count **and the reading that produced it**
print on the order, every run. A cap nobody can see is a cap nobody can debug.

Two measured gotchas are in the code as comments and in the record:

- **`vm_stat` "Pages free" is not available memory.** Counting only
  free+speculative reported *31.2 of 32 GiB used* on an idle machine and drove
  the meter to its floor. Fixed by adding inactive and purgeable.
- **`load1` lags badly** — a 1-minute average. Six busy cores moved it only
  2.14 → 3.31 in 20 s, so the throttle never engaged; after the 12-core burn
  ended it read 20.58 and stayed high for minutes. A dispatcher metering on it
  stays throttled well after the machine is free. This is a real weakness of
  the chosen instrument and belongs in the child's spec, not hidden here.

## What else the build passed through

- **Cold-directory discovery** works from `/tmp`. `cmd_ensure` dies with no
  board above the cwd, but that is correct: a cold daemon watches nothing, so
  ensuring from a boardless directory buys an empty watch set and a stray
  process. No daemon and no board is honestly "nothing to work".
- **The `all` row is in `/status` with `path: None`** and must be skipped.
- **No double count** — the master is watched beside its four members; dropping
  rows carrying a `board` leaves the master only its own.
- **Ordering needs no new arithmetic** — `compute_plan` per board, interleaved
  on its own schedule start.
- **In-flight rows must be excluded.** `compute_plan` runs `dispatchable` over
  `open`/`specced` only, because for one board a `claimed` PRD is in flight
  rather than refused; across the machine that is a double-book. Before the fix
  a claimed PRD sat in a wave.
- **Cross-board `needs` stay held, correctly**, exactly as on their own boards.

## The symlink overlap, built and proven

Fixture built at run time (two git repos, one's `skills/` a symlink to the
other's `src/`), each PRD naming the same real file by a different relative path:

```
raw  A ['src/skill.md']  B ['skills/skill.md']  → plan.overlap(...) = False
real both → …/repoA/src/skill.md                → clash, serialised
wave 1 ['@repoA/edit-the-skill']   wave 2 ['@repoB/edit-the-skill-too']
```

Two things had to be undone: `plan.qualify_paths` leaves a plain board's own
footprints **bare**, so two boards' `resources/x.py` would compare equal; and
comparison must be `realpath` against the PRD's **code** root, since a string
cannot see a symlink.

## Findings — outside this PRD's scope, not fixed here

**1 · `repo_root` stops at a board that is a git worktree.** It walks up testing
`os.path.exists(d/".git")`; a worktree writes `.git` as a *file*, so the walk
stops at the board.

```
repo_root('/Users/feb/dev/infra/pearde/.pearde') → …/.pearde   (should be the repo)
  all 8 footprint paths of one PRD: exists = False
  newest_mtime(...)                             → 0.0
repo_root('/Users/feb/dev/dotfiles/.pearde')    → /Users/feb/dev/dotfiles  (correct)
```

Affects `silent_of` (claim staleness) and `collect`'s commit union. This board
alone. Recorded as `[[260902-b1f6]]`; the probe walks from the board's parent.

**2 · Two dead scratchpad boards** (`rampdemo`, `proj`) are in the watch set,
pointing at other sessions' temp directories. `serve reap` exists; nothing runs it.

**3 · Four of ten watched boards contribute nothing** — the header saying
"6 boards" while `boards` says 10 reads as a discrepancy; the order should name
the silent ones.

**4 · One pre-existing red row, untouched:** `index broken` —
`resources/board/edit.py references @questions.py — not on disk`. The
`knowledge broken` row that was red at baseline went green when this pass
wrote its two notes.

**5 · A grammar word I needed and could not find.** One round of concurrent
dispatch across the machine has no term; I used *wave*. Not coined here — a row
is written from use, and this is one run.

## Sizing — why this is REFINE and not SPECCED

What is left, given the probe stands:

| unit | left to do | complexity |
|---|---|---|
| the script's placement, imports, manifest row, harness | frontier + footprint logic proven | 10 |
| the slot meter | built and proven; left: portability, settings keys, harness | 8 |
| skill, parts doc, and the four wiring points | nothing built | 10 |
| the parallel dispatch loop | **nothing built** | 14 |

**42 — above this board's `split-above` of 40**, so the brief's rule makes this
REFINE. The rule and the sense agree here: the first three are read-only and
carry no risk at all, while the fourth *moves ten boards' state*. Splitting
lets the safe half land and be used — printing the order is itself the
deliverable the user asked for — while the half that dispatches gets its own
analysis and its own blast-radius.

## What already stands, for the children

`probe/machine.py` runs steps 1-4 of the contract against ten real boards:
ensure, `/status`, merge, order, real-path clash, slot meter, printed order,
and one merged progress line —

```
machine: 10 boards · done 563/634 · 86% · derived 211/241 · open 88/889 · 10%
· ready 46 · blocked 4 · collect 3 @12 workers · as engineer
```

Step 5, the dispatch, is deliberately unbuilt: dispatching real pass workers
across six live boards would move other people's work as a side effect of an
analysis. The waves that would drive it are built and printed.

Neither child needs `all.md`'s or `master.md`'s lines loosened — fork 1 holds.

## Split

| child | contract | needs |
|---|---|---|
| the-machine-frontier-is-one-ordered-list | Run from any directory, one command prints every watched board's PRDs as a single dependency-ordered frontier, with the concurrency it would use and the reading that produced it, and moves nothing | — |
| the-machine-frontier-is-dispatched-in-parallel | That frontier's waves are dispatched as pass workers across boards, serialised on real-path footprint clashes, claim refusals named and skipped, one progress line over the merged set | the-machine-frontier-is-one-ordered-list |
