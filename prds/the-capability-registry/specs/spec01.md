---
complexity: 12
footprint:
  - resources/capabilities.py
  - resources/pearde.py
  - capabilities.md
  - references/files.md
---

# spec01 — `pearde capabilities` generates the registry from the same walk `pearde.py` already does

`resources/capabilities.py` is new: it reuses `pearde.py`'s own `discover()`
(the `COMMANDS` walk under every directory of `resources/`) and `FORWARD`
table, so it names every verb `pearde` actually dispatches — 44 today, `add`
through `workflow`. It writes `capabilities.md` at the repo root, beside
`index.md`: one row per verb — name, its docstring's first line as the
one-line contract, `reads`/`writes` (read off a `.reads`/`.writes` attribute
a command can set, the way `--help`'s `takes:` line already reads `.flags` —
undeclared prints `—`, since nothing in this tree declares either today),
and a cost class (`shell` for a `.sh` script, `python` for a `.py` one —
`network` and `human` are declared the same way once a command needs them;
none does yet). `resources/pearde.py`'s `FORWARD` table gains one row so
`pearde capabilities` and `pearde capabilities check` route to it — the one
hand-edit any `FORWARD` addition costs, same as `index` or `guard` before
it; the registry's own rows still need no hand edit when a verb is added.
This already stands, built and run in the tree.

## Acceptance

- [x] `pearde capabilities` prints the registry and rewrites
      `capabilities.md`; its row count equals `len(discover()[0]) +
      len(FORWARD)` from `pearde.py` — provable by diffing the two in one
      command (box 1).
- [x] A stub verb added to any tool's `COMMANDS` appears in the registry on
      the next `pearde capabilities`, with no hand edit to
      `capabilities.py` or `capabilities.md` (box 2).
- [x] `pearde capabilities check` is silent and exits 0 on a freshly
      generated file; it reports and exits 1 when a row names a verb that
      no longer exists, when a live verb has no row, or when the file was
      hand-edited away from what regeneration would write (box 3).

## Verify and Proof

```sh
# box 1 — row count matches discover()+FORWARD exactly
cd /Users/feb/dev/infra/pearde/.pearde/.lanes/the-capability-registry
python3 resources/pearde.py capabilities >/tmp/cap.out
n_rows=$(grep -c '^| `' /tmp/cap.out)
n_live=$(python3 -c "
import sys; sys.path.insert(0,'resources')
import pearde
found,_ = pearde.discover()
print(len(found)+len(pearde.FORWARD))
")
[ "$n_rows" = "$n_live" ] || { echo "COUNT_MISMATCH $n_rows != $n_live"; exit 1; }
echo COUNT_OK

# box 2 — a stub verb appears with no hand edit to the generator or the file
python3 - <<'EOF'
p = "resources/board/orphans.py"
src = open(p, encoding="utf-8").read()
assert "zzstub" not in src
src2 = src.replace(
    'COMMANDS = {"orphans": cmd_orphans}',
    'def cmd_zzstub(argv):\n    """probe stub."""\n    return 0\n\n\n'
    'COMMANDS = {"orphans": cmd_orphans, "zzstub": cmd_zzstub}')
assert src2 != src
open(p, "w", encoding="utf-8").write(src2)
EOF
python3 resources/pearde.py capabilities | grep -q '| `zzstub` |' || { echo NO_STUB_ROW; exit 1; }
echo STUB_FOUND
# revert the stub — no trace left for the next box
python3 - <<'EOF'
p = "resources/board/orphans.py"
src = open(p, encoding="utf-8").read()
src2 = src.replace(
    '\ndef cmd_zzstub(argv):\n    """probe stub."""\n    return 0\n\n\n'
    'COMMANDS = {"orphans": cmd_orphans, "zzstub": cmd_zzstub}',
    '\nCOMMANDS = {"orphans": cmd_orphans}')
assert src2 != src
open(p, "w", encoding="utf-8").write(src2)
EOF

# box 3 — check: clean, then dead-verb, then stale-content, each convicted
python3 resources/pearde.py capabilities >/dev/null
python3 resources/pearde.py capabilities check
[ $? -eq 0 ] || { echo CHECK_SHOULD_BE_CLEAN; exit 1; }
sed -i '' 's/| `scan` | the board, read and ordered/| `scan` | HAND EDITED/' capabilities.md 2>/dev/null \
  || sed -i 's/| `scan` | the board, read and ordered/| `scan` | HAND EDITED/' capabilities.md
out=$(python3 resources/pearde.py capabilities check) && rc=0 || rc=$?
[ $rc -eq 1 ] && echo "$out" | grep -q "stale" || { echo "STALE_NOT_CAUGHT: $out"; exit 1; }
python3 resources/pearde.py capabilities >/dev/null   # restore
echo VERIFY_DONE
```
