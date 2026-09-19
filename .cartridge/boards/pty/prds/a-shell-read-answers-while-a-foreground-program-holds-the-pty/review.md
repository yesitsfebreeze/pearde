# @pty/a-shell-read-answers-while-a-foreground-program-holds-the-pty review history

Plan: `@pty/a-shell-read-answers-while-a-foreground-program-holds-the-pty`,
`prd.ctg/.cartridge/boards/pty/prds/a-shell-read-answers-while-a-foreground-program-holds-the-pty/prd.md`.
Scope: executable leaf. One observable outcome — a `tool.shell` read of a session
answers within its timeout while a foreground program holds that session's pty and
another `tool.shell` call of the same session is still waiting out its readback.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: 1, from `@pty/a-wedging-help-picker-must-not-hold-the-pty-node`,
out of whose review round 1 this PRD was split. The count survives the split and is
never reset, so the first review of this PRD in its own right is round 2.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.

## Round 2 — 2026-09-19

Presented revision: `prd.ctg` `813bfb5` working tree (`prd.md` modified, `specs/spec01.md`
new); source `pty.ctg` `9c64ee37a6622fb2192f2e73150108c14fe64891`, clean at HEAD.
Host read for the boundary claim: `cartridge.ctg` `ab2383a`.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../prd.md` — `7e51367ac17de214e26d80d52047c68806792d47714a5837538109712767d796` |
| Specs | `specs/spec01.md` — `696efc55ef6f201d7e6ad55ce5bc050d758936dfa49359593811a7991dff1997` |
| Material contracts/dependencies | `pty.ctg/cartridge.json` `43c7066cea16c57c8fecba36008f8fba24e701a7a9c9ce2d4670ec0f8ad3f847`; `pty.ctg/src/lib.rs` `a6e0f33fae29291b80e73db8009da7d83babdf812714645b683c5c980d41ccc9`; `pty.ctg/src/tool.rs` `1995a0e33516e61e0c9a9e01662893d2e06d1c97b55833bab3271157677ad085`; `cartridge.ctg/.cartridge/settings.json` (`event_timeout_ms` default 60000); `prd.ctg/src/lifecycle.ts` `verificationBlocks`/`testBlock`/`runTestBlock` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | The outcome is the failure coordinator sessions actually hit. The spec names one root cause and the reviewer reproduced it independently, from a `git archive` of `pty.ctg` HEAD outside the repository: the spec's test verbatim fails with "the concurrent read waited 3.610770167s for the in-flight call" (analyst measured 3.614 s). `shell_op` at `src/lib.rs:884` is registered with `lua.create_function` and calls `runtime().block_on(tool::dispatch(...))` at `src/lib.rs:888`; `cartridge.json` puts no `timeout_ms` on `tool.shell` and caps its input `timeout_ms` at 600000, so the held Lua state is caller-chosen and unbounded by the manifest. One outcome, no scope creep. |
| Ownership and reuse | 20 | Every step is inside `pty.ctg`. The spec's footprint (`src/lib.rs`, `src/tool.rs`, `Cargo.toml`, `Cargo.lock`, `.cartridge/tests/integration/process.rs`, `README.md`, `.cartridge/help.md`) covers each of the six steps with nothing left over; `planner.ts:7` unions the spec's footprint with the PRD's, so the spec does narrow the otherwise repo-wide reservation. The fix reuses mlua's own `async` feature and the existing `tool_gate` (`src/lib.rs:213`, a `tokio::sync::Mutex` taken by `try_lock` at `src/tool.rs:118`) rather than adding new serialization; the doc pair is updated in the same change, as the cartridge README rule requires. |
| Dependencies and implementable slices | 17 | The claim that the host is not the blocker holds: the host drives listeners with `f.call_async(...)` at `cartridge.ctg/src/node/mod.rs:219-235`, and the reviewer's fixed tree passed against the **unmodified** live `cartridge.ctg/target/release/cartridge` binary. `@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node` is therefore not a prerequisite. One slice, seven files, mechanical. The `Cargo.lock` claim is accurate and was checked: the lock really does gain `futures-core`, `futures-task`, `futures-util` and `slab` (diff against `HEAD:Cargo.lock`), so `--locked` in two blocks genuinely forces the implementer to commit it. `runtime()` is `new_multi_thread` (`src/lib.rs:766`), which is what makes `spawn(...).await` sound where a direct await is not. **Deduction, −3, finding 5:** the spec's rationale generalises. "A handler that yields lets another request in" and "Only pty.ctg refuses to yield" are stated without any condition, and evidence from another session (below) shows the same shape built in `mcp.ctg` cannot reach a single provider. The spec never says *why* it works here, so its own reasoning invites the generalisation that breaks a sibling cartridge. |
| Observable acceptance and baseline evidence | 19 | The `test` block discriminates. At HEAD the named test fails (above); with the spec's `shell_op`/`Cargo.toml` patch applied verbatim the whole `process` suite is 12 passed, 0 failed in 23.19 s, and all five pinned `pass:` names appear as `test <name> ... ok`, the exact form `passedTests` parses. The python block discriminates in three states, each executed as `sh -eu`: exit 1 at live HEAD ("mlua is not built with the async feature"), exit 1 with only the `mlua` feature added ("the shell handler still blocks the node's Lua state"), exit 0 fully patched. No inert construct in any block — no `! grep`, no `test -n … && test …`, no `${VAR:?}`; both parameter expansions are `:-` and safe under `set -u`. All three `sh` blocks were run as the collector runs them and exited 0 on the patched tree. `CARGO_TARGET_DIR` is exported for `clippy` and for the `test` block, and the reviewer confirmed cargo passes that variable through to the test binary, so `module()`'s inner `cargo build --lib` also lands in the isolated dir and never rebuilds the live `target/debug` dylib. Deductions: `cargo clippy --locked --all-targets` carries no `-- -D warnings`, so the "clippy is clean" acceptance box is only partly gated (mitigated, not cured, by `[lints.rust] warnings = "deny"` in `pty.ctg/Cargo.toml:30-31`, which does fail the block on rustc warnings); and the python block's first message names its own cure, which is tolerable only because that cure is not a bypass of the behavioural gate. |
| Failure, recovery and compatibility | 19 | The two now-false comments are both real and both in the footprint (`src/tool.rs:152` and `.cartridge/tests/integration/process.rs:616`); the spec rewrites them instead of leaving the code lying about itself. The concurrency the fix opens is already bounded: a second `call` carrying `command`/`input` is refused by `tool_gate.try_lock()` at `src/tool.rs:118`, and `shell_serializes_input_and_only_cancels_the_matching_invocation` is pinned in the `test` block and passes with the fix, so the cancel/serialization contract is proved, not asserted. `JoinError` is mapped rather than unwrapped. Deduction: the `pty_op` ceiling is stated but its safety is left implicit. It is in fact defensible — `pty`'s own dispatch awaits at most an 80 ms sleep, and `tool.shell` declares no `timeout_ms` so it inherits the host's 60000 ms `event_timeout_ms` default, far above the 2000 ms `pty` bound — but the spec asserts "bounded and short" without naming the number that makes a `pty_op` hold harmless to this outcome. Checked against finding 5: `pty_op` is on the *same* side of the re-entry line as `shell_op`, so the asymmetry gains no second justification from it and remains purely a latency choice. |
| Reviewer total | 95 / 100 | Pass. No blocking finding; finding 5 is a mandatory pre-collect revision. |

Findings and concrete revisions:

1. Non-blocking, optional. `cargo clippy --locked --all-targets` (Verify block 2)
   has no `-- -D warnings`, so clippy's own lints cannot fail collection even
   though the acceptance box claims clippy is clean. `pty.ctg/Cargo.toml:30-31`
   denies rustc warnings, which covers the realistic fallout of this change (an
   unused import when `&Lua` becomes `Lua`), and `just check pty` is named as the
   post-integration gate. Recommendation: append `-- -D warnings`. Not required to
   pass.
2. Non-blocking. `cargo fmt --all --check` (Verify block 1) sets no isolated
   `CARGO_TARGET_DIR`. Verified empirically that `cargo fmt --all --check` creates
   no `target/` directory at all, so it cannot rebuild the live dylib; collected
   specs on this board already carry a bare `cargo fmt` block. No change needed.
3. Non-blocking, wording. The `pty_op` ceiling would read as a measured bound
   rather than a hope if it named the two numbers behind it: `pty`'s dispatch
   awaits at most 80 ms, and `tool.shell` inherits the host's 60000 ms
   `event_timeout_ms` because it declares none, so a 2000 ms `pty_op` hold cannot
   make a `tool.shell` read time out.
4. Accepted ceiling, not a finding. The README and `.cartridge/help.md` sentences
   of step 6 carry no executable gate. The spec's reason is true and was checked:
   both files already contain "readback" at `9c64ee3`
   (`README.md:15`, `.cartridge/help.md:7`), so `grep -qi readback` is inert, and
   a tighter phrase test would print its own cure. `review-plan.md` permits
   exactly this — one round spent, ceiling recorded, diff reading named as the
   backstop — and says such a claim "is not by itself a blocking finding". The
   spec states the ceiling in the open rather than hiding it. Honest and adequate.

5. **Mandatory before collect, not blocking. The spec's rationale claims more
   than it proved.** Cross-session evidence supplied by the coordinator during
   this round: another analyst built the exact shape this spec prescribes (mlua
   `async`, handler as `async fn`, `create_async_function`, dispatch via
   `runtime().spawn(...).await`) in a clean clone of `mcp.ctg` `1595a6f` with
   `init.lua` untouched. It compiles and answers lines but reaches no provider —
   both readings return `Err("not on the base's thread")`, the tool list A/Bs
   from `[{"name":"slow",…}]` to `[]`, and `cancel.test.ts` and
   `instances.test.ts` both go 0 pass, 1 fail. The cause is structural:
   `mcp.ctg/src/base.rs:30-54` reaches the node through an `ENTERED` thread-local
   that only `base::entered` sets, and `create_async_function` never passes
   through `entered` at all, so re-adding it cannot rescue the shape — a
   synchronous scope cannot span an await the host's driver may poll on any
   thread. `agent.ctg` and `router.ctg` vendor the same `base.rs`.

   The spec's sentences "a handler that yields lets another request in" and
   "Only pty.ctg refuses to yield" are therefore false as general statements, and
   the spec gives no condition under which they hold. The reviewer verified the
   discriminator against `pty.ctg` directly:
   `grep -rnE "base::bail|base::notify|cartridge\.call_function|base::needs" pty.ctg/src/`
   returns nothing (exit 1), and the structural reason is stronger than the grep:
   `pty.ctg` has no `base.rs` at all, and its notifications leave as protocol
   lines through a `cartridge.pipe` file handle (`Relay(Mutex<Option<File>>)`,
   `src/lib.rs:728-730`), documented at `src/lib.rs:18-21` as "which the node
   sends without touching Lua". `pty::tool::dispatch` only spawns processes. So
   the fix works here **because** pty's handler never re-enters its own node's
   Lua state — and that, not "the host uses `call_async`", is the load-bearing
   fact.

   Required revision, one sentence in the paragraph that currently ends "Only
   pty.ctg refuses to yield": state that a handler may become
   `create_async_function` only when it never calls back into its own node, that
   `pty.ctg` qualifies because it owns no vendored `base.rs` and relays output
   through a pipe file rather than Lua, and that a cartridge which does re-enter
   (`mcp.ctg`, `agent.ctg`, `router.ctg`) needs a trampoline instead. Naming the
   grep above as the mechanical test is worth a clause.

   Ruled non-blocking rather than blocking, deliberately: the spec executed as
   written still produces the correct, proven result for `pty.ctg`, and the
   revision narrows a claim without changing any behaviour, footprint, block or
   acceptance box, so under the method's rule on formatting-grade change it does
   not make this rating stale and does not need round 3. It is nonetheless
   mandatory — the spec is the only place this mechanism is written down, and an
   unqualified rule here is what a later analyst will cite at `agent.ctg` or
   `router.ctg`. If the coordinator prefers the stricter reading, treat it as
   blocking and spend round 3; the score would be unchanged either way.

6. **Record correction.** Nothing of this fix has landed. `pty.ctg` HEAD
   `9c64ee3` still carries `fn shell_op(lua: &Lua, …)` at `src/lib.rs:884`,
   `runtime().block_on(...)` at `:888`, `lua.create_function(shell_op)` at `:909`
   and `mlua` without `async` at `Cargo.toml:17`; `git status --porcelain` in
   `pty.ctg` is empty. Every "with the fix applied" row in the validation table
   below is a throwaway tree under `/tmp`, never the checkout. This round scores
   a proposal.

Scope: confirmed clean. The spec's footprint and all six steps are inside
`pty.ctg`. `@pty/a-wedging-help-picker-must-not-hold-the-pty-node` and
`@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node` are
referenced only to disclaim them; no file of either is touched, and the
disclaimer of the runtime PRD was independently verified against the unmodified
host binary rather than taken on the spec's word.

Disposition: keep. Proceed to implementation on this spec as written.

Validation (reviewer's own commands; the live checkout was never built in):

| cwd | command | exit / result |
| --- | --- | --- |
| `/Users/feb/dev/cartridge/pty.ctg` | `git log --oneline -1`; `git status --porcelain` | `9c64ee3`, clean |
| `/Users/feb/dev/cartridge/pty.ctg` | `sh -eu` on the spec's python Verify block (extracted by `verificationBlocks`'s own regex) | 1, "mlua is not built with the async feature" |
| `/tmp/rev2-gate` (copy, `mlua` async only) | same block | 1, "the shell handler still blocks the node's Lua state" |
| `/tmp/rev2-gate` (copy, full fix) | same block | 0 |
| `/` | `git -C pty.ctg archive HEAD \| tar -x -C /tmp/rev2-pty` | 0 |
| `/tmp/rev2-pty` (HEAD + spec's test only) | `CARGO_TARGET_DIR=/tmp/rev2-target CARTRIDGE_BIN=<live release> cargo test --locked --test process read_answers_… -- --test-threads=1` | 101; **FAILED**, "the concurrent read waited 3.610770167s for the in-flight call" |
| `/tmp/rev2-pty` (spec's fix applied verbatim) | `cargo fmt --all --check`; `cargo clippy --all-targets`; `cargo test --locked --test process -- --test-threads=1` | 0; **12 passed, 0 failed** in 23.19 s, all five pinned names `… ok` |
| `/tmp/rev2-pty` | `diff <(git -C pty.ctg show HEAD:Cargo.lock) Cargo.lock` | lock changes, gaining exactly `futures-core`, `futures-task`, `futures-util`, `slab` |
| `/tmp/rev2-pty` | `sh -eu` on Verify blocks 0, 1 and 2 as the collector runs them | 0, 0, 0 |
| `/tmp/rev2-envprobe` | `CARGO_TARGET_DIR=… cargo test` printing `env::var("CARGO_TARGET_DIR")` from inside the test binary | 0; the variable is inherited, so `module()`'s inner build stays isolated |
| `/tmp/rev2-fmt` | `cargo fmt --all --check` with `CARGO_TARGET_DIR` unset | 0; no `target/` created |
| `/Users/feb/dev/cartridge` | `grep -rnE "base::bail\|base::notify\|cartridge\.call_function\|base::needs" pty.ctg/src/` | 1, no output — pty never re-enters its node |
| `/Users/feb/dev/cartridge` | `ls pty.ctg/src/`; `sed -n '18,21p;726,730p' pty.ctg/src/lib.rs` | no `base.rs`; output relays through a `cartridge.pipe` `File`, "without touching Lua" |
| `/Users/feb/dev/cartridge` | `sed -n '17p' pty.ctg/Cargo.toml`; `sed -n '884p;888p;909p' pty.ctg/src/lib.rs`; `git -C pty.ctg status --porcelain` | HEAD still `create_function`/`block_on`/no `async`; tree clean — the fix has not landed |

Reviewer identity: independent reviewer subagent `reviewer-1`, Claude Opus 5 (1M context),
session `18d6b8b7906f0a28-2`, working directory `/Users/feb/dev/cartridge`.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this round.
Result: **PASS** (95/100).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: apply finding 5's one-sentence scoping revision to `specs/spec01.md`,
then proceed to implementation. Findings 1 and 3 are optional polish. None of the
three changes behaviour, footprint, a Verify block or an acceptance box, so this
rating survives them and round 3 stays unspent.
