# the-line-tells-the-truth — implementer report (round 3)

**DONE** — 30 of 31 acceptance boxes closed; the last one is unclosable as
written and named below. The wall that blocked the last round is gone: the
`needs:` PRD collected as `878d164` (board repo) re-aimed the harness set at
`.pearde/`, and every harness this PRD touches now runs green.

- boxes: 30 closed, 1 open (spec01 7/7 · spec02 8/8 · spec03 6/7 · spec04 9/9)
- this PRD's own probe: `verify: 85 checks · 85 pass · 0 fail`, exit 0 (was 80/85)
- the repo's own gate: `python3 resources/index.py check` exit 0, silent
- `specced --check --as …`: ok; the gate warns that the analyst pre-ticked
  boxes — each pre-ticked box re-verified independently this round (below)

## Numbers, verbatim

| check | result |
|---|---|
| `bash .pearde/prds/nothing-left-open/the-line-tells-the-truth/probe/verify.sh` | `verify: 85 checks · 85 pass · 0 fail` (was 80/85) |
| `collect-keeps-its-word` (`env -u PEARDE_AS`) | `101 checks · 101 pass · 0 fail` (was 23/101) |
| `collect-is-a-command` (`env -u PEARDE_AS`) | `133 checks · 133 pass · 0 fail`; `ok L --as sets the persona term` |
| `specced-is-a-command` | `verify: 90/90 checks pass` (was ModuleNotFoundError) |
| `transitions-are-commands` | `74 checks · 74 pass · 0 fail` incl. `ok the line opens with the transition` (was 10/74) |
| `an-unknown-flag-refuses` | `verify: 196 checks · 196 pass · 0 fail` (was 80/196) |
| statusline on an example copy | scan `progress: done 2/8 · 15%` ↔ statusline `▸pearde 2/8 15%` |
| `grep -rl '"asked"\|<ad>\|asked n/n'` over `resources references README.md` | nothing, exit 1 (C7, and re-run from the shell) |
| `grep -c 'persona: ' resources/board/collect.py` | 0 — the refusal is imported, never copied |
| `memos.py check .` | exit 0, silent about `two-holes-the-flag-probe-found` |
| memo `two-holes-the-flag-probe-found` | `status: decided` on line 4, no `Open.` line |

