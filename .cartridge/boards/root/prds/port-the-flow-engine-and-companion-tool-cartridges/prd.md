---
state: open
origin: requested
priority: 40
repo: "/Users/feb/dev/cartridge"
work-kind: rollup
canonical-scope: port-the-flow-engine-and-companion-tool-cartridges
needs:
- '@root/ctrl-flow-engine-cartridge'
- '@root/repo-checks-cartridge'
- '@root/background-jobs-cartridge'
- '@root/cli-spec-cartridge'
- '@root/runnable-recipes-cartridge'
- '@root/function-index-cartridge'
- '@root/process-introspection-cartridge'
- '@memory/ingestion-distiller-seam'
- '@policy/bounded-search-guard-rules'
- '@router/measured-model-ledger'
- '@sessions/file-drift-awareness'
- '@harness/reflex-tool-audit-loop'
- '@harness/slim-failed-turn-distillation'
- '@mcp/deferred-tool-band'
---

# Port the flow engine and companion tool cartridges

Roll-up only: coordinate the ported tool surfaces and the improvements they enable in existing cartridges. This parent carries no implementation; each child lands in its own owner board.

Two upstream sources are surveyed and reusable. `yesitsfebreeze/ctrl` is a workflow engine whose graph of Connector, Transform, Route, Store, Capability and Trigger nodes describes a reusable flow — pull the latest from a source, inspect it, split it, ingest the result — that an agent proposes and a person approves before it runs. `yesitsfebreeze/pi` carries a set of self-contained agent tools in `packages/coding-agent/src/core/`, verified present at survey time, whose mechanisms this composition lacks. The value is the mechanism in each: named reusable flows, an ingestion walk that reports every way a chunk failed to arrive, digested output stored with provenance, reaction to schedule and signal, and task dispatch behind approval.

## Acceptance

- [ ] Every linked child is `done` with its own recorded evidence, or retired by its owner-board review with the reason copied into Result.
- [ ] After the last child lands, `just check` and `just test` exit 0 from `/Users/feb/dev/cartridge` at one recorded set of submodule revisions.
- [ ] Result lists, per child, the upstream source revision it ported from and the mechanism it delivered.
- [ ] No child leaves `needs` without its owner-board disposition.

## Work items

### New cartridges

- [The flow engine runs named reusable workflows](../ctrl-flow-engine-cartridge/prd.md)
- [The repository's own checks run as a post-pass](../repo-checks-cartridge/prd.md)
- [Background jobs outlive the call that started them](../background-jobs-cartridge/prd.md)
- [An external command is learned once and driven from its spec](../cli-spec-cartridge/prd.md)
- [A recorded procedure is runnable, not just readable](../runnable-recipes-cartridge/prd.md)
- [A function-level index answers where code lives](../function-index-cartridge/prd.md)
- [A live process is inspectable from the agent](../process-introspection-cartridge/prd.md)

### Improvements to existing cartridges

- [Digested ingest output lands in memory with provenance](../../../memory/prds/ingestion-distiller-seam/prd.md)
- [Unbounded repository searches are refused with a bounded retry](../../../policy/prds/bounded-search-guard-rules/prd.md)
- [Model selection reads a measured cost and latency ledger](../../../router/prds/measured-model-ledger/prd.md)
- [A file changed outside the session is named before it is trusted](../../../sessions/prds/file-drift-awareness/prd.md)
- [The tool surface is audited by use, not by declaration](../../../harness/prds/reflex-tool-audit-loop/prd.md)
- [A failed turn leaves one retrievable line behind](../../../harness/prds/slim-failed-turn-distillation/prd.md)
- [A deferred tool costs its one-line summary, not its schema](../../../mcp/prds/deferred-tool-band/prd.md)

## Sequencing

`repo-checks` first: it is the smallest port and its post-pass verifies the later children's own work. `background-jobs` next, so a long check or ingest runs detached. The remaining new cartridges are independent of each other. The improvement children each touch one existing owner and may land in any order, except that `ingestion-distiller-seam` consumes the flow engine's `Distiller` seam and follows `ctrl-flow-engine-cartridge`.

## Proof and recovery

Baseline: the composition has 18 cartridges (`agent auth cartridge docs fs gitfs harness live lsp mcp memo memory policy prd proxy pty router sessions tools`); none of the mechanisms above is present. Sources verified at survey: `/Users/feb/dev/pi/packages/coding-agent/src/core/` holds `cli/` (889 lines), `rigor/` (542), `recipes/` (933), `mem/` (1132), `reflex/` (461), `slim/` (71), `launch.ts` (482), `search-guard.ts` (201), `model-ledger.ts` (288), `file-touch-tracker.ts` (64). `ctrl` and `splinter` have no local checkout and are cloned from GitHub at port time.

Each child records its own gate. This parent's gate, cwd `/Users/feb/dev/cartridge`: `just check`, `just test`. Not run for this plan.
