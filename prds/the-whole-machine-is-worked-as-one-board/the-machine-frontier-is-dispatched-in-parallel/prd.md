---
state: done
origin: requested
priority: 80
complexity: 38
blast-radius: high
needs:
  - the-machine-frontier-is-one-ordered-list
workflow: probe-then-spec
actual: 0.85h
commit: 0ca4c4c 59fb13a
---

# the-machine-frontier-is-dispatched-in-parallel — That frontier's waves are dispatched as pass workers across boards, serialised on real-path footprint clashes, claim refusals named and skipped, one progress line over the merged set

That frontier's waves are dispatched as pass workers across boards, serialised on real-path footprint clashes, claim refusals named and skipped, one progress line over the merged set

## Report

spec01: exit 0
ok   fixture dry      2 would · nothing on disk moved
ok   fixture clash    serialised · gap 0.04s
ok   fixture noclash  overlapped by 0.61s
ok   fixture adapter  claude · argv ['--print', '--dangerously-skip-permissions', '/pearde run one']
ok   fixture dead     dead: API Error: 402 {"error":"credit balance"}
ok   fixture instant  dead: exited 0 after 0.05s — under the 0.25s launch grace, so it never worked
ok   fixture refuse   refused [('@alpha/two', 'needs: one is `question`, not done')]
ok   fixture alive    both in · 4 lines
ok   fixture cap      workers: 1 serialised · workers: 0 overlapped
ok   fixture adapters name one with --adapter (a, b)
ok   fixture once     1 out, returned in 0.00s
ok   fixture deadline stop · deadline reached with 1 in flight
ok   fixture workers  load-derived 12 · --workers labels its override
ok   the verb is machine's, not a second command
ok   --dry runs from / with no board above the cwd
ok   the order is printed before anything moves
ok   --dry names every row it would launch
ok   --dry opened no run log on this board
ok   a claim refusal is named with its reason
ok   the merged progress line is printed
ok   the closing tally accounts for every row
ok   a row the frontier marks ready but claim refuses is skipped
ok   the sibling read-only harness is still 33/33
PASS
resources/board/lanes.py is on disk with no row in references/files.md

spec02: exit 0
PASS dead     dead: API Error: 402 {"error":"credit balance"}
PASS instant  dead: exited 0 after 0.05s — under the 0.25s launch grace, so it never worked
PASS alive    both in · 4 lines

spec03: exit 0
PASS refuse   refused [('@alpha/two', 'needs: one is `question`, not done')]
skip @pearde/the-whole-machine-is-worked-as-one-board · leaf: the-whole-machine-is-worked-as-one-board has children not done — the-machine-frontier-is-dispatched-in-parallel
skip @mitosys/plugins-visible · leaf: plugins-visible has children not done — a-mounted-child-has-no-census-row, view-scripts-have-no-runtime
skip @dotfiles/09-simplify/propagate-a-tinty-apply-into-a-running-nvim · needs: 09-simplify/05-terminal is `blocked`, not done

spec04: exit 0
PASS alive    both in · 4 lines

spec05: exit 0
resources/board/lanes.py is on disk with no row in references/files.md
