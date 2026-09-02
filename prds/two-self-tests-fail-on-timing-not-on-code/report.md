# two-self-tests-fail-on-timing-not-on-code — implementer report

Verdict: DONE

worker `impl-timing`, as engineer, workflow `probe-then-spec` — second pass on
this PRD. The analyst ran the same route and left the build in the tree; this
pass ran the harnesses, proved every acceptance box against real output, and
ticked them as each closed. **No flip is claimed here.** Every red-to-green on
this tree was earned by the analyst's pass that wrote the rewrite; this pass
measured it.

Boxes: `spec01` 4/4, `spec02` 5/5. Both `## Verify and Proof` blocks exit 0 the
way `pearde collect` runs them (`bash -e -o pipefail` over the awk-extracted
block).

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | done — `prd.md`, `specs/spec01.md`, `specs/spec02.md`, the prior report, and `git status --short` in **both** roots recorded before the first edit |
| 2 | `capture-the-harness-baseline` | done — baseline **inherited and confirmed**, not re-taken (see below) |
| 3 | `attempt-the-build` | **not entered.** The route's own `Fails when` row covers this: the specs exist and the build is in the tree, so this is the second pass. Nothing was rebuilt; a rebuild would have discarded a working build |
| 4 | `re-run-the-harnesses` | done — all three footprint harnesses plus both flip probes plus the repo gate |
| 5 | `write-the-specs` | **not entered.** The specs were written by the analyst's pass. This pass only ticked their boxes, which is the implementer's act |

### Edits

None. No atomic gave a wrong command, a stale path, an uncheckable check or a
shape `## Fails when` does not list. The one row that had to be taken — step 3's
"the route's steps 3 and 5 have nothing to do because the specs already exist" —
described this run exactly.

## The baseline, and why it is inherited

The analyst's pass published its counts and left the tree uncommitted. Per
`capture-the-harness-baseline`, the cheaper and safer confirmation was taken:
the same set was re-run on the built tree and every count matched the published
one, with no window in which the tree was half-reverted.

| harness | analyst published | this pass | exit |
|---|---|---|---|
| `scan-parses-…/probe/verify.sh` | 5 named checks, pass | `parse-cache verify: pass`, same 5 | 0 |
| `readme-in-three-rings/probe/verify.sh` | `75 checks · 75 pass · 0 fail` | `75 checks · 75 pass · 0 fail` | 0 |
| `readme-in-three-rings/probe/quickstart.sh` | `41 checks · 41 pass · 0 fail` | `41 checks · 41 pass · 0 fail` | 0 |

Repo HEAD `d646168` and board HEAD `f06f6e3` were recorded before the first
command and are unchanged at the end. `git -C .pearde status --porcelain` is
byte-identical before and after this run: this pass wrote only inside
`.pearde/prds/two-self-tests-fail-on-timing-not-on-code/`, whose whole directory
is untracked.

## spec01 — the parse-cache harness counts work, not milliseconds — 4/4

```
ok   files walked (True)
ok   a cold walk reads every file once (14)
ok   a warm walk reads nothing (0)
ok   one changed mtime costs exactly one re-read (1)
ok   the check can fail: without the cache the walk reads every file (14)
parse-cache verify: pass
```

- **box 1** — exit 0, and `ok   a warm walk reads nothing (0)` printed verbatim.
- **box 2** — `grep -cE 'perf_counter|ms above the|warm >= cold'` prints `0`. The
  only remaining occurrences of the word "clock" or "ms" in the file are in the
  comment block that records why they were removed. The file's one `sleep 0.01`
  is an mtime nudge, not an assertion.
- **box 3** — `flip-scan.sh` exits 0:

  | tree | exit | what the harness said |
  |---|---|---|
  | `good` | 0 | five ok |
  | `never` (`_PCACHE.get` to `None`) | 1 | `warm walk reads nothing — got 14, want 0`; `one changed mtime — got 14, want 1` |
  | `stale` (mtime test to `True`) | 1 | `one changed mtime costs exactly one re-read — got 0, want 1` |

- **box 4** — the board is unwritten across a run. See finding 8 on the box's own
  spelling; the load-bearing form was run and is clean.

## spec02 — the README harness judges the README — 5/5

- **box 1** — `75 checks · 75 pass · 0 fail`, exit 0.
- **box 2** — `cat "$V" "$Q" | grep -cE '"(16|80|19)"$'` prints `0`. The two
  surviving literals in either file are inside comments recording what the
  pinned counts used to be.
- **box 3** — `steady-doctor.sh` exits 0 under one injection (the view service
  stopped between the two `doctor` runs):

  ```
  old logic — a plain diff of the two whole reports:
    rows differing: 2  (the old check demanded 0) -> RED
  re-aimed logic — a control pair:
    moved with the home held constant, so not judged: view
    home-dependent rows, reproduced on a second pair: ''
    -> green
  ```

