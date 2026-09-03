---
complexity: 16
footprint:
  - resources/board/lanes.py
  - resources/board/orphans.py
  - resources/board/ramp.py
  - resources/board/refuse.py
  - resources/board/repos.py
  - resources/board/shared.py
  - resources/board/transitions.py
---

# spec01 — the seven modules delegate their git runner and section extractor to `common.py`

`resources/board/lanes.py`, `orphans.py`, `ramp.py`, `refuse.py`,
`repos.py`, `shared.py` and `transitions.py` each held their own copy of
one of `common.py`'s two primitives (a hand-rolled `subprocess.run(["git",
...])` wrapper, or — `transitions.py` — a hand-rolled `## <name>` section
reader). Each now calls `common.run_git` / `common.section` in one line,
keeping its own return-or-raise shape.

## What already stands

Every call site, in the lane:

- **`lanes.git(root, *args, check=True)`** → `common.run_git(root, *args,
  check=check, raise_as=LaneError)`. Reproduces the checked-failure message
  format exactly (`common.run_git`'s default is byte-for-byte what
  `lanes.git` built by hand). One behaviour change, noted under Findings:
  a process-level failure (git missing, a timeout) now also raises
  `LaneError` instead of the raw `OSError`/`TimeoutExpired` that fell
  through uncaught before — `LaneError` is what every caller of this
  module already catches (`collect.py`, `session.py`, `transitions.py`),
  so this closes a gap rather than opening one.
- **`orphans.git(repo, *args)`** → `common.run_git(repo, *args, check=True,
  default="", stdout=True, timeout=120)`. Same "" on any failure, same
  stdout on success.
- **`ramp.tracked(repo)`**'s inline `git ls-files` call →
  `common.run_git(repo, "ls-files", check=True, default="", stdout=True,
  timeout=60)`; the `os.walk` fallback below it is untouched.
- **`refuse.toplevel(path)`**'s one git call site (of `_run`'s several —
  the others run `ps`, out of `run_git`'s reach, and keep calling `_run`)
  → a lazy-loaded `common.py`, mirroring the file's own `_guard_board_of`
  pattern exactly (module already imported, else loaded from its file
  directly, never through `sys.path` — this file's docstring states it
  "leaves alone"), falling back to the original `_run` call if `common.py`
  cannot be loaded. This is the one call site that could not take the
  plain `import common` the other six use: `refuse.py`'s docstring
  documents, on the record, that it imports nothing so that a broken
  sibling module never blocks the guard `guard.py` runs on every Bash
  tool call. The lazy loader preserves that guarantee for `common.py` too.
- **`repos.git(root, *args)`** → `common.run_git(root, *args, check=True,
  default=None, stdout=True, timeout=5)`.
- **`shared.git(root, *args, check=False)`** → `common.run_git(root,
  *args, check=check, raise_as=Refused)`. Reproduces both the
  process-failure and the checked-exit message formats exactly.
- **`transitions.section(body, name)`** → `common.section(body, name,
  prefix=True, word=True, ci=False)`, replacing the call into
  `plan.py`'s (really `prdfile.py`'s) own `_h2_sections` — the first-hit,
  word-boundary-prefix match `transitions.section` always had.

`lanes.py` and `refuse.py` did not import their siblings the way the other
five already do; `lanes.py` now opens with the same two-line
`pearde_path` header (`import common` resolves the same way `plan`,
`edit`, `questions` already do in its five siblings); `refuse.py` keeps
its own no-`sys.path` policy and loads `common.py` the way it already
loads `guard.py`.

`probe/probe_delegate.py` reimplements each module's *old* subprocess/regex
code beside the new one-line call and diffs their output, success and
failure, for every function above, against a real git repo and a
non-existent path. `PEARDE_ROOT=<lane> python3
.pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/the-lane-and-repo-modules-delegate-to-common/probe/probe_delegate.py`
→ `PASS: every checked caller contract reproduced`.

`PEARDE_ROOT=<lane> python3 resources/index.py check` and `PEARDE_ROOT=<lane>
bash resources/doctor.sh` were run before and after the edit. `index.py
check`: identical output, exit 1 both times (the pre-existing
`resources/common.py is on disk with no row in references/files.md` and
two `hotreload-test.js` rows, none naming this footprint). `doctor.sh`:
identical except (a) the statusline's own dirty-file count and (b) the
`memo` row's line number inside `refuse.py`, which moved because the
lazy-loader added lines above it — the same pre-existing "no such memo on
this board" failure, same file, new line number.

## What is left

Nothing in this footprint. `resources/board/plan.py`'s own `_h2_sections`
— the second real definition `transitions.section` used to call through
— is a distinct primitive in a file outside this PRD's footprint; whether
it, too, delegates to `common.section` is for whichever PRD owns
`plan.py`/`prdfile.py`, not this one.

## Acceptance

- [x] None of the seven files defines its own `subprocess.run(["git", ...])`
  wrapper or its own `## <name>` heading regex any more, except the parts
  that are not git or not this shape: `refuse.py`'s `_run` (still used for
  its `ps` call sites) and `ramp.py`'s `route` (a `bash` subprocess, not
  git). Confirmed by reading each file's diff.
- [x] A probe reproduces, for every listed function, its old success and
  failure shape from the new one-line call. Ran
  `PEARDE_ROOT=<lane> python3 .../probe/probe_delegate.py` →
  `PASS: every checked caller contract reproduced`
- [x] `resources/index.py check` and `resources/doctor.sh` show no new
  failures against the pre-edit baseline. Diffed both before/after in the
  lane — see "What already stands" above for the two accounted-for lines.

## Verify and Proof

```sh
python3 .pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/the-lane-and-repo-modules-delegate-to-common/probe/probe_delegate.py
python3 -c "
import ast
for f in ('lanes','orphans','ramp','refuse','repos','shared','transitions'):
    ast.parse(open(f'resources/board/{f}.py').read())
print('all seven parse')
"
```
