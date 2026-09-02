# Pass — cap PRD proven under collect's runner, one commit away; a new requested PRD filed; a sibling session is renaming round→pass in the same tree

Written by session `8a88cea0`, 2026-09-02 ~10:40 CEST. **One transition
landed** (`a-session-start-brings-the-board-up` filed `open`). HEAD `bc1c589`.
This file was `.state/round.md` until the sibling session's rename moved it;
the guard now names `pass.md`, and this is the file the next pass reads.

## Read this first: a live peer is mid-rename in this working tree

A second `claude` session (pid 1936 or 3434, ~1h old) is renaming
**round → pass** across the repo: ~40 files modified, `references/agents/pearde-round.md`
→ `pearde-pass.md`, `references/parts/round.md` → `pass.md`, and it touched
`resources/doctor.sh` (7 comment/string hunks) and `references/parts/doctor.md`
(3 hunks) — both in the cap PRD's footprint. **`collect` stages a footprint
file whole**, so a plain collect would commit the peer's half-rename under the
cap PRD's name. Do not `git add`/commit anything that is not yours; do not
touch its files beyond the lift/re-apply below; never amend its HEAD.

## Established

- Previous pass's implementers lived in session `f54db065`'s process; the
  restart ended it. Re-dispatched, not messaged. 09:13.
- Cap PRD: bounded implementer `a0cfb56eaeb0958bb` (opus) ran spec01's
  block, 20/20 boxes, `Verdict: DONE` at 09:35.
- **Collect #1 refused 09:42, `spec01 exit 1`**: collect runs blocks under
  `bash -e -o pipefail` (`collect.py:1057`); `doctor.sh --harnesses | sweep`
  with any red harness aborted the block. The spec's defect (the atomic's
  Fails-when row 3 already names it). Fixed 09:47: producers guarded
  `{ … || true; } | sweep`, `diff && echo` → if/else.
- **Collect #2 refused 10:21, `spec03 exit 1`** — but **spec01 exit 0 under
  collect's own runner**: `capped: 1 contention red across five runs` ·
  `uncapped: 2 in one run` · `MET` (log: scratchpad `collect-cap.log` lines
  26-36). spec02 exit 0. spec03 failed on its leak check, which counted
  `$TMPDIR/tmp.*` machine-wide: `2461 -> 2471`, ten dirs made by the peer
  session mid-run — a check decided by scheduling. Fixed 10:35: the harness
  runs under a TMPDIR of the block's own and that dir is counted.
- Workflow riders staged for the cap collect (`--also workflows/<x>.md`,
  board-relative — right for the probe `also_path` on disk): runs 32→33
  `probe-then-spec`, `attempt-the-build`; 53→54 `read-the-contract`,
  `capture-the-harness-baseline`, `re-run-the-harnesses`; `write-the-specs`
  Fails-when: the `grep -c` row replaced by the worker's two rows verbatim,
  `updated: 2026-09-02`. `workflows.py check` green 09:44.
- Scratchpad `/private/tmp/claude-501/-Users-feb-dev-infra-pearde/8a88cea0-1f9d-4c24-86ce-bc98939e5be1/scratchpad/`
  holds: `doctor-sh-cap.patch` (hunk @735 — the cap's) and
  `doctor-sh-other.patch` (8 hunks: the brief PRD's @577/@585 + the peer's
  6); `doctor-md-cap.patch` (@85, +17) and `doctor-md-other.patch` (3 peer
  hunks). Both `-other` patches `git apply --check -R` clean at 10:38.
  `brief-file.md` is the filing PRD's brief; `brief-cap.md` the cap's.
- New requested PRD `a-session-start-brings-the-board-up` filed 10:25 via
  `pearde add`, p40, body written from the user's words and the dispatcher's
  verified context (no launchd, no SessionStart hook, `install.md:186`
  claims what nothing does; decision: a SessionStart hook running
  `serve.py ensure <board>`, installed beside the guard hooks, reported by
  doctor). Needs an analyst.
- Requested active: filing, cap, four-stale, brief, session-start = 5.
  Derived active: collect-stages, leaked, two-self-tests = 3. After cap and
  filing go `done`: 3 v 3 — **tripwire trips**; the fork is this pass's ASK.
- `knowledge.py query` on the tripwire: keyword noise only, no answer. 09:30.

## Decided

- Skeptic consult before `done` on the cap PRD: not called — the number was
  measured three times by two workers plus once by collect's own runner, and
  the acceptance is the user's rewording.
- Cap collect goes `--trust` in a seconds-long window: lift both `-other`
  patches, `collect --trust`, re-apply both. spec01+spec02 were proven by
  collect #2's own run; spec03 by a hand run under `bash -e -o pipefail`
  (result below). A 15-minute re-run while the peer edits the same two files
  is the worse risk.
- Q1's answer applied to filing PRD spec01 (09:19): box 6 inverted, a
  precedence box added, all ten boxes unticked. `also_path` at
  `collect.py:128` is the function to change.
- Memo `also-drops-a-path-it-cannot-find` → superseded by new memo
  `also-resolves-against-the-board-first`; index regenerated; check green
  09:17. All three ride the filing PRD's collect (`--also memos/...`).
- Filing implementer dispatched only after the cap collect lands.

## Asked

- Q1–Q6 of the 08:xx drill · answered
- The derived tripwire fork · not yet put — `ask.md` at end of pass

## Edits

- `write-the-specs` `## Fails when` — applied (two rows replace the `grep -c`
  row) · the atomic's
- `capture-the-harness-baseline` — the previous pass's edit stays withdrawn
  by its own author

## Owed

- spec03 hand run result → if 0: `git apply -R` both `-other` patches;
  `collect the-harness-sweep-… --trust --report … --also (six workflow
  files) --also-note …`; `git apply` both `-other` patches back; `git show
  --stat HEAD`, `git status` in repo and `.pearde`. Then dispatch the filing
  implementer (opus, brief at `brief-file.md`), hold, collect it with the
  memo riders. Then `ask.md` (tripwire) → `ASK`.

## Carried — still true, cite do not re-derive

- `pearde answer` cannot write `## Answers` on a template PRD (`edit.py:79`
  substring match). Check `questions list` after every `answer`. Unfiled.
- `verdict_of` accepts only a bare line beginning `Verdict:`.
- The brief PRD's fix belongs in `brief:every` (`brief.py:340`); its
  doctor.sh hunks @577/@585 and `brief.py`/`workers.md` mods are its
  analyst's pass one.
- `the-fixtures-meet-the-tool` reddens on uncommitted `resources/` work.
- Four-stale PRD forbids editing `render.py:459` / `view.css:508`; its
  spec04 reads `workers.md`, which the brief PRD rewrites — brief first,
  four-stale last, never parallel.
- Sandboxed `date` lags the host ~6.7h; sandbox off when the clock matters.
- `PEARDE_AS=engineer python3 /Users/feb/dev/infra/pearde/resources/pearde.py …`
  absolute. sonnet 402s; pin `model: opus`. `--also` needs `--also-note`.
  A background Bash is capped at 10 min; a collect that re-runs sweeps
  outlives it — run it foreground in 10-min holds or use `--trust`.
- Leaked `serve.py` daemons: recount after the restart is the baseline.
- Noted, unfiled: `vision` init/upgrade divergence; `obsidian.json` dead
  vaults; `knowledge.py board` counts `memos/README.md`; four-stale body
  cites `resources/view/…` for `resources/board/…` files.
