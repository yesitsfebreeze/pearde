#!/bin/bash
# pearde graph — graphify passes over any folder, Obsidian vault out.
#
#   graph.sh extract [folder] [--force]   full extraction, clusters + Obsidian vault
#   graph.sh update [folder]              re-extract changed files only (AST, no LLM), vault rebuilt
#   graph.sh query [folder] "question"    BFS over graph.json, capped budget
#   graph.sh path [folder] "A" "B"        shortest path between two nodes
#   graph.sh explain [folder] "X"         one node and its neighbors, plain language
#   graph.sh god-nodes [folder]           most connected nodes
#   graph.sh open [folder]                open .pearde/graphify/obsidian as a vault
#
# The folder defaults to the PROJECT ROOT (the board's parent), never the cwd.
# Output lands in <folder>/.pearde/graphify/ — graphify's own default
# (graphify-out/ relative to cwd) is redirected there with GRAPHIFY_OUT, set
# absolute before every invocation so extract, update and every read command
# resolve to the same place with no --graph flag needed.
#
# Defaults come from here; PEARDE_GRAPH_MODEL / PEARDE_GRAPH_FOLDER override.
set -uo pipefail

# The skill root, resolved before any cd — `open` reads the one register
# writer, obsidian_register.py, out of resources/board/.
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

BACKEND=ollama
MODEL="${PEARDE_GRAPH_MODEL:-glm-5.3-flash:cloud}"

cmd="${1:-help}"; [ $# -gt 0 ] && shift

case "$cmd" in
  extract|update|query|path|explain|god-nodes|open)
    : ;;
  help|-h|--help|"")
    awk 'NR>1 && /^#/ {sub(/^# ?/,""); print; next} NR>1 {exit}' "$0"; exit 0 ;;
  *)
    echo "unknown command: $cmd (extract | update | query | path | explain | god-nodes | open)" >&2
    exit 2 ;;
esac

# Every dependency this command needs, named before any work starts — a pass
# that dies at the model call leaves a half-written graphify/ behind, and
# `open` failing after the vault is registered is a URI printed to no one.
# One line per missing piece, with the command that installs it; exit 2.
MISSING=()
case "$cmd" in
  extract)
    command -v graphify >/dev/null 2>&1 || MISSING+=("graphify — pip install graphify")
    if ! command -v ollama >/dev/null 2>&1; then
      MISSING+=("ollama — brew install ollama")
    elif ! LISTED=$(ollama list 2>/dev/null); then
      MISSING+=("the ollama daemon — ollama serve")
    elif ! printf '%s\n' "$LISTED" | awk '{print $1}' | grep -qx "$MODEL"; then
      MISSING+=("model $MODEL — ollama pull $MODEL")
    fi ;;
  update|query|path|explain|god-nodes)
    command -v graphify >/dev/null 2>&1 || MISSING+=("graphify — pip install graphify") ;;
  open)
    command -v python3 >/dev/null 2>&1 || MISSING+=("python3 — the vault register is written through obsidian_register.py")
    command -v open >/dev/null 2>&1 || command -v xdg-open >/dev/null 2>&1 \
      || MISSING+=("an opener — \`open\` (macOS) or \`xdg-open\` (Linux); the vault URI is printed instead") ;;
esac
if [ "${#MISSING[@]}" -gt 0 ]; then
  for m in "${MISSING[@]}"; do echo "graph $cmd: missing $m" >&2; done
  exit 2
fi

# The corpus is the PROJECT, never the board. Climb for the nearest board
# directory above the cwd and graph its parent, so a call made from inside
# `.pearde/` — a pass writing the round file, `graph.sh` typed in the vault —
# maps the repo and lands beside the board, not a second board one level
# deeper. `.pearde/.pearde/graphify` was the shape of that bug on disk.
# Falls back to the cwd where no board is above it: a bare folder graphed for
# its own sake still works, and an explicit folder argument still wins.
project_root() {
  local d="$PWD"
  while [ "$d" != "/" ]; do
    for n in .pearde pearde; do
      if [ -f "$d/$n/settings.md" ] || [ -d "$d/$n/prds" ]; then
        printf '%s\n' "$d"; return 0
      fi
    done
    d="$(dirname "$d")"
  done
  printf '%s\n' "$PWD"
}

# First positional arg that is a directory is the folder; the rest are args.
FOLDER="${PEARDE_GRAPH_FOLDER:-$(project_root)}"
ARGS=()
for a in "$@"; do
  if [ -d "$a" ] && [ "${#ARGS[@]}" -eq 0 ]; then FOLDER="$a"; else ARGS+=("$a"); fi
done

cd "$FOLDER" || exit 1
FOLDER_ABS="$(pwd)"

