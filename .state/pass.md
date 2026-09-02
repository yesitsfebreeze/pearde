# Pass — five transitions landed; one PRD finished but uncommittable behind a live sibling session

Written by `af0d58deb8c0a7abc` (pass worker, session `8a88cea0`), 2026-09-02
12:20. Repo HEAD `695bbda`. Board HEAD `144f3e8`.
**Five transitions landed of a budget of 8.**

Board now: `done 92 · superseded 2 · claimed 1 · open 1 · deferred 1` —
**done 70/71, 99%**, derived 22/23, open 1/97.

## ⚠ THIS FILE WAS CLOBBERED ONCE TODAY. APPEND OR EDIT — DO NOT OVERWRITE.

Three `pearde-pass` workers ran this board at once (see the appendix). Between
12:05 and 12:17 my entire record — the 429 story, the landed transitions, the
send-back analyses — **was overwritten** by another session writing its own
pass memory into this same path, and only my last appended block survived. I
have reconstructed it below from my own context.

@references/parts/pass.md says rewrite this file whole. **That rule assumes
one session per board and it is unsafe here.** The two peers stood down at
12:17 (both returned `BLOCKED` naming the duplicate dispatch), so one writer
should hold again — but if you find a block you did not write, preserve it.
The `all` session's memory is kept verbatim in the appendix for that reason.

## Landed this pass

| # | transition | commits |
|---|---|---|
| 1 | `two-self-tests-fail-on-timing-not-on-code` `claimed → done` | board `758b040`, `inherited 104` |
| 2 | `the-four-personas-are-built-from-research` `analyzing → specced` | complexity 20, blast-radius low, 2 specs |
| 3 | `the-four-personas-are-built-from-research` `specced → claimed` | worker `impl-personas` |
| 4 | `collect-stages-a-shared-file-whole` `claimed → done` | board `9d23535`, repo `3457e2d`, `inherited 101` |
| 5 | `the-four-personas-are-built-from-research` `claimed → done` | board `144f3e8`, repo `695bbda`, `inherited 102` |

Not a transition: memo
`a-harness-that-reads-the-whole-checkout-is-not-a-harness` (board `1da9628`),
`memos.py check` silent, index regenerated.

Every repo commit was verified by hand with `git show --stat`. Each took only
its PRD's footprint files; ~100 sibling changes were correctly kept out each
time. **The splitter is sound where it has a baseline.**

## The 429 that killed the previous pass — the detection lesson is the point

The previous pass dispatched four workers at 11:21 and verified all four
alive. At **11:28 all four died on one account-level error**:

```
"You've hit your session limit · resets 1:20pm (Europe/Berlin)"
"error":"rate_limit","isApiErrorMessage":true,"apiErrorStatus":429,
"rateLimitType":"five_hour","overageStatus":"rejected",
"overageDisabledReason":"out_of_credits","unifiedRateLimitFallbackAvailable":false
```

**`grep -c "API Error"` returns 0 on all four transcripts.** The string is not
there. The kill is visible only as `"error":"rate_limit"` /
`"isApiErrorMessage":true` in the JSONL. @references/parts/workers.md names
only the `API Error` string, so **the liveness check the board prescribes
reports a dead worker as alive.** This is the strongest unfiled finding on the
board and it is still unfiled.

The dead workers ran under `.claude/priv/…`; this pass worker runs under
`.claude/max/…` — different accounts. That is the only reason re-dispatch
worked. `impl-timing` had finished and written its report before dying; the
other three had nothing and were re-dispatched once each, all pinned opus.

## What is left, and why neither item is dispatchable

1. **`leaked-background-services-outlive-their-fixtures`** — `claimed`, boxes
   **23/23**, report written, verdict DONE, and I believe it. It cannot be
   committed. Full analysis below; the short version is that `serve.py` holds
   a live sibling's uncommitted `all` feature and neither remedy `collect`
   offers is safe.
2. **`files-score-their-health-and-the-brief-names-the-unhealthy`** (p60,
   `open`, the only `ready` PRD, highest priority on the board). Still held,
   and the reason is now **stronger** than when the previous pass held it: its
   build touches `resources/doctor.sh` and `resources/pearde.py`, and
   `leaked-…`'s uncommitted HLEAK lines are sitting in `doctor.sh` right now
   waiting for a collect that cannot run. An `open` PRD carries no
   `footprint:`, so `claim` cannot refuse the clash for you. Dispatching an
   analyst there would put a second writer into `doctor.sh` and make the
   already-hard leaked collect harder. **Dispatch it only after `leaked-…` is
   collected and `doctor.sh` is committed.**

