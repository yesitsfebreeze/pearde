# Round — container closed, two API-killed workers resumed on opus, graph-probe back DONE

> **Another session overwrote this file at 12:07.** A `/pearde`-adjacent
> session (`ca1fce64`) working a ⌘K search-palette feature in
> `resources/board/` wrote its own round notes over the board round's memory.
> Nothing of theirs was lost: their file is preserved verbatim at
> **`.pearde/.state/round.ck-search-palette.md`** and the one thing it says is
> owed — running `kskinds.js`, the 14-check kind-filter browser probe, then
> re-running the three regression suites — is still owed and is **not** this
> board round's work. That session should read its own file, not this one.
> This is a one-writer violation on `.state/round.md`; see **Decided** below.

## Established

- **the board at 12:20** — 85 PRDs. After this round's container collect:
  done 59/64 · 93% · derived 19/19 · open 3/85 · ready 0 · blocked 5.
- **`.pearde/` is its own git worktree.** `/Users/feb/dev/infra/pearde` is on
  branch `board-wiki-obsidian-work-together`; `/Users/feb/dev/infra/pearde/.pearde`
  is a **separate worktree on branch `pearde`**. Verified `git worktree list`
  11:56. This is why a collect writes two hashes — the code commit on the
  outer branch, the board record on `pearde`. The pairs earlier rounds
  recorded (`a90f539`+`97bf65c`, `eca3408`+`78357ed`, `5eee6e8`+`9a7ce2c`)
  are that shape, **not** a lost commit. `git status` means a different thing
  in each root; any worker asked for `git status --short` is asked for both.
- **page-report-agree's commit is not lost.** `bbfe9b5` (11:34:40) is on
  branch `pearde`, touches only that PRD's `prd.md`, `report.md`,
  `specs/spec01.md`, 163 insertions. Record sibling `602a218`, same second.
  Checked because the round file named a hash the outer branch's log does not
  show; the worktree is the whole explanation.
- **the round file's own clock drifts.** The 11:34 round file carried entries
  stamped 11:42–11:50 while the commits it names are 11:25–11:34.
  Worker-reported times run up to ~15 min fast. Trust commit times and `stat`.
- **there is no `pearde` on `PATH`** in a round window — drive the board as
  `python3 /Users/feb/dev/infra/pearde/resources/pearde.py <cmd>`, from the
  **repo root** (from `.pearde/workflows` the relative path resolves wrong).
  Every command needs `PEARDE_AS=engineer`.
- **the uncommitted tree is two sessions', now separable.** The ⌘K session
  (`ca1fce64`) owns `resources/board/serve.py`, `view.js`, `view.css`,
  `render.py` — `render.py` landed mid-run at ~12:05 and is why it appeared
  under a worker's feet. The memo/`.state`-move session owns
  `references/memo.md`, `references/parts/memos.md`,
  `references/parts/dispatch.md`, `references/agents/*.md`,
  `references/skills/pearde-memo.md`, `references/templates/memo.md`,
  `resources/memos.py`, `resources/index.py`, `resources/pearde.py`,
  `resources/board/transitions.py`, `README.md`, untracked
  `resources/board/example/memos/README.md`, and `doctor.sh:648`
  (`.plan.json` → `.state/plan.json`). **`resources/doctor.sh` also carries a
  second, unclaimed hunk** — see Owed.
- `readme-in-three-rings` and `workflow-skill` fail as a pair: the second
  asserts the first's baseline (`got 74 · 71 pass · 3 fail`, `want 74 · 74 ·
  0`), so one repair closes both. Red on the analyst's committed-tree
  baseline too. Unowned. (The older note that this was the `graph.json` /
  `knowledge.py doctor` red is superseded by the implementer's read.)
- **38 of 45 harnesses pin no denominator** — the sweep says so itself. That
  is the `an-acceptance-box-that-cannot-fail-is-refused` family's business.
- **the live view daemon is restarted by the `--harnesses` sweep** — pid moved
  7370 → 12235 → 75265. Five harnesses run `serve.py stop`, all five inherit
  an exported `PEARDE_PORT="$SPARE"`, so none reaches 8443 deliberately, yet
  the pid moves anyway and three registry members read `synced never` right
  after. Row ends `view ok · watching`. Churn the coordinator owns.
- `doctor.sh --harnesses .` renders the view row's board name as `?` —
  `http://127.0.0.1:8443/board/?` from a relative invocation vs
  `/board/pearde` from an absolute one. Cosmetic, makes the link unclickable.

