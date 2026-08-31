#!/usr/bin/env bash
# Pass-one probe for init-writes-a-board-on-the-pearde-layout.
#
# Builds a fresh `.pearde/` with `pearde init --example` in a throwaway
# directory (never under prds/ — that would itself look like a PRD dir) and
# checks the two things the PRD's "Done when" names:
#   1. the example PRDs land at <board>/prds/<name>, not <board>/<name>
#   2. `plan.py scan` reports them by their example-tree names, unprefixed
# Also checks the five-empty-directories requirement on a plain `init`
# (no --example), and that nothing lands outside <board>.
#
# Usage: bash check.sh
set -euo pipefail

BOARD_PY=/Users/feb/dev/infra/pearde/resources/board
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

# 1. --example lands PRDs under prds/, not the board root
mkdir -p "$WORK/ex"
python3 "$BOARD_PY/init.py" init "$WORK/ex" --example >"$WORK/ex.log" 2>&1

for name in asking big big/first big/second building finished landed next; do
  [ -f "$WORK/ex/.pearde/prds/$name/prd.md" ] \
    || fail "expected $WORK/ex/.pearde/prds/$name/prd.md"
done
for name in asking big building finished landed next; do
  [ -e "$WORK/ex/.pearde/$name" ] \
    && fail "$name leaked into the board root instead of prds/"
done
[ -f "$WORK/ex/.pearde/settings.md" ] || fail "settings.md missing from board root"
[ -f "$WORK/ex/.pearde/vision.md" ] || fail "vision.md missing from board root"
[ -f "$WORK/ex/.pearde/memos/dates-are-written-not-stamped.md" ] \
  || fail "memos/ did not land at the board root"
[ -f "$WORK/ex/.pearde/workflows/fix-a-line.md" ] \
  || fail "workflows/ did not land at the board root"
[ -e "$WORK/ex/.pearde/README.md" ] \
  && fail "example/README.md leaked into the board — it is not board content"

# 2. scan reports the example PRDs by their unprefixed names
SCAN="$(python3 "$BOARD_PY/plan.py" scan "$WORK/ex" 2>&1)"
echo "$SCAN" | grep -q "8 PRDs" || fail "scan did not find 8 PRDs — got: $SCAN"
for name in asking building finished next big "big/second"; do
  echo "$SCAN" | grep -qE "· $name ·" \
    || fail "scan output missing an unprefixed row for $name"
done
echo "$SCAN" | grep -q "prds/" && fail "scan output names a PRD prds/-prefixed"

# 3. plain init (no --example) still makes the five empty dirs
mkdir -p "$WORK/plain"
python3 "$BOARD_PY/init.py" init "$WORK/plain" >"$WORK/plain.log" 2>&1
for d in prds memos wiki workflows .state; do
  [ -d "$WORK/plain/.pearde/$d" ] || fail "plain init did not make $d/"
done

echo "PASS - example board lands under prds/, scan sees it unprefixed, the five empty dirs are made on a plain init"
