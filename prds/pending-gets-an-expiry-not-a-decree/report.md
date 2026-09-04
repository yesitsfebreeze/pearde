Verdict: DONE

# Report — retry pass, rebuilt from spec01

## What happened to the probe's code

The brief said the tree holds the probe's uncommitted code to continue. It
does not: the lane worktree was clean at `1be5d2b`, no branch carried
`pending_expiry` anywhere, and the main checkout's `resources/knowledge.py`
had none either — the prior pass's uncommitted build died with the swept
worktree, exactly as the PRD's history warned. The prior worker's
`report.md` (verdict SPECCED, 2026-09-03 17:42) and the surviving
`probe/verify.sh` were the record, so I rebuilt the whole contract from
`spec01.md`'s `## What already stands` list, then ran the spec's verify
block against the rebuild. `probe/verify.sh` is untracked on the board
repo (`.pearde/` is not in this repo's git), so the sweep never touched it.

## Built (one commit, `b30b3a2` on the lane)

- `CONFIG["pending_expiry_days"]` default 14, `_count`-coerced; `0` keeps
  nothing because `_expired` tests `today >= expiry`.
- `cmd_enqueue` writes `expires: <today + window>`; its dedupe now skips a
  match that `_expired` (not `keep:`) so a stale duplicate never answers
  "already pending" for a live ask.
- `pending_expiry_date(meta, config)` — own `expires:`, else `date:` +
  window, so no existing row needs migrating; unreadable dates read as
  None and doctor names them rather than silently passing them.
- `archive_expired_pending(store, config)` — rename() to
  `pending/.expired/`, never a delete; called last in `cmd_query` on all
  three return paths, printing `pending: <name> expired on <date> —
  re-enqueue with knowledge.py enqueue` per file.
- `cmd_doctor`'s pending check flags only a row past its own expiry and
  still un-archived (`expired <date>` in the line); the age-only decree is
  gone from the tool and from every prose home (`references/knowledge.md`
  rule row, seed `WORKFLOW.md` loop paragraph). `keep: true` is exempt
  from both via `_expired`'s first test.
- Seed: `pending_expiry_days: 14` in `resources/board/knowledge/WORKFLOW.md`
  and a new `pending/.expired/_index.md` marker (the `sources/.absorbed/`
  convention); `init.py`'s `write_knowledge` os.walks the preset, so the
  dotfolder copies without init changes.
- `references/files.md` gains the marker row.

## Verify output

```
python3 -c "import ast; ast.parse(open('resources/knowledge.py').read())"   → AST-OK
PEARDE_ROOT=<lane> bash .pearde/prds/.../probe/verify.sh                    → 11 ok, 0 fail
PEARDE_ROOT=<main checkout> same probe                                       → 3 ok, 8 fail  (not vacuous)
python3 resources/index.py check            → common.py row + hotreload-test.js rows only (baseline per spec)
bash resources/doctor.sh                    → knowledge row broken: "graph.json is behind the files:
                                              260903-949d, 260903-cbc4"
```

The doctor knowledge row is not this footprint: 949d (21:43) and cbc4
(21:42) are another session's notes in the live `wiki/`, written around my
claim, no `relink` behind them. I touched nothing under the live
`.pearde/wiki/` — every probe fixture was a `mktemp -d` vault — and the
spec's own baseline note calls the knowledge/questions rows pre-existing.
Left as found; a `relink` is the fix and it is outside my footprint.

## Box status

spec01: 6/6 acceptance boxes ticked, each with its verify output quoted
inline, ticked as each closed.

## Health floor

None under the floor per the brief; nothing moved.

## Defects outside scope, reported not fixed

- The lane branch carried three commits before my pass — `56f7ce5`
  every-documented-command-exists, `e861cca` a-verify-block-resolves-the-board-absolutely-not-from-its-cw,
  `1be5d2b` common-py-gains-a-git-runner-and-a-section-extractor — none
  this PRD's (claims.py, common.py, doctor.sh, specs.py). They ride the
  branch into collect; whoever collects should know the lane is 29 behind
  main and carries that work.
- The prior report's `specced`-verb side effect: frontmatter on disk now
  reads `state: claimed` with a fresh claim line, so the orchestrator
  repaired it; nothing for me to do.

## Scores

complexity: 15
blast-radius: mid