---
state: failed
origin: requested
priority: 45
complexity: 24
blast-radius:
---

# the-lifecycle-contract-and-purge-reclaims-it

*Source: `docs/content/docs/improvements/lifecycle-contract.mdx` — the page
this PRD files; the body below is the page's own argument. The verb is
implemented in the same pass this PRD is filed: `resources/board/purge.py`
holds the one command, `references/parts/handles.md` the handle row,
`doctor.sh` the `lifecycle` row, and `references/files.md` / `index.md` the
map rows.*

**Tool:** board · **Axis:** hygiene (4 → 7) · **Pulls the score up by
~8 points**

## Why now

A board holds more than its plan: a session tree per run session, a worker
lane per claim, a watch daemon per machine, a probe fixture per harness run,
a reaped ref per swept session. Each has a lifecycle, and only half of each
half is written down. `session take` starts a tree and `reap` ends it;
`claim` cuts a lane and `sweep` is the only edge that drops one — a `retry`,
a `question` release or a worker that died leaves the worktree standing with
nothing to reclaim it later; a daemon `ensure` starts it and `IDLE_EXIT_S`
ends it; a probe makes its fixture and no trap survives a SIGKILL;
`session reap` snapshots work to `refs/pearde/reaped/<id>` and the ref
outlives the need for it forever. Measured on this board on 2026-09-03:
twenty lane worktrees whose PRD holds no claim any more, and 286 probe
fixtures under /tmp, the oldest a month old — the shutdown half of the
contract is a habit, not a mechanism.

## The change

The contract, written down per participant — one page, one table (session
tree, worker lane, daemon, probe fixture, reaped ref: start, working,
shutdown) — and the reclaim, so the contract is enforced rather than
remembered: `pearde purge`, one verb, read-only until `--apply`, over the
five leftovers a skipped shutdown leaks. The refuse rule is the page's
teeth: a board the scan reads in-flight, and every registered board, is
never touched.

## Done when

- [x] `pearde purge` with no flag writes nothing and lists every candidate
  with its class; the same run with `--apply` removes each one through the
  same remover the sweep and the reaper already run, and the second run
  lists nothing. Measured on the real run of 2026-09-03: 310 removed (302
  probe fixtures · 45 MB, oldest 33d, and 2 clean lane worktrees, branches
  kept); the follow-up run lists nothing; the 18 stale lanes that re-grew
  claims or held worker dirt were kept by the fresh read — the refuse rule
  held.
- [x] A lane whose PRD carries a live `claim:`, and any board whose session
  ledger answers alive or unknown, is absent from the list whatever its age;
  a tmp board the daemon holds a serve.json for is absent too.
- [x] A probe fixture an hour old survives every run; one 25 hours old does
  not. `reap-cap` decides how many snapshots outlive the cap, and
  `--reap-cap` overrides it for one run.
- [x] The page is wired in: `docs/content/docs/improvements/lifecycle-contract.mdx`,
  the improvements index and `meta.json` carry it; `pearde help`, the
  handles table and the map name the verb.

## Fails when

- The purge runs while the worker it would sweep is still writing. Guard:
  a claim is the working state, and every reader is the existing one —
  `plan.claim_of` for the lane, `session.liveness` for the tree, whose
  unknown answer has never been a verdict.
- A tmp board mid-probe is rmtree'd under the probe. Guard: a tmp board
  with any session row that is not provably dead is never a candidate, and
  the day gate holds a fresh fixture out of the first run.

## What stays out

No new deletion mechanism: `purge` is a schedule over removers that exist.
The daemon's idle exit, the vanished-board rule and the four destructive
commands' refusal are untouched — those are the contract's working and
start halves, and they already end the right lives.

## Failure

swept 2026-09-04 02:41 — claim impl-the-lifecy-r2 2026-09-03 21:01, silent 5.7h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/the-lifecycle-contract-and-purge-reclaims-it`, whose worktree this sweep removed — the branch is kept.
