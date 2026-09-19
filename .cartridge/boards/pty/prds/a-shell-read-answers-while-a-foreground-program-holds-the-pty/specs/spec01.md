---
complexity: 2
footprint:
  - src/lib.rs
  - src/tool.rs
  - Cargo.toml
  - Cargo.lock
  - .cartridge/tests/integration/process.rs
  - README.md
  - .cartridge/help.md
---

# spec01 — the shell tool yields the node while it waits, so a read answers during an in-flight call

Spec for the leaf @pty/a-shell-read-answers-while-a-foreground-program-holds-the-pty.
Base: pty.ctg `9c64ee3` (clean at HEAD). The two accounts in the PRD's Evidence
were both partly right, and an executed probe settled it.

The read path in `src/tool.rs` is correct, as the sibling's analyst judged: a
plain read (no `command`, no `input`) returns at `src/tool.rs:117` before
`tool_gate`, and `readback()` takes only short-lived grid and ring locks. That
was confirmed by probe: with `cat` holding the pty as a standing foreground
program, sequential `tool.shell` reads returned `phase: "running"` and a screen
containing the program's own output.

The failure the coordinator sessions saw is one level below that, and it is
pty.ctg's own. `shell_op` (`src/lib.rs:884`) is registered with
`lua.create_function` and calls `runtime().block_on(tool::dispatch(...))`. A
synchronous Lua function cannot yield, so the node's single Lua state is held
for the entire duration of a `tool.shell` call, including the caller-chosen
`timeout_ms` readback wait of up to 600000 ms. Every other event on the pty node
queues behind it. The probe reproduced the reported symptom verbatim: with a
`tool.shell` call in flight on a 4000 ms readback, `pty {"op":"commands"}`
returned the string `pty did not answer in time` after 2012 ms, which is the
`pty` event's declared 2000 ms bound in `cartridge.json`.

This is a defect inside this cartridge's footprint, not the host's event
serialization. The host already drives listeners with `call_async`
(`cartridge.ctg/src/node/mod.rs:219-235`), so a handler that yields lets another
request in. Only pty.ctg refuses to yield. The host-side question in
@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node is
therefore not a prerequisite for this outcome, and this spec does not touch it.

`shell_op` must become an async Lua function. Its future is polled by the host's
tokio runtime, which is a different tokio instance from the one linked into this
cdylib, so awaiting pty's own futures directly there fails at runtime with
`there is no reactor running, must be called from the context of a Tokio 1.x
runtime` (observed). The work is therefore handed to pty's own runtime with
`runtime().spawn(...)` and the resulting `JoinHandle` awaited, which needs only a
waker and no reactor.

`pty_op` keeps its `block_on`. Its dispatch awaits at most an 80 ms sleep, and
`tool.shell` declares no `timeout_ms` in `cartridge.json`, so it inherits the
host's 60000 ms `event_timeout_ms` default; an 80 ms `pty_op` hold therefore
cannot make a `tool.shell` read time out, and the `pty` event's own declared
bound is 2000 ms. That is a deliberate latency ceiling, not an oversight.

## Steps

1. `Cargo.toml`: add `"async"` to the `mlua` feature list, giving
   `features = ["lua54", "module", "serde", "async"]`. Commit the resulting
   `Cargo.lock`, which gains `futures-core`, `futures-task`, `futures-util` and
   `slab`. The Verify block runs `cargo` with `--locked`, so an uncommitted lock
   fails collection.
2. `src/lib.rs`: make `shell_op` an async function taking `Lua` by value, and
   register it with `lua.create_async_function`. It resolves the shell, then
   awaits `runtime().spawn(async move { tool::dispatch(&shell, args).await })`
   and maps a `JoinError` to its string. `answer` is then called with `&lua`.
   The proven shape:

   ```rust
   async fn shell_op(lua: Lua, args: LuaValue) -> LuaResult<Answer> {
   	let args = lua_json::to_json(args)?;
   	let prepared = service().map(|service| service.shell.lock().unwrap().clone());
   	let result = match prepared {
   		Ok(shell) => match runtime()
   			.spawn(async move { tool::dispatch(&shell, args).await })
   			.await
   		{
   			Ok(result) => result,
   			Err(error) => Err(error.to_string()),
   		},
   		Err(error) => Err(error),
   	};
   	answer(&lua, result)
   }
   ```

