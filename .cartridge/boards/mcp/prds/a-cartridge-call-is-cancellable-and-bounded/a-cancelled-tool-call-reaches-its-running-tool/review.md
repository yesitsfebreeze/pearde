# @mcp/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool review history

Plan: `@mcp/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool`,
`prd.ctg/.cartridge/boards/mcp/prds/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool/prd.md`.
Scope: one observable outcome, executable leaf — an MCP client's
`notifications/cancelled` stops the tool that is running.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-19

Presented revision: `mcp.ctg` HEAD `1595a6fa52e4f8f4635ca426ec1fcddd40e7d277`
(clean). `cartridge.ctg` HEAD `804a08b`; the daemon binary used for every probe
below is `cartridge.ctg/target/debug/cartridge`, mtime 2026-09-19 13:17, built
from that repo at `beb8213`. No file in any live checkout was written.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` — `c55917e983d98c7f72da49b432f992c463342f3802f99081ba328b1e1981d128` |
| Specs | `specs/spec01.md` — `8ea498bee5f253701dae81c7e3f6a74401c8ddd34949f981f36f13d53d6edb6e` |
| Material contracts/dependencies | `mcp.ctg` `1595a6f` (`src/lib.rs`, `src/base.rs`, `src/service.rs`, `init.lua`, `cartridge.json`); `cartridge.ctg/src/node/mod.rs` (`either` at `:48-72`, listener driven by `call_async` at `:219-235`); `pty.ctg/src/lib.rs:884-891` and `pty.ctg/src/tool.rs:32`; `@runtime/a-cartridge-call-can-be-cancelled` (done) |

### The coordinator's question: does `create_async_function` remove the need for the trampoline?

**Ruled: no.** The spec's own section (`specs/spec01.md:156-200`) reaches the
same conclusion; I checked its claims by building and running the shape myself
rather than accepting them, in three throwaway clones of `1595a6f` under
`$TMPDIR/rev-cancel`. The spec's claims hold.

| Variant built and run | `tools/list` | outcome |
| --- | --- | --- |
| `create_async_function` + `base::runtime().spawn(...)` (mlua `"async"` feature, `async fn answer`) | `[]` | test fails at `cancel.test.ts:73` |
| the same, plus a `NEEDS` snapshot taken on the base's thread in `start()`, so a stale `needs` read cannot be the cause | `[]` | test fails identically — the failure is the outbound `describe`, not the needs read |
| `create_async_function` awaiting `service.message` inline, no spawn | — | host `WARN mcp: runtime error: there is no reactor running, must be called from the context of a Tokio 1.x runtime` |
| this spec's trampoline | `[{"name":"slow",…}]` | `1 pass, 0 fail`, tool answered `stopped-on-cancel` |

The reason is a property of `mcp.ctg`, not of the host, and it is checkable in
two greps:

- Every unit of work `mcp` does is an outbound call back into its own node —
  `policy`, `sessions`, `tool.*` describe, `tool.*` call, the cancel op — and
  every one goes `Call` → `base::bail` → `send` → `with()` →
  the `ENTERED` thread-local (`mcp.ctg/src/base.rs:30-54`, `:61-73`). `ENTERED`
  is pushed only by `base::entered` (`:37-42`), and only on a thread the base
  called into. `create_function` gives that thread; `create_async_function`
  does not, and a `runtime().spawn` worker never can. Re-adding `entered`
  cannot rescue it — it is a synchronous scope and cannot span an await.
- `pty.ctg` never calls back into its own node at all: `grep -rn "bail"
  /Users/feb/dev/cartridge/pty.ctg/src/` returns **0 hits**. `shell_op`
  (`pty.ctg/src/lib.rs:884-891`) calls `tool::dispatch(&shell, args)`
  (`pty.ctg/src/tool.rs:32`), which only touches the pty's own already-open
  `Arc<Shell>`. Its future is therefore free to leave the base's thread;
  `mcp`'s is not. That is the whole difference, and it is why the three-line
  fix is correct there and inert here.

Two secondary points in the same direction: the async route also needs a
`Cargo.toml` change (the mlua `"async"` feature), a path outside the PRD's
declared five, which the trampoline does not; and the recorded trap ("there is
no reactor running") is not a detail to route around but the executed outcome of
the only variant that keeps the base's thread.

Not a blocking finding. The spec already carries this reasoning, and it is
accurate. One cosmetic inaccuracy in it: `specs/spec01.md:186` says
`tool::dispatch` "only spawns processes"; it operates on an already-open shell.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome, one cartridge, no speculative surface. `src/service.rs` correctly left untouched — I verified by building: `Service::message` is `pub async fn` (`src/service.rs:236`) and its future is `Send + 'static` behind `Arc<Service>`, so the prototype compiles and passes without it. −1: Acceptance box 1 restates the mechanism rather than an outcome (see F3). |
| Ownership and reuse | 19 | The trampoline is placed in `src/base.rs` on purpose, so `@root/the-vendored-base-rs-stays-identical-across-native-cartridges` carries it to `agent.ctg` and `router.ctg`; host unchanged; no new dependency and no `Cargo.toml` change, which the rejected alternative would have needed. −1: the spec commits the vendored `base.rs` to a `job` module whose only consumer today is `mcp`, and says nothing about what the two sibling cartridges inherit at that moment; it defers entirely to the other PRD. |
| Dependencies and implementable slices | 19 | The child need `@runtime/a-cartridge-call-can-be-cancelled` is done and the PRD explains correctly why it is insufficient. The whole change was built and run end to end before being written down, and the cheaper alternative is now excluded by execution rather than assertion. −1: the `wait` arm is a slice shipped with no proof attached (F2). |
| Observable acceptance and baseline evidence | 18 | The gate is behavioural, not a census: it asserts on the string the fixture tool itself returns, set by a flag its own `cancel` arm writes. I reproduced both directions independently (below). JUnit name matches the `pass:` line exactly. Cold timings match the spec's stated numbers. −2 for F1, the one path by which this gate can go green in pass 2 without having tested the change. |
| Failure, recovery and compatibility | 17 | Provider errors route through `pcall` → `resume.error` → the `Err` the existing code already handles; the `{op="ready"}` path is preserved by the `type(step) == "table"` test; the silent `base::needs` hazard is identified and given its own Acceptance box — and my second async variant confirms that hazard is real and silent, since snapshotting `needs` changed nothing visible. −3: the deadlock the `wait` step exists to prevent is asserted but never demonstrated and never checked (F2), and the spec does not say what `resume` answers for an id the map no longer holds, so a listener that errors between steps leaves a job filed and its future running (F4). |
| Reviewer total | **92** / 100 | ≥ 90 with no unresolved blocking finding. |

