---
complexity: 3
footprint:
  - resources/doctor.sh
---

# spec01 — the view row defines every variable it reads

The view service row in `resources/doctor.sh` matched the live daemon's
registered board path against three spellings of `$BOARD`; commit e628725
(the board row walks for `.pearde/`, not `prds/`) removed the `PBOARD`
definition the third of those still read. Under `set -u` bash 3.2 does not
abort there — it prints `PBOARD: unbound variable` and the elif chain falls
through to `broken`, so a board whose path this shell spells differently from
the registry (a symlinked cwd; /tmp vs /private/tmp on macOS) reports "the
service is up but this board is not registered" with a real daemon watching
it, and an unbound-variable line mid-report.

What already stands (built in this PRD's probe round, uncommitted on the
tree at spec time — a later worker re-verifies, it does not rebuild):

- the view block defines `PBOARD=$(cd "$BOARD" 2>/dev/null && pwd -P)` after
  `WBOARD_JSON`, before the `if [ -z "$SRV" ]` chain (resources/doctor.sh:590)
- the probe harness
  `.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh`
  runs 6 checks green against a fixture /status server on scratch ports

What is left to finish: nothing in the row itself. The remaining work is
confirmation breadth only — the unit is complete when the checks below pass
on this machine and the two view harnesses named in the PRD round are still
green.

## Acceptance

- [x] `resources/doctor.sh` defines `PBOARD` inside the view block, before
      the `elif` line that greps `"\"$PBOARD\""` — `grep -n 'PBOARD'
      resources/doctor.sh`: `590:  PBOARD=$(cd "$BOARD" 2>/dev/null && pwd
      -P)`, read at `598: || printf '%s' "$SRV" | grep -qF "\"$PBOARD\"" \`,
      both inside the `if [ -n "$BOARD" ]` view block opened at 584
- [x] `bash resources/doctor.sh` on a board whose daemon answers /status with
      a path spelled through a symlinked cwd prints `view ok`, and no line of
      the report contains `unbound variable` — probe checks 3 and 5:
      `ok    no unbound-variable line anywhere in doctor's report`,
      `ok    view ok across a symlinked START — pwd -P bridges the spelling`
- [x] every variable the view row's `elif` condition names is assigned
      somewhere in resources/doctor.sh — probe check 2:
      `ok    every variable the view row names is defined`
- [x] `bash .pearde/prds/the-page-shows-the-round/probe/verify.sh` still
      prints 24/24 checks pass, and
      `.pearde/prds/one-page-that-says-whats-up/probe/verify.sh` 30/30 — the
      view row's change touches only the path match, never the page.
      `the-page-shows-the-round` is a child of `the-board-runs-itself`, so the
      real path is
      `.pearde/prds/the-board-runs-itself/the-page-shows-the-round/probe/verify.sh`:
      rc=0, `24/24 checks pass` (its served half skipped — no daemon on
      :8443). `one-page-that-says-whats-up`: rc=0, `30 checks · 30 pass · 0
      fail`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
r=$(env -i PEARDE_PORT=1 bash resources/doctor.sh "$PWD" 2>&1 || true)
grep -c 'unbound variable' <<<"$r" || true
grep -E '^ +view ' <<<"$r"
grep -n 'PBOARD=\$(cd' resources/doctor.sh
bash .pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh
echo "verify done rc=$?"
```