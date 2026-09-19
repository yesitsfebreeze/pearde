---
state: "done"
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/mcp.ctg"
footprint:
- "src/service.rs"
- "src/lib.rs"
- "src/base.rs"
- "init.lua"
- ".cartridge/tests/integration/cancel.test.ts"
needs:
- "@runtime/a-cartridge-call-can-be-cancelled"
commit: "624afb3ab7bab6f2644e8287981d878c636e3df8"
---

# A cancelled tool call reaches its running tool

## Outcome

An MCP client that cancels a tool call stops the tool that is running. The
cancellation machinery this cartridge already ships actually fires, instead of
always arriving after the call it was meant to stop has finished.

## Evidence

Established 2026-09-17 by analyst-1 of the parent, against `mcp.ctg` HEAD
`345871e` and `cartridge.ctg` HEAD `63ff234`. Re-verified 2026-09-19 against
current HEADs — `mcp.ctg` `5a7c54c` (the `inflight` map moved from the
service onto each attached `Instance`) and `cartridge.ctg` `beb8213` (the
child need below, now done) — by `git show <HEAD>:<path>` and by an executed
probe; every line reference below is current.

The cartridge already implements MCP cancellation: the per-instance `inflight`
map (`src/service.rs:120,126`), registered in `invoke` (`:612-616`), consumed by
`notified` on `notifications/cancelled` (`:254-262`); and `pty.ctg/src/tool.rs:44-58`
genuinely honours `{"op":"cancel", context}`.

It is dead code by construction. `answer` in `src/lib.rs:41-64` is a synchronous
Lua function (registered via `create_function`, `src/lib.rs:74`) that does
`base::runtime().block_on(service.message(...))` (`:58`). `invoke`'s call goes
`(self.call)` -> `base::bail` (`src/base.rs:71-73`) -> `with(...)`'s
`cartridge.call_function("bail", ...)` (`src/base.rs:49-67`), a **synchronous**,
thread-pinned call ("only a thread the base called into may touch it",
`src/base.rs:6-7,30-38`) that reaches `cartridge.bail` and takes the
**blocking** branch of `either` (`cartridge.ctg/src/node/mod.rs:48-72`, bound at
`:266-278`), because `coroutine.isyieldable()` is false behind mlua's
non-continuation C-call boundary. The thread holds `mcp.ctg`'s node's Lua state
for the whole tool call, including the wait on the tool's own reply — the exact
scenario the host's own comment now names in prose
(`cartridge.ctg/src/transport/cartridge.rs:976-980`, added by the child need's
own commit): "a listener takes its node's Lua lock synchronously, and a lock
held by a handler waiting on another cartridge would park the worker whose
queue carries that very reply." The cancellation line is bridged concurrently
(`cartridge.ctg/src/cli/host.rs`, `Backend::message`/`stdio`'s
`serving.spawn(...)` per line), and it does reach the transport as its own
independent `event` request with its own permit and its own cancellation token
(`cartridge.rs:855-889`) — dispatch itself is not serialized. But its `mcp`
event's Lua call still queues behind the same node's Lua lock that the first
event's `answer()` is holding, so `notified` runs only after `invoke` has
already removed its entry and the lookup at `src/service.rs:261` always misses.

**Probed 2026-09-19** (the parent's own "first step," previously unexecuted):
fresh debug builds of both repos at these exact HEADs, composed with a fixture
tool whose Lua listener busy-loops (CPU-bound, since this sandbox is
`StdLib::ALL_SAFE ^ IO ^ PACKAGE` — no `io`, no `os.execute` — per
`cartridge.ctg/src/lua/mod.rs:26`) and checks a shared upvalue set by its own
`{"op":"cancel"}` arm. A real `cartridge mcp` bridge process called the tool,
and 300 ms into a ~5.5 s call sent a real `notifications/cancelled` for that
request id on the same stdio. The call ran to completion
(`"completed-without-cancel …"`) rather than stopping early — reproducing the
exact failure this PRD names, unchanged by the now-`done` child need. Command
and result are in the analyst report; the harness is the same shape as this
cartridge's own `.cartridge/tests/integration/instances.test.ts` (which already
sends a real `notifications/cancelled` over real stdio, just not against an
in-flight call).

