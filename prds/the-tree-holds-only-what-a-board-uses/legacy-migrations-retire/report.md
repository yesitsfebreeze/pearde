# legacy-migrations-retire — analyst pass one

Verdict: SPECCED

Four specs, sum `complexity` 36, in `specs/`. The build ran in the lane at
`.pearde/.lanes/the-tree-holds-only-what-a-board-uses-legacy-migrations-retire`;
pass one is uncommitted there and captured as `probe/pass-one.diff`.

## What the build did

Spec01 and spec02 are **built and green**. Spec03 and spec04 are scoped from
probes that ran, not from reading.

- `migrate_legacy_state`, `LEGACY_MACHINE_DIR` and the import-time `try:` call
  are out of `resources/board/boards.py`; the two names are out of `plan.py`'s
  re-export; `json` went with them. `every-artifact-lands-inside-the-board.sh`
  lost its `LEGACY_MACHINE_DIR` exemption and passes — the grep now fails on
  any `MACHINE_DIR` at all. `resources/board/state/` does not exist on this
  machine, so the migration had no work left.
- `unhide_board` and its two callers are out of `resources/board/init.py`.
- All six invariants run: five pass, and
  `no-colour-group-in-the-vault-preset-is-a-path-query.sh` is BROKEN **in the
  lane only** (a lane has no board) and passes against the checkout. Not mine.

## The door the whole contract routes migrations through was shut

The PRD's premise is `pearde upgrade`. It refused every board:

```
pearde upgrade: refused — a board directory is one plain name with no dot in
front of it — `.pearde` is what the move is out of
```

`cmd_upgrade` computes `into = args.opt.get("dir") or planlib.BOARD_DIR` and
hands it to `unhide_board`, which rejects any name starting with a dot.
`BOARD_DIR` has been `.pearde` since the 2026-09-02 revert, so the call refused
before doing anything. `cmd_vault` refused identically. Reproduced in a fresh
temp project, not inferred. `unhide_board` moves a board *out of* `.pearde/` —
the reverted direction — so it goes rather than gets flipped; with it removed,
`pearde upgrade` runs a board end to end and `pearde vault --dry` stops
refusing. That is spec02.

## The two board spellings can go today, with no board moved

Contract-critical and measured, not assumed. Seven of the nine boards on this
machine are a real `pearde/` directory with a `.pearde` symlink beside it
(manola, racer/.mi, dotfiles, mitosys, shared, model, realm); `zirkle/kern` and
this repo hold a real `.pearde/`; `/Users/feb/dev/infra`'s board is named
`board`. `probe/resolves-without-the-legacy-name.py` resolves all ten with and
without the legacy name in `BOARD_DIRS`:

```
0 board(s) resolve differently without the legacy name
```

`board_link` reads back through the compatibility symlink, so the name can
leave resolution with nothing renamed or upgraded first. This is why the PRD
does not need a `## Split` — spec04 does not wait on spec02.

## The PRD's second item names something that is not there

> guard's `LEGACY` handling for the retired machine dir

`resources/guard.py` has no machine-dir migration — `grep -n 'legacy\|machine
dir\|board/state\|retired'` over it returns nothing. What it has is its own
`LEGACY_BOARD_DIR`, and it is **inverted**: `BOARD_DIR = "pearde"` and
`LEGACY_BOARD_DIR = ".pearde"`, the reverse of `common.py` and `boards.py`,
which both hold `BOARD_DIR = ".pearde"`. Three copies of one pair and one of
them disagrees. It is harmless on today's disk only because `BOARD_DIRS` is
searched in order and no project on this machine holds both a real non-board
`pearde/` and a real `.pearde/` board. Folded into spec04, which deletes the
pair from all three modules rather than reconciling it.

## The store fold is not spent, so it moves rather than goes

