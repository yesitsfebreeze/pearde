---
complexity: 8
footprint:
  - resources/knowledge.py
---

# spec01 — knowledge.py resolves the live board's wiki, from a lane as from the checkout

`knowledge.py` resolved its store from the *script*: `default_root()` returned
`Path(__file__).resolve().parent.parent / "pearde" / "wiki"`. Every other
board reader on this repo — `memos.py`, `grammar.py`, `health.py`,
`questions.py`, `workflows.py`, `plan.py` — climbs from the cwd with
`board_above` instead. A lane is a git worktree at `<board>/.lanes/<slug>`
materialised **without** the board directory on purpose
(@resources/board/lanes.py `create`: a worktree cut from a repo that tracks
its board hands every command a stale copy), so a lane holds a checkout of
`knowledge.py` and no wiki beside it. Script-relative therefore answered
`<lane>/pearde/wiki`, `Store.ensure` created it, and the query the analyst
brief tells every worker to run first — @references/parts/workers.md, `Query
the record first` — reported `0 notes on record` against a record holding 82.
Silently: no error, no warning, once per worker.

`default_root()` now takes the board above the cwd
(`memos.board_above(os.path.abspath(start or os.getcwd()))`) and falls back to
the folder beside this file only when the climb finds none — a call from
`/tmp`, a fixture, a checkout with no board. `--root` still overrides both,
and is short-circuited before the climb runs (`args.root or default_root()`),
so every explicit caller — `resources/doctor.sh:709` passes `--root
"$BOARD/wiki"` — is untouched by the change.

`memos` is imported the way `workflows.py` already imports it
(`sys.path.insert(0, dirname(abspath(__file__)))`, then `import memos`), so
the board resolver keeps one home rather than growing a seventh copy.

The module docstring said "Written for the folder this file sits beside" —
the claim the change falsifies — and is rewritten to name the rule that now
holds.

## What already stands

Built in the lane, uncommitted, in `resources/knowledge.py`: the new
`default_root(start=None)`, the `import os` / `import memos` header, and the
docstring. `pearde/prds/a-lane-s-wiki-is-a-stub-.../probe/verify.sh` is the
harness — sections A–F of it belong to this spec, section G to spec02. It
builds a clean-room fixture under `mktemp -d` at run time (a code repo whose
`/pearde` board is gitignored, one source note in its wiki, and a lane cut
with `git worktree add --no-checkout` + `sparse-checkout … '!/pearde'`), so it
touches neither the live wiki nor the checkout.

Section D is the negative control: it reconstructs the pre-fix resolver by
stripping the two `board_above` lines out of a copy of the file and requires
that copy to report `0 notes on record` and to create the stub. A box here
cannot be silently green.

## What is left

Nothing but landing it: the change is in the lane's working tree only. Whoever
implements this re-runs the harness against the tree they build in
(`PEARDE_ROOT=<lane>`) and quotes what it printed.

## Acceptance

- [x] `PEARDE_ROOT=<tree> bash pearde/prds/a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re/probe/verify.sh` prints `0 fail` and `verify.sh done, fail=0`, with sections A, B, C, D, E and F all `ok`.
- [x] Section D of that run ticks both control boxes — the pre-fix resolver reports `0 notes on record` from a lane and creates `<lane>/pearde/wiki`. Without them the section A box proves nothing.
- [x] `python3 resources/knowledge.py query "board"` run with the cwd inside a lane worktree prints the same `N notes on record` as the same command run from the checkout, and creates no directory under `<lane>/pearde/`.
- [x] `python3 resources/knowledge.py doctor` from a lane reports the live board's note count, not `0 notes`.
- [x] `bash resources/doctor.sh` still prints its `knowledge` row `ok` with the live note count — the row passes `--root` explicitly and must be unaffected.
- [x] `pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh` run with `PEARDE_ROOT=<lane>` no longer prints `knowledge.py board wrote 0 PRD note(s)`; its fail count is one lower than the same harness run against the same tree with the resolver reverted. Its other failures are that PRD's, pre-existing, and not to be touched here.
- [x] `python3 resources/index.py check` from the tree under test reports no new problem beyond the three it already reports (`index.md → @pearde/memos/lanes-share-one-copy-of-what-they-regenerate.md`, `references/language.md → @references/personas/writer.md`, `resources/board/edit.py → @questions.py`).

## Verify and Proof

```sh
PEARDE_ROOT="$PWD" bash pearde/prds/a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re/probe/verify.sh
python3 -c "import ast; ast.parse(open('resources/knowledge.py').read())" && echo "knowledge.py parses"
python3 resources/knowledge.py doctor
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
if [ -z "$out" ] && [ "$rc" != 0 ]; then echo "index.py check crashed before printing"; exit 1; fi
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -q 'resources/knowledge\.py'; then exit 1; fi
echo "verify block complete"
```
