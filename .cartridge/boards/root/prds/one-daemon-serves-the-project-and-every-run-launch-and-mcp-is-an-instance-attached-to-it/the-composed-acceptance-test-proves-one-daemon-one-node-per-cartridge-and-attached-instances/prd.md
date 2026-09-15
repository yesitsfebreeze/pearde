---
state: open
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/sessions-runs-once-in-the-daemon-with-one-buffer-id-space"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/mcp-keys-sessions-and-inflight-calls-by-attached-instance"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/live-attaches-to-the-daemon-instead-of-spawning-its-own"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/prd-journals-and-outbox-replay-once-in-the-daemon"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/agent-runs-key-per-attached-instance-not-per-process"
footprint:
- ".cartridge/tests/"
---

# The composed acceptance test proves one daemon, one node per cartridge and attached instances

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
its "composed test" analysis item. This is the parent's Acceptance, made
runnable as one composed test in cartridge.ctg.

## Outcome

One test composes the full profile, starts instances against it and proves
the parent's four acceptance boxes:

1. With a daemon running, `cartridge run memory '{"op":"status"}'` answers
   without starting any node process (count `cartridge node` children before
   and after).
2. Two `cartridge launch` instances and one `cartridge mcp` leave exactly one
   `cartridge daemon` and one node per composed cartridge.
3. A memory `ingest` from one instance is returned by `query` from another,
   with no writer-lock error; two instances' sessions and pty shells stay
   separate.
4. With no daemon running, two instances started concurrently end up sharing
   one daemon.

## What changes

- A composed test (likely under `.cartridge/tests/`, following the host-tests
  conventions: `CARTRIDGE_HOME` per test, no daemon kills by process name —
  use the documented stop command from the host-attach child).
- The test uses a temporary project/home so it does not depend on a
  developer's live daemon (parent open question: solo/test hosts stay
  self-contained; the test asserts that, too).

## Acceptance

- [ ] The composed test runs green in `just test` (or the gates' suite it
      belongs to) and covers the parent's four boxes.
- [ ] No test in the suite kills daemons by process name; stopping uses the
      documented stop command.
- [ ] The test passes with a dirty developer environment (live daemon running,
      other sessions active) — contention-safe like host-tests-hold-under-suite-contention.