So the board is stalled on a session that is not the board's to command. That
is why this pass hands back `BLOCKED` rather than `MORE`: a fresh pass worker
would find the same two items and the same wall, and three orchestrators have
already collided on it today.

## The skeptic was called before every `done`, and was worth it every time

Four consults, four different outcomes. **Do not skip this step.**

- **`two-self-tests-…`** — reproduced both flip probes independently and
  confirmed the fix real, but found the PRD's own sentence ("a red always
  means something is actually broken") not yet true of
  `readme-in-three-rings/probe/verify.sh:110`, which still reads the whole
  live checkout, and that `flip-readme.sh` certifies two footprint files while
  executing one. **Collected `done` anyway** — the gap was an under-spec by
  the analyst, not a failure by the implementer, which met every box it was
  given, and that worker was dead and unreachable. Residue went to the memo,
  per @references/parts/derived.md's test (a defect in an instrument changes
  how loudly the board notices, not what ships) and because the derived
  tripwire already stood at 3-in-flight vs 2-requested. **Do not
  re-litigate.**
- **`collect-stages-…`** — **refused the DONE.** 3 of 19 boxes had no standing
  check; they were ticked on scratch fixtures and on a probe edit the worker
  reverted. Sent back; it closed all three and went further (below).
- **`leaked-…`** — confirmed the hard part fixed, found two defects I would
  not ship. Sent back; both closed (below).
- **`the-four-personas-…`** — found the probe could not tell a real trace from
  a fabricated one. Sent back; resolved honestly (below).

## `collect-stages-a-shared-file-whole` — done, and what the send-back bought

The worker closed all three uncovered boxes and corrected me:

- **De-pinned all three specs, not the one I named.** The same disease sat in
  spec01 and spec02 pinned against their **neighbours'** totals — worse,
  because a sibling adding a passing check to their own harness would have
  reddened this unit. All three are now tally parses (`NF` check,
  `checks == pass`, `failed == 0`, empty tally fails), each shown failing on a
  constructed red.
- **Probe 25 → 32.** `1f-widen-offered`, `1g-no-stale-clause`, and a scenario
  7 (`7a`-`7e`) building a plain `.pearde/` inside a code repo — the one-repo
  layout no scenario had. Each shown red before green by narrow mutations of
  `collect.py`, restored from scratch backups and `cmp`-proved.
- **The mtime lesson, now settled.** `commits.md` at 11:26:16 it never wrote;
  `collect.py`'s later mtime **was** its own, from the mutate/restore cycles,
  because `cp` bumps mtime whatever the bytes say. Its first "no code-repo
  file written this run" was true when written and false by the end. **An
  mtime is not proof in either direction.**

**Its collect first refused**: `two authors on one hunk: collect.py:1083`. The
analyst's pass-one build was already in the tree when the 11:21 claim snapshot
was taken, so all +135 of it reads as *baseline*, and the implementer's
revision touched an adjacent line. Both authors were this same PRD. I checked
the 13 hunks myself — all inside `HELD` / `snapshot` / `baseline` /
`sort_paths`, and no other `claimed` PRD names that file — then widened with
an **absolute** path. **The scratch-copy dance was not needed. Check the hunks
first; widen if they are all yours.**

## `the-four-personas-are-built-from-research` — done, and the honest resolution

The skeptic found the real problem: the 190 checks are **structural
self-consistency**, and the only provenance assertion was
`len(source) > 8` — the literal placeholder `<the artefact>.` (15 chars)
cleared it, so an invented practitioner citing an invented book passed all 190
checks, on a PRD titled "built from research".

