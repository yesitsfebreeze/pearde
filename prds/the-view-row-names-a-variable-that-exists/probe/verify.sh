#!/usr/bin/env bash
# the-view-row-names-a-variable-that-exists — probe harness.
#
# The view row in resources/doctor.sh reads $PBOARD; e628725 (the board row
# walks for `.pearde/`) removed the only definition. Under `set -u` bash 3.2
# does not abort the row: it prints "PBOARD: unbound variable" and the elif
# chain falls through to `broken`, so a board reached through a symlinked
# path reports "the service is up but this board is not registered" with a
# real daemon watching it.
#
# Fixture: a one-row /status JSON server on a scratch port and a board in a
# run-time mktemp -d, never under prds/. Every doctor call is pointed at a
# PEARDE_PORT nothing real holds, so the probe never touches the live daemon,
# a real registry, or any real board. Run as:
#   bash .pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh
set -u
cd "$(dirname "$0")/../../../.." || exit 1
DOCTOR="$PWD/resources/doctor.sh"

pass=0; fail=0
ok()  { pass=$((pass+1)); echo "  ok    $1"; }
bad() { fail=$((fail+1)); echo "  FAIL  $1${2:+  — $2}"; }
# the view row, out of a full doctor report — never a filename argument
vrow() { printf '%s' "$1" | grep -E '^ +view ' | head -1; }

D="$(mktemp -d /tmp/pearde-viewrow.XXXXXX)"
SRVPID=""; SRVPID2=""
cleanup() {
  [ -n "$SRVPID" ]  && kill "$SRVPID"  2>/dev/null
  [ -n "$SRVPID2" ] && kill "$SRVPID2" 2>/dev/null
  [ -n "$SRVPID3" ] && kill "$SRVPID3" 2>/dev/null
  rm -rf "$D"
}
trap cleanup EXIT
mkdir -p "$D/.pearde"; printf 'name: viewrow-fixture\n' > "$D/.pearde/settings.md"

# the physical spelling of the board dir — macOS /tmp is a symlink to
# /private/tmp, so pwd -P is what a service built on the physical path holds
PHYS="$( cd "$D" && pwd -P )"

# one fixture server per spelling; both answer /status with one board row
mk_srv() {  # $1 = port, $2 = the path the service claims to watch, $3 = out file
  cat > "$3" <<PY
import http.server, json
BODY = json.dumps({"pid":1,"port":$1,"boot":"fixture","boards":[
  {"name":"nope-fixture","path":"$2","seq":0,"last_sync":0.0,
   "last_error":None,"members":[]}]}).encode()
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(BODY)))
        self.end_headers(); self.wfile.write(BODY)
    def log_message(self,*a): pass
http.server.HTTPServer(("127.0.0.1",$1),H).serve_forever()
PY
}

# ── the defect the PRD names ─────────────────────────────────────────────
# 1. the view block defines PBOARD before the line that reads it
if grep -q 'PBOARD=$(cd "$BOARD" 2>/dev/null && pwd -P)' "$DOCTOR"; then
  ok "the view block defines PBOARD before its elif reads it"
else
  bad "no PBOARD definition inside the view block"
fi

# 2. the elif line itself — the line that carried the bare $PBOARD — names
#    only variables defined in doctor.sh. Scanned off the elif's three grep
#    lines: WBOARD_JSON is defined beside the PBOARD line, in the same block.
VA=$(sed -n '/^  elif printf/,/WBOARD_JSON"; then/p' "$DOCTOR" \
     | grep -oE '\$[A-Za-z_][A-Za-z0-9_]*' | sort -u | tr -d '$')
# BOARD is the script's own walk; WBOARD_JSON is defined two lines above PBOARD
VA=$(printf '%s\n' "$VA" | grep -vE '^(BOARD|WBOARD_JSON)$')
miss=""
for v in $VA; do
  grep -qE "(^|[^A-Za-z_])$v=" "$DOCTOR" || miss="$miss $v"
done
[ -z "$miss" ] && ok "every variable the view row names is defined" \
                || bad "undefined in the view block:$miss"

# 3. a live service on the spelling doctor walks → view ok, no unbound line
mk_srv 8477 "$D/.pearde" "$D/srv1.py"
python3 "$D/srv1.py" & SRVPID=$!
sleep 1
out="$(env -i PEARDE_PORT=8477 /bin/bash "$DOCTOR" "$D" 2>&1)"
[ "$(printf '%s' "$out" | grep -c 'unbound variable' || true)" -eq 0 ] \
  && ok "no unbound-variable line anywhere in doctor's report" \
  || bad "doctor still trips over an unset variable"
if printf '%s' "$(vrow "$out")" | grep -qE 'view +ok'; then
  ok "view ok when the service holds the spelling doctor walks"
else
  bad "same-spelling service: view should be ok — got: $(vrow "$out")"
fi

# 4. the everyday macOS symlink case: shell walks the symlink spelling,
#    the service holds the physical /private/tmp one. Only PBOARD bridges it.
mk_srv 8478 "$PHYS/.pearde" "$D/srv2.py"
python3 "$D/srv2.py" & SRVPID2=$!
sleep 1
LNK="$(mktemp -d /tmp/pearde-viewrow-lnk.XXXXXX)/b"
rm -rf "$LNK"; ln -s "$PHYS" "$LNK"
out="$(env -i PEARDE_PORT=8478 /bin/bash "$DOCTOR" "$LNK" 2>&1)"
if printf '%s' "$(vrow "$out")" | grep -qE 'view +ok'; then
  ok "view ok across a symlinked START — pwd -P bridges the spelling"
else
  bad "symlink START, physical-spelling service: view should be ok — got: $(vrow "$out")"
fi

# 5. the name-extraction arm: the ok line still prints the board's name,
#    and an unrelated board row in the same /status does not disturb it
mk_srv 8479 "$D/.pearde" "$D/srv3.py"
python3 "$D/srv3.py" & SRVPID3=$!
sleep 1
out="$(env -i PEARDE_PORT=8479 /bin/bash "$DOCTOR" "$D" 2>&1)"
if printf '%s' "$(vrow "$out")" | grep -qF 'board/nope-fixture'; then
  ok "the ok line names the board, spelled $D · /status holds it"
else
  bad "the name arm should print the registered name — got: $(vrow "$out")"
fi

echo "$((pass+fail)) checks · $pass pass · $fail fail"
echo "probe harness complete"
[ "$fail" -eq 0 ] || exit 1