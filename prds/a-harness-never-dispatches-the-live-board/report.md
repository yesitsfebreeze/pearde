# a-harness-never-dispatches-the-live-board — implementer report

Verdict: DONE

worker: impl-harness-nodispatch · as engineer · lane
`lane/a-harness-never-dispatches-the-live-board` · 3 specs · 26 of 27
acceptance boxes ticked.

The fan-out is gone. `211 harness file(s) read · 0 dispatcher launch(es)`, and
the run log count on this board is `12` before and `12` after the whole
verification round, including both repaired harnesses and the realpath probe.

All three of the contract's `Done means` bullets hold:

- the probe's last check reads the frontier through `plan.py plan all`, and
  that read is reachable from a command line
- no harness under `.pearde/prds/` launches a dispatcher, proved over every
  `probe/` on the board by a reader, not over the one file this PRD named
- `run.py`'s bare `all` refuses, exit 2, naming both `pearde plan all` and
  `python3 run.py run all`

The one box left open is spec03's last, and it is open for two facts outside
this PRD — both measured against the **unmodified** checkout as well as the
lane, and identical in both. See *The one open box*.

## Per-spec box status

| spec | boxes | state |
|---|---|---|
| spec01 — the frontier has a read again, and the bare scope refuses | 9/9 | green |
| spec02 — the check that proves no harness on this board dispatches it | 9/9 | green |
| spec03 — the three harnesses stop launching the machine | 8/9 | one open |

## spec01 — the read, and the refusal

The two hunks that already stood in the lane were reviewed and are correct.
`_merged_plan` is loaded only when a scope or a window asks for it —
`_merged_plan([])` and `_merged_plan(["here"])` both return `(False, 0)` with
`run` absent from `sys.modules` — so the single-board `plan` page never pays
for the merged machinery. Nothing in `resources/` invokes `run.py` as a
script; the only occurrences are the refusal's own text, two comments, and the
invariant's fixtures and `run all --dry` mechanism check.

Measured (run from `/`, with the script named absolutely — see *A defect in a
verify block*):

    $ python3 <lane>/resources/board/plan.py plan slots
    12 slots (load1 stale, ceiling 12) · cpu 9.33 of 10 loaded, … → 0 · mem …
    $ python3 <lane>/resources/board/plan.py plan all | head -2
    2 of 18 board(s) · 45 PRDs on the frontier · 2 wave(s)
    $ python3 <lane>/resources/board/plan.py plan all | grep -c '^wave 1: @'
    1
    $ python3 <lane>/resources/board/plan.py plan progress | wc -l
    1
    $ python3 <lane>/resources/board/run.py all ; echo $?
    run.py: refused — `run.py all` would DISPATCH, and a bare scope reads as
    the frontier.
      the read : pearde plan all          (moves nothing)
      the move : python3 run.py run all   (the verb, spelled)
    2

`run.py --json` and `run.py progress` refuse the same way. The in-process path
is untouched:

    PASS the verb dispatches, the bare scope does not, pearde run is unchanged

— `script_main(["run","all","--dry"]) == 0` reaching `dispatch.main` with
`(["--dry"], ["entries"])`, `script_main(["all"]) == 2` reaching nothing, and
`cmd_run(["all"]) == 0` reaching `dispatch.main` with `([], ["entries"])`.

## spec02 — the invariant, the memo, the manifest

The reader and its shell wrapper stood in the lane and are correct. What this
run added:

- **the memo** — `.pearde/memos/no-harness-under-the-board-dispatches-it.md`,
  `kind: invariant`, carrying the script as its `verify:`. `memos.py check`
  names it no longer; its `tags:` block was written by `memos.retag_text`
  rather than typed, because `tags:` is derived and never authored.
  `memos.py index` regenerated `.pearde/memos/README.md` — before that run
  exactly one memo of the 44 was missing from the kind index, and it was mine.
