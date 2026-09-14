# Plan refresh pass — 2026-09-14 (parked)

Scope authorized by the user: re-review every open PRD whose review was stale or missing,
reconcile each against current decisions and the route taken since it was written, and
disposition the 15 unfinished work items that had no PRD. Reviews were agent reviews
(threshold 90, five rounds); no product gates were run. `./prd check`: 233 records, no problems.

Per-PRD results are in each `prds/<slug>/review.md` (new round with a verdict: CURRENT,
REBASE, DELIVERED, SUPERSEDED or CONFLICT) and in the frontmatter `review-status`.
`state:` was not changed anywhere; nothing was retired or closed.

The pass was parked on request of another session before the integration step.

## Route findings (verified)

- cartridge.ctg ee7e295 removed `provide`, `call`, the Rust SDK and wire.ts. On main every
  cartridge still uses that API. The port to the events model is in flight on
  `/Users/feb/dev/cartridge-worktrees/ws/<name>.ctg` branch `transport`, guided by
  `cartridge-worktrees/coordination/PORTING.md`. Merging it is a prerequisite for implementing
  any PRD; it needs no PRD of its own.
- cartridge.ctg local main and origin/main (= transport-design) have diverged from b02b200.
  The root gitlink still records d2a761e. See
  `runtime/prds/the-runtime-reaches-top-tier-quality/the-in-flight-rewrite-lands-in-reviewable-commits`.
- The fabric graph is in memo (`memo.ctg/src/fabric_graph.rs`, crate `memo.ctg/evidence`), not in
  core. The decision memo `.cartridge/memos/decision/the-fabric-lives-in-core.md` is outdated.
- The `ui` board targets `tui.ctg`; the `landscape` board's PRDs now target memo (or
  sessions/pty/router for the context providers).

## Decisions waiting on the user

1. Document execution (runtime/one-runner-executes-documents and its three children):
   A each owner declares its own `tool.<name>` and runs its memo in its own grant (recommended);
   B memo runs every recipe under a broad grant; C the base runs tool memos; D retire execution.
   Related: the mcp/agent/proxy/fs/gitfs/memo/router/sessions "document" client PRDs.
2. File write confinement (policy/improve-policy-resource-scope): A fs and gitfs confine their
   own writes with no-follow opens (recommended); B policy returns a scope from config.lua;
   C narrower sandbox grants only.
3. Shipped policy default (…/the-shipped-policy-defaults-to-ask): A keep allow and retire;
   B policy declares ask, root keeps explicit allow (recommended); C setup writes ask.
4. On-demand provider start (runtime/a-key-starts-its-provider-on-demand): A retire;
   B lazy opt-in; C idle stop. Blocks runtime/cartridges-compose-recursively.
5. CI location (runtime/ci-proves-the-supported-terminal-matrix): no remote, Linux refuses
   cartridges today. Blocks runtime-stays-small-and-provable.
6. runtime/semantic-tool-recovery-retires-failed-generations: retire (recommended), new LSP
   cartridge, or park.
7. memory/memory-signals-become-events: name a consumer or retire.
8. work/event-fabric: scope call deferred by memo to the user.
9. Live model spend for agent/improve-agent-task-baseline.
10. Decisions `the-agent-can-diagnose-and-extend-its-runtime` (promises removed debug mode) and
    `the-agent-surface-preserves-the-visible-shell` (tui ships a split view) need refresh.

## Remaining integration (not done)

- Apply retire / delivered dispositions only after user approval; verify delivered items with
  their owner gates first.
- Rehome: landscape PRDs -> memo (providers -> sessions/pty/router); tools-* runtime leaves ->
  tools; every-enabled-tool and tool-probes -> runtime; fabric query -> memo; memory lock ->
  memory; per-cartridge-versioned-test-runner -> root; policy default PRD -> policy.
- Re-reconcile parents whose children changed after their round:
  mcp/clients-share-document-execution (passed CURRENT, children superseded),
  runtime/documents-own-live-processes, root/the-composed-system-proves-the-plan (82 FAIL),
  root/cartridge-improvement-programme (85 FAIL), runtime/the-runtime-reaches-top-tier-quality.
- Missing PRDs: harness projects journal events by declared type; harness coalesces bursts of
  board posts into one run.
