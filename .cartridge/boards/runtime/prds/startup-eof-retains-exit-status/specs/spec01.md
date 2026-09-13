---
complexity: low
footprint: ["src/sdk.rs","src/cartridge.rs",".cartridge/tests/unit/src/tests/wire.rs","src/loader.rs",".cartridge/tests/unit/src/tests/mod.rs",".cartridge/tests/unit/src/tests/composition.rs"]
---

# Await exit after startup EOF within the original deadline

In sdk.rs Host::spawn and cartridge.rs start, replace the one-shot try_wait at pre-ready stdout EOF with child.wait().await. The wait stays inside the existing STARTUP_TIMEOUT future; do not create a new deadline, reset the original timeout, poll with sleeps or weaken the exit-status assertion. A normal exited child returns its real status. A child that keeps running with stdout closed reaches the existing timeout branch, which shuts down the link and drops the owned process; Child::drop retains kill/reap behavior. Preserve a wait I/O failure as an explicit startup failure. Existing ready/malformed/error-frame/size behavior is unchanged.

Extend the existing wire startup test to exercise both direct runtime and nested SDK startup, retaining exact expected immediate exit7 and unreadable-line errors and adding deterministic stdout-close/50ms-delayed-exit7. Add a live stdout-closed child fixture which records its actual PID, execs a long-running process and never signals ready. For both host layers, assert the original startup deadline returns timeout, and poll kill -0 under a short test deadline until the owned PID is gone. No arbitrary PID and no user process is touched. Existing pre-ready disposal/cancellation tests remain in the public gate.

## Acceptance

- [x] The new deterministic delayed-exit case fails without source fix, then strict direct/nested exit7 assertions pass with the fix.
- [x] Both stdout-closed live-child cases timeout within the existing bounded deadline and their recorded PID is reaped.
- [x] Public runtime test/check pass, retaining startup/cancellation limits and observation integration.

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just test runtime
```

```sh
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just check runtime
```

Coordinator collects in a detached clean lane at the exact committed runtime HEAD while verification explicitly uses the actual composed checkout. The same declared source footprint must match; unrelated runtime changes stay untouched. No observer source changes or acceptance weakening are part of this fix.
