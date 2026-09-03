# Files

One row per tracked file. @resources/index.py reads this against @index.md: a
file on disk with no row here is an incomplete map; a row naming nothing is a
map pointing nowhere.

Read this to add a file, move one, or chase a drifted index — never to answer
a question about the work, which @index.md's Keywords table does.

**Adding a file**: write its row here, then update every Keywords row in
@index.md whose scope changed.

## Entry points

| anchor | is |
|---|---|
| @SKILL.md | the installer — invocable before the skills are, retired once they exist |
| @README.md | the manual — board, states, loop, briefs, view |
| @index.md | the map — the `@` and `@@` syntaxes, and every scope |
| @.gitignore | what git leaves alone |

## `references/agents/` — dispatch

| file | what it is |
|------|------------|
| @references/agents/pearde-analyst.md | the analyst worker type — model and return contract |
| @references/agents/pearde-pass.md | the pass worker type — the window the loop runs in, and the four verdicts it hands back |
| @references/agents/pearde-implementer.md | the implementer worker type — model and return contract |

## `references/` — read

| anchor | is |
|---|---|
| @references/archive.md | how a finished PRD leaves `.pearde/prds/` — the flat `.pearde/prds/archive/` shape, and why `scan` already ignores it |
| @references/files.md | this manifest — every tracked file, one row |
| @references/language.md | how every document is written |
| @references/install.md | what the system is, and how to install it for any agent |
| @references/update.md | keeping an install current — what each `update` row means, and why `off` is never repaired unasked |
| @references/settings.md | board knobs |
| @references/memo.md | how a decision is recorded |
| @references/workflow.md | how a job is done — the two file shapes, the steps grammar, the report section |
| @references/grammar.md | what a word means here — the closed frontmatter set, the collision table, and what never earns a row |
| @references/health.md | how much a file resists being worked on — the six axes, the two knobs, the note and the ranking, the check |
| @references/report.md | the board written for a person |
| @references/drill.md | how to ask |
| @references/graph.md | the knowledge-graph feature — graphify passes, the ollama backend, the Obsidian vault |
| @references/knowledge.md | the research layer — sources, conclusions, the ask→capture→conclude loop, the tool behind it |
| @references/system.md | drop-in instructions block for `AGENTS.md` |
| @references/plugins.md | the curated plugin list — what to install alongside pearde, what not to, and why |
| @references/obsidian.md | the vault and its native access — REST + MCP from the same port, the two required plugins, how a pass uses them |

### `references/parts/` — the workflow, one part per step

| anchor | is |
|---|---|
| @references/parts/loop.md | the eight steps, in order |
| @references/parts/dispatch.md | the dispatcher — the session that holds nothing and starts passes |
| @references/parts/board.md | the layout the scan walks, and how the board's own directory is found whatever it is called |
| @references/parts/pass.md | `.pearde/.state/pass.md` — what the session holds, across a compaction |
| @references/parts/guard.md | the loop's rules as a hook that refuses the waste |
| @references/parts/contract.md | the frontmatter keys, and their defaults |
| @references/parts/states.md | the nine states, and what a tenth means |
| @references/parts/order.md | the three axes that pick what runs next |
| @references/parts/derived.md | work the board found, and its tripwire |
| @references/parts/roles.md | orchestrator, analyst, implementer, consultant |
| @references/parts/workers.md | the exact brief handed to each |
| @references/parts/solo.md | the same loop without parallel workers |
| @references/parts/personas.md | who works the session, and how one is picked |
| @references/parts/consult.md | putting one problem to one persona, mid-pass |
| @references/parts/commits.md | one PRD, one commit |
| @references/parts/memos.md | what was decided, and what it beat |
| @references/parts/workflows.md | the how, accumulated — the folder on one page |
| @references/parts/grammar.md | what the words mean, and how a vocabulary grows |
| @references/parts/health.md | which files resist being worked on, when they are scored, and what a worker owes one the brief names |
| @references/parts/progress.md | the line printed on every state change |
| @references/parts/statusline.md | the same numbers, continuously, for a person |
| @references/parts/handles.md | every command the board answers to |
| @references/parts/view.md | the live view at `127.0.0.1:8443` |
| @references/parts/doctor.md | broken install vs absent one |
| @references/parts/master.md | one plan across several repos |
| @references/parts/all.md | `all` — every board this machine watches on one read-only page; what it merges, what it deliberately leaves out, and how it differs from a master |
| @references/parts/run.md | `run` — the command that moves a board, a group or every watched board, and the `plan` that reads the same merged frontier without moving it; how a bare word resolves, the slot count and the reading behind it |
| @references/parts/ramp.md | loop step 0 — is this machine tooled for this repo, and the `happiness:` key that closes the question |

