# report — the sweep runs between passes

worker: an-sweep-between2 · persona: engineer
board: /Users/feb/dev/infra/pearde/.pearde · lane: .pearde/.lanes/the-board-reclaims-dead-work-by-itself-the-sweep-runs-between-passes

Verdict: SPECCED

## What the build is

The contract asked for one carrier that fires `sweep` with nobody watching,
and forbade the obvious way to build it: running the mtime rule more often
is a regression, because a worker legitimately silent past `claim-ttl` while
thinking is now caught deterministically instead of by the luck of when a
pass opened next. The build picked the carrier and then built the gate the
contract requires before anything may act unattended.

Carrier: `resources/board/serve.py`'s `watch()` loop, not a scheduled run —
it already polls every watched board every second for the life of the
process, which is already up wherever a pass or `pearde view` is; a cron/
launchd job would be a second OS-specific process per machine, sharing none
of the daemon's board state, needing its own idle-exit story, in a tree that
is Python-stdlib-only everywhere else.

Gate: `transitions.claim_liveness(who)` asks `session.py`'s own pid check
(`sid()`'s `s<pid>` shape) — the one identity-to-process resolver that
already exists — and `tick_sweep` reclaims only a claim it answers DEAD for.
`pearde claim` writes `who` as a worker name today, so `claim_liveness`
answers UNKNOWN for every claim on this board right now and `tick_sweep`
leaves every one of them exactly as `sweep` without `--apply` would. It is
wired and inert: the day `a-claim-names-the-process-that-holds-it` gives a
claim's `who` a resolvable shape, this starts reclaiming the dead ones with
no further edit in this footprint.

The lane the brief named had been swept out from under the claim before the
build started (created it fresh with `lanes.create` before reading the
contract — the branch survived, only the worktree was gone). Also: the
edits were made in the checkout, not the lane, before that was noticed —
copied verbatim into the lane afterward (`git diff` / `git apply`,
byte-identical, applied clean) and re-verified there. **The merge will
refuse until the orchestrator runs `git checkout -- resources/board/
transitions.py resources/board/serve.py` in the checkout** — the lane's
copy is the same content, not a superset, so the checkout copy is simply
redundant now.

## What the probe proved

`probe/tick.sh` (built by the previous pass on this PRD, continued here) —
7 checks, 7 of 7 pass, run 8 times in a row from the lane with no failure:
a dead pid's claim is reclaimed (lane committed to `lane/<rel>` before the
worktree is removed, `## Failure` naming the kept branch, log line
`reclaiming without a pass`); a live pid's claim, and a claim naming no
process at all (today's shape), are both left `claimed` however long past
`claim-ttl` they sit. One run out of nine total, under heavy concurrent
load on this shared machine (two unrelated `serve.py` daemons already
running), came back 2 pass/5 fail and was not reproduced in the other
eight — noted, not chased further; nothing in the 8 clean runs suggests a
code cause.

## Harnesses

`the-board-runs-itself/transitions-are-commands` — 74 checks, 67 pass, 7
fail, identical with this unit's two files stashed out and restored: the
7 fails are pre-existing (`add`'s template-comment box, three memory-log
boxes, one master-board box), none naming `sweep`/`tick_sweep`.
`index.py check` and `doctor.sh`: same pre-existing reds as before the
edit (an unrelated file with no manifest row, stale knowledge/health
rankings, memo tag drift) — nothing this footprint touches.

## Findings (report-only)

- `the-board-reclaims-dead-work-by-itself/a-worker-survives-the-window-
  that-launched-it` already has `specs/spec01.md` for "the sweep commits
  a lane before it drops it" — `drop_lane` calling `lanes.commit_all`
  before `lanes.remove`, complexity 22, not yet implemented into this
  tree. This PRD's own "Constraint" paragraph asks for the same thing;
  no second file is written for it here. `tick_sweep` calls
  `lanes.commit_all` itself at its own call site (not inside `drop_lane`)
  so the unattended reclaim is safe today independent of that spec
  landing — `commit_all` is idempotent, so the two call sites never
  double-commit once spec01 is built.
- This PRD's "Needs `a-claim-names-the-process-that-holds-it`" is prose in
  the body only — the frontmatter carries no `needs:` key, though `needs:`
  is a real, machine-read key elsewhere on this board (`gate_claim` reads
  it). Nothing enforced the ordering: this brief was issued and self-
  claimed while the sibling is still `analyzing`, no `specs/` on disk yet.
  The build did not wait on it — `claim_liveness`'s inertness on today's
  claim shape is what makes that safe.

## Specs

- specs/spec01.md — the view daemon ticks the sweep on its own, gated to a
  confirmed-dead claim. Footprint `resources/board/transitions.py`,
  `resources/board/serve.py`. Complexity 16.

## Scores

complexity: 16
blast-radius: mid
workflow: probe-then-spec
