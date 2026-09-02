#!/usr/bin/env bash
# probe — does the union change a plain board's numbers?
# Runs the committed ramp.py and the working-tree ramp.py over every board on
# this machine's master and diffs `need`. A plain board must be byte-identical;
# only the master may move.
set -u
OLD="${1:?usage: compare.sh <a HEAD export of this repo, e.g. git archive HEAD | tar -x -C DIR>}"/resources/board
# NEW defaults to the orchestrator's checkout; a worker in a lane worktree
# points it at the lane, whose ramp.py is the one under test.
NEW="${NEW:-/Users/feb/dev/infra/pearde/resources/board}"
BOARDS=(/Users/feb/dev/infra/mitosys/.pearde /Users/feb/dev/infra/model/.pearde \
        /Users/feb/dev/infra/realm/.pearde /Users/feb/dev/infra/shared/.pearde \
        /Users/feb/dev/infra/pearde/.pearde /Users/feb/dev/infra/.pearde)
rc=0
for b in "${BOARDS[@]}"; do
  a=$(python3 "$OLD/ramp.py" need --board "$b" 2>&1)
  n=$(python3 "$NEW/ramp.py" need --board "$b" 2>&1)
  if [ "$a" = "$n" ]; then
    echo "same   $b"
  else
    echo "MOVED  $b"
    diff <(echo "$a") <(echo "$n") | sed 's/^/       /'
    rc=1
  fi
done
exit $rc
