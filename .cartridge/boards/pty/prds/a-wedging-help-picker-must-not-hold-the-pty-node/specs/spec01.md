---
complexity: small
footprint:
  - src/cli/manual.rs
---

# spec01 — A single `q` or `Esc` quits the help picker's list instead of being consumed

Base: `cartridge.ctg` at `beb8213d7236a228be2dca531e726cdad5d624ab`
(`Cancel an abandoned call on the provider, not just the caller's future`).

Revision 2, after review round 1 (76/100, FAIL): B1 (the test proved only a
pure helper, not the loop it was meant to protect) is fixed by giving the
test a seam into the real loop. B2 (the concurrent-read box) is resolved by
the coordinator moving it to its own PRD; it is gone from this spec. N1–N4
are folded in below.

## Repo correction (recorded, per coordinator decision)

The PRD's `repo` was `pty.ctg`; the picker and its bug live in `cartridge.ctg`
(the host CLI), not in the pty cartridge. `repo` is now
`/Users/feb/dev/cartridge/cartridge.ctg`. `pty.ctg` allocates the real pty
(`libc::openpty`, `pty.ctg/src/lib.rs:230-264`) that makes `isatty` true for
`cartridge help` inside the wrapped shell, same as a human terminal, but
carries no defect of its own here.

## The concurrent-read box moved out

