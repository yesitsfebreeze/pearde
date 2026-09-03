---
memo: the-board-s-prefix-inside-its-own-repo-is-the-empty-string
kind: decision     # decision | note | invariant
status: decided    # open | decided | superseded
tags:
  - memo
  - kind/decision
  - status/decided
subject: on a board that is its own git repo the board's prefix is the empty string, and one function reads it
date: 2026-09-03
prds:
  - board-rel-is-a-third-wrong-board-path-resolution
---
<!-- Unlike a prd.md, a memo's keys are a CLOSED set: an undeclared key is a
     typo and @resources/doctor.sh fails on it. @references/memo.md is the
     format. -->

# the-board-s-prefix-inside-its-own-repo-is-the-empty-string — a prefix of nothing is not "."

## Decision

`sort_paths` asks one question of every dirty path in the board's repo: is
this path under the board, and if so what is it called there? The answer is a
prefix, and on a board that **is** its own git repo that prefix is the **empty
string** — every path that repo prints is already under the board, spelled as
it stands. On the flat layout, where the board sits inside the code repo, it
is the board's directory name.

`board_prefix(board, board_root)` computes it by comparing the two absolute
paths, and `under_board(path, board_rel)` is the only function that reads it.
Both readers go through `under_board`:

- `scratch`, which drops the board's machine-local dotfiles;
- the rider sweep, which carries the board's own edits into this PRD's commit.

Neither may do the arithmetic itself. `inside(path, [prefix])` plus
`path[len(prefix) + 1:]` is correct only while the prefix is non-empty, and
wrong in two different ways the moment it is not.

The `scratch` drop is subject to a claim. A dotfile a `footprint:` names, a
`--widen` path, or anything under the PRD's own folder is committed like any
other file — somebody said out loud that it is theirs.

## Why

`board_rel` was `os.path.relpath(board, board_root)`. When those two name one
directory `relpath` answers `"."`, and `"."` is a prefix of no path git ever
prints: `inside(path, ["."])` is False for every one of them. So both readers
went dead at once, silently, on the layout this repo itself runs.

Measured on this board on 2026-09-02: 543 dirty paths in the board's repo, **0**
recognised as under the board. Every one was reported `inherited, not added`.
A worker's memo, its workflow edit, the report it wrote beside its build —
committed nowhere, left dirty on the board branch for ever. And 6 machine-local
`.state/` files were listed in that same block, as if a person had to decide
about them.

This is the **third** wrong resolution of a board path, after the two
@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md replaced. All
three had the same shape — a board path decided by string arithmetic against a
prefix — and all three failed only on the nested layout, which is the one this
repo runs. That is why the answer here is a named function rather than a fixed
expression: a fourth caller doing it inline is the same bug again.

The two halves have to move together, and the fix has a trap on each side.
Correct the prefix and leave `scratch`'s slicing alone and it chops the first
character off every name. Correct both and leave the `scratch` skip unguarded
and a `footprint:` naming `pearde/.gitignore` is dropped in silence — measured,
that took `a-board-s-own-file-commits-in-the-board-repo` from 12 PASS to 2 FAIL
in the middle of the build. The guard is not decoration; it is the reason that
invariant was green before, by accident, and is green now on purpose.

## Alternatives considered

**Keep `relpath` and special-case `"."` at each reader.** Two call sites today,
and the next one is written by somebody who does not know. It is the shape that
produced three bugs already.

**Make `inside()` treat `""` as "every path".** One line, and it changes a
function four other branches of `sort_paths` call with a footprint union. A
`union` that ever went empty would then match everything and the collect would
stage the tree. The empty prefix is a fact about the board, not about `inside`.

**Absolute paths everywhere, no prefix at all.** Honest, and a much wider
change: `dirty_paths`, `predates`, `new_hunks`, the plan's `add`/`inherited`
lists and every message a person reads are all repo-relative today. Worth
doing, worth its own contract, and not worth doing while a resolver is wrong.

**Leave the sweep off and require `owe()` for every board file.** That is
what the bug amounted to, so it is the option of doing nothing. It means a
worker must remember to register each memo it writes, and a forgotten one is
invisible: nothing prints, nothing fails, the file simply never lands.

## Consequences

- A worker writes a memo, a workflow file or a report beside its build and the
  collect commits it, on both layouts. It no longer has to know which layout it
  is on, and neither does a spec author.
- Board dirt that predates the claim is still inherited, so the sweep does not
  carry the board's 543 standing dirty paths into whichever PRD lands next.
  `predates` against the claim's snapshot is what holds that line; a claim
  taken on a board with no snapshot falls back to mtime, as it always did.
- A machine-local dotfile is now dropped rather than listed. The
  `inherited, not added` block on a board that is its own repo gets shorter
  and means something again.
- `--widen` and a `footprint:` both beat the dotfile rule. A spec that wants
  the board's `.gitignore` says so and gets it.
- @references/parts/commits.md carries all of this in prose, so the
  expectation is readable before the merge rather than after it.
- The regression is caught by this PRD's own probe, 24 rows over both layouts,
  rather than by a script under `resources/invariants/`. Promoting it there
  would give it a row in the manifest and a place in `memo verify`; it was not
  done here because the probe already runs in doctor's harness census and a
  second copy of the same fixture is a second thing to keep true.