3. `src/tool.rs`: the comment closing `dispatch_inner`, "The owner stays while
   its command runs: the node answers one event at a time, so a `cancel` or
   takeback can only arrive after this wait", is now false in its reason. The
   logic is unchanged and stays: `tool_owner` is set before the wait, a matching
   `cancel` arriving during the wait is exactly what `cancel` is for, and a
   non-matching one is still refused. Rewrite the comment to say that the owner
   is published before the wait so a concurrent matching `cancel` can interrupt
   the command, and that the owner is cleared only when the shell is no longer
   running.
4. `.cartridge/tests/integration/process.rs`: add the named test below. `cat`
   with no argument is the standing foreground program that reads the terminal
   and never exits, so the test needs no picker, pager or editor on the PATH.
   The test has two halves. The first drives sequential reads and asserts the
   screen carries the program's output while `phase` is `running`; that half
   already passes at HEAD. The second is the one that fails at HEAD: it holds a
   `tool.shell` call in flight on a 4000 ms readback from another thread, issues
   a read of the same session, and asserts that the read both carries the screen
   and returned in under 2000 ms.

   ```rust
   /// A foreground program that reads the terminal and never exits holds the pty;
   /// a read of the same session still answers within its timeout with the screen,
   /// including while another `tool.shell` call of the same session is in flight.
   #[test]
   fn read_answers_while_a_foreground_program_holds_the_pty() {
   	let (host, _dir) = boot("/bin/bash");
   	let context = json!({"session":"s","run":"picker","call":"open","cwd":"/"});
   	// `cat` with no argument reads the terminal and never exits: the standing
   	// foreground program a picker or a pager is, without the dependency.
   	let launched = host
   		.call(
   			"tool.shell",
   			json!({"op":"call","context":context,"input":{"command":"printf 'picker-open\\n'; cat","timeout_ms":500}}),
   		)
   		.unwrap();
   	assert_eq!(launched["error"], false, "{launched}");
   	let mut screen = Value::Null;
   	for _ in 0..100 {
   		let read = host
   			.call(
   				"tool.shell",
   				json!({"op":"call","context":context,"input":{"timeout_ms":0}}),
   			)
   			.unwrap();
   		screen = serde_json::from_str(read["content"].as_str().unwrap()).unwrap();
   		if screen["screen"].as_str().unwrap().contains("picker-open") {
   			break;
   		}
   		sleep_ms(20);
   	}
   	assert!(
   		screen["screen"].as_str().unwrap().contains("picker-open"),
   		"{screen}"
   	);
   	assert_eq!(screen["phase"], "running", "{screen}");

   	// The decisive case: a second call of the same session is in flight, waiting
   	// out a long readback, while the read is issued.
   	let held = {
   		let host = Arc::clone(&host);
   		std::thread::spawn(move || {
   			host.call(
   				"tool.shell",
   				json!({"op":"call","context":{"session":"s","run":"picker","call":"hold","cwd":"/"},"input":{"input":"held-input\r","timeout_ms":4000}}),
   			)
   		})
   	};
   	sleep_ms(400);
   	let started = Instant::now();
   	let read = host
   		.call(
   			"tool.shell",
   			json!({"op":"call","context":{"session":"s","run":"picker","call":"concurrent","cwd":"/"},"input":{"timeout_ms":0}}),
   		)
   		.unwrap();
   	let waited = started.elapsed();
   	let concurrent: Value = serde_json::from_str(read["content"].as_str().unwrap()).unwrap();
   	assert!(
   		concurrent["screen"]
   			.as_str()
   			.unwrap()
   			.contains("picker-open"),
   		"{concurrent}"
   	);
   	assert!(
   		waited < Duration::from_millis(2000),
   		"the concurrent read waited {waited:?} for the in-flight call"
   	);
   	held.join().unwrap().unwrap();
   	host.stop();
   }
   ```