### `references/personas/` — who works

| anchor | is |
|---|---|
| @references/personas/INDEX.md | the roster, and how `persona create` builds a new one |
| @references/personas/engineer.md | Mara Vogt — the default, engineering generalist |
| @references/personas/designer.md | Ines Calder — product/design engineer |
| @references/personas/mentor.md | Tomas Berg — teaching engineer |
| @references/personas/skeptic.md | Nadia Ross — adversarial reviewer |

### `references/templates/` — what a handle writes from

A template is the shape and nothing else — it lands whole in every file written from it. `<name>.doc.md` beside it holds the how and the why, read on demand, never copied.

| anchor | is |
|---|---|
| @references/templates/prd.md | one PRD |
| @references/templates/spec.md | one implementable unit |
| @references/templates/memo.md | one decision record |
| @references/templates/atomic.md | one unit of work |
| @references/templates/workflow.md | one ordered route over atomics |
| @references/templates/grammar.md | one board's vocabulary, pearde's own already in it |
| @references/templates/health.md | one file's health note — the closed key set, the thresholds in its comments |
| @references/templates/report.md | the one rolling state, for a person |
| @references/templates/vision.md | one board's destination — the vision, its terminals, its edges |
| @references/templates/prd.doc.md | how to fill prd.md — every key, heading and rule the template no longer carries |
| @references/templates/spec.doc.md | how to fill specNN.md, and what `pearde specced` refuses |
| @references/templates/memo.doc.md | how to fill memo.md — the closed key set, the four sections |
| @references/templates/atomic.doc.md | how to fill atomic.md — the closed key set, the three sections |
| @references/templates/workflow.doc.md | how to fill workflow.md — the closed key set, the steps table's rules |
| @references/templates/report.doc.md | how to fill report.md — the opening, the three sections |
| @references/templates/vision.doc.md | how to fill vision.md — terminals, edges, the body |

## `resources/` — run

