#!/bin/bash
# Probe for the-graph-lands-inside-the-board. Run from anywhere; verifies
# resources/graph/graph.sh (in the CODE repo, /Users/feb/dev/infra/pearde)
# lands its output at .pearde/graphify/, not graphify-out/ at the repo root.
#
# Confirmed by analyst pass one (2026-08-31):
#   - graphify's paths.py DOES honor a GRAPHIFY_OUT env var, including an
#     absolute-path override (docstring: "worktrees or shared-output setups").
#     The PRD's stated constraint ("no environment variable") is wrong; see
#     the report's Findings section. graph.sh now exports GRAPHIFY_OUT
#     absolute before every graphify call instead of moving/symlinking.
#   - extract's .graphify_root write already does Path(target).resolve() —
#     safe with any target.
#   - update's .graphify_root write does NOT resolve — str(watch_path) as
#     passed. graph.sh must pass the FOLDER's resolved absolute path, never
#     ".", or the marker stamps a literal "." (confirmed by reproduction).
set -euo pipefail
REPO=/Users/feb/dev/infra/pearde
SH="$REPO/resources/graph/graph.sh"

echo "[1] update, then check output location + marker"
bash "$SH" update "$REPO" --force >/dev/null
test -f "$REPO/.pearde/graphify/graph.json" || { echo FAIL: no graph.json under .pearde/graphify; exit 1; }
marker="$(cat "$REPO/.pearde/graphify/.graphify_root")"
[ "$marker" = "$REPO" ] || { echo "FAIL: marker is '$marker', want '$REPO'"; exit 1; }
[ -e "$REPO/graphify-out" ] && { echo "FAIL: graphify-out/ leaked at repo root"; exit 1; }
echo ok

echo "[2] query answers from the new location"
bash "$SH" query "$REPO" "what is graph.sh" | grep -q "\.pearde/graphify/graph.json" || { echo "FAIL: query did not report the new graph path"; exit 1; }
echo ok

echo "[3] extract (full, --force) leaves the vault + marker in place too"
bash "$SH" extract "$REPO" --force >/dev/null
test -d "$REPO/.pearde/graphify/obsidian" || { echo "FAIL: no obsidian vault under .pearde/graphify"; exit 1; }
marker="$(cat "$REPO/.pearde/graphify/.graphify_root")"
[ "$marker" = "$REPO" ] || { echo "FAIL: marker after extract is '$marker', want '$REPO'"; exit 1; }
[ -e "$REPO/graphify-out" ] && { echo "FAIL: graphify-out/ leaked at repo root after extract"; exit 1; }
echo ok

echo "ALL PASS"

# the harness carries its own verdict — a run with a failed check must
# not exit 0, or the proof cannot fail. every check above exits 1 on
# first failure, so reaching here means none failed.
fail=0
exit "$fail"