# Absolute, so extract/update's target-relative writes (a resolved scan root
# and the .graphify_root marker) land under the FOLDER being graphed, not
# wherever the shell happened to start. graphify honours an absolute
# GRAPHIFY_OUT as-is (paths.py); every subcommand below gets it, so the read
# commands' own default (<GRAPHIFY_OUT>/graph.json) already resolves here —
# --graph is passed too, defensively, matching the PRD's stated shape.
# `.pearde/` is the board, `pearde/` the legacy name a board that has not
# run `pearde upgrade` still carries — @references/parts/board.md is the order.
GRAPH_BOARD="$FOLDER_ABS/.pearde"
if [ ! -d "$GRAPH_BOARD" ] && [ -d "$FOLDER_ABS/pearde" ]; then
  GRAPH_BOARD="$FOLDER_ABS/pearde"
fi
export GRAPHIFY_OUT="$GRAPH_BOARD/graphify"
GRAPH_JSON="$GRAPHIFY_OUT/graph.json"

# The Obsidian vault is a product of a graph pass, not a separate command a
# person has to know to run: the pearde-graph skill describes
# .pearde/graphify/obsidian/ as an output of extraction, and `graph.sh open`
# opens it. graphify writes it ONLY from `export obsidian` — its `extract`
# has no obsidian step at all — so every pass that rebuilds graph.json ends
# here. Pure graph.json -> notes: no LLM call, no network. One function, so
# extract and update cannot drift apart.
export_vault() {
  # Export into an EMPTY directory. graphify refuses to overwrite notes it
  # did not itself create, so exporting over a previous vault silently skips
  # every colliding note — 16 of 1311 on this repo (Drill.md, PRD.md,
  # Settings.md, the templates...) — and warns instead of failing, leaving a
  # vault that is quietly short. Its own advice is to export into an empty
  # directory. The vault is pure output (references/graph.md: "edit nothing
  # in it, edit the corpus and re-extract instead") and graphify writes even
  # its .obsidian/ config, so nothing of anyone's is lost by clearing it.
  [ -n "${GRAPHIFY_OUT:-}" ] || { echo "export_vault: GRAPHIFY_OUT unset" >&2; return 1; }
  rm -rf "$GRAPHIFY_OUT/obsidian"
  graphify export obsidian --graph "$GRAPH_JSON"
}

case "$cmd" in
  extract)
    graphify extract "$FOLDER_ABS" --backend "$BACKEND" --model "$MODEL" --max-concurrency 1 ${ARGS[@]:-} \
      && export_vault
    ;;
  update)
    # Pass the resolved absolute path, not ".": update never writes the
    # .graphify_root marker (only extract does, cli.py, and both its writes
    # resolve) — it only READS it, to recover a scan root when no path
    # argument is given. Naming the folder absolutely keeps the scan root
    # _rebuild_code relativizes against independent of the caller's cwd.
    graphify update "$FOLDER_ABS" \
      && export_vault
    ;;
  query)
    graphify query "${ARGS[0]}" --graph "$GRAPH_JSON" ${ARGS[@]:1}
    ;;
  path)
    graphify path "${ARGS[0]}" "${ARGS[1]}" --graph "$GRAPH_JSON"
    ;;
  explain)
    graphify explain "${ARGS[0]}" --graph "$GRAPH_JSON"
    ;;
  god-nodes)
    graphify god-nodes --graph "$GRAPH_JSON"
    ;;
  open)
    # `obsidian://open?path=` only resolves a vault Obsidian has registered —
    # an unregistered folder opens its nearest registered ancestor instead
    # (the board's own vault, which is not this one). So the graph vault is
    # registered by exact path first, through the one register writer
    # (@resources/board/obsidian_register.py), and the URI names it by id.
    # Obsidian rewrites its register on quit: a registration made while the
    # app runs is certain after a restart, which is why this one passes
    # `even_if_running` — the alternative is no link at all until the user
    # quits an app they did not open for this.
    VAULT_URI=$(python3 -c "
import os, sys, urllib.parse
sys.path.insert(0, os.path.join('$SKILL_DIR', 'resources', 'board'))
vault = os.path.abspath(os.path.join('$GRAPHIFY_OUT', 'obsidian'))
try:
    import obsidian_register as obsreg
    _, vid = obsreg.write(vault, even_if_running=True)
except Exception:
    vid = None
print('obsidian://open?vault=' + vid if vid
      else 'obsidian://open?path=' + urllib.parse.quote(vault))
")
    if command -v open >/dev/null 2>&1; then open "$VAULT_URI"
    elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$VAULT_URI"
    else echo "$VAULT_URI"
    fi
    ;;
esac