# every-probe-harness-is-re-aimed-at-the-pearde-layout — implementer report

**DONE.** Spec01 re-verified end to end (13/13 boxes re-run, all quoted below)
and ticked as closed. Spec02 is the real work of this pass: all 22 footprint
files were re-aimed from the `<dir>/prds` board to the `<dir>/.pearde` board —
root derivations were already correct from the analyst's pass, the board-path
half was done here, following spec01's recipe: fixture board roots moved to
`$D/.pearde`, `PRDS="$B/prds"` added as the second variable wherever PRD
directories are addressed directly, `settings.md`/`vision.md`/`workflows/`/
`memos/` left at the board root, `.transitions.jsonl`/`.round.md`/
`.history.jsonl` moved under `.state/` (with the marked `mkdir -p
"<board>/.state"` workaround where a harness needs the dir before Python
writes it), `.view.html` moved to `.state/view.html` (the state-dir move), and
every `--board <x>/prds` rewritten to `--board <x>/.pearde`.

Nothing under `resources/` was touched. No assertion was added, removed or
weakened on purpose; every call-site census per footprint file is unchanged
between `HEAD:prds/<file>` and disk (verified file by file, 22/22 SAME).

## Both verify blocks, run verbatim

spec01 (all fourteen files, from the repo root and again by absolute path
from `/`):

```
a-parked-prd-comes-back       44 checks · 44 pass · 0 fail           (44/44 ✓)
the-gate-runs-the-harnesses   57 checks · 56 pass · 1 fail           (56/57 ✓)
an-unknown-flag-refuses       verify: 196 checks · 194 pass · 2 fail (✓)
collect-keeps-its-word        101 checks · 101 pass · 0 fail         (101/101 ✓)
collect-is-a-command          133 checks · 133 pass · 0 fail         (133/133 ✓)
specced-is-a-command          verify: 88/90 checks pass              (✓)
transitions-are-commands      74 checks · 59 pass · 15 fail; the named box
                              `ok   the line opens with the transition` passes (✓)
a-question-in-plain-words     0 FAIL lines                           (✓)
hunks-land-where-they-came    47 checks · 47 pass · 0 fail           (✓)
the-loop-is-commands          60 checks · 59 pass · 1 fail           (✓)
init-asks-nothing             89 checks · 76 pass · 13 fail          (✓)
init-writes-a-board (check.sh) PASS, exit 0, from repo root and from /   (✓)
abs-path-from-/: all twelve resolve their root to /Users/feb/dev/infra/pearde (✓)
```

spec02 (the twenty-two files, from `/` by absolute path), with the board-path
gains this landing bought:

