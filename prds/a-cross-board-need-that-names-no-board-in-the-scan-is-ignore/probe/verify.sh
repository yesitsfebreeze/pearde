#!/bin/sh
# The contract: a cross-board `needs:` naming a board this scan does not hold
# is ignored, not held. Every other unresolvable need still holds.
set -e
here=$(cd "$(dirname "$0")" && pwd)
exec python3 "$here/harness.py" "$@"
