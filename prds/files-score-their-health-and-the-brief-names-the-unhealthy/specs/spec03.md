---
complexity: 4
footprint:
  - references/parts/health.md
  - references/skills/pearde-health.md
  - references/settings.md
  - references/templates/grammar.md
  - references/parts/doctor.md
  - references/parts/handles.md
  - resources/doctor.sh
  - resources/pearde.py
  - resources/board/init.py
---

# spec03 — health is a registered part, with its knobs, its row and its words

`health` is registered everywhere a part is registered: the `FORWARD` table,
the skill file, the part doc, the settings contract, the doctor row, the
handles table, the grammar template's **part** row and its collision rows,
and the board's own `.gitignore` through `init.py`. Two flat knobs live in
`references/settings.md` — `health-floor` and `health-weights` — and the
record is regenerable, so the board ignores it.

## What already stands

All of it, committed.

- `resources/pearde.py:85` — `"health": ("health.py", [], ("score", "list", "show", "check", "init"))`
- `references/skills/pearde-health.md` — the skill file; `doctor`'s `skills`
  row lists `pearde-health` among 18 well-formed
- `references/parts/health.md` — the part doc, including a `## Next, and not
  this round` section naming all four of the PRD's non-goals: the derived
  split PRD, the guard note on editing an unhealthy file, the rescore at
  collect, and the mtime cache
- `references/settings.md:43-44` — `health-floor` default 40 and
  `health-weights` default `lines=25 branching=30 longest=20 fan_out=5
  fan_in=10 links=10`, with the behaviour on an unknown axis or an unreadable
  weight written down