### Validation: what I actually ran

All probing in `$TMPDIR/rev-cancel`, three `git clone --local` copies of
`mcp.ctg` at `1595a6f` (`orig`, `tramp`, `async`, plus `async2`/`async3`
derived from `async`). The trampoline tree carries the analyst's prototype
`src/base.rs`, `src/lib.rs`, `init.lua`; every tree carries the shipping
`.cartridge/tests/integration/cancel.test.ts` unmodified. Nothing was written
into `/Users/feb/dev/cartridge/mcp.ctg` or any other live checkout.

**1. The gate bites — reproduced, both directions, twice each.**

| tree | structural guard | `cancel.test.ts` |
| --- | --- | --- |
| unmodified `1595a6f` | exit **1**, "src/lib.rs still waits for another cartridge on the base's own thread" | `0 pass, 1 fail` — `Expected: "stopped-on-cancel" / Received: "ran-to-completion"` |
| trampoline | exit **0** | `1 pass, 0 fail` |

**2. `CARTRIDGE_YOLO` does not touch this gate.** `jq -r '.settings|keys[]'
mcp.ctg/cartridge.json` → `band, cwd, hot, record_usage, tools` — `mcp.ctg`
declares no `yolo` setting, and `grep -rn yolo cartridge.json src/ init.lua`
returns nothing, so the host has nothing to merge into it. Confirmed by
execution as well as by declaration; my session carries `CARTRIDGE_YOLO=1`, so
I ran the pair both ways:

```
tramp / CARTRIDGE_YOLO=1     1 pass  0 fail
tramp / env -u CARTRIDGE_YOLO 1 pass  0 fail
orig  / CARTRIDGE_YOLO=1     0 pass  1 fail   Received: "ran-to-completion"
orig  / env -u CARTRIDGE_YOLO 0 pass  1 fail   Received: "ran-to-completion"
```

Red stays red and green stays green in both environments. The structural guard
is a pure `grep` and is environment-independent by construction. The gate is not
measuring an inherited variable in either direction.

**3. Every Verify block run verbatim, cold, with the environment stripped.**
`CARGO_TARGET_DIR`, `CARTRIDGE_RUNTIME`, `CARTRIDGE_BIN`, `MCP_MODULE` and
`MCP_TARGET_DIR` unset (`env -u`), fresh target directory, `PRD_TEST_REPORT`
supplied as the engine supplies it:

```
block 1 (cargo build, cold)                     exit 0, real 4.25 s
block 2 (structural guards)                     exit 0
test block 1 (bun, --reporter=junit)            1 pass 0 fail, real 3.92 s
  report name: "a cancelled tools/call reaches the running tool"  — matches `pass:` exactly
test block 2 (cargo test --lib)                 23 passed; 0 failed; 1 ignored, real 5.63 s
  all four named tests present at 1595a6f and reported ok
```

Every block is far inside the 120 s limit on a cold target dir, not only a warm
one. No `${VAR:?}` anywhere; every variable uses `:-`, so nothing aborts under
`sh -eu` with no environment injected. `CARGO_TARGET_DIR` is pinned on both
cargo commands, and `/target/` is in `mcp.ctg/.gitignore`, so no block writes
inside the footprint. The absolute defaults for `CARTRIDGE_RUNTIME` and
`CARTRIDGE_BIN` are the pattern the spec template explicitly sanctions; no
block `cd`s anywhere and no block builds `cartridge.ctg`.

**4. Inert guards: none.** Both guards sit inside `if`, so neither is the
`! grep` form that never fails under `set -e`, and there is no
`test -n "$X" && test "$X" -ge N`. I did not take this from reading — the
unmodified tree returns exit 1.

