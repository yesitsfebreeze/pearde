# prd

`prd` owns planning for the composition: the central PRD boards under `.cartridge/boards/`, their dependency plan, Gantt, specifications, claims and checked work transitions. It gives back what is ready to work, a brief for one item, and a verified collection that refuses to mark work done on a worker's exit alone. A spec's `test` Verify block names the tests the runner must report as passed, and a lane of a superproject carries its submodules at their pinned commits. An agent reaches it through the `prd` tool; a trusted native caller reaches the `prd` service, which adds read-only source declaration and record ops; a person reaches the same engine through `just prd`. Memory supplies recalled context; PRD records stay the authority.

## Use

`plan` and `scan` accept `--limit` from 1 to 200 and `--offset` for pagination.
Consumers follow `next_offset` and compare `snapshot` across pages.

On macOS, the process grant includes Command Line Tools Git, which the system
Git launcher executes. An execution denial otherwise holds every repository task.

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

## ASP plans and tasks

Expand `plan:root` through `asp` to discover declared boards, task pages, and
canonical `task:<board>/<record>` IDs. For example, `@agent/example` becomes
`task:agent/example`, and root `example` becomes `task:root/example`. Record keys
omit `prds/` and `/prd.md`; nested directories remain.

`prd.state`, `prd.claim`, `prd.complexity`, `prd.checks_done` and `prd.checks_total`
show recorded work. Task expansion adds `prd.checks` and actual public
`depends-on`, `contains` and `recorded-in` links. `prd.record` and
`prd.record_revision` identify the exact source. A worker's exit alone never
changes these attributes into completed work.

Pages contain at most 50 tasks; follow returned `#page=N` IDs. The public reader
excludes private records and labels partial indexes. The contributor reads at
most 64 declared boards and 1,024 records per board, under an 1,800 millisecond
request deadline. It does not run the planner, claim work, recall memory, or
invent timing information. The PRD plan API still owns computed scheduling.

## Scope presentation

The plugin publishes `prd.scope.summary` inside its ASP node attributes
(the attribute `prd.scope` is an object with a `summary` field). Scope uses
this provider-owned text in the shared list. Declared `scope.detail.*` listeners
run the plugin's `src/scope_detail.py` helper to return version 1 detail
documents. Rendering is read-only, takes the item, selected field or occurrence,
and viewport dimensions, and returns a title and labeled JSON sections. The
base owns terminal input, layout and navigation. Python 3 is an explicit exec
grant for the lazily started helper; generic details remain usable if it fails.

The `scope_python` setting selects the helper executable (default `python3`).
On macOS, use the actual Python executable rather than an SDK launcher shim
when the sandbox cannot execute the shim. The setting supplies the explicit
exec grant and is excluded from the native core configuration.

## Refresh committed collection evidence

`prd collect <ref> --committed` verifies a clean committed snapshot and preserves
unrelated dirty source files. `verification_target`, `workspace_verified` and
`workspace_drift` distinguish committed proof from workspace state. Verify the
loaded artifact separately. `prd collect <done-ref> --reverify` reruns the same
published contract at current HEAD and retains immutable prior receipts. Changed
contracts, missing provenance, unverified dependencies or active ownership refuse
the refresh. Default collection remains strict; dirty files overlapping a lane
merge still require scoped reconciliation before retry.

ASP search overlaps up to four independent board indexes, and each index verifies its recorded directories in groups of sixteen. Results retain board order; no freshness, visibility or symlink check is skipped. Exact reads start with an observed-size buffer and grow within the existing file and aggregate limits. Timeouts and incomplete source reads remain explicit.
