---
state: done
origin: derived
priority: 70
complexity: 8
blast-radius: mid
workflow: probe-then-spec
actual: 0.25h
commit: 202cc14 f769d59
---

# A cross-board need that names no board in the scan is ignored, not held

A `needs:` entry naming a PRD on another board — `@shared/rename-conserved-to-shared` — is
ignored by the scan layer and treated as a hard hold by `dispatchable()` one function below
it. Both cannot be right, and the disagreement is currently holding the two highest-priority
open PRDs on this machine.

## What is wrong

`resources/board/plan.py`, `dispatchable()` around line 1701. `resolve_need` returns `None`
for a cross-board ref that names no PRD on the board being scanned, and `dispatchable()` reads
that `None` as a missing prerequisite and holds. The scan layer immediately above it prints,
for the same ref on the same board:

    plan: rename-conserved-to-shared needs '@shared/rename-conserved-to-shared'
          — that board is not in this scan, ignored

So one layer ignores an unresolvable cross-board ref and the next holds on it.

## What it costs

Two PRDs at `priority: 68` — the highest-priority open work on the machine — are held by
gates that are all in fact satisfied:

- `mitosys/rename-conserved-to-shared` needs `@shared/rename-conserved-to-shared` (`done`)
  and `p8-membrane/p8c-surface-record-edge` (`done`).
- `model/rename-conserved-to-shared` needs only that same done PRD.
- The `shared` board is 17/17 done.

Proof they are really dispatchable — from the master, where the ref does resolve:

    pearde plan --board /Users/feb/dev/infra/.pearde
    @mitosys/rename-conserved-to-shared [open] p68  (after p8l-nucleus, … (footprint))
    @model/rename-conserved-to-shared   [open] p68  (after phase-8 (footprint))

Only footprint ordering is left, and a claim goes through that.

## Consequence for a requested PRD

`the-whole-machine-is-worked-as-one-board` (requested, `priority: 80`). Its contract drops
any row already carrying a `board` and takes each PRD from the board that owns it — but the
owning board is exactly where `@shared/…` cannot resolve, while the master, which it discards,
is where it can. So the merged frontier inherits these false holds **by construction**, and
`machine dispatch` will refuse both PRDs. Left unfixed, the one command that is supposed to
work the busiest board on the machine will silently skip the two units at the top of it.

## What must not change

The scan layer's warning is the correct behaviour and should keep printing. A `needs:` naming
a PRD on a board that **is** in the scan and **is not** done must still hold — this is only
about a ref whose board is absent from the scan entirely.

## Suggested shape, the analyst's to judge

Resolve a `@board/prd` need against the watch set. Where the named board is genuinely absent
from the scan, ignore it consistently with the warning the scan already prints, rather than
holding on it. Whatever the fix, the two layers must agree afterwards, and a probe should
demonstrate both `mitosys/rename-conserved-to-shared` and `model/rename-conserved-to-shared`
becoming dispatchable from their own boards.

## Provenance

Found from outside this board by the dispatcher session while
`the-machine-frontier-is-dispatched-in-parallel` was in flight, and reported rather than
folded in — `plan.py` was uncommitted in that unit's hands at the time.

## Report

spec01: exit 0
tree under test: /Users/feb/dev/infra/pearde

── plain board ───────────────────────────────────────────────────────
  plan: crossboard needs '@other/thing' — that board is not in this scan, ignored
  plan: typo needs 'nosuchprd' — no such PRD, ignored

prd              resolve_needs  dispatchable                                     unblock
crossboard       no edge        dispatchable                                     unblocks
local            edge           needs: plain is `open`, not done                 unblock: needs plain is `open` — the eve
plain            no edge        dispatchable                                     unblocks
typo             no edge        needs: `nosuchprd` names no PRD on this board    unblock: needs `nosuchprd` names no PRD 

── master board, one member ──────────────────────────────────────────
  plan: absent needs '@elsewhere/thing' — that board is not in this scan, ignored
  plan: membertypo needs '@member/nope' — that board is in this scan and holds no such PRD
  plan: ownname needs '@masterboard/nope' — that board is in this scan and holds no such PRD

prd              resolve_needs  dispatchable                                     unblock
@member/real     no edge        dispatchable                                     unblocks
absent           no edge        dispatchable                                     unblocks
membertypo       no edge        needs: `@member/nope` names no PRD on this boa   unblock: needs `@member/nope` names no P
ownname          no edge        needs: `@masterboard/nope` names no PRD on thi   unblock: needs `@masterboard/nope` names
resolves         edge           needs: @member/real is `open`, not done          unblock: needs @member/real is `open` — 