- work-map.json: add rpc-contracts-run-across-rust-lua-and-bun (runtime), the three context
  providers and the three root PRDs never mapped; update changed needs and canonical paths.
- Drop resolved needs listed in the work-item disposition below.
- Frontmatter key `capability-capability-owner` remains in about 60 PRDs.
- Refresh BACKLOG.md, PROGRESS.md and OPEN-WORK-REVIEW.md from the new review statuses.

## Reviewer results (raw)

## g9 small boards (done)
fs/direct-fs-document SUPERSEDED; gitfs/gitfs-document SUPERSEDED; memo/improve-memo-programme DELIVERED; memo/landscape-live-owner-context-facade REBASE 91 PASS; memo/memo-write-document SUPERSEDED; policy/improve-policy-programme CONFLICT; policy/improve-policy-resource-scope CONFLICT (options A fs/gitfs self-confine [rec], B policy scope via config.lua, C sandbox grants); proxy/proxy-document-client SUPERSEDED; router/router-document SUPERSEDED; tools/development-tooling-has-one-home SUPERSEDED.
Cross-board: document-runner programme (root/capabilities-live-with-their-owners, mcp/clients-share-document-execution, runtime/one-runner-executes-documents) likely superseded — inference, needs user confirm. live-owner-evidence-adapters needs inversion + rehome. runtime-development-package retire; development-clean-checkout rebase. Frontmatter typo `capability-capability-owner` in 68 PRDs. memo facade lacks review-migration.json.
## g8 pty/harness/mcp (done) — all 10 PASS
harness-consumes-landscape REBASE r3 90; improve-harness-programme CURRENT r4 93; improve-harness-quality-eval REBASE r3 93; mcp/clients-share-document-execution CURRENT r4 91; improve-mcp-programme CURRENT r4 93; improve-mcp-tool-readiness REBASE r3 92; pty/improve-pty-command-wait REBASE r3 93; improve-pty-input-ownership REBASE r3 93 (mostly delivered cacd7e1, narrowed); improve-pty-programme CURRENT r4 93; pty-document REBASE r3 91.
CONTRADICTION: g8 kept mcp/clients-share-document-execution CURRENT+PASS; g9 thinks document-runner programme SUPERSEDED. User decision.
Cross: landscape context-comparison-gate/baseline-corpus target dissolved lib; unqualified needs memory-document-works-end-to-end; ui->tui names; leaf gates start red (release-status failures). `./prd check` root graph: 229 records ok.
## g5 ui (done) — all 12 REBASE, r3 FAIL -> r4 PASS (90-93), 1 round left each
copy-mode 90, human-context 90, improve-ui-programme 92, run-history 93, terminal-owner 91, tool-availability 90, embedded-terminal-is-gone 92, gutter-is-the-boundary 90 (merge into the-inline-agent recommended), gutter-shows-both-sides 92, the-inline-agent 92, panel-switches-to-a-sub-agent 91, ui-paints-the-grid 92.
Findings: old links to ui.ctg, `just test ui` -> "Unknown owner: ui"; now tui.ctg/tui gates. Board dir still named ui. pty grid frames delivered pty main.rs; tui still EmbeddedTerminalRenderable. root--pty-encodes-input looks delivered. Decision the-agent-surface-preserves-the-visible-shell + tui inline-agent-overlay describe surface tui doesn't ship -> decision refresh needed. capability-capability-owner typo fixed in ui board only.
## g7 landscape+sessions (done) — 10 PASS, 1 DELIVERED
landscape: search-ranks-current-guidance REBASE 92; usage-ranked-tool-graph REBASE 90; context-quality-is-measured REBASE 90; landscape-composes-system-context REBASE 92; one-search-covers-record-and-memory DELIVERED (verify just test memory/memo); recursive-development-graph REBASE 91. All repo->memo.ctg, owner memo; should move to memo board.
sessions: board-message-is-reference REBASE 91; sessions-document REBASE 90; agents-chat-through-one-tool REBASE 90; board-log-replays REBASE 90; swarm-talks-on-a-board CURRENT r4 91.
Found: fabric in memo not core (digest corrected, reviewers told). Stale landscape children: context-baseline-corpus, context-comparison-gate, recursive-source-refresh, live-file-context-contributors. Need harness leaf for burst-post coalescing. root--the-board-is-channels-of-lines delivered (sessions channels.rs).
## g6 root (done; resumed for fabric correction)
capabilities-live-with-their-owners REBASE 90 PASS; cartridge-improvement-programme REBASE 85 FAIL; every-enabled-tool-ships-a-contract-probe REBASE 91; fabric-query-times-out REBASE r1 90 (reproduce first else retire); memory-document-works-end-to-end REBASE 90; memory-tool-refuses-reads REBASE r1 90; the-composed-system-proves-the-plan REBASE 82 FAIL; the-vision CURRENT r4 91; tool-probes REBASE 90 (mostly delivered); unit-process-tests SUPERSEDED (939e7d1 deleted process.rs).
Rehome: every-enabled-tool+tool-probes->runtime, fabric query->memo, memory lock->memory. 3 new-reviewed PRDs missing from work-map. rpc-contracts PRD links missing review.md.
## g1 runtime A (done) — 7 PASS, 2 FAIL, 2 SUPERSEDED, 1 DELIVERED, 2 CONFLICT
installs-from-its-source REBASE 92; key-starts-provider-on-demand CONFLICT (A retire / B lazy opt-in / C idle-stop; eager wave start today); listener-subscribes-to-event-types REBASE 92 (mostly delivered); plugins-ingests-unwind SUPERSEDED; ancestry-test REBASE 93 (->tools); cartridges-compose-recursively REBASE 88 FAIL (waits on on-demand decision); ci-proves-terminal-matrix CONFLICT (no remote; linux refuses cartridges; pick CI location); development-clean-checkout REBASE 90 (manifests call missing recipes); disk-adapters-detach SUPERSEDED; documents-own-live-processes REBASE 85 FAIL; extension-inspect DELIVERED (just test runtime); extension-loader-plugin-tree REBASE 94; tools-bundle-provenance REBASE 91 (->tools); tools-preflight REBASE 92 (->tools).
Cross: tools/development-tooling-has-one-home needs runtime-development-package, contradicts decisions. agent an-event-declares-its-type links missing model_loop.rs. root memo a-cartridge-declares-what-it-needs covered by loader/document.rs.
- g6 recheck: no score change; removed 3 links to outdated decision the-fabric-lives-in-core. TODO coordinator: correct/supersede that decision memo.
## g2 runtime B (done) — 7 PASS, 3 FAIL, 2 SUPERSEDED, 1 CONFLICT
improve-tools-programme REBASE 90 (->tools); tools-worktree-resume REBASE 93 (->tools); launch-authority REBASE 91; linux-policy REBASE 91 (OrbStack/Lima runner); macos-policy REBASE 93; one-runner-executes-documents REBASE 82 FAIL (runner belongs in cartridge, memo rec.); per-cartridge-versioned-test-runner REBASE 90 (->root); plugins-from-memory-toml SUPERSEDED; runtime-development-package SUPERSEDED; runtime-stays-small-and-provable REBASE 88 FAIL; second-harness-composition-proof REBASE 91; semantic-tool-recovery CONFLICT (retire rec / new LSP cartridge / park); the-runtime-reaches-top-tier-quality REBASE r1 84 FAIL (13 children unreconciled); the-sandbox REBASE 91.
Cross: nested children unreviewed (one-runner 3 children, top-tier 13 children). tools lane.test.ts uses missing cartridge.ctg/builtin.
## g3 memory (done) — 16 PASS, 1 FAIL, 1 DELIVERED, 1 SUPERSEDED
degrade 92; improve-memory-programme CURRENT r4 92; tool-correct 91; tool-errors 93; tool-get 93; tool-programme 93; keep-tree-and-record-true 90; memory-002 92; memory-004 92; daemon-boots-root-context 90; memory-integration-assessment SUPERSEDED; memory-owns-its-tool DELIVERED (src/cartridge.rs, 9e4cde8); memory-signals-become-events 86 FAIL (needs consumer or retire — user); multimodal 90; parked-memory 92; retrieval-is-a-piece 91; agent-surface-is-usable 92; graph-converges 94; track-record-across-stores 92.
Needs: tool-correct +tool-get; parked-memory -memory-004. memory-adapter-core blocks 4 leaves but looks delivered.
## g10 15 unmapped work items (done)
DELIVERED: a-cartridge-declares-what-it-needs, agents-query-the-tool-graph, every-tool-is-one-command, pty-encodes-input, context-is-living-not-per-session, the-palette-and-exit.
SUPERSEDED: a-nested-cartridge-is-a-first-class-entry, the-sidebar-slides-over-the-shell, debug-mode-opens-and-closes-from-the-shell.
COVERED: fresh-checkouts (->runtime/ci-proves...), terminal-profile-starts-only-needed (->runtime/a-key-starts...), the-agent-can-extend-and-verify (->root/the-composed-system...), the-terminal-is-drawn-from-pty (->ui children).
NEW-PRD: runtime/rpc-contracts-run-across-rust-lua-and-bun r3 92 PASS (root draft kept, superseded-recommend-retire). Not in work-map.
CONFLICT: event-fabric (memo defers to user scope call).
Implementation findings: wire.ts copies in tui/live/auth/prd target protocol dropped in ee7e295; tui init.lua calls old cartridge.process; most cartridge.json still declare `provide` which loader ignores (likely smoke failures). Decision the-agent-can-diagnose-and-extend-its-runtime promises removed debug mode.
Needs cleanup: resolved prereqs in runtime/a-key-starts, runtime/a-cartridge-installs, runtime/ci-proves, ui/the-ui-paints-the-grid, ui/the-panel-switches, root/every-enabled-tool.
## g4 agent (done) — 10 PASS, 2 FAIL, 1 SUPERSEDED
live-run-accepts-events-from-outside 90; priority-event-unblocks-the-step 91; stalled-step-raises-own-event 91; agent-document-client SUPERSEDED; an-event-declares-its-type 86 FAIL (needs harness projection PRD); debug-mode-correlates-a-terminal-turn 85 FAIL (children not rebased onto cartridge verify/doctor); decision-attribution 92; improve-agent-programme 92; resume-boundaries 93; task-baseline 90 (live runs need user approval to spend); sub-agents-share-the-terminal 90; spawns-wakes-owns-sub-agents 90; run-is-a-stream-of-typed-events 90.
Missing PRDs: harness projects journal events by declared type. review-inputs.json + work-map canonical_prd still point at old agent.ctg/.cartridge/prds paths.
## ROUTE FINDING (coordinator verified)
Event-model port in flight on ws/<name>.ctg branch `transport` (coordination/PORTING.md); all 18 declare events; 6 dirty (agent, mcp, pty, router, sessions, tools). Main still on removed provide/call API -> main doesn't run. No port PRDs needed; merge of transport branches is the prerequisite for all implementation. Unmerged shared-checkout edits also dirty on main: cartridge, fs, pty, router, live, tui (another session).
## g11 top-tier children (done)
DELIVERED: lua-restricted-environment, lua-calls-without-blocking, documents-describe-this-checkout, host-logs-through-tracing, socket-name-stable-file-private.
SUPERSEDED: stream-and-process-edges-bounded-and-loud.
CONFLICT: shipped-policy-defaults-to-ask (A keep allow+retire / B policy default ask, root keeps explicit allow, move to @policy [rec] / C setup writes ask).
PASS r2: dependencies-released 93, failures-carry-a-type 91, no-panic 91, one-function-per-command 90, in-flight-rewrite-lands (now: reconcile local main with origin/main) 90, unit-suite-offline 90. Self-reviewed.
DIVERGENCE (verified): cartridge.ctg local main 3 ahead / 10 behind origin/main (=transport-design), merge-base b02b200. Root gitlink still d2a761e.
## g12 nested children (done)
PASS REBASE: context-baseline-corpus 91, context-comparison-gate 92, live-owner-evidence-adapters (now rollup) 91, live-file-context-contributors 92, document-event-activation 91, document-sidecar-lifecycle 91. NEW: session-context-provider 91, terminal-context-provider 90, route-context-provider 92.
DELIVERED: recursive-source-refresh, memory-adapter-core, memory-wrapper-retirement.
SUPERSEDED: mcp client-document-contract, mcp-document-client, memory-consumer-parity.
CONFLICT: one-runner children x3 — executor choice A owner cartridge declares tool.<name> in own grant [rec] / B memo runs all under broad grant / C base runs tool memos (contradicts slim core) / D retire execution, keep memo-run.
Fix: mcp/clients-share-document-execution parent passed CURRENT but children superseded -> re-reconcile. memory port 6889302 deleted second-writer test.
