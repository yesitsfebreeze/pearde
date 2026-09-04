#!/usr/bin/env bash
# ported-verbs-match — run from the repo root:
#
#     bash resources/invariants/ported-verbs-match.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant: every verb in `PORTED` (@resources/pearde.py) answers the
# same bytes on stdout and the same exit code whether the Python script or
# the `jd` binary runs it — on a fresh copy of the example board, so the
# live board is never the fixture. `--no-shim` is what keeps the Python
# side honest: without it `pearde <verb>` execs into `jd` and the diff is
# jd against itself.
#
# One line per verb, `ok <verb>` or `drift <verb>`. An empty PORTED is green
# with nothing to say; no `jd` on PATH is a skip, exit 0, because the
# invariant binds the port, not the machine it is checked on.

set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 1

if ! command -v jd >/dev/null 2>&1; then
    echo "ported-verbs-match: skipped — no jd on PATH"
    exit 0
fi

PORTED=$(python3 -c 'import sys; sys.path.insert(0, "resources"); import pearde; print(" ".join(sorted(pearde.PORTED)))')
if [ -z "$PORTED" ]; then
    echo "ported-verbs-match: green — PORTED is empty"
    exit 0
fi

# The argument table: what each verb is run with on the example board. A
# verb with no row runs bare. Extend a row as a verb is ported.
args_for() {
    case "$1" in
        scan|status|plan) echo "" ;;
        *) echo "" ;;
    esac
}

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
if ! python3 resources/pearde.py example "$TMP/board" >/dev/null 2>&1; then
    echo "FAIL pearde example could not write $TMP/board"
    exit 1
fi

fail=0
for v in $PORTED; do
    # shellcheck disable=SC2046 — the table is word-split on purpose
    set -- $(args_for "$v")
    (cd "$TMP/board" && python3 "$ROOT/resources/pearde.py" --no-shim "$v" "$@") >"$TMP/py.out" 2>/dev/null
    prc=$?
    (cd "$TMP/board" && jd "$v" "$@") >"$TMP/jd.out" 2>/dev/null
    jrc=$?
    if [ "$prc" = "$jrc" ] && cmp -s "$TMP/py.out" "$TMP/jd.out"; then
        echo "ok $v"
    else
        echo "drift $v · exit $prc vs $jrc"
        diff "$TMP/py.out" "$TMP/jd.out" | head -5
        fail=1
    fi
done

exit $fail
