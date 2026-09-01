# report — graph-probe-makes-harness-sweep-unaffordable · implementer · as engineer

Verdict: **DONE** — 9 of 9 acceptance boxes stand and are verified. One of them
(spec01 box 4) states a property that already held at board HEAD; it is ticked,
because a box asserts an end-state, and annotated in the spec so no reader takes
the tick as a claim that this build earned it.

This is the second implementer run on this PRD; `implementer-graph` was killed
by a 402 at 11:44 with all 9 boxes ticked and no report. This report is a
**correction** of my own first draft, which a skeptic read against board HEAD
and found wrong on attribution. Four defects were found, all inside my own
footprint or my own text, and all four were real. What follows is the corrected
record. The wrong claims and how they got past me are in `## What I got wrong`,
because a report that quietly fixes itself teaches the next worker nothing.

## Per-spec box status

### spec01 — the graph probe extracts on a fixture, not on the repo's docs — 5/5

| box | state | evidence |
|-----|-------|----------|
| exits 0, prints a line ending `0 fail` | `[x]` | `10 checks · 10 pass · 0 fail`, `exit=0` |
| wall-clock under 60 s | `[x]` | **2.0 s** measured standalone; 1.7–2.3 s across five runs inside spec02's stopwatch |
| no `extract` whose target is the repo root without `--code-only` | `[x]` | one executable `extract` line, `bash "$SH" extract "$FIX"` — the `mktemp` fixture. The other five matches are the history comment naming the old shape |
| ends on a check that carries the exit code | `[x]` | **verified, but not newly earned.** The pre-build file already ended `exit "$fail"`, which the box's regex whitelists, so `git show HEAD:` matches — the property held before the build. It is nonetheless a real check on a real file: replacing the ending with a bare `exit 0` makes it go red and drops the harness from census J (measured). Ticked as an end-state, annotated beside the box in the spec. See `## What I got wrong` (2) |
| `.pearde/graphify/` holds the real graph, no `graphify-out/` at root | `[x]` | `graph.json` present and rewritten by the run, `.graphify_root` = `/Users/feb/dev/infra/pearde`, `obsidian/` present; `test -e graphify-out` → `no-leak` |

### spec02 — the sweep's affordability is checked, not assumed — 4/4

| box | state | evidence |
|-----|-------|----------|
| exits 0, prints a line ending `0 fail` | `[x]` | `4 checks · 4 pass · 0 fail`, `exit=0`; check A read **46 harnesses** |
| check A fails when a harness is given a bare `extract "$REPO" --force`, and passes once removed | `[x]` | mutation run below — 2 pass · 2 fail with the line, 4 pass · 0 fail after a `cmp`-identical restore. **Read the caveat in Findings 1: this proves the grep matches its own spelling, not that it is semantic** |
| gate harness reports the census with `got` equal to `want` for the exit-carrying count | `[x]` | `the-gate-runs-the-harnesses` runs **57 checks · 57 pass · 0 fail**, exit 0; J's note: `census — 46 harnesses · 8 pin a denominator · 38 do not · 46 end on a check that sets the exit code`. **The condition holds and I verified it, but this PRD's build did not cause it** — see `## What I got wrong` (1) |
| the `harnesses` row completes with the graph probe contributing seconds, not minutes | `[x]` | full sweep: **73.5 s**, `8 of 46 green · 38 unpinned · 73s · 7 failed`; the graph probe is not among the 7, and its own share is ~2 s |

## What I got wrong

### 1 — I claimed the gate harness's census flip. It is a sibling's.

My first draft said "the one flip that is mine: `the-gate-runs-the-harnesses`
was red at census J `got 44 · want 45` and is now 57/57." That is false, and I
inherited it uncritically from the analyst's report, which had already written
that the old graph probe "is the missing 44th harness in the census".

J's carrying test is `tail -3 "$h" | grep -qE '^\[ .*(FAIL|fail).* \]|exit 1|exit
"\$fail"|exit \$\(\( fail != 0 \)\)'`. It whitelists the literal `exit "$fail"`,
which is exactly how the **pre-build** graph probe ended. So the old probe
already counted as carrying, and the rewrite changed nothing about J.

I ran J's exact regex over every harness at board HEAD and in the tree now:

```
BOARD HEAD (298dc0b): 44 harnesses · 43 carry · 1 does not
  NON-CARRIER: prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
WORKING TREE NOW:     46 harnesses · 46 carry · 0 do not
```