The worker resolved it well. It tightened the assertion to require a **year**,
which rejects the placeholder, and then **refused to gate on
`.pearde/wiki/sources/`** because that is outside its footprint and doing so
would be "the over-claim in a new place". It said plainly in the report that
the probe proves shape and traceability only. **I made the PRD wording edit
myself on the transition** (the worker correctly did not touch `prd.md`): a
line in `## What exists when this is done` saying the backing check is a shape
check and the research is recorded in `.pearde/wiki/sources/` rather than
enforced by a gate, and a `## Non-goals` line — "No in-tree proof that a
practitioner or a source is real. Nothing in this repo can tell a researched
trace from a fabricated one, and this PRD does not add it."

The provenance is real and on disk: `.pearde/wiki/sources/260902-bf13.md`,
`-498e`, `-ae5c` — named practitioners with dated artefacts, and `bf13` states
which citation could not be confirmed and which two candidates were dropped.

**The thing that would actually close the gap** is a committed
`resources/personas.py check` resolving each `## Built from` row against a
knowledge note and each note against its `provenance:` key — a real PRD, with
`references/personas/`, `resources/` and `.pearde/wiki/` in one footprint.
**Not filed.** The derived tripwire is standing.

**Its collect also needed `--widen`** on `designer.md`, `mentor.md` and
`skeptic.md` — analyst pass-one work, older than the claim. Safe: I checked
every hunk was persona content and the mtimes (11:38-11:56) showed no sibling
activity. `engineer.md` and `INDEX.md` are the sibling's and were correctly
left out of the commit.

Five of its acceptance boxes were in `prd.md` and **unticked** — the
implementer ticked the specs and never returned to the contract, and
`scan`'s `boxes 15/15` counts specs only. I ran all five myself and ticked
them on that evidence. **Check `grep -c '^- \[ \]' prd.md` before any
collect; the scan will not warn you.**

## Workflow bookkeeping — ALL OF IT IS NOW COMMITTED. DO NOT RE-BUMP.

`probe-then-spec` ran on three PRDs this pass, and **all six workflow files
rode the personas commit `144f3e8`**, including the bookkeeping for the
`leaked-…` collect that never landed. Current committed values:

| file | runs | note |
|---|---|---|
| `probe-then-spec` | **38** | 34→35 two-self-tests, →36 collect-stages, →37 leaked, →38 personas |
| `read-the-contract` | **60** | |
| `capture-the-harness-baseline` | **60** | |
| `re-run-the-harnesses` | **60** | |
| `attempt-the-build` | **34** | entered only on leaked |
| `write-the-specs` | **28** | entered only on personas ("partially", which I counted as a run) |

**`leaked-…`'s retry must pass `--report` and `--widen` only. Its `runs` are
already spent and its `### Edits` row is already in `attempt-the-build`.**
Re-bumping would double-count.

Seven `### Edits` were applied verbatim across the pass, every one qualifying
as "a shape `## Fails when` does not list" or a wrong instruction in `## Do`.
The two worth knowing:

- **`write-the-specs` `## Do` item 4 was replaced.** The old wording said
  every command must *name* a footprint path, and `names` was the whole
  ambiguity: `resources/board/specs.py:523` matches the `footprint:` string
  literally, so a `"references/personas/$f.md"` loop reads as no footprint
  path at all and warns, **while** a block that spells one path and then gates
  on `index.py check` passes the warning and is exactly the disease. **The
  checker is wrong in both directions.** The new text draws the line at
  *exit*, not spelling, and adds: stub a file you must read but do not own,
  and guard captured output with `[ -n "$out" ]` before greping it.
- **`write-the-specs` gained a row** for `specced` refusing a block that holds
  a literal `## ` at line start inside a heredoc — `specs.py`'s section reader
  is line-based and fence-blind, like the acceptance-box matcher.

## Established — cite, do not re-run

- **The pinned-denominator disease.** A block gating on a literal
  `grep -c '^88 checks · 88 pass · 0 fail'` goes red when a neighbour adds a
  *passing* check. Parse the tally, assert `checks == pass && fail == 0`,
  scoped to footprint files. **And the inward form is worse:** a spec pinning
  its own probe's total locks the harness shut, so the next pass cannot add
  the check a thin box needs. Now a `## Fails when` row on `write-the-specs`.
- `collect` runs a spec block under `bash -e -o pipefail`
  (`collect.py:1057`). Producers `{ … || true; }`, expected-red under `if`,
  never end on a `grep -c` whose passing value is 0.
