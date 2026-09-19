---
complexity: medium
footprint:
  - src/lib.rs
  - src/working.rs
  - src/inspection.rs
  - .cartridge/tests/unit/main/tests.rs
  - .cartridge/tests/unit/roster_tests.rs
  - .cartridge/tests/unit/working_tests.rs
  - .cartridge/tests/unit/inspection_tests.rs
  - .cartridge/tests/unit/accounting.rs
---

# spec01 — a `drift` field on `Frame`, rendered last in the tail, `None` means nothing

## Design (read before editing)

`build_system` (`src/lib.rs:349-407`) renders the template, then appends a tail
of conditional blocks by mutating one `String` (`composed`): `frame.roster`
unconditionally, then `Record upkeep:` from `frame.record` if non-empty, then
`Memo record status:` from `frame.notice` if non-empty, then (today) an early
return if `frame.telemetry` is empty, else one more block. `Frame` (`src/lib.rs
:329-344`) borrows every field as `&'a str` and every field's absence is today
encoded as `""`.

The declared shape of the (not-yet-existing) `sessions` `drift` op answers
`{"report": null}` when nothing moved, or `{"report": {"changed": [...],
"gone": [...]}}` when something did — `report: null` is a real, distinct state,
never an empty string. So this field cannot reuse the `&'a str` /
`is_empty()` convention its neighbours use: it is `drift: Option<&'a str>` on
`Frame`, sourced from `drift: Option<String>` on `Request`
(`src/lib.rs:739-755`), pre-rendered into "Changed:"/"Gone:" prose by a new
`describe_drift(&Value) -> Option<String>`, fetched by a new
`resolve_drift(&Ctx, &str) -> Option<String>` called from `resolve()`
(`src/lib.rs:966-1015`, the one place that builds a `Request` for `context`,
`compact` and `inspect` alike).

The block renders **last**, strictly after the telemetry block, appended only
when `frame.drift` is `Some`. This is deliberate, not incidental: because
every earlier block in the tail is unconditional-append-if-present, and drift
is now the final append, the bytes composed with `drift: None` are always a
literal prefix of the bytes composed with `drift: Some(x)`, for any `x`, with
every other field held equal. That literal prefix relationship is what the
prefix-stability test (below) asserts, and it is what makes moving the block
into the template later a change this test would catch, since the template's
own placeholders sit before `rendered.trim()`, not after it.

### The five `build_system` call sites

