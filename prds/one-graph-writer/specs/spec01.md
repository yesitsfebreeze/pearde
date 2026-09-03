---
complexity: 14
workflow: probe-then-spec
footprint:
  - resources/knowledge.py
---

# spec01 — `relink` merges the KB graph into the repo's own `graph.json`, root by root

Two writers, two files, two schemas today: `graph.sh extract`/`update`
(graphify, external) writes the repo's own scan to
`.pearde/graphify/graph.json` (networkx node-link shape — `nodes`/`links`,
`source_file`, `relation`); `knowledge.py relink` writes the KB's own scan to
a sibling file, `.pearde/wiki/.graphify/graph.json` (`nodes`/`edges`,
`from`/`to`/`type`). This unit makes `relink` the second writer of the *same*
file instead of the sole writer of a second one.

**All of it already stands in the tree, uncommitted.** The implementer's job
is to read it, run the probe, and tick each box against what it printed.

## What already stands

- `Store.__init__` (`resources/knowledge.py:83-100`) — `self.graphify` and
  `self.graph_json` now resolve to `<board>/graphify/graph.json` (`self.root`
  is `<board>/wiki`, so `self.root.parent` is the board — the same path
  `health.py`'s `load_graph` already reads), not
  `<board>/wiki/.graphify/graph.json`. `self.old_graph_json` names the
  pre-fix sibling path so `cmd_relink` can retire it.
- `build_graph` — every KB node it returns now carries `"root": "kb"`.
- `_load_repo_graph(path)` — reads the existing `graphify/graph.json`
  (graphify's native shape) or returns an empty skeleton of the same shape
  when `graph.sh extract` has never run, so `relink` always has somewhere to
  write even on a board with no code scan yet.
- `merge_kb_into_repo_graph(repo_graph, kb_nodes, kb_edges)` — repo
  nodes/links already on disk are kept (tagged `root: repo` if untagged,
  never otherwise altered); the KB's own nodes/links from the *current* run
  replace whichever KB-tagged ones were there before (so a second `relink`
  does not accumulate); KB edges are translated `from/to/type` →
  `source/target/relation` so both sides are typed the same way; the union is
  keyed by `(source, relation, target)`, so a link recorded by both roots is
  never doubled.
- `cmd_relink` — calls the above, writes the one merged file, and deletes the
  pre-fix sibling directory if a board still carries one. `cmd_doctor`'s graph
  staleness check now compares KB note stems only against nodes tagged
  `root: kb` — before this fix it compared every KB note against every node
  in the file, and once the file also holds the repo's few-thousand code
  nodes that comparison never matches, which would have made every board
  report "graph.json is behind the files" permanently the moment the merge
  landed. This was found only by running `doctor` against the merged file
  during the probe, not read off the contract.

## What is left to finish

Nothing to build. `graph.sh` needed no change: it already writes to
`<board>/graphify/graph.json`, which is now also `relink`'s target, so a
`relink` run after an `extract` merges onto whatever `extract` just wrote.

- `cmd_wiki` (`graphs/`) and `cmd_dashboard` still call `build_graph(store)`
  directly and render the KB layer only — they were never reading the repo's
  nodes and do not need to for the PRD's own `## Done when` boxes, none of
  which name either command. Widening them to read repo nodes as well is a
  separate contract, not folded in here.

## Acceptance

- [ ] `relink` on a board that already holds a `graphify/graph.json` (as if
      `graph.sh extract` had just run) writes the KB's nodes and edges into
      that same file, tagged `root: kb`, and the pre-existing nodes/links are
      still there, tagged `root: repo` — no second `graph.json` exists under
      the board afterward.
- [ ] The repo edges that were on disk before `relink` ran are still on disk
      after, field for field (`source`, `target`, `relation`, and whatever
      else graphify wrote), with only `root: repo` added — proved by
      comparing the pre-relink file to the post-relink one.
- [ ] A second `relink` run does not double the KB nodes or the KB edges, and
      does not touch the repo edge count.
- [ ] Simulating a fresh `graph.sh extract` (a new native file with an extra
      repo node/edge and a new `built_at_commit`) between two `relink` runs
      carries the new repo edges through on the next `relink` — the merge
      survives an extract in between, not just a bare re-run.
- [ ] `doctor` on the merged board reports no false "graph.json is behind the
      files" — the KB-vs-node comparison is scoped to `root: kb` nodes only.
- [ ] `python3 -m py_compile resources/knowledge.py` — compiles.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 -m py_compile resources/knowledge.py && echo "knowledge.py compiles"
bash .pearde/prds/one-graph-writer/probe/verify_knowledge.sh
```