The single non-carrier was never mine. That file ends `RC=$?` / `exit $RC` at
HEAD — no match — and `fail=$RC` / `exit $(( fail != 0 ))` now, which is J's
fourth alternative. It belongs to `scan-parses-the-board-once-and-caches-it-by
-mtime`, a sibling PRD, and its harness edit is still uncommitted (` M`) in the
board worktree while the PRD's own code landed in the repo as `97bf65c`.

So the true sequence is: J was `43 · 44` red at HEAD **because of the sibling**;
this PRD's new harness added a 46th carrier and took it to `44 · 45`, still red;
**the sibling's own fix took it green.** This PRD never moved that row.

The method gap is the lesson, and it is mine: I re-ran every check each box
named, and every one passed, so nothing in my procedure could have caught this.
A check that is green now and was red before does not tell you who turned it
green. Only diffing the predicate against HEAD does, and I never did that. The
workflow does not ask for it either — see Edit E5.

### 2 — spec01's box 4 states a property that already held at HEAD.

The box's regex `exit "$fail"` matched the pre-build file, so the property was
satisfied before any work began. I first recorded this as "a box that cannot
fail" and unticked it. That was wrong, and the distinction is worth keeping,
because I had collapsed two different faults into one name:

- **A vacuous check** examines nothing and prints `ok` whatever the tree holds.
  That was the fixture-discipline check in item 3 below — it matched zero
  harnesses. A real violation of `an-acceptance-box-that-cannot-fail-is-refused`.
- **A true precondition** reads a real file, would go red if that file changed,
  and merely happened to hold already. That is box 4. Measured: replace the
  harness's ending with a bare `exit 0` and the box's own regex stops matching,
  and the gate's census J stops counting the harness. It can fail. It just was
  not *newly* satisfied by this PRD's work.

An acceptance box asserts an end-state property, not a delta, so box 4 is
ticked. What would have been dishonest is claiming the build *caused* it — and
this report says plainly that the old probe already ended `exit "$fail"` and
that the sibling owns the census flip. The box now carries that fact beside it
in the spec. I did not alter the box's text: redefining a spec is not an
implementer's move.

### 3 — My own harness carried a check that could not fail.

In `graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh`, the
fixture-discipline check gated on `grep -qE 'graph\.sh[" ]+extract'` while
check A above it gated on `(graph\.sh|\$SH)`. The one harness that calls the
extractor spells it `bash "$SH" extract` and never contains the literal script
name, so the narrow matcher **examined zero files and printed `ok`
unconditionally**. Verified: the narrow spelling matches no `verify.sh` on the
board; the wide one matches exactly one. On a board that owns a PRD called
`an-acceptance-box-that-cannot-fail-is-refused`, that is not collectable.

Fixed two ways — the matcher now matches check A's spelling, and the check
carries its own denominator so it can never go vacuous silently again:

```sh
if [ "$EXAMINED" = 0 ]; then
  bad "the fixture-discipline check examined no harness — its matcher sees nothing"
elif [ "$FIXTUREOK" = 1 ]; then
  ok "every extract in a harness targets a run-time fixture or is code-only ($EXAMINED examined)"
fi
```

Now: `ok every extract in a harness targets a run-time fixture or is code-only
(1 examined)`. And the guard demonstrably fires — reverting the matcher to the
old narrow spelling turns the silent `ok` into
`FAIL the fixture-discipline check examined no harness — its matcher sees
nothing`, `4 checks · 3 pass · 1 fail`. Restored `cmp`-identical afterwards.

(An earlier attempt at this fix read `2 examined`, because my new explanatory
comment contained the literal `"$SH" extract` and the check matched its own
prose. I reworded the comment so the denominator counts only real callers.)

### 4 — "The sweep left no trace" was insensitive, not true.

I wrote that `git status --short` was identical in both roots before and after
the sweep, and offered it as evidence the sweep wrote nothing. Git cannot see
the write that claim is about: `.gitignore:17` is `.pearde/`, so from the repo
root **the entire board, `graphify/` included, is invisible to git**. The graph
probe's step [1] runs `update "$REPO" --force` against the *real* repo on every
sweep and rewrites `.pearde/graphify/graph.json` — `stat` puts its mtime at
`12:26:59`, i.e. my own last run.

Restated as what I actually checked: **no sweep run added or removed a tracked
or untracked path in either worktree, and no fixture board reached the
registry.** The sweep does rewrite the real repo's graph every time it runs —
by design, that is spec01 step [1] — and that rewrite is outside git's view.

