# ramp is a doctor row not a gate — implementer report

Verdict: DONE

Pass one had already written the code; this pass measured it. Every acceptance
box in both specs is closed against output quoted below, both `## Verify and
Proof` blocks ran, and the board's gate is green in the sense the gate can be
green here — `index.py check` and `doctor.sh` carry the same problems at HEAD
as they carry with this work applied, and not one of them is ours.

Nothing was committed. `@references/parts/commits.md` says the orchestrator
commits and never a worker; the lane holds nine modified files, staged by
nobody, waiting for `collect`.

## What was run

`probe/verify.sh` in the lane, 19 checks, every one green, ending
`ramp is a doctor row, not a gate — every check green`.

### spec01 — the gate comes out of the code · 7/7

- `grep -rl happiness resources/` — no match, exit 1.
- `ramp.py` — no `def happiness`, `def write_ask`, `def cmd_happy`, `def
  cmd_gate`; `verbs = {"have", "need", "gap", "find"}` at line 618, no `happy`.
- `init` on a fresh repo writes five knobs — `language, workers, pipeline,
  weight-default, gantt-day` — and `grep -c happiness` is 0 on both the plain
  and the `--example` board.
- `ramp gap` on a Cargo.toml + five `.rs` fixture with empty skill dirs:
  `GAP rust  6  Cargo.toml×1, *.rs×5` / `gap: 1 of 1 jobs unanswered`, exit 0.
- Bare `ramp` on that fixture printed the gap, then six rust candidates each
  with its `npx skills add … -l` line, closing `ramp: 1 gap — nothing is
  installed by this command, and nothing waits on it`, exit 0. The fixture's
  file list hashed the same before and after.
- No `.pearde/.state/ask.md` on a board that has only ever been `init`ed —
  `.state/` holds `history.jsonl` and `parse-cache.json` and nothing else.
- `a-master-need-is-the-union-of-its-members.sh` — 17 PASS, exit 0.
- `ast.parse` on `ramp.py` — clean.

### spec02 — the reading moves to a doctor row · 9/9

- `bash -n resources/doctor.sh` clean; `doctor` prints `ramp` between `board`
  and `vault` on both the real board and the fixture.
- Gap standing: `ramp  off  0 of 1 job answered · gap: rust`, with
  `fix: … pearde.py ramp ./.pearde — the candidates for each gap, with the line
  that installs one` and `a gap is a reading, not a failure — the board
  installs nothing and no pass waits on this row`.
- Every job answered, this repo's board: `ramp  ok  4 jobs · every one answered
  by an installed skill`. A tree the jobs table knows nothing in reads `off ·
  the tree asks for nothing the jobs table recognises` (doctor.sh:422).
- `broken` on that row is reachable only through `no python3 to read the tree's
  asks` (doctor.sh:414) — never through a gap; the probe asserts the row adds 0
  to the broken count.
- The row calls `python3 "$DIR/board/ramp.py" gap "$BOARD"` (doctor.sh:417) and
  nothing else — no `find`, no bare verb, no network.
- `grep -c happiness references/settings.md` is 0; the yaml block shows the five
  keys plus `context-budget`.
- `loop.md` holds no `0 ramp` row and no `**0 · Ramp.**`; its step table opens
  `| 1 scan | nothing — read |`.
- `doctor.md` line 26 carries the `ramp` row, reading *a reading, never a
  failure*.
- `index.py check` returns the same four problems with the work applied as it
  returns at HEAD — no new one.

### The board's gate

`@.pearde/settings.md` names `index.py check`, `memos.py check` and `doctor.sh`.
Run with the lane's code against this repo's board, and again from HEAD for the
comparison:

- `memos.py check` — silent, exit 0.
- `index.py check` — four problems, byte-identical to HEAD's four.
- `doctor.sh` — the row set is identical to HEAD's row for row, with the one
  new `ramp ok` line added. `index`, `vault`, `origin`, `health` and `knowledge`
  read `broken` in both runs.

## Findings, out of scope

- **The four `index.py check` problems the analyst named still stand**, and each
  reproduces on a clean HEAD checkout: `resources/common.py` has no row in
  `references/files.md`; `references/files.md` and the `@@view` scope both name
  the deleted `@resources/board/hotreload-test.js`;
  `references/parts/commits.md` cites a memo not on disk. Map fixes, not this
  contract.
- **Four doctor rows read `broken` on this board before and after** — `index`,
  `vault`, `origin`, `health`, `knowledge`. Each is its own PRD's business. The
  board's gate cannot be *all three green* on this repo today, which is why the
  reading above is HEAD-relative rather than absolute.
- **`no-colour-group-in-the-vault-preset-is-a-path-query.sh` cannot run inside a
  lane** — it prints `BROKEN: no board at pearde/ — the second check has nothing
  to read` and exits 0, because a lane worktree carries no `.pearde`. It is
  green in the checkout. An invariant that reports broken and exits 0 is worth a
  look, but nothing here touched it.
- **`one-copy-per-machine-of-what-every-lane-regenerates.sh` did not finish in
  two minutes** and was not waited out. Unrelated to this footprint; noted so
  the next run knows it is slow, not hung.
- No word in the contract needed `grammar.py show`. No fact came from outside
  this tree, so nothing was written with `knowledge.py remember`.
- No file in the footprint sits under the health floor; nothing was moved.

## Footprint, uncommitted in the lane

```
references/files.md
references/parts/doctor.md
references/parts/handles.md
references/parts/loop.md
references/parts/ramp.md
references/settings.md
resources/board/init.py
resources/board/ramp.py
resources/doctor.sh
```
