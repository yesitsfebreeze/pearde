---
complexity: 12
footprint:
  - references/grammar-board.md
  - resources/grammar.py
  - references/templates/grammar.md
---

# spec01 — pearde's own words live in one file, and every read merges them

pearde's vocabulary — the rows every board shares — is held once at
`references/grammar-board.md`. `grammar.py` reads it beside the board's own
`grammar.md` and answers `list`, `show`, `brief` and `undefined` from the two
as one, a board row of the same spelling winning. `check`, `add` and `stale`
stay on the board's file: a shared row is not one board's to break, to define
twice, or to be told is unused. The template a board starts from drops the copy
and keeps `## This repo`.

**What stands.** All of it, uncommitted in the lane. `references/grammar-board.md`
holds the fourteen shipped groups, 163 terms and 20 collision rows.
`grammar.py` grew `shipped()`, `merged()` and a `read_file()` that `read()` now
calls; `check` also reports a missing or malformed shipped file, naming that
file rather than the board; `add` says on stderr when a row overrides a shared
word; `trim` is the migration verb spec02 wires into `upgrade`.
`references/templates/grammar.md` is 19 lines.

**What is left.** Nothing but landing it against the boxes below. One defect
the first pass shipped is already fixed and must not come back: `merged()` also
popped, from each table, every spelling the other table held, so a word with a
group row *and* a collision row — `state`, `pass`, `run`, seventeen of them on
this board — vanished from both. `grammar list` lost 34 of 183 rows and
`doctor` read 149. The two tables are not exclusive; the `mine` filter already
drops the shipped copy of anything the board respells, and nothing further is
popped. Box five is that regression.

## Acceptance

- [x] `references/grammar-board.md` exists, parses clean, and holds every group the old template shipped; `## This repo` is not one of them.
- [x] A board created by `grammar.py init` has a `grammar.md` under 20 lines holding `## This repo` and no shipped group.
- [x] On that board `grammar show prd` answers from the shipped file, and `grammar list` prints over 100 terms.
- [x] A board row spelling a shared term wins: after `grammar add prd ...`, `grammar show prd` prints one line, the board's.
- [x] The merge is lossless — a word carrying both a group row and a collision row keeps both, and `grammar list` on this repo's board prints 183 lines, the number `doctor` printed before the change.
- [x] `grammar check` reports a missing `references/grammar-board.md` as an incomplete install, naming that file and not the board.
- [x] The shipped file resolves through the install's symlink shape — `<skills>/<skill>/resources/grammar.py` finds `<skills>/<skill>/references/grammar-board.md`.
- [x] `python3 resources/index.py check` prints nothing it did not print at baseline.

## Verify and Proof

```sh
bash .pearde/prds/the-tree-holds-only-what-a-board-uses/a-board-s-grammar-holds-only-its-own-words/probe/probe.sh
N=$(python3 resources/grammar.py list .pearde 2>&1 | grep -c . || true)
echo "grammar list on this repo's board: $N terms"
[ "$N" = 183 ] || exit 1
python3 resources/grammar.py check .pearde
# index.py check is a repo-wide gate with four pre-existing baseline lines
# (resources/common.py, the hotreload-test.js rows, parts/commits.md) — it is
# captured and printed, and only a line naming a grammar file decides.
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E 'grammar-board|grammar\.py|templates/grammar\.md'; then exit 1; fi
```