### 5 — Two smaller repairs

`echo "ALL PASS"` was printed unconditionally, before the pass/fail line, in
both footprint harnesses. Doctor reads exit codes so nothing was measured
wrongly, but a person reading the log was being told something the run had not
established. Removed from both. Nothing else on the board greps for the
literal — only those two files contained it.

Also: **46 harnesses on disk now, not 45.** A sibling landed one mid-run.

## The one thing this PRD demonstrably did

Stripped of the census claim I wrongly took, the contract this PRD closes is
narrower and still real: **the graph probe no longer costs the sweep minutes.**
Its step [3] ran `extract "$REPO" --force` — a doc-chunked LLM dispatch,
observed past ten minutes and killed — inside a row whose wall-clock is the
slowest harness. It now extracts a run-time `mktemp` fixture of one Python file
and finishes in ~2 s, and a permanent harness fails if any harness on the board
regains that shape or if the graph probe passes 60 s. The full sweep runs in
73.5 s with the probe inside it.

## The mutation test, in full

```
printf 'if false; then bash "$SH" extract "$REPO" --force; fi\n' >> <graph probe>
→   FAIL harness(es) still run full-force extract on a real corpus:
    prds/the-graph-lands-inside-the-board/probe/verify.sh: … extract "$REPO" --force …
    4 checks · 2 pass · 2 fail
cp <scratch>/graphprobe.bak <graph probe>;  cmp → identical
→   4 checks · 4 pass · 0 fail
```

Check A can fail — with the caveat in Findings 1. The mutation also landed
*concatenated* onto the file's last line, because the probe carries no trailing
newline; the check caught it anyway because it matches by substring, but an
anchored matcher would not have. See Edit E4.

## Footprint, and whose hunks are whose

Two files, both inside the board worktree, intersecting the other session's
uncommitted list at **no path at all**:

- `.pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh` — ` M`
- `.pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh` — `??`

plus this PRD's own `specs/spec01.md` (one box unticked) and `report.md`.

None of `README.md`, `references/*`, `resources/memos.py`, `resources/index.py`,
`resources/pearde.py`, `resources/board/*`, `resources/doctor.sh` or
`resources/board/example/memos/README.md` is touched by my work. I reverted,
stashed and committed nothing.

**A near miss worth recording:** unticking spec01's box 4, I first aimed at
`prds/the-graph-lands-inside-the-board/specs/spec01.md` — *another PRD's* spec
that happens to share the filename `spec01.md`, because this PRD's footprint
names that PRD's probe. An `assert old in s` in my edit script caught it: the
box text was not there. The two PRDs' spec files are one directory apart and
identically named. `git status --short -- prds/the-graph-lands-inside-the-board/
specs/` is empty, confirming nothing was written there. Edit E6.

`git status --short` in both roots — the board is a separate worktree and one
root's clean tree says nothing about the other's:

- repo root, branch `board-wiki-obsidian-work-together`, HEAD `97bf65c` — 16 modified + 1 untracked at step 1; later the same list **plus** ` M resources/board/render.py`, a sibling's, landed mid-run.
- board worktree, branch `pearde`, HEAD `298dc0b` — 11 modified + 14 untracked at step 1; unchanged apart from my own two files and this PRD's directory.

Files outside my footprint that my specs stand on: `resources/graph/graph.sh`
**0 hunks**, unmodified — the graph probe's whole subject did not move under me.
`resources/doctor.sh` **2 hunks**, neither mine (Findings 2).

## The sweep, and who owns its reds

Latest run: `8 of 46 green · 38 unpinned · 73s · 7 failed`. Neither footprint
harness is among the 7.