**What the child need actually changed, and why it does not reach here:**
`@runtime/a-cartridge-call-can-be-cancelled` (done, `beb8213`) makes the
*transport* observe a *caller's own* abandoned call — an expired bound now
cancels that specific `event` RPC's listener via a `select!` inside its
`spawn_blocking`/`block_on` (`cartridge.rs:976-993`). That is orthogonal to this
PRD's mechanism: the MCP `notifications/cancelled` here is not a caller giving
up on the first `tools/call`'s own RPC — it is a **second, independent** `mcp`
event whose own Lua call cannot start running its `notified()` logic until the
first event's `answer()` releases the same node's Lua lock. Nothing in the
child need's change touches that lock, and the probe confirms it: the lock is
acquired by `base::bail`'s synchronous, thread-pinned call convention
(`src/base.rs`, vendored into every native cartridge, not part of this PRD's
declared footprint), not by anything `cartridge.ctg`'s transport layer
arbitrates.

## Acceptance

- [x] A `notifications/cancelled` for an in-flight tool call is observed by
      `notified` while that call is still registered in `inflight`.
- [x] The running tool receives the cancel and stops; a tool that honours
      `{"op":"cancel"}` is proven to have been reached.
- [x] A test drives a real in-flight call and a cancellation of it, failing in
      the world it denies — a test that passes when the lookup misses proves
      nothing.

## Needs

