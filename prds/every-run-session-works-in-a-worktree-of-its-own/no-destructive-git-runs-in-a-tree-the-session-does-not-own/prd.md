---
state: done
origin: requested
priority: 90
complexity: 30
blast-radius:
needs:
  - a-session-ledger-names-who-holds-what-and-reaps-what-is-gone
workflow: probe-then-spec
actual: 9.44h
---

# no-destructive-git-runs-in-a-tree-the-session-does-not-own — reset --hard`, `checkout --`, `clean` and a real `stash` are refused in any tree the running session does not own — in the board's own code and in a session's own shell

reset --hard`, `checkout --`, `clean` and a real `stash` are refused in any tree the running session does not own — in the board's own code and in a session's own shell

## Report

spec01: exit 0
  ok   A1  reset --hard discards
  ok   A2  reset --keep does not
  ok   A3  checkout -- discards
  ok   A4  checkout <branch> does not
  ok   A5  clean discards
  ok   A6  clean -n does not
  ok   A7  a real stash discards
  ok   A8  stash create does not
  ok   A9  a cd carries to the git
  ok   A10 a quoted mention does not
  ok   B1  two sessions took two trees
  ok   B2  a session may discard its own tree
  ok   B3  it may not discard the other's
  ok   B4  nor the other way round
  ok   B5  nor the checkout neither owns
  ok   B6  a shell sitting in the checkout may
  ok   C1  reaching into a peer's tree by -C
  ok   C2  reaching in by cd
  ok   C3  its own tree is allowed
  ok   C4  a read is allowed
  ok   D1  the guard denies a peer's tree
  ok   D2  the guard allows a session its own tree
  ok   D3  the guard denies a real stash in the checkout
  ok   D4  the denial names the command
  ok   D5  the denial names the memo
  ok   G1  a cwd outside every board is no way round
  ok   E1  session one's work stands
  ok   E2  session two's work stands
  ok   F1  no board above it: allowed

probe: green
refuse routes, exit 0 in a tree this session owns
refuse cmd exits 3 when refused
_park's reason is on record
the lane reset is conditional
  harnesses   broken  4 of 76 green · 64 unpinned · 114s · 50 failed
pearde/prds/a-harness-measures-the-tree-its-worker-built-in/probe/verify.sh
pearde/prds/a-parked-prd-comes-back/probe/verify.sh
pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh
pearde/prds/an-unknown-flag-refuses/probe/verify.sh
pearde/prds/board-rel-is-a-third-wrong-board-path-resolution/probe/verify.sh
pearde/prds/brief-does-not-refuse-the-claim-it-was-just-handed/probe/verify.sh
pearde/prds/check-crosses-member-boundaries/probe/verify.sh
pearde/prds/collect-resolves-a-board-path-two-ways-and-both-are-wrong/probe/verify.sh
pearde/prds/complexity-is-guarded-like-priority/probe/verify.sh
pearde/prds/every-run-session-works-in-a-worktree-of-its-own/probe/verify.sh
pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh
pearde/prds/nothing-left-open/the-line-tells-the-truth/probe/verify.sh
pearde/prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh
pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh
pearde/prds/one-page-that-says-whats-up/probe/verify.sh
pearde/prds/resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule/probe/verify.sh
pearde/prds/resources-are-organised-by-responsibility/probe/verify.sh
pearde/prds/resources-are-organised-by-responsibility/the-largest-module-is-cut-by-responsibility/probe/verify.sh
pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe/verify.sh
pearde/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh
pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
pearde/prds/the-board-asks-for-itself/two-questions-start-a-drill/probe/verify.sh
pearde/prds/the-board-runs-itself/an-example-board/probe/verify.sh
pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh
pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh
pearde/prds/the-board-runs-itself/one-command/probe/verify.sh
pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh
pearde/prds/the-board-runs-itself/the-loop-is-commands/probe/verify.sh
pearde/prds/the-board-runs-itself/the-next-line-runs/probe/verify.sh
pearde/prds/the-board-runs-itself/the-page-shows-the-round/probe/verify.sh
pearde/prds/the-board-runs-itself/tokens-per-transition/probe/verify.sh
pearde/prds/the-board-runs-itself/too-big-splits-itself/probe/verify.sh
pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh
pearde/prds/the-brief-names-the-verdict-line-collect-requires/probe/verify.sh
pearde/prds/the-collect-and-brief-harnesses-are-carried-across-the-layou/probe/verify.sh
pearde/prds/the-daemon-must-not-write-into-a-board-path-it-no-longer-own/probe/verify.sh
pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh
pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh
pearde/prds/the-round-runs-in-a-window-that-ends/probe/verify.sh
pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh
pearde/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh
pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/verify.sh
pearde/prds/upgrade-leaves-the-memo-index-stale/probe/verify.sh
pearde/prds/workflows-on-the-board/workflow-attach/probe/verify.sh
pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh
pearde/prds/workflows-on-the-board/workflow-reader/verify.sh
pearde/prds/workflows-on-the-board/workflow-seed/probe/verify.sh
pearde/prds/workflows-on-the-board/workflow-skill/probe/verify.sh

spec02: exit 0
handles has the row
guard.md has the row
the false claim is gone
the surviving point is still there
files.md has the row
index.md has the keyword
the index check names nothing of this PRD's (index.py check exit 1)

spec03: exit 0
PASS  the reader sees an ungated `reset --hard`, a `clean` spelled with a concatenated pathspec, and a real `stash`, in a synthetic module
PASS  and reads `reset --keep`, `stash create` and a plain `checkout` as discarding nothing
PASS  resources/board/collect.py:578 — git stash in `_park`, exempt while its recorded reason ('stash-then-POP') stands
PASS  resources/board/collect.py:970 — git stash in `guarded_run`, exempt while its recorded reason ('stash-then-POP') stands
PASS  resources/board/lanes.py:257 — git reset in `merge`, gated
PASS  28 Python file(s) under resources/ hold no ungated destructive git
no-destructive-git-runs-in-a-tree-the-session-does-not-own: holds
the check fails on an injected reset --hard
bash: /resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh: No such file or directory
