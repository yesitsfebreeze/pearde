---
complexity: small
footprint:
  - .cartridge/tests/integration/loop.rs
---

# spec01 — the loop harness strips CARTRIDGE_YOLO from every base binary it spawns

`.cartridge/tests/integration/loop.rs` spawns the base binary twice — in
`Base::cli` (line 165) and in `start` (line 201) — and neither spawn removes any
variable from the inherited environment. `just launch claude --yolo` exports
`CARTRIDGE_YOLO=1`, every worker shell on this machine inherits it, and the host
then merges `yolo: true` into the config of every cartridge declaring that
setting (`cartridge.ctg/src/settings/mod.rs:15-16`, reading
`cartridge.ctg/src/transport/settings.rs:190-192`). `src/lib.rs:634` skips the
whole policy branch under `yolo`, the denied read is dispatched for real, and
`multiple_tool_calls_execute_and_persist_in_response_order` fails at
`loop.rs:798` on a correct journal entry.

The change is two `.env_remove` calls in the test harness. Nothing in
`src/lib.rs` changes.

## The two decisions this spec had to make, and the probes that settled them

### Removing the variable is the only available fix; setting the setting is not

The obvious alternative — leave the environment alone and pin `yolo = false` in
the test profile at `loop.rs:148-149` — does not work, and this was measured
rather than reasoned. `settings::apply` merges `{"yolo": true}` *over* the
composed config, and `merge` overwrites a scalar leaf outright
(`transport/settings.rs:126-145`, the `(base, over) => *base = over` arm). The
environment therefore beats any declared value. Probe: with `yolo = false`
added to the `agent` stanza of the test profile and `CARTRIDGE_YOLO=1` exported,
`multiple_tool_calls_execute_and_persist_in_response_order` still failed at
`loop.rs:798` (exit 101). Explicitly setting the setting is not a stronger
alternative to removing the variable; it is a non-fix.

### This is the whole leak, not one instance of a general one

`settings::apply` in `cartridge.ctg/src/settings/mod.rs:14-19` is the only place
in the host where an environment variable becomes the value of a declared
setting, and `YOLO_ENV` is the only variable it reads. The host's other
environment reads — `CARTRIDGE_HOME` (set explicitly by this harness),
`CARTRIDGE_DIAGNOSTICS`, `CARTRIDGE_DIAGNOSTICS_MAX_BYTES`, `CARTRIDGE_BIN`,
`CARTRIDGE_PROXY_KEY`, `CARTRIDGE_LISTENER_FD`, `XDG_RUNTIME_DIR`, `PATH`,
`HOME` — change runtime behaviour or process wiring, never a settled config
value. So a single `.env_remove` per spawn closes the class, and a blanket scrub
of `CARTRIDGE_*` would buy nothing and would break `CARTRIDGE_HOME` isolation.

`CARTRIDGE_YOLO` does have a second effect the harness also stops inheriting:
under `yolo` the host skips trust verification (`cartridge.ctg/src/trust/mod.rs:94`,
`cartridge.ctg/src/cli/trust.rs:71`). Removing the variable therefore makes the
suite run *with* trust enforced. That is the stricter posture and it already
passes: the unmodified tree under `env -u CARTRIDGE_YOLO` reports 13 passed, 0
failed, exit 0, because the temporary project is its own `CARTRIDGE_HOME` and is
its own owner to the trust check (`loop.rs:156-158`).

### `src/lib.rs` is reserved, not modified

`src/lib.rs` stays in the footprint because the PRD reserves it and narrowing
would drift from the PRD, but the diff must not touch it. Under `yolo`,
bypassing the policy is the declared meaning of the setting
(`cartridge.json:100-104`), so the agent is behaving as specified and there is
nothing there to repair. The probe confirms it by execution: with `src/lib.rs`
byte-identical to HEAD and only the harness changed, the whole `loop` target
passes under `CARTRIDGE_YOLO=1`. The diff reviewer is the backstop for this
box; no Verify block gates it, because a text check on a file's contents is the
class of gate this board has seen beaten every time.

## Steps

1. In `.cartridge/tests/integration/loop.rs`, declare the variable name once
   near `base_binary` with a comment naming why it is stripped:

       const YOLO_ENV: &str = "CARTRIDGE_YOLO";

   The precedent is `memory.ctg/src/hub/src/lib.rs:121` and
   `memory.ctg/src/commands/src/commands_hub.rs:454`, which both
   `.env_remove(identity::TAKEOVER_ENV)` on a spawn with a comment naming the
   failure the inherited variable would cause. This crate has no dependency on
   the `cartridge` crate, so the name is a literal here rather than a re-export
   of `cartridge::settings::YOLO_ENV`.
2. Add `.env_remove(YOLO_ENV)` to the `Base::cli` spawn, after the
   `.env("CARTRIDGE_HOME", &self.dir)` call.
3. Add `.env_remove(YOLO_ENV)` to the `start` spawn, after the
   `.env("CARTRIDGE_HOME", dir)` call.
4. Change nothing else. In particular the assertion at `loop.rs:798` and the
   test profile at `loop.rs:148-149` stay as they are, and `src/lib.rs` is not
   edited.

## Acceptance

- [x] `.cartridge/tests/integration/loop.rs` removes `CARTRIDGE_YOLO` from the
      environment of both base-binary spawns, `Base::cli` and `start`.
- [x] With `CARTRIDGE_YOLO=1` exported, the whole `loop` target passes and
      `multiple_tool_calls_execute_and_persist_in_response_order` is reported
      passed.
- [x] The same target passes under `env -u CARTRIDGE_YOLO`, so the two runs
      agree and the suite no longer measures the shell it was launched from.
- [x] The diff touches no file but `.cartridge/tests/integration/loop.rs`; in
      particular `src/lib.rs` and the assertion at `loop.rs:798` are unchanged.

## Verify and Proof

The first block is the agreement half: the target under `env -u CARTRIDGE_YOLO`,
which is green at HEAD and must stay green. The second block is the
discriminator: it exports `CARTRIDGE_YOLO=1` itself, so it fails before the fix
and passes after it, with no grep and no count anywhere.

Both blocks were executed verbatim, as `sh -eu -c`, from the repository root of
two throwaway rsync copies of this checkout at `620857d`. On an unfixed copy
block 1 exits 0 (13 passed) and block 2 exits 101 (12 passed, 1 failed at
`loop.rs:798`); on a copy carrying only the harness change both exit 0 with 13
passed, and the output carries the line
`test multiple_tool_calls_execute_and_persist_in_response_order ... ok` that the
`pass:` name matches. Block 1 therefore passes on a broken tree and is not the
gate; block 2 is. A cold run of block 2's command line into an empty
`CARGO_TARGET_DIR` took 16 seconds wall, exit 0, against the 120 second limit.

`CARTRIDGE_BIN` carries an absolute default because `base_binary`
(`loop.rs:52-65`) otherwise resolves `../cartridge.ctg/target/release/cartridge`,
which does not exist from the lane.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/harness-yolo-verify}"
export CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}"
env -u CARTRIDGE_YOLO cargo test --locked --test loop
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/harness-yolo-verify}"; export CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}"; export CARTRIDGE_YOLO=1; cargo test --locked --test loop
pass: multiple_tool_calls_execute_and_persist_in_response_order
```

## Remaining risk

The same hole exists in other harnesses and is out of scope here; it is named in
`analyst-2.md` for separate PRDs on the owning boards. Within this footprint the
only residual risk is that `CARTRIDGE_BIN`'s default points at a release build
of the base that a collector may not have built; the block then fails loudly on
`base_binary`'s own assertion rather than passing vacuously.
