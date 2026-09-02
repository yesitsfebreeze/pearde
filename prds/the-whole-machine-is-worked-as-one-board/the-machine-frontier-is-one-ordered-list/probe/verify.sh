#!/usr/bin/env bash
# the machine frontier — read-only, so the whole harness is: it runs from a
# directory with no board above it, it prints an order, it prints the reading
# that produced the count, and the tree is no different afterwards.
set -u
ROOT="${PEARDE_ROOT:-/Users/feb/dev/infra/pearde}"
MACHINE="${MACHINE_PY:-$ROOT/resources/board/machine.py}"
# the command is run from `/`, so a relative MACHINE_PY is resolved against
# the repo root here — a path that stops working when you cd is not a path
case "$MACHINE" in /*) ;; *) MACHINE="$ROOT/$MACHINE" ;; esac
[ -f "$MACHINE" ] || MACHINE="$(cd "$(dirname "$0")" && pwd)/machine.py"
fail=0
t() { if eval "$2" >/dev/null 2>&1; then echo "ok   $1"; else echo "FAIL $1"; fail=1; fi; }

# what the tree looked like BEFORE the read-only command ran. Snapshotting it
# afterwards could not tell this build's own new files from a write the
# command made, which is the only thing this row is asking about.
BEFORE="$(cd "$ROOT" && git status --porcelain)"
OUT="$(cd / && python3 "$MACHINE" machine 2>&1)"

t "runs from / with no board above the cwd"      '[ -n "$OUT" ]'
t "prints a board count over the watch set"      'grep -qE "^[0-9]+ of [0-9]+ board\(s\) · [0-9]+ PRDs on the frontier · [0-9]+ wave\(s\)$" <<<"$OUT"'
t "prints the slot count and its reading"        'grep -qE "^[0-9]+ slots \(.*ceiling [0-9]+\) · " <<<"$OUT"'
t "the reading names the cpu term"               'grep -qE "· cpu [0-9.]+ of [0-9]+ loaded" <<<"$OUT"'
t "the reading names the memory term"            'grep -qE "· mem [0-9.]+ of [0-9]+ GiB used" <<<"$OUT"'
t "every row is addressed @<board>/<rel>"        'grep -qE "^ *[0-9]+\. @[a-z0-9-]+/" <<<"$OUT"'
t "prints at least one wave"                     'grep -qE "^wave 1: @" <<<"$OUT"'
t "a row marked ready is in a wave"              '! comm -23 <(grep -oE "@[^ ]+" <<<"$(grep " ready  " <<<"$OUT")" | sort -u) <(grep "^wave " <<<"$OUT" | grep -oE "@[^,]+" | sed "s/^wave [0-9]*: //" | tr -d " " | sort -u) | grep -q .'
t "no row marked ready carries a non-dispatchable state" '! grep -E " (question|blocked|analyzing|claimed|deferred) +ready " <<<"$OUT"'
t "the merged progress line is one line"         '[ "$(cd / && python3 "$MACHINE" machine progress 2>&1 | wc -l | tr -d " ")" = 1 ]'
t "--json parses and carries slots, rows, waves" 'cd / && python3 "$MACHINE" machine --json 2>/dev/null | python3 -c "import json,sys;d=json.load(sys.stdin);assert d[\"slots\"]>=1 and d[\"rows\"] and d[\"waves\"]"'
t "it moved nothing in this repo"                '[ "$BEFORE" = "$(cd "$ROOT" && git status --porcelain)" ]'

# ── the ceiling is a setting, and `0` is the word this board uses for
# unlimited. These three ran against a throwaway board rather than the repo's
# own, because the case is what `machine-ceiling` SAYS, not what this machine
# is doing: the count is read straight out of `slots()` with the meter held
# still, so a busy afternoon cannot make the answer flap.
CEIL="$(mktemp -d)"; mkdir -p "$CEIL/.pearde"
ceil() {  # ceil <value|-> -> "<ceiling> <slots on a quiet machine>"
  if [ "$1" = "-" ]; then rm -f "$CEIL/.pearde/settings.md"
  else printf -- '---\nmachine-ceiling: %s\n---\n\n# s\n' "$1" > "$CEIL/.pearde/settings.md"; fi
  MDIR="$(dirname "$MACHINE")" BOARD="$CEIL/.pearde" python3 - <<'PY'
import os, sys
sys.path.insert(0, os.environ["MDIR"])
import machine as m
m.SLOT_CEILING = m.ceiling(os.environ["BOARD"])
m._machine = lambda: (10, 32768.0, 0.20, 2000.0)   # a quiet 10-core/32GiB
n, r = m.slots()
print(m.SLOT_CEILING, n, r.split(" · ")[0])
PY
}

t "machine-ceiling: 0 lifts the ceiling"         '[ "$(ceil 0 | cut -d" " -f1-2)" = "0 24" ]'
t "an unlimited ceiling prints ∞, never 0"       'ceil 0 | grep -q "ceiling ∞)"'
t "an unlimited ceiling keeps the floor of 1"    'MDIR="$(dirname "$MACHINE")" python3 -c "
import os,sys; sys.path.insert(0, os.environ[\"MDIR\"]); import machine as m
m.SLOT_CEILING = 0
m._machine = lambda: (10, 32768.0, 40.0, 30000.0)
m._busy_now = lambda seconds=1: (0.99, 1.0)
n, r = m.slots(); assert n == 1, (n, r)"'
t "a set machine-ceiling is honoured"            '[ "$(ceil 4 | cut -d" " -f1-2)" = "4 4" ]'
t "an absent machine-ceiling still gives 12"     '[ "$(ceil - | cut -d" " -f1-2)" = "12 12" ]'
t "an unparseable machine-ceiling gives 12"      '[ "$(ceil banana | cut -d" " -f1-2)" = "12 12" ]'
rm -rf "$CEIL"

[ $fail -eq 0 ] && echo "PASS" || echo "FAIL"
exit $fail
