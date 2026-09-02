#!/usr/bin/env bash
# Proves the timing assertion in scan-parses-.../probe/verify.sh judges the
# machine, not the code: the SAME HEAD, the SAME plan.py, run under CPU load,
# crosses the 40 ms bar and inverts warm-vs-cold.
set -u
REPO="$(cd "$(dirname "$0")/../../../.." && pwd)"
H="$REPO/.pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh"
N="${1:-8}"
echo "== idle =="
bash "$H" 2>&1 | tail -3
echo "== under $N spinners (nothing in the tree changed) =="
for _ in $(seq 1 "$N"); do python3 -c '
import time
t=time.time()
while time.time()-t < 25: pass' & done
SPIN=$(jobs -p | tr '\n' ' ')
bash "$H" 2>&1 | tail -3; RC=$?
kill $SPIN 2>/dev/null; wait 2>/dev/null
exit 0
