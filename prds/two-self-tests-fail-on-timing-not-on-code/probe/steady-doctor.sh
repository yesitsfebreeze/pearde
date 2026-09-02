#!/usr/bin/env bash
# The pair to flake-doctor.sh: the SAME injection — the view service stopped
# between the two doctor runs, which is what a neighbouring session's
# `serve.py stop` does — run through the re-aimed section-6 logic. The old
# logic went red on it (flake-doctor.sh). The control pair names it as a row
# that moved with the home held constant, does not judge it, and stays green.
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
TOP="$(mktemp -d)"; COPY="$TOP/pearde"; PROJ="$TOP/proj"; NOOBS="$TOP/no-obsidian"
SPARE=""
trap 'PEARDE_PORT=$SPARE python3 "$COPY/resources/board/serve.py" stop >/dev/null 2>&1; rm -rf "$TOP"' EXIT
mkdir -p "$COPY" "$PROJ" "$NOOBS"
( cd "$ROOT" && git ls-files -z | rsync -a0 --files-from=- "$ROOT/" "$COPY/" )
SPARE="$(python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()')"
export PEARDE_PORT="$SPARE" PEARDE_AS=engineer
cd "$PROJ" && git init -q .
python3 "$COPY/resources/pearde.py" init --example >/dev/null 2>&1
python3 "$COPY/resources/board/serve.py" ensure "$PROJ/.pearde" >/dev/null 2>&1

rows()  { printf '%s\n' "$1" | sed -nE 's/^  ([a-z]+) +(ok|broken|off) .*/\1 \2/p'; }
docA()  { bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1; }
docB()  { env -u XDG_CONFIG_HOME HOME="$NOOBS" bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1; }
moved() { diff <(rows "$1") <(rows "$2") | sed -nE 's/^[<>] ([a-z]+) .*/\1/p' | sort -u; }

WITH="$(docA)"
# --- the injection, at exactly the moment the old logic could not survive ---
python3 "$COPY/resources/board/serve.py" stop >/dev/null 2>&1
OUT="$(docB)"
AGAIN="$(docA)"

echo "old logic — a plain diff of the two whole reports:"
OLD="$(diff <(rows "$WITH") <(rows "$OUT") | grep -c '^[<>] ' || true)"
echo "  rows differing: $OLD  (the old check demanded 0) -> $([ "$OLD" = 0 ] && echo green || echo RED)"

VOLATILE="$(moved "$WITH" "$AGAIN")"
HOMEDEP="$(comm -23 <(moved "$WITH" "$OUT") <(printf '%s\n' "$VOLATILE" | sed '/^$/d'))"
if [ -n "$HOMEDEP" ]; then
  W2="$(docA)"; O2="$(docB)"
  HOMEDEP="$(comm -12 <(printf '%s\n' "$HOMEDEP") <(moved "$W2" "$O2"))"
fi
echo "re-aimed logic — a control pair:"
echo "  moved with the home held constant, so not judged: $(printf '%s' "$VOLATILE" | tr '\n' ' ')"
echo "  home-dependent rows, reproduced on a second pair: '$(printf '%s' "$HOMEDEP" | tr '\n' ' ')'"
N="$(printf '%s\n' "$HOMEDEP" | sed '/^$/d' | grep -c . || true)"
echo "  -> $([ "$N" = 0 ] && echo green || echo RED)"
[ "$OLD" != 0 ] && [ "$N" = 0 ]
