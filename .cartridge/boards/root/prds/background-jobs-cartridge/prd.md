---
state: open
origin: requested
priority: 30
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: background-jobs-cartridge
footprint:
  - "jobs.ctg"
---

# Background jobs outlive the call that started them

`pty.ctg` owns the one visible terminal, so a dev server, a watcher or a long ingest started there holds the surface the user is working in. Nothing in the composition owns a job that should run beside the session instead of inside it. Port pi's `launch` as `jobs.ctg`.

Each job runs in its own process group with a ring buffer and a log file, so its output is readable without it being attached to anything, and the group is what gets signalled when the job is stopped. Jobs die with the session that started them: a background process surviving its session is a leak, not a feature. A failed job is reported as failed and stays readable rather than being cleared.

## Acceptance

- [ ] A started job runs in its own process group, and stopping it terminates the whole group, verified by the group having no surviving member.
- [ ] A job's recent output is readable from its ring buffer while it runs, and its full output from its log file after it ends.
- [ ] Every job is killed when its session ends, including a job whose child re-parented itself, verified by no surviving process in the recorded group.
- [ ] A job that exits non-zero is reported as failed with its exit code and remains readable; it is not cleared by the next start.
- [ ] A health report names the failed jobs and their count, and reports no jobs as a skip rather than a pass.
- [ ] Start, read, stop and cleanup are tested offline in `just test jobs` using short-lived fixture commands.

## Proof and recovery

Port from `/Users/feb/dev/pi/packages/coding-agent/src/core/launch.ts` (482 lines at survey, verified present). Upstream registers a health check through its extension API; here that report is exposed as an operation the composition's own diagnostics read.

Sequenced after `repo-checks-cartridge` in the roll-up so a long check runs detached.

Gates, cwd `/Users/feb/dev/cartridge`: `just test jobs`, `just check jobs`. Not run for this plan.
