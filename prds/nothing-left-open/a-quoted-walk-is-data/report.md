# report — nothing-left-open/a-quoted-walk-is-data

**DONE** · spec01 · 5 of 5 acceptance boxes ticked.

The predecessor's blocker resolved inside this round: the PRD named in
`needs:` — `every-probe-harness-is-re-aimed-at-the-pearde-layout` — landed
commit `878d164`, which re-aimed the three sibling probes at the `.pearde/`
layout. The wall below is now gone; everything re-verified from disk.

## What the spec asked for, and its state

| box | check | state | evidence |
|-----|-------|-------|----------|
| 1 | this PRD's probe `19 checks · 19 pass · 0 fail` | **[x]** | `a-quoted-walk-is-data -> 19 checks · 19 pass · 0 fail` |
| 2 | guard-on-is-one-command `78 · 78 · 0` | **[x]** | `the-tool-keeps-its-word/guard-on-is-one-command -> 78 checks · 78 pass · 0 fail` |
| 3 | the-skill-tree-is-guarded `41 · 41 · 0` | **[x]** | `nothing-left-open/the-skill-tree-is-guarded -> 41 checks · 41 pass · 0 fail` |
| 4 | the-loop-is-commands, count not below `60 checks` | **[x]** | `the-loop-is-commands -> 60 checks · 60 pass · 0 fail` — the loop.md length red line is gone too; no `  FAIL ` line at all |
| 5 | `guard status` reads `ok … skill tree guarded` | **[x]** | quoted below, exit 0 |

Box 5, verbatim:

```
  guard       ok      wired in /Users/feb/dev/infra/pearde/.claude/settings.json · MAX_THINKING_TOKENS=8000 · skill tree guarded
```

Repo gate: `bash resources/doctor.sh` exits 0 —
"pearde: every part this repo owns checks out."

## One defect fixed in the spec's own Verify block

The box-4 line was `echo "$out" | grep -i FAIL | grep -qv 'loop\.md is
[0-9]* lines' && bad=1`. Two false-reds in it:

1. `grep -i FAIL` also matches "failed" and "Failure" inside the loop probe's
   **ok** lines ("…and the state is failed"), so a perfectly clean run set
   `bad=1`. Fixed to the case-sensitive `  FAIL ` that is the probe's actual
   failure format (`bad() { printf '  FAIL %s\n' … }`).
2. When the grep found nothing — the clean case — the pipeline exited 1 and
   `set -e` killed the block. It is now an `if` condition, which may fail
   without ending the run.

Full block re-run after the fix: prints all five probe/status lines above,
`exit $bad` with `bad=0`, block exit 0.

## What was implemented

`resources/guard.py` already carries the spec's subject — `data_free()`,
`HEREDOC`, `RUNS_ITS_STRING`, and the `WALKS` match against `data_free(cmd)`
at the `Bash` branch — and `references/parts/guard.md` already carries the
`carried as data` row. Both landed in commit `982afde`. Neither file is in
this session's diff; nothing in the footprint needed changing.

What was broken was this PRD's **probe**, and only the probe. Two edits, both
inside `prds/nothing-left-open/a-quoted-walk-is-data/`:

1. `ROOT` was `dirname/../../../..`. That was right when the board sat at the
   repo root; `.pearde/` added a level, so it resolved to `.pearde` and every
   `$ROOT/resources/...` lookup missed. Replaced with a walk up to the nearest
   ancestor holding `resources/guard.py` — depth-independent from here on.
2. The fixture board was built at `$D/proj/prds/one/`. `board_of()` looks for
   `.pearde/`, so the fixture was not a board and the walk rule was out of
   scope for every case. Moved to `$D/proj/.pearde/prds/one/`.

With those two, the probe is `19 checks · 19 pass · 0 fail`.

## Why boxes 2-4 were blocked, and what reopened them

The three sibling probes carried the identical stale `ROOT`:

```
prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh:9
prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh:5
prds/the-board-runs-itself/the-loop-is-commands/probe/verify.sh:5
    ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
```

That repair belonged to `every-probe-harness-is-re-aimed-at-the-pearde-layout`
(this PRD's `needs:`), which landed it as commit `878d164`. Re-running all
three from disk this session, every baseline restored:

| probe | before 878d164 | now, from disk |
|-------|----------------|----------------|
| guard-on-is-one-command | `78 · 11 pass · 67 fail` | `78 checks · 78 pass · 0 fail` |
| the-skill-tree-is-guarded | `41 · 12 pass · 29 fail` | `41 checks · 41 pass · 0 fail` |
| the-loop-is-commands | `48 · 9 pass · 39 fail` | `60 checks · 60 pass · 0 fail` |

The earlier predicted residual failures — fixtures at `$d/prds`, stale
`prds/memos/...` strings, `status` exiting 2 — are all gone in the re-aimed
probes. Even `loop.md is 141 lines` resolved (loop.md landed in shape).

`resources/guard.py` is not in this session's diff at all, so no failure above
can originate here.

## The Verify block

Rewritten so it no longer depends on the caller's cwd — it walks up to the
code repo — and so its **last command is `exit $bad`**, which is 0 exactly
when all five boxes hold. It previously ended in `... | head -1`, which exits
0 unconditionally and would have reported this spec green while three boxes
were red. This session additionally fixed the box-4 grep (see above).

## Defects found, outside this footprint

| # | defect | where | state |
|---|--------|-------|-------|
| 1 | stale `ROOT` `../../../..` after the `.pearde/` move | the 3 sibling probes | **fixed** by `every-probe-harness-is-re-aimed-at-the-pearde-layout`, `878d164` |
| 2 | fixtures built at `$d/prds`, not `$d/.pearde/prds` | same 3 probes | **fixed** in the same commit |
| 3 | `guard status` exits 2 where probes expect 0/1 | `resources/guard.py` | **gone** — status now behaves; box 5 green |
| 4 | expectations still spell `prds/memos/...` | guard-on-is-one-command, the-skill-tree-is-guarded | **gone** — both probes all green |
| 5 | context-budget guard fires on *worker* sessions and denies every tool call, including writing the worker's own report | `resources/guard.py` `budget()` | **still open** — worth a PRD |

Defect 5 stopped the earlier run once mid-task. The budget rule reads the
round's context and is meant for the orchestrator loop, but it applies to an
implementer subagent working in the same cwd, and its allowlist (round file,
`loop.md`, `round.md`, board commands) does not include the worker's report
path — so a walled worker cannot report that it is walled.

## Files changed

Board repo, all inside this PRD:

- `prds/nothing-left-open/a-quoted-walk-is-data/probe/verify.sh` — ROOT walk, `.pearde/` fixture (earlier sitting)
- `prds/nothing-left-open/a-quoted-walk-is-data/specs/spec01.md` — all five boxes ticked with quoted output; box-4 grep fixed (`  FAIL ` case-sensitive, `if`-guarded so a clean run cannot exit nonzero)
- `prds/nothing-left-open/a-quoted-walk-is-data/report.md` — this file

Code repo: nothing. Not committed — the orchestrator collects.
