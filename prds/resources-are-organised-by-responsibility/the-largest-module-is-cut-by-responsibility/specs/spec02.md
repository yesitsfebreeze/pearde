---
complexity: 6
footprint:
  - references/files.md
  - index.md
  - references/settings.md
  - references/archive.md
  - references/parts/view.md
  - references/parts/order.md
  - references/templates/grammar.md
---

# spec02 — the map names the nine new files, and no sentence still points at the old one

`index.py check` is the gate that proves a moved file was written down. A cut
tree with no rows added scores nine problems more than the tree it was cut
from: nine new modules on disk with no row in `references/files.md`. Beside
that, five sentences in the prose name `plan.py` as the file holding something
that has moved out of it, and `cmd_calibrate` prints one more.

**What stands.** All of it — the rows, the scopes and the six claims. The gate
was re-measured on the rebased tree and names none of them.

**The inherited set is not a number.** When these specs were written the gate
printed three problems none of which was this unit's, and the box asserted the
three. It prints one in the checkout now and two in the lane — siblings closed
`references/skills/pearde-machine.md` and `edit.py`'s `@questions.py`, and the
lane adds `@pearde/memos/…` because `lanes.create` gives a lane no board, so
every reference from a tracked file into the board dangles there by
construction and closes on the merge. An equality on a board-wide count is a
wall: it fails for a reason no worker on this unit can reach. The block prints
the count and asserts the footprint instead.

Nine rows in `references/files.md`, beside the existing
`| @resources/board/plan.py | read + order the board |`, one line each:
`boards.py` where a board is on disk and how a new one is made; `prdfile.py`
one PRD file — frontmatter, boxes, typed numbers; `repos.py` the git tree
under a board and the lanes cut off it; `registry.py` the PRDs a board holds
and the boards a master merges; `silence.py` whether a held PRD is still
moving; `needs.py` what a PRD waits on; `vision.py` the axis `vision.md`
declares; `schedule.py` what may run now and in what order; `mapfile.py` the
plan on disk, the journals and the view's payload. `plan.py`'s own row becomes
the command line and the module every caller imports.

`index.md` names `resources/board/plan.py` in five `@@` scopes — `@@board`,
`@@order`, `@@view`, `@@pass` and `@@machine`. Each scope gains the modules
its subject actually lives in now: `@@board` the board resolution and the
parse, `@@order` the schedule and the axis, `@@view` the map file, `@@pass`
the map file's journals, `@@machine` the schedule.

Six claims that name the wrong file once the code has moved:

| where | says | now |
|---|---|---|
| `references/settings.md:52` | ``plan.py``'s `silent_of` is the one reader | `silence.py` |
| `references/parts/view.md:231` | `silent_of` in `@resources/board/plan.py` | `silence.py` |
| `references/archive.md:24` | `_scan_one` (`@resources/board/plan.py`) | `registry.py` |
| `references/parts/order.md:82` | hard-coded in `plan.py` (1.618) | `mapfile.py` |
| `references/templates/grammar.md:90` | `TUNE` … the hand-set margin in `plan.py` | `mapfile.py` |

`cmd_calibrate` prints the same wrong claim on stdout —
`TUNE — the hand-set margin, hard-coded in plan.py`. That line is inside
`plan.py`, spec01's file, and is corrected there rather than here, so no two
units write the same file.

## Acceptance

- [x] no line `python3 resources/index.py check` prints names any of the ten
  modules of the cut or any file in this spec's `footprint:` — every line it
  prints is a problem this unit does not own
- [x] `references/files.md` holds exactly one row for each of
  `@resources/board/boards.py`, `prdfile.py`, `repos.py`, `registry.py`,
  `silence.py`, `needs.py`, `vision.py`, `schedule.py`, `mapfile.py`
- [x] every `@@` scope in `index.md` that names `@resources/board/plan.py`
  also names at least one module the code it describes moved into
- [x] no file under `references/` says `silent_of`, `_scan_one`, `TUNE` or
  `1.618` in the same line as `plan.py`
- [x] `pearde calibrate` prints the margin's home as `mapfile.py`, not
  `plan.py`
- [x] `index.py check`'s problem count is printed beside its exit code, and no
  number is asserted — the inherited set is board-wide and every sibling that
  lands moves it

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
# index.py check is board-wide and exits non-zero on problems no unit here
# owns, so its exit is captured and never allowed to become the block's. Its
# exit still has to say the tool RAN: 0 is clean, 1 is problems, anything
# else is a crash whose empty output would otherwise pass every grep below.
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
test "$rc" -le 1
for m in boards prdfile repos registry silence needs vision schedule mapfile; do
  test "$(grep -c "@resources/board/$m.py" references/files.md)" = 1 || exit 1
done
if grep -rn 'plan\.py' references/ | grep -E 'silent_of|_scan_one|TUNE|1\.618'; then exit 1; fi
# The inherited set moves every time a sibling lands, so the count is printed
# and never asserted. What is asserted is this spec's own footprint: no line
# may name a module the cut wrote or a file this spec edits.
printf 'index.py check: %s line(s), exit %s\n' \
  "$(printf '%s\n' "$out" | grep -c . || true)" "$rc"
mine=$(printf '%s\n' "$out" | grep -cE \
  'resources/board/(boards|prdfile|repos|registry|silence|needs|vision|schedule|mapfile|plan)\.py|references/(files|settings|archive)\.md|references/parts/(view|order)\.md|references/templates/grammar\.md|^index\.md ' || true)
test "$mine" = 0
```
