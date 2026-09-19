# Contractors execute planner-produced event workflows: review history

Canonical plan: `prd.ctg/.cartridge/boards/root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/prd.md`. Reviewer: `/root/workflow_contract`, an independent planning sub-agent. Threshold is 90/100 with no blockers; maximum is five substantive rounds. No inherited reviews apply to this new workflow scope. Existing tmux-worker reviews remain on their original records.

## Round 1 — 2026-09-19

The reviewer inspected this delivery leaf, the parent workflow contract and the example against the actual ASP, agent, sandbox, filesystem and PRD sources. Score: **95/100**, from dimensions 20, 19, 19, 18, 19. Result: PASS with no blocking findings. This historical assessment preceded the round-two refinements below and does not authorize a later changed contract.

Findings: make semantic tool success explicit, use trusted exact candidate reads rather than numbered or truncated display text, type normalized outputs, test an empty worker event set, and probe workflow-only publication, claim and readiness before collection. These were nonblocking bounded refinements. User correction was applied before review: planner-produced event workflows are the specification; no duplicate prose job spec is generated.

## Round 2 — 2026-09-19

The independent reviewer read the final refinements and confirmed this plan has no blockers. Unchanged runtime, planner and composition scores were explicitly retained after checking the shared-contract implications. The exact final inputs are bound below and in the parent's planning-evidence.json. No implementation or runtime performance is claimed.

| Dimension | Score / 20 |
| --- | ---: |
| Current user value and scope | 20 |
| Ownership and reuse | 19 |
| Dependencies and implementable slices | 19 |
| Observable acceptance and baseline evidence | 19 |
| Failure, recovery and compatibility | 19 |
| Total | **96/100** |

| Input | SHA-256 |
| --- | --- |
| `prd.ctg/.cartridge/boards/root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/prd.md` | `c534a352dd64cdca06667abc78d85f50f07767a0efca8ac539efdc1ed7384668` |
| `prd.ctg/.cartridge/boards/root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-workflows-validate-declared-events-requirements-and-agent-assignments/prd.md` | `23d0ee53a531b9f3a60167695f3e5d2257653b797f667209df851c243c464f6f` |
| `prd.ctg/.cartridge/boards/runtime/prds/contractor-workers-receive-immutable-job-capabilities/prd.md` | `29618214e98bb92c76fb705c5019cb638cc0bb3b3137c796465c932e8597c05b` |
| `prd.ctg/.cartridge/boards/agent/prds/contractor-agents-run-with-a-sealed-event-and-context-set/prd.md` | `f50b80763ec2a1f24dd49d81d07ebde0b273df9f2c655dc91c0bfe891d2352ed` |
| `prd.ctg/.cartridge/boards/root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-workflows-dispatch-and-recover-bounded-event-runs/prd.md` | `78437628c52bf0ff8f8c02a338538c04dcc346bde89908405ccbe3e3fe00dcb0` |
| `prd.ctg/.cartridge/boards/root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/planning-agents-produce-executable-contractor-workflows/prd.md` | `ba5a6521ca5f44b858bef3208bbe118743bafe1bb6785179ca63749e831eee6c` |
| `prd.ctg/.cartridge/boards/prd/prds/prd-collects-contractor-workflow-requirements-directly/prd.md` | `749325635381968d057160273f3fdb5c1dd4a0b617dbe3f16fe55a6c9d9588db` |
| `prd.ctg/.cartridge/boards/root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-event-workflows-pass-the-composed-dispatch-proof/prd.md` | `6c457990f99507c4ee91be9c532485c62ed122c520eea7db659e05c79c645497` |
| `prd.ctg/.cartridge/boards/root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/workflow.md` | `82d99c2b0768ef3a8c8742983cb9f4c310d7cb7b498ccb2b855f3e07e3860119` |
| `prd.ctg/.cartridge/boards/root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/workflow.example.json` | `f84d16dcd4e3d96ca08803768aa34cd41e2eb71958b7bca284ed2a6f5a59ed43` |
| `cartridge.ctg/docs/asp.txt` | `dc0e16529dcaeffbb06d411b01fa5400b12109f361d421daaa84a0447af90402` |
| `fs.ctg/cartridge.json` | `63907657311c422a629f4dabb0807546ee1d4793095c9b81affbf96b895e7a5f` |
| `agent.ctg/src/module.rs` | `9e04f3b9f729c1bb57e6e55696727bdcedded6a0c666a297059a5b5e14680783` |
| `agent.ctg/src/lib.rs` | `7e36d3610f1acd4ebf40d35c071e80c0b91f8544aa7f16389615273bcc5590e1` |
| `cartridge.ctg/src/sandbox/mod.rs` | `0c9759d1c0edc90fcc18b9a206d3f88fdaf755f2b4623414d88e487f869f0d1d` |
| `cartridge.ctg/src/host/process.rs` | `40ffe8f2168a8a1efabc2072edd8030ea21ff2a82b1d063cb2b359af991a1f13` |
| `prd.ctg/src/lifecycle.ts` | `504a35ddf8c48cc6902bca8c29d650af1e334728e549eec897dc5a06dd28a7c7` |

Result: PASS. Unresolved blocking findings: none. Rounds used: 2; remaining: 3. User rating was not requested or invented. The independent ratings concern plan quality, not tested product behavior. No specs exist for contractor jobs beyond the proposed workflow object; delivery leaves remain open for implementation.

Validation from /Users/feb/dev/cartridge: `./task prd check --json` exited zero with 772 records, no problems and no warnings. `./task audit prd` passed hard checks, retaining unrelated dirty-path findings. `./task isolation` passed for 21 cartridges. JSON parsing and the example DAG/assignment check passed; a runtime validator does not exist yet. The live board plan retained existing claims. JEV timed out, so the plan rests on direct evidence rather than a validated JEV decision.

Next action: begin the first bounded admission or host capability probe when its footprint is available. Capture current revisions and narrow discovery footprints before implementation. Material contract changes require another available review round. No unrelated worker claim is reassigned.
