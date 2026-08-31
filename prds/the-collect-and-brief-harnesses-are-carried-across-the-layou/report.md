# report — the-collect-and-brief-harnesses-are-carried-across-the-layou

**DONE.** 1 spec, 6 of 6 acceptance boxes ticked, each against output quoted
below. Zero code written — the unit is a proof, and every count matched the
denominator spec01 recorded.

## Boxes

| # | box | run | result |
|---|---|---|---|
| 1 | `collect-keeps-its-word` from repo root | `bash .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh` | `101 checks · 101 pass · 0 fail` |
| 2 | `collect-is-a-command` from repo root | `bash .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh` | `133 checks · 133 pass · 0 fail` |
| 3 | `brief-is-printed` from repo root | `bash .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh` | `verify: 104/104 checks pass` |
| 4 | same three by absolute path from `/` | `cd / && bash /Users/feb/dev/infra/pearde/…` ×3 | `101 checks · 101 pass · 0 fail`, `133 checks · 133 pass · 0 fail`, `verify: 104/104 checks pass` — identical to the repo-root lines |
| 5 | no bare `<dir>/prds` board handed to a tool | `grep -E -- '--board [^ ]*prds'` over the three | one hit only: `collect-keeps-its-word:40` `run_old() … --board "$D/.pearde/prds"` — the documented back-compat exception. No other `prds` mention in the three lies outside `.pearde/prds` |
| 6 | root derivation survives the move and resolves from `/` | resolved each file's `..` chain from `/` | all three land on `/Users/feb/dev/infra/pearde`, `resources/guard.py` present at each; `grep -ln '/Users/feb'` over the three → no match, exit 1 |

Whole `## Verify and Proof` block, run under `bash -e -o pipefail` with the
code repo on stdin: exit `0`.

```
collect-keeps-its-word: 101 checks · 101 pass · 0 fail
collect-is-a-command: 133 checks · 133 pass · 0 fail
brief-is-printed: verify: 104/104 checks pass
101 checks · 101 pass · 0 fail
133 checks · 133 pass · 0 fail
verify: 104/104 checks pass
.pearde/…/collect-keeps-its-word/probe/verify.sh:run_old()     { ( cd "$D" && python3 "$OLD/board/collect.py" --board "$D/.pearde/prds" "$@" ) 2>&1; }
spec01: three suites, counts quoted above by name
```

The PRD's own `probe/verify.sh` (pass one, carried in) re-asserts the same
seven facts: `probe: 7 checks · 7 pass · 0 fail`, exit 0.

## No count moved under this run

Four sibling edits landed in the code repo between the analyst's baseline and
mine — `references/drill.md`, `references/parts/guard.md`, `parts/loop.md`,
`parts/round.md` modified, `resources/board/orphans.py` new, on top of the
`collect.py`/`plan.py`/`specs.py`/`transitions.py`/`doctor.sh`/`questions.py`
the analyst already saw. None moved a denominator: 101 / 133 / 104 are the
numbers spec01 recorded from disk. Nothing was back-edged.

## Footprint untouched

`git -C .pearde status --short` over the three footprint paths is empty — the
three harness files are byte-identical to their committed state. The only
files this run wrote are `specs/spec01.md` (six boxes ticked) and this report.

## Findings — none fixed, all outside this contract

1. **`collect` does not refuse this footprint; it silently drops it.** The
   round hazard predicted a refusal. What
   `python3 resources/board/collect.py --board …/.pearde <prd> --dry --as engineer`
   actually prints is exit `0` and a two-repo split:

   ```
   <prd>: repo /Users/feb/dev/infra/pearde/.pearde
     footprint: prds/the-collect-and-brief-harnesses-are-carried-across-the-layou
     would add: …/prd.md, …/probe/verify.sh, …/report.md, …/specs/spec01.md
   <prd>: repo /Users/feb/dev/infra/pearde
     footprint: .pearde/prds/…/brief-is-printed/probe/verify.sh, …/collect-is-a-command/probe/verify.sh, …/collect-keeps-its-word/probe/verify.sh
     would add: (clean — commit: none)
   ```

   The three `.pearde/prds/…` footprint entries are routed to the **code**
   repo, which ignores them (`.gitignore:17` = `.pearde/`) and does not track
   them (`git ls-files --error-unmatch` → "did not match any file(s) known to
   git"). The board repo, which does track them, is handed only
   `prds/<prd>` as its footprint. Net: an edit to a named footprint file would
   have been committed by neither repo, with no error. This run wrote none, so
   nothing was lost — but a footprint spelled `.pearde/prds/…` is unenforced,
   not rejected. Reported, not fixed: frontmatter is not mine to edit and
   `collect.py` is a sibling's live file.

2. **`doctor` gate exits 1 on two rows, neither mine.** `index broken` —
   `resources/board/orphans.py` is on disk with no row in
   `references/files.md`; that file is a sibling's untracked, in-flight work
   this hour. `origin broken` — `6 derived in flight vs 4 requested`, which the
   round predicts and which clears when the analysts land. Every other row is
   `ok` or `off`. `python3 resources/index.py check` exits 1 on the same single
   `orphans.py` problem.

3. **`harnesses` is still `off`** — `42 harnesses · not run`, no
   `harnesses: on` in `.pearde/settings.md`. The parent report's "nobody is
   being told" stands: these three suites are green and nothing routine runs
   them. A settings change outside this contract.

4. **Box 6 is satisfied by the weaker of the two permitted forms.** All three
   files derive `ROOT` by a fixed five-segment `..` count from the probe dir,
   not by walk-up to `resources/guard.py`. spec01 allows either, and the count
   resolves correctly from `/` — but it is depth-coupled: moving one of these
   PRDs a level deeper or shallower breaks all three at once, silently, in a
   way the walk-up form would not. Not a defect against this spec; a note for
   whoever next moves a board folder.

5. **`collect-keeps-its-word:40` `run_old`** passes `"$D/.pearde/prds"` to a
   pinned pre-move `collect.py` copy. Deliberate, documented, untouched — it
   is the back-compat assertion, not a stale path.

Nothing was learned outside this repo; no `knowledge.py remember` was owed.
