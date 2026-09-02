# Index

| write | means | resolves to |
|---|---|---|
| `@<path>` | **one file** — the real path from the repo root with `@` in front | itself. Nothing to look up |
| `@@<keyword>` | **one scope** — everything you must read to understand a feature | its row in [Keywords](#keywords) |

`@@` names a row in this index, never a path on disk. No keyword is a directory.

Board paths (`.pearde/…`) are neither — they address a board, not this skill.

**A scope is what a feature is made of, not a reading list.** Read the one
file that answers the question in front of you: a row's first anchor. The
rest are where that file sends you. Opening a whole scope pays for the manual
again after every compaction, in the window the work needs.

**Where a file goes.** Markdown someone reads lives under `references/`.
Anything executed — a script, a tool, its config and its data — lives under
`resources/`, whole. A tool's own README ships inside the tool.

**Every skill is one file under `skills/`** — frontmatter deciding when it
fires, a body pointing into `references/` and stopping. The knowledge never
lives in the skill. What a skill *runs* lives under `resources/`, one folder
per skill that has one: @resources/board/, @resources/scout/,
@resources/graph/. `.pearde/wiki/` is data the tools read and write —
gitignored, not source, with its own Obsidian vault.

Installing turns each file into a folder of links elsewhere; nothing in the
repo moves. @references/install.md covers the whole of it and names no agent
— working out which directory to build in is the reader's job.

**Every tracked file has a row in @references/files.md** — the manifest,
split off so this map stays the size of the question it answers. Moving or
adding a file means writing its row there, then updating every
[Keywords](#keywords) row whose scope changed.

@resources/index.py reads both, the only reader of either format.

## Keywords

A file appears in every scope it belongs to. The first anchor in a row
explains the rest.

| keyword | is | read |
|---|---|---|
| `@@loop` | the pass, start to finish | @references/parts/loop.md · @references/parts/dispatch.md · @references/parts/pass.md · @references/parts/states.md · @references/parts/commits.md · @references/parts/progress.md · @references/parts/order.md · @references/parts/roles.md |
| `@@board` | what the scan walks and what it parses | @references/parts/board.md · @references/parts/pass.md · @resources/board/plan.py · @references/parts/contract.md · @references/parts/states.md · @references/templates/prd.md · @references/templates/vision.md · @references/settings.md · @resources/board/init.py · @references/archive.md |
| `@@states` | the nine states and what moves a PRD between them | @references/parts/states.md · @resources/board/transitions.py · @resources/board/specs.py · @references/parts/contract.md · @references/parts/commits.md |
| `@@order` | what runs next, and why no axis is a clock | @references/parts/order.md · @references/parts/derived.md · @resources/board/plan.py · @references/templates/vision.md |
| `@@workers` | dispatching a pass, an analyst or an implementer | @references/parts/workers.md · @references/parts/dispatch.md · @references/agents/pearde-pass.md · @references/agents/pearde-analyst.md · @references/agents/pearde-implementer.md · @resources/board/brief.py · @references/parts/roles.md · @references/parts/solo.md · @references/language.md |
| `@@specs` | one implementable unit, written and read | @references/templates/spec.md · @references/parts/workers.md · @references/parts/contract.md |
| `@@personas` | who works the **session**, and how one is chosen or made — the roster is @references/personas/INDEX.md, and a persona file is read only when it is worn | @references/parts/personas.md · @references/personas/INDEX.md · @references/parts/progress.md |
| `@@consult` | putting one problem to one persona, mid-pass | @references/parts/consult.md · @references/parts/workers.md · @resources/board/brief.py · @references/personas/INDEX.md |
| `@@derived` | work the board found, and its tripwire | @references/parts/derived.md · @references/parts/order.md · @references/templates/prd.md |
| `@@commits` | one PRD, one commit, on the transition that lands it | @references/parts/commits.md · @references/parts/states.md · @resources/board/orphans.py |
| `@@memos` | recording a decision and checking it | @references/skills/pearde-memo.md · @references/memo.md · @references/parts/memos.md · @references/templates/memo.md · @resources/memos.py |
| `@@workflows` | how a kind of job is done, and improved on every run | @references/skills/pearde-workflow.md · @references/workflow.md · @references/parts/workflows.md · @references/templates/workflow.md · @references/templates/atomic.md · @resources/workflows.py |
| `@@grammar` | what the words mean, and how a vocabulary grows | @references/skills/pearde-grammar.md · @references/grammar.md · @references/parts/grammar.md · @references/templates/grammar.md · @resources/grammar.py |
| `@@health` | which files resist being worked on — scored, worst first, named in the brief | @references/skills/pearde-health.md · @references/health.md · @references/parts/health.md · @references/templates/health.md · @resources/health.py |
| `@@report` | the board written for a person, one rolling state | @references/skills/pearde-report.md · @references/report.md · @references/templates/report.md · @references/parts/handles.md · @references/parts/loop.md |
| `@@drill` | asking until the request is a contract | @references/skills/pearde-drill.md · @references/drill.md · @references/templates/prd.md · @resources/questions.py · @references/parts/handles.md |
| `@@handles` | every command the board answers to | @references/parts/handles.md · @resources/pearde.py · @resources/board/transitions.py · @resources/board/brief.py · @resources/board/orphans.py · @references/parts/loop.md · @references/drill.md |
| `@@view` | the live view — service, plan, render, writers | @references/skills/pearde-view.md · @references/parts/view.md · @references/parts/all.md · @resources/board/serve.py · @resources/board/plan.py · @resources/board/render.py · @resources/board/view.css · @resources/board/view.js · @resources/board/all.py · @resources/board/lit-core.min.js · @resources/board/viewtest.js · @resources/board/hotreload-test.js · @resources/board/edit.py · @resources/board/adapters/claude.json |
| `@@pass` | what one session holds, and what survives a compaction | @references/parts/pass.md · @references/parts/dispatch.md · @references/parts/loop.md · @references/parts/guard.md · @resources/board/plan.py |
| `@@guard` | the loop's rules, enforced rather than written | @references/parts/guard.md · @resources/guard.py · @references/parts/loop.md · @references/install.md |
| `@@progress` | the line printed on every state change | @references/parts/progress.md · @references/parts/states.md |
| `@@statusline` | the numbers rendered continuously in the terminal | @references/parts/statusline.md · @resources/statusline.sh · @references/install.md |
| `@@install` | putting every skill where this agent finds it | @references/install.md · @SKILL.md · @resources/install.sh · @resources/pearde.py · @resources/guard.py · @references/system.md · @references/parts/doctor.md · @resources/doctor.sh |
| `@@skills` | the entry points, what each is a door to, and how one is named | @SKILL.md · @references/skills/pearde.md · @references/skills/pearde-drill.md · @references/skills/pearde-memo.md · @references/skills/pearde-view.md · @references/skills/pearde-report.md · @references/skills/pearde-master.md · @references/skills/pearde-doctor.md · @references/skills/pearde-update.md · @references/skills/pearde-persona.md · @references/skills/pearde-persona-ask.md · @references/skills/pearde-persona-create.md · @references/skills/pearde-scout.md · @references/skills/pearde-workflow.md · @references/skills/pearde-grammar.md · @references/skills/pearde-health.md · @references/skills/pearde-graph.md · @references/skills/pearde-knowledge.md · @references/skills/pearde-machine.md · @references/install.md |
| `@@doctor` | telling a broken install from an absent one | @references/skills/pearde-doctor.md · @references/parts/doctor.md · @resources/doctor.sh · @resources/guard.py · @resources/index.py · @resources/questions.py · @references/install.md |
| `@@update` | keeping every install of this repo current — the set of links, not the content | @references/skills/pearde-update.md · @references/update.md · @resources/update.sh · @resources/install.sh · @references/install.md |
| `@@master` | one plan across several repos | @references/skills/pearde-master.md · @references/parts/master.md · @references/settings.md · @references/parts/board.md |
| `@@all` | every watched board on one read-only page | @references/parts/all.md · @resources/board/all.py · @resources/board/serve.py · @resources/board/view.js · @references/parts/view.md · @references/parts/master.md |
| `@@machine` | every watched board as one ordered frontier, what could run at once, and the verb that runs it | @references/skills/pearde-all.md · @references/parts/machine.md · @resources/board/machine.py · @resources/board/dispatch.py · @resources/board/plan.py · @resources/board/serve.py · @references/parts/all.md · @references/settings.md |
| `@@settings` | every board-wide knob | @references/settings.md · @references/parts/contract.md · @resources/board/init.py |
| `@@language` | how everything on the board is written | @references/language.md · @resources/prose.py · @references/grammar.md · @references/templates/prd.md · @references/templates/spec.md · @references/templates/memo.md |
| `@@templates` | the files a handle writes from — each the shape only, its `.doc.md` the how and why | @references/templates/prd.md · @references/templates/prd.doc.md · @references/templates/spec.md · @references/templates/spec.doc.md · @references/templates/memo.md · @references/templates/memo.doc.md · @references/templates/report.md · @references/templates/report.doc.md · @references/templates/vision.md · @references/templates/vision.doc.md · @references/templates/atomic.md · @references/templates/atomic.doc.md · @references/templates/workflow.md · @references/templates/workflow.doc.md |
| `@@index` | addressing itself — the syntaxes, the scopes, the manifest, the check | @index.md · @references/files.md · @resources/index.py · @references/language.md |
| `@@scout` | the discovery tool, whole — stars, routes, findings | @references/skills/pearde-scout.md · @resources/scout/README.md · @resources/scout/scout.sh · @resources/scout/buckets.txt · @resources/scout/route.sh · @resources/scout/routes.md · @resources/scout/findings.md · @resources/scout/reading-list.md |
| `@@graph` | knowledge-graph passes — graphify, the ollama backend, the vault | @references/skills/pearde-graph.md · @references/graph.md · @resources/graph/graph.sh |
| `@@knowledge` | the research layer — sources, conclusions, links, dashboards | @references/skills/pearde-knowledge.md · @references/knowledge.md · @resources/knowledge.py · @resources/board/knowledge/ |

## Files

@references/files.md — every tracked file, one row. Read when a file is added
or moved, and by @resources/index.py — never to answer a question about the
work.
