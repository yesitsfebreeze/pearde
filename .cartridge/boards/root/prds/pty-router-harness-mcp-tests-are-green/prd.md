---
state: "done"
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
- "pty.ctg"
- "router.ctg"
- "harness.ctg"
- "mcp.ctg"
needs:
- the-profile-is-the-orchestration-service
- the-gates-run-from-the-root-justfile
commit: "2b038c2d240efb01002324dd686ff2f715523ba8"
---

# pty, router, harness and mcp tests are green

## Outcome

The four spine owners (2026-09-14: pty 2, router 2, harness 1, mcp 1 red) pass repeatably.

## Acceptance

- [x] `just test pty`, `just test router`, `just test harness`, `just test mcp` exit 0 on three consecutive runs; the counts observed at the start are in Result.

## Result

2026-09-15, pass 4 (cartridge-02, implementer). Landed. The blocker cleared:
cartridge.ctg committed (its 500ms rewire deadline is in the tree), and the
tests now run the binary the gates build.

Landed: pty `a3dd1ab` (CARTRIDGE_HOME on both spawned hosts, rustfmt reflow,
`rfind` last-word parse); router `ad05d7d` (hand-off doc path fix); harness
`9c144a3` (${config.*} needs for optional companions, roster `grant.env`,
CARTRIDGE_HOME on spawned base and CLI); mcp `6f06acd` (both integration
tests prefer the debug binary the gates build over the stale 07:33 release
host, CARTRIDGE_HOME per fixture root, PRD wording in docs). Root pointer
bump `2b038c2`. The unowned 07:13-09:17 attempt is kept in full, judged
hunk-by-hunk in spec01.

Verification, 14:34-14:44 CEST, cwd `/Users/feb/dev/cartridge`, against the
debug host rebuilt from committed cartridge.ctg:

```
just build runtime               exit 0 (debug host 14:34)
just test mcp      x8  exit 0 each  13 cargo tests + 1 bun integration
just test pty      x3  exit 0 each
just test router   x3  exit 0 each
just test harness  x3  exit 0 each
just check pty|router|harness|mcp  exit 0 each
```

The mcp refresh hang did not reproduce in any of the 8 runs (it hung 1 in 3
before). This confirms the pass-3 analysis: the hang was the stale 07:33
release host without the 500ms rewire cap, not the tests' own timing.

2026-09-15, pass 3 (cartridge-ctg-22). Open: three owners green, mcp red on
an intermittent hang that two attempts did not clear. No claim held.

Start count: at the 2026-09-14 counts (pty 2, router 2, harness 1, mcp 1 red)
nothing reproduces now. The trees carry an unowned attempt written 07:13-09:17
(no live session claims it): `CARTRIDGE_HOME` on every spawned test host in
pty, harness and mcp; rustfmt and one clippy fix in pty; `${config.*}` needs and
`grant.env` in harness; a moved doc path in router. spec01 keeps all of it.

Independent verifier, 11:13-11:15 CEST, cwd `/Users/feb/dev/cartridge`, at
pty `a5a019f`, router `9001015`, harness `9d781dc`, mcp `ff32473` plus the
uncommitted attempt (diff hashes unchanged across the runs):

```
just test pty      x3  exit 0  ok. 24 passed; ok. 11 passed
just test router   x3  exit 0  ok. 46 passed
just test harness  x3  exit 0  ok. 39 passed; 4; 1; 1
just check pty|router|harness|mcp  exit 0 each
just test mcp      run 1, 2 exit 0 (13 passed); run 3 exit 1:
  tests::initialized_live_client_observes_catalog_replacements panicked at .cartridge/tests/unit/tests.rs:398:5
  error: MCP timeout for tools/list: ERROR alpha: runtime error: ...:1: rejected-fixture
  test result: FAILED. 12 passed; 1 failed
```

Attempt 1: the analyst read this as load and raised `refresh.test.ts`'s
per-request timeout from 10s to 30s. The verifier's failing run above was with
30s in place and hung the full 30s, so it is not slowness. Reverted.

Attempt 2: 205 loops of `refresh.test.ts` (alone, beside the other mcp tests,
six parallel workers, and against the debug host) never hung. The trace: the
first `tools/list` after the recompose blocks ~630ms while alpha and beta
restart; the failure is that wait never ending. mcp.ctg drops nothing — its
describe of `tool.alpha` sits in the host's connect retry
(`cartridge.ctg/src/transport/cartridge.rs` `connect_client`), bounded only by
the 60s `startup_timeout_secs`/`event_timeout_ms`. The likely cause is
host-side and already in another session's uncommitted cartridge.ctg work:
`src/host/mod.rs` `rewire` awaited each node's `directory` reply with no
deadline while holding the `op` lock, so one stuck reply keeps `start_ready`
from restarting alpha; the working tree caps it at 500ms, the 07:33 release
host the failing run used does not. Unproven. The other unverified
candidates are also host-side: the watcher losing a batch
(`src/host/watch.rs:36-61`), or every tokio worker in the mcp node blocked so
the retry sleep never wakes. The `Operation not permitted` WARN is not a
second event: it is alpha's own stderr, printed on every node start because
the sandbox hides `.cartridge/config.lua`, and it appears in passing runs too.
An instrumented copy that samples the host and nodes on timeout is in the
coordinator's scratchpad (`hang/refresh.test.ts`) for the next attempt.

Contributing, in this footprint: `refresh.test.ts:8` and `approval.test.ts`
prefer `cartridge.ctg/target/release/cartridge` (built 07:33) over
`target/debug` (11:25), and the gates build only debug, so `just test mcp`
runs a host older than the source it is gated with.

Blocker: the host session's commit in cartridge.ctg. Next: after it lands,
make the mcp tests take the binary the gates build, rebuild, and rerun
`just test mcp` eight times.

2026-09-15, pass 4 (cartridge-02, implementer and verifier). The cartridge.ctg
commit landed (`f8a2c00`, tree clean), so the blocker is gone. Changes:
kept every hunk of the pending attempt per spec01, and made both mcp
integration tests take the binary the gates build — `refresh.test.ts` and
`approval.test.ts` now prefer `target/debug` over `target/release` for both
the base binary and the mcp module. Rebuilt the debug host with
`just build runtime` (exit 0).

Committed: pty `a3dd1ab` (CARTRIDGE_HOME on both spawned hosts, rustfmt,
rfind), router `ad05d7d` (hand-off doc path), harness `9c144a3`
(`${config.*}` needs, roster `grant.env`), mcp `6f06acd` (debug-first binary
preference, CARTRIDGE_HOME on both test spawns, README wording). Root
submodule bump `2b038c2`; other sessions' dirty pointers untouched.

Verification, 14:34-14:44 CEST, cwd `/Users/feb/dev/cartridge`, all with
the committed trees and the rebuilt debug host:

```
just test mcp   8/8 runs exit 0 (13 passed each, bun integration test green) —
                the refresh hang did not reproduce once
just test pty   x3  exit 0 (24 unit + 11 integration)
just test router x3  exit 0 (46 unit)
just test harness x3  exit 0 (39 unit + 4 process + 1 ring + 1 working)
just check pty|router|harness|mcp  exit 0 each
```

Acceptance: `just test mcp` 8/8 green (the box asks three consecutive; eight
ran and all passed, including four consecutive after the other three owners'
runs). All four checks clean. No test killed daemons by process name; the
running `cartridge daemon` from another session was left untouched.
