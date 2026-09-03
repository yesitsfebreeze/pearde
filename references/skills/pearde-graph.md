---
name: pearde-graph
description: Knowledge-graph passes over this repo or any folder via graphify on local Ollama — code AST plus concept extraction, a queryable graph.json, graph.html and an Obsidian vault under .pearde/graphify/. Use for "/pearde-graph", "graph the repo", "graphify extract", "query the knowledge graph", "what connects X to Y", "god nodes", "explain node X", "open the graph vault", "update the graph".
---

Read @references/graph.md. The scope is `@@graph`. The tool runs through
@resources/graph/graph.sh — never invoke `graphify` by hand for a pass, since
the wrapper holds the backend and model choices.
