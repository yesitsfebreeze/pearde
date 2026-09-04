---
state: failed
origin: requested
priority: 60
complexity: 32
blast-radius: mid
workflow: probe-then-spec
---


# the documented board matches the code

The drift list from the 2026-09-03 sweep is fixed line by line — each line either changed to match the code or its code implemented, chosen per line:

- `board.md` draws settings/vision/memos/workflows under `prds/` (they are siblings).
- `plan.py` and `transitions.py` docstrings name `prds/.plan.json`, `prds/.claims`, `prds/.pass.md`, `prds/settings.md`, `prds/vision.md` (all moved).
- `commits.md` promises `commits: off` (nothing reads it).
- `order.md` and `contract.md` say blast-radius breaks ties (`compute_plan` never reads it).
- `settings.md` says pipeline caps analyst slots (only ramp/machine/init read it).
- `doctor.md` lists 14 rows for 21.
- `statusline.md` and `obsidian.md` root the vault at the board (code: project).
- `view.md` says seven views and a `/pass` route.
- `all.md` documents `/sync`.
- `plan.py` cites memo `done-counts-which-boxes.md` (absent).
- `handles.md` and `skills/pearde.md` name `master <path>`, which no module implements.
- README says `init` writes four `.gitignore` names (ten) and `unblock` lands on done (specced — already fixed).

## Done means

Each line changed or its code implemented, chosen per line; `every-documented-command-exists` (when it lands) reports zero for these.

## Needs

No gate.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 20:59 — claim impl-doc-matches 2026-09-03 12:37, silent 8.3h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/the-tree-holds-only-what-a-board-uses-the-documented-board-matches-the-code`, whose worktree this sweep removed — the branch is kept.

## Failure

swept 2026-09-04 02:41 — claim impl-nova2-the-document 2026-09-03 21:40, silent 4.7h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/the-tree-holds-only-what-a-board-uses-the-documented-board-matches-the-code`, whose worktree this sweep removed — the branch is kept.