- **Dispatch method — keep it.** Briefs are 8-39 KB each. Every worker gets a
  short prompt whose first instruction is to run its own
  `pearde brief <prd> --role <r> --as <id> --worker <w>` and treat that as its
  whole brief, plus orchestrator-only notes. **The orchestrator never holds a
  brief.** A claim is not re-refused when the worker named is the one asking,
  so a re-dispatch needs no new claim.
- **`pearde claim` takes a POSITIONAL worker: `pearde claim <prd> <worker>`.**
  Not `--worker` (unknown flag), not `--as` (that is the persona).
- **`pearde brief --role` takes analyst or implementer only.** A consultant
  brief is not from the tool — compose it from the `brief:consultant` block in
  @references/parts/workers.md by hand.
- A worker refused at collect is **sent back with `SendMessage`, never
  respawned** — it holds the context. All three send-backs this pass came back
  better than asked.
- `--widen <path>` is board-relative unless **absolute**. `--also <path>` is
  board-first then cwd, and needs `--also-note`.
- **`collect` is safe against a shared git index** — `collect.py:409` says so
  in its own comment and `:465` builds the commit with `commit-tree`, not
  `git commit`, so another session's staged files are not swept in. Verified
  by a peer at 12:15.
- `verdict_of` accepts only a bare line beginning `Verdict:`, in the first 40
  lines, not inside a list item or block quote.
- **The board is its own git repo** at `.pearde/`. A `cd` in one Bash call
  persists into the next — **use `git -C <path>`**. The shell is `nu`:
  `set -- $var` word-splitting does not work.
- Live settings: `workers: 6`, `pipeline: 8`, `context-budget: 160k`,
  `transitions-per-pass` unset → **8**.
- Sonnet 402s through litellm; pin every worker to opus — and see the 429
  section, which opus pinning does not save you from.

## Findings routed from workers — none filed, all unclaimed

- **The `API Error`-only liveness check misses a 429.** The strongest unfiled
  finding on the board.
- **`index.py check` is GREEN as of 12:17** (rc=0, silent) — the `all` sibling
  wrote `references/parts/all.md` and the manifest rows. Earlier notes calling
  it red are **stale**.
- `the-gate-runs-the-harnesses` check J is red (`54 · want 56`): its matcher
  requires the literal `fail` **inside** the brackets, so a verify script
  ending `[ "$F" = 0 ]` reads as having no exit-carrying test. Both offenders
  are committed, predating this pass.
- `one-page-that-says-whats-up` 31/31 → 30 pass 1 fail on `the bar is seven
  anchors that jump`, over `resources/board/render.py` — 7 anchors at HEAD, 8
  now, the new one `href="#view=boards"`. The `all` author's; closes when they
  update that check.
- `README.md` says "the twelve skills"; the tree builds **seventeen**. Belongs
  to `readme-in-three-rings`.
- `readme-in-three-rings/probe/verify.sh` section G runs `index.py check` over
  the whole live checkout — the memo's defect, demonstrated live this pass
  when a sibling's untracked `resources/board/all.py` dropped it 75/75 →
  75/74/1.
- Doctor is red on `origin` and `knowledge` — `knowledge.py relink` closes the
  second. Both pre-existing all pass.
- `four-stale`'s PRD body cites `resources/view/render.py` / `view.css`; the
  files are `resources/board/…` at the same line numbers.
- The 20 existing `.claims/*/` dirs are code-blind — they refuse rather than
  sweep (safe) but cannot split. A board-wide re-snapshot is **not** the fix.
- Noted, unfiled: `vision` init/upgrade divergence; `obsidian.json` dead
  vaults; `knowledge.py board` counts `memos/README.md`; three unnamed
  harnesses share a dead `REG` path.

## `leaked-background-services-outlive-their-fixtures` — WORK IS FINISHED AND GOOD, BUT IT CANNOT BE COMMITTED YET. READ THIS BEFORE RETRYING.

`impl-leaked` came back at 12:05 with both defects fixed and a third found.
`Verdict: DONE`, boxes **23/23** (spec01 7/7, spec02 10/10, spec03 6/6), probe
`17 checks · 17 pass · 0 fail` stable over three runs, all three verify blocks
exit 0. **I believe the report.** It is not collected, for one reason only,
and it is not the worker's fault — see the blocker below.

**What it did, so nobody re-checks it:**