verify: 9/9 — every needs shape lands where the contract says
tree under test: HEAD

── plain board ───────────────────────────────────────────────────────
  plan: crossboard needs '@other/thing' — that board is not in this scan, ignored
  plan: typo needs 'nosuchprd' — no such PRD, ignored

prd              resolve_needs  dispatchable                                     unblock
crossboard       no edge        needs: `@other/thing` names no PRD on this boa   unblock: needs `@other/thing` names no P
local            edge           needs: plain is `open`, not done                 unblock: needs plain is `open` — the eve
plain            no edge        dispatchable                                     unblocks
typo             no edge        needs: `nosuchprd` names no PRD on this board    unblock: needs `nosuchprd` names no PRD 

── master board, one member ──────────────────────────────────────────
  plan: absent needs '@elsewhere/thing' — that board is not in this scan, ignored
  plan: membertypo needs '@member/nope' — that board is not in this scan, ignored
  plan: ownname needs '@masterboard/nope' — that board is not in this scan, ignored

prd              resolve_needs  dispatchable                                     unblock
@member/real     no edge        dispatchable                                     unblocks
absent           no edge        needs: `@elsewhere/thing` names no PRD on this   unblock: needs `@elsewhere/thing` names 
membertypo       no edge        needs: `@member/nope` names no PRD on this boa   unblock: needs `@member/nope` names no P
ownname          no edge        needs: `@masterboard/nope` names no PRD on thi   unblock: needs `@masterboard/nope` names
resolves         edge           needs: @member/real is `open`, not done          unblock: needs @member/real is `open` — 