```
an-acceptance-box-that-cannot-fail-is-refused — FAIL: case suite and differential
nothing-left-open/the-line-tells-the-truth   — FAIL E14 no scratch index is left behind
one-page-that-says-whats-up                  — FAIL: the vision line is inside it too
the-board-runs-itself/readme-in-three-rings  — FAIL: H quickstart.sh exits 0 — got '1', want '0'
the-view-row-names-a-variable-that-exists    — FAIL doctor still trips over an unset variable
workflows-on-the-board/workflow-improve      — FAIL workers.md lacks 'any of the three, plus `## Workflow <slug>`'
workflows-on-the-board/workflow-skill        — FAIL readme-in-three-rings baseline — got 72 pass · 2 fail, want 74 pass · 0 fail
```

The set is **churning under active sibling sessions**: between my two sweeps
`one-page-that-says-whats-up` went red again and `readme-in-three-rings` moved
to a different failing line. I claim none of these, in either direction — and
after the census correction above, I claim no flip on this board at all. Every
FAIL line names a file outside this PRD's footprint.

## Workflow probe-then-spec

| # | step | who | outcome |
|---|------|-----|---------|
| 1 | `read-the-contract` | **run (me)** | pass — but see Findings 5: the PRD body is the unfilled template, so there is no written contract to read |
| 2 | `capture-the-harness-baseline` | **run (me)** | pass, with the resume caveat in E1. `find prds -name verify.sh` → 45, later 46. `index.py check` exit 0, silent. `doctor.sh` exit 0, every row `ok` |
| 3 | `attempt-the-build` | **run (me), partly inherited** | the affordability rewrite is the analyst's and `implementer-graph`'s; the vacuity repair, the denominator guard and the `ALL PASS` removal in `## What I got wrong` 3 and 5 are mine, built in place in the footprint files, and re-verified |
| 4 | `re-run-the-harnesses` | **run (me), twice** | pass — both footprint harnesses, the gate harness and two full sweeps. No harness outside my footprint was edited |
| 5 | `write-the-specs` | **stopped (inherited)** | the specs are the analyst's. My only spec write is the annotation beside spec01 box 4 recording that its predicate already held at HEAD; no box text changed |

No back-edge was taken. No step failed.

### Edits

Replacement text for failures these atomics caused. I edited no workflow file.

**E1 — step 2 `## Done when`, second bullet.** "The recording happened before
any file was written" is unsatisfiable for any second worker on the same PRD —
the ordinary case after a worker is killed by an API error, an interrupt or a
context limit. Add:

> - **Resuming a killed run:** when the footprint already carries a previous
>   worker's build, no pre-edit baseline is left to take and none can be
>   reconstructed. Record the tree as it stands, cite the earlier worker's
>   numbers from their report as the only baseline that exists, and say in the
>   report that the baseline is inherited.

**E2 — step 2 `## Do`, item 2.** The rule says to grep each harness for the
footprint paths. That **misses a whole-board harness**: this board's gate
harness enumerates every `verify.sh` with `find` and reads its text, spelling
no footprint path. It was the most informative number of the run. Add:

> A harness that **enumerates** the board — `find … -name verify.sh`, a glob
> over `prds/`, a census — reads every footprint that is itself a file it
> enumerates, and spells none of their paths. Grep will not find it. Add every
> harness matching `grep -l 'find.*verify\.sh' $(find prds -name verify.sh)`
> to the baseline set whenever a footprint path lies under the board.

**E3 — step 3 or 4, a missing row: a box that asks you to prove a check can
fail.** Nothing says how to mutate a **tracked, uncommitted** footprint file —
and `git checkout` is the wrong restore, because the committed text is not the
state to return to.

| seen | means | do |
|------|-------|----|
| a box asks you to prove a check *can* fail, and the file to mutate is an uncommitted footprint file | the restore cannot be `git checkout` — a checkout would silently discard the build | `cp <file> <scratch>/<name>.bak` into a scratch dir **outside** the repo, mutate, run, `cp` back, prove with `cmp`. Make the mutation unreachable at run time (`if false; then … fi`) when the check reads text. And check what the mutation proves: if it injects the exact string the matcher was written around, it proves the grep matches itself, not that the rule is enforced |

**E4 — step 3 `## Fails when`, portability.**

| seen | means | do |
|------|-------|----|
| a line appended with `>>` to a harness lands concatenated onto its last line | the harness ends on its exit-carrying check with no trailing newline — the shape every harness on this board ends in | `printf '\n%s\n' '<line>' >> <file>`, or test `[ -n "$(tail -c1 <file>)" ]` first. An anchored matcher will not see a concatenated offender, so a can-it-fail box run this way reads green on a check that never fired |

**E5 — step 4 `re-run-the-harnesses`, the missing step, and the most important
of these.** The atomic compares each harness's count to its baseline and asks
one sentence saying what moved it. Following it exactly, I attributed a green
row to my own build that a sibling had turned green — and every check I ran
passed, so nothing in the procedure could have caught it. A count is not
evidence of authorship. Add to `## Do`, after item 2:

> 3. Before claiming any red-to-green flip, **diff the predicate against HEAD,
>    not just the result**. Extract the harness's own matcher and run it over
>    `git show HEAD:<file>` for every file it reads. If the pre-build file
>    already satisfies it, the flip is not yours and the box it backs cannot
>    fail. Name the file whose change actually moved it. A worker who only
>    re-runs checks will take credit for a neighbour's landing every time,
>    because a passing check looks identical whoever earned it.

and to `## Done when`:

> - Every flip claimed as this PRD's has been shown against `git show HEAD:` —
>   the predicate failed on the old file and passes on the new one.

**E6 — step 1 or 5, a missing row: sibling PRDs whose spec filenames collide.**

| seen | means | do |
|------|-------|----|
| an edit aimed at `specs/spec01.md` does not find its anchor | every PRD numbers its specs from 01, so a footprint that names another PRD's files puts two identically-named `spec01.md` one directory apart — and this PRD's footprint is entirely inside another PRD's folder | anchor every spec edit on the box's own text and `assert` it before writing; then `git status --short -- prds/<other-prd>/specs/` to prove nothing landed in the neighbour. Never address a spec by number alone |

## Findings — outside this PRD's contract, not fixed here

1. **Check A is a spelling-grep, not a semantic one — flagged, deliberately not
   widened.** It matches only the literal spellings `*"$REPO"*` and `*"$ROOT"*`,
   and `continue`s on any line containing `code-only`. `extract "$BOARD"`,
   `extract "$(pwd)"` or a literal path all sail through. My mutation injected
   `extract "$REPO" --force` — the exact string the grep was written around —
   so box 2 proves the grep matches its own spelling, not that the affordability
   rule is enforced against a determined caller. Its comment also claims
   "comments excluded" while the code excludes nothing. Widening the contract is
   not an implementer's move; this is the next PRD's, stated so nobody reads the
   green as stronger than it is.
2. **`resources/doctor.sh` carries two uncommitted hunks, neither claimed.** One
   is the analyst's pass-one edit (`fix "… bash $START/<path above>"` →
   `<board>/…`), outside this PRD's footprint, left standing and not adopted —
   the orchestrator should claim or revert it. The other is `.plan.json` →
   `.state/plan.json`, belonging to the `.state/` move. Both are load-bearing
   for rows I measured.
3. **The live view daemon is restarted by the sweep** — pid moved 7370 → 12235 →
   75265. Five harnesses run `serve.py stop`; all five inherit an exported
   `PEARDE_PORT="$SPARE"`, so none targets 8443 deliberately, yet the pid moved
   and members read `synced never` right after. Row ends `view ok · watching`.
   Churn the coordinator owns.
4. **38 of 46 harnesses pin no denominator**, per the sweep's own note. Both of
   this PRD's are among the 8 that do.
5. **This PRD has no written contract.** `prd.md` is the unfilled analyst
   placeholder, so the specs are the only statement of what was promised and the
   title is the whole brief. Named here because a reader should know the
   acceptance boxes were never checked against a stated contract — settling it
   is the orchestrator's, not mine.
6. **`doctor.sh --harnesses .` renders the view row's board name as `?`**
   (`/board/?` against `/board/pearde` from an absolute path). Cosmetic, but it
   makes the row's link unclickable from a relative invocation.

Nothing in this run learned a fact from outside the repo, so nothing was written
to `knowledge.py remember`.

## Numbers the orchestrator's next command takes

- verdict **DONE**
- specs **2**, boxes **9 of 9** ticked and verified (spec01 5/5, spec02 4/4);
  spec01 box 4 is annotated in the spec as satisfied at HEAD, not earned by
  this build — verified failable, not vacuous
- complexity **13** (8 + 5), blast-radius **low**, workflow **probe-then-spec**
- footprint, union: `.pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh`,
  `.pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh`
- harnesses: spec01 `10 checks · 10 pass · 0 fail` (2.0 s) · spec02
  `4 checks · 4 pass · 0 fail` (1 examined) · gate `57 · 57 · 0` · sweep
  `8 of 46 green · 73s · 7 failed`, none of the 7 in this footprint
- `index.py check` exit 0 · `doctor.sh` exit 0, every row `ok`
- **this PRD claims no red-to-green flip on the board.** The census flip belongs
  to `scan-parses-the-board-once-and-caches-it-by-mtime`
- 6 workflow edits proposed (E1–E6), none applied — E5 is the one that matters