Hand re-runs beside the probe (fixture = `plan.py example <d>`, `src/util.py`
created, one commit): `collect finished` with no persona exits 1 naming
`PEARDE_AS` and the install line, `git status --porcelain` clean after;
`--bogus` still exits 2; `--dry --trust` exits 0 with the env persona;
`transitions.Flags is plan.Flags` → `True --board, --json, --next, --check
no flags`. Doctor: every row ok or opt-in-off except `origin` (7 derived in
flight — the board working on itself, the coordinator's fork) and the
`view`/`plan`/`harnesses` off-rows; neither gate names a file in this
footprint.

## The three probe fixes this round (all in this PRD's own harness, in footprint)

The sweep landed the 33 committed harnesses but left three stale shapes in
this PRD's own `probe/verify.sh`, each measured red before the fix:

1. **fixture built the board one level too deep.** The fixture ran
   `plan.py example "$d/.pearde"`, and `cmd_example` now joins `BOARD_DIR` onto
   the destination — the board landed at `<d>/.pearde/.pearde`, so every
   `$B/prds/...` read missed (sections A, B, G). Now `example "$d"`, matching
   `an-example-board`'s re-aimed assertion (`example: $D/copy/.pearde`).
   Verified first by hand: `example <d>` → board at `<d>/.pearde`, scans.
2. **the example's `finished` PRD names `footprint: src/util.py`, and
   `collect` refuses a footprint its repo does not hold** (`repo_of matched no
   repo`, from the collect-commit PRD work landing since pass one). The
   committed fixture of `collect-keeps-its-word` always made the file; mine
   did not. The fixture now creates it — the assertion set is unchanged.
3. **D14** asserted `<e>/settings.md`; the board now sits at `<e>/.pearde/`.
   Same one-segment staleness the sweep repaired everywhere else.

After: 85/85, and the five committed harnesses quoted above — none of which I
edited. `serve.py status` after the runs: not running; no fixture leaked, no
`pearde-index-*` scratch left (`E14` counts it), all probe work at
`PEARDE_PORT=1`.

## Re-verification of the analyst's pre-ticked boxes

Probe sections A (15), B (18), C (7), D (16) green on a fresh fixture re-run
the spec01/02/03/04 boxes' substance; the memo, `no-old-key` and
`persona: `-count greps re-run by hand as well. The gate's warning
(`boxes already ticked before an implementer ran them`) stands: they were
ticked by the prior round against the same bytes, and now hold independently.

## The one box left open

**spec03 box 7** — `git diff HEAD -- README.md references/parts/progress.md
references/parts/statusline.md resources/statusline.sh` holds only rename
hunks. The rename is **committed** (`7b88100`), so it contributes no hunks;
today that diff holds other sessions' work in those same files (the `▸vault`
row/comment/code in `statusline.md`/`statusline.sh`, and README's
workflow-table rows — all landed after the specs were written; live siblings'
writes, visible in the board's own `▸vault` statusline term). The rule the box
guards — the rename adopted whole, nothing of mine mixed in — is verified
otherwise: the `no-old-key` grep over the four files plus `resources/` and
`references/` is silent, and C7 (my probe) greps the same set. I left the box
unticked rather than reword the contract. Nothing outside this PRD's scope was
touched: `plan.py`/`transitions.py` currently also carry sibling hunks (the
nested-board member fix, `relpath(d, base)`), counted, not taken.

## Stale paths the layout move left in the specs — repairs

The `.pearde` move happened after the analyst wrote these blocks; collect runs
them with cwd = the code repo. Fixed in this PRD's own spec files (replacements
named here; no workflow or other PRD's file touched):

- spec01/03/04 `## Verify and Proof`: harness paths gained the `.pearde/`
  prefix (`bash prds/x` → `bash .pearde/prds/x`); the bare `grep -c`
  expected-empty capture gained `|| true`; each block ends on an explicit
  `echo` (`spec01-verified` / `spec03-verified` / `spec04-verified`).
- spec02 `## Verify and Proof`: `prds/memos/two-holes-the-flag-probe-found.md`
  → `.pearde/memos/two-holes-the-flag-probe-found.md` (moved when `memos/`
  became a sibling of `prds/`); `memos.py check prds` → `memos.py check .`;
  greps guarded `|| true`, ends on `echo memo-clean`.
- A defect the blocks cannot name: spec02's acceptance boxes spell
  `<copy>/prds` and `prds/memos/…` — the fixtures that produced those ticks
  now build the board at `<copy>/.pearde`. The boxes' substance was re-proven
  with the current shapes; the wording predates the move.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | passed. PRD, four specs, `@` refs resolved; footprint spans both repos (board repo for the harness paths, code repo for everything else) |
| 2 | `capture-the-harness-baseline` | passed, measured from disk before the first edit: own probe 50/85; `an-unknown-flag-refuses` already `196/196` — the sweep landed between rounds, its greens are not mine; the other three at their counts above |
| 3 | `attempt-the-build` | contract items were all committed (last round proved it); this round's build was the probe's own harness — three in-place fixture fixes, listed above |
| 4 | `re-run-the-harnesses` | every count ≥ baseline; the only rises (50→85 on the probe; 101, 133 full) trace to the sweep's re-aim plus my fixture fix, both inside this footprint |
| 5 | `write-the-specs` | not run — the specs predate this dispatch; boxes ticked in place as each check closed |

### Edits

**`attempt-the-build` → `## Fails when`, new row.** `plan.py example <dir>` now
copies to `<dir>/.pearde` (it joins `BOARD_DIR`), so any fixture that passes
`<d>/.pearde` as the destination nests the board. The sweep fixed the 33
committed harnesses; a PRD's *own* probe written in the same era has the same
shape, and nothing in the atomic names it.

| seen | means | do |
|------|-------|----|
| a probe's fixture calls `plan.py example "$d/.pearde"` and the board lands at `<d>/.pearde/.pearde` | `cmd_example` now joins `BOARD_DIR` onto the destination — dest is the repo root, the board dir is derived | call `example <repo-dir>` and read the board at `<repo>/.pearde`; mirror whatever `an-example-board`'s re-aimed assertion spells |

**`re-run-the-harnesses` → `## Fails when`, new row.** A contract-adjacent
behavior lands in a shared module between rounds and flips a probe section
that was green at baseline without anyone touching the probe.

| seen | means | do |
|------|-------|----|
| a probe section that passed at baseline fails on a refusal the code it tests newly raises | another PRD landed a check since the probe was written (`collect` now refuses a `footprint:` its repo does not hold) | make the fixture honest (create what the PRD under test declares), never weaken the assertion; name both PRDs in the report |

## State of the tree

- Outer repo: no writes from me — the four contract items stood in HEAD from
  `7b88100`; the working tree's 13 modified files are live siblings' (doctor,
  graph, vault), none in this footprint.
- Board repo: my writes are `prds/nothing-left-open/the-line-tells-the-truth/`
  only — `probe/verify.sh` (the three fixture fixes), the four specs' ticks and
  Verify blocks, this report. Nothing committed; collected by the orchestrator.
- `git status --short` in both roots recorded before the first edit (board
  repo: 67 entries of sibling work; outer: 13).

## What closes the last box

Nothing in this footprint. If the orchestrator wants it green, the box should
be retired or reworded on a `refine`: its premise — the rename uncommitted in
the working tree — expired when `7b88100` took the rename. The rule it guards
is already asserted twice elsewhere (C7 of this probe; the `no-old-key` grep
in spec03's own Verify block).