- **two manifest rows** in `references/files.md`, one per new file.
- **the `@@` scope entry** — both files added to `@@run`, the scope whose own
  sentence is already "the command that dispatches … and the `plan` that reads
  the same frontier without moving it". `pearde index check` reports the same
  four lines as the baseline and no fifth.
- one correctness fix inside the footprint: the reader's usage line and
  docstring still called the file `scan.py`, its name in the probe directory.

The mechanism it holds, run against the lane:

    PASS  the reader sees all six spellings of a dispatching harness
    PASS  the reader clears --dry, the read, a grep, a test, open(), a comment
          and an exemption
    PASS  no harness under /Users/feb/dev/infra/pearde/.pearde/prds launches a
          dispatcher · — 211 harness file(s) read · 0 dispatcher launch(es)
    PASS  run.py refuses a bare scope: `run.py all` exits 2
    PASS  the refusal names the read that replaces it
    PASS  pearde plan reaches the merged read: `plan slots` prints the reading
    PASS  plan.py names read_main, so the read has one implementation
    rc=0

It refuses rather than passes when there is no board (`FAIL no board at or
above / — refused rather than passed over nothing`, exit 1), and it can fail:
injecting `python3 "/repo/resources/board/run.py" all` into a throwaway
`probe/verify.sh` comes back as `RED prds/z/probe/verify.sh:2`, exit 1.

## spec03 — the three harnesses

**`the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` line 59.**
The line the PRD measured now reads `python3 "$ROOT/resources/board/plan.py"
plan all`. Its box `a row the frontier marks ready but claim refuses is
skipped` still passes against this board, and `--dry opened no run log on this
board` is now true of the whole file: 12 logs before, 12 after.

**`the-machine-frontier-is-one-ordered-list/probe/verify.sh`.** `RUN` points at
`plan.py` (`RUN_PY` keeps its override role, and the missing-file fallback
follows), and all seven invocations carry the `plan` verb. Two boxes needed
more than the rename, exactly as spec03 said:

- `--json carries the scope and the labels` asserted `d["scope"] is None`. The
  payload has no `scope` key and never did; it now asserts `d["group"] ==
  "all" and isinstance(d["groups"], dict)`, and passes.
- the two unknown-scope boxes now get their refusal from the scope resolver:
  `pearde plan: 'no-such-group-here' is neither a group nor a PRD here. Groups:
  private. A board joins a group by writing 'groups: no-such-group-here' in its
  own settings.md; nothing here keeps that list`.

Re-recorded count: **33 ok, PASS, exit 0** — the same 33 the sibling's `the
sibling read-only harness is still 33/33` box already asserts, so that box was
left as it stands rather than edited to the same number.

**`the-board-locks-by-realpath/probe/probe.py`.** `run_here`'s argv spells the
verb (`[sys.executable, run_py, "run"]`) and both spawns carry a
`# dispatch-exempt:` line naming the mktemp board and the stubbed adapter. The
verb is what makes it dispatch at all now — without it `script_main` refuses —
and it is backward-compatible: `main` strips a leading `run`, so the same file
behaves identically against the un-landed checkout.

## The one open box

`all three harnesses pass` is not ticked. Two rows are red, neither caused by
this PRD, and both re-measured against the **unmodified** checkout to prove it.

**`--dry names every row it would launch`** wants a `^would @…` line, and
today `run all --dry` produces none: every row the frontier marks ready is
refused by the gate for a structural reason — `leaf: … has children not done`
or `needs: … is 'open', not done`. `dispatched 0 · refused 18 · dead 0`, from
the lane and from `/Users/feb/dev/infra/pearde/resources/board/run.py` alike.
The box asserts that the live board currently holds a dispatchable row, which
is a property of the board's dependency graph on the day it runs, not of the
code. Recorded as a defect of that harness, outside this footprint, not fixed
here — see *Defects outside this scope*.

**`the-board-locks-by-realpath/probe/probe.py` fails 8 claims of 12.** Every
one is its own PRD's unbuilt feature: `A. one watch entry for one realpath`,
`C. the second run refuses`, `E. the refusal names the physical board`. That
PRD is `claimed` and in flight right now. Byte-identical failures from both
trees:

    --skill <lane>            8 claim(s) failed
    --skill <checkout>        8 claim(s) failed

