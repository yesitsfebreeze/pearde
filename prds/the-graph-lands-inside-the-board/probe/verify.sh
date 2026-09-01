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
#
# Affordability (graph-probe-makes-harness-sweep-unaffordable, 2026-09-01):
# step [3] used to run `extract "$REPO" --force` — a full semantic pass, LLM
# per doc chunk, unbounded (10+ min observed, then killed mid-flight), inside
# doctor's --harnesses sweep whose wall-clock design is "the slowest harness".
# The location contract extract must prove does not need the LLM: extract's
# output placement (GRAPHIFY_OUT honored, marker resolved, no graphify-out
# leak, vault emitted) is identical for a code-only corpus, which dispatches
# zero LLM chunks. So extract now runs on a run-time fixture holding one
# small Python file — 0 docs, 0 papers, 0 images — and the sweep pays seconds,
# not minutes. The real repo's own graph is never rebuilt by a full extract.
set -u
REPO=/Users/feb/dev/infra/pearde
SH="$REPO/resources/graph/graph.sh"

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf '  ok   %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf '  FAIL %s\n' "$1"; }

FIX=$(mktemp -d "${TMPDIR:-/tmp}/graphprobe.XXXXXX")
trap 'rm -rf "$FIX"' EXIT
mkdir -p "$FIX/src"
printf 'def add(a, b):\n    return a + b\n\nclass Calculator:\n    def total(self, xs):\n        return sum(add(x, 0) for x in xs)\n' > "$FIX/src/calc.py"

echo "[1] update, then check output location + marker"
if bash "$SH" update "$REPO" --force >/dev/null; then
  ok "update runs clean and fast (AST, no LLM)"
else
  bad "update exited non-zero"
fi
if [ -f "$REPO/.pearde/graphify/graph.json" ]; then
  ok "graph.json under .pearde/graphify"
else
  bad "no graph.json under .pearde/graphify"
fi
marker="$(cat "$REPO/.pearde/graphify/.graphify_root" 2>/dev/null)"
if [ "$marker" = "$REPO" ]; then
  ok "update's marker is the repo root"
else
  bad "marker is '$marker', want '$REPO'"
fi
if [ ! -e "$REPO/graphify-out" ]; then
  ok "no graphify-out/ leak at repo root"
else
  bad "graphify-out/ leaked at repo root"
fi

echo "[2] query answers from the new location"
if bash "$SH" query "$REPO" "what is graph.sh" | grep -q "\.pearde/graphify/graph.json"; then
  ok "query reports the graph at .pearde/graphify/graph.json"
else
  bad "query did not report the new graph path"
fi

echo "[3] extract lands vault + marker in place too — on a code-only fixture"
if bash "$SH" extract "$FIX" >/dev/null; then
  ok "extract runs clean on a 0-doc corpus (no LLM dispatched)"
else
  bad "extract exited non-zero on the fixture"
fi
if [ -f "$FIX/.pearde/graphify/graph.json" ]; then
  ok "extract writes graph.json under the folder's .pearde/graphify/"
else
  bad "no graph.json under the fixture's .pearde/graphify/"
fi
if [ -d "$FIX/.pearde/graphify/obsidian" ]; then
  ok "extract emits the obsidian vault"
else
  bad "no obsidian vault under the fixture's .pearde/graphify/"
fi
marker="$(cat "$FIX/.pearde/graphify/.graphify_root" 2>/dev/null)"
if [ "$marker" = "$FIX" ] || [ "$marker" = "$(cd "$FIX" && pwd -P)" ]; then
  ok "extract's marker resolves to the folder (never '.')"
else
  bad "extract marker is '$marker', want the fixture root"
fi
if [ ! -e "$FIX/graphify-out" ]; then
  ok "no graphify-out/ leak in the fixture"
else
  bad "graphify-out/ leaked in the fixture"
fi

# The line below reports checks executed, not checks expected: drop one to a
# stray `continue` or a quoting slip and it prints a smaller total and exits 0,
# which is indistinguishable from success. Pin the denominator.
[ "$((PASS+FAIL))" = 10 ] || { FAIL=$((FAIL+1)); printf '  FAIL expected 10 checks, ran %s\n' "$((PASS+FAIL))"; }
echo
echo "$((PASS+FAIL)) checks · $PASS pass · $FAIL fail"
[ "$FAIL" = 0 ]