# report — the-guard-finds-the-board-the-way-the-scan-does

Verdict: **DONE**. spec01, 7/7 boxes closed, all run from
`/Users/feb/dev/infra/pearde` (this repo's root):

- [x] `board_of()` walks for `.pearde/` — confirmed by the three checks below
      agreeing on one board.
- [x] `python3 resources/guard.py check` -> `guard: /Users/feb/dev/infra/pearde/.pearde`
- [x] `python3 resources/board/plan.py scan | head -1` ->
      `board: /Users/feb/dev/infra/pearde/.pearde . 61 PRDs . workers=1 . axis: 0 on . 20 off`
      -- same path as `guard.py check`.
- [x] `python3 resources/guard.py status` ->
      `guard ok wired in /Users/feb/dev/infra/pearde/.claude/settings.json . MAX_THINKING_TOKENS=8000 . skill tree guarded`
- [x] Edit probe on `resources/guard.py` itself (cwd = repo root): no
      `"deny"` in output -- the bug that blocked the analyst's own fix is gone.
- [x] Edit probe changing this PRD's own `state:` line: denied, reason names
      `pearde set the-guard-finds-the-board-the-way-the-scan-does <state>`
      (bare dir name, not `prds/<name>`, not the full path). Ran against the
      file's actual current line (`state: claimed`, not the spec's literal
      `state: analyzing` -- that string is no longer in the file since the PRD
      advanced past `analyzing`; substituted the live value to exercise the
      same code path).
- [x] `grep -c "prds/\.round\.md\|prds/settings\.md" resources/guard.py` -> `0`
- [x] `guard_status`'s self-test fixture builds `os.path.join(tmp, BOARD_DIR)`
      (`.pearde`, not `prds`) -- and `guard status` above returned `ok`,
      proving that self-test's deny still fires.

Repo gate (`.pearde/settings.md`'s `## Deliverable`): `resources/memos.py
check` -- clean, no output. `resources/index.py check` and `resources/doctor.sh`
both fail, but on pre-existing, out-of-footprint issues untouched by this
spec (stale skill/agent doc paths for `index.py`; doctor's own `"$d/prds"`
walk for `GSET`, already ticketed as the sibling PRD
`the-doctor-checks-the-path-a-board-is-on` -- spec01 names this exact
duplicate explicitly as out of scope). No new failures introduced by
`resources/guard.py`'s change.

## Scores

complexity: 15
blast-radius: high
workflow: none fit
