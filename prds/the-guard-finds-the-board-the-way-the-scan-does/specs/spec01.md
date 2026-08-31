---
complexity: 15
footprint:
  - resources/guard.py
---
<!-- Add your own keys freely. Nothing outside complexity, footprint and
     workflow is read. -->

# spec01 — the guard walks up for `.pearde/`, the way `plan.py find_board` does

`resources/guard.py`'s `board_of()` walked up from `cwd` looking for a bare
`prds/` directory — the pre-move layout. Since the board moved into
`.pearde/` (`resources/board/plan.py`'s `find_board`, `BOARD_DIR = ".pearde"`),
that walk finds the wrong thing: from this repo's root it climbed straight
past `.pearde/` to an unrelated sibling directory (`/Users/feb/dev/infra/prds`,
a leftover from another project), and reported that as "the board". Every
guard decision keyed off it — the context-budget board, the dedup stamp, the
skill-tree-write refusal, `guard status`'s target `.claude/settings.json` —
was keyed off the wrong repo. Confirmed live before the fix: `guard.py check`
named `/Users/feb/dev/infra/prds` while `plan.py scan` in the same shell
correctly named `/Users/feb/dev/infra/pearde/.pearde`; `guard status` reported
`wired in /Users/feb/dev/infra/.claude/settings.json` (one level above the
real repo); and this very session's own `Edit` of `guard.py` was refused as
"a round on another board" because `board_of(cwd)` had resolved to that same
stray directory.

This unit is built and verified, not merely planned: `board_of` now walks up
for `BOARD_DIR = ".pearde"`, matching `find_board` byte-for-byte in behavior.
Everywhere `board_of`'s return value was treated as the `prds/` directory
itself (state-by-hand's PRD-name computation, the skill's-own-board write
exemption) now goes through the new `prds_dir(board)` helper instead, since
`board_of` now returns the board *root*, matching `plan.py`'s convention that
`settings.md`, `.state/round.md` and `member_dirs()` already assumed. The
stale `prds/.round.md` / `prds/settings.md` text in denial messages and
docstrings — accurate before the move, wrong after it — now reads
`.state/round.md` / `.pearde/settings.md`. `guard_status`'s own self-test
fixture (the probe `doctor`'s `guard` row and `pearde guard status` run) built
a fake foreign board out of a bare `prds/` dir; it now builds a `.pearde/` dir,
so the self-test still proves what it claims to prove under the new
discovery rule instead of silently testing nothing.

Left to finish: nothing functional. What remains is confirming this in a
fresh session once merged (the fix was necessarily built and verified from
inside this same session, which is not a substitute for a second, independent
run) and folding it into any pending guard.py edit the board has in flight
elsewhere, per `several-sessions-write-one-board`.

Out of scope, found but not touched: `resources/doctor.sh` duplicates its own
shell-side `prds/`-walking probe (lines ~250, 282, 290-311) with the same
stale assumption — already the contract of the sibling PRD
`the-doctor-checks-the-path-a-board-is-on`, not this one.

## Acceptance

- [x] `board_of()` in `resources/guard.py` walks up from a start path for a
      `.pearde/` child directory (not `prds/`) and returns that `.pearde/`
      path, mirroring `resources/board/plan.py`'s `find_board`
- [x] `python3 resources/guard.py check`, run from this repo's root, names
      `/Users/feb/dev/infra/pearde/.pearde` — the same board
      `python3 resources/board/plan.py scan` names — not any ancestor beyond it
- [x] `python3 resources/guard.py status`, run from this repo's root, reports
      `ok` and names `/Users/feb/dev/infra/pearde/.claude/settings.json` (this
      repo's own settings file, not one level up)
- [x] an `Edit`/`Write` PreToolUse probe targeting `resources/guard.py` itself,
      with `cwd` at this repo's root, is NOT refused as "a round on another
      board" (the bug that blocked this very session's own fix)
- [x] an `Edit` PreToolUse probe that changes a real `prd.md`'s `state:` line
      under `.pearde/prds/<name>/prd.md` is refused, and the refusal names
      the bare PRD directory name (e.g. `the-guard-finds-the-board-the-way-the-scan-does`)
      in its `pearde set <prd> <state>` suggestion — not `prds/<name>` and not
      the full path
- [x] no literal `prds/.round.md` or `prds/settings.md` text remains anywhere
      in `resources/guard.py`
- [x] `guard_status`'s own self-test (the second probe, proving the
      skill-tree-write refusal) still triggers a `deny` after the fix — it
      must build its foreign-board fixture as a `.pearde/` directory, not a
      `prds/` directory, or it silently stops testing anything

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 resources/guard.py check
python3 resources/board/plan.py scan | head -1
python3 resources/guard.py status

python3 - <<'PY'
import subprocess, json
# the fix that unblocked this very session
probe = json.dumps({"tool_name": "Edit", "cwd": "/Users/feb/dev/infra/pearde",
    "tool_input": {"file_path": "/Users/feb/dev/infra/pearde/resources/guard.py",
                   "old_string": "a", "new_string": "b"}})
out = subprocess.run(["python3", "resources/guard.py", "pre"], input=probe,
    capture_output=True, text=True, cwd="/Users/feb/dev/infra/pearde").stdout
assert '"deny"' not in out, out

# state-by-hand names the bare PRD dir
prd = "/Users/feb/dev/infra/pearde/.pearde/prds/the-guard-finds-the-board-the-way-the-scan-does/prd.md"
cur = next(l.rstrip("\n") for l in open(prd) if l.startswith("state:"))
probe = json.dumps({"tool_name": "Edit", "cwd": "/Users/feb/dev/infra/pearde",
    "tool_input": {"file_path": prd, "old_string": cur,
                   "new_string": "state: analyzing"}})
out = subprocess.run(["python3", "resources/guard.py", "pre"], input=probe,
    capture_output=True, text=True, cwd="/Users/feb/dev/infra/pearde").stdout
assert '"deny"' in out and "pearde set the-guard-finds-the-board-the-way-the-scan-does" in out, out
print("OK")
PY

# must be 0 — grep -c exits 1 on no match, so assert rather than run it bare
test "$(grep -c "prds/\.round\.md\|prds/settings\.md" resources/guard.py)" = 0
```