## The model situation — read before dispatching anything

Three distinct walls, verified in transcripts at 11:56. They are not the same:

- **sonnet through litellm: 402 `reject_no_credit`.** Killed
  `implementer-graph` (pinned sonnet, ran 11:27→11:44). Account-level, not
  transient. Matches the 08-31 memory note.
- **the inherited default subagent group: 429 `litellm.RateLimitError` — "you
  (shadowhvlmnns) have reached your session usage limit … ollama.com".** This
  killed `analyst-fixtures` (11:29→11:49) **and the previous round worker
  itself** (died 11:48). So "own model (inherit, no pin)" — what the 10:25
  round chose — lands on an ollama-backed group that is now exhausted.
  **Inherit is no longer a safe re-dispatch target.**
- **opus works.** This window runs on it; every worker dispatched at 11:59 and
  after on `model: "opus"` has stayed alive.

**Decided: a re-dispatch pins `model: "opus"` explicitly.** Neither the sonnet
pin (402) nor bare inherit (429) survives.

## Decided

- **the ⌘K session's round file is preserved, not reverted.** Copying it aside
  and writing the board round's memory back beat both alternatives: leaving it
  (the next board round would resume from a stranger's feature notes and lose
  every fact above) and overwriting it (that session's fresh window would lose
  the one probe it has left to run). Both files now exist and each names the
  other. If this recurs, the fix is a per-session round file, not a race.
- **`graph-probe` was not collected off its ticked boxes at 11:55.** All 9
  were `[x]` and the board showed it in *collect*, but the first implementer
  died on the command after ticking the last one and wrote no report —
  `report.md` was still the **analyst's**, dated 11:02. Collecting on that
  would have closed the PRD on evidence nobody checked. Resumed instead,
  which is the loop's own rule for a worker its infrastructure killed.
- **all four workflow edits were the atomic's, and all four were applied.**
  None was the code's or the PRD's:
  - **E1** → `capture-the-harness-baseline` `## Done when`: "the recording
    happened before any file was written" is unsatisfiable for *any* second
    worker on a PRD, which is the ordinary case after a kill. Replaced with a
    this-run wording plus a **Resuming a killed run** bullet — record the tree
    as it stands, cite the dead worker's numbers as the only baseline, and say
    the baseline is inherited.
  - **E2** → same atomic, `## Do` item 2: the grep-for-footprint-paths rule
    **misses a board-enumerating harness**. This board's
    `the-gate-runs-the-harnesses` walks `find … -name verify.sh` and so reads
    every footprint that is itself a harness while spelling no path. Both of
    this PRD's footprint paths are harnesses, and that gate was the single
    most informative number of the run. A worker following the written rule
    would never have baselined it.
  - **E3** → `attempt-the-build` `## Fails when`, new row: proving a check
    *can* fail by mutating a **tracked-but-uncommitted** footprint file has no
    safe restore in the text, and `git checkout` is actively wrong there — the
    committed state is not the state to return to.
  - **E4** → same table: a line appended with `>>` concatenates onto the last
    line, because every harness here ends `[ "$FAIL" = 0 ]` with no trailing
    newline. An anchored matcher would miss the offender and the box would
    read green on a check that never fired.
- **`runs` bumped only where a step ran.** `probe-then-spec` 25→26,
  `read-the-contract` 45→46, `capture-the-harness-baseline` 45→46,
  `re-run-the-harnesses` 45→46. `attempt-the-build` (25) and
  `write-the-specs` (24) were `stopped (inherited)` — **no bump**, though
  `attempt-the-build` carries `updated: 2026-09-01` because E3/E4 changed its
  text. `probe-then-spec`'s own `updated:` was left at 2026-08-28: its text
  did not change. `pearde workflow check` rc=0 before the commit.
