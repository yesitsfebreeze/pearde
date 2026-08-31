# report — state dir belongs to the board

**DONE.** 1 spec, 5 of 5 acceptance boxes ticked, every one re-run by hand
against the tree as it stands. One of the five was **false** when I arrived
and is ticked only because I fixed the code under it.

## What was on disk when I started

The probe's pass one was already in the tree, uncommitted: `MACHINE_DIR`
defined once after `state_dir()`, `CALIB_PATH` and `GUARD_DIR` derived from
it, `serve.py`'s `APP_DIR = planlib.MACHINE_DIR`, and `init.py`'s literal
`".state"` workaround replaced by `planlib.STATE_DIR`. Boxes 1, 2, 3 and 4
held as written. Box 5 did not.

## The defect I found and fixed — `calib_rows()` lost the whole registry

`plan.py` had one surviving reader of the old leaked global. At HEAD, line
1329 sat *below* the `STATE_DIR` rebinding at 1296, so `os.path.join(
STATE_DIR, "serve.json")` resolved to the machine directory. Pass one removed
the rebinding and did not follow that use down:

```python
    try:
        boards = json.load(open(os.path.join(STATE_DIR, "serve.json"),
```

With `STATE_DIR == ".state"` that path is cwd-relative. There is no `.state`
at the code repo root, so the open raised, the `except (OSError, ValueError)`
swallowed it, and `boards` came back empty — silently. Proof of the shape of
the loss:

```
$ ls -d .state
ls: .state: No such file or directory
pre-fix path .state/serve.json -> FileNotFoundError -> boards=[] -> calib_rows returns 0 rows
```

Calibration would have refitted from nothing and reported `n=0` while looking
like it ran. Fixed to `os.path.join(MACHINE_DIR, "serve.json")` — the one
line I changed this session. After the fix:

```
registry rows: 9
calib_rows returned 41 done PRDs with actual:
```

This is exactly the failure mode the PRD names, inverted: the first bug merged
every board's plan into one file, this one would have emptied the calibration
that reads across every board.

## The boxes, each re-run

**Box 1 — `STATE_DIR` bound exactly once.**
```
$ grep -n "^STATE_DIR" resources/board/plan.py
61:STATE_DIR = ".state"
```

**Box 2 — `state_dir(d)` returns a path under `d` and creates it.**
```
state_dir -> /var/folders/.../tmp9lr55wj_/.state
MACHINE_DIR -> /Users/feb/dev/infra/pearde/resources/board/state
state_dir/MACHINE_DIR OK
```

**Box 3 — two boards, two plans, nothing shared.** Two fresh boards built with
`init.py init`, one PRD each, `plan.py plan` run on both:
```
$ cat bA/.pearde/.state/plan.json     $ cat bB/.pearde/.state/plan.json
{"after": {"only-bA": []}, ...        {"after": {"only-bB": []}, ...
 "schedule": {"only-bA": {...}}}       "schedule": {"only-bB": {...}}}
$ ls resources/board/state/
calibration.json  guard  serve.json  serve.log
```
Two separate files, no shared PRD name, and no `plan.json` in the machine
directory. Neither temp board was written into `serve.json` — the registry
still holds the same 9 rows it held before. Both temp boards were removed
after the check.

**Box 4 — `init.py` names the planner's constant.**
```
$ grep -n '".state"' resources/board/init.py        # exit 1 — no literal left
$ grep -n 'planlib.STATE_DIR' resources/board/init.py
139:                 planlib.STATE_DIR):
$ grep -n "reassigns\|1296\|out of scope here" resources/board/init.py   # exit 1
```
The comment that named this bug is gone with the fix, as the spec requires.

**Box 5 — the machine-scoped corner is unmoved.** Current values against what
they were at HEAD, identical in every case:
```
CALIB_PATH  /Users/feb/dev/infra/pearde/resources/board/state/calibration.json
GUARD_DIR   /Users/feb/dev/infra/pearde/resources/board/state/guard
APP_DIR     /Users/feb/dev/infra/pearde/resources/board/state
REG_PATH    /Users/feb/dev/infra/pearde/resources/board/state/serve.json
LOG_PATH    /Users/feb/dev/infra/pearde/resources/board/state/serve.log
```
`PEARDE_GUARD_STATE` still redirects both readers:
```
plan.GUARD_DIR -> /var/folders/.../tmp.cJ5aRlMHfT
guard.STATE    -> /var/folders/.../tmp.ckOoLE8fr9
```
and the default with no env is still `resources/board/state/guard`.
`.gitignore:5` still reads `resources/board/state/`. Ticked only after the
`calib_rows` fix above — before it, `serve.json` was not resolving there.