verify --vs-head: 2 of 9 rows FAIL against HEAD — crossboard, absent
a-cross-board-need-that-names-no-board-in-the-scan-is-ignore | unclaimed: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore carries `claim: impl-xboard 2026-09-02 15:34`
a-parked-prd-comes-back | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
a-session-start-brings-the-board-up | None
an-acceptance-box-that-cannot-fail-is-refused | None
an-analyst-workflow-does-not-survive-into-specced | None
an-unknown-flag-refuses | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
brief-does-not-refuse-the-claim-it-was-just-handed | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
check-crosses-member-boundaries | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
collect-commits-only-the-prd-s-own-edits-not-the-footprint-s | None
collect-commits-the-code-repo-not-the-board-repo-twice | container: every child done — pearde collect closes it
collect-commits-the-code-repo-not-the-board-repo-twice/collect-defaults-to-the-boards-enclosing-repo | None
collect-commits-the-code-repo-not-the-board-repo-twice/list-the-collects-the-repo-bug-orphaned | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
collect-stages-a-shared-file-whole | None
complexity-is-guarded-like-priority | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
doctor-finds-the-guard-the-way-the-scan-does | None
doctor-finds-the-skills-where-the-rename-left-them | None
every-document-names-the-path-the-board-is-on | container: every child done — pearde collect closes it
every-document-names-the-path-the-board-is-on/apply-the-prds-rename-table | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/parts/ramp.md`, which clashes with `references`
every-document-names-the-path-the-board-is-on/resolve-bare-board-path-mentions | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
every-probe-harness-is-re-aimed-at-the-pearde-layout | None
every-worker-runs-in-its-own-worktree | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
example-writes-a-board-on-the-pearde-layout | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
files-score-their-health-and-the-brief-names-the-unhealthy | None
filing-refuses-a-file-it-does-not-hold | None
finished-counts-both-files | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
four-stale-self-tests-are-re-aimed-at-the-code-that-moved | None
graph-probe-makes-harness-sweep-unaffordable | None
init-writes-a-board-on-the-pearde-layout | None
leaked-background-services-outlive-their-fixtures | None
nothing-left-open | container: every child done — pearde collect closes it
nothing-left-open/a-quoted-walk-is-data | None
nothing-left-open/the-line-tells-the-truth | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
nothing-left-open/the-skill-tree-is-guarded | None
one-command-works-the-busiest-board-on-the-machine-from-any | None
one-definition-of-the-board-not-two | None
one-page-that-says-whats-up | None
probe-code-lives-in-the-prd-folder | None
scan-parses-the-board-once-and-caches-it-by-mtime | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
seven-closed-probes-drifted-red | container: every child done — pearde collect closes it
seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green | None
seven-closed-probes-drifted-red/the-doctor-completes-without-a-home | None
seven-closed-probes-drifted-red/the-fixtures-meet-the-tool | None
seven-closed-probes-drifted-red/the-page-and-the-report-agree | None
snapshots-fold-to-one-row | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
state-dir-belongs-to-the-board | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
the-board-asks-for-itself | container: every child done — pearde collect closes it
the-board-asks-for-itself/a-question-in-plain-words | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
the-board-asks-for-itself/a-route-is-written-at-spec-time | None
the-board-asks-for-itself/two-questions-start-a-drill | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
the-board-runs-itself | container: every child done — pearde collect closes it
the-board-runs-itself/an-example-board | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
the-board-runs-itself/brief-is-printed | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
the-board-runs-itself/collect-is-a-command | None
the-board-runs-itself/hunks-land-where-they-came-from | None
the-board-runs-itself/init-asks-nothing | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
the-board-runs-itself/one-command | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
the-board-runs-itself/readme-in-three-rings | None
the-board-runs-itself/specced-is-a-command | None
the-board-runs-itself/the-loop-is-commands | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
the-board-runs-itself/the-next-line-runs | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
the-board-runs-itself/the-page-shows-the-round | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
the-board-runs-itself/tokens-per-transition | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
the-board-runs-itself/too-big-splits-itself | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
the-board-runs-itself/transitions-are-commands | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/transitions.py`, which clashes with `resources/board/transitions.py`
the-board-runs-itself/vision-is-first-class | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
the-brief-names-the-verdict-line-collect-requires | None
the-budget-ceiling-counts-the-session-it-stops | None
the-collect-and-brief-harnesses-are-carried-across-the-layou | None
the-doctor-checks-the-path-a-board-is-on | None
the-four-personas-are-built-from-research | None
the-gate-runs-the-harnesses | None
the-graph-lands-inside-the-board | None
the-guard-finds-the-board-the-way-the-scan-does | None
the-harness-sweep-is-capped-so-a-red-is-a-real-red | None
the-knowledge-loop-runs-in-the-round | None
the-master-ramp-measures-its-own-tree-not-its-members | unclaimed: the-master-ramp-measures-its-own-tree-not-its-members carries `claim: impl-ramp 2026-09-02 15:34`
the-other-boards-move-once-and-the-script-goes | None
the-round-is-handed-its-step-not-the-manual | container: every child done — pearde collect closes it
the-round-is-handed-its-step-not-the-manual/collect-reads-the-worker-s-report-and-routes-its-own-verdict | None
the-round-is-handed-its-step-not-the-manual/pearde-next-prints-the-step-and-the-decision-it-owes | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
the-round-runs-in-a-window-that-ends | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
the-sweep-leaves-nothing-unregistered | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
the-tool-keeps-its-word | container: every child done — pearde collect closes it
the-tool-keeps-its-word/collect-keeps-its-word | None
the-tool-keeps-its-word/guard-on-is-one-command | None
the-tool-keeps-its-word/one-predicate-for-dispatchable | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `resources/board/plan.py`, which clashes with `resources/board/plan.py`
the-vault-ignores-the-paths-the-board-writes | None
the-view-row-names-a-variable-that-exists | None
the-whole-machine-is-worked-as-one-board | container: every child done — pearde collect closes it
the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
two-self-tests-fail-on-timing-not-on-code | None
upgrade-leaves-the-memo-index-stale | None
upgrade-says-two-contradictory-things | None
view-components | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `resources/board/ramp.py`, which clashes with `resources/board`
view-source-split | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `resources/board/ramp.py`, which clashes with `resources/board`
view-user-extensions | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `resources/board/ramp.py`, which clashes with `resources/board`
workflows-on-the-board | container: every child done — pearde collect closes it
workflows-on-the-board/workflow-attach | footprint: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore is claimed and holds `references/parts/contract.md`, which clashes with `references/parts/contract.md`
workflows-on-the-board/workflow-format | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
workflows-on-the-board/workflow-improve | None
workflows-on-the-board/workflow-reader | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
workflows-on-the-board/workflow-seed | None
workflows-on-the-board/workflow-skill | footprint: the-master-ramp-measures-its-own-tree-not-its-members is claimed and holds `references/files.md`, which clashes with `references/files.md`
1830:def unscanned_need(prds, d, board=None):
3
282:            if planlib.unscanned_need(prds, d, board):
references/parts/master.md:1
references/parts/contract.md:1
resources/board/lanes.py is on disk with no row in references/files.md