The original box 2 ("while the picker is open, a concurrent `tool.shell`
read still answers within its timeout") is no longer part of this PRD. It is
`pty.ctg` behavior, outside this spec's footprint and repo, and round 1
correctly found that a code reading alone — with no named, executed check —
is not an Acceptance proof, and that the reading conflicted with this PRD's
own observed evidence ("mcp did not answer in time"). The coordinator filed
`@pty/a-shell-read-answers-while-a-foreground-program-holds-the-pty` to
carry it, with this note as a starting point: a plain read (no
`command`/`input`) in `dispatch_inner` (`pty.ctg/src/tool.rs:117` at
`pty.ctg` HEAD `9c64ee3`) returns before touching `tool_gate`, and
`readback()` (`pty.ctg/src/tool.rs:20-28`) only takes short-lived
`std::sync::Mutex` locks on the ring buffer/grid — but `tool.rs` also says
"the node answers one event at a time", and a `run` call (not a plain read)
can wait behind an in-flight command for up to that call's `timeout_ms`
(≤600000). That tension, and the observed "did not answer in time", is
unresolved and belongs to the new PRD, not here.

## What is broken, exactly

`cartridge help <id>` on a terminal opens `browse()` (`src/cli/manual.rs:723`),
a list picker with a text filter. Its key loop (`src/cli/manual.rs:743-773`
at base) treats every plain character — including `q` — as filter text
(`Key::Char(c) => level.query.push(c)`), and binds `Esc`/`Left` (both decode
to `Key::Back`, `src/cli/manual.rs:716`) to walking one level up the address
stack, only returning from `browse()` when that walk reaches the root with
an empty address. From a module's doc list that is two or three presses, not
one, and `q` never exits at all — only `Ctrl-C` (`Key::Quit`) does. This is
the observed wedge: the picker consumes both `q` and a single `Esc` as
ordinary input instead of exiting, and nothing sends it further keystrokes
when it is opened by an automated `tool.shell` command rather than a human.

On the search path (`cartridge help <words>`, no exact address match: `help()`
passes `what` as the picker's initial `query`, `src/cli/manual.rs:51`), the
list opens with a non-empty filter already in place, so `q` is literal
filter text from the first frame and only `Esc` exits in one press — stated
explicitly in Acceptance below, since this path never has an "empty filter"
moment for `q` to catch.

The doc/section viewer, `view()` (`src/cli/manual.rs:888-946`), is not part
of this bug: its footer already reads `esc back · q quit`, and its key match
(`Key::Quit | Key::Char('q') => return Ok(false)`, `Key::Back | Key::Erase =>
return Ok(true)`, `src/cli/manual.rs:934-935`) already does exactly that —
`q` quits the whole picker, `Esc`/`Left` return to the list. `view()`'s
behavior does not change.

## The fix

`Esc` and `Left` currently decode to the same `Key::Back` (`src/cli/manual.rs
:716`, `KeyCode::Esc | KeyCode::Left => Key::Back`). Round 1's N1 finding: a
fix that makes `Key::Back` always exit would make `Left` quit the whole
picker too, when today `Left` only steps up a level and should keep doing
that. So `Esc` gets its own `Key` variant, `Key::Exit`, distinct from
`Key::Back` (which `Left` keeps):

```rust
// enum Key gains a variant:
Exit,

// key(): split the combined arm
KeyCode::Esc => Key::Exit,
KeyCode::Left => Key::Back,

// view(): Esc still means "back to the list", exactly as before
Key::Back | Key::Erase | Key::Exit => return Ok(true),
```

In `browse()`'s loop, extract the loop itself into `run()`, generic over a
key source and a renderer, and call it from `browse()`:

```rust
fn browse(manual: &Manual, start: &str, query: &str) -> std::io::Result<()> {
	let _screen = Screen::open()?;
	let mut stack = vec![Level { address: start.into(), query: query.into(), selected: 0 }];
	if !is_branch(manual.find(start)) {
		if !view(manual, start, None)? {
			return Ok(());
		}
		stack[0].address = up(manual, start);
	}
	run(manual, &mut stack, key, draw_list)
}

fn run(
	manual: &Manual,
	stack: &mut Vec<Level>,
	mut next: impl FnMut() -> std::io::Result<Key>,
	mut render: impl FnMut(&Level, &[Row]) -> std::io::Result<()>,
) -> std::io::Result<()> {
	loop {
		let level = stack.last_mut().expect("the root level is never popped");
		let node = manual.find(&level.address).unwrap_or(Node::Root);
		let rows = rows(manual, node, &level.query);
		level.selected = level.selected.min(rows.len().saturating_sub(1));
		render(level, &rows)?;
		let pressed = next()?;
		if exits(&pressed, &level.query) {
			return Ok(());
		}
		match pressed {
			Key::Char(c) => { level.query.push(c); level.selected = 0; }
			Key::Erase if !level.query.is_empty() => { level.query.pop(); level.selected = 0; }
			Key::Back if !level.query.is_empty() => level.query.clear(),
			Key::Back | Key::Erase => {
				if stack.len() == 1 {
					if stack[0].address.is_empty() {
						return Ok(());
					}
					stack[0] = Level {
						address: up(manual, &stack[0].address),
						query: String::new(),
						selected: 0,
					};
				} else {
					stack.pop();
				}
			}
			Key::Up(n) => level.selected = level.selected.saturating_sub(n),
			Key::Down(n) => level.selected += n,
			Key::Open => {
				let Some(row) = rows.get(level.selected) else { continue; };
				if row.line.is_none() && is_branch(manual.find(&row.address)) {
					stack.push(Level { address: row.address.clone(), query: String::new(), selected: 0 });
				} else if !view(manual, &row.address, row.line)? {
					return Ok(());
				}
			}
			Key::Quit | Key::Exit | Key::Other => {}
		}
	}
}

fn exits(k: &Key, query: &str) -> bool {
	matches!(k, Key::Quit | Key::Exit) || matches!(k, Key::Char('q') if query.is_empty())
}
```

`Key::Back` (Left) is **untouched** — it keeps stepping up the address stack
exactly as at base, exiting only at the root with an empty address, exactly
as before this fix (round 1's N1). Only `Key::Quit` (Ctrl-C) and the new
`Key::Exit` (Esc) always end the list in one press, from any depth and any
filter state. A bare `q` ends the list only when the filter is empty; once a
query is underway `q` is ordinary filter text again, so nothing that could
be typed today becomes untypeable — to filter on a literal `q`, type any
other character first (a leading space is enough: `" q"` filters on the word
`q`, since the row filter splits the query on whitespace,
`src/cli/manual.rs:788`).

`render`/`next` are the seam: `browse()` passes the real `key()` and
`draw_list()`, both of which need a real terminal (`draw_list` and `view()`
call `crossterm::terminal::size()`, `src/cli/manual.rs:833,899`, which errors
without one); a test passes a scripted key sequence and a no-op renderer
instead, and drives the exact function `browse()` calls — not a copy of its
logic. This is round 1's accepted reading of box 3, replacing "a fake pty"
(`Screen::open`'s raw-mode/alternate-screen calls have no headless
equivalent to fake) with a scripted key source into the real loop.

Three static strings describe these keys and now name `q` (round 1's N2 —
`q` is the key box 1 depends on, and it was undiscoverable before):
`src/cli/manual.rs:341` (`cartridge help`'s no-terminal listing: "esc to go
back" → "esc quit, q quits an empty filter") and the list's live footer at
`src/cli/manual.rs:878` ("esc back · ctrl-c quit" → "esc/ctrl-c quit · q
quits empty filter"). `view()`'s footer (`src/cli/manual.rs:925`) is
unchanged — it was already accurate.

No separate test file: `src/cli/manual.rs` already carries
`#[cfg(test)] mod tests` (`src/cli/manual.rs:950` at base) exercising
`Manual`/`up`; both new tests below are plain `#[test]` fns added to that
module. Neither needs a terminal, a pty or any real IO — `run()`'s `next`/
`render` closures replace them — so no new file is needed and the footprint
stays one file.

```rust
#[test]
fn q_and_escape_exit_the_list_instead_of_being_consumed() {
	assert!(exits(&Key::Quit, ""), "ctrl-c always exits");
	assert!(exits(&Key::Exit, ""), "esc exits with no filter typed");
	assert!(exits(&Key::Exit, "shel"), "esc exits in one press even mid-filter");
	assert!(exits(&Key::Char('q'), ""), "bare q exits an empty filter");
	assert!(
		!exits(&Key::Char('q'), "shel"),
		"q stays literal filter text once a query is underway"
	);
	assert!(!exits(&Key::Char('x'), ""), "other characters are never consumed as exit");
}

fn run_keys(manual: &Manual, start: &str, keys: &[Key]) -> (std::io::Result<()>, String) {
	let mut stack = vec![Level { address: start.into(), query: String::new(), selected: 0 }];
	let mut it = keys.iter().copied();
	let result = run(manual, &mut stack, || Ok(it.next().unwrap_or(Key::Quit)), |_, _| Ok(()));
	let query = stack.last().expect("root level is never popped").query.clone();
	(result, query)
}

#[test]
fn scripted_keys_drive_the_real_list_loop() {
	let guide = "# Root\n\nintro\n";
	let manual = module(vec![Doc::new("docs/g.txt".into(), guide.into())]);

	let (result, query) = run_keys(&manual, "", &[Key::Char('q')]);
	assert!(result.is_ok());
	assert_eq!(query, "", "q must exit the root list before it is appended");

	let (result, query) = run_keys(&manual, "memo", &[Key::Char('q')]);
	assert!(result.is_ok());
	assert_eq!(query, "", "q must exit a pushed module level too");

	let (result, query) = run_keys(&manual, "", &[Key::Char('s'), Key::Char('q'), Key::Quit]);
	assert!(result.is_ok());
	assert_eq!(query, "sq", "q is consumed as filter text once a query is underway");

	let (result, query) = run_keys(&manual, "", &[Key::Char('s'), Key::Exit]);
	assert!(result.is_ok());
	assert_eq!(query, "s", "esc must exit before appending anything of its own");
}
```

`Key` needs `#[derive(Clone, Copy)]` for `keys.iter().copied()` above — a
one-line, behavior-free addition (every existing variant is already
`Copy`-safe: a `char` and a couple of `usize`s).

`scripted_keys_drive_the_real_list_loop` is what catches a loop that keeps
consuming `q`: it calls `run()` itself, the function `browse()` delegates
to, so a mutant that reorders the match (e.g. moves the `exits()` check to a
low-priority arm placed after `Key::Char(c) => level.query.push(c)`, so a
plain character always matches first) makes `q` get appended before `exits`
is ever consulted, and the first two assertions above go red — this is
exactly the reviewer's `mut2` from round 1, reproduced and confirmed below.

Probed in `git clone --local` copies (`base` = `beb8213` plus only the two
new tests, unmodified otherwise; `reference` = `base` plus the fix above;
`mutant` = `reference` with `exits()` demoted to a match arm ordered after
`Key::Char(c)`, reproducing round 1's `mut2`), isolated `CARGO_TARGET_DIR`,
`env -i PATH="$PATH" HOME="$HOME" sh -c`, cold build 11–14 s on this machine:

| Clone | `scripted_keys_drive_the_real_list_loop` |
| --- | --- |
| `base` | does not compile: `run`/`exits`/`Key::Exit` do not exist |
| `reference` | ok |
| `mutant` (`mut2`) | **FAILED** — `q must exit the root list before it is appended`, left: `"q"`, right: `""` |

`cargo build --bin cartridge` and the two pre-existing/new-but-unrelated
tests (`addresses_resolve_and_search_lands_in_the_section`,
`q_and_escape_exit_the_list_instead_of_being_consumed`) all stay green on
`reference`.

## Acceptance

- [x] A single `q` (with an empty filter) or a single `Esc` (any filter
      state) exits `cartridge help`'s list picker in one press, instead of
      being consumed as filter text or a partial level-up. `q` remains
      ordinary filter text once a query is non-empty; on the search path
      (`cartridge help <words>`), the filter starts non-empty, so only `Esc`
      exits in one press and `q` is literal from the first frame. `Left`
      keeps stepping up one level, exactly as today, and is not a quit key.
- [x] `scripted_keys_drive_the_real_list_loop` (`src/cli/manual.rs`) feeds
      key sequences through `run()` — the exact loop `browse()` calls, not a
      copy of it — and fails if the loop ever appends `q` to the filter
      instead of exiting on an empty one, or fails to exit on `Esc`.
- [x] `q_and_escape_exit_the_list_instead_of_being_consumed`
      (`src/cli/manual.rs`) pins `exits()`'s truth table directly, as a
      companion to the scripted-loop test above.

## Verify and Proof

<!--
How collect runs these blocks (engine facts, src/lifecycle.ts collect/verify):
- Each sh/bash/shell block runs as `sh -eu -c`, 120 s limit, empty stdin, the
  collector's environment.
- It runs twice: first with cwd = the lane, a worktree of the PRD's `repo` at
  `prd.ctg/.cartridge/boards/pty/.lanes/a-wedging-help-picker-must-not-hold-the-pty-node`;
  then, after the fast-forward, with cwd = `repo` itself. Paths are relative
  to the repo root.
- Pass 2 runs in the live checkout; the host hot-restarts a cartridge when its
  target/debug dylib changes, so the cargo block sets an isolated
  CARGO_TARGET_DIR under `target/<slug>-verify`.
- A block must not write inside the footprint.
-->

Block 1 — the behavioral gate, both new tests named exactly; a name change,
deletion, or a filter match on zero tests fails the block.
`scripted_keys_drive_the_real_list_loop` is the one round 1 required: it runs
the real `run()`, so the `mut2` reordering above turns it red. Cold build of
this crate measured 11–14 s in probing, well inside the 120 s limit; a warm
`target/<slug>-verify` (pass 2, same tree as pass 1 fast-forwarded) is
faster still.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/help-picker-verify}"
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
for t in q_and_escape_exit_the_list_instead_of_being_consumed scripted_keys_drive_the_real_list_loop; do
	cargo test --bin cartridge -- --exact "cli::manual::tests::$t" > "$log" 2>&1 || { cat "$log"; exit 1; }
	cat "$log"
	grep -q "^test cli::manual::tests::$t \.\.\. ok\$" "$log" || { echo "$t did not run"; exit 1; }
done
```

Block 2 — the mechanism is the one described: a distinct `Key::Exit` for
`Esc` (not a `Key::Back` remap that would also make `Left` quit), a single
`exits()` gate ahead of the match, and `Left`'s address-walk untouched. A
pure grep backstop; behavior is block 1's job.

```sh
grep -q 'Exit,' src/cli/manual.rs
grep -q 'KeyCode::Esc => Key::Exit,' src/cli/manual.rs
grep -q 'KeyCode::Left => Key::Back,' src/cli/manual.rs
grep -q 'fn exits(k: &Key, query: &str) -> bool' src/cli/manual.rs
grep -q 'Key::Quit | Key::Exit) || matches!(k, Key::Char(.q.) if query.is_empty' src/cli/manual.rs
grep -q 'Key::Back | Key::Erase | Key::Exit => return Ok(true)' src/cli/manual.rs
grep -q 'fn addresses_resolve_and_search_lands_in_the_section' src/cli/manual.rs
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/help-picker-verify}"
cargo build --bin cartridge > /dev/null
```

## Denied worlds

- Make `q` exit unconditionally (ignoring `level.query`): any query
  containing the letter `q` becomes untypeable past that character, and
  `scripted_keys_drive_the_real_list_loop`'s third case
  (`query == "sq"`) fails.
- Reorder the match so `Key::Char(c)` is checked before `exits()` (round 1's
  `mut2`, reproduced above): `q` is appended instead of exiting, and
  `scripted_keys_drive_the_real_list_loop`'s first two cases go red exactly
  as shown in the probe table.
- Remap `Esc` to the existing `Key::Back` instead of a new `Key::Exit`:
  `Left` would then also quit the whole picker in one press, contradicting
  the untouched-`Left` Acceptance line; block 2's `KeyCode::Esc => Key::Exit`
  grep also fails.
- Only test the pure `exits()` function (round 1's original mistake): a
  mutant that never wires `exits()` into `run()`'s early-return, or wires it
  after `Key::Char(c)`, still passes such a test, because the function is
  correct in isolation — which is exactly why
  `scripted_keys_drive_the_real_list_loop` now exists.
- Claim the concurrent-read box here: it moved to
  `@pty/a-shell-read-answers-while-a-foreground-program-holds-the-pty` and is
  out of this spec's footprint and repo.
