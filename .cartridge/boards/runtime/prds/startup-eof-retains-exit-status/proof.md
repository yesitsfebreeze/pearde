# Startup EOF fix proof

Source `294b39fd1b8dd420e4e40bce6c2679cf1044220c`; independent /root round1 **96/100 PASS**. [Exact input/log digests](proof-inputs.json).

The deterministic new regression failed on unchanged source: `nested=false: exited before ready: closed stdout` ([before](regression-before.log)). After replacing try_wait with wait under the existing deadline, strict immediate and delayed exit7 and malformed-line cases pass for both host layers ([after](regression-after.log)). The original nested error assertions were preserved. Direct fixtures use a valid provide frame before EOF because an unknown frame correctly fails earlier in that host layer.

The stdout-closed but live fixture execs sleep under its own recorded PID. Both host layers hit their unchanged startup deadline and the owned PID is reaped ([timeout/reaping](timeout-reaping.log)). The nested case launches the real SDK sub-host with host stdin open so its own deadline is measured independently of an earlier outer runtime deadline. Existing cancellation/disposal tests remain in the full gate.

Public runtime tests passed **163 library +2 binary Rust tests**, plus existing memo-run **4 tests/47 assertions** ([log](proof-test.log)). Public formatting/Clippy passed ([log](proof-check.log)); rebuilt real runtime and observer integration **3 tests/38 assertions** passed ([build](proof-build.log), [integration](proof-observation-integration.log)).

No deadline reset, sleep-based production polling, stderr change, assertion weakening, observer behavior change or user data access. Wait errors now remain explicit startup errors. If stdout closes without process exit, startup times out rather than inventing an exit status. Source stable for coordinator collection in a fresh exact-HEAD detached lane.
