# Native planner completion

2026-09-13. Source owner: Analyze plan rating, thread
`01a097e6-4d34-7390-b55f-23792b974627`. Coordination acknowledged to PRD consolidation
thread `01a099c9-c11d-7a20-8805-b3aec5651ae2`; no competing source relocation occurred.

The engine, service and CLI share the maintained TypeScript/Bun implementation.
Project Python has been retired. The preserved `prd-relocation-inputs` snapshot is
`76c49b60c927d1c4dd688f08ba66cf2e5367493c`; the upstream worktree and personal state
remain separate. Migration validation still preserves 182 PRDs and 386 native
work/question states. Backlog acceptance is not implementation completion.

The handoff fixes cover recursive current-contract proof, member ownership and
capacity, checked collection of returning owned workers, foreign claims, partial
run receipts, confirmed process-group cleanup, committed source footprint checks,
serialized response limits, strict memory acknowledgments and live domain events.
The shipped MCP profile now exposes the same PRD service.

The independent [revision-bound review](native-typescript-final-parity-review.md)
preserves failed findings and the passing recheck. Review uses the canonical
[90/100, five-round method](../workflows/review-plan.md); this does not change any
other plan's score or used rounds.

Validation of the final source:

- Full planner suite: **57 passed, 5,080 assertions**; TypeScript check passed.
- Actual runtime, memory and MCP fixtures pass with isolated stores and a local
  deterministic embedding endpoint. No remote model or worker was invoked.
- Event suite repeated ten times: **60 passed, 790 assertions**. An additional
  100 disposable Unix-socket lifecycle probes passed.
- `just check all` and `just layout` pass for the composition and 22 cartridges.

Repeated tests exposed `EPIPE` on the former extra-descriptor event channel even
with its parent alive. Explicit EOF waiting alone did not correct that transport.
A private per-invocation Unix socket now owns connection, buffering, drain and
cleanup; limits and delivery failures remain visible. This is observed behavior
on Bun 1.3.14/macOS, not a claim about every Bun version or an upstream root cause.

The maintained installer/statusline memos migrated the local `prd`, `pearde` and
Claude statusline consumers. Previous configuration is backed up under
`~/.local/state/cartridge/planner-migration/1789295827065`. `prd check --json`,
`pearde help` and statusline rendering pass. Legacy names use the documented
native CLI; ancillary authoring stays in memos. Remote adapters, other operating
systems and full legacy UI equivalence were not established by these fixtures.
