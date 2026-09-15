---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
needs:
- "@memory/extension-services-provide-and-inject"
- "@memory/extension-events-four-dispatch-modes"
estimate: "2h"
actual: "1h"
---

# plugin config validation before `apply`, `fiber.update(config)` through the `internal/update` waterfall, `fiber.restart()`, and the `internal/config` resolution hook

Landed on main at `2e6f7c7b` (`src/extension/` only): the seven checks and `just test` (1501/1501) green in the lane before landing.

## Do

- `Plugin` gains `fn validate(&self, config: serde_json::Value) -> Result<serde_json::Value, ValidationError>`
  with the identity as default; a plugin with a typed config deserializes
  there and serializes back the normalized value. `reload` resolves the
  config after the injections are committed: first the `internal/config`
  waterfall (a listener may rewrite it — the loader's interpolation hook),
  then `validate`; a `ValidationError` ends the fiber `Failed` without
  running `apply`.
- `fiber.update(config, no_save: bool)` per the vendored `Fiber.update`:
  store the raw config; when the fiber is not `Active`, clear the error and
  `refresh`; otherwise resolve the config and run the `internal/update`
  waterfall whose inner closure sets the config, clears the error and
  restarts — an update listener that does not call `next` vetoes the
  restart. `fiber.restart()` retires the target, refreshes, and awaits
  `settled()`.
- `fiber.config()` returns the validated config the running `apply` saw.

## Spec

The probe built the whole Do and it passes; it is commit `660aff15` on the
branch `agent-aa3de6387b4851b2d` (worktree
`/Users/feb/dev/memory/.claude/worktrees/agent-aa3de6387b4851b2d`, one commit
over `main`). What is left is the landing and the ticking. Files, all under
`src/extension/src/`:

- `lib.rs` — `Error::Validation(String)`; exports `ValidationError`,
  `InternalConfig`, `InternalUpdate`.
- `events.rs` — `InternalConfig` (`Waterfall`, args `(u64, Value)`, ret
  `Value`) and `InternalUpdate` (`Waterfall`, args `(Value, bool)`, ret
  `Result<(), Error>`).
- `plugin.rs` — `Plugin::validate` (identity default), `ValidationError(pub
  String)` with `From<serde_json::Error>` and into `Error::Validation`;
  `Load { plugin, raw: Mutex<Value>, config: Mutex<Value> }`;
  `resolve_config` (waterfall, then `validate`) called in `reload` after the
  view is committed and `Loading` is set; `Fiber::config`, `Fiber::restart`,
  `Fiber::update`; the transition loop unloads a stale `Loading` fiber before
  it reloads.
- `tests/config_test.rs` (new) and `tests/mod.rs` — six tests.

Four shapes the Do names could not be written as written. `ValidationError` is
a newtype over the message and not an `Error` variant, because `validate`
returns it and `FiberState::Failed` holds an `Error`; the `From` bridges them
and a `serde_json::Error` converts, so a typed config is one `?`. The
`internal/config` waterfall carries `(uid, config)` and is unfiltered, as the
vendored `waterfall(this, 'internal/config', …)` is — a fiber target has no
filter in Cordis. The `internal/update` waterfall targets the fiber's own
context filtered to hooks whose context sits on that fiber, `global` admitted
always, which is what Cordis's per-fiber `_hooks['internal/update']` list
does. And `update` on a non-`Active` fiber bumps the epoch as well as clearing
the error and target: Cordis's `_setEpoch(INACTIVE)` — a load in flight
becomes stale, and the transition loop now unloads a fiber still `Loading`
before it reloads, so what the stale load installed comes out first.
`update` and `restart` refuse only a disposed fiber (`InactiveEffect`), not one
mid-transition, since the transition re-reads at its end.

Steps for the hand, from `/Users/feb/dev/memory`:

1. `cargo nextest run -p extension` in the worktree above — 37 run, 37 pass.
2. `cargo clippy -p extension --tests` and `cargo test --test layer_headers`
   — clean, and the crate still at L0.
3. Tick the Check boxes, one per behaviour the run proved.
4. `just land agent-aa3de6387b4851b2d`; then `just lane-rm` per [[git-policy]].

## Acceptance
- [x] A plugin whose `validate` rejects ends `Failed(Error::Validation(..))`,
      `apply` was never called, and `fiber.config()` is `Null`
      (`a_refused_validate_fails_the_fiber_before_apply`).
- [x] `update` on an `Active` plugin runs its disposers, runs `apply` once
      more, `apply` sees the new value, and `fiber.config()` is the
      normalized value `validate` returned
      (`update_on_an_active_fiber_restarts_it_with_the_new_config`).
- [x] An `internal/update` listener that returns without `next` leaves the
      plugin `Active` on its old config with `apply` still called once
      (`an_update_listener_that_keeps_next_vetoes_the_restart`).
- [x] `update` on a `Failed` plugin with a valid config brings it `Active`
      (`update_on_a_failed_fiber_brings_it_active`).
- [x] An `internal/config` listener's rewrite is what `validate` and `apply`
      see (`an_internal_config_listener_rewrites_what_validate_sees`).
- [x] `restart` on a disposed fiber is refused with `InactiveEffect`
      (`restart_on_a_disposed_fiber_is_refused`).
- [x] `cargo clippy -p extension --tests` is warning-free and
      `cargo test --test layer_headers` still accepts the crate at L0.

```sh
cd /Users/feb/dev/memory/.claude/worktrees/agent-aa3de6387b4851b2d
cargo nextest run -p extension config_test
cargo nextest run -p extension
cargo clippy -p extension --tests -- -D warnings
cargo test --test layer_headers
```

Red-proof on the probe: dropping `*self.target.lock() = None` from
`Fiber::restart` fails exactly
`update_on_an_active_fiber_restarts_it_with_the_new_config` (5 of 6 pass) and
the inverse edit returns 37 of 37.
