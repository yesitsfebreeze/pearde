#!/bin/bash
# ramp is a doctor row, not a gate — the whole contract as checks.
#
#   bash probe/verify.sh                 # against the repo this probe sits in
#   PEARDE_ROOT=<checkout> bash probe/verify.sh
#
# Every fixture is built in a temp dir made at run time. Nothing here reaches
# the network: `pearde ramp` itself does, and it is the one command a person
# runs, so the checks stop at `ramp gap`, which is local.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="${PEARDE_ROOT:-$(cd "$HERE/../../../../.." && pwd -P)}"
PEARDE="$ROOT/resources/pearde.py"
RAMP="$ROOT/resources/board/ramp.py"
DOCTOR="$ROOT/resources/doctor.sh"
FAILED=0
ok()  { printf 'PASS  %s\n' "$1"; }
no()  { printf 'FAIL  %s\n' "$1"; FAILED=1; }
is()  { if [ "$2" = "$3" ]; then ok "$1 (got $3)"; else no "$1 — want $2, got $3"; fi; }

[ -f "$PEARDE" ] || { echo "no pearde.py at $PEARDE"; exit 2; }

W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
EMPTY="$W/emptyhome"; mkdir -p "$EMPTY"

# ── 1. the key is gone from the code ─────────────────────────────────────────
# references/parts/ramp.md names the key once, to say it was removed — prose
# about a key nobody reads. Every other mention is a reader.
N=$(grep -rl 'happiness' "$ROOT/resources" 2>/dev/null | wc -l | tr -d ' ')
is "no file under resources/ still reads happiness:" 0 "$N"
M=$(grep -c 'happiness' "$ROOT/references/settings.md" 2>/dev/null); M=${M:-0}
is "settings.md declares no happiness key" 0 "$M"

for fn in cmd_gate cmd_happy write_ask "def happiness"; do
  if grep -q "$fn" "$RAMP"; then no "ramp.py still defines $fn"; else ok "ramp.py defines no $fn"; fi
done
if grep -q '"happy"' "$RAMP"; then no "ramp still answers the happy verb"; else ok "ramp answers no happy verb"; fi

# ── 2. a fresh board carries no gate ─────────────────────────────────────────
B="$W/board"; mkdir -p "$B"; cd "$B" || exit 2
git init -q . && printf 'x\n' > a.md && git add -A \
  && git -c user.email=a@b -c user.name=c commit -qm init >/dev/null
python3 "$PEARDE" init --example . >/dev/null 2>&1
if [ -f "$B/.pearde/settings.md" ]; then ok "init --example wrote a board"; else no "init --example wrote no board"; fi
if grep -q 'happiness' "$B/.pearde/settings.md"; then
  no "init --example wrote happiness: into settings.md"
else ok "init --example writes no happiness: key"; fi

P="$W/plain"; mkdir -p "$P"; cd "$P" || exit 2
git init -q . && printf 'x\n' > a.md && git add -A \
  && git -c user.email=a@b -c user.name=c commit -qm init >/dev/null
python3 "$PEARDE" init . >/dev/null 2>&1
if grep -q 'happiness' "$P/.pearde/settings.md"; then
  no "init wrote happiness: into settings.md"
else ok "init writes no happiness: key"; fi

# ── 3. pass one reaches the scan, and asks nothing ───────────────────────────
cd "$B" || exit 2
OUT=$(python3 "$PEARDE" next 2>&1)
case "$OUT" in
  *"step 0"*|*ramp*|*ASK*) no "next opens on a ramp step or an ASK: $(printf '%s' "$OUT" | head -1)" ;;
  "") no "next printed nothing" ;;
  *) ok "next opens on the scan — $(printf '%s' "$OUT" | head -1 | cut -c1-52)" ;;
esac
if [ -f "$B/.pearde/.state/ask.md" ]; then
  no "a pass on a fresh board left .state/ask.md behind"
else ok "no .state/ask.md on a fresh board"; fi

# ── 4. the measurement still measures, and gates nothing ─────────────────────
printf '[package]\nname="x"\n' > "$B/Cargo.toml"
mkdir -p "$B/src"; for i in 1 2 3 4 5; do printf 'fn main(){}\n' > "$B/src/m$i.rs"; done
( cd "$B" && git add -A && git -c user.email=a@b -c user.name=c commit -qm rust >/dev/null )
G=$(cd "$B" && env HOME="$EMPTY" CLAUDE_CONFIG_DIR="$EMPTY" python3 "$RAMP" gap . 2>&1); RC=$?
is "ramp gap exits 0 with a gap standing" 0 "$RC"
case "$G" in *"GAP rust"*) ok "ramp gap sees the rust the tree asks for" ;;
             *) no "ramp gap missed rust: $(printf '%s' "$G" | head -2 | tr '\n' ' ')" ;; esac

# ── 5. doctor carries the row, and a gap is off, never broken ────────────────
D=$(cd "$B" && env HOME="$EMPTY" CLAUDE_CONFIG_DIR="$EMPTY" bash "$DOCTOR" . 2>&1)
R=$(printf '%s\n' "$D" | grep -m1 '^  ramp ')
if [ -z "$R" ]; then no "doctor printed no ramp row"; else ok "doctor prints a ramp row —$(printf '%s' "$R" | sed 's/^  ramp *//' | cut -c1-46)"; fi
case "$R" in
  *broken*) no "doctor calls an unanswered job broken" ;;
  *off*)    ok "an unanswered job reads off, not broken" ;;
  *)        no "the ramp row read neither off nor broken: $R" ;;
esac
case "$D" in *"pearde.py ramp"*) ok "the row's fix line names pearde ramp" ;;
             *) no "the ramp row names no fix" ;; esac
# the row must not be what makes doctor red
BR=$(printf '%s\n' "$D" | grep -c ' broken ')
RB=$(printf '%s\n' "$D" | grep -c '^  ramp .*broken')
is "the ramp row contributes no broken part" 0 "$RB"

# ── 6. a board whose tree asks for nothing says so ───────────────────────────
E="$W/bare"; mkdir -p "$E"; cd "$E" || exit 2
git init -q . && printf 'x\n' > a.txt && git add -A \
  && git -c user.email=a@b -c user.name=c commit -qm init >/dev/null
python3 "$PEARDE" init . >/dev/null 2>&1
DE=$(cd "$E" && env HOME="$EMPTY" CLAUDE_CONFIG_DIR="$EMPTY" bash "$DOCTOR" . 2>&1 | grep -m1 '^  ramp ')
case "$DE" in *off*) ok "a tree asking for nothing reads off — $(printf '%s' "$DE" | sed 's/^  ramp *off *//' | cut -c1-40)" ;;
              *) no "a tree asking for nothing did not read off: $DE" ;; esac

echo
[ "$FAILED" = 0 ] && echo "ramp is a doctor row, not a gate — every check green" \
                  || echo "ramp: a check failed above"
exit $FAILED