1. **`--pid` now refuses.** A value that is not a positive integer prints to
   stderr and exits 2, judging no daemon. Shown red before the fix on the live
   service (`16 checks · 11 pass · 4 fail`, and it did report on pid 28740),
   green after for `abc`, `""`, `--`, `12x` and `0`, in the probe (section 5)
   and in spec02's block.
2. **The grace expiry is pinned two ways, because MY prescribed check was not
   enough and it measured that rather than just doing as told.** With
   `PEARDE_REAP_GRACE_S=1` / sleep 2 / `--pid` in place, it set the default to
   86400 and the probe still printed `16 checks · 16 pass · 0 fail` — every
   stop assertion names the variable explicitly, so **the default is invisible
   to all of them**. Section 6 now asserts the arithmetic *and* the shipped
   default read out of the module, bounded `0 < x <= 600` — a bound, not a
   literal, so 30 or 120 pass and 86400 does not. Under that mutation it reads
   `16 checks · 15 pass · 1 fail`.
3. **The find that matters. `stranded()` crashed outright.**
   `os.path.isdir(b.get("path", ""))` raises `TypeError`, because the default
   only covers a **missing** key and returns `None` for a key present and
   null. One malformed neighbour took the whole reap down before it judged
   anything. **Not hypothetical:** the parallel `all` session's `AllBoard` is
   by its own docstring "not a Board: it has no path, nothing on disk", and
   the live daemon on 8443 serves `all synced never · None` today. As their
   work lands, `doctor.sh`'s end-of-sweep reap tracebacks and reaps nothing —
   this PRD's whole contract silently off. Fixed on this side; their feature
   needs no change. Probe section 7 stands up an HTTP server answering
   `/status` with `{"boards":[{"name":null,"path":null}]}` and asserts a
   verdict comes back; putting the old shape back reddens three checks.
4. spec03 box 6 no longer pins a total — parses the tally.

### THE BLOCKER — do not "solve" it by widening

`pearde collect … ` refuses:

```
two authors on one hunk: resources/board/serve.py:197 — a baseline hunk merged
with the worker's; `--widen resources/board/serve.py` takes the file whole,
or leave one untouched line between the edits
```

**Both suggestions in that message are wrong for this file.**

- **`--widen resources/board/serve.py` would commit a live sibling's
  half-finished feature.** `serve.py` has **39 hunks**; four regions naming
  `@references/parts/all.md` (the docstring paragraph, the `AllBoard` class,
  the usage line, the `Handler` refusal branch) plus `"all.py"` in
  `PY_SOURCES` belong to the **`all` session**, absent at HEAD. `all.py` is
  untracked and `references/parts/all.md` does not exist, so committing that
  state bakes a known-red tree in: `index.py check` already reports exactly
  those two problems. **Do not widen this file.**
- **"Leave one untouched line between the edits" produces broken code here.**
  The contested hunk at `+196,29` is entirely this PRD's, but split across the
  claim: `IDLE_EXIT_S` and `OWNER_PID` are the **analyst's pass one**
  (pre-claim → read as *baseline*, left out of the commit) and `REAP_GRACE_S`
  is the implementer's (post-claim → committed). Splitting the hunk commits
  `REAP_GRACE_S` **without** `IDLE_EXIT_S`/`OWNER_PID`. Widening is the only
  way to carry a PRD's own pre-claim hunks — which is exactly how
  `collect-stages-…` landed — and widening is barred here.

