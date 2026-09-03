Verdict: SPECCED

workflow: probe-then-spec

## What the build found

The docs page this PRD files (`docs/content/docs/improvements/knowledge-one-graph.mdx`,
still on disk, recovered nothing from git) names two writers of one question
("what links to what"): `graph.sh extract`/`update` (graphify, external tool)
writes the repo's own scan to `.pearde/graphify/graph.json` (networkx
node-link shape: `nodes`/`links`, `source_file`, `relation`); `knowledge.py
relink` writes the KB's own scan to a sibling file,
`.pearde/wiki/.graphify/graph.json` (`nodes`/`edges`, `from`/`to`/`type`).
`health.py`'s `load_graph` already reads `<board>/graphify/graph.json` — the
repo file — which is the natural single location: it is the one an external
tool writes on its own schedule, so `relink` becomes its second writer rather
than the reverse. The PRD's own text names the wiki path as the one "gaining"
the `root:` field; reading the actual code shows that claim is imprecise
(likely predating the recent board-directory rename in this repo's own
history) — the two-file, two-schema problem the PRD describes is real and
verified by reading both writers, but the specific path it names is not where
the merge naturally lands. Noted here as a finding, not carried into a spec
verbatim.

The build implemented, in the lane, and proved with a probe against a scratch
board (never the live one — this board is under heavy concurrent PRD
activity, `.pearde/graphify/.rebuild.lock` was held throughout):

- `resources/knowledge.py`: `Store`'s `graph_json` now points at
  `<board>/graphify/graph.json`; `build_graph` tags every KB node
  `root: kb`; a new `merge_kb_into_repo_graph` unions repo and KB
  nodes/links (repo tagged `root: repo` if untagged, KB edges translated
  `from/to/type` → `source/target/relation`), keyed by
  `(source, relation, target)` so a link recorded by both roots is never
  doubled; `cmd_relink` writes the merge back to the one file and retires the
  pre-fix sibling; `cmd_doctor`'s staleness check was fixed to compare KB
  note stems against `root: kb` nodes only — **found only by running
  `doctor` against the merged file**: before that fix, every board would
  have reported "graph.json is behind the files" permanently, since the
  merged file also holds the repo's few-thousand code nodes that no KB note
  stem ever matches.
- `resources/health.py`: `load_graph` drops `root: kb` nodes/links before
  they reach `file_of` or the returned link list; the "built from another
  root?" wording is gone (the file now says its own root, so a low match is
  named staleness, not identity doubt).
- `resources/graph/graph.sh` needed no change — it already targets
  `<board>/graphify/graph.json`.

Both specs' `## Verify and Proof` blocks were run verbatim from this
checkout: red before the two files carry the build (proved on the live
tree), green once they do (proved by copying the lane's two files over the
checkout's, running the blocks, then restoring the checkout — `git diff
--stat` empty afterward). Targeted harnesses that read either footprint file
(`files-score-their-health-and-the-brief-names-the-unhealthy`,
`the-graph-lands-inside-the-board`) were re-run under `PEARDE_ROOT=<lane>`
and matched their pre-build baselines (36/37 and 10/10 respectively, the one
`I3` failure pre-existing and unrelated). `python3 resources/index.py check`
is unaffected — no file was added, removed or renamed.

## Findings (not specced)

- The PRD's own text names `.pearde/wiki/.graphify/graph.json` as the file
  gaining the `root:` field; the actual merge target is
  `.pearde/graphify/graph.json` (see above) — a wrong claim in the source
  page, not a decision this build made freely.
- `cmd_wiki` (`graphs/`) and `cmd_dashboard` still call `build_graph(store)`
  directly and render the KB layer only, untouched by this merge — the PRD's
  `## Done when` boxes never test either, so widening them to also read the
  repo's nodes is left alone rather than folded in.
- `the-graph-lands-inside-the-board`'s probe flaked once under concurrent
  board activity (a `.graphify_root` marker check, unrelated to either
  footprint file) and passed clean on immediate re-run with no code touched
  in between — a scheduling artefact of the shared live `.pearde/graphify`
  directory, not this build's.

## Scores

complexity: 28
blast-radius: mid
workflow: probe-then-spec
