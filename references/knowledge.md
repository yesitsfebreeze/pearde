# Knowledge

The research layer: what the board learned outside the repo, as linked notes
with provenance. The board holds process and decisions, knowledge the
conclusions and their sources — one home per question, a decision going to a
memo per @references/memo.md, a conclusion here.

```
.pearde/wiki/          one folder, the whole layer — the wiki and its graph
    sources/             external findings, one file per topic; raw, arguing nothing of ours
    conclusions/         synthesized answers, each derived from named sources
    pending/             research questions queued, priority-tagged, not yet run
    graphs/              generated wiki pages over the KB
    .graphify/           the note graph, graph.json (gitignored, regenerable)
    WORKFLOW.md          focus, rules, routing — the configuration every verb reads
    Dashboard.md         live Dataview views over all of it
```

The board's vault roots at `.pearde/` (@references/obsidian.md): the dashboard
renders at `wiki/Dashboard.md`, every Dataview source `.pearde/`-relative —
`wiki/conclusions`, not `conclusions`. @resources/knowledge.py runs the loop:
stdlib-only Python, `--root` per board.

## The loop — ask, gap, capture, conclude, link

| step | verb | decides |
|---|---|---|
| ask | `knowledge.py query "<question>"` | whether an answer is on record |
| gap | prints `gap:` when nothing strong hits | `enqueue` it (auto) or research now |
| capture | `remember <title>` — body on stdin, one topic per file | the finding, and the sweep or page behind it (`--provenance`) |
| conclude | `conclude <title> --sources <slug,…>` | whether ≥ `min_sources_per_conclusion` takeaways agree enough to synthesize |
| link | `relink` | the note graph, symmetrized `related:`, `graphs/` communities via `wiki` |

| rule | mechanism |
|---|---|
| a source states, a conclusion argues | findings plus the route id or URL behind them (`--provenance`); a conclusion's `sources:` names every file it derived from — under two, refused as a hunch |
| wikilinks hold the graph together | `[[their-slug]]`, conclusion to source or conclusion; `relink` resolves them, symmetrizes `related:`, writes `.pearde/wiki/.graphify/graph.json`. A note id like `260831-cbe9` or its title resolves — hand-built, no LLM pass, no backend key, no orphans |
| scout is the tap | a sweep finds, the ranking pages raw material per @@scout. Distill winners into `sources/` notes tagged by bucket and route id, then `conclude` once a job's answer is stable |
| pending is not a backlog | a question never needed again is deleted, not drained to zero; stale rows read as work owed, `doctor` naming them |
| the vault is output | hand edits to `graphs/` die on the next `wiki`, `Dashboard.report.md` on the next `dashboard --write` |
| `doctor` closes the loop | frontmatter valid, wikilinks resolving, graph in sync, pending honest — after moves, before calling a KB fact settled |

## The verbs write only under `.pearde/wiki/`

Gitignored, machine-local, defaulting to the tool's repo. The scope is
`@@knowledge`, its door @references/skills/pearde-knowledge.md. `WORKFLOW.md`
is the configuration, re-read every call: `active_focus` biases `query`,
`min_sources_per_conclusion` guards `conclude`, `auto_enqueue` queues a gap.

## Relationship to the rest

| the other | how they meet |
|---|---|
| memos | a memo wikilinks `[[<conclusion>]]` where a decision rests on knowledge, the conclusion links back; neither moves a state |
| scout | `@resources/scout/findings.md` holds a sweep's dated record, never copied here — the note is the takeaway, the sweep the citation |
| `@@graph` | `@resources/graph/graph.sh extract` maps the repo, semantic passes included; `knowledge.py relink` maps the KB from `.pearde/wiki/` wikilinks — hand-built, never an LLM call |
| the dashboard | the view a person opens; a pass queries through the tools, never by reading `Dashboard.md` |