| anchor | is |
|---|---|
| @resources/pearde.py | the one command — a dispatcher over every script; discovers `COMMANDS` in `resources/board/*.py`; `help` from docstrings |
| @resources/install.sh | build one skill folder of links per file in `references/skills/` |
| @resources/update.sh | check every install on this machine and re-link the set — local, global, and the global that is not in force |
| @resources/doctor.sh | install check + repair |
| @resources/guard.py | the PreToolUse/PostToolUse hook that enforces the loop |
| @resources/statusline.sh | continuous progress numbers |
| @resources/memos.py | read + check memos — the only reader of that format |
| @resources/workflows.py | read + check the workflow library, and brief one — the only reader of that format |
| @resources/grammar.py | read + grow + check the board's vocabulary — the only reader of that format |
| @resources/health.py | score every tracked file 1-100, worst first, and check the record — the only reader of that format |
| @resources/index.py | read + check the map — the only reader of that format; `rows` and `scope_text` hand it to @resources/knowledge.py's `index` |
| @resources/prose.py | check density — word count, mean sentence length, unbound waste words, banned openers/closers, per file — the only reader of `## Density` |
| @resources/questions.py | read + check a PRD's question pass — the only reader of that format |
| @resources/invariants/ | one script per `kind: invariant` memo — what its `verify:` runs, named for its slug |
| @resources/invariants/every-artifact-lands-inside-the-board.sh | the tool writes nowhere but a board: no `.state/` outside a `.pearde/`, a driven throwaway project that stays clean, and the guard that still refuses a pass file written beside the board |
| @resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh | the vault's graph stays coloured: every `colorGroups` query in the preset is a `tag:` query, and every tag one names is carried by a note on the board — a group matching nothing draws grey and reports no error |
| @resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh | a footprint path inside a board that is its own git repo commits in the BOARD repo, never staged in the code repo that ignores it nor in the lane that is cut without it — asserted on three git repos and a worktree built at run time, with the flat layout that must not move; `COLLECT=` points the run at another copy of the module |
| @resources/invariants/a-master-need-is-the-union-of-its-members.sh | a master's `ramp need` is the union over `members:` to any depth, its own tree one member of it, the floor on the sum and a row crediting members — asserted on git repos built at run time, with the plain board that must not move |
| @resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh | the shared store still holds one copy: every surveyed worktree points at one store, no shared path is a real copy in two trees at once, no link is visible to `git status`, and no retired store key holds a second copy of an object — read off `share --json`, which `SHARE_JSON` can replace with a fixture survey |
| @resources/graph/graph.sh | graphify passes — extract, update, query, path, explain, god-nodes, vault open |
| @resources/knowledge.py | the research loop — query, enqueue, remember, conclude, relink, wiki, board, index, dashboard, doctor — over the board's `wiki/`; `index` writes one note per manifest row so a `@@<keyword>` is answerable from the dashboard |
| @resources/board/serve.py | the live service |
| @resources/board/plan.py | read + order the board |
| @resources/board/render.py | the page — markup, and the arithmetic behind it |
| @resources/board/view.css | the page's stylesheet, inlined at render |
| @resources/board/view.js | the page's script, inlined at render |
| @resources/board/viewtest.js | the view's gate — a rendered page in a real browser |
| @resources/board/hotreload-test.js | the view's hot-reload gate — one live page, a view source moved under it (`node hotreload-test.js <served-board-url>`) |
| @resources/board/adapters/claude.json | the Start button's default launch target — one JSON per adapter (`{"name","command","prompt"}`, optional `"plugins"` list of suggestions), read live by serve.py; doctor reports missing ones |
| @resources/board/lit-core.min.js | Lit 3, vendored — the page's component base |
| @resources/board/all.py | `all` — every watched board merged into one read-only page; no file of its own, the watch set is its whole configuration |
| @resources/board/run.py | `run` — the scope resolved (reserved, group, PRD) and dispatched; the same watch set merged into one dependency-ordered frontier, cut into waves by a load-derived slot count, and `read_main` is what `plan` prints |
| @resources/board/dispatch.py | the launcher `run` calls — that frontier run down to nothing: a rolling pool of pass workers, serialised on real-path footprint clashes, the claim gate re-asked per row, and a launch counted only once it has outlived the grace window |
| @resources/board/edit.py | the writers — one line at a time |
| @resources/board/collect.py | `collect` — verify, commit the footprint, `done`, one call |
| @resources/board/ramp.py | `ramp` — need, have, gap and the toolbox gate; proposes skills off scout's routes and installs none |
| @resources/board/orphans.py | `orphans` — every done PRD whose footprint never reached the branch that holds it; per-branch, never `git log --all`, reads only |
| @resources/board/brief.py | `brief` — a worker's or a consultant's brief, one command's output; the text is the marker blocks of workers.md, this fills them and holds no copy |
| @resources/board/transitions.py | the eight transition commands — the one writer of `state:` |
| @resources/board/lanes.py | one git worktree per worker — cut `lane/<slug>` on the claim, board dir sparse-checked out of it, rebase-then-ff-only so the lane's commit is the PRD's, drop the worktree on a sweep and keep the branch |
| @resources/board/session.py | `session take/list/reap/land/owns` — one git worktree per RUN SESSION, the layer above lanes, and the module every board command asks before it names a code repo: `instead_of` answers the session's tree, or the repo it was handed when no session holds one, so `collect.repo_of` and `plan.prd_repo` both end here. `<board>/.sessions/<id>` on `session/<id>`, a ledger at `<board>/.state/sessions.json` keyed on pid and start time, a reaper that commits everything a dead session left (untracked included) to `refs/pearde/reaped/<id>` before it removes the tree — alive and unknown are both never reaped — and `land`, rebase then fast-forward, putting the session's commits on the branch the checkout is on |
| @resources/board/refuse.py | `refuse tree/cmd` — `reset --hard`, `checkout --`, `clean`, a real `stash`, `restore` and `switch --discard-changes` refused in any tree the running session does not own; a tree is owned when the ledger's row for it is this session's, or when it is the worktree this process is itself working in and no other live session holds it; stdlib only and imports nothing from the planner, so @resources/guard.py can call it on every Bash tool call |
| @resources/board/shared.py | `share` — one copy per machine of what every lane regenerates, under the git common dir and symlinked into each worktree; only a path `git status` cannot see is ever linked, and a refusal puts the tree back as it was |
| @resources/board/specs.py | `specced` and `refine` — the two transitions a spec set decides |
| @resources/board/init.py | `init`, `settings` and `vault` — a board after one command, no question; one key of settings.md; seeds the Obsidian vault at the board (`.pearde/.obsidian/`, and `vault` registers it in Obsidian's `obsidian.json` so the URI resolves — written only while the app is closed, `--wait` holds for the quit — dataview + local-rest-api copied from the preset the install fetched, a bundle the install never fetched named rather than skipped, fresh REST key minted at `.pearde/wiki/.obsidian-api-key`) |
| @resources/board/example/ | the example board — eight PRDs, one per band; copied by `plan.py example`, never run in place |
| @resources/board/obsidian/ | the vault preset — `.obsidian` root files (app, graph colors, community/core plugin lists, appearance), every path in them `.pearde/`-relative and the two required plugins' settings; copied by `init` to any new board, an existing install wins. The plugin bundles (`main.js`, `manifest.json`, `styles.css`) are **not** in the repo: `install.sh` fetches them at pinned versions and `.gitignore` holds them out |

## `references/skills/` — one file per skill

Frontmatter, and a body that points into `references/`. One per feature: a
scope a person or an agent **invokes** gets a skill, a scope the loop **reads
mid-task** stays a reference reached through `@@`. The file name is the
command, and @references/install.md is the naming rule and the install.

| anchor | is | scope |
|---|---|---|
| @references/skills/pearde.md | the pass, and every handle that moves a PRD | `@@loop` |
| @references/skills/pearde-drill.md | asking until the request is a contract | `@@drill` |
| @references/skills/pearde-memo.md | recording a decision, and checking the record | `@@memos` |
| @references/skills/pearde-view.md | the timeline, the order, and editing through it | `@@view` |
| @references/skills/pearde-report.md | the board written for a person, one rolling state | `@@report` |
| @references/skills/pearde-master.md | one plan across several repositories | `@@master` |
| @references/skills/pearde-doctor.md | a broken install against an absent one | `@@doctor` |
| @references/skills/pearde-update.md | check every install and bring it current | `@@update` |
| @references/skills/pearde-persona.md | who is working, and switching for the pass | `@@personas` |
| @references/skills/pearde-persona-ask.md | one problem, one colleague, nothing written | `@@consult` |
| @references/skills/pearde-persona-create.md | composing one for a field the roster misses | `@@personas` |
| @references/skills/pearde-scout.md | ranked discovery, the route index, and the quality gates | `@@scout` |
| @references/skills/pearde-workflow.md | how a kind of job is done, and improved on every run | `@@workflows` |
| @references/skills/pearde-grammar.md | what a word means here, and how the vocabulary grows | `@@grammar` |
| @references/skills/pearde-health.md | which files resist being worked on, scored worst first | `@@health` |
| @references/skills/pearde-graph.md | knowledge-graph passes over any folder, Obsidian vault out | `@@graph` |
| @references/skills/pearde-knowledge.md | the research layer — query, capture, conclude, link | `@@knowledge` |
| @references/skills/pearde-all.md | every watched board as one ordered frontier, and what could run at once — and the waves that dispatch it | `@@run` |
| @references/skills/pearde-run.md | dispatch a board, a group or every watched board — the one command that moves, and how its bare word resolves | `@@run` |

### `resources/board/knowledge/` — the layer's content seed, planted by `init` and `upgrade`

Distinct from @resources/board/obsidian/, which is the `.obsidian` app config
(dataview + local-rest-api) `init.py`'s `write_obsidian` copies into
`<dir>/.obsidian` on every fresh board. This folder seeds a board's
`.pearde/wiki/` *content* — dashboard, workflow config, indexes. `init.py`'s
`write_knowledge` plants it: `init` on a new board, `upgrade` on an older one.
`knowledge.py`'s `Store` makes directories on first use but writes no
Dashboard and no WORKFLOW — without this seed a vault opens with no views.
Each file copies only where absent; an edited file is never replaced.

Every path inside is **vault-relative**, rooted at `.pearde/`: a query reads
`wiki/conclusions`, never `conclusions`, in `FROM` clauses and `dv.pages()`
calls alike.

| anchor | is |
|---|---|
| @resources/board/knowledge/ | the seed for a board's `.pearde/wiki/` — dashboard, workflow, indexes, the empty pending/graphs/absorbed scaffolds; planted by `init.py`'s `write_knowledge` |
| @resources/board/knowledge/Dashboard.md | the dashboard template — Dataview views, vault-relative |
| @resources/board/knowledge/WORKFLOW.md | the configuration template — focus, rules, routing |
| @resources/board/knowledge/conclusions/_index.md | the conclusions index, under conclusions/ |
| @resources/board/knowledge/sources/_index.md | the sources index template |
| @resources/board/knowledge/sources/.absorbed/_index.md | the absorbed-sources marker |
| @resources/board/knowledge/.graphifyignore | the extract-scope template |

### `.pearde/wiki/` — data, not source

One folder, gitignored, the layer's whole: notes, graph, wiki, and its own
Obsidian vault. No rows — the folder is machine-local output of
@resources/knowledge.py, seeded from the row above by `init` or `upgrade`.

### `resources/scout/` — a self-contained tool

Nothing outside it links in past `@@scout`. Its docs ship with it.

| anchor | is |
|---|---|
| @resources/scout/README.md | the scout manual — what @references/skills/pearde-scout.md is a door to |
| @resources/scout/scout.sh | sweep / delta / trending |
| @resources/scout/toolscout.sh | one-off dependency ranker |
| @resources/scout/route.sh | call one ranking page by id — reader of the route index |
| @resources/scout/routes.md | index one — every page a ranking comes from |
| @resources/scout/findings.md | index two — what won, on which axis, when |
| @resources/scout/buckets.txt | the taxonomy — the knob |
| @resources/scout/reading-list.md | the curated, mechanism-mapped list |
| @resources/scout/snapshots/ | the sweep's dated star counts, one row for the directory |
| @resources/scout/templates/_typos.toml | typos gate config |
| @resources/scout/templates/deny.toml | cargo-deny gate config |
| @resources/scout/templates/dependabot.yml | dependency updates |
| @resources/scout/templates/quality.yml | the quality gate workflow |
| @resources/scout/templates/scout.yml | the sweep in CI |
