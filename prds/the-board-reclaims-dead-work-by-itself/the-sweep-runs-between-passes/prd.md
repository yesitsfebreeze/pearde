---
state: done
origin: requested
priority: 85
complexity: 16
blast-radius: mid
workflow: probe-then-spec
---

# the sweep runs between passes

`sweep` is loop step 1 — it runs once, when a pass opens. Between passes
nothing reclaims anything, so a ghost claim survives until somebody starts a
pass, regardless of what `claim-ttl` says. The four ghosts of 2026-09-03 sat
claimed from 11:18:04 until a pass happened to open at ~12:0x; the ttl of 30m
had expired long before, and no ttl could have helped, because nothing was
running to notice.

When this is done, the sweep fires without a pass. Decide and implement one
carrier: the view daemon's own tick, or a scheduled run — `resources/board/
schedule.py` already exists — and say in the report which was chosen and what
the other would have cost.

**Needs `a-claim-names-the-process-that-holds-it`.** A sweep that runs more
often against the *mtime* rule reclaims live work faster, which is a
regression, not a fix. It must be asking the session ledger before it is
allowed to run unattended.

**Constraint.** `sweep --apply` drops uncommitted lane paths. An unattended
sweep must commit a lane before it releases the claim over it, or it turns a
cancelled worker into lost work automatically instead of manually.

## Blocked

**2026-09-03 18:03 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-the-sweep-runs-between-passes` does not land on `session/s98669`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-the-sweep-runs-between-passes` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/the-sweep-runs-between-passes`.

## Report

the-board-reclaims-dead-work-by-itself/the-sweep-runs-between-passes: session/s27323 moved under the lane — resources/board/transitions.py

spec01: exit 0
PASS  dead holder: the claim was reclaimed with no pass open — state failed
PASS  live holder: silent past claim-ttl and left held — mtime alone does not reclaim
PASS  claim naming no process: left held — unknown never reclaims
PASS  the lane worktree is gone
PASS  the worker's uncommitted edit and new file are on lane/a-held-prd
PASS  the daemon said what it committed before it removed the worktree
PASS  the swept PRD carries the ## Failure section naming the branch
PASS  the ## Failure section names the branch the sweep kept
PASS  the daemon's log line says it reclaimed with no pass open
--- daemon log (/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.iGUVrcXC5x) ---
serve: watching on http://127.0.0.1:8471 — 3 board(s)
serve: a-held-prd · claimed · claim s59069 2020-01-01 00:00 · silent 58507.9h · pid 59069 is gone — reclaiming without a pass
serve: sweep: a-held-prd uncommitted path(s) committed as f0655942a546
▸ a-held-prd: claimed → failed · done 0/1 · 0% · open 0/1 · 0% · ready 0 · blocked 1 @∞ workers · pass file owed · as sweep
serve: sweep: a-held-prd lane removed · branch lane/a-held-prd kept
PASS  SWEEP_S unset: a dead pid's claim, silent since 2020, is never ticked
PASS  a board whose tick raised is logged and the loop still swept the next one
--- isolation log (/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.Vyzzh2Ejqc) ---
serve: watching on http://127.0.0.1:8473 — 2 board(s)
serve: sweep tick on tmp.YDjlhguwOs raised PermissionError(13, 'Permission denied')
serve: a-held-prd · claimed · claim s60890 2020-01-01 00:00 · silent 58507.9h · pid 60890 is gone — reclaiming without a pass
serve: sweep: a-held-prd uncommitted path(s) committed as e3347a5d76a3
▸ a-held-prd: claimed → failed · done 0/1 · 0% · open 0/1 · 0% · ready 0 · blocked 1 @∞ workers · pass file owed · as sweep
serve: sweep: a-held-prd lane removed · branch lane/a-held-prd kept
11 passed, 0 failed
/Users/feb/dev/infra/pearde/.pearde/prds/the-board-reclaims-dead-work-by-itself/the-sweep-runs-between-passes/probe/tick.sh: line 101: 60182 Terminated: 15          env -u PEARDE_SWEEP_S PEARDE_PORT=$((PORT+1)) PEARDE_IDLE_EXIT_S=600 python3 "$SKILL/resources/board/serve.py" run "$R_OFF/pearde" > "$LOG_OFF" 2>&1
/Users/feb/dev/infra/pearde/.pearde/prds/the-board-reclaims-dead-work-by-itself/the-sweep-runs-between-passes/probe/tick.sh: line 123: 60898 Terminated: 15          PEARDE_PORT=$((PORT+2)) PEARDE_SWEEP_S=2 PEARDE_IDLE_EXIT_S=600 python3 "$SKILL/resources/board/serve.py" run "$R_BAD/pearde" "$R_OK/pearde" > "$LOG_BAD" 2>&1
