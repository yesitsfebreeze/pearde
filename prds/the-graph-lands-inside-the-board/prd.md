---
state: open        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 60        # higher first
complexity: 0      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual:          # a record. Nothing reads it
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
---
<!-- Ordering reads three axes and no clock: dependency (needs + footprint),
     vision importance (priority), and complexity/blast-radius. Add your own
     keys freely, at any nesting. Nothing outside state, origin, from,
     priority, complexity, blast-radius, claim, repo, workflow, needs and
     footprint is read, and nothing you add is ever dropped.
       needs:     — PRD dir names this one depends on. A hard gate in `plan`
       footprint: — paths this PRD touches. The overlap check
       workflow:  — the route a worker is handed, expanded into its brief

     One sitting is the limit: specs summing `complexity` above `split-above`
     or counting above `specs-above` (both in prds/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# the graph lands inside the board

The knowledge graph's output lives at `.pearde/graphify/`. Nothing named
`graphify-out` sits at the repository root any more, and every graph command
in `resources/graph/graph.sh` reads and writes the new location.

The board's own directory is `.pearde/`, holding `prds/`, `memos/`, `wiki/`,
`workflows/` and `.state/`. The graph is board state like the rest of it and
belongs in there, as `.pearde/graphify/`. Today it is `graphify-out/` at the
repository root, which is the graphify tool's own default and not a name this
project chose.

The constraint that shapes the work: `graphify extract` and `graphify update`
have no output flag and no environment variable for the output directory —
they write `graphify-out/` relative to the current working directory, always.
Only the read commands are addressable: `query`, `path`, `explain`,
`affected`, `god-nodes` and `cluster-only` each take `--graph <path>`.

That leaves two shapes, and choosing between them is part of this work:

  - extract into the tool's default and move the directory to
    `.pearde/graphify/` as the last step of extract and update, with every
    read command passed `--graph .pearde/graphify/graph.json`; or
  - keep a gitignored symlink at the repository root pointing into
    `.pearde/graphify/`, so the tool's hardcoded path resolves there and no
    command needs a flag.

Whichever is chosen, one detail must be handled deliberately: graphify writes
a `.graphify_root` marker inside its output directory and treats it as the
authoritative repository root, falling back to a grandparent heuristic
(`<root>/graphify-out/graph.json` -> `<root>`) when it is missing. That
heuristic is wrong for `.pearde/graphify/`, and `build.py` says its pruning is
the part that suffers. The marker must exist and must name this repository's
root, or graph rebuilds will prune against the wrong tree.

Done when a full extract and an update both leave their output at
`.pearde/graphify/` with a correct `.graphify_root`, `graph.sh open` opens the
vault from the new path, `graph.sh query` answers from it, and the repository
root holds no `graphify-out` directory.

Also update what names the old path: `.gitignore`, `references/graph.md`,
`skills/pearde-graph.md`, `resources/board/obsidian/app.json` and
`resources/board/obsidian/graph.json`.

Not in scope: patching or forking graphify itself, and any change to what the
graph contains.

Pointers: `resources/graph/graph.sh`, `references/graph.md`,
`skills/pearde-graph.md`, `resources/knowledge.py`, and graphify's own
`build.py` for the root marker and the prune path.

<!-- Three more headings exist, and none of them is a slot to copy down. Each
     is a claim about the state of this PRD, so an empty copy of it is a false
     one: an empty `## Questions` stops the board on nothing, an empty
     `## Answers` reads as answered, an empty `## Failure` reads as a failed
     attempt. Write the heading when it has content; until then it is absent,
     which is the honest state. @resources/questions.py reports the empty
     ones, and `doctor`'s `questions` row runs it. -->

<!-- `## Questions` — analyst-only, when blocked on the user: one round in the
     format of drill.md — `### Q1: <title>`, the fork in two sentences ending
     in "?", then exactly three prepared answers, each a complete decision,
     one `(recommended)`. Only real forks the user must settle (naming, scope,
     cost) — never facts a worker could look up, never the PRD restated. A PRD
     parked on the user with no such round never says what it is asking.
     Written in plain words for the person who asked, never for the board — no
     backtick, no path, no PRD name, no board word, 60 words in the fork and 25
     in an answer: the table in @references/drill.md is the whole rule, and
     @resources/questions.py refuses a round that breaks it. -->

<!-- `## Answers` — orchestrator-only (or the view), written after asking the
     user: `**Q1** — <the picked answer verbatim, or the user's own words>`,
     numbers matching the round above it. Analysts read these before speccing.
     An `## Answers` with no `## Questions` above it answers nothing. -->

<!-- `## Failure` — implementer-only, after a FAILED attempt: what broke, what
     was tried. `retry` moves this into the body as history and reopens the
     PRD. -->
