---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
actual: "1h"
---

# Report unreadable embedding metadata as an explicit unknown or error state instead of a false compatible state.

## Do

Change embedding-stamp decoding and health projection in `src/store_core/src/lib.rs` and its callers so missing, readable-compatible, readable-mismatched, and unreadable metadata are distinct. Preserve the unreadable bytes for diagnosis and repair, throttle repeated logs, and report the decode error without treating unknown compatibility as `embed_mismatch: false`. Keep destructive migration or production-store repair in [finish-the-store-the-doctor-found](../finish-the-store-the-doctor-found/prd.md), not this item.

**Landed 2026-09-09, two commits on `main`.** `Store::embed_stamp()` answered
`Option<EmbedStamp>` through `.ok().flatten()`, so a stamp nobody could decode
and a store nobody had stamped were the same answer; `EmbedRead` (`Missing`,
`Stamped`, `Unreadable(String)`) splits them, and the unreadable arm carries a
bounded diagnostic — the decode error, the row's length, and its first eight
bytes as hex, which is where the format version sits and so what tells a
foreign row from a truncated one. The bytes stay on disk: `check_embed_stamp`
still returns `Err` before any write, and its error line is now throttled by its
own `LogThrottle` like the mismatch line beside it, because the check runs on
every flush and the guarded save retries five times.

Downstream, `HealthStats` gains `embed_unreadable: String` — non-empty means
`embed_mismatch: false` says "nothing could be compared", not "compatible" —
and `HealthRes` gains the same field append-only under `serde(default)`, the
pattern `build_stamp` set an hour earlier. `embed_line` comes out of
`cmd_health` beside the `*_health_lines` helpers so all four states are
assertable without a daemon; the unreadable one prints `(unreadable) … UNKNOWN`
with the diagnostic, never `(unstamped)`. `memory doctor` raises `embed_unreadable`
as an `error` before the mismatch check — the stronger claim first, since
`embed_mismatch` is false there for want of a comparison rather than for want of
a fault.

## Acceptance
Tests construct each embedding metadata state and assert its health representation. A corrupt version stamp reports `unknown` or `unreadable` plus a bounded diagnostic, never the empty-model and no-mismatch combination. Existing compatible and mismatch behavior remains green.

**Green 2026-09-09.** `store_core::an_unreadable_stamp_is_neither_missing_nor_a_match`
writes `ff0102` under the stamp key and asserts the read is `Unreadable`, that
the diagnostic names the length and the head and stays under 200 characters,
that `check_embed_stamp` errs rather than adopting or matching, that the bytes
survive it, and that a restamp repairs the state.
`commands::the_embed_line_keeps_an_unreadable_stamp_apart_from_an_unstamped_store`
asserts all four health representations and that the fourth is neither of the
clean two. `just check` clean; `cargo nextest run --workspace --no-fail-fast`
1469 of 1470, the one red `memory::cited_paths`, owned by
[the-plan-crate-cites-an-untracked-file](../the-plan-crate-cites-an-untracked-file/prd.md) and red in every lane.
