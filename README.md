# prd

`prd` owns planning for the composition: the central PRD boards under `.cartridge/boards/`, their dependency plan, Gantt, specifications, claims and checked work transitions. It gives back what is ready to work, a brief for one item, and a verified collection that refuses to mark work done on a worker's exit alone. A spec's `test` Verify block names the tests the runner must report as passed, and a lane of a superproject carries its submodules at their pinned commits. An agent reaches it through the `prd` tool; a trusted native caller reaches the `prd` service, which adds read-only source declaration and record ops; a person reaches the same engine through `just prd`. Memory supplies recalled context; PRD records stay the authority.

## Events

Everything between cartridges is an event, declared in `cartridge.json`.

- **Defines** — `tool.prd`, `prd`, `source.board`
- **Listens to** — `prd`, `tool.prd`, `source.board`
- **Needs** — nothing. It stands alone in any composition.

## Use

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

## Committed collection evidence

Use `prd collect <ref> --committed` to verify the integrated commit in a clean
checkout while preserving unrelated dirty files. Results explicitly name
`verification_target: committed` and separately report `workspace_verified` and
`workspace_drift`; they do not certify a loaded binary. After later committed
footprint changes, `prd collect <done-ref> --reverify` reruns the unchanged contract
and preserves the prior receipt by content digest. Changed contracts, invalid
provenance and unresolved dependencies are refused. Normal collection remains
strict. See [.cartridge/docs/collection-proof.md](.cartridge/docs/collection-proof.md).
