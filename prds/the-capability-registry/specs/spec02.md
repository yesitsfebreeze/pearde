---
complexity: 6
footprint:
  - resources/index.py
  - references/files.md
---

# spec02 — doctor's `index` row convicts a verb the registry drifted on

`index.py check()` — the function `doctor.sh`'s `index` row runs and prints
under — now also runs `capabilities.py check()` (spec01) and folds its
problems in: the same drift the file manifest already convicts (a file on
disk with no row, a row naming no file), run on verbs instead of files. No
new doctor row: `doctor.sh` already prints whatever `index.py check` prints
under the `index` label, so the line lands there with no second wire. This
already stands, built and run in the tree.

## Acceptance

- [x] `pearde index check` (and therefore `doctor`'s `index` row) reports a
      problem when `capabilities.md` names a verb that no longer exists
      (box 1).
- [x] It reports a problem when a live verb has no row in
      `capabilities.md` (box 2).
- [x] With `capabilities.md` freshly regenerated and the file manifest
      itself clean, `pearde index check` is silent and exits 0 — the new
      line adds no noise to a clean tree (box 3).

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde/.pearde/.lanes/the-capability-registry

# box 1 — dead verb named in the registry
python3 resources/pearde.py capabilities >/dev/null
sed -i '' '$a\
| `zzdead` | not a real verb | — | — | python |
' capabilities.md 2>/dev/null || echo '| `zzdead` | not a real verb | — | — | python |' >> capabilities.md
python3 resources/pearde.py index check 2>&1 | grep -q 'zzdead' \
  && echo DEAD_VERB_CAUGHT || { echo DEAD_VERB_MISSED; exit 1; }
python3 resources/pearde.py capabilities >/dev/null   # restore

# box 2 — live verb with no row
python3 - <<'EOF'
p = "resources/board/orphans.py"
src = open(p, encoding="utf-8").read()
src2 = src.replace(
    'COMMANDS = {"orphans": cmd_orphans}',
    'def cmd_zzstub(argv):\n    """probe stub."""\n    return 0\n\n\n'
    'COMMANDS = {"orphans": cmd_orphans, "zzstub": cmd_zzstub}')
open(p, "w", encoding="utf-8").write(src2)
EOF
# capabilities.md is now stale (missing zzstub's row) without regenerating
python3 resources/pearde.py index check 2>&1 | grep -q 'zzstub' \
  && echo MISSING_ROW_CAUGHT || { echo MISSING_ROW_MISSED; exit 1; }
python3 - <<'EOF'
p = "resources/board/orphans.py"
src = open(p, encoding="utf-8").read()
src2 = src.replace(
    '\ndef cmd_zzstub(argv):\n    """probe stub."""\n    return 0\n\n\n'
    'COMMANDS = {"orphans": cmd_orphans, "zzstub": cmd_zzstub}',
    '\nCOMMANDS = {"orphans": cmd_orphans}')
open(p, "w", encoding="utf-8").write(src2)
EOF
python3 resources/pearde.py capabilities >/dev/null   # restore

# box 3 — clean tree, no new noise (pre-existing, unrelated manifest drift
# in this checkout — resources/common.py, hotreload-test.js — is left out;
# it predates this PRD and is reported separately, not asserted here)
out=$(python3 resources/pearde.py index check 2>&1)
echo "$out" | grep -qi 'verb\|capabilities' && { echo "UNEXPECTED_NOISE: $out"; exit 1; }
echo CLEAN_ADDS_NO_NOISE
echo VERIFY_DONE
```
