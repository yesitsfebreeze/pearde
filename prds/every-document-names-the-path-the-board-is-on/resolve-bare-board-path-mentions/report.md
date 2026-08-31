# Report — resolve-bare-board-path-mentions

Verdict: **DONE**. One spec, five acceptance boxes, each re-run by me against
what is on disk now. Verify block exits 0 under `bash -e -o pipefail`; the
repo's gate is green.

## Numbers

| measure | value |
|---|---|
| bare `prds/` tokens at `HEAD`, in the 14 scoped files | 20, across 11 files |
| bare tokens in the working tree now | 0 |
| of the earlier pass's 25 rewrites, present on disk | 25 — none lost |
| of those, wrong target, corrected by me | 6 |
| documented exceptions still bare, by design | 5 |
| forbidden tokens (`.pearde/.pearde`, `prds/prds`) | 0 |
| gate | `index.py check` 0, `memos.py check` 0, `doctor.sh` 0 |

## The analyst's counts were wrong, in both directions

The brief said not to trust them. They do not hold.

**25 across 14 files is an overcount.** Measured `HEAD` against the working
tree with one scanner: **20** bare tokens across **11** files. Three of the
14 footprint files — `references/parts/workers.md`, `resources/memos.py`,
`resources/guard.py` — carry no bare token at `HEAD` at all. The rename-table
PRD had already corrected them. The earlier pass counted five already-correct
tokens (`workers.md` x3, `memos.py` x1, `guard.py` x1) as its own work.

**Nothing was lost to concurrent editing.** The specific worry — that the
`guard.py` `skill_file()` edit was made under another session's rewrite and
might need reapplying — does not arise: `guard.py` at `HEAD` already reads
`.pearde/prds/` in that docstring, and it matches the code below it, which
tests `os.path.join(SKILL, BOARD_DIR, PRDS_DIR)`. All 25 claimed rewrites are
present on disk. The 20 real ones are uncommitted working-tree changes.

## Six rewrites picked the wrong one of the two targets — fixed

This is the real defect, and it is the thing the contract actually asks for:
`.pearde/` **or** `.pearde/prds/` "as its context actually means, verified
against the code it describes."

`BOARD_DIR = ".pearde"` in `@resources/board/plan.py`; `find_board` returns
`<repo>/.pearde`. Every reader that resolves a setting does
`os.path.join(board, …)` — onto `.pearde/`, never onto `.pearde/prds/`. Six
mentions describe exactly that join and had been rewritten to `.pearde/prds/`,
which is false against the code:

| file | mention | reader that settles it |
|---|---|---|
| `references/settings.md` | `memos:` relative to | `memos.py` `memos_dir` — `os.path.join(board, v)` |
| `references/settings.md` | `workflows:` relative to | `workflows.py` `workflows_dir` — the same join |
| `references/settings.md` | `members:` relative to | `plan.py` `members` — the same join |
| `references/parts/master.md` | "resolves against the master's" | `plan.py` `members` |
| `references/parts/doctor.md` | "`workflows:` pointing outside" | `doctor.sh` — the default `$BOARD/workflows` sits *inside* `.pearde/`, so "outside" can only mean the board root |
| `references/parts/doctor.md` | "every `verify.sh` that `find` returns under" | `doctor.sh:642` — `find "$BOARD" -name verify.sh`, `BOARD="$d/.pearde"` |

All six now read `.pearde/`. Diff is 8 lines across 3 files, all in footprint.

The old text was not wrong when it was written: before the move the board dir
*was* `<repo>/prds`, so "relative to `prds/`" meant "relative to the board
dir". Expanding it to `.pearde/prds/` is the one rewrite that changes the
meaning instead of preserving it.

## The exceptions

The two the earlier pass named — `resources/index.py`'s `board()` and
`resources/doctor.sh`'s board-walk comment — are still the right calls, and
both sit **outside this spec's footprint**, so neither was touched.
`index.py:89` still tests `path == "prds" or path.startswith("prds/")`; its
docstring describes that literal accurately. `doctor.sh:248/250/287/298`
phrase `prds/` as historical contrast ("not a literal `prds/` — that was the
pre-migration contract"), which is correct as written.

Five bare tokens remain in the footprint, all deliberate and all now asserted
as exceptions by the Verify block rather than merely described in prose:
`guard.md` and `guard.py`'s quoted `ls prds/*/prd.md` walk pattern, `guard.py`'s
regex that matches it, and `workers.md`'s two `<prds/>` brief placeholders.

## Defects outside the footprint — reported, not fixed

- **`resources/doctor.sh:480` and `:486` are genuinely stale**, and `:486` is
  user-facing. The code guards on `[ -d "$BOARD/knowledge" ]` and reads
  `"$BOARD/knowledge"`, but the comment says `prds/knowledge/` and the broken
  row prints `"prds/knowledge/ present, no python3 to read it"` — a path that
  does not exist on any board since the move. This was carried as a
  "knowledge-row exception" by the sibling PRD; it is not an exception, it is
  a miss. `doctor.sh` is outside this spec's footprint and is modified by
  another session right now, so it wants its own PRD.
- **`resources/board/plan.py`'s `members()` never learned about `.pearde`.**
  It appends a literal `"prds"` (`if os.path.basename(path) != "prds" and
  os.path.isdir(os.path.join(path, "prds"))`), so a member named by its repo
  root can no longer be found — a member board now lives at `<repo>/.pearde`,
  not `<repo>/prds`. `references/parts/master.md`'s "A path at a repo root
  gains `/prds`" and `references/install.md:195-196`'s example
  `- ../mitosys/prds` both describe this behaviour **truthfully**, so I left
  them: rewriting the prose would misdescribe working code. Neither is a bare
  `prds/` token — no trailing slash — so neither is in this PRD's scope. The
  fix is behavioural and belongs in its own PRD.

## The Verify block was broken, and is rebuilt

The block as specced would have failed `collect` while being correct. Two
faults:

1. `for f in $FILES; do grep -n "prds/" "$f" | grep -v '<prds/>'; done` —
   `index.md`, `references/install.md` and `references/system.md` contain no
   `prds/` at all, so the first `grep` exits 1; under `-o pipefail` the
   pipeline fails and `-e` kills the block on the clean case.
2. It asserted only that no bare token remained. It could not have caught the
   six wrong-target rewrites, because `.pearde/prds/` passes a
   "no bare `prds/`" test perfectly.

The replacement scans in Python, classifies each occurrence by the characters
immediately before it, asserts the six board-root strings positively, and ends
on an explicit `echo`. One trap worth recording: my own first scanner allowed
any line containing `"ls"` and `"*"` as a walk pattern, and silently swallowed
`settings.md`'s `workflows:` row — **"elsewhere" contains "ls"**, and that row
contains `**the**`. A substring test over a whole line is unsound here; the
test has to be on the token's immediate left context. That bug hid one real
token from my first count, which is why the table above reports 20 and not 19.

## Scores

complexity: 10
blast-radius: low
workflow: none fit
