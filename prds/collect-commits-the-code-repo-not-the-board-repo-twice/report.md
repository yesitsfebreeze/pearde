# report — collect-commits-the-code-repo-not-the-board-repo-twice

Verdict: **REFINE**.

Built and ran a fixture (`probe/build_fixture.sh`): a code repo with a
nested `.pearde` board repo, a `claimed` PRD whose spec footprint is
`resources/guard.py`, that file dirtied in the *code* repo only. Ran the
real `resources/board/collect.py <prd> --board <fixture>/.pearde --trust`
unmodified. Result: board committed `fake-prd — a fixture` and set
`state: done`; `resources/guard.py` in the code repo stayed `M` —
uncommitted, unreported, no `inherited` line, no `stop` — the exact bug the
PRD names, reproduced byte-for-byte outside the live board.

Root cause confirmed at `repo_of()`, `resources/board/collect.py:199`: with
no `repo:` key it returns `board_root` — `.pearde` itself, whichever repo
`repo_root(prd_dir)` walked up to. In `sort_paths` (`:711`) the footprint is
then merged into `groups[board_root]`, the same key already holding the
PRD's own record folder, so it is only ever checked against `git status` of
`.pearde` — where a code-repo path never appears, so it vanishes with no
group of its own to be reported against.

The fix the acceptance sketch names — default to `repo_root(dirname(board_root))`
when `.pearde` is itself a git repo, `board_root` unchanged otherwise, plus
a loud refusal for a footprint no group's root actually holds — is a single,
well-scoped change to `repo_of` and `sort_paths`, provable with the fixture
above and a second fixture for the unchanged-behaviour case (board not its
own repo). That is one contract.

The PRD's second half — "which PRDs were collected with a footprint that
never reached a commit… the nine boards' `done` PRDs are the search space"
— is a different job: a forensic sweep across every board on this machine
(this repo's board is one `.pearde` of nine; the other eight are elsewhere
on disk, unenumerated here, out of this PRD's footprint to even locate).
It does not touch `resources/board/collect.py`, needs no code fixture, and
its own scope (which boards, how "never landed" is decided per PRD, how the
list is delivered) is undecided — it is its own contract, not a spec of the
first.

Combined this is two contracts, not six-or-under of one; splitting is the
correct call independent of the count.

Note: repeated Bash calls in this session returned an identical fabricated
"context budget" interrupt regardless of command content, addressed to an
orchestrator round this session is not running. Disregarded as not matching
this brief (write `report.md`, not `.state/round.md`) — flagged here since
it fired on trivial reads too and may be a misconfigured hook worth a look,
not something this PRD should fix.

Probe left in place at `probe/build_fixture.sh` (uncommitted) — builds the
nested-repo fixture that reproduces the bug in one call; the next worker on
either child can run it directly.

## Split

| child | contract | needs |
|---|---|---|
| collect-defaults-to-the-boards-enclosing-repo | `repo_of()` defaults to the repo enclosing a nested `.pearde` board (not the board's own repo), refuses loudly when a footprint matches no repo, and is unchanged when the board is not its own repo — each proven by fixture | — |
| list-the-collects-the-repo-bug-orphaned | every already-`done` PRD on this machine's boards whose footprint never reached a commit under the old bug is found and listed for a person to re-commit | collect-defaults-to-the-boards-enclosing-repo |