`@runtime/a-cartridge-call-can-be-cancelled` — done, but insufficient alone
(see Evidence): it lets a caller abandon its own call, not a second event
interleave with a first on the same node. Still needed, and not yet proposed
as a PRD: a `runtime`-board outcome that lets a native cartridge's own
outbound call to another cartridge (`base::bail`'s synchronous, thread-pinned
convention behind `cartridge.bail`'s blocking branch) not hold its whole
node's Lua state for the call's duration, so a second, independent event
dispatched to that node can run while the first is parked on another
cartridge's reply. Analyst verdict: SPLIT: propose that outcome as a sibling
child, this PRD's `needs` gains it, and this PRD is not specced until it
lands. See the analyst's `2026-09-19` report for the proposed child text.

## First step for the analyst

Done 2026-09-19: probed rather than argued from source alone. See Evidence.
The result is negative — dispatching a second `mcp` event while one is in
flight still does not let its cancellation reach the running tool, at the
current HEAD of the child need this PRD already lists.

## Answer applied (2026-09-19, user chose option A)

The user chose option A for
`@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node`: a
trampoline in each cartridge, with the host unchanged. So this PRD no longer
waits on a host change and owns the mcp side. `answer` returns a
`{call, data, id}` step instead of blocking in `base::bail`, and `init.lua`
loops `cartridge.bail` in the yieldable listener until the handler is done. The
footprint gains `src/base.rs` and `init.lua`. The proof is the probe from
`analyst-cancelled-1`: a `notifications/cancelled` sent 300 ms into a long call
reaches the tool. `base.rs` is vendored identically into `agent.ctg` and
`router.ctg`; bringing those copies in line is
`@root/the-vendored-base-rs-stays-identical-across-native-cartridges`, which
needs this PRD.

## Decision (2026-09-19, coordinator, at publish of spec01)

**The footprint gains one path: `.cartridge/tests/integration/cancel.test.ts`.**
Acceptance box 3 demands a test that drives a real in-flight call and observes
the cancellation reaching the running tool, and none of the four declared paths
can hold a test. The analyst cited the board's own precedent, which I checked:
`@mcp/the-mcp-event-declares-its-own-bound` carried a PRD footprint of
`["cartridge.json"]`, its spec added `.cartridge/tests/unit/tests.rs`, and it
landed as `1595a6f`. This is the same shape and is recorded rather than done
silently. `src/service.rs` stays in the footprint although the analyst found it
needs no change; removing it would not make the spec smaller.

## Open question for the reviewer (2026-09-19, coordinator)

The spec takes the trampoline route the user chose as Option A, and it is
prototyped rather than sketched: against a real `cartridge mcp` bridge the tool
answered `stopped-on-cancel 280052`, where the same test on unmodified
`1595a6f` gives `ran-to-completion`. But the trampoline costs two hazards the
spec has to solve — a 25 ms `wait` step answered by a bare `coroutine.yield()`
to break a deadlock when two messages of one instance race `Instance::session`'s
`OnceCell`, and a per-message snapshot of the base because `base::needs` reads
through a thread-local that a job does not have.

A cheaper mechanism for the same root cause was proven today in another
cartridge and the reviewer is asked to rule on it. cartridge-eb established
that `pty.ctg`'s `shell_op` (`pty.ctg/src/lib.rs:884`) held its node for the
same reason — a synchronous Lua function registered with `create_function`,
doing `block_on` — and that converting it to an async fn registered with
`create_async_function`, dispatching through `runtime().spawn(...)`, fixed it on
an **unmodified host**, because the host already drives listeners with
`call_async` (`cartridge.ctg/src/node/mod.rs:219-235`). Measured there: a
concurrent call that had timed out at 2012 ms against a 2000 ms bound answered
in 13.6 ms. Three lines of substance, no trampoline, no `init.lua` change.

`mcp.ctg`'s `answer` (`src/lib.rs:41-64`, registered at `:74`) has the same
shape as `shell_op`. So the question the reviewer must answer, by reading both
sites and saying which it is, is whether `create_async_function` does this
PRD's job without the trampoline and its two hazards — in which case spec01 is
solving a harder problem than the code requires — or whether `mcp.ctg`'s call
shape genuinely needs the trampoline, in which case the spec should say so
explicitly and that reasoning belongs in it.

One recorded trap either way: awaiting the dispatch future directly dies with
"there is no reactor running", because the cdylib links its own tokio and the
host's runtime cannot see it. Hence `runtime().spawn(...)`.

## Decision (2026-09-19, coordinator, after review round 1 passed at 92)

Round 1 passed at 92 of 100 with no blocking findings, so this PRD is
`specced`. The reviewer ruled on the `create_async_function` question by
building and running three variants itself rather than accepting the spec's
account: the async shape with `runtime().spawn(...)` and the same shape with a
`NEEDS` snapshot both answer `tools/list` as `[]`, the inline await dies with
`there is no reactor running`, and only the trampoline returns a populated
list and `stopped-on-cancel`. It also closed the `CARTRIDGE_YOLO` concern by
measurement: `mcp.ctg` declares no `yolo` setting, so the host has nothing to
merge, and the red/green pair is identical with the variable set and unset.

**I have applied the reviewer's F1 to the spec before publishing it, as a
one-line change that only tightens the gate.** F1: the bun `test` block set no
`CARGO_TARGET_DIR`, while `cancel.test.ts:10-11` falls back to a bare
`owner/target`. If the collector's environment exports `CARGO_TARGET_DIR`,
pass 2 would silently load the live tree's stale `target/debug/libmcp.dylib`
and could go green for code it never built — a false pass, which is the
dangerous direction. The block's `run:` line now pins
`CARGO_TARGET_DIR="$PWD/target/a-cancelled-tool-call-verify"` unconditionally,
matching the two cargo blocks around it. No Acceptance box, mechanism or
measurement changes, so the round-1 score stands and no re-review is owed.

The reviewer's other findings are recorded and not fixed here, deliberately:

- **F2** the `wait` step and its 25 ms park are unexercised — no probe reached
  them, no Acceptance box covers them, and the deadlock they prevent is
  asserted rather than demonstrated.
- **F3** Acceptance box 1 is not independently observable: its only check is a
  `grep block_on src/lib.rs`, and the design deliberately keeps a `block_on` in
  `base.rs`, which that guard never inspects.
- **F4** the spec does not say what a late or duplicate `resume` answers, so a
  job whose listener errors between steps stays filed with its future running.
- **F5** cosmetic: the spec says `tool::dispatch` "only spawns processes"; it
  works on an already-open shell.

F2, F3 and F4 are real gaps in what this spec proves, and the implementer's
verifier should be told so. They did not block a 92 and I am not inventing a
sixth round to chase them, but if the verifier finds box 1 unprovable by
anything but that grep, F3 becomes the reason and this PRD comes back rather
than being ticked on a text match.

One unscored side note from the reviewer, out of this footprint and worth its
own PRD: `cancel.test.ts` leaks a daemon per run, because `c.close()` kills the
bridge and not the daemon it started with `--idle-timeout 3600`.

## Verification (2026-09-19, coordinator, before ticking)

My implementer died on an API spend limit and wrote **no report**. Its lane
commit survived — `624afb3` on `1595a6f`, tree clean, exactly four files, no
`Cargo.toml` and no `src/service.rs` — but every claim it might have made was
lost with it. So the evidence below comes entirely from an independent verifier
(peer session cartridge-d0), which had the lane and the spec and was told
plainly that there were no claims to check. Its report is at
`.state/loop/a-cancelled-tool-call/verifier-1.md`. Every block ran verbatim
under `env -i`, twice: once with nothing set, once with `CARTRIDGE_YOLO=1`.

What was observed:

- **The red/green pair, in both directions and repeatedly.** The structural
  guard exits 1 on `1595a6f` with the lane's test copied in, and 0 on `624afb3`.
  `cancel.test.ts` is red in **6 of 6** runs unmodified — `Received
  "ran-to-completion"`, 0 pass 1 fail — and green in **6 of 6** on the lane,
  1 pass 0 fail. Six runs each way matters here: this test drives a real stdio
  bridge against a real daemon, so a single green could have been luck.
- `cargo test --lib`: 23 passed, 0 failed, 1 ignored on **both** trees in
  **both** environments, with all four named tests `ok`.
- `CARTRIDGE_YOLO` made no difference anywhere, which matches the reviewer's
  finding that `mcp.ctg` declares no such setting.
- The daemon started at 15:03:19, before every run, so no restart straddled the
  evidence.

**Box 1 is ticked on consequence, not on the guard, and the distinction is
worth recording.** Reviewer finding F3 stands exactly as written: `block_on`
remains at `src/base.rs:154` and the spec's grep never inspects that file, so
the guard alone cannot prove box 1. What proves it is the end-to-end result.
A `notifications/cancelled` arrives as its own event on the same node; if
`answer` still waited on the base's thread, that event would queue behind the
call it was meant to stop, `notified` would run too late, and the tool could not
answer `stopped-on-cancel`. It did, six times out of six. The node was free.
That is sound, but it is indirect, and the guard should be strengthened if this
code is revisited.

**The owner gates prove nothing here and were not treated as evidence.**
cartridge-d0 reports `just check mcp` and `just test mcp` exiting 0 in both
forms — but run against the live `mcp.ctg` at `1595a6f`, not against the lane.
That is the same trap that let a sibling PRD collect carrying unformatted code
earlier today. No box depends on them, so this does not block the collection;
it is recorded so nobody later mistakes those zeros for lane evidence.

**Two reviewer findings remain unproven and are not claimed.** F2: nothing
anyone ran shows whether the 25 ms `wait` step is ever taken, so the deadlock it
prevents is still asserted rather than demonstrated. F4: a late or duplicate
`resume` is not exercised. Neither is an Acceptance box, and neither is
invented into one now — but both are real gaps in what this PRD proves, and the
`wait` step in particular is load-bearing by the spec's own argument.

cartridge-d0 stopped the 12 daemons its runs leaked, by pid.
