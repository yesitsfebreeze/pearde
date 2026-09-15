# prd

`prd` owns planning for the composition: the central PRD boards under `.cartridge/boards/`, their dependency plan, Gantt, specifications, claims and checked work transitions. It gives back what is ready to work, a brief for one item, and a verified collection that refuses to mark work done on a worker's exit alone. An agent reaches it through the `prd` tool; a trusted native caller reaches the `prd` service, which adds read-only source declaration and record ops; a person reaches the same engine through `just prd`. Memory supplies recalled context; PRD records stay the authority.

## Use

- `tool.prd` (`prd` to the model): `{op, board?, args?}` with `op` one of `scan`, `plan`, `gantt`, `read`, `brief`, `next`, `add`, `refine`, `specced`, `claim`, `release`, `collect`, `run`, `status`, `stop`; `board` defaults to the configured board; `args` are the CLI-style positional strings and flags for that op. `status` and `stop` take one job id and address only this session's jobs. `run` needs a configured adapter or `--dry`.
- `source.board` (native service only, the owner of board search roots): `{op:"source_declarations", board, deadline_ms}` returns declared child boards and a settings `revision`; `{op:"source_records", board, action:"index"|"read", expected_source_revision, path?, expected_revision?}` indexes and reads public records.
- `just prd help`, `just prd scan`, `just prd plan --json`, `just prd check`; add `--board <name>` to select a registered board.

## Read next

- [PRD cartridge](.cartridge/docs/README.md) — What does the engine do, how is it run and tested, and what does a collection check before marking work done?
- [PRD owns planning](.cartridge/memos/system/prd.md) — What does the agent's prompt say about who owns planning state and events?
- [Run the board](.cartridge/memos/routine/run-board.md) — How does an agent work a board continuously with scan, next, brief, claim and collect?
- [Spec a PRD](.cartridge/memos/routine/spec-a-prd.md) — What does the analyst return for one open PRD: a spec, a split or a question?
- [Implement a PRD](.cartridge/memos/routine/implement-a-prd.md) — How does an implementer build one specced PRD and report observed checks?
- [Land a PRD](.cartridge/memos/routine/land-a-prd.md) — How is a worked PRD verified, integrated and collected before it is done?
- [Read declared source edges](.cartridge/docs/source-declarations.md) — What does `source_declarations` return, and what are its limits and failure statuses?
- [Native public source records](.cartridge/docs/source-records.md) — How do `index` and `read` expose only public records under a revision guard?
- [Planner status line](.cartridge/memos/routine/planner-statusline.md) — How is a read-only board progress line rendered for the current owner?
- [Install the planner CLI](.cartridge/memos/routine/install-planner-cli.md) — How are the `prd` and `pearde` launchers installed and the old statusline migrated?
- [Develop the planner](.cartridge/memos/routine/develop-planner.md) — How is the native engine checked and exercised without Python or a model?
