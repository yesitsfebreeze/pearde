#!/usr/bin/env bash
# Proves quickstart.sh section 6 judges the machine, not the code: it diffs
# two WHOLE doctor reports taken at two different moments, so any row that
# reads machine-global state can move between them for a reason that has
# nothing to do with HOME. Injected here: the view daemon going away between
# the two runs — exactly what a neighbouring session's `serve.py stop` does.
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
TOP="$(mktemp -d)"; COPY="$TOP/pearde"; PROJ="$TOP/proj"; NOOBS="$TOP/no-obsidian"
trap 'PEARDE_PORT=$SPARE python3 "$COPY/resources/board/serve.py" stop >/dev/null 2>&1; rm -rf "$TOP"' EXIT
mkdir -p "$COPY" "$PROJ" "$NOOBS"
( cd "$ROOT" && git ls-files -z | rsync -a0 --files-from=- "$ROOT/" "$COPY/" )
SPARE="$(python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()')"
export PEARDE_PORT="$SPARE" PEARDE_AS=engineer
cd "$PROJ" && git init -q .
python3 "$COPY/resources/board/init.py" init --example >/dev/null 2>&1 \
  || python3 "$COPY/resources/pearde.py" init --example >/dev/null 2>&1
python3 "$COPY/resources/board/serve.py" ensure "$PROJ/.pearde" >/dev/null 2>&1

rows() { printf '%s\n' "$1" | sed -nE 's/^  ([a-z]+) +(ok|broken|off) .*/\1 \2/p'; }

WITH="$(bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1)"
# --- the injection: a neighbour stops the service between the two runs ---
python3 "$COPY/resources/board/serve.py" stop >/dev/null 2>&1
OUT="$(env -u XDG_CONFIG_HOME HOME="$NOOBS" bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1)"

echo "rows read: $(rows "$WITH" | wc -l | tr -d ' ')"
D="$(diff <(rows "$WITH") <(rows "$OUT") | grep -c '^[<>] ' || true)"
echo "section-6 'no row's verdict moves' diff count: $D  (the harness demands 0)"
diff <(rows "$WITH") <(rows "$OUT") | grep '^[<>] ' || true
[ "$D" = 0 ] && echo "RESULT: green" || echo "RESULT: RED — and README, doctor.sh and the board are all correct"
