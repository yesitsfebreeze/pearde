---
state: open
origin: requested
priority: 30
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: a-trigger-fires-a-flow-from-a-schedule-or-a-signal
footprint:
  - "flow.ctg"
---

# A trigger fires a flow from a schedule or a signal

A reusable flow is only reusable if something other than a person can start it. Port the trigger surface: a `Schedule` trigger compiles to a crontab line that runs the flow, an `Event` trigger fires from a signal the composition already publishes, and a `Manual` trigger waits for a person.

The cartridge owns no clock. A schedule is emitted as crontab lines inside a marker-delimited block keyed by the flow document's absolute path, so re-installing the same document replaces its own block instead of appending a duplicate. Event triggers subscribe to declared events from the composition rather than polling. A trigger that cannot produce a line — an empty cron, an event no cartridge declares — is reported as skipped with its reason, never emitted as a line that a crontab would reject or silently mis-parse.

## Acceptance

- [ ] A graph with two `Schedule` triggers emits one crontab line each, in graph node order, each line naming the flow document and the trigger id.
- [ ] Installing the same document twice leaves exactly one marker-delimited block for it; a second flow document adds its own block and does not disturb the first.
- [ ] A `Schedule` trigger with an empty or whitespace cron emits no line and is reported as skipped with its reason; `Event` and `Manual` triggers emit no line and are reported as carrying no clock.
- [ ] An `Event` trigger naming a declared composition event starts its flow when that event is published, and one naming an undeclared event is refused at authoring time with the event name in the error.
- [ ] Emission is pure and offline in `just test flow`: no crontab is read or written, no clock is read, and the caller supplies the absolute paths.

## Proof and recovery

Port from upstream `ctrl` `src/schedule.rs` (172 lines at survey), which is already the pure half — graph plus paths plus forwarded flags to crontab lines, with the `crontab -l` / `crontab -` invocation left to the composition root. The `Event` half has no upstream implementation to port: upstream fires events off an external knowledge tool's signal, and here it binds to the composition's own declared events, which is new work.

Depends on the workflow graph child for the `Trigger` node and on the ingest-walk child for the run it starts.

Gates, cwd `/Users/feb/dev/cartridge`: `just test flow`, `just check flow`. Not run for this plan.
