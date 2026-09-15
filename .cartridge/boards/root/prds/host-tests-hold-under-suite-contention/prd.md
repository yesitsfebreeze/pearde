---
state: "analyzing"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 2
date: "2026-09-15"
footprint:
- "cartridge.ctg"
needs:
- the-profile-is-the-orchestration-service
- the-gates-run-from-the-root-justfile
claim: "cartridge-ctg-22 2026-09-15T09:00:19.848Z"
---

# Host tests hold under suite contention

## Outcome

The host's own check and test gates are green when the whole suite runs at once.

## Acceptance

- [ ] `just check cartridge` exits 0 (2026-09-15: rustfmt diff in `.cartridge/tests/unit/src/host/socket.rs`).
- [ ] `just test cartridge` exits 0 on three consecutive runs with the suite in parallel; `$CARTRIDGE_HOME` is set per test, never process-global; the `cli::setup` and `cli::trust` tests pass on macOS CI.

## Folds

Deferred with `superseded-by` pointing here:

- @root/unit-process-tests-time-out-and-redden-under-suite-contention-after-the-settings-refactor-raised-startup-timeout-to-60s
- root memo `prd/the-binary-target-passes-on-a-runner`

## Result

Dispatchable as of 2026-09-15 and not started: its footprint is held.

cartridge.ctg carries 30 uncommitted changes belonging to two other sessions,
neither of them this one.

One session is running a review-and-fix pass there. It reports its own part
finished and green: formatting and clippy clean, 152 library tests passing,
and it confirmed the remaining failures are not its own by checking `891a2c2`
into a separate worktree, applying only its files and running the suite there,
where 15 of 15 binaries passed. It is deliberately not committing, because four
CLI tests are red from the other session's host work and committing now would
put that red on main.

The other session holds the host files and is working those four failures with
the diagnosis in hand. When it lands, the first session commits immediately.
Dispatching a worker into those trees would either build on work that is still
moving or overwrite it, and the acceptance here is about whether the suites are
green, which cannot be judged at a revision that does not exist yet.

This clears the moment the owning session commits. Nothing about this item is
otherwise blocked: the composition starts, the gates report per target, and
`just test` already names exactly which of these owners are red.
