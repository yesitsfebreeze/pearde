#!/usr/bin/env bash
# The contract: a cross-board `needs:` naming a board this scan does not hold
# is ignored, not held. Every other unresolvable need still holds.
set -e
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# proves a tree holding none of the work. BOARD is the `.pearde` this harness
# sits under, found by walking, so no count of `..` has to match the PRD's
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's repo
# otherwise.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
here="$HERE"
# harness.py takes the tree from PEARDE_TREE; the runner names it here.
exec env PEARDE_TREE="${PEARDE_TREE:-$ROOT}" python3 "$here/harness.py" "$@"
