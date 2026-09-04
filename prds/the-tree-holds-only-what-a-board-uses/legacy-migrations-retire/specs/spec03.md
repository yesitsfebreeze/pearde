---
complexity: 11
footprint:
  - resources/board/shared.py
  - resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh
---

# spec03 — the store fold moves to the door it belongs at

`shared.RETIRED` folds a store copy at `.pearde/graphify/cache` into
`pearde/graphify/cache`, and `shared.apply()` runs it on every `pearde share
apply`. It is a 2026-09-02 one-shot: measured today only one repo store on this
machine still holds the retired key (`/Users/feb/dev/infra/mitosys/.git/pearde-shared/.pearde/`,
beside its survivor), so the fold is not spent and cannot simply be deleted —
it moves to `pearde upgrade`, which spec02 makes runnable.

The table and `retire()` leave `shared.py` for `resources/board/init.py`, where
`cmd_upgrade` calls the fold as one more step row. `shared.py` keeps
`merge_into` and `store_of`, which the fold uses and which are not migration
code. `state()`'s `stale` verdict stays — it names any link onto another key of
the same store and does not depend on the table; only its docstring's `RETIRED`
mention has to be reworded. The invariant's fourth check reads the table from
its new home.

**Nothing of this is built.** Pass one scoped it and proved the fold is still
needed; the move itself is left.

## Acceptance

- [x] `RETIRED` and `retire(` appear nowhere in `resources/board/shared.py`, including its docstrings. — `grep -n 'RETIRED\|def retire' resources/board/shared.py` → no match.
- [x] `shared.apply()` runs no fold and returns the per-tree rows only. — `out = []` ahead of the per-tree loop; the fold lives in `init.retire`, called from `cmd_upgrade`.
- [x] `cmd_upgrade` prints one step row for the fold, naming what it folded or that there was nothing to fold, and exits 0 on a board whose store has no retired key. — second run printed `store  nothing to fold — no retired key in the store`, rc=0.
- [x] Given a store holding both keys with a file only under the retired one, one `pearde upgrade` leaves one key, the survivor holds that file, and a second run reports nothing to do. — planted `probe` under `.pearde/graphify/cache` in `/Users/feb/dev/infra/pearde/.git/pearde-shared`; `upgrade .` printed `store  folded into pearde/graphify/cache — 1 entry(ies) kept`, `.pearde/` gone, `probe` in the survivor; next run reported nothing to fold.
- [x] `one-copy-per-machine-of-what-every-lane-regenerates.sh` reads the table from its new home and passes; its fourth check still fails when a retired key is planted in the store. — planted: `FAIL the store holds .pearde/graphify/cache beside pearde/graphify/cache — one object, two copies`; after the fold that line is gone. The script's other FAIL (`.pearde/graphify/cache is a real copy in 2 trees at once` — two neighbour lanes) reproduces identically from the untouched main checkout: pre-existing, outside this footprint.
- [x] `pearde share apply --dry` and `pearde share` still exit 0 and list every tree. — `share --dry` rc=0 (493 shared rows surveyed), `share` rc=0, 627/627 rows.

## Verify and Proof

```sh
cd "$REPO"
if grep -n 'RETIRED\|def retire' resources/board/shared.py; then exit 1; fi
python3 resources/pearde.py share --dry
bash resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh
S=$(git rev-parse --git-common-dir)/pearde-shared
mkdir -p "$S/.pearde/graphify/cache" && echo x > "$S/.pearde/graphify/cache/probe"
if bash resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh; then exit 1; fi
python3 resources/pearde.py upgrade .
test ! -e "$S/.pearde" && test -f "$S/pearde/graphify/cache/probe"
rm -f "$S/pearde/graphify/cache/probe"
bash resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh
```
