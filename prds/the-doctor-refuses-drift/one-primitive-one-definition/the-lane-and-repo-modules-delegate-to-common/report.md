Verdict: DONE

# the-lane-and-repo-modules-delegate-to-common — implementer report (pass two)

Second pass of `probe-then-spec` on this PRD: the analyst's pass built all
seven delegations and wrote `specs/spec01.md` from them. Per
`attempt-the-build`'s second-pass row I checked the spec's own footprint
with `git status --short` and `git diff` before deciding: all seven files
are dirty in the lane, so the build **is** in the tree and step 3 was not
re-entered. Nothing in this pass was newly built; every number below is a
re-measurement, and no flip is claimed for anything this pass wrote.

## Workflow probe-then-spec

| # | step | result |
|---|------|--------|
| 1 | read-the-contract | `prd.md` body is title-only (`read-the-contract`'s "unedited template" row): the contract is `specs/spec01.md` and the analyst pass's `report.md`, read as such. `repo:` root is a lane with no board — symlinked the live board in at `<lane>/pearde` and `<lane>/.pearde` (both gitignored, `git status --short` in the lane still shows only the 7 footprint files). `git status --short` recorded in **both** roots before the first command: checkout has `.gitignore index.md references/drill.md references/files.md references/skills/pearde-drill.md resources/board/dispatch.py ?? docs/` — none in this footprint; lane has exactly the 7 footprint files and nothing else |
| 2 | capture-the-harness-baseline | Baseline **re-taken, not inherited**: the earlier build is uncommitted and the lane's `HEAD` (`1be5d2b`, the `common.py` sibling) is the pre-edit tree, so `git clone --no-hardlinks <lane> <scratch>/preedit` gave a real pre-edit baseline with no window in which the lane was half-reverted. Gate pair + 21 board harnesses measured on it |
| 3 | attempt-the-build | Not entered — second pass, build already in the tree (see above). No file was written in this pass |
| 4 | re-run-the-harnesses | Gate pair and all 21 footprint-reading harnesses re-run on the built lane. Nothing reddened; two counts moved and both moved green — see below |
| 5 | write-the-specs | No spec authored (second pass). Applied its `Fails when` table to the block that already stands: carried the earlier pass's `## Findings` forward by name, and found one box that overclaims — see **Box 1 overclaims** |

## Verify and Proof

Spec01's block, run verbatim from the lane root with `PEARDE_ROOT=<lane>`:

```
$ PEARDE_ROOT=<lane> python3 .pearde/prds/.../probe/probe_delegate.py
PASS: every checked caller contract reproduced
EXIT 0

$ python3 -c "import ast; ... for the seven ..."
all seven parse
EXIT 0
```

Beyond the block, each of the seven imported in a real interpreter (not
just parsed), `plan` first as every entry point does:
`import lanes ok / orphans ok / ramp ok / refuse ok / repos ok / shared ok
/ transitions ok`.

`refuse.py`'s no-`sys.path` policy re-proved by loading it by file from
`/tmp`: `toplevel(lane)` returns the lane root, `toplevel('/nope/nowhere')`
and `toplevel('/tmp')` return `None`, `_common()` resolves, and
`sys.path == before` is `True`. Forcing `_COMMON['mod'] = None` (a missing
or broken `common.py`) still answers through `_run` with the same three
results — the fallback is live, not decorative.

## Acceptance (spec01)

- [x] **No second git wrapper or `## <name>` regex in the seven** — checked
  by grep over all seven, not by memory. `grep -n 'subprocess.run'` returns
  exactly the two the box excepts: `ramp.py:445` (`bash ROUTE`, not git)
  and `refuse.py:215` (`_run`, kept for its `ps` call sites); `import
  subprocess` survives in those two files only. Every diff read: the seven
  are `+52/-42` and each git call site is a single `common.run_git(...)`.
  **One exception the box does not list survives — see "Box 1 overclaims".**
- [x] **The probe reproduces every listed function's success and failure
  shape** — `PASS: every checked caller contract reproduced`, exit 0, run
  in the lane. Independently re-derived by reading `common.run_git`'s body
  against each old block: `shared.git`'s process-failure text
  (`f"git {' '.join(args)}: {e}"`) and checked-exit text are byte-identical
  in `common`; `refuse.toplevel` keeps `_run`'s own `timeout=15`;
  `ramp.tracked`'s `check=True, default=""` then `if out.strip()` is exactly
  the old `returncode == 0 and stdout.strip()` gate, and the `os.walk`
  fallback below is untouched.
- [x] **No new failure against the pre-edit baseline** — `index.py check`
  pre and post are **byte-identical**, exit 1 both (the three pre-existing
  rows: `resources/common.py is on disk with no row in
  references/files.md`, and two `hotreload-test.js` rows — all three failing
  **before the first edit**, none naming this footprint). `doctor.sh` pre
  and post are 91 lines, exit 1 both; **no row's status differs** (checked
  column-wise, not by eye). Every textual diff is the two trees' own paths,
  plus `health 85 files` vs `188 files` and the statusline's `*7` — both
  properties of where the tree sits, not of the edit.

## Harnesses

All 21 board harnesses that name a footprint path or enumerate the board
(`grep -l` on the footprint spellings, plus `grep -l 'find.*verify\.sh'`);
all 21 honour `PEARDE_ROOT` (`grep -L PEARDE_ROOT` came back empty), so
both runs measured the tree named and not the checkout. **Every exit code
identical, pre and post.** Whole outputs kept under
`<scratch>/impl-lane-repo-delegate/h.pre/` and `h.post/`.

