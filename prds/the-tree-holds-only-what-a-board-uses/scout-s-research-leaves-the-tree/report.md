# scout's research leaves the tree — implementer report (redo pass)

Verdict: DONE

Claim: impl-redo-scout-s-rese 2026-09-03 21:38. Second pass on the
`probe-then-spec` route: the analyst's build and specs stand, the first
implementer's session was reaped after committing the lane, and this pass
re-measures and applies the `Fails when` tables to the blocks that already
stand, without authoring a spec.

## Carried forward from the analyst's pass (by name)

Every finding in the analyst's `## Findings` above stands as reported and none
was closed by this pass:

- **The advertised verb goes with the files** — `/scout reading` and
  `/scout quality` retired with `reading-list.md` and `templates/`.
- **The board's wiki is the same GitHub repository** — `.pearde/`'s origin is
  `github.com/yesitsfebreeze/pearde.git`, `pearde` branch; leaving the tree is
  not leaving the repo. If leaving the repository was the intent, spec02 is the
  wrong destination and only the author can name the right one.
- **Frontmatter is what makes the wiki a destination** — a `.md` in
  `wiki/sources/` with no fence reddens `knowledge.py doctor` with
  `no frontmatter`; non-markdown files must ride in `attachments/`.
- **A wrong claim outside this scope** — `references/knowledge.md` says every
  verb takes "`--root` per board"; `--root` is the wiki directory, not a board.
  Not fixed; no spec here owns that prose.
- **A defect outside this scope** — `resources/index.py check` problems at
  HEAD belonging to some sibling or nobody (see Baseline below: the set has
  grown from four lines to twelve, still none naming this footprint).
- **The PRD's arithmetic checks out** — 1,847 lines measured at HEAD.

## Workflow probe-then-spec

| # | atomic | verdict | note |
|---|--------|---------|------|
| 1 | read-the-contract | ok | prd.md, both specs, the analyst's report read; `git status --short` recorded in both roots before any edit (code repo: `M resources/board/collect.py`, a sibling's live work, not mine; board repo: state files and other PRDs' files, not mine; lane: clean) |
| 2 | capture-the-harness-baseline | ok (inherited) | the earlier build is **committed** (lane f116e5f; board repo 3bf5ead), so there is no pre-edit tree to recover; the analyst published counts and the harnesses are deterministic, so per the atomic the inherited baseline was **confirmed** by re-running the same set on the built tree and matching it — named pass: the analyst's, 2026-09-03 |
| 3 | attempt-the-build | ok (second pass) | entered for both specs as footprint verification only; nothing was built. spec01's build stands in the lane at f116e5f; spec02's build stands in the board repo — its nine files were **committed by a sibling's collect**, 3bf5ead "ramp-is-a-doctor-row-not-a-gate" (2026-09-03 12:27), which took the first implementer's uncommitted wiki files with its own (attempt-the-build `Fails when`, the sibling-committed-the-tree row) |
| 4 | re-run-the-harnesses | ok | no board harness names any footprint path (`grep -rl --include=verify.sh` over all eight footprint paths over `prds/` — zero files), so the measured set is the repo gate plus both spec blocks; every count equal to the published baseline; flips claimed: none |
| 5 | write-the-specs | ok (no authoring) | no spec authored; the `Fails when` tables were applied to the standing blocks — both run as `collect` runs them (`bash -e -o pipefail` over the awked fence), one re-aim below, both proved falsifiable |

### Edits

One failure the atomics caused, one edit:

- `specs/spec02.md`, Verify and Proof block, the line backing box 7 — as it
  stood: `git -C .pearde status --short -- wiki/sources/scout | grep -q 'scout-findings-index-2026-08'`
  — as it now reads: `git -C .pearde ls-files -- wiki/sources/scout | grep -q 'scout-findings-index-2026-08'`.
  Reason: the box's words are "the board repo commits its own"; a sibling's
  collect committed the notes at 3bf5ead, so the literal `status --short`
  grep can only fail *before* the merge and reads red on the pass state the
  box names. The re-aim asserts the shape that still meets the box — tracked
  in the board repo — and is not weaker: the block's own `test -f` lines fail
  on a deleted working file and the `ls-files` grep fails on an untracked
  one. Proved both ways: `git -C .pearde ls-files -- wiki/sources/no-such-dir | grep -q …` → rc 1, and the whole block with
  `scout-findings-index-2026-08.md` moved aside → rc 1; file restored,
  `cmp` byte-identical. No other line, box or frontmatter key moved, and no
  other spec file was touched.

## Per-spec status — 7/7 boxes green, both specs

### spec01 — resources/scout holds only tool files (7/7 `[x]`)

Ran in the lane, as `collect` will: `bash -e -o pipefail -c "$(awk …)"` →
`spec01 green`, rc 0. Output quoted:

```
index.py check — 3 line(s):
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk
  skills      ok      19 well-formed · pearde-all pearde-doctor … (19 named)
spec01 green
```

The lane's `index.py check` is down to three inherited lines, none naming
`resources/scout`. Falsifiable: appending `<!-- see findings.md -->` to
`resources/scout/routes.md` in the lane → block rc 1; restored, `cmp`
byte-identical.

### spec02 — the research lands in the board's wiki (7/7 `[x]`)

Ran from the code-repo checkout root (the block reads `.pearde/wiki/…`
relative and `git show HEAD:resources/scout/...` against checkout HEAD, which
still holds the departing files): → `spec02 green`, rc 0, with
`doctor: clean — 114 notes, graph in sync, pending honest` and the query
returning `scout-findings-index-2026-08` among its hits. All seven
attachments `cmp` byte-identical to `git show HEAD:resources/scout/...` in
the code repo. Falsifiable as described under `### Edits`.

## Baseline (inherited, confirmed)

No board harness touches the footprint, so the baseline set is the repo gate —
`python3 resources/index.py check` + `bash resources/doctor.sh` — plus both
spec blocks, exactly the set the analyst published.

- `index.py check` in the **lane**: three lines (above). In the **checkout**:
  twelve lines — the analyst's four, plus eight that landed since from other
  sessions' work (`resources/board/obsidian_register.py` with no row; six
  `@docs/*` rows; `@resources/board/purge.py`; `@@purge` in
  `references/parts/handles.md`; `@@docs`). None names this footprint; all are
  inherited and quoted for the next reader. The analyst's own extra finding —
  `resources/common.py` with no row and the deleted `hotreload-test.js` —
  still stands in both roots.
- `doctor.sh` (checkout): `skills ok · 19 well-formed`, `plugins ok`, matching
  the analyst's baseline; `index broken — 13 problems` and `claims broken — 7
  drifted names`, all inherited, none naming this footprint. `doctor rc=0`.
- `knowledge.py --root .pearde/wiki doctor`: `doctor: clean — 114 notes`,
  as published.

Flips claimed: none. Counts that changed against the published baseline: only
the inherited `index.py check`/doctor lines above, all naming files outside
the footprint, all explainable by sibling sessions' landings — not mine.

## Health floor

No footprint file is under the health floor; nothing to move. One live
sibling hunk sits in the code repo (`M resources/board/collect.py`) — not
mine, not touched. A split outside scope: none observed.

## Knowledge

`python3 resources/knowledge.py remember "an acceptance box asserting git
status shows the new files goes stale the moment a sibling's collect commits
the board repo"` → `sources/260903-949d.md · [[260903-949d]]` (provenance:
this run's spec02 line 91). It landed untracked in the board repo, where the
board's own commits will take it.

## Failure

None.