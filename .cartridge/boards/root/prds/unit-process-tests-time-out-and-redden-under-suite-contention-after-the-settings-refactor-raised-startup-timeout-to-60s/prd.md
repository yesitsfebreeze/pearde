---
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
superseded-by: "@root/host-tests-hold-under-suite-contention"
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge"
review-round: 1
review-status: superseded-recommend-retire
---

# Unit/process tests time out and redden after settings refactor raised startup_timeout.

After the settings refactor landed the default host startup_timeout is 60
seconds. Tests that exercise a child that never becomes ready now take the full
60s to fail (e.g. tests::process::a_child_that_stays_alive_without_ready_
times_out_and_is_reaped passes in isolation but takes 60s). Under full-suite
contention several process/stream tests run past their local tokio::time::timeout
wrappers and redden: slow_stream_handlers_..., a_child_that_stays_alive..., and
stdout_closed_live_children_... — some reported hangs >60s.

This makes the unit suite slow and flaky rather than wrong in one place.

## Outcome

The unit suite finishes in normal time and the process/stream timeout tests
fail fast against a short synthetic timeout instead of waiting on the real 60s
default, without regressing the actual host default behavior.

## Acceptance

- [ ] A child that never becomes ready fails within ~seconds in the test, not
      60s, by injecting a small startup timeout into the test fixture rather
      than changing the host default.
- [ ] cargo test --lib completes without any test exceeding its tokio::time
      wrapper or hanging; the previously-red process/stream tests pass.
- [ ] The host's real default startup_timeout remains 60s (or whatever the
      intended production value is) — the fix is test-side injection, not a
      production slowdown.
- [ ] No test asserts behavior that only holds at the production default where
      a short timeout is now injected.

## Proof and recovery

The tests boot a Host through crate::lua tests; confirm the boot path lets a
test override settings::host() keys (or takes the profile config) so a fixture
can set host.startup_timeout_secs low. Start at .cartridge/tests/unit/src/tests/
process.rs (unready_fixture) and the boot() helper.