- **box 4** — `flip-readme.sh` exits 0 and ends `FLIP:`:

  ```
  --- good (baseline): 0 fail
  --- skill: adds 0 over the baseline
  --- home: adds 2 over the baseline
      + FAIL: 6 ...and the scrubbed home breaks no row the checkout had not already broken
      + FAIL: 6 no row but vault reads the home
  --- board: adds 2 over the baseline
      + FAIL: 2 the board init wrote breaks no doctor row
      + FAIL: 6 ...and the scrubbed home breaks no row the checkout had not already broken
  FLIP: green on the input it must pass, red on the input it must catch
  ```

  A seventeenth skill file adds **nothing** — the input the old harness went red
  on. Note the baseline is `0 fail` this pass where the analyst's was non-zero:
  `index.py check` went green in the live checkout between the two passes (see
  finding 2), so the `good` tree now carries no inherited failure at all. The
  differential judgement is unaffected — that is what the differential form is
  for.

- **box 5** — the note line appears and the run still ends green:

  ```
    note: broken before any board existed, so not init's — index
  41 checks · 41 pass · 0 fail
  ```

## The repo's own gate

| gate | result |
|---|---|
| `python3 resources/index.py check` | exit 0, **0 lines** — silent |
| `bash resources/doctor.sh` | exit 1 on two rows, **both outside this footprint**: `origin broken — 3 derived in flight vs 2 requested` (board state, three sessions are dispatching) and `knowledge broken — the research layer does not check out` |

Neither broken row names a file in this PRD's footprint, and both were broken
before this pass's first command. `view ok · watching · http://127.0.0.1:8443/board/pearde`
after every probe: nothing in the set left the daemon stopped, and
`serve.py status` registered no fixture board (checked before and after
`steady-doctor.sh`, which is the one probe that starts a service — it binds a
spare port and its trap stops it).

## Findings — outside this contract, not fixed

Carried forward from the analyst's pass by name, with this pass's re-reading.

1. **`README.md` states a stale number.** Its `install --apply` row says
   "built … for the twelve skills"; the tree now builds seventeen. `README.md`
   is `readme-in-three-rings`' footprint, a `correct-a-documented-claim` job.
   **Still open.**

2. **The manifest was red in the live tree — now closed by a sibling.** The
   analyst recorded `index.py check` printing two problems (`resources/board/ramp.py`
   with no row, `@references/parts/ramp.md` not on disk). At this pass it prints
   nothing: `index ok · 144 files · 34 keywords · every anchor resolves`. A
   sibling session closed it between the two passes. This is the shrinking-red
   case, not a flip of mine.

3. **`pearde view`'s output shape depends on whether the service was already
   up.** Fixed inside the footprint by matching the `/board/` URL rather than
   the first URL on the page. **Closed.**

4. **The cache harness is unpinned.** `doctor`'s pinned-detector wants a
   `$((PASS+FAIL))` total and `scan-parses-…/probe/verify.sh` prints none, so it
   counts toward the `unpinned` figure. That is
   `the-harness-sweep-is-capped-so-a-red-is-a-real-red`'s row. **Still open.**

5. **Two neighbours carry the same defect and are not mine.**
   `the-fixtures-meet-the-tool`'s `F no file under resources/` row reads the
   whole working tree's `git diff`. `init-seeds-a-board-doctor-calls-green`
   asserts on a whole `doctor` report and is inside
   `the-harness-sweep-is-capped-so-a-red-is-a-real-red`'s spec03. **Still open.**

6. **The 6.7-hour sandbox clock lag did not bite these two,** and cannot arrive
   later through either file — there is no clock left in them. **Closed.**

7. **Nothing was learned outside this repo,** so nothing was written back with
   `knowledge.py remember`. **Unchanged.**

New this pass:

8. **Box 4 of `spec01` names a command that cannot fail.** The box says
   `git status --porcelain .pearde` is unchanged across a run. `.pearde` is
   gitignored in the parent repo, so that command prints **0 bytes** whatever
   the harness does — the box would tick against a harness that wrote the real
   board. The honest form is the board's own repo,
   `git -C .pearde status --porcelain`, which **is** what was run to tick it:
   byte-identical before and after. The box is ticked on the honest form and the
   weaker spelling is recorded here rather than edited, since editing an
   acceptance box mid-run rewrites the contract this pass is measured against.
   A one-line spelling fix for whoever next opens this spec.

9. **`readme-in-three-rings/probe/verify.sh` section G carries one more reading
   of the machine.** `eq "G index.py check is silent" … "0"` runs
   `index.py check` over the whole live checkout — a neighbour's uncommitted
   file reddens it, which is exactly this PRD's disease. It is **not** one of
   the four assertions `spec02` names, so it was left alone. It is a fifth item
   for the same sweep, in a file already in this footprint: the smallest honest
   repair is to run the check over `git archive HEAD` rather than over the
   working tree, or to scope it to the anchors the README itself names.

10. **Neither footprint harness pins a denominator, and both should stay that
    way.** `readme-in-three-rings/probe/verify.sh:117` asserts the quickstart's
    tail contains `" 0 fail"`, never a literal `N checks · N pass · 0 fail`. On
    a file three sessions write, a pinned total reddens on a neighbour's
    *passing* added check; the `0 fail` suffix reddens only on a failing one.
    Recorded so a later editor does not re-pin it.

## Scores

complexity: 20
blast-radius: mid
workflow: probe-then-spec