Per the orchestrator's note on the two contradicting PRDs: `resources/board/
state/` is live and untouched. Only `plan.json` left it, which it had already
done; the directory still holds `calibration.json`, `guard/`, `serve.json`
and `serve.log`.

## The verify block

The spec's `## Verify and Proof` block ran green end to end, ending on its
explicit `echo` so `collect` reads exit 0:

```
61:STATE_DIR = ".state"
state_dir/MACHINE_DIR OK
STATE_DIR joins are board files only: ['history.jsonl', 'round.md', 'transitions.jsonl']
serve.json/serve.log machine-scoped OK
init.py: no literal .state left
machine dir still gitignored
PEARDE_GUARD_STATE still overrides both
verify-ok
LAST-EXIT=0
```

I extended the block — I did not change the contract. As the analyst wrote it,
nothing in it would have caught the `calib_rows` regression: it asserted
`CALIB_PATH` and `GUARD_DIR` start with `MACHINE_DIR` but said nothing about
the third machine-scoped file. The added assertion enumerates *every*
`os.path.join(STATE_DIR, ...)` in `plan.py` and requires the set to be exactly
the three board journals, so any future machine-scoped file joined onto the
board name fails the spec instead of failing silently. Confirmed it bites:

```
with the pre-fix line, STATE_DIR joins would be:
['history.jsonl', 'round.md', 'serve.json', 'transitions.jsonl']   -> assertion fails
```

The block also now asserts `serve.py`'s three paths against `MACHINE_DIR`, the
`PEARDE_GUARD_STATE` override on both readers, and the `.gitignore` line — the
three claims box 5 makes that nothing was previously executing.

## Defects outside this footprint — reported, not fixed

Both are in `resources/doctor.sh`, which is out of my footprint and is being
edited by another worker in the tree right now. Neither is caused by this
change: `guard.py` imports nothing from `plan.py`, `serve.py` or `init.py`.

1. **`doctor`'s `guard` row reports broken on a healthy guard.** Line 250
   walks up for `$d/prds` — the pre-rename layout. From this repo that walk
   passes `/Users/feb/dev/infra/pearde` (whose board is `.pearde/prds`) and
   lands on a stray `/Users/feb/dev/infra/prds`, so the probe runs with the
   wrong `cwd` and the guard correctly declines to deny. Run at the repo root
   the same probe denies:
   ```
   $ echo '{"tool_name":"Bash","tool_input":{"command":"find prds -name prd.md"},
            "cwd":"/Users/feb/dev/infra/pearde"}' | python3 resources/guard.py pre
   {"hookSpecificOutput": {... "permissionDecision": "deny" ...}}
   ```
   This is the territory of `the-guard-finds-the-board-the-way-the-scan-does`,
   which fixed the same walk elsewhere and did not reach line 250.

2. **`doctor`'s `plan` row reads a path that has never existed.** Line 610
   reads `"$BOARD/.plan.json"`, so the row says "no plan on record" while
   `.pearde/.state/plan.json` is on disk and fresh. It should read
   `$BOARD/.state/plan.json` — and with `$BOARD` being `.pearde/prds`, the
   board-vs-prds level needs settling in the same edit.

## Files changed

- `resources/board/plan.py` — one line, `calib_rows()`'s `serve.json` path.
  The rest of this file's diff is pass one plus two other PRDs' in-flight work
  (`dispatchable`'s `holder` parameter, `cmd_example`'s board dir); untouched.
- `resources/board/serve.py`, `resources/board/init.py` — pass one as found,
  verified, unchanged by me.
- `.pearde/prds/state-dir-belongs-to-the-board/specs/spec01.md` — verify block
  extended as described above.

Nothing committed. `resources/board/state/` intact. No other PRD touched.