`shared.RETIRED` folds `.pearde/graphify/cache` into `pearde/graphify/cache`.
Surveyed every repo store on this machine: `infra/pearde` and `manola` hold the
survivor only, but `/Users/feb/dev/infra/mitosys/.git/pearde-shared/` still
holds `.pearde/` beside `pearde/`. So deleting the table would strand a real
duplicate. It moves to `cmd_upgrade` — spec03, which spec02 makes reachable.

`state()`'s `stale` verdict survives the move: line 333 returns it for any link
onto another key of the same store and never reads the table. Only its
docstring names `RETIRED`.

## The vault row and the reverted direction — a finding, not a spec

`resources/doctor.sh:472` reports this repo's own board **broken** for being
`.pearde`, and line 473 prescribes `pearde upgrade`, which "moves it to
`$PROJ/pearde` and leaves a `.pearde` symlink". `references/obsidian.md` and
`write_obsidian`'s docstring argue the same reverted direction. Meanwhile
`boards.py`'s own header says the undotted name "cost more than it bought" and
the board is `.pearde/`.

Doctor and the board's contract disagree about the layout. Before pass one the
prescribed fix refused; after it the command succeeds and moves nothing, so the
row would stay broken forever. Spec02 stops the fix line naming a no-op, which
is the defect spec02 itself creates. **What the row should say instead — that a
dotted board is `off` rather than `broken`, or that `pearde upgrade --dir
<name>` is the way to a vault, `named_boards` already supporting it — is a
wrong claim outside this footprint and belongs in its own PRD.** Not specced
here; widening the contract is not this pass's call.

## Other findings, all outside the footprint

- `resources/index.py check` fails four rows at HEAD, before anything I
  touched: `resources/common.py` has no row in `references/files.md`;
  `references/files.md` and `@@view` both name `resources/board/hotreload-test.js`,
  deleted in b1d3f5d; `references/parts/commits.md` cites
  `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md` — an
  **undotted** board path, which is the same two-spelling drift in prose.
- `no-colour-group-in-the-vault-preset-is-a-path-query.sh:49` hardcodes
  `pearde/` in its refusal text. Cosmetic, but it is another copy.
- `register_vault` takes a parameter named `retire`, unrelated to
  `shared.retire`. Renaming it would make spec03's greps cleaner.
- `doctor.sh` also reports `origin broken` (6 derived PRDs with no `from:`) and
  `health broken` (4 dropped files, ranking 33 commits behind). Both
  pre-existing.

## Record

Queried `knowledge.py query` with the contract first — 95 hits, and
`[[260901-ee0f]]` ("Every pearde board on this machine is on the .pearde
layout", 2026-09-01) is **stale**: it predates the 09-02 undot and this pass
re-measured it. No gap auto-enqueued. Two facts written back:
`[[260903-03e8]]` and `[[260903-fcc0]]`.

## Workflow probe-then-spec

Followed `probe-then-spec` unchanged — its `## Use when` names an `open` PRD
needing specs before anyone can be sent at it, which is this. Every step fired
as written; step 1's `Fails when` row about a lane whose footprint paths exist
under it applied, and the footprint is entirely in the lane, so no board copy
was needed. No new atomic. One recurrence worth noting rather than filing:
`attempt-the-build` twice found that the *documented premise* of the contract
was itself broken (here the migration door; on
`the-advisors-share-one-resolver-and-one-parser` the duplicated parser). The
library already holds `verify-the-claim-before-fixing-it` for that shape and it
is the right file — no second one written.

## Reasoning for the two numbers

- **complexity 34** — four units, sum 36, none of them novel design: three are
  deletions the probe already proved safe, and only spec03 writes new code, a
  fold moved between two modules that already hold every helper it needs.
- **blast-radius high** — spec04 changes how *every* module finds a board, and
  a wrong resolution loses a board silently rather than loudly. Nine live
  boards on this machine, seven of them on the spelling being dropped.

## Scores

complexity: 34
blast-radius: high
workflow: probe-then-spec