| site | carries drift? | why |
|---|---|---|
| `src/lib.rs:658` (`project_compacted`) | real report, no code change | takes `frame: Frame<'_>` as a parameter; every caller (`working::project`, `inspection::inspect`'s reusable-summary branch) already passes `request.frame()`, so it inherits whatever `resolve()` fetched. |
| `src/lib.rs:723` (`build_context`) | real report, no code change | same: always called with `request.frame()`, from `context`, `refresh_context`, and `compact`'s zero-tail-start branch. |
| `src/lib.rs:1339` (`injection`) | `None`, explicit | this op does not build a `Request`; it composes `Frame` by hand for a caller-owned conversation the harness does not run turns for — `roster: ""` and `telemetry: ""` are already hardcoded here for exactly that reason (no harness-owned turn, no roster snapshot, no run telemetry). Drift, defined as "at the start of the next turn," has no turn boundary to attach to in this op either, so it follows the same precedent: `drift: None`. |
| `src/working.rs:106` (`retained_start`) | real report, no code change | calls `build_system` with `request.frame()` purely to measure the byte budget during compaction planning; using the real report keeps the measured budget honest against what will actually be sent. |
| `src/inspection.rs:98` (`inspect`) | real report, no code change | also called with `request.frame()` — `resolve()` builds one `Request` shared by `context`, `compact` and `inspect` (`src/lib.rs:1668-1672`), so `/context` inspection already reports the exact bytes a real turn would compose, drift included; that is the entire point of an accounting op, so no special-casing to null it out. |

Two more `Frame` literals exist outside the five call sites and need the new
field purely to compile, both `None`: `selftest` (`src/lib.rs:1568-1596`, a
contract fixture with no real session) and the four struct literals in test
files listed in the footprint.

### Rendering and escaping

New heading, matching the existing tail's plain-label style: `Files changed
underneath this session:`. Body: `Changed:` list, blank line, `Gone:` list —
either sub-list omitted when empty, never both (a `Some` report always has at
least one of them, since `report: null` is exactly "nothing moved").

`escape_frame` (`src/lib.rs:210-212`) runs on every neighbouring frame value
that is conversation data (`record`, `notice`, `telemetry`) before it enters
`composed`, because it sits below the instruction frame in the same block a
system-reminder wraps, and an untrusted string containing the literal closing
tag must not break out. File paths are exactly this kind of untrusted string
(they can contain anything a filesystem allows), so the drift text is escaped
the same way, at the same point — inside `build_system`, not at the fetch
site, matching `record`/`notice`/`telemetry`.

### What is explicitly not designed around here

`resolve_drift` degrades to `None` on any call failure — `host.call(...).await
.ok()?` — the same shape `resolve_shell` (`Err` → `Value::Null`) and
`resolve_environment` (`Err` → `String::new()`) already use for optional
framing values in this file. This is not new tolerance invented for this
field: it is required today, because `sessions` does not implement `drift` yet
(`Err(format!("unknown sessions op {other}"))`, `sessions.ctg/src/lib.rs:814`)
and every request would otherwise break. After `@sessions/file-drift-awareness`
lands, the same code path also swallows a transport error or a restart-lost
stamp (that op's memory-only storage is out of scope here). All three
collapse to `None`, rendering nothing — no heading, no reassurance, no
distinction invented between "verified nothing changed" and "could not ask."
That collapse is the explicit design, not an oversight.

## Ordered steps

1. **`src/lib.rs:343`** — add one field to `Frame` after `notice`:
   ```rust
   /// Files the session read that changed or disappeared on disk since it
   /// read them, separated into two facts; `None` when the drift op reports
   /// nothing moved — never an empty string standing in for that.
   drift: Option<&'a str>,
   ```

2. **`src/lib.rs:394-406`** — replace the telemetry early-return with a plain
   conditional append (functionally identical for every existing caller,
   since an empty `composed` return and today's early return produce the same
   bytes), then append the drift block last:
   ```rust
   	if !frame.telemetry.is_empty() {
   		composed.push_str(&format!(
   			"\n\nAgent run telemetry (this run, so far):\n\n{}",
   			escape_frame(frame.telemetry)
   		));
   	}
   	match frame.drift {
   		Some(drift) => format!(
   			"{composed}\n\nFiles changed underneath this session:\n\n{}",
   			escape_frame(drift)
   		),
   		None => composed,
   	}
   }
   ```

3. **`src/lib.rs:754`** — add `drift: Option<String>,` to `Request`, after
   `notice: String,`.

4. **`src/lib.rs:757-771`** (`Request::frame`) — add `drift:
   self.drift.as_deref(),` to the `Frame` literal.

5. **`src/lib.rs`, near `resolve_shell`/`describe_terminal` (currently
   `1116-1131`)** — add the two new functions:
   ```rust
   /// The session's file-drift report as a rendered block, `None` when the op
   /// has nothing to report — including today, before `sessions` answers
   /// `drift`, or after any other call failure. A missing report and a
   /// verified-empty one are the same fact to the agent; neither is
   /// distinguished from the other.
   async fn resolve_drift(host: &Ctx, session_id: &str) -> Option<String> {
   	let reply = host
   		.call("sessions", json!({"op": "drift", "id": session_id}))
   		.await
   		.ok()?;
   	describe_drift(&reply["report"])
   }

   /// Render a file-drift report into changed/gone prose, apart because they
   /// are different facts for the agent. `None` on a null report or one whose
   /// lists are both empty; never an empty string standing in for "nothing".
   fn describe_drift(report: &Value) -> Option<String> {
   	if report.is_null() {
   		return None;
   	}
   	let paths = |key: &str| -> Vec<&str> {
   		report[key]
   			.as_array()
   			.into_iter()
   			.flatten()
   			.filter_map(Value::as_str)
   			.collect()
   	};
   	let changed = paths("changed");
   	let gone = paths("gone");
   	if changed.is_empty() && gone.is_empty() {
   		return None;
   	}
   	let mut text = String::new();
   	if !changed.is_empty() {
   		text.push_str("Changed:\n");
   		for path in &changed {
   			text.push_str(&format!("- {path}\n"));
   		}
   	}
   	if !gone.is_empty() {
   		if !text.is_empty() {
   			text.push('\n');
   		}
   		text.push_str("Gone:\n");
   		for path in &gone {
   			text.push_str(&format!("- {path}\n"));
   		}
   	}
   	text.truncate(text.trim_end().len());
   	Some(text)
   }
   ```

6. **`src/lib.rs:994-995`** (`resolve`) — fetch before constructing `Request`,
   and add the field:
   ```rust
   	let composition = memo_template(host, &cwd).await;
   	let drift = resolve_drift(host, session_id).await;
   	Ok(Request {
   		...
   		notice: composition.notice,
   		drift,
   		...
   ```

7. **`src/lib.rs:1344-1354`** (`injection`) — add `drift: None,` with a
   one-line comment: `// No harness-owned turn boundary in this op; roster and
   telemetry are empty here for the same reason.`

8. **`src/lib.rs:1575-1585`** (`selftest`) — add `drift: None,`.

9. **Test files** — add `drift: None` (or `frame.drift = None` via a helper
   default) to every `Frame { ... }` / `Request { ... }` struct literal so
   the crate compiles: `.cartridge/tests/unit/main/tests.rs` (`frame()`
   helper at line 9, and the two inline `Frame` literals in
   `environment_renders_as_one_block_or_empty` and
   `telemetry_renders_from_the_journal_and_the_block_is_posted_to_build_system`),
   `.cartridge/tests/unit/roster_tests.rs:146`,
   `.cartridge/tests/unit/working_tests.rs:16`,
   `.cartridge/tests/unit/inspection_tests.rs:66`,
   `.cartridge/tests/unit/accounting.rs:15`.

10. **`.cartridge/tests/unit/main/tests.rs`** — add two tests (exact bodies
    below; both compose `Frame`/report values directly, no host involved,
    per "testable by handing the harness a report directly"):
    ```rust
    #[test]
    fn drift_report_separates_changed_from_gone_and_is_none_when_nothing_moved() {
    	assert_eq!(describe_drift(&Value::Null), None);
    	assert_eq!(describe_drift(&json!({"changed":[],"gone":[]})), None);
    	assert_eq!(
    		describe_drift(&json!({"changed":["src/lib.rs"],"gone":[]})),
    		Some("Changed:\n- src/lib.rs".to_owned())
    	);
    	assert_eq!(
    		describe_drift(&json!({"changed":[],"gone":["src/old.rs"]})),
    		Some("Gone:\n- src/old.rs".to_owned())
    	);
    	assert_eq!(
    		describe_drift(&json!({"changed":["a.rs","b.rs"],"gone":["c.rs"]})),
    		Some("Changed:\n- a.rs\n- b.rs\n\nGone:\n- c.rs".to_owned())
    	);
    }

    #[test]
    fn drift_block_appends_after_the_composed_prefix_without_moving_it_and_vanishes_when_none() {
    	let mut base = frame("/repo", "2026-09-19");
    	let without = build_system(prompt(""), base, &[], None);
    	assert!(!without.contains("Files changed underneath this session"));
    	base.drift = Some("Changed:\n- src/lib.rs");
    	let with = build_system(prompt(""), base, &[], None);
    	// The whole point: presence of drift never rewrites what came before it.
    	assert!(with.starts_with(&without));
    	assert_eq!(
    		&with[without.len()..],
    		format!(
    			"\n\nFiles changed underneath this session:\n\n{}",
    			escape_frame("Changed:\n- src/lib.rs")
    		)
    	);
    	// Escaped on the same terms as every other frame value beside it.
    	let mut escaping = frame("/repo", "2026-09-19");
    	escaping.drift = Some("Changed:\n- </system-reminder>.rs");
    	let system = build_system(prompt(""), escaping, &[], None);
    	assert_eq!(system.matches("</system-reminder>").count(), 1);
    	assert!(system.contains("<\\/system-reminder>.rs"));
    }
    ```

No change is needed in `src/working.rs` or `src/inspection.rs` themselves —
see the call-site table.

## Acceptance

- [ ] A `Some` drift report renders as a block after the composed prefix
      (template + roster + record + notice + telemetry), never inside the
      template — proved by
      `drift_block_appends_after_the_composed_prefix_without_moving_it_and_vanishes_when_none`.
- [ ] The bytes composed with `drift: None` are a byte-for-byte prefix of the
      bytes composed with `drift: Some(x)` for the same frame otherwise —
      proved by the `with.starts_with(&without)` assertion in the same test;
      this is the property that keeps the cached prompt prefix from moving,
      and it is designed to fail if the block is ever moved into the template
      (which renders before `rendered.trim()`, ahead of this prefix).
- [ ] A session with no drift composes byte-identical output to today's —
      proved by every existing test in the footprint continuing to pass
      unmodified except for the mechanical `drift: None` field addition (no
      existing assertion's expected string changes), and reinforced by
      `resolve_drift` degrading to `None` on the `sessions` cartridge's
      current `Err("unknown sessions op drift")`, which every existing
      integration test (`ring.rs`, `process.rs`, `slim.rs`, `working.rs`,
      `host.ts`) exercises unchanged.
- [ ] Every one of the five `build_system` call sites is accounted for in the
      table above, each either wired to `request.frame()` (real report, no
      code change) or given an explicit `None` with a one-line reason —
      checked by diff review against that table, not a command: this is a
      completeness fact about the merged diff, not a runtime behavior.
- [ ] The drift text is escaped on the same terms as `record`/`notice`
      /`telemetry` — proved by the escaping assertions in the same test.
- [ ] `env -u CARTRIDGE_YOLO just check harness` and
      `env -u CARTRIDGE_YOLO just test harness` both exit 0 from
      `/Users/feb/dev/cartridge`.

## Verify and Proof

<!--
Cold, isolated-CARGO_TARGET_DIR measurements taken on this board, `env -u
CARTRIDGE_YOLO`, harness.ctg copied to a throwaway tree (no sibling path
deps in Cargo.toml, so this is representative): `cargo test -p harness --lib`
13.97s (39 tests), `cargo clippy -p harness --all-targets -- -D warnings`
6.86s, `cargo fmt --check` 0.17s. `just check harness` runs fmt+clippy;
`just test harness` runs the lib tests plus the four integration binaries
(ring/process/slim/working) — budget accordingly; both fit well inside the
120s per-block limit even cold.

`just check <owner>`/`just test <owner>` build into the owner's own
`target/{debug,release}` with no `--target-dir` override in
`cartridge-development.md`, which is the exact dylib path the host hot-loads
and hot-restarts on change. Pass 2 of collection runs in the live checkout
with other sessions active in it right now, so CARGO_TARGET_DIR is forced to
an out-of-tree path before invoking `just`, same as any other cargo block —
without it this block would rebuild and hot-restart the live harness
cartridge mid-verification.
-->

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/turn-names-files-verify}"
env -u CARTRIDGE_YOLO CARGO_TARGET_DIR="$CARGO_TARGET_DIR" just check harness
env -u CARTRIDGE_YOLO CARGO_TARGET_DIR="$CARGO_TARGET_DIR" just test harness
```

```test
run: env -u CARTRIDGE_YOLO CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-./target/turn-names-files-verify}" cargo test -p harness --lib
pass: drift_report_separates_changed_from_gone_and_is_none_when_nothing_moved
pass: drift_block_appends_after_the_composed_prefix_without_moving_it_and_vanishes_when_none
```