- `resources/doctor.sh` — the row, green: `health ok 151 files · 5 under 40`
- `references/templates/grammar.md` — `health` and `unhealthy` term rows, the
  **part** row listing `health`, and the collision rows for `floor`
  (`health-floor` vs the billing window) and `complexity` (the PRD weight vs
  a file's health). `grammar.py check` is clean; `doctor`'s `grammar` row is
  green on 177 terms
- `resources/board/init.py:85` — `"health/"` in the board `.gitignore` list;
  `git check-ignore` confirms `.pearde/health/ranking.md` is ignored
- `references/parts/handles.md`, `references/parts/doctor.md`,
  `references/files.md`, `index.md`, `SKILL.md` — all carry their health rows;
  `index.py check` is green on 149 files with every anchor resolving

## What is left

Nothing to write. The implementer re-runs the five gates and the doctor row
and reports. `SKILL.md`, `index.md` and `references/files.md` already carry
their health rows and are deliberately **not** in this footprint: they are in
the working set of the in-flight machine PRD, and claiming them here would
block it for no work.

## Acceptance

- [x] `health` is in the `FORWARD` table with its five verbs and `pearde
  help` lists it.
  `resources/pearde.py:85` · `  ok    I2 pearde help lists health`
- [x] `references/settings.md` documents `health-floor` (default 40) and
  `health-weights`, and an unreadable weight is one problem line that still
  writes the record.
  `  ok    G2 an unreadable weight exits 1` · `  ok    G3 and says which` ·
  `  ok    G4 and still writes the record` ·
  `  ok    G1 lines alone gives deep.py a different score (10 → 30)`
- [x] `doctor.sh` carries a `health` row and it is green.
  `health      ok      153 files · 5 under 40`. The row is asserted `ok`, not
  on its file total: that number is the whole tracked tree and a sibling
  landing moves it (151 → 152 → 153 during this pass alone). `5 under 40` and
  every score held across all three.
- [x] `init.py` puts `health/` in a new board's `.gitignore`.
  `resources/board/init.py:85` — `"wiki/Dashboard.report.md", ".obsidian/", "health/",` ·
  probe `  ok    A10 health/ is ignored on the board`, which builds a board
  with `init.py` under `mktemp -d` and reads the `.gitignore` it wrote
  (`probe/verify.sh:69`).
  `git check-ignore .pearde/health/ranking.md` **is not evidence for this box
  and has been removed from the block**: it passes off `.gitignore:16:.pearde/`,
  which ignores the whole board directory, so it stays green with `"health/"`
  stripped out of `init.py` — measured, exit 0 with the line mutated. It tested
  this repo's own `.gitignore`, never the registration.
- [x] The grammar template carries the **part** row naming `health`, the
  `health` and `unhealthy` term rows, and the collision rows for `floor` and
  `complexity`; `grammar.py check` is clean.
  `references/templates/grammar.md:258,261,262,289,290` · `grammar.py check` exit 0, no output
- [x] `memos.py check`, `grammar.py check` and `brief.py --check` exit 0; and
  `index.py check` runs without crashing and names no file in this spec's
  `footprint:`. Its **exit is deliberately not asserted** — it reads the whole
  checkout, so a sibling's unregistered file reddens it and the route forbids
  a block whose exit is decided outside its own footprint.
  `memos.py check` exit 0 silent · `grammar.py check` exit 0 silent ·
  `brief.py --check` exit 0 silent ·
  `index.py check` exit **1**, its one line
  `resources/board/lanes.py is on disk with no row in references/files.md` —
  a sibling's file, and `references/files.md` is one of the three shared files
  this spec deliberately leaves out of its footprint. The block prints that
  line on every run rather than swallowing it.
  `doctor.sh` has two broken rows today, `index broken 1 problem` (the same
  `lanes.py`) and `knowledge broken`; **both outside this footprint**, and the
  footprint's own rows are green: `health ok`, `grammar ok 177 terms`,
  `skills ok 18 well-formed`, `briefs ok`.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
FP='resources/health\.py|resources/doctor\.sh|resources/pearde\.py|resources/board/init\.py|references/health\.md|references/settings\.md|references/parts/(health|doctor|handles)\.md|references/skills/pearde-health\.md|references/templates/(health|grammar)\.md'
N=0
grep -q '"health": *("health.py"' resources/pearde.py || N=$((N+1))
grep -q '`health-floor`' references/settings.md || N=$((N+1))
grep -q '`health-weights`' references/settings.md || N=$((N+1))
grep -q '"health/"' resources/board/init.py || N=$((N+1))
grep -q '^| \*\*health\*\* |' references/templates/grammar.md || N=$((N+1))
grep -q '^| \*\*unhealthy\*\* |' references/templates/grammar.md || N=$((N+1))
grep -q '^| \*\*floor\*\* |.*health-floor' references/templates/grammar.md || N=$((N+1))
grep -q '^| \*\*part\*\* |.*`health`' references/templates/grammar.md || N=$((N+1))
grep -q 'health' references/parts/handles.md || N=$((N+1))
grep -q 'health' references/parts/doctor.md || N=$((N+1))
grep -q 'health' references/parts/health.md || N=$((N+1))
grep -q 'health' references/skills/pearde-health.md || N=$((N+1))
grep -q 'health' resources/doctor.sh || N=$((N+1))
python3 resources/memos.py check   || N=$((N+1))
python3 resources/grammar.py check || N=$((N+1))
python3 resources/board/brief.py --check || N=$((N+1))
idx=$(python3 resources/index.py check 2>&1) && irc=0 || irc=$?
printf 'index.py check exit=%s\n%s\n' "$irc" "$idx"
if [ "$irc" != 0 ] && [ "$irc" != 1 ]; then N=$((N+1)); fi
if printf '%s\n' "$idx" | grep -q 'Traceback'; then N=$((N+1)); fi
if printf '%s\n' "$idx" | grep -Eq "$FP"; then N=$((N+1)); fi
out=$(bash resources/doctor.sh 2>&1 || true)
[ -n "$out" ] || N=$((N+1))
printf '%s\n' "$out" | grep -E '^  health +ok' || N=$((N+1))
printf '%s\n' "$out" | grep -E '^  grammar +ok' || N=$((N+1))
echo "spec03 failures: $N"
[ "$N" = 0 ]
```
