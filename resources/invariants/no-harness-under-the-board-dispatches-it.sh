#!/usr/bin/env bash
# no-harness-under-the-board-dispatches-it — run from the repo root:
#
#     bash resources/invariants/no-harness-under-the-board-dispatches-it.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant: no file under any `prds/**/probe/` on this board launches
# something that moves a board. The reader is
# `.pearde/prds/a-harness-never-dispatches-the-live-board/probe/scan.py`,
# which resolves shell variables and reads Python as an AST; a command whose
# command word resolves to `run.py`, `dispatch.py`, `machine.py`, `pearde run`
# or a `claude … /pearde run`, with no `--dry` and no read word after it, is a
# defect wherever written.
#
# The second half of the contract: `run.py all` refuses, the refusal names
# `pearde plan`, `plan slots` prints its reading, and `plan.py` names
# `read_main`. Those are the mechanism the reader's tally rests on — a bare
# scope that dispatches would make every "0 dispatcher launches" green.

set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 1

fail=0

# 1. the reader finds no dispatcher launch on this board
if ! python3 .pearde/prds/a-harness-never-dispatches-the-live-board/probe/scan.py .pearde >/dev/null 2>&1; then
    echo "FAIL the reader found a dispatcher launch on this board"
    python3 .pearde/prds/a-harness-never-dispatches-the-live-board/probe/scan.py .pearde || true
    fail=1
fi

# 2. the mechanism: bare `run.py all` refuses, and the read is reachable
if ! python3 resources/board/run.py all 2>&1 | grep -q 'refused'; then
    echo "FAIL run.py all did not refuse"
    fail=1
fi
if ! python3 resources/board/plan.py plan slots | grep -qE '^[0-9]+ slots '; then
    echo "FAIL plan slots did not print its reading"
    fail=1
fi
if ! grep -q read_main resources/board/plan.py; then
    echo "FAIL plan.py does not name read_main"
    fail=1
fi

if [ "$fail" -eq 0 ]; then
    echo "no-harness-under-the-board-dispatches-it: green"
    exit 0
fi
exit 1