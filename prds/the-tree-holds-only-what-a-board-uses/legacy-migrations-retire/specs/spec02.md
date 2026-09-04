---
complexity: 6
footprint:
  - resources/board/init.py
  - resources/doctor.sh
---

# spec02 — the migration door opens

`pearde upgrade` refuses on every board on the current layout. `unhide_board`
rejects any target whose name starts with a dot, and its default target is
`planlib.BOARD_DIR`, which is `.pearde` — so the door the whole contract routes
migrations through raises `Refused` before it does anything. `pearde vault`
refuses the same way. The function moves `pearde/` to an undotted name: the
2026-09-02 direction, reverted the same day. It goes, with its two callers and
the `--dir` plumbing that only fed it.

**Already standing** (pass one): `unhide_board` and both call sites are removed
and `pearde upgrade` runs a board end to end. **Left to finish**: doctor's
`vault` row still prescribes `pearde upgrade` as the fix for a dotted board and
that command now moves nothing, so the row would stay broken forever — the fix
line has to stop naming a move `upgrade` no longer makes. See the report's
`## The vault row and the reverted direction` for what the row should say
instead; this spec only stops it prescribing a no-op.

## Acceptance

- [x] `unhide_board` is defined nowhere and called nowhere. — `grep -rn unhide_board resources/` → no match.
- [x] `cmd_upgrade` and `cmd_vault` name `LEGACY_BOARD_DIR` nowhere, and `upgrade`'s `--dir` flag is either gone from `FLAGS` or still consumed by a step that uses it. — `grep LEGACY_BOARD_DIR resources/board/init.py` → no match; `--dir` still declared in `FLAGS` with its comment, accepted by `Args`.
- [x] `pearde upgrade <dir>` on a freshly `init`ed board prints its step rows and exits 0, in a run and in `--dry`. — dry prints `dry · upgrade tmp.X — would fold the store's retired keys, seed wiki/ …` rc=0; real run rc=0.
- [x] `pearde vault <dir> --dry` on the same board exits 0 and does not refuse. — prints `dry · would register <dir> with Obsidian`, rc=0.
- [x] `resources/doctor.sh`'s `vault` fix line names no command that leaves the row broken when it succeeds. — the dotted-board branch is now `row vault off` with no `fix` line; the remaining `fix` lines sit on other branches (`no $PROJ/.obsidian`, unregistered vault) and name `vault --wait --open`, which fixes those rows.

## Verify and Proof

```sh
cd "$REPO"
if grep -rn --exclude-dir=__pycache__ 'unhide_board' resources/; then exit 1; fi
if grep -n 'LEGACY_BOARD_DIR' resources/board/init.py; then exit 1; fi
T=$(mktemp -d); git -C "$T" init -q .
python3 resources/pearde.py init "$T" >/dev/null
python3 resources/pearde.py upgrade "$T" --dry && python3 resources/pearde.py upgrade "$T"
python3 resources/pearde.py vault "$T" --dry
rm -rf "$T"
```
