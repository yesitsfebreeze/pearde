---
complexity: 12
footprint:
  - resources/board/plan.py
  - .pearde/.state
---

# spec01 — the parse cache stands in plan.py, wired through `scan`

The cache exists inside `resources/board/plan.py`: `parse_prd` serves
`(fm, title, body)` from a module dict keyed on abspath + mtime_ns + size and
parses only on a miss; `scan` loads it from `<board>/.state/parse-cache.json`
before walking and saves merged entries back after, only when a miss happened.
A served `fm` is a fresh dict with fresh lists, so `transitions.py` and
`collect.py` mutating `fm["state"]` cannot poison the cache. Anything short of
a clean current-version file (missing, corrupt, unreadable, `version` ≠
`CACHE_VERSION`) reads as an empty cache silently and never fails a call.

## Already standing

A previous analyst's pass-one probe and this pass-two attempt left the
mechanism working and verified in the tree (uncommitted, `prds/scan-parses-…/
probe/`): `parsecache.py` (the mechanism, proved standalone), `bench.py` (cold
16.3 ms / warm 4.5 ms over 229 files), `attempt.py` (the wiring simulated:
cmd_scan warm 29-39 ms against ~66 ms cold), and `verify.sh` (the contract
checks below, passing). In `plan.py` itself the cache is implemented and
wired: `parse_cache_load`, `parse_cache_save`, `parse_prd` (cached) and
`_parse_prd_uncached`, with `scan()` loading before the walk and saving after,
gated on a dirty flag so an all-hit call never writes. The real board's
`scan` runs 60-80 ms warm, down from ~70 ms cold measured the same way; the
PRD's 142-173 ms headline was not reproducible on 2026-09-01 (see report,
Finding 1).

## Acceptance

- [x] `parse_prd` on a warm cache does not open the file: a second call in one
      process over an unchanged board performs zero `open` calls on those
      paths, and the returned `fm` is a fresh dict (mutating it, as
      `transitions.py` does to `fm["state"]`, does not change what the next
      call returns) — warm call: 0 opens, mutation isolated: True
- [x] an edit made outside pearde — a rewritten `prd.md` with a new mtime and
      size — is served with its new frontmatter and title on the next call,
      with exactly one re-parse — mtime change: re-opens 1, same content served
- [x] a cache file holding invalid JSON, a wrong `version`, or a non-dict
      `files` is discarded silently: the next `scan` succeeds with correct
      output and exit 0 — all three on the real board: exit 0, 81 PRDs
- [x] a PRD directory deleted between two calls is not served from the cache:
      the next scan's PRD count reflects the deletion, and the saved cache no
      longer holds the deleted path's entry — fixture 81→80, entry dropped on
      the next miss-triggered save (an all-hit save never fires; see report)
- [x] `scan` saves the cache only when a miss happened since the last save —
      an unchanged board does not rewrite `parse-cache.json` — unchanged
      board: cache mtime unchanged across a scan
- [x] cold and warm `scan` over an unchanged board print byte-identical output
      — `diff` cold.out/warm.out on the fixture: identical

## Verify and Proof

```sh
python3 resources/board/plan.py scan | head -3
bash .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
```