---
complexity: medium
footprint:
  - src/main.rs
  - src/context.rs
  - src/search.rs
  - src/service.rs
  - .cartridge/tests/unit/search/tests.rs
  - .cartridge/docs/search-pages.md
---

# spec01 — Page a bounded captured search result

Retain existing typed chains and run/cwd-scoped refs. A ref names the full
captured result, so later narrowing never silently loses the omitted tail.
Add search cursor input, snapshot revision, total count, consistency metadata
and next_cursor. Validate a versioned cursor against service lifetime, session,
run, cwd, ref, offset and captured content; reject invalid, foreign and retired
cursors. Replaying a valid cursor is idempotent. Every page obeys item and JSON
item-array byte caps; an indivisible oversized item fails explicitly.

Execute stages over bounded full input before paging. Distinguish an empty
intermediate set from an initial workspace sweep; accept documented files_of
and its legacy filesof spelling. Remove the hidden 200-match-per-file cap.
Use NUL-delimited path enumeration and preserve line-addressed match identity.

Bound stdout and stderr while reading, and keep both drains plus child wait
under cancellation/deadline control. Excess output fails with an actionable
capacity error after killing/reaping the child. Bound aggregate retained snapshot
bytes per service and count via existing chain caps; free retired run snapshots.
Do not evict a cursor silently. Mutations remain outside this change.

## Acceptance

- [x] More than a thousand real paths, including a newline filename, paginate once each with bounded pages; more than 200 matches in one file survive. Exact-cap results report complete.
- [x] Snapshot replay is stable after tree changes and reports captured consistency explicitly; fresh searches see changes. Invalid, foreign, retired and cancelled cursors fail explicitly.
- [x] Empty intermediate stages never re-enumerate; refs address the complete captured result; output floods, oversized items and storage exhaustion are explicit failures with bounded process lifetime.
- [x] Public fs tests/check pass, including guarded mutations and partial_success compatibility.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test fs
```

Run `just check fs` through the same public runtime entry point. Query-time
changes may produce a mixed-time scan; this is documented, never called an
atomic filesystem snapshot. New queries are the explicit refresh operation.

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just check fs
```
