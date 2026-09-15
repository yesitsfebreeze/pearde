---
state: "specced"
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
---

# pty, router, harness and mcp tests are green

## Outcome

The four spine owners (2026-09-14: pty 2, router 2, harness 1, mcp 1 red) pass repeatably.

## Acceptance

- [ ] `just test pty`, `just test router`, `just test harness`, `just test mcp` exit 0 on three consecutive runs; the counts observed at the start are in Result.

## Result

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
from restarting alpha; the working tree caps it at 500ms. Unproven.

Contributing, in this footprint: `refresh.test.ts:8` and `approval.test.ts`
prefer `cartridge.ctg/target/release/cartridge` (built 07:33) over
`target/debug` (11:25), and the gates build only debug, so `just test mcp`
runs a host older than the source it is gated with.

Blocker: the host session's commit in cartridge.ctg. Next: after it lands,
make the mcp tests take the binary the gates build, rebuild, and rerun
`just test mcp` eight times.
