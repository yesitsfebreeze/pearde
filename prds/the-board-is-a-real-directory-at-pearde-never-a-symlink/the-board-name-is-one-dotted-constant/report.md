# report — the-board-name-is-one-dotted-constant

Verdict: SPECCED

complexity 28 · blast-radius high · workflow `probe-then-spec`

The build went through end to end. Three specs, all three verify blocks green
in the lane, 84 lines added against 347 removed. The probe is uncommitted in
`.pearde/.lanes/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-board-name-is-one-dotted-constant`.

## What the build found

**The two copies had already disagreed, and it was live.** `resources/guard.py`
spelled `BOARD_DIR = "pearde"` with `.pearde` as its legacy — the exact inverse
of `resources/board/boards.py`. On a fixture project holding a real `.pearde/`
board and a real `pearde/` board, `plan.find_board` answered `.pearde` and
`guard.board_of` answered `pearde`: the guard counted a session's blocks
against one board while `pearde scan` reported the other. Measured, not
inferred — the fixture matrix is in `probe/verify.sh` and it fails on `HEAD`
with `both guard want .pearde, got pearde`.

**The status line reported a finished board that was not finished.**
`statusline.sh` carried a bare `prds/` fallback no other resolver has, so
standing anywhere inside a board it resolved to `<board>/prds`, read no
`settings.md`, found no `members:` and dropped a master board's members. On the
`both` fixture it printed `2/2 100%` where `pearde scan` reported one open PRD.
Folding it onto the shared walk fixes that, and it is the one visible
behaviour change in this PRD: the second line's numbers move when the cwd is
inside a board.

**All three shell readers tried the legacy name first.** `doctor.sh`,
`statusline.sh` and `graph/graph.sh` each walked `pearde` before `.pearde`, and
`statusline.sh` took `settings.md` as its only marker where `doctor.sh` took
either. One sourced file, and a fifth test added there is added everywhere.

**`install.sh` needs no change.** It links `resources` as a whole directory
(`LINKS=(SKILL.md README.md index.md references resources)`), so a new file
under `resources/` is present in every install already. Checked, not assumed.

## The PRD's premise is one commit out of date

The contract says *six duplicating readers*. By the time this build ran there
were three: `resources/common.py` landed on `main` in `7e4d610` and had already
folded `grammar.py`, `health.py`, `memos.py`, `questions.py`, `index.py` and
`knowledge.py` onto one resolver. The lane was four commits behind that, and
pass one's probe — a new `resources/board/name.py` — was written against the
old tree and would have re-introduced a third copy. The lane was rebased onto
`main` and that probe discarded; a copy is parked outside the tree.

So the module is `common.py`, not a new file: it is stdlib-only, imports
nothing from `resources/board/`, and is already what five readers stand on. The
guard's own objection — a PreToolUse hook must not import something a broken
planner can break — is satisfied by it, and its import cost is 0 ms against a
29 ms interpreter start.

## Findings outside this contract

- `resources/common.py` was on disk with **no row in `references/files.md`** —
  `index.py check` reported it on the untouched tree. It is inside this
  footprint now, so spec03 adds the row; index went from four problems to three.
- The three remaining index problems are not this PRD's:
  `@resources/board/hotreload-test.js` named by `references/files.md` and by
  `@@view` after the file was deleted, and `references/parts/commits.md`
  pointing at `@pearde/memos/…` — an undotted board path in prose, which is
  `the-prose-and-the-invariants-say-dot-pearde`'s.
- `resources/invariants/a-master-need-is-the-union-of-its-members.sh` and
  `a-board-s-own-file-commits-in-the-board-repo.sh` build every fixture board
  under the legacy `pearde/` name. Correct as a test that the legacy name still
  resolves, but it means no committed invariant exercises the dotted one. That
  is the same sibling PRD's business, not a fix here.
- `doctor.sh`'s vault row still calls a real `.pearde/` board **broken** and
  prints a fix that moves it back to `pearde/`. Untouched here: the parent
  report assigns it to `the-vault-roots-at-the-board-not-the-project`.
- The word **resolver** is used throughout this PRD's contract and
  `grammar.py show resolver` says it is not defined on this board.
- The knowledge query returned 90 strong hits and enqueued no gap. The one
  pending entry written today (`260903-deee`) is another session's.
- A job seen twice now — fold N copies of a block into one module, re-export
  every name so no caller changes, prove the copies had drifted — has no
  workflow file. It ran inside `probe-then-spec` both times and needed no
  route of its own, so this is a note, not a second file.

## Specs

| spec | goal | complexity |
|---|---|---|
| spec01 | one Python module holds the board's name; `guard.py` and `boards.py` import it | 12 |
| spec02 | one shell file holds the same walk; `doctor.sh`, `statusline.sh`, `graph.sh` source it | 12 |
| spec03 | both shared modules named in the manifest and reachable by `index scope board` | 4 |

Footprint union — nine files, no directory:
`resources/common.py`, `resources/guard.py`, `resources/board/boards.py`,
`resources/board-name.sh`, `resources/doctor.sh`, `resources/statusline.sh`,
`resources/graph/graph.sh`, `references/files.md`, `index.md`.

**complexity 28** — the change is large in lines and small in decisions: one
module already existed, the two Python copies come out mechanically, and the
shell walk is a transcription of the one the Python side already agreed on. The
cost is in review, not in design.

**blast-radius high** — `guard.py` runs on every tool call, `statusline.sh` on
every prompt, `boards.py` under every command; and the fix changes which board
each of them names. A mistake is felt on all nine boards on this machine at
once, and the status-line numbers demonstrably move.

## Harnesses

Baselines in `probe/base-*.txt`, taken on `main` before the first edit.
`install.sh --check` identical. Six invariants identical (one red at baseline
and still red: `no-colour-group-in-the-vault-preset-is-a-path-query`).
`index.py check` four problems to three. `doctor.sh` changed in four rows, all
accounted for: index improved; the statusline row's numbers moved, which is the
finding above; `graph.json` gained a note another session wrote; the harness
count went 78 to 80 as other lanes specced.

## Scores

complexity: 28
blast-radius: high
workflow: probe-then-spec
