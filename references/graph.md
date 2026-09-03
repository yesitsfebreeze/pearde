# Graph

The knowledge-graph feature, whole. One tool:
[graphify](https://github.com/Graphify-Labs/graphify), installed per machine,
driven through @resources/graph/graph.sh.

## What a pass writes, under `.pearde/graphify/`

| piece | is |
|---|---|
| `graph.json` | the persistent graph — nodes, typed edges, provenance (`EXTRACTED` / `INFERRED` / `AMBIGUOUS`) |
| `graph.html` | interactive — click nodes, search, filter by community |
| `obsidian/` | an Obsidian vault — one note per concept, wikilinks per edge |
| `GRAPH_REPORT.md` | god nodes, surprising connections, suggested questions |
| `cache/` | SHA256 cache — re-runs touch only changed files |

The folder sits inside whatever is mapped, `graph.sh` redirecting graphify's
default with `GRAPHIFY_OUT`, absolute on every call. Regenerable and
gitignored: data, not source.

## Code parses locally, prose goes to an ollama cloud model

Code takes a tree-sitter AST pass: deterministic, no LLM, nothing leaving the
machine. Docs, PDFs and images take a semantic pass through the backend, pinned
by the wrapper to `--backend ollama` and `--model glm-5.3-flash:cloud` — an
ollama cloud model on the local daemon, so that half leaves. Fully local:

```bash
PEARDE_GRAPH_MODEL=gpt-oss:20b graph.sh extract <folder>
```

`PEARDE_GRAPH_MODEL` overrides the model for one call, `PEARDE_GRAPH_FOLDER`
the default folder.

## Commands — folder first, optional, default the cwd

```bash
bash @resources/graph/graph.sh extract @.          # full: AST + semantic + clusters + vault
bash @resources/graph/graph.sh extract @. --force  # skip the incremental manifest gate and cache
bash @resources/graph/graph.sh update @.           # changed files only; code needs no LLM
bash @resources/graph/graph.sh query @. "what connects the board to the view?"
bash @resources/graph/graph.sh path @. "plan.py" "render.py"
bash @resources/graph/graph.sh explain @. "guard.py"
bash @resources/graph/graph.sh god-nodes @.
bash @resources/graph/graph.sh open @.             # .pearde/graphify/obsidian as a vault in Obsidian
```

Run from a pass, not for its own sake.

- **Extract is the only LLM call.** Update, query, path, explain, god-nodes
  read `graph.json` locally.
- **Cloud models answer through the local daemon.** `ollama list` names them:
  `glm-5.3-flash:cloud` and `deepseek-v4-flash:cloud` paired, `gpt-oss:20b` and
  `granite4:3b` local.
- **A mixed corpus needs the backend up.** Code-only work needs none; a failed
  semantic pass leaves the AST graph intact.

## The vault is output, separate from the board's

`.pearde/graphify/obsidian/` is its own vault, `.pearde/` being one already and
the board vault ignoring `graphify/`. `graph.sh open` opens it in Obsidian —
edit the corpus and re-extract, never a note.

## Relationship to the rest

- The `.pearde/wiki/` KB is the research layer's graph of conclusions,
  hand-built by @resources/knowledge.py; graphify's is the corpus map —
  different questions, different vaults.
- One commit per PRD holds @references/files.md and @index.md;
  `.pearde/graphify/` never enters one.
