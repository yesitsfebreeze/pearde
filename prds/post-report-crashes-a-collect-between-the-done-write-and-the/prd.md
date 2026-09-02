---
state: done
origin: requested
priority: 95
complexity: 9
blast-radius:
workflow: probe-then-spec
actual: 0.12h
commit: 1abd630 0377a70
---

# post_report crashes a collect between the done write and the commit

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
R. reproduced at 58c92e6: the four live-but-wrong daemons
  ok   R/garbage the pinned collect does not exit 0
  ok   R/garbage ...it exits by traceback
  ok   R/garbage ...raised through post_report
  ok   R/garbage the record on disk says done
  ok   R/garbage ...and no commit: on it
  ok   R/garbage ...and nothing was committed
  ok   R/truncate the pinned collect does not exit 0
  ok   R/truncate ...it exits by traceback
  ok   R/truncate ...raised through post_report
  ok   R/truncate the record on disk says done
  ok   R/truncate ...and no commit: on it
  ok   R/truncate ...and nothing was committed
  ok   R/list the pinned collect does not exit 0
  ok   R/list ...it exits by traceback
  ok   R/list ...raised through post_report
  ok   R/list the record on disk says done
  ok   R/list ...and no commit: on it
  ok   R/list ...and nothing was committed
  ok   R/entry the pinned collect does not exit 0
  ok   R/entry ...it exits by traceback
  ok   R/entry ...raised through post_report
  ok   R/entry the record on disk says done
  ok   R/entry ...and no commit: on it
  ok   R/entry ...and nothing was committed
R. reproduced at 58c92e6: anything raised in the same place
  ok   R/inject the injected error escapes the process
  ok   R/inject ...as a traceback
  ok   R/inject the record on disk says done
  ok   R/inject ...and no commit: on it
  ok   R/inject ...and nothing was committed
R. reproduced at 58c92e6: the container path tears the same way
  ok   R/container the pinned collect does not exit 0
  ok   R/container ...it exits by traceback
  ok   R/container the record on disk says done
  ok   R/container ...and nothing was committed
T. the tree: a wrong daemon is said, never raised
  ok   T/garbage exit 0
  ok   T/garbage ...no traceback
  ok   T/garbage ...the line says not posted
  ok   T/garbage the record says done
  ok   T/garbage ...with a commit: on it
  ok   T/garbage ...two commits on top
  ok   T/truncate exit 0
  ok   T/truncate ...no traceback
  ok   T/truncate ...the line says not posted
  ok   T/truncate the record says done
  ok   T/truncate ...with a commit: on it
  ok   T/truncate ...two commits on top
  ok   T/list exit 0
  ok   T/list ...no traceback
  ok   T/list ...the line says not posted
  ok   T/list the record says done
  ok   T/list ...with a commit: on it
  ok   T/list ...two commits on top
  ok   T/entry exit 0
  ok   T/entry ...no traceback
  ok   T/entry ...the line says not posted
  ok   T/entry the record says done
  ok   T/entry ...with a commit: on it
  ok   T/entry ...two commits on top
T. the tree: a daemon that answers is still posted to
  ok   T/ok exit 0
  ok   T/ok the line says report posted
  ok   T/ok ...two commits on top
T. the tree: anything raised in the window puts the record back
  ok   T/inject exit 1 — a refusal, not a traceback
  ok   T/inject ...nothing escaped
  ok   T/inject ...it says the record was put back
  ok   T/inject ...and names what raised
  ok   T/inject the record was put back whole
  ok   T/inject ...and nothing was committed
T. the tree: the container path is guarded the same way
  ok   T/container exit 0
  ok   T/container ...no traceback
  ok   T/container ...the line says not posted
  ok   T/container the record says done
  ok   T/container ...one commit on top
  ok   T/container-inject exit 1
  ok   T/container-inject ...nothing escaped
  ok   T/container-inject the record was put back whole
  ok   T/container-inject ...and nothing was committed

verify: 75 checks · 75 pass · 0 fail
PASS 0a-board-is-its-own-root
PASS 0b-baseline-holds-code-path
PASS 1a-specced-sibling-refused
PASS 1b-dry-exit
PASS 1c-real-exit
PASS 1d-nothing-committed
PASS 1e-b-not-carried
PASS 1f-widen-offered
PASS 1g-no-stale-clause
PASS 2a-dry-exit
PASS 2b-dry-splits
PASS 2c-real-exit
PASS 2d-a-line-committed
PASS 2e-b-line-not-committed
PASS 2f-b-line-still-in-tree
PASS 3a-dry-ok
PASS 3b-dry-adds
PASS 3c-real-ok
PASS 3d-committed
PASS 4a-widen-ok
PASS 4b-widen-named
PASS 4c-whole-file
PASS 5a-done-sibling-ok
PASS 6a-exit
PASS 6b-says-why
PASS 6c-b-not-carried
PASS 6d-nothing-committed
PASS 7a-board-is-not-its-own-root
PASS 7b-no-repo-side-written
PASS 7c-sides-board-only
PASS 7d-alias-is-the-board-side
PASS 7e-code-dirt-in-the-one-side
---- 32 passed, 0 failed
verify.sh exit 0
A. reproduced at e8b262d: the record staged by hunk
  ok   A1 the old collect exits 0
  ok   A1 ...and says by hunk on the board's own record
  ok   A1 HEAD's record says analyzing
  ok   A1 ...with the three ticks under it
  ok   A1 the tree says done
  ok   A1 ...and the folder is dirty after its own collect
