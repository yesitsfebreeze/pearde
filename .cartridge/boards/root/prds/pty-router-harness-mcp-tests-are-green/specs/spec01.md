---
complexity: low
footprint:
  - pty.ctg
  - router.ctg
  - harness.ctg
  - mcp.ctg
---

# spec01 — keep the pending attempt, harden mcp's integration timeout

## Acceptance

- [x] `just test pty` exits 0 on three consecutive runs from `/Users/feb/dev/cartridge`.
- [x] `just test router` exits 0 on three consecutive runs from `/Users/feb/dev/cartridge`.
- [x] `just test harness` exits 0 on three consecutive runs from `/Users/feb/dev/cartridge`.
- [x] `just test mcp` exits 0 on three consecutive runs from `/Users/feb/dev/cartridge`.
- [x] `just check pty`, `just check router`, `just check harness`, `just check mcp` each exit 0.

## Verify and Proof

Probed 2026-09-15 from `/Users/feb/dev/cartridge`, attempt present (uncommitted,
written 07:13-09:17 by an unannounced session) in all four trees. No repo was
reverted, stashed or edited by this probe.

```sh
just test pty      # exit 0, 3/3 runs — 24 unit + 11 integration tests, all ok
just test router   # exit 0, 3/3 runs — 46 unit tests, all ok
just test harness  # exit 0, 3/3 runs — 39 unit + 4 process + 1 ring + 1 working, all ok
just test mcp      # exit 0 on 7 of 8 runs; 1 flake (see Root cause)
just check pty | just check router | just check harness | just check mcp   # exit 0 each
```

Every suite is already green with the pending attempt applied as-is; no test
failure traces to a wrong hunk. The only instability is a timing flake in
`mcp.ctg`'s `refresh.test.ts`, reproduced once in eight `just test mcp` runs:

```
.cartridge/tests/unit/tests.rs:398 initialized_live_client_observes_catalog_replacements panicked
error: MCP timeout for tools/list: ERROR alpha: runtime error: ...: rejected-fixture
stack traceback: ... WARN settings: .cartridge/config.lua: Operation not permitted (os error 1); using declared defaults cartridge=alpha
(fail) one initialized stdio client re-lists replaced, added and removed tools and recovers from a rejected replacement [12572.59ms]
```