— same rows, same reasons. This harness is red because the lock it probes does
not exist yet, which is what a probe for an in-flight PRD is supposed to do.

## A defect in a verify block

Every spec here writes its checks as `cd / && python3 resources/board/plan.py
…`. After `cd /` that relative path resolves against `/` and cannot run; the
proof was executed with the script named absolutely and the cwd still `/`,
which is what the line means. The board already holds a PRD for this —
`a-verify-block-resolves-the-board-absolutely-not-from-its-cw`, `analyzing`.
Reported, not fixed.

`python3 resources/memos.py verify no-harness-under-the-board-dispatches-it`
is the same shape of problem for a different reason: `memos.verify` runs a
`verify:` command with `cwd` set to the board's parent — the checkout — and
the two new files exist only in the lane until this PRD collects. Staging both
files into the checkout for the length of one command and removing them again
gives `BROKEN (exit 1) — 4 check(s) failed`, those four being the mechanism
half, which is also only in the lane. Run with the lane as its repo, which is
what the checkout becomes on collect, the same command's script is green
(7 PASS, exit 0, quoted above). The checkout was left byte-identical.

## Defects outside this scope

- **`--dry names every row it would launch` reads the live board's dependency
  graph as its assertion.** It is red whenever nothing on the machine happens
  to be dispatchable, which is a fact about the day rather than about the
  dispatcher. `@.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`
  is the neighbouring ruling. Belongs to
  `the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel`.
- **`plan boards` and `plan all` print a row for a board named `all`** —
  `skipped all — no path — the merged page, not a board`. `boards()` returns
  it in `skipped`, so the merged read prints a line about a scope word as
  though it were a board. Cosmetic, pre-existing, in `read_main`/`boards`, not
  in this footprint.
- **`memos.py check` is red board-wide**: 43 of 44 memos carry no `tags:`
  block. One `memos.py retag` fixes every one of them, and it would rewrite
  eleven other PRDs' in-flight memo files, so it was not run. Mine was tagged
  on its own.
- `python3 resources/prose.py check` on the new memo reports one unbound waste
  word, below every neighbouring memo (the reference invariant memo reports
  nine). Seven were removed; the last reads worse without it.

## The gate

`bash resources/doctor.sh` from the lane: `skills ok · plugins ok · index
broken (4 problems — the baseline four) · statusline ok · guard ok · board ok
· vault broken · vision ok · origin broken · memos broken (44 memos · 43
problems) · workflows broken · grammar ok · health ok · knowledge broken ·
briefs ok · questions broken · view ok · plan ok`. Every broken row is
pre-existing and belongs to another PRD; `index` holds at its baseline four
and `memos` went from 44 problems to 43, the README staleness this PRD created
and closed.

`doctor.sh --harnesses` was **not** run — spec03 says not to until the three
pass, and one does not. It is now safe to run in the sense the PRD meant: no
harness under `prds/` launches a dispatcher any more.

## Footprint

In the lane, `lane/a-harness-never-dispatches-the-live-board`:

    M  resources/board/plan.py                  (already stood; reviewed)
    M  resources/board/run.py                   (already stood; reviewed)
    ?? resources/invariants/harness-dispatch-reader.py
    ?? resources/invariants/no-harness-under-the-board-dispatches-it.sh
    M  references/files.md
    M  index.md

On the board, in the board's own git repo:

    .pearde/memos/no-harness-under-the-board-dispatches-it.md      (new)
    .pearde/memos/README.md                                        (regenerated)
    .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
    .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/verify.sh
    .pearde/prds/no-work-is-lost-on-the-board/the-board-locks-by-realpath/probe/probe.py

No file under `health`'s floor is in this footprint. No word was needed that
`grammar.py show` does not define. Nothing was learned outside this tree, so
nothing was written to `knowledge.py`.
