---
state: done
origin: requested
priority: 88
complexity: 32
blast-radius:
workflow: probe-then-spec
actual: 9.33h
---

# collect resolves a board path two ways and both are wrong

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
collect.py parses
491:def holder(path):
540:def foot_places(p, board, board_root, repo):
515:        r = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
no board prefix test left
no wrong refusal left
board modules: /Users/feb/dev/infra/pearde/resources/board

L1 plain board
  pass  footprint stays in the code repo
L2 board is its own git repo
  pass  a code path stays in the code repo
  pass  a board path spelled from the CODE repo reroutes
  pass  a board path spelled the BOARD's own way resolves
  pass  sort_paths places every footprint
L3 the code repo is checked out under the board
  pass  a code path under the board stays in the CODE repo
  pass  sort_paths groups it under the code repo

every fixture was under /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/probe-collect-paths-hq_fr8cl, removed on exit
7 pass / 0 fail

7 checks · 7 pass · 0 fail
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
PASS  every fixture is under one mktemp -d, removed on exit (/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.wKAjW3rMKa)
the-tool-keeps-its-word/collect-keeps-its-word 101 checks · 101 pass · 0 fail
the-board-runs-itself/collect-is-a-command 133 checks · 133 pass · 0 fail
the-board-runs-itself/hunks-land-where-they-came-from 47 checks · 47 pass · 0 fail
filing-refuses-a-file-it-does-not-hold 52 checks · 52 pass · 0 fail

spec02: exit 0
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
PASS  every fixture is under one mktemp -d, removed on exit (/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.wXJK6mU5wi)
20
4
4
1

spec03: exit 0
memos.py check rc=0

index.py check rc=1
references/language.md references @references/personas/writer.md — not on disk
1
1
1
1
1
the claim is gone
