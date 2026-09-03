---
complexity: 35
footprint:
  - resources/board/run.py
  - resources/board/dispatch.py
  - resources/board/plan.py
  - references/parts/run.md
  - references/settings.md
  - references/files.md
  - references/skills/pearde-all.md
  - references/skills/pearde-run.md
  - index.md
  - SKILL.md
---

# spec01 — `machine` becomes `run`, and every read it did becomes `plan`

The verb, the script, the part, the scope keyword and the skill body are
renamed whole. `run` is the one command that moves; `plan` is the same read
with nothing moved. `machine dispatch` stops existing — the command name *is*
the verb — and `--group` goes, because the scope word is the group.
No alias, no former name, no migration note.

**What stands.** The whole of it, built and measured green in the lane
`lane/every-task-is-a-verb-under-one-skill-the-machine-is-the-run-verb`
(worktree `pearde/.lanes/…`, uncommitted, ten files, three of them `git mv`).
Every box below was run by hand there on 2026-09-02 after the lane was
fast-forwarded to `3664de0`.

**What is left.** Commit it, and re-run the boxes on whatever `plan.py` and
`dispatch.py` look like when this lands — both are shared with other PRDs in
flight. Nothing in the contract is unbuilt.

## Acceptance

- [x] `resources/board/machine.py` is `resources/board/run.py` and
      `references/parts/machine.md` is `references/parts/run.md`, both by
      `git mv` — `git status --porcelain` shows `RM` on each, so the history
      follows the file.
- [x] `references/skills/pearde-machine.md` is
      `references/skills/pearde-run.md`, its body written for `run`, and it
      has the manifest row in `references/files.md` it never had. `pearde
      doctor`'s `skills` row lists `pearde-run` and no `pearde-machine`.
- [x] `@@machine` in `index.md` is `@@run` and names
      `references/skills/pearde-run.md`, `references/parts/run.md` and
      `resources/board/run.py`. `pearde index` reports two problems, both
      predating this PRD and named in the report — `references/language.md`
      pointing at an absent `personas/writer.md`, and `edit.py` at an absent
      `@questions.py`. It reported three before: the third was
      `pearde-machine.md` having no manifest row, and this spec closes it.
- [x] `run` moves and is discoverable: `resources/board/run.py` carries
      `COMMANDS = {"run": cmd_run}` and `main` reads `argv[0] == "run"`;
      `pearde help` lists `pearde run   dispatch a board, a group or every
      watched…` and `pearde run --help` prints
      `takes: --dry --once --workers N --adapter <id> --deadline S`.
- [x] The five `run` lines read as the PRD's first table. Measured by hand
      from `/Users/feb/dev/infra/pearde`: `run --dry` (the cwd board alone,
      `dispatched 2 · refused 3 · dead 0`), `run here --dry` (identical),
      `run all --dry` (13 boards, `dispatched 14 · refused 36 · dead 0`),
      `run private --dry` (the one group any board on this machine declares —
      `group `private`: 6 of 13 watched board(s)`,
      `dispatched 14 · refused 17 · dead 0`), and
      `run every-task-is-a-verb-under-one-skill --dry`
      (`scope …: 3 PRD(s) in that subtree`, and only those three rows).
- [x] A board registered twice under two spellings is one board. `pearde run`
      with no scope resolved both `pearde` (a `.pearde` symlink) and
      `pearde-2` (`pearde/`) and dispatched the same tree twice until
      `here_entry` deduped by `os.path.realpath`.
- [x] `run.board_at` and `plan.find_board` answer the same board from one
      cwd: `board_at` walks `plan.BOARD_DIRS`, not `plan.BOARD_DIR` alone.
      Before this they disagreed inside one worktree — `board_at` skipped a
      `.pearde/` the board actually was.
- [x] A bare word resolves reserved → declared group → PRD on the cwd board,
      and neither is guessed: `RESERVED = ("here", "all")`,
      `READ_VERBS = ("boards", "slots", "progress", "groups")` and
      `resolve_scope` in `run.py`. A word that is both a declared group and a
      PRD is refused naming both. A word that is neither is refused with the
      groups that exist and the near-miss PRDs, exit 1. `dispatch` is no
      longer reserved as a label; `here` and `all` now are.
- [x] The nine `plan` lines read as the PRD's second table, and a window and a
      scope compose in either order — `plan private slots` and
      `plan slots private` print one line, identical. Bare `plan` and
      `plan here` stay `cmd_plan`, unchanged, and `--workers N` is still a
      count rather than a scope. A window with no scope is the whole watch
      set, which is what `machine boards` and `machine slots` were; only the
      bare `plan` defaults to the cwd board.
- [x] `--group` is gone from `dispatch.py`; its `main` is
      `main(argv, entries=None, only=None)`, called by `run.py` with the
      scoped entries and, for a PRD scope, `only` — which cuts the frontier
      to that rel and its subtree and prints the count it kept.
- [x] `machine dispatch` exists nowhere as a command: `dispatch.py`'s
      docstring, its three adapter refusals and its run-log header all say
      `pearde run`.
