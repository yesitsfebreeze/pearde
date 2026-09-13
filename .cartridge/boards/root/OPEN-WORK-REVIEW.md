# Open work review

159 original open plans map to **180 small PRDs: 139 executable leaves and 41 parents/milestones**. Twelve overlapping historical proposals share canonical scopes. Original files and round-1 evidence are retained.

Round 2 self-review: **178 PRDs pass the 90/100 plan threshold; 2 fail**. Implementation remains open. New specs or changed contracts require another review within the five-round allowance.

| Failed PRD | Score | Unresolved prerequisite |
| --- | ---: | --- |
| [linux-policy — Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement.](../runtime/prds/linux-policy/prd.md) | 86 | Linux enforcement needs a real runner with a recorded kernel/Landlock ABI; this checkout supplies only a refusal implementation. |
| [semantic-tool-recovery-retires-failed-generations](../runtime/prds/semantic-tool-recovery-retires-failed-generations/prd.md) | 80 | No maintained editor/LSP provider and teardown API has been identified in the current runtime/tooling owners. |

## Work by owner

- [root](BACKLOG.md)
- [runtime](../runtime/BACKLOG.md)
- [memory](../memory/BACKLOG.md)
- [agent](../agent/BACKLOG.md)
- [fs](../fs/BACKLOG.md)
- [gitfs](../gitfs/BACKLOG.md)
- [harness](../harness/BACKLOG.md)
- [landscape](../landscape/BACKLOG.md)
- [mcp](../mcp/BACKLOG.md)
- [memo](../memo/BACKLOG.md)
- [policy](../policy/BACKLOG.md)
- [proxy](../proxy/BACKLOG.md)
- [pty](../pty/BACKLOG.md)
- [router](../router/BACKLOG.md)
- [sessions](../sessions/BACKLOG.md)
- [tools](../tools/BACKLOG.md)
- [ui](../ui/BACKLOG.md)

[Canonical source map](work-map.json) · [Round-1 inventory](reviews/round-1/inventory.json) · [Validation](reviews/validation.md) · [Review method](../../workflows/review-plan.md)

Scores are attributed agent judgments of the plans, not product-test results. No source claim was reassigned, no implementation was marked complete, and no user score was invented.

PRD, dependency, workflow and grammar validation pass. The full board check is
blocked by the concurrent native-memo migration's metadata mismatch; details are
in the validation record.