Two counts moved, both **green**:

- `every-module-finds-its-siblings-by-one-rule`: `32 modules open with the
  one rule` → `33`. This is `lanes.py` adopting the `pearde_path` header —
  the one file of the seven that had not. A gain, and the only harness
  number this edit is responsible for.
- `the-gate-runs-the-harnesses`: `4 fail` → `3 fail`, on
  `the opt-out path costs under a second more than HEAD's doctor`
  (`delta 1.38s` → `delta -1.74s`). A wall-clock threshold on a shared
  machine — noise, and it moved the safe way. `the-fixtures-meet-the-tool`
  tracks that same row second-hand (`got [2]` → `got [1]`) and its own
  tally is unchanged at `35 checks · 30 pass · 5 fail`.

Everything else differs only by temp-dir name or elapsed seconds
(`graph-probe` `7.1s` → `8.6s`, still `ok`).

## Box 1 overclaims

Box 1 says no file of the seven holds its own `## <name>` heading regex
"except `refuse.py`'s `_run` and `ramp.py`'s `route`". One does:

`resources/board/transitions.py:844`, in `cmd_retry`:

    m = re.search(r"(?ms)^## Failure\b[^\n]*\n(.*?)(?=^## |\Z)", tail)

It is a second definition of the same primitive, it is inside this PRD's
footprint, and it is in neither exception. `specs/spec01.md`'s
`## What is left` ("Nothing in this footprint") is wrong for the same
reason. I did not fix it and did not edit the box, for a reason the build
hit rather than guessed:

**`common.section` cannot serve this call site.** `cmd_retry` does not read
a section, it **excises** one — it needs `m.start()` and `m.end()` to cut
`## Failure` out of the body and re-emit the rest as `## History`.
`common.section(text, name, *, all, lines, prefix, word, ci, heading,
chomp, default)` returns bodies, never spans, and reconstructing the span
from `heading=True`'s `(h, body)` is not exact: `_H2_RE` is
`^##\s+(.*?)\s*$`, so a heading written `##  Failure ` does not come back
byte-identical and the `str.find` would silently miss. The delegation the
PRD contracts — "a one-line delegation into `common.py`" — needs
`common.py` to grow a span-returning mode, and `common.py` is not in this
spec's footprint. The sibling PRD that owns it
(`common-py-gains-a-git-runner-and-a-section-extractor`, `DONE`)
catalogued `transitions.section` and not this call site: its
`probe/probe_common.py` checks `transitions.section` only.

A follow-up is one of two, for whoever owns `common.py`:

1. give `common.section` a `span=True` mode returning `(start, end)`, then
   `cmd_retry` takes the one-line delegation the contract asks for; or
2. delegate `cmd_retry` to `resources/board/edit.py:72 section_span(body,
   heading)`, which already returns exactly that span, is public, is
   already imported here as `editlib`, and is line-anchored the same way.
   I checked the equivalence: `section_span`'s `i` is the old `m.start()`
   and its `j` is the old `m.end()` for every body a PRD file can hold.
   This closes the duplicate *in the seven* but points at `edit.py` rather
   than `common.py`, so it is the orchestrator's call, not mine.

## Findings

Carried forward from the analyst pass, each re-checked:

- **`lanes.git`'s process-level failure now raises `LaneError`** where a
  raw `OSError`/`TimeoutExpired` fell through uncaught before. Confirmed:
  `common.run_git` with `raise_as=LaneError` wraps the `except (OSError,
  TimeoutExpired)` arm too. Every caller that catches
  (`collect.py`, `session.py`, `transitions.py`) catches `LaneError`, so
  this closes a gap. Still a real, if narrow, behaviour change.
- **`orphans.board_git` shadows the new module name.** Re-read
  `orphans.py:69-81`: `common` is a local (the git common-dir path) two
  lines below the module-level `import common`. No runtime bug — `git()`
  resolves `common` in its own scope and `board_git` never refers to the
  module — but the collision is a trap for the next editor of that
  function. Reported, not renamed: a rename is outside the spec's scope.
- **`plan.py`/`prdfile.py`'s `_h2_sections`** is still the second real
  definition `transitions.section` used to call through. Outside this
  footprint; belongs to whichever PRD owns `plan.py`.
- **`repos` imported first in a fresh interpreter hits a pre-existing
  circular import** (`repos → questions → plan → silence → repos`). I
  re-checked it this pass: importing `plan` first, as every real entry
  point does, resolves it, and all seven import clean that way. Unrelated
  to this PRD — it reproduces against `HEAD`.

New this pass:

- **`repos.git` narrows its caught exception set** from
  `subprocess.SubprocessError` to `common.run_git`'s `(OSError,
  TimeoutExpired)`. Not a behaviour change in practice — `subprocess.run`
  without `check=True` raises no other `SubprocessError` subclass — but it
  is the one place the delegation is not a strict superset of the old
  `except` clause, and it is worth knowing if `repos.git` ever gains
  `check=True`.

## Health

The brief lists no file in this footprint under the health floor, and
`doctor.sh`'s `health` row is `ok` on both trees (`6 under 40`, unchanged).
Nothing moved.

## Scores

complexity: 16
blast-radius: mid
workflow: probe-then-spec
