# prd

`prd` owns planning for the composition: the central PRD boards under `.cartridge/boards/`, their dependency plan, Gantt, specifications, claims and checked work transitions. It gives back what is ready to work, a brief for one item, and a verified collection that refuses to mark work done on a worker's exit alone. A spec's `test` Verify block names the tests the runner must report as passed, and a lane of a superproject carries its submodules at their pinned commits. An agent reaches it through the `prd` tool; a trusted native caller reaches the `prd` service, which adds read-only source declaration and record ops; a person reaches the same engine through `just prd`. Memory supplies recalled context; PRD records stay the authority.

## Events

Everything between cartridges is an event, declared in `cartridge.json`.

- **Defines** — `tool.prd`, `prd`, `source.board`
- **Listens to** — `prd`, `tool.prd`, `source.board`
- **Needs** — nothing. It stands alone in any composition.

## Use

Read-only `plan` and `scan` accept `--limit` from 1 to 200, matching the native
engine. Larger pages avoid recomputing an unchanged dependency graph for each
small page; consumers still follow `next_offset` and validate `snapshot`.

The process grant includes macOS Command Line Tools Git because `/usr/bin/git`
executes that binary. Without it, repository checks report an execution denial
and correctly hold tasks instead of reporting them ready.

- `tool.prd` (`prd` to the model): `{op, board?, args?}` with `op` one of `scan`, `plan`, `gantt`, `read`, `brief`, `next`, `add`, `refine`, `specced`, `claim`, `release`, `collect`, `run`, `status`, `stop`; `board` defaults to the configured board; `args` are the CLI-style positional strings and flags for that op. `status` and `stop` take one job id and address only this session's jobs. `run` needs a configured adapter or `--dry`.
- `source.board` (native service only, the owner of board search roots): `{op:"source_declarations", board, deadline_ms}` returns declared child boards and a settings `revision`; `{op:"source_records", board, action:"index"|"read", expected_source_revision, path?, expected_revision?}` indexes and reads public records.
- `just prd help`, `just prd scan`, `just prd plan --json`, `just prd check`; add `--board <name>` to select a registered board.

## In this composition

`prd.ctg` is one cartridge of the [Cartridge](https://github.com/yesitsfebreeze/cartridge-workspace)
runtime: an independent component with its own repository, manifest and
sandboxed node. It reaches its siblings only through the events declared
above, and `just isolation` fails the composition if it reaches past them.

`cartridge help prd` prints the full page for this cartridge;
[.cartridge/help.md](.cartridge/help.md) is that page, and the documents it
links are the ones worth reading next.

## Status

Early (`0.1.0`). Interfaces change without notice.

## ASP task graph

PRD contributes `plan:root` to the composition's ASP root. It contains the actual
registered child boards and public tasks in pages of 50. Expand `plan:<board>` or
its returned `#page=N` nodes, then a returned `task:<board>/<record>` identity.
For example, PRD reference `@agent/example` maps to `task:agent/example`; the
root reference `example` maps to `task:root/example`. A task key excludes the
record's `prds/` prefix and `/prd.md` suffix. Nested record directories remain.

Task attributes expose recorded state, claim, positive authored complexity (or
null), checked and total acceptance items, and the canonical record path and
SHA-256. Task expansion adds the recorded checks and verified public dependency
links. `recorded-in` links name actual files relative to the host working directory
when the file is inside it. No file link is invented for a record outside that
workspace. Missing, private and ambiguous dependency targets produce no links;
the unresolved count explains omitted dependencies without disclosing them.

The contributor uses the existing bounded public source reader, not Git, memory
recall or planner execution. It supports 64 declared boards, 1,024 indexed public
records per board, 50 tasks per page, 128 displayed checks and 32 dependency
references per task expansion. Partial indexes and truncated checks are labelled.
A request has an 1,800 millisecond deadline. Search reads only reachable public
boards. Scheme-owner revisions follow ASP's expanded-subject convention;
`prd.record_revision` separately retains the exact task record digest.

These entities are a graph of recorded work, not a fabricated schedule. The
planner's computed dispatchability and dependency intervals remain available
through the PRD plan API; relative complexity does not represent elapsed time.

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

## Committed collection evidence

Use `prd collect <ref> --committed` to verify the integrated commit in a clean
checkout while preserving unrelated dirty files. Results explicitly name
`verification_target: committed` and separately report `workspace_verified` and
`workspace_drift`; they do not certify a loaded binary. After later committed
footprint changes, `prd collect <done-ref> --reverify` reruns the unchanged contract
and preserves the prior receipt by content digest. Changed contracts, invalid
provenance and unresolved dependencies are refused. Normal collection remains
strict. See [.cartridge/docs/collection-proof.md](.cartridge/docs/collection-proof.md).

ASP search indexes at most four independent declared boards concurrently, retaining board order and the existing request deadline. Directory stability checks run in bounded groups while preserving every revision and symlink check. Exact source reads allocate for the observed file size and grow only when necessary, rather than allocating the maximum one-megabyte file budget for every small record. Growing files still debit actual bytes and obey the existing aggregate cap.