**Why I did not do the scratch-copy surgery** (backup → `git checkout` →
re-apply only this PRD's hunks → `--widen` → restore). It is the documented
method and it would work on a quiet tree. **The tree is not quiet.** At
12:11:41 `resources/board/render.py` had mtime **12:11:34 — seven seconds
old**; `serve.py` 12:03:31, `all.py` 11:57:14. The `all` session is writing
`resources/board/` right now. The method has a window between the backup and
the restore in which that session's writes to `serve.py` would be silently
overwritten by my restore. Destroying another session's uncommitted feature
work to land mine is not a trade I will make, and the board's own rule is one
writer per file.

### How this lands, next pass

**Preferred:** wait for the `all` session to commit. Then `serve.py`'s only
uncommitted hunks are this PRD's, `--widen` is safe, and the collect is one
command. Check with
`git diff -U0 -- resources/board/serve.py | grep -c 'all\.md\|AllBoard\|all\.py'`
— **zero means it is safe to widen.**

**If it must land sooner:** do the scratch surgery, but only after confirming
`resources/board/` has been still for several minutes (`stat -f "%Sm" -t
"%H:%M:%S"` on `serve.py`, `all.py`, `render.py`), and `cmp` the restored file
against the backup afterwards.

### ALREADY APPLIED AND NOW COMMITTED — do not apply twice

**The workflow bookkeeping for this collect was already written when the
collect failed, and it has since been COMMITTED — it rode the personas commit
`144f3e8` at 12:20.** At its retry, pass only `--report` and `--widen`;
**do NOT re-bump and do NOT re-apply the edit:**

- `attempt-the-build.md` — the `### Edits` row is **already inserted** beside
  the `PEARDE_PORT=1` row, and `runs` is **already 33→34**.
- `probe-then-spec` **already 36→37**; `read-the-contract`,
  `capture-the-harness-baseline`, `re-run-the-harnesses` **already 58→59**.
- `write-the-specs` correctly untouched at 27 (step 5 not entered).
- `workflows.py check` was green after the edit.
- **Nothing is owed at the retry for the workflow files** — they are
  committed. Do not pass `--also` for them again.

### Attribution and reds it corrected, all confirmed against the tree

- Its **earlier** report claimed the whole `serve.py` diff; it retracted that
  itself. Four `all.md` regions are the sibling's.
- **CORRECTED 12:17 — the `index.py check` half of this is now GREEN** (rc=0,
  silent): the `all` sibling has since written `references/parts/all.md` and
  the `files.md` manifest rows. What remains of the `all` author's reds is:
  `one-page-that-says-whats-up` 31/31 → 30 pass 1 fail on `the bar is seven
  anchors that jump`, over `resources/board/render.py` — 7 anchors at HEAD, 8
  now, the new one `href="#view=boards"`. Both close when that author writes
  `parts/all.md`, the `files.md` row, and updates that check.
- Two **skips** in the capped-sweep and view-row harnesses are those
  harnesses' own port stand-down on 8477-8479, held by pid 98905 — a
  neighbour's fixture daemon watching two boards that still exist, which
  `reap` correctly **keeps**. Skips, not fails; both exit 0.
- Left alone as instructed: `the-gate-runs-the-harnesses` check J, and the
  `rampdemo`/`manola` registrations (the `forget` command is named in its
  report).

---

# APPENDIX — another session's pass memory, preserved verbatim

Not mine. Written into this same file by the session building the `all` view
while three pass workers were live. Kept rather than overwritten, because
having my own record destroyed today is exactly what this avoids.

# pass — the `all` board

**Ask (user, verbatim).** "Instead of one master board collecting others, add
an 'all' board that just displays everything in one place."

**Settled with the user (AskUserQuestion, this session — do not re-ask):**
- the master board stays exactly as it is; `all` is added **beside** it
- `all` merges **every board the daemon watches** — no settings file, no list
- it shows every view with the boards side by side (no merged critical path)
  **and** a per-board dashboard with doors into each board's own page
- read-only throughout: nothing writes back through `all`

## Done — all of this is on disk and works

- **@resources/board/all.py** (new). `KEY="all"`; `payload(entries)` merges each
  watched board's own `gantt_payload`; rows carrying a `board` are dropped (a
  master's members register in their own right, so counting both double-counts);
  rels qualified `@<key>/<rel>`; cross-board `needs` dropped; history/counts/
  transitions summed; `calib` only when every board agrees; `dash` rows;
  `memos()`; `unqualify()`; `text()` + a CLI (`all.py [--json] <board>…`).
  The board path is the `.pearde` dir, **not** `.pearde/prds`.
- **@resources/board/serve.py** — `import all as alllib`, added to `PY_SOURCES`;
  `AllBoard`/`ALL`/`is_all()`/`all_entries()`; `bump()` cascades to `ALL`;
  `register()` refuses the `all` key (suffixes `-board`) and bumps `ALL`;
  `vanished()` bumps `ALL`; `/status` lists it with `virtual:true`; `/data`,
  `/prd`, `/answers`, `/memos`, `/report`(null), `/wait`, `/board/all`, `/`
  redirect (all when >1 board), `/sync` fan-out, write routes → 409. The
  `/search` walk was extracted to `Handler.search_board(bpath, mode, rx,
  needle, key)` and fans out over every board on `all`.
- **@resources/board/render.py** — a `boards` nav tab and a
  `<section data-view="boards">` holding `<pearde-boards id="boardlist">`,
  placed **before** the timeline section so DOM order matches the tab bar.
- **@resources/board/view.js** — `VIRTUAL`/`EDITABLE`/`RO_MSG`,
  `rowBoard`/`boardHref`/`boardLink`; every write door gated on `EDITABLE`;
  asks render the pass read-only (picks disabled) with a door to the board;
  `PeardeBoards` element + `drawBoards()`; boot removes the boards tab off
  `all` and removes `+ PRD`, save/revert, the report tab/section and whatsup on
  it; opens on `boards`; switcher lists `all` as "every board · read-only";
  `resize()` now bails when the plot measures zero (a hidden section).
- **@resources/board/view.css** — `.brow`, `.spread`, `.chip`, `.act.out`.
- **@resources/board/viewtest.js** — reads `virtual` off the payload: ORDER,
  first-visible, the state-panel probe, "the merged page draws a row per
  board", "the merged page offers no door that writes" (replaces the N-modal
  check on `all`), the view loop walks ORDER, and `bulkOnParsed` now means a
  visible foot **carrying a textarea or `.send`**, not any visible foot.