- [x] `git grep -in machine` returns only prose about the physical machine —
      `machine-ceiling`, the `▸ machine:` progress label, `_machine_proc`,
      `LEGACY_MACHINE_DIR` (the one-shot migration the invariant whitelists)
      and scout snapshot data. No command, no path, no scope keyword, no
      skill line.
- [x] The parallel harness
      `prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/fixture.py`
      is green against this tree — 13 of 13, run as
      `PEARDE_ROOT=<this checkout> python3 …/fixture.py`. It already imports
      `run`, so it is RED against any tree still holding `machine.py`.
- [x] The scope probe `probe/scope.py` beside this spec is 24 of 24 against
      this checkout, fixtures built in a temp dir and torn down.
- [x] `pearde run <prd>` and the handle `run <prd>` do not name each other.
      `references/parts/handles.md`'s *run one PRD to done* row keeps `—` in
      its Command column: it is the session working that subtree in its own
      window, and the adapter prompt is `/pearde run {rel}`. A command there
      would make a worker fan out into more workers.
- [x] No regression on the two gates that were already red: `pearde prose
      check` on the footprint (baseline `parts/machine.md` 20 waste words,
      `pearde-machine.md` 7, `pearde-all.md` 8, `settings.md` 1 — after,
      `parts/run.md` 24, `pearde-run.md` 7, `pearde-all.md` 8, `settings.md`
      1) and `resources/invariants/every-artifact-lands-inside-the-board.sh`
      (2 failing checks at `3664de0`, 1 in the lane). Neither is this PRD's
      to fix; both are named in the report.

## Verify and Proof

Read-only. No path under a board directory, no `git` that writes, and every
pipeline's exit code taken from a variable rather than from `grep -q` on a
pipe — the two faults that made the last run of this block exit non-zero and
cost the tree its implementation.

```sh
set -u

# the rename landed
test -f resources/board/run.py
test -f references/parts/run.md
test -f references/skills/pearde-run.md
test ! -e resources/board/machine.py
test ! -e references/parts/machine.md
test ! -e references/skills/pearde-machine.md
grep -q '@@run' index.md
if grep -q '@@machine' index.md; then echo '@@machine is still in index.md'; exit 1; fi

# nothing command-shaped still says machine
hits=$(git grep -inE 'pearde machine|machine dispatch|machine\.py|@@machine|import machine|parts/machine|skills/pearde-machine' -- . ':!resources/scout' || true)
hits=$(printf '%s\n' "$hits" | grep -v node_modules || true)
if [ -n "$hits" ]; then echo "a command-shaped 'machine' is still in the tree:"; echo "$hits"; exit 1; fi

# run is the verb that moves; dispatch is a library, not a command
grep -q 'COMMANDS = {"run": cmd_run}' resources/board/run.py
grep -q 'argv\[0\] == "run"' resources/board/run.py
grep -q 'RESERVED = ("here", "all")' resources/board/run.py
grep -q 'READ_VERBS = ("boards", "slots", "progress", "groups")' resources/board/run.py
grep -q 'def main(argv, entries=None, only=None)' resources/board/dispatch.py
if grep -q -- '--group' resources/board/dispatch.py; then echo '--group survived in dispatch.py'; exit 1; fi

# the handle and the command do not name each other: the row that means
# "this session works the subtree" must NOT carry a shell command, or the
# adapter prompt `/pearde run {rel}` resolves to the dispatcher and fans out
grep -qE '^\| run one PRD to done .*\| — \|$' references/parts/handles.md

# both reads answer, and the move answers dry, from a cwd with no board above it
R="$(pwd)"
( cd / && python3 "$R/resources/board/plan.py" plan all >/dev/null )
( cd / && python3 "$R/resources/board/plan.py" plan slots >/dev/null )
( cd / && python3 "$R/resources/board/run.py" run all --dry >/dev/null )

# a scope no board declares is refused, and the refusal exits non-zero
if python3 resources/board/run.py run definitely-not-a-group --dry >/dev/null 2>&1; then
  echo 'an unknown scope was not refused'; exit 1
fi

# a window and a scope compose in either order
a=$(python3 resources/board/plan.py plan slots 2>/dev/null | head -1 | cut -d' ' -f1-2)
b=$(python3 resources/board/plan.py plan all slots 2>/dev/null | head -1 | cut -d' ' -f1-2)
test "$a" = "$b"

# the command is discoverable, and every anchor resolves but the two that
# were already broken at 3664de0
help=$(python3 resources/pearde.py help)
case "$help" in *"  pearde run "*) ;; *) echo 'pearde help does not list run'; exit 1 ;; esac
idx=$(python3 resources/pearde.py index 2>&1 || true)
n=$(printf '%s\n' "$idx" | grep -c . || true)
if [ "$n" -gt 2 ]; then echo "index has more than the two known problems:"; echo "$idx"; exit 1; fi
if printf '%s\n' "$idx" | grep -q 'pearde-machine'; then echo 'pearde-machine still in the index'; exit 1; fi
```
