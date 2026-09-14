# The socket name is stable and the file is private — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/the-socket-name-is-stable-and-the-file-is-private` (`prd.md`).
Scope: one leaf. Socket names are stable across toolchains, and socket files are owner-only.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **DELIVERED** (pending verification).

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `9a1c3069403bb5bdf9b61b0d5e666520990a4056dfabe33298ae3ef0e28a04e0` (frontmatter only; prior text `932486465ab822f4c529446b9e052e6254b7a253ff10886c578d442b0446a06d`).
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

Evidence, identical on both lines:

- **Name.** `src/socket.rs` with `DefaultHasher` was deleted by `939e7d1`. Names come from `transport::typed::path_tag`, an FNV-1a hash over the canonical path, so they are stable across processes and toolchains (`typed.rs:388-411`). `host/socket.rs::tag` takes 12 hex characters. Tests `path_tag_is_stable_and_nonempty` and `for_root_includes_the_tag` are in `src/transport/tests/typed.rs:153-213`. The PRD asked for SHA-256; FNV-1a meets the stated goal of stability across toolchains, though it is not collision-resistant.
- **Mode.** `transport::typed` binds and then sets `0o600` (`typed.rs:612`). `bind_unix.rs:28,45` assert the mode. Token files are written `create_new` with mode `0o600` (`host/socket.rs:167-180`).
- **Directory.** `host/socket.rs::base` (`:30-57`) creates `$XDG_RUNTIME_DIR/cartridge` or `/tmp/cartridge-<uid>` with mode `0o700`. It refuses a directory that is not owned by the uid and tightens any group or other bits. This closes the privacy gap of a shared macOS `/tmp` without moving the path.
- **`sun_path`.** The limit is named `SUN_LEN_MAX` (`typed.rs:332`). `base()` falls back when the XDG path is 48 bytes or longer.
- **Sweep.** The `sweep` race was removed with its code. `run_dir` removes only directories whose owning pid is dead (`kill(pid, 0)`), and `bind_unix.rs:73,102` assert that a refused bind does not unlink.

Residual gaps, not blocking:
- There is no fixed-input exact-name test.
- Removing a run directory checks the pid but not an inode swap.

Result: no score (verdict round). Status: `delivered-pending-verification`.
Unresolved blocking findings: none.
Validation (read-only):
- `rg 'DefaultHasher|0o600|0o700|sun_path|XDG_RUNTIME_DIR|path_tag'` on both lines;
- reads of `src/host/socket.rs:25-180` and `src/transport/typed.rs:325-411`;
- `shasum -a 256`.

Tests were not run.
Rounds used / remaining: 2 / 3.
Next action: collect after `just test runtime` passes.