A. the record lands whole, commit: in a second commit
  ok   A2 exit 0
  ok   A2 two commits on top
  ok   A2 HEAD is the record commit
  ok   A2 ...carrying only prd.md
  ok   A2 HEAD~1 carries the code and the record
  ok   A2 HEAD~1's record says done
  ok   A2 ...with the three ticks
  ok   A2 ...and actual:
  ok   A2 ...and no claim:
  ok   A2 ...and the analyst's paragraph, the baseline hunk, whole
  ok   A2 HEAD~1 does not carry commit:
  ok   A2 HEAD's commit: names HEAD~1
  ok   A2 the tree's commit: is the same
  ok   A2 the folder is clean
  ok   A2 the line does not say by hunk on the record
  ok   A2 the line names the record commit
  ok   A2 the line names the code commit
  ok   A2 nothing owed for the record
  ok   A2 one transition row
  ok   A3 clean tree: exit 0
  ok   A3 HEAD~1 is the record, alone
  ok   A3 commit: names it — never none
  ok   A3 the folder is clean
  ok   A4 --dry exit 0
  ok   A4 --dry names the record and the second commit
  ok   A4 --dry leaves the state
  ok   A4 --dry commits nothing
B. reproduced at e8b262d: the merged hunk goes as the worker's
  ok   B1 the diff is one merged hunk
  ok   B1 the old collect exits 0
  ok   B1 ...and commits the foreign line as the worker's
B. refused, named, nothing staged; --widen takes it; one line apart both land right
  ok   B2 exit 1
  ok   B2 named: file and line
  ok   B2 ...and the way out
  ok   B2 nothing committed
  ok   B2 the index is HEAD
  ok   B2 the PRD is still claimed
  ok   B2 the record is untouched
  ok   B2 --widen exits 0
  ok   B2 --widen commits both lines
  ok   B2 --widen said on the line
  ok   B3 one untouched line between: exit 0
  ok   B3 the worker's line is in HEAD~1
  ok   B3 the foreign line is not
  ok   B3 ...and stays in the tree
  ok   B3 by hunk on the line
  ok   B4 a merged insertion is refused
  ok   B4 named at the working line
  ok   B5 a baseline hunk undone before collect is not two authors
  ok   B5 the worker's line landed
  ok   B6 the record with adjacent hunks goes whole
  ok   B6 ...four ticks in HEAD~1
C. reproduced at e8b262d: a parent whose children are all done has no way to done
  ok   C1 the old collect refuses it
  ok   C1 ...on its state
  ok   C1 the old scan does not list it under collect
C. scan lists it, collect closes it in one commit
  ok   C2 scan lists big under collect — compute_plan's one list, the row without a why
  ok   C2 ...and not big/first
  ok   C2 --dry exit 0
  ok   C2 --dry says the phrase
  ok   C2 --dry names the sum and the sha
  ok   C2 --dry writes nothing
  ok   C2 exit 0
  ok   C2 done
  ok   C2 actual is the children's sum
  ok   C2 commit: is the last child's
  ok   C2 one commit
  ok   C2 its subject
  ok   C2 its paths: the parent's prd.md alone
  ok   C2 clean under it
  ok   C2 the line
  ok   C2 a transition row
  ok   C2 collecting it again is refused
  ok   C3 a parent with its own spec is not listed under collect
  ok   C3 ...and collect refuses it
  ok   C3 ...on its state — ordinary held work, the specs decide
  ok   C3 nothing written
  ok   C4 a parent with an open box of its own is refused
  ok   C4 nothing written
  ok   C5 a child still open: refused
  ok   C5 ...and not listed
  ok   C6 a parent that finished its own work goes the ordinary way
  ok   C6 ...two commits
  ok   C6 ...the record commit last
  ok   C6 ...never as a container
D. the posted report is in the commit
  ok   D the daemon came up on a spare port
  ok   D exit 0
  ok   D report posted
  ok   D ## Report is in HEAD~1
  ok   D ...holding the verify's exit
  ok   D the folder is clean
  ok   D the real registry is untouched
Z. hygiene
  ok   Z no path under .pearde/prds/.claims/ on any commit above
  ok   Z the bare collect exits 0
  ok   Z ...and closes finished
  ok   Z ...and big
  ok   Z two lines

101 checks · 101 pass · 0 fail
