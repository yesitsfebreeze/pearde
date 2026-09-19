---
state: "failed"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/pty.ctg"
---

# A shell read answers while a foreground program holds the pty

## Outcome

While a foreground program holds the wrapped shell's pty (an interactive picker,
a pager, a REPL), a concurrent `tool.shell` read of that session answers within
its timeout with the current screen. It never reports "mcp did not answer in
time".

## Evidence

Coordinator sessions saw the failure on 2026-09-16 and 2026-09-17: while
`cartridge help <id>` held the picker open, the next shell tool call returned
"mcp did not answer in time". On 2026-09-19 the analyst of
`@pty/a-wedging-help-picker-must-not-hold-the-pty-node` read `pty.ctg/src/tool.rs`
and `src/lib.rs` and judged the concurrent-read path correct at HEAD. The two
accounts disagree, and only a test can settle which is true. The host-side
picker fix is that sibling's work; this PRD owns the pty side. The earlier
failure may also have come from the host serializing events on a node, which is
`@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node`.

## Acceptance

- [ ] A named test in `pty.ctg` runs a foreground program that reads the terminal and never exits, then performs a concurrent read of the same session. The read answers within its timeout with the screen contents.
- [ ] If the test fails at HEAD, the fix makes it pass. If it passes at HEAD, the report says so, and the test stays as a regression lock.

## Scope note: why this fix is not general

Recorded 2026-09-19 by the coordinator, from another session's measurement, so
that no reader generalises the spec's fix to the other native cartridges.

`create_async_function` is the right shape here **because** `pty.ctg`'s
`tool::dispatch` only spawns processes and never calls back into its own node's
Lua state. The mechanical test is
`grep -rn "base::bail|base::notify|cartridge.call_function|base::needs" pty.ctg/src/`,
which returns nothing.

In `mcp.ctg` the same shape was built as a clean clone and fails: it compiles in
5.57 s and answers lines, but reaches no provider, returning
`{"inline":"Err(\"not on the base's thread\")","spawned":"Err(\"not on the base's thread\")"}`.
A/B with only the module differing gave `{"result":{"tools":[]}}` for the async
shape against `{"result":{"tools":[{"name":"slow",...}]}}` for the existing
trampoline, and both `cancel.test.ts` and `instances.test.ts` went 0 pass, 1
fail. `mcp` needs its node's state for every unit of work — policy, sessions,
describe, call, cancel — through `base::bail` to `with()` to the `ENTERED`
thread-local set by `base::entered` (`src/base.rs:30-54`). The inline reading
fails too, not only the spawned one: `create_async_function` never passes
through `base::entered`, and that is a synchronous scope which cannot span an
await the host's driver may poll on any thread.

So: a handler that never re-enters its own node can become
`create_async_function`; a handler that does needs a trampoline handing the call
back out to the listener already on the base's thread. `agent.ctg` and
`router.ctg` carry the same vendored `base.rs` as `mcp.ctg` and fall on the
trampoline side. Run the grep before pointing this fix at any of them.

## Failure

**The implementation is done and verified; one Acceptance box could not be
proven before this coordinator session ended. The lane is intact and must not
be discarded.**

Lane `a1ee509d9bf5be5b4b6a6d743b772f601f2df6e9` on
`lane/pty-a-shell-read-answers-while-a-foreground-program-holds-the-pty`,
parent `9c64ee3`, tree clean, seven files, 125 insertions and 14 deletions, all
inside `pty.ctg`.

**What is proven.** An independent verifier (peer session cartridge-d0, not the
implementer) reproduced three-state discrimination with the lane's `process.rs`
copied into every state, so the behavioural test runs in all three:

- A, `9c64ee3`: python gate exit 1, `mlua is not built with the async feature`;
  test block exit 101, sole failure `read_answers_while_a_foreground_program_holds_the_pty`.
- B, `9c64ee3` plus only the `mlua` `async` feature: gate exit 1,
  `the shell handler still blocks the node's Lua state`; test block exit 101,
  same sole failure.
- C, the lane: gate exit 0.

`fmt` and `clippy` exit 0 in all three states. `Cargo.lock` gained exactly
`futures-core`, `futures-task`, `futures-util` and `slab`. Nothing in the lane
reaches outside `pty.ctg`. `CARTRIDGE_YOLO` made no difference anywhere. A
half-done implementation cannot pass this gate, which is what state B
establishes.

**Why it was not collected.** Spec Acceptance box 4 requires that the rest of
the `process` suite "still passes unchanged, **including**
`shell_serializes_input_and_only_cancels_the_matching_invocation`". In state C
that named test passed 5 of 6 runs and failed once, exit 101, at
`process.rs:696:5` (`sleep 30` still running, "no output marks yet"). It passed
in states A and B. A foreign second daemon (pid 18435, 16:17:39) was up around
the failing run, but **the cause was not established**. Five of six is not
"passes unchanged" for a box that names the test explicitly, and the difference
matters: the whole point of that box is that the async conversion must not
disturb input serialization.

**A caution for whoever picks this up: my own attempt to rerun that test was
invalid, and its red is not evidence.** I ran it in the lane with
`CARGO_TARGET_DIR` pointed at a fresh empty directory and no `CARTRIDGE_BIN`.
Both the single-test run and the full suite failed instantly — the full suite
in 0.19 s with all twelve red — at `.cartridge/tests/integration/process.rs:25`
with `…/cartridge.ctg/target/release/cartridge is not built; build the base or
set CARTRIDGE_BIN`. That is a harness failure of my making, not a defect in the
lane. Reproduce the spec's own block instead of improvising one.

**What the next coordinator should do.** `retry` this row, then run the `process`
suite in the lane through the spec's Verify block several times on a quiet host,
with no other session's daemon starting or stopping. If
`shell_serializes_input_and_only_cancels_the_matching_invocation` is green
consistently, tick the boxes and collect `a1ee509` unchanged — no
re-implementation is needed. If it is genuinely intermittent on the lane and
not at base, that is a real finding about the async conversion and belongs in a
new review round, not in a tick.

**One more thing the record should carry.** The owner gates `just check pty` and
`just test pty` exited 0, but `pty.ctg` is at `9c64ee3`, so they **did not
execute this lane**: their `process` suite reports 11 tests against the lane's
12, and the missing one is the lane-only test. Those zeros are not evidence for
this revision. This is the same trap that let a sibling PRD collect carrying
unformatted code earlier today.