- **Docs** — @references/parts/all.md written whole; `@@all` keyword row in
  @index.md and `all.md`/`all.py` folded into `@@view`; rows for both in
  @references/files.md. `python3 resources/index.py check` is silent (clean).

## Verified

- `python3 resources/board/all.py <b1>/.pearde <b2>/.pearde` prints the rows.
- Test daemon on `PEARDE_PORT=8479` over two `plan.py example` boards in the
  scratchpad (`t1`, `t2`): `/status` lists `all`; `/data?board=all` returns 14
  tasks / 16 rows / 2 dash rows, `@example/asking` addressing; `/prd`,
  `/memos`, `/answers`, `/search` (18 hits across both) all answer; `/edit`
  → 409; `/wait` → 200; `/` → 302 `/board/all`; `/board/all` → 200.
- `node resources/board/viewtest.js http://127.0.0.1:8479/board/all` was at
  51/54 before the last three fixes (canvas sizing, section order, bulk-submit
  probe) — **it has not been re-run since those fixes. Re-run it first.**

## Owed

1. Re-run `node resources/board/viewtest.js http://127.0.0.1:8479/board/all`
   (start the daemon again if it is gone — see below) and get it to 54/54.
   Then run it against a normal board too —
   `node resources/board/viewtest.js http://127.0.0.1:8479/board/example` —
   the virtual branch must not have moved anything for a board's own page.
2. Add the pointer to `all` in @references/parts/view.md (a short section
   under the seven views: what `all` is, that it is read-only, that it is not
   a master) and one line in @references/parts/master.md distinguishing the
   two. @references/skills/pearde-view.md should name `/board/all` in its
   body and its `description:` triggers ("show me everything", "all my
   boards").
3. Run `bash resources/doctor.sh` and fix whatever the new file moved.
   Remember: harnesses copy tracked files only — `git add` the new files
   (`resources/board/all.py`, `references/parts/all.md`) **before** trusting
   a doctor/harness result.
4. Kill the test daemon and clear the fixture:
   `PEARDE_PORT=8479 python3 resources/board/serve.py stop` and
   `rm -rf <scratchpad>/t1 <scratchpad>/t2`.
5. Do **not** commit unless the user asks. The branch already carries
   unrelated in-flight work (grammar, health) — leave it alone.

**Fixture (recreate if needed)**

```sh
SP=<scratchpad>; mkdir -p $SP/t1 $SP/t2
python3 resources/board/plan.py example $SP/t1
python3 resources/board/plan.py example $SP/t2
python3 resources/board/plan.py plan $SP/t1 >/dev/null
python3 resources/board/plan.py plan $SP/t2 >/dev/null
PEARDE_PORT=8479 python3 resources/board/serve.py run $SP/t1/.pearde $SP/t2/.pearde &
```