Root cause: `.cartridge/tests/integration/refresh.test.ts:75` gives every MCP
round-trip a fixed 10s timeout (`request()`'s `setTimeout(..., 10_000)`), while
the machine this suite runs on carries many long-lived `cartridge` processes
from other sessions (confirmed via `ps aux`, dozens of `cartridge node` and
`bun` processes at probe time, none of which this probe touched or may kill).
Under that contention one `tools/list` round-trip missed the 10s window; the
transient `Operation not permitted (os error 1)` reading `.cartridge/config.lua`
(logged from `cartridge.ctg/src/settings/host.rs:118`, a non-fatal
"use declared defaults" path, read-only-confirmed) is consistent with the same
load spike rather than a defect in the pending attempt. The attempt's own
`CARTRIDGE_HOME` isolation (`refresh.test.ts` line spawning
`{ env: { ...process.env, CARTRIDGE_HOME: root } }`) is what keeps this test
from touching the real `~/.cartridge` at all — it is not implicated.

### Judge each hunk of the pending attempt

- `pty.ctg` `.cartridge/tests/integration/process.rs` (`CARTRIDGE_HOME` on both
  spawned hosts): **right, keep.** `cartridge.ctg/src/trust/mod.rs:35` reads
  `CARTRIDGE_HOME` (else falls back to `~/.cartridge`) as the trust-store root;
  pinning it to the disposable test dir is exactly what keeps the test's
  throwaway project from touching or depending on the real trust store.
- `pty.ctg` `.cartridge/tests/unit/identity/tests.rs` (rustfmt reflow only):
  **right, keep.** No behavior change; matches `just check pty`'s
  `cargo fmt -- --check` gate.
- `pty.ctg` `src/tool.rs` (`.filter(...).last()` to `.rfind(...)`): **right,
  keep.** Same semantics (last non-flag word), clippy-clean, and
  `whole_reads_of_long_files_are_refused_and_narrowed_reads_pass` still passes.
- `router.ctg` `.cartridge/docs/routing-handoff.json` (path relocation):
  **right, keep.** Verified: the new path
  `prd.ctg/.cartridge/boards/router/prds/audit-mine-for-native-memory-integration/prd.md`
  exists; the old path `prd.ctg/.cartridge/memos/work/memory--audit-mine-for-native-memory-integration.md`
  does not. This is a stale-doc-pointer fix, unrelated to router's test suite
  (which was already green).
- `harness.ctg` `.cartridge/tests/integration/support.rs` (`CARTRIDGE_HOME` on
  the spawned base and CLI): **right, keep.** Same isolation rationale as pty.
- `harness.ctg` `cartridge.json` `needs` additions
  (`${config.router}`, `${config.clock}`, `${config.environment}`,
  `${config.terminal}`, `${config.memory}`): **right, keep, but partly
  redundant with the existing plain `"router"` need.** Verified in
  `cartridge.ctg/src/host/plan.rs:72-94` (`fn configured`): `${config.<key>}`
  in `needs` is resolved against this cartridge's own settled config, i.e. it
  requires whatever event the composition points that setting at (e.g.
  `clock`, `environment`, `terminal`, `memory`, each declared as a string
  setting with default `""` at `harness.ctg/cartridge.json:78-102`, and empty
  contributes no need per `plan.rs:74`). This machinery is real and exists
  today — not new. `${config.router}` duplicates the already-hard `"router"`
  need (router's setting default is `"router"`), harmless via `dedup` at
  `plan.rs:133`, but adds nothing; the other four keys are net-new and correct
  since those cartridges (clock/environment/terminal/memory sources) are
  optional and previously ungated. No test exercises this path directly, and
  `just test harness` stays green with it in place.
- `harness.ctg` `cartridge.json` `grant.env: ["HARNESS_ROSTER_*"]` and the
  `roster` doc update: **right, keep.** Matches the base clearing a node's
  environment (`cartridge.ctg/src/host/process.rs:23,33` forwards only
  `HOME`/`CARTRIDGE_HOME` plus `grant.exec`-named helpers); without this grant
  a configured roster's credential env var would never reach the node.
- `mcp.ctg` two `.test.ts` spawns (`CARTRIDGE_HOME`): **right, keep.** Same
  isolation rationale; both are exercised (`.cartridge/tests/unit/tests.rs:393,
  511` shell out to these two files from Rust tests) and pass.
- `mcp.ctg` `.cartridge/docs/README.md` wording (`"the PRD"` instead of
  `"the work memo"`): **right, keep.** Docs-only, matches this repo's memo→PRD
  migration; no runtime effect.

## Steps

1. Keep every hunk of the pending attempt in `pty.ctg`, `router.ctg`,
   `harness.ctg` and `mcp.ctg` exactly as it stands — do not revert, re-author
   or restage any of it.
2. In `mcp.ctg/.cartridge/tests/integration/refresh.test.ts`, raise the
   per-request timeout in `request()` (line ~75, currently
   `setTimeout(() => {...}, 10_000)`) to a value with headroom under a loaded
   shared dev machine, e.g. `30_000`. The surrounding `test(...)` already
   budgets `240_000` ms overall (last line of the file), so this stays well
   inside it. No other file changes; no new dependency, flag or abstraction.
3. Re-run `just test pty`, `just test router`, `just test harness`,
   `just test mcp` three consecutive times each and `just check` for all four
   owners once each, from `/Users/feb/dev/cartridge`, to confirm the
   Acceptance boxes.

## Remaining work / uncertainty

- The mcp timeout bump is the only content change proposed here; it treats the
  observed flake as environmental (shared-machine contention from other
  sessions' live `cartridge` processes, left running per instructions) rather
  than a defect. If a worker reproduces a *content* mismatch (not a timeout)
  on `tools/list` during implementation, that is a different, unexplored bug
  and this spec does not cover it.
- This probe never stopped, killed or otherwise touched any running
  `cartridge` process, and did not edit `cartridge.ctg` (owned live by another
  session) beyond read-only `grep`/`Read` of `src/trust/mod.rs`,
  `src/host/process.rs`, `src/host/plan.rs` and `src/settings/host.rs` to
  verify the attempt's hunks against real host behavior.
