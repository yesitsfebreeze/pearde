---
state: done
origin: requested
priority: 80
complexity: 14
blast-radius:
workflow: probe-then-spec
actual: 0.18h
---

# board_rel is a third wrong board-path resolution

`collect` decides where a footprint path lives by manipulating strings instead
of asking git, and this is the third and last place it does so. `foot_root`
(landed `3f4afe2`) fixed the staging half and
`collect-resolves-a-board-path-two-ways-and-both-are-wrong` fixed membership by
`git rev-parse --show-toplevel`. `board_rel` was never taught the same thing.

`sort_paths` computes `board_rel = os.path.relpath(board, board_root)`. Since
2026-09-02 the board at `pearde/` is a git repo of its own, so `board` and
`board_root` are the same directory and the expression answers `"."`. `"."` is a
prefix of no path git ever prints, so `inside(path, ["."])` is False for every
one of them: `scratch()` swallows nothing, the rider sweep never runs, and 523
board paths read as inherited rather than as the board's own. It raises no
error and refuses nothing — it silently mis-sorts, which is why three passes of
collect defects were diagnosed around it without anyone naming it.

**Done when** a board path is recognised as the board's by which git repo holds
it, never by a relative-path prefix; `scratch()` and the rider sweep act on the
paths they were written for; and the 523 mis-sorted paths sort as the board's
own. The count is measured, not asserted.

**Must not change:** the two resolutions already landed. This is the same
underlying mistake, not a rewrite of their fix — build on
`collect-resolves-a-board-path-two-ways-and-both-are-wrong`'s membership test
rather than adding a fourth way to answer the question. No footprint outside
@resources/board/collect.py without saying why.

## Report

spec01: exit 0
collect.py parses
1186:def board_prefix(board, board_root):
1200:def under_board(path, board_rel):
1723:    board_rel = board_prefix(board, board_root)
1886:                  and under_board(path, board_rel) is not None
1822:                    and full not in widen and not inside(path, union)
no relpath board_rel left
no inside() on the board prefix left
the prefix arithmetic is right on both layouts
PASS  arithmetic: own-repo prefix is the empty string, not '.'
PASS  arithmetic: nested prefix is the directory name
PASS  arithmetic: under_board keeps the whole name under an empty prefix
PASS  arithmetic: under_board strips the prefix and the slash under a named one
PASS  arithmetic: under_board answers None for a path outside a named prefix
PASS  arithmetic: scratch sees a board dotfile through an empty prefix
PASS  arithmetic: scratch leaves an ordinary board file alone
PASS  own-repo: collect exits 0 (got 0)
PASS  own-repo: the memo written after the claim rides into the commit
PASS  own-repo: the board's own .state/ ledger does not ride
PASS  own-repo: the board's own .state/ ledger is not even listed
PASS  own-repo: a board file dirty before the claim does not ride
PASS  own-repo: that older file is reported inherited, not silently dropped
PASS  own-repo: the board dotfile the footprint names is added anyway
PASS  own-repo: the code file still lands in the code repo
PASS  nested-in-code: collect exits 0 (got 0)
PASS  nested-in-code: the memo written after the claim rides into the commit
PASS  nested-in-code: the board's own .state/ ledger does not ride
PASS  nested-in-code: the board's own .state/ ledger is not even listed
PASS  nested-in-code: a board file dirty before the claim does not ride
PASS  nested-in-code: that older file is reported inherited, not silently dropped
PASS  nested-in-code: the board dotfile the footprint names is added anyway
PASS  nested-in-code: the code file still lands in the code repo
PASS  every fixture is under one mktemp -d, removed on exit (/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.YFynxI46Be)

probe: 0 check(s) failed
PASS  the lane does not hold the board own file — it is cut without the board
PASS  nested: collect exits 0 (got 0)
PASS  nested: no run hits `fatal: pathspec … did not match any files`
PASS  nested: a NEW commit in the BOARD repo holds .gitignore
PASS  nested: the board working tree is clean after (got '')
PASS  nested: the code repo commits the code file
PASS  nested: the code repo never stages the board own path
PASS  nested: collect names the board-owned path it dropped from the lane add
PASS  flat: collect exits 0 (got 0)
PASS  flat: the code file lands in the one repo there is
PASS  flat: nothing is rerouted — the two roots are one
PASS  board-spelled: collect exits 0 (got 0)
PASS  board-spelled: no run refuses the footprint for want of a repo
PASS  board-spelled: a NEW commit in the BOARD repo holds prds/p1/probe/verify.sh
PASS  board-spelled: the code repo never stages the board own probe path
PASS  under: collect exits 0 (got 0)
PASS  under: the CODE repo commits resources/board/session.py
PASS  under: the BOARD repo commits the code path under no spelling
PASS  under: the code working tree is clean after (got '')
PASS  every fixture is under one mktemp -d, removed on exit (/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.YZxIvbEOkN)
the-tool-keeps-its-word/collect-keeps-its-word 101 checks · 101 pass · 0 fail
the-board-runs-itself/collect-is-a-command 133 checks · 133 pass · 0 fail
the-board-runs-itself/hunks-land-where-they-came-from 47 checks · 47 pass · 0 fail
filing-refuses-a-file-it-does-not-hold 52 checks · 52 pass · 0 fail
collect-must-not-reset-the-checkout-it-did-not-write 31 checks · 31 pass · 0 fail
