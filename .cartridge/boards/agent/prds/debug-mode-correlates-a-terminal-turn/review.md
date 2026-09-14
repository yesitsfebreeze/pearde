# The agent tests and diagnoses its own runtime — review

Canonical PRD: [@agent/debug-mode-correlates-a-terminal-turn](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [debug-mode-correlates-a-terminal-turn](../../../root/reviews/round-1/debug-mode-correlates-a-terminal-turn.md): reviewer 85/100; Reconcile. Good child split, but old socket/correlation absence claims need re-probing; connect probe discovery/execution to current owner-document gates.
  Original SHA-256: `84425f4fa287c7f933338d9c4fe967b830627b880f367b4656fd7310bd42b585`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 20 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 20 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: Parent reduced to linked scope and integration acceptance; only leaves are implementation work.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14 (reconciliation and rebase)

Reconciliation verdict: **REBASE**. The goal (decision `the-agent-can-diagnose-and-extend-its-runtime`) stands, but the host changed underneath its children: manifests now declare `selftest`/`integration` contracts run by `cartridge verify` and a `doctor` event run by `cartridge doctor` (cartridge.ctg `b02b200`, `docs/creating-cartridges.txt` CONTRACTS, SETUP AND DOCTOR), and `cartridge.trace()` carries a turn trace ID. Both root probe leaves predate this and still cite `settings.md`/`justfile` via board-relative links.

Presented revision: prd.md SHA-256 `8b5a3fc854cc21d811e7f708bb35c227212f163f327a04d5cfb388bc3f73edb1` (rebased from `aace3a6f837826ac5368602b8ede0ca5b8f242f07c6959feb3432da6a0d1280b`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Parent reduced to outcome, children and integration gate; all four original children accounted for. −2: slug and title still diverge (historical canonical ID). |
| Ownership and reuse | 17 | Integration now targets host `cartridge verify`/`doctor`. −3: every child is root-owned while the parent sits in the agent board; one child is a blocked memo without a PRD. |
| Dependencies and slices | 16 | Needs were unqualified and resolved to nonexistent `boards/agent/prds/every-enabled-tool-ships-a-contract-probe` — now qualified `@root/...` and resolve. −4: `debug-mode-opens-and-closes-from-the-shell` (memo, blocked) has no PRD; both probe leaves are unreconciled with `cartridge verify`. |
| Observable acceptance and baseline | 17 | Concrete end-to-end integration check and gate (`just verify`, `just test runtime` exist in `.cartridge/justfile`). −3: gate composition depends on how children rebase. |
| Failure, recovery and compatibility | 17 | PTY preserved; limitations recorded. −3: no statement on what happens if verify itself hangs or a cartridge lacks contracts. |
| Reviewer total | **85 / 100** | |

Findings and concrete revisions: (1) dead unqualified needs fixed. (2) Restored the two children dropped in migration (shell open/close memo, turn-ID memo) and the context need. (3) Integration rebased on `cartridge verify`/`doctor`.
Blocking findings: (a) the blocked child memo has no PRD; (b) `@root/every-enabled-tool-ships-a-contract-probe` and `@root/tool-probes-run-and-locate-a-failing-provider` must be reconciled against `cartridge verify`/`selftest` (possibly partly delivered) before this parent's gate is final. Both are root-board actions for the coordinator.
Disposition: revise; consider rehoming this parent to the root board with its children.
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **FAIL** (85/100).
Unresolved blocking findings: (a), (b) above.
Rounds used / remaining: 3 / 2.
Next action: coordinator reconciles the root probe leaves and creates or retires the shell open/close PRD; then round 4.
