# root work items

One plan, four waves, three milestones. Everything else on every board is
`deferred` as of 2026-09-15 with `deferred-from` and, where folded,
`superseded-by` pointing at the item here that replaces it. A deferred item is
not picked up; it is re-added on this board if it is still wanted after the
milestone that would have needed it.

| Wave | PRD | Kind | Needs |
| --- | --- | --- | --- |
| 1 | [The profile is the orchestration service](prds/the-profile-is-the-orchestration-service/prd.md) | leaf | — |
| 1 | [The record has one vocabulary and no shadowed copies](prds/the-record-has-one-vocabulary-and-no-shadowed-copies/prd.md) | leaf | — |
| 1 | [The gates run from the root justfile](prds/the-gates-run-from-the-root-justfile/prd.md) | leaf | — |
| 2 | [Sessions and gitfs tests are green](prds/sessions-and-gitfs-tests-are-green/prd.md) | leaf | profile, gates |
| 2 | [pty, router, harness and mcp tests are green](prds/pty-router-harness-mcp-tests-are-green/prd.md) | leaf | profile, gates |
| 2 | [Host tests hold under suite contention](prds/host-tests-hold-under-suite-contention/prd.md) | leaf | profile, gates |
| 2 | [Smoke passes mcp and proxy](prds/smoke-passes-mcp-and-proxy/prd.md) | leaf | the two test items |
| 2 | [One daemon serves the project; run, launch and mcp are instances](prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/prd.md) | parent | host tests |
| 2 | [Every exchange reaches the memory ledger](prds/every-exchange-reaches-the-memory-ledger-and-condenses-on-the-one-daemon/prd.md) | leaf | one daemon, @proxy ledger hand-off |
| 2 | [The gates are green at one pinned set of SHAs](prds/the-gates-are-green-at-one-pinned-set-of-shas/prd.md) | milestone | record, all wave-2 leaves |
| 3 | [A worker launches in tmux through the proxy](prds/a-worker-launches-in-tmux-through-the-proxy/prd.md) | leaf | M1, one daemon |
| 3 | [The orchestrator sees and talks to its workers](prds/the-orchestrator-sees-and-talks-to-its-workers/prd.md) | leaf | M1 |
| 3 | [The orchestrator knows what is in the works](prds/the-orchestrator-knows-what-is-in-the-works/prd.md) | leaf | M1 |
| 3 | [The text door runs one delegation end to end](prds/the-text-door-runs-one-delegation-end-to-end/prd.md) | leaf | the three wave-3 leaves |
| 3 | [The repository answers by text](prds/the-repository-answers-by-text/prd.md) | milestone | text door |
| 4 | [The voice door reaches the orchestrator](prds/the-voice-door-reaches-the-orchestrator/prd.md) | leaf | M2 |
| 4 | [A fresh checkout runs the daemon and the gates](prds/a-fresh-checkout-runs-the-daemon-and-the-gates/prd.md) | leaf | M2 |
| 4 | [run-board dispatches through the orchestrator](prds/run-board-dispatches-through-the-orchestrator/prd.md) | leaf | M2 |
| 4 | [Context holds across a long orchestration](prds/context-holds-across-a-long-orchestration/prd.md) | leaf | M2 |
| 4 | [CI runs the gates on macOS and Linux](prds/ci-runs-the-gates-on-macos-and-linux/prd.md) | leaf | M2 |
| 4 | [The repository drives itself](prds/the-repository-drives-itself/prd.md) | milestone | all wave-4 leaves |

Replanned 2026-09-15 by the user: every composed cartridge runs, memory
included, over one project daemon that every command attaches to as an
instance. A worker is such an instance, so wave 3 waits for the one daemon, and
the exchange ledger lands beside it in wave 2. M1 does not wait for either.
The memory/proxy rename question is closed: `memory proxy` is retired.

Deferred by name and not on this plan: the live `federation.ts` graph folded into the memo
fabric, corrections landing in the record during a turn, every UI or TUI
item, the event fabric, tool-graph ranking (landscape), sandbox policy
(runtime), the upstream-engine board.