| file | arrival | now | left, and why it is not this PRD's |
|---|---|---|---|
| guard-on-is-one-command | 64/78 | **78/78** | — |
| one-predicate-for-dispatchable | 23/53 | **52/53** | `references/parts/board.md` no longer carries the `container` wording the last check greps (doc drift) |
| one-command | 43/54 | **51/54** | plan.py's no-board message is now `no .pearde/ board found walking up…`; `memos.py`'s checker grew `memo:`/`kind:`/`status:` requirements — both `resources/` behavior change |
| brief-is-printed | 41/104 | **100/104** | brief template prose drift: `<board>` now fills, worker.md's "never under `prds/`" clause rewritten by the rename round |
| the-page-shows-the-round | 14/29 | **27/29** | the two serve-half checks fail against a daemon whose in-memory build predates the 18:29 serve.py — started 15:50, never restarted |
| too-big-splits-itself | 16/60 | **60/60** | — |
| tokens-per-transition | 3/43 | **42/42** | the 43rd check lived behind the playwright branch; the count line is the file's own denominator, unchanged |
| vision-is-first-class | 18/52 | **51/52** | `references/parts/order.md` now writes `.pearde/vision.md`; the check pins `prds/vision.md` (doc drift) |
| the-next-line-runs | 70/96 | **84/96** | `add`'s row records `prds/<slug>` (the `add()` rel bug in `resources/board/transitions.py`); `pearde init` in the copy dies writing `.obsidian/.../data.json.tmp` — init feature grown since |
| an-example-board | 30/37 | **37/37** (1 skip: playwright) | — |
| readme-in-three-rings/quickstart.sh | 24/31 | **29/31** | `install --apply` builds 14 skills / 70 links, the check pins twelve / 60 (install grew pearde-graph + pearde-knowledge) |
| readme-in-three-rings/verify.sh | 65/72 | **66/72** | loop.md row-drift (D), twelve-skills (F), `skills/pearde.md` absent at the repo root (G ×2, pre-existing), quickstart's two (H ×2) |
| workflow-skill | fails at its first check | **45/55** | the rename moved `skills/` → `references/skills/` and rewrote registration (`files.md` holds no `@skills` rows; the twelve/15-hunks pins are stale) — the rename PRD's, not the re-aim's |
| workflow-improve | 63/71 | **70/71** | `references/parts/workflows.md`+`round.md` no longer carry the refusal-to-round-file sentence (doc drift) |
| workflow-attach | 29/46 | **44/47** | the two master-member scan checks fail on the `members()` double-`/prds` resources bug; `workers.md` lost `workflow: none fit` (doc drift) |
| workflow-reader | 5/39 | **39/39** | — |
| workflow-seed | 33/48 | **68/68** | — |
| the-skill-tree-is-guarded | 22/41 | **41/41** | — |
| check-crosses-member-boundaries | 6/18 | **7/18** | `plan.py members()` + `_scan_one()` double-`/prds` empties every master fixture; list-valued `workflow:` behavior changed in workflows.py — both `resources/` |
| complexity-is-guarded-like-priority | 19/61 | **61/61** | — |
| one-page-that-says-whats-up | 22/30 | **22/30** | every failure is a stale repo-layout assertion (`prds/.round.md`, `prds/report.md` gitignore and page rules) — the report PRD's own update; no fixture or board path involved |

Census: `find .pearde/prds -name '*.sh' | xargs grep -l -- '--board [^ ]*prds'`
returns exactly one file, `collect-keeps-its-word/probe/verify.sh` — the
standing exception the spec names (`run_old` drives a pinned pre-move
`collect.py`), outside this footprint. No file in either footprint hardcodes a
machine path; the four `/Users/feb` hits board-wide belong to
`tokens-per-transition`'s NODE_PATH fallback (a pre-existing default, not a
root derivation) and to three PRDs collected before this one.

## Findings carried forward (confirmed from disk this round, left unfixed)

All six the analyst reported are still present and untouched:

1. `transitions.py add()` computes `rel` against the board root — rows read
   `prds/<slug>`, and the-next-line-runs' `"prd": "a-first-title"` check now
   fails on it.
2. `plan.py members()` appends `/prds` and `_scan_one()` adds it again — the
   master fixtures in check-crosses and workflow-attach see zero member PRDs.
3. `specs.py` refuses `--workflow none` outright.
4. `specs.py` imports `datetime`, outside specced-is-a-command's allow-list.
5. `brief.py` gained `--worker`, unpinned in an-unknown-flag-refuses.
6. `collect.py transition_row()` opens `.state/transitions.jsonl` without
   `makedirs` — every re-aimed fixture carries the marked `mkdir -p`.

New findings from this pass, all outside the footprint:

7. The live daemon (PID 14977, started 15:50 today) predates the 18:29
   serve.py — every served-half assertion in the board measures a stale build.
8. `one-page-that-says-whats-up`'s eight failures are stale repo-layout
   assertions renamed by the report PRD's round; that harness's update belongs
   with the report PRD.
9. `resources/board/example` stays the pre-move shape on purpose — it is the
   template copied INTO `<dir>/.pearde`, and `plan.py example <dir>` writes
   `<dir>/.pearde`, re-confirmed empirically this round.

## Notes for the orchestrator

- nothing-left-open/the-line-tells-the-truth and a-quoted-walk-is-data share
  probes with this footprint; their already-correct patterns were left
  untouched, and of the five boxes the pointer names, all stand green except
  the two statuses the pointer itself marks as not this PRD's.
- No commit was made; the only `prds/…` lines this run wrote outside its own
  PRD folder are the footprint files above.
