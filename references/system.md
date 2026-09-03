<!-- pearde:begin — <PEARDE>/references/system.md -->
## Pearde

The board is `.pearde/`; the skill is `<PEARDE>`, absolute, written in at
install. Every `@<path>` resolves there, never in this repo.

On "pearde", "work the board", "run the prds", or "pearde status": read
`<PEARDE>/README.md` and follow it exactly.

`@<path>` is one file, `@@<keyword>` a scope in `@index.md`. Read the file
answering the question in front of you — `@README.md` names it — then follow
where it sends you. A scope is what a feature is made of, not a reading list.

| topic | rule |
|---|---|
| The pass — `@@loop` | scan, answer, refine, spec ahead, implement, collect, drill-then-stop. Nothing dispatchable means the board is blocked on a person: drill the whole open frontier in one pass, per `@@drill`, never a report of what is stuck. `@@board` is the scan's reach, `@@states` a state's meaning and who sets it |
| Settings — `.pearde/settings.md` | `language`, `workers`, `pipeline`. Read before the pass, write when the user changes one. Missing means first run: `pearde init`, English by default, said on its first line; `pearde settings language=<l>` changes it |
| Who works — `@@personas` | one per session, one id, stored nowhere: `engineer` until switched, carried on the pass's line. A candidate governing the pass: ask once, recommend it, wear the answer — never switch silently. The user naming one is no question. A worker's persona comes from its own job in `@@workers` and moves nothing |
| Calling one — `@@consult` | put one problem to a persona you are not wearing, mid-pass, on your own judgment, without asking. Talk, then relay what it said, attributed. The colleague writes nothing, your persona holds. Call the `skeptic` before `done` on work you implemented. `ask <id> <question>` is the user doing the same |
| Writing — `@@language` | PRDs, specs and reports go in the board `language` |
| Asking — `@@drill` | one pass, the whole frontier, each question carrying your recommended answer |
| Following — `@@workflows` | a recurring job is a `workflow`: an ordered route of atomics, named by `workflow:` on a PRD or spec and handed to the worker expanded. A run returns its edits; only the orchestrator writes the library, only from a run |
| Deciding — `@@memos` | a call the code will not explain goes in `.pearde/memos/<slug>.md`, never in a PRD |
| Dispatching — `@@workers` | the analyst and implementer briefs, verbatim, and the single-agent mode |
| Not wired up? | `@@install` is what installed means; `@@doctor` tells broken from absent |

Handles: `status`, `once`, `add <title>`, `drill <prd>`, `retry <prd>`,
`unblock <prd>`, `sweep`, `collect`, `run <prd>`, `memo <subject>`,
`workflow [<slug>]`, `plan`, `view`, `persona [<id>]`,
`persona create <topic>`, `workers=N`, `pipeline=N` — `@@handles` is all of
them.
<!-- pearde:end -->
