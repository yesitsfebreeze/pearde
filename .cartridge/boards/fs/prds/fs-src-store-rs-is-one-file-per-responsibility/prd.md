---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/fs.ctg"
work-kind: leaf
footprint:
  - "src/store.rs"
  - "src/git.rs"
  - "src/query.rs"
  - "src/write.rs"
  - "src/materialize.rs"
  - "src/review.rs"
  - "src/remote.rs"
  - "src/ledger.rs"
  - ".cartridge/tests/unit/store/tests.rs"
---

# fs src/store.rs is one file per responsibility

## Outcome

`fs.ctg/src/store.rs` is 1382 lines (`wc -l fs.ctg/src/store.rs`, verified
2026-09-19) and one `impl Store` block answers for at least seven distinct
git-plumbing jobs. Two `.unwrap()` calls sit in that same file
(`store.rs:975` inside `repository_identity`'s digest, `store.rs:1089` inside
`commit_path_captured`'s stdin write) and become handled errors instead.
Serves ranking row 2 of `.cartridge/memos/ranking/cartridges.md` (fs:
"`src/store.rs:1089` unwrap; `src/store.rs` 1383 lines; README and help.md
duplicated" — the README/help gap is filed separately, see below).

## Responsibilities found in `store.rs`, with target files

1. **Git process wrapper and refs** — `IDENT_NAME`/`IDENT_EMAIL`,
   `IndexLock`, `MutationLock`, `git_cmd`, `run`, `run_tolerant`, `lossy`,
   `mutation_lock`, `index_file`, `branch`, `git`, `git_str`, `shared_index`,
   `repository_identity` (both `cfg` variants) (`store.rs:48-233,
   950-982`). Target: `src/git.rs`.
2. **Read-only queries** — `tip`, `head`, `branch_name`, `blob_for`, `read`,
   `merge_base`, `owned_paths`, `session_change`, `session_commits`,
   `is_ancestor`, `tree_diff`, `head_is_ship` (`store.rs:236-371,
   916-930, 1185-1192`). Target: `src/query.rs`.
3. **Git object writes** — `rollback_captured`, `tree_of`, `hash_object`,
   `apply`, `commit_tree`, `update_branch`, `write_blob`,
   `write_blob_captured`, `commit_path_captured` (`store.rs:378-647`).
   Target: `src/write.rs`. `commit_path_captured`'s unwrap (today
   `store.rs:1089`, `child.stdin.take().unwrap()`) moves here and is fixed
   here. The other current unwrap, inside `repository_identity`'s digest
   (today `store.rs:975`), moves to `src/git.rs` with responsibility 1 above
   and is fixed there.
4. **Working-tree materialization** — `materialize`, `materialize_captured`
   (`store.rs:653-872`, ~220 lines on its own). Target: `src/materialize.rs`.
5. **Review/ship construction** — `preview_ship`, `preview_ship_locked`,
   `commit_ship`, `reviewed_tree_locked`, `reviewed_tree`, `reviewed_diff`,
   `commit_reviewed` (`store.rs:880-912, 935-948, 984-1182`). Target:
   `src/review.rs`.
6. **Remote sync** — `push`, `undo` (`store.rs:1199-1266`). Target:
   `src/remote.rs`.
7. **Ledger/mtime bookkeeping** — `LedgerEntry`, `tip_time`, `path_time`,
   `write_disk`, `load_ledger`, `save_ledger`, `seconds_end_ms`, `now_ms`,
   `fs_mtime`, `literal`, `var_str`, `parse_name_status`
   (`store.rs:1271-1378`). Target: `src/ledger.rs`.

`store.rs` retains: `Store`/`StoreConfig`/`ReviewedTree`/`Materialize` type
definitions, `directory`, `new`, `at`, `at_readonly`, `root`, `to_value`,
`trimmed_opt`, `printable`, `publication_failure` (`store.rs:20-131,
214-221`) — construction and the shared types every other file's `impl
Store` block needs.

This is the found grouping, not a mandate on exact boundaries: two adjacent
tiny files may merge during implementation if they are genuinely
inseparable, but no file may mix two of the seven jobs above, and none may
exceed the acceptance bound below.

## Acceptance

- [ ] `wc -l fs.ctg/src/store.rs` reports 350 lines or fewer.
- [ ] `wc -l fs.ctg/src/{git,query,write,materialize,review,remote,ledger}.rs`
      reports no file over 350 lines.
- [ ] `rg -c '\.unwrap\(\)' fs.ctg/src/store.rs fs.ctg/src/git.rs
      fs.ctg/src/write.rs` (and any other split file) sums to 0; both
      current unwraps return `Result::Err` via `.ok_or_else(...)?` or
      `.map_err(...)?` instead of panicking on a missing stdin handle or a
      JSON-serialization failure.
- [ ] `just test fs` passes, naming `fs.ctg/.cartridge/tests/unit/store/tests.rs`
      explicitly as still green against the split files.
- [ ] `just check fs`, `just audit fs` and `just isolation` report nothing
      for fs.

## Proof and recovery

Starting file: `fs.ctg/src/store.rs`. No fixture needs creating —
`.cartridge/tests/unit/store/tests.rs` already exercises `Store` through its
public methods and does not reach into module-private layout, so it should
compile unchanged against the split as long as every `pub`/`pub(crate)`
signature named above is preserved.

Before touching code, capture the baseline:
`wc -l fs.ctg/src/store.rs` and `rg -n '\.unwrap\(\)' fs.ctg/src/store.rs`,
both from `/Users/feb/dev/cartridge`, so the acceptance boxes measure a real
move rather than restating today's numbers.

Gates, cwd `/Users/feb/dev/cartridge`: `just check fs`, `just test fs`,
`just audit fs`, `just isolation`. Compatible fallback: every function this
PRD names keeps its exact signature and visibility, so no caller in
`service.rs`, `overlay.rs`, `push.rs`, `ship.rs` or elsewhere in `fs.ctg`
observes a change; this is an internal file reorganization plus two error
handling fixes, not a behavior change.

## Dependencies and review

No live PRD on the fs board touches `store.rs` today: `rg -l "store\.rs"
prd.ctg/.cartridge/boards/fs/prds/*/prd.md` names only
`@fs/the-fs-cartridge-ships-the-readme-its-audit-demands`, which is `done`
and scoped to `README.md` only (it quotes `store.rs`'s line count as
evidence, it does not touch the file). No `needs` is set.

The README/help.md duplication the same ranking row names is a different
footprint (`README.md`, `.cartridge/help.md`, no `src/**`) and an
independent outcome from splitting `store.rs`, so it is filed as its own
leaf, `@fs/fs-readme-and-help-md-share-one-source`, rather than folded in
here.