5. `.cartridge/tests/integration/process.rs`: the comment inside
   `shell_serializes_input_and_only_cancels_the_matching_invocation`, "The node
   answers one event at a time, so the call waits out its own timeout first", is
   now wrong about the node. That test asserts sequential behaviour and keeps
   passing; correct the comment to say the call waits out its own readback
   before returning, without claiming the node is serialized.
6. `README.md` (`## Use`) and `.cartridge/help.md` (`## Use`, the `shell` bullet):
   one sentence each saying that a read of the terminal answers while another
   `tool.shell` call of the same session is still waiting out its readback, so a
   standing foreground program never makes the shell tool time out. Both files
   are updated in the same change, as the cartridge README rule requires.

## Acceptance

- [ ] `.cartridge/tests/integration/process.rs` carries a test named `read_answers_while_a_foreground_program_holds_the_pty` that starts a foreground program reading the terminal that never exits, and asserts a concurrent `tool.shell` read of the same session returns the screen contents in less than 2000 ms while another call of that session waits out a 4000 ms readback.
- [ ] That test passes. It fails on pty.ctg `9c64ee3` before the fix, waiting 3.614 s for the in-flight call, so it is a live regression lock and not a tautology.
- [ ] `shell_op` in `src/lib.rs` is registered with `lua.create_async_function` and no longer calls `runtime().block_on`, so a `tool.shell` call releases the node's Lua state while it waits.
- [ ] The rest of the `process` integration suite still passes unchanged, including `shell_serializes_input_and_only_cancels_the_matching_invocation`, `shell_controls_nvim_and_reads_the_visible_screen` and `handoff_blocks_agent_input_and_takeback_interrupts_without_closing_shell`.
- [ ] `cargo fmt --all --check` and `cargo clippy --all-targets` are clean, and `Cargo.lock` is committed so `cargo --locked` succeeds.
- [ ] `README.md` and `.cartridge/help.md` both state that a read answers while another `tool.shell` call of the same session is waiting out its readback.

## Verify

```sh
cargo fmt --all --check
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/shell-read-verify}"
cargo clippy --locked --all-targets
```

```sh
python3 - <<'PY'
import pathlib, sys, tomllib
root = pathlib.Path(".")
mlua = tomllib.loads((root / "Cargo.toml").read_text())["dependencies"]["mlua"]
if "async" not in mlua["features"]:
    sys.exit("mlua is not built with the async feature")
lib = (root / "src/lib.rs").read_text()
start = lib.index("fn shell_op")
body = lib[start:lib.index("\n}\n", start)]
if "block_on" in body:
    sys.exit("the shell handler still blocks the node's Lua state")
PY
```

The README and help sentences of step 6 are a reviewer gate, not a block. Every
text test for them that was tried is inert: both files already say "readback"
at `9c64ee3` (`.cartridge/help.md`, the `shell` bullet), and any tighter phrase
test would print the exact words that satisfy it. The diff reviewer is the
backstop for that box, as the spec template says it is for a block's body.

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/shell-read-verify}"; CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}" cargo test --locked --test process -- --test-threads=1
pass: read_answers_while_a_foreground_program_holds_the_pty
pass: shell_serializes_input_and_only_cancels_the_matching_invocation
pass: shell_controls_nvim_and_reads_the_visible_screen
pass: handoff_blocks_agent_input_and_takeback_interrupts_without_closing_shell
pass: terminal_tool_runs_in_the_users_shell_and_commands_report_it
```

Measured on a clone of pty.ctg `9c64ee3` with the fix applied, this machine, a
cold `CARGO_TARGET_DIR`: the single test builds and runs in 16 s. The `test`
block above was run exactly as `runTestBlock` runs it, `sh -eu` with the same
two positional arguments and a cold `target/shell-read-verify`, and finished in
32 s at exit 0 with all five named tests reported as `... ok`. `cargo clippy` is
4 s warm and `cargo fmt --all --check` under 1 s. All are inside the collector's
120 s per-block limit. `CARTRIDGE_BIN` is pinned because the test's `base()`
otherwise falls back to `../cartridge.ctg/target/release/cartridge`, which does
not resolve from the lane.

Note, not a box: after collection, `just check pty` and `just test pty` from
`/Users/feb/dev/cartridge`, and `just isolation`, are the post-integration gates.
