---
state: "open"
origin: requested
priority: 30
repo: "/Users/feb/dev/cartridge"
work-kind: rollup
canonical-scope: ctrl-flow-engine-cartridge
footprint:
  - "flow.ctg"
---

# The flow engine runs named reusable workflows

A recurring job in this composition is a host script or a hand-driven sequence of tool calls: nothing names it, nothing reports what it lacks before it runs, and a failed step leaves an absence rather than a record. Port `yesitsfebreeze/ctrl` as `flow.ctg` so a recurring job is a named sub-graph an agent composes, a person approves, and the engine runs step by step.

The engine's shape, from the upstream source: six node kinds (`Connector`, `Transform`, `Route`, `Store`, `Capability`, `Trigger`), `apply` as the only mutation path, and `readiness(&Graph, &Facts)` deriving per node whether it is ready or blocked by named requirements. An incomplete graph is storable and says exactly what it lacks. The ingest walk performs the authored `Route` and `Transform` nodes and returns every way a chunk did not arrive — unrouted, dropped branch, refused pattern, unreachable target, failed model — as typed data beside the targets. Triggers are `Schedule` (compiled to crontab lines; the OS cron is the clock), `Event` and `Manual`.

Upstream is Rust with two dependencies (`regex`, `rustls`), no async runtime, and a suite that passes offline, which matches this composition's cartridge shape. The knowledge tiers are seams, not dependencies: the `Distiller` and `Claims` seams are filled by `memory.ctg` here, and the upstream `kern-adapter` is dropped.

## Acceptance

- [ ] Each linked child passes its own review and acceptance.
- [ ] Integration: at one recorded `flow.ctg` revision, `just test flow` and `just check flow` exit 0 from `/Users/feb/dev/cartridge` with no network, no model credentials and no external service.
- [ ] A worked example lands end to end: one staged flow that pulls from a filesystem source, transforms, routes and stores, run from its `Schedule` trigger, with its digested output readable from `memory`.
- [ ] Result names the upstream revision ported from and every upstream module dropped, with the reason.

## Work items

- [The workflow graph names what it lacks before it runs](the-workflow-graph-names-what-it-lacks-before-it-runs/prd.md)
- [The ingest walk names every way a chunk did not arrive](the-ingest-walk-names-every-way-a-chunk-did-not-arrive/prd.md)
- [A trigger fires a flow from a schedule or a signal](a-trigger-fires-a-flow-from-a-schedule-or-a-signal/prd.md)
- [The agent stages a flow and a person approves it](the-agent-stages-a-flow-and-a-person-approves-it/prd.md)

Order: the graph first — the other three read its readiness derivation and node model. The ingest walk and the trigger surface are independent of each other once it lands. The agent surface is last: it stages changes against the graph and declares the seams the other children fill.

## Proof and recovery

Baseline: no flow, pipeline or trigger surface exists in the composition. Upstream `ctrl` has no local checkout; clone `yesitsfebreeze/ctrl` at port time and record the revision. Survey observations to re-verify against that revision: one crate, twelve modules under `src/`, one `[[bin]]`, `src/domain/` (graph, node, link, change, readiness, validate, error, id), `src/pipeline.rs`, `src/run.rs`, `src/template.rs`, `src/schedule.rs`, `src/agent/` (six tools, staged-not-applied change), `src/serve.rs` (`POST /api/<op>`).

Gates, cwd `/Users/feb/dev/cartridge`: `just test flow`, `just check flow`. Not run for this plan.