- the memo session's and the ⌘K session's hunks are left alone and are not
  collected. The implementer confirmed **zero** intersection with its own
  two-file footprint.

## This round's transitions

1. **11:57 — `the-round-is-handed-its-step-not-the-manual` collected.** The
   container whose every child was done: `open → done`, commit `eca3408`,
   record `298dc0b`. done 58/64 → 59/64.
2. **11:59 — `implementer-graph` re-dispatched** on `graph-probe-…`, as
   `pearde-implementer`, `model: opus`, brief + a resume note (boxes already
   ticked, first worker died on 402, `report.md` is the analyst's and must be
   overwritten, job is re-verification not rebuild, mark inherited steps
   `stopped`). Returned **DONE** at 12:07, 464 s, 23 tool uses.
3. **11:59 — `analyst-fixtures` re-dispatched** on
   `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool`, as
   `pearde-analyst`, `model: opus`, brief + a resume note (first analyst left
   nothing on disk; build starts fresh). **Still in flight at 12:20**, alive,
   no API error.
4. **12:2x — `graph-probe-makes-harness-sweep-unaffordable` collected DONE**
   after a skeptic consult. 9/9 boxes re-verified by the second implementer,
   none ticked on inheritance: spec01 `10 · 10 · 0` (2.1 s), spec02
   `4 · 4 · 0`, gate `57 · 57 · 0`, sweep `7 of 45 green · 89 s · 6 failed`
   none in footprint, `index.py check` 0, `doctor.sh` 0 all rows `ok`.
   Complexity 13, blast low. Footprint, both in the board worktree:
   `.pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh`,
   `.pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh`.
   The one count flip that is genuinely this PRD's:
   `the-gate-runs-the-harnesses` was red at census J `got 44 · want 45` and is
   now 57/57 — the probe now ends on `[ "$FAIL" = 0 ]` and this PRD's harness
   is the 45th. Counts that **rose** on `one-page-that-says-whats-up`,
   `scan-parses-…`, `tokens-per-transition`, `transitions-are-commands` are
   sibling sessions landing, claimed by nobody here.

## Owed

- **collect `the-fixtures-meet-the-tool` when its analyst lands.** SPECCED →
  `pearde specced <prd> --blast <x> --workflow <slug>`; REFINE →
  `pearde refine <prd> < report`; QUESTION → carry the fork to
  `.pearde/.state/ask.md` and hand back `ASK`. A **second** death on it is
  `BLOCKED` quoting the error — it has used its one re-dispatch.
- **gated, in this order, as their gates clear**:
  `the-doctor-completes-without-a-home` (needs `the-fixtures-meet-the-tool`)
  → `init-seeds-a-board-doctor-calls-green` (needs the doctor one) → the
  parent `seven-closed-probes-drifted-red` (needs all three children).
  Nothing else is dispatchable: `ready 0`, `blocked 5`.
- **`resources/doctor.sh` carries an unclaimed hunk that belongs to nobody.**
  At `doctor.sh:743`, `fix "… bash $START/<path above>"` → `<board>/<path
  above>` — the graph-probe *analyst's* own pass-one edit, outside that PRD's
  footprint, so the implementer correctly left it standing rather than
  adopting it. It is load-bearing for rows this round's numbers were taken
  against. **The orchestrator's call per @references/parts/derived.md**: give
  it a derived PRD (not `open`) or revert it. Not settled this round.
- **findings still unacted, candidates for derived PRDs**: the
  committed-harness mechanism is still missing; `reportParts()` in `view.js`
  parses only three of the report's four parts; the one-page harness lives in
  a git-ignored probe dir so it travels nowhere; a collect landed a sibling's
  pass-one code inside a shared `plan.py`; `transitions-are-commands` at
  64/74 (fixture has no round file for the drill gate) — though the sweep now
  reads it green, so re-check before acting; `scan-parse`'s 40 ms warm-scan
  bar does not reproduce (71–83 ms wall; walk+parse cold 5.8 → warm 4.0 ms).
- **parked, untouched**: `probe-code-lives-in-the-prd-folder`,
  `snapshots-fold-to-one-row`.
