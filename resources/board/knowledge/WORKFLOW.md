---
type: workflow
active_focus: []
priority_tags: []
research_depth: default
auto_enqueue: true
min_sources_per_conclusion: 2
default_workflow: default
---

# Knowledge workflow — the loop's configuration

Read on every invocation: frontmatter, then `## Focus`, then `## Rules`.

## Focus

Topics, tags or folders the loop attends to. Empty means no filter; set,
`query` prefers the matching nodes.

- (add focus areas here)

## Rules

- Link every source to its conclusion with `[[wikilinks]]`.
- A conclusion saves only on `min_sources_per_conclusion` sources or more.
- Never enqueue a duplicate — `pending/` already holds it.
- `auto_enqueue: false` returns the gap and writes no pending file.
- Skip domains: (list domains to exclude)

## Workflows

### default

Query → gap → enqueue → research → learn.

1. `query` against the KB
2. Gap → `enqueue` with context, or call `graphify extract` directly
3. `graphify extract` fetches sources for the topic and calls `graphify update` to absorb them
4. `graphify update` alone drains anything still pending, with no new fetches

### deep-dive

Performance, architecture, hard problems — more sources, deeper synthesis.

1. `query`, expanding the `related` graph one hop
2. `web-research`, five sources minimum
3. Synthesize, save the conclusion with `depth: deep` frontmatter
4. `relink` to cross-reference siblings

### triage

Only pending at `priority: high`; every other gap waits.

1. List pending sorted by priority
2. Process `high` only
3. Defer the rest

### crystalize

Absorb redundant sources into the mature conclusion already carrying the
canonical takeaway. The files move to the hidden `sources/.absorbed/`, and
the conclusion records them under `derived_from:`.

1. Identify the mature conclusion and the redundant sources
2. `crystalize conclusion=<slug> absorb=[<source-slugs>] dry_run=true` — preview
3. `crystalize` without `dry_run` — moves the files, updates `derived_from:`
4. `graphify update` — rebuild the graph

Restore: move the file back from `.absorbed/` and edit the frontmatter.
`graphify query` carries the full contract.

## Routing

Question pattern → workflow. First match wins.

| pattern             | workflow   |
| ------------------- | ---------- |
| `/perf|gpu|render/` | deep-dive  |
| `/quick|lookup/`    | default    |
| `/urgent|blocker/`  | triage     |
| (default)           | default    |
