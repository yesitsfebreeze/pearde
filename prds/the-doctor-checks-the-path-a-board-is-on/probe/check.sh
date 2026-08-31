#!/bin/bash
# Probe for "the doctor checks the path a board is on". Builds two throwaway
# fixtures under a fresh mktemp dir (never under prds/) and runs
# resources/doctor.sh against each, to show the contract-path (`board`) row
# on both a healthy `.pearde/` layout and a leftover old-layout `prds/`.
set -uo pipefail
DOCTOR=/Users/feb/dev/infra/pearde/resources/doctor.sh
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

echo "=== on THIS repo (.pearde/ layout) ==="
bash "$DOCTOR" /Users/feb/dev/infra/pearde 2>&1 | grep -A1 '^  board'

echo
echo "=== fixture: old layout, root-level prds/, no .pearde/ ==="
OLD="$T/old-layout"
mkdir -p "$OLD/prds/some-prd"
cat > "$OLD/prds/some-prd/prd.md" <<'PRD'
---
state: open
---
# a prd
PRD
git -C "$OLD" init -q
bash "$DOCTOR" "$OLD" 2>&1 | grep -A1 '^  board'

echo
echo "=== fixture: no board at all ==="
EMPTY="$T/no-board"
mkdir -p "$EMPTY"
bash "$DOCTOR" "$EMPTY" 2>&1 | grep -A1 '^  board'
