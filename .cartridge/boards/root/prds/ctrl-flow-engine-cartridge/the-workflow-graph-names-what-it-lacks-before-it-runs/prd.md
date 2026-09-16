---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: the-workflow-graph-names-what-it-lacks-before-it-runs
---

# The workflow graph names what it lacks before it runs

Port the flow engine's pure core: the graph as data, `apply` as the only mutation, readiness derivation, and the document round trip. A flow that is missing a credential, a cron string or a connector type is stored and reports exactly those gaps; it is never refused for being incomplete and never fails at execution for something that could have been named at authoring time.

Malformed structure and absent configuration stay distinct: the first is rejected and never stored, the second is stored and reported. There is no third category. Named flow templates build on this: a template is a builder producing a change set for a named sub-graph, so a recurring job is a graph an agent stages rather than a script someone wrote by hand.

## Acceptance

- [ ] A graph with a missing credential, an empty cron and an unset connector type is stored, and readiness reports one named requirement per gap, identifying the node and the field.
- [ ] A structurally invalid change (unknown node reference, a link whose port pair the matrix forbids) is rejected with a typed error naming node, field and cause, and nothing is written.
- [ ] A change set is applied whole or rejected whole: no partial application is observable after a rejected change.
- [ ] A graph written as a document, read back, and re-applied produces an identical graph.
- [ ] A named template stages the flow `Trigger(Schedule) -> Connector -> Store` from a spec, deriving stable node ids from the flow name, and re-staging the same name twice is idempotent.
- [ ] All of the above run offline in `just test flow`, with no network, no service and no model.

## Proof and recovery

Baseline: nothing in the composition holds a workflow graph. Port from upstream `ctrl` `src/domain/` (graph, node, link, change, readiness, validate, error, id), `src/author.rs` and `src/template.rs`, all pure and IO-free upstream. Keep them IO-free here: this child adds no transport, no store and no model.

Gates, cwd `/Users/feb/dev/cartridge`: `just test flow`, `just check flow`. Not run for this plan.