**5. Self-referential or self-curing checks: none.** Neither failure message
names the token that would satisfy it ("still waits for another cartridge on
the base's own thread", not "`block_on`"). The behavioural assertion is on a
string the fixture tool composes from a flag written by its own `cancel` arm
(`cancel.test.ts:41-53`); the test never builds the value it then asserts on.

**6. Footprint and Acceptance.** The spec's four paths — `src/base.rs`,
`src/lib.rs`, `init.lua`, `.cartridge/tests/integration/cancel.test.ts` — all
sit inside the PRD's declared five. The PRD's three Acceptance boxes are each
covered: PRD-1 by spec box 2, PRD-2 by spec boxes 2 and 3, PRD-3 by spec box 3,
which names the mutant direction explicitly. The spec's two extra boxes are
earned, not padding: box 4 guards the `tools/list` hazard my async2 probe shows
is real and silent, and box 5 pins the unit suite. The `src/service.rs`
omission is right and I verified it by building. The coordinator's footprint
widening is settled and not relitigated here.

### Findings

**F1 — `CARGO_TARGET_DIR` default divergence opens a false-green path in
pass 2. (non-blocking, cheap fix)** Block 1 builds into
`${CARGO_TARGET_DIR:-$PWD/target/a-cancelled-tool-call-verify}`, but the bun
`test` block sets no `CARGO_TARGET_DIR`, and `cancel.test.ts:10-11` searches
`MCP_TARGET_DIR` → `owner/target/a-cancelled-tool-call-verify` →
**`owner/target`**. Blocks inherit whatever the collector carries. If the
collector already exports `CARGO_TARGET_DIR` — which this board's standing
practice encourages — block 1 builds somewhere else, and in pass 2 (cwd = the
live checkout, which holds `mcp.ctg/target/debug/libmcp.dylib`, mtime
2026-09-17) the test loads a **stale dylib** and can report green for code it
never built. In pass 1 the lane has no `target/`, so it fails loudly instead;
only pass 2 is silent. Fix: put
`CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-cancelled-tool-call-verify}"`
on the bun `run:` line and pass `MCP_TARGET_DIR="$CARGO_TARGET_DIR"`, or drop
the bare `owner/target` fallback from the test's search list. Test block 2 has
the same divergence in its hard-coded `ls` path, but there an empty
`MCP_MODULE` fails the block loudly, so only the bun block is a false-green
risk.

**F2 — the `wait` step and its 25 ms park are entirely unexercised.
(non-blocking)** The analyst's own report records it: nothing in any probe
reached the `wait` step. The spec asserts a specific deadlock — two messages of
one instance racing `Instance::session`'s `tokio::sync::OnceCell`
(`src/service.rs:122`, used at `:446-462`) — and adds a timeout arm to prevent
it, but ships no Acceptance box and no Verify line that the arm is ever taken
or that the deadlock is real. Two concurrent messages on one instance is
precisely the shape this PRD's own scenario produces, so this is the arm most
likely to be silently wrong, and `PARK = 25 ms` is a chosen number. One unit
test that begins two jobs on one instance and asserts both complete would close
it, or at minimum an Acceptance box naming it.

**F3 — Acceptance box 1 is not independently observable. (non-blocking,
cosmetic)** "`mcp.answer` never waits on another cartridge on the base's
thread" is checked only by `grep -qn 'block_on' src/lib.rs`, and the spec's own
design puts a `block_on` in `advance` inside `src/base.rs` (spec `:82-85`),
which that guard does not look at. The box is therefore green by construction
for this design and proves nothing about the property it names. Harmless —
the behavioural test is the real gate, and the spec says so itself — but the
box overstates what is checked.

**F4 — the spec does not say what a late or duplicate `resume` answers.
(non-blocking)** `advance` removes the job from the map before any `block_on`;
the spec does not state what happens on re-entry for an id that is no longer
there, nor what becomes of a job whose Lua listener errors between steps. As
written such a job stays filed and its future keeps running. One sentence in
the `src/base.rs` section would settle it.

**F5 — cosmetic.** `specs/spec01.md:186` describes `pty.ctg`'s `tool::dispatch`
as "only spawns processes"; it operates on an already-open `Arc<Shell>`. The
point it supports is correct.

**Side note, not scored.** `cancel.test.ts` leaks a daemon per run: `c.close()`
kills the `cartridge mcp` bridge child but not the daemon that bridge starts,
which lingers with `--idle-timeout 3600`. I stopped 27 such processes after my
probes. In collect this leaves one background daemon per pass for an hour.
Worth a `cartridge stop` in the test's `finally`, but it does not affect
correctness of the gate.

Findings and concrete revisions: F1–F5 above; none blocking. F1 is the only one
that touches whether the gate measures the change, and it is a one-line fix on
the `run:` line.
Disposition: **keep** — implement spec01 as written, ideally with F1 applied.
Validation: commands, cwd and exit statuses recorded in "Validation: what I
actually ran" above; cwd for every probe was a throwaway clone under
`$TMPDIR/rev-cancel`, never a live checkout. All probe daemons stopped
(`ps` count of `mcp-cancel-*` = 0 at the end of the round).
Reviewer identity: independent reviewer agent (Claude Opus 5), not the spec's
author; spawned fresh for this round with no part in writing spec01.
User rating: not required under delegation; none supplied.
User feedback/provenance: the user's 2026-09-19 choice of Option A for
`@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node`,
recorded in `prd.md` under "Answer applied". This round confirms Option A is
also the only option that works here, by execution.
Result: **PASS** (92/100, no unresolved blocking finding).
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed to implementation of `specs/spec01.md`. Apply F1 to the
bun `test` block's `run:` line before collect; F2–F5 are improvements the
implementer or the diff reviewer may fold in without another review round.
