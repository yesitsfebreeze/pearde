---
state: done
origin: requested
priority: 50
complexity: 15
blast-radius:
actual: 0.35h
---

# ramp is a doctor row not a gate

A fresh board no longer opens with an ASK from ramp on pass 1 (`init` writes `happiness: 0`, ramp calls scout's `route.sh` over the network). `happiness` absent means closed; ramp runs by hand or as a doctor row.

## Done means

`pearde init --example` then `pearde next` reaches the scan without an ask; `pearde ramp` still measures on demand.

## Needs

No gate.

## Report

spec01: exit 0
PASS  no file under resources/ still reads happiness: (got 0)
PASS  settings.md declares no happiness key (got 0)
PASS  ramp.py defines no cmd_gate
PASS  ramp.py defines no cmd_happy
PASS  ramp.py defines no write_ask
PASS  ramp.py defines no def happiness
PASS  ramp answers no happy verb
PASS  init --example wrote a board
PASS  init --example writes no happiness: key
PASS  init writes no happiness: key
PASS  next opens on the scan — step 2 · answer — asking 1 — one standing is no
PASS  no .state/ask.md on a fresh board
PASS  ramp gap exits 0 with a gap standing (got 0)
PASS  ramp gap sees the rust the tree asks for
PASS  doctor prints a ramp row —off     0 of 1 job answered · gap: rust
PASS  an unanswered job reads off, not broken
PASS  the row's fix line names pearde ramp
PASS  the ramp row contributes no broken part (got 0)
PASS  a tree asking for nothing reads off — the tree asks for nothing the jobs table

ramp is a doctor row, not a gate — every check green
PASS  a plain board counts its own tree: 30 (got 30)
PASS  a plain board's why is the marker list, not a member credit (got  *.rs×30)
PASS  the second member counts its own 12 (got 12)
PASS  the master sums 30+12+its own 1 = 43 (got 43)
PASS  the master's row credits member a (got  a 30, b 12, top 1)
PASS  the master's row credits its own tree as one more member
PASS  the master's row is a member credit, not a marker list
PASS  the master's credits are loudest member first
PASS  one member's 15 .md stays under writing's floor on its own
PASS  the floor lands on the sum: 35 over two members that each fall short
PASS  a master under a master reaches the grandchildren: 43 (got 43)
PASS  a members cycle terminates and counts each repo once: 8 (got 8)
PASS  board_words unions a member's PRD titles (got perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
	LC_ALL = (unset),
	LC_CTYPE = "C.UTF-8",
	LANG = "English"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
MEMBER OWN)
PASS  board_words keeps the master's own PRD titles in that union
PASS  a master's fork names the member that asked (got: a 30, b 12, top 1 ask for rust)
PASS  a master's fork does not say "The tree"
PASS  a plain board's fork still says "The tree" (got: The tree asks for rust (*.rs×30))

spec02: exit 0
PASS  no file under resources/ still reads happiness: (got 0)
PASS  settings.md declares no happiness key (got 0)
PASS  ramp.py defines no cmd_gate
PASS  ramp.py defines no cmd_happy
PASS  ramp.py defines no write_ask
PASS  ramp.py defines no def happiness
PASS  ramp answers no happy verb
PASS  init --example wrote a board
PASS  init --example writes no happiness: key
PASS  init writes no happiness: key
PASS  next opens on the scan — step 2 · answer — asking 1 — one standing is no
PASS  no .state/ask.md on a fresh board
PASS  ramp gap exits 0 with a gap standing (got 0)
PASS  ramp gap sees the rust the tree asks for
PASS  doctor prints a ramp row —off     0 of 1 job answered · gap: rust
PASS  an unanswered job reads off, not broken
PASS  the row's fix line names pearde ramp
PASS  the ramp row contributes no broken part (got 0)
PASS  a tree asking for nothing reads off — the tree asks for nothing the jobs table

ramp is a doctor row, not a gate — every check green
