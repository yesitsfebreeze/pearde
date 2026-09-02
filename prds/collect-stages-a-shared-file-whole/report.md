# collect-stages-a-shared-file-whole — implementer report

Verdict: DONE

19/19 boxes ticked — spec01 6/6, spec02 7/7, spec03 6/6. **Second revision**,
after a review refused the first: three boxes were green by construction, and
one spec pinned its own harness's total. Both are closed below; every box now
rests on a check that stands in the tree and that I have shown going red.

This is the route's **second** pass. The analyst probed, specced and built;
a first implementer was killed by a rate limit at 11:28 having ticked nothing.
Per `attempt-the-build`'s "the specs already exist and the build is already in
the tree" row I ran steps 1, 2 and 4 only — step 3 (build) and step 5
(write-the-specs) were not entered, and **I claim no red-to-green flip**:
every behavioural flip on this tree was earned by the pass that built it.

Probe: `probe/verify.sh`, **32 passed, 0 failed** (was 25 — three checks
folded in this revision). No spec pins that number any more.

## What the two footprint files' mtimes mean

Asked directly, so answered directly.

- `references/parts/commits.md` — mtime **11:26:16**, and it has not moved
  since. My first command ran at ~11:29. **I have never written this file.**
  That mtime is the killed implementer's (claimed 11:21:22, died 11:28), which
  is also when the work spec02 and spec03 contracted for it landed. Its content
  is correct and I verified it by needle, not by mtime.
- `resources/board/collect.py` — mtime was **11:27:35** when the review looked,
  for the same reason. It now reads **11:50:33, and that one is mine**: this
  revision mutated the file three times to prove the three new checks can fail,
  restoring it from a scratch backup each time. `cp` bumps mtime whatever the
  bytes say. **The content is byte-identical to the pre-mutation backup** —
  `cmp <scratch>/collect.py.bak resources/board/collect.py` clean, `git diff
  -U0` still 13 hunks in the same four places, `git diff --stat` still
  `135 +++…---`, and `git status --short` still byte-identical to the baseline
  I took before my first command.

So: my first report's "no code-repo file written this run" was true when
written and is **false now**, and the review was right not to accept a mtime
as proof either way. The honest statement is: I wrote `collect.py` three times
and restored it three times; the delivered bytes are pass one's, unchanged.

## What this revision changed

**1 — the pinned total is gone, from all three specs, not one.** The review
found the literal `25` pinned in one place. It is one place for `25`, but the
same disease was in the other two specs against their *neighbours'* totals, and
those are worse: a sibling adding a **passing** check to their own harness would
have reddened this unit.

| spec | was | now |
|---|---|---|
| spec01 box 6 + block | `grep -q '47 pass · 0 fail'` | the tally is parsed: `NF == 8 && checks == pass && fail == 0` |
| spec02 box 7 + block | `grep -q '23 passed, 0 failed'` | parsed: `NF == 4 && passed >= 1 && failed == 0` |
| spec03 box 4 + block | `grep -q '25 passed, 0 failed'` | parsed, same shape |

Shown able to fail, by feeding each matcher a losing tally:

```
  checks-tally [47 checks · 46 pass · 1 fail] -> exit 1
  checks-tally [47 checks · 47 pass · 0 fail] -> exit 0
  checks-tally []                             -> exit 1
  passed-tally [31 passed, 1 failed]          -> exit 1
  passed-tally [32 passed, 0 failed]          -> exit 0
  passed-tally []                             -> exit 1
```

The empty case matters: a harness that dies before printing a tally must not
read as a pass, and it does not.

**2 — the three missing checks are standing scenarios now**, not scratch.
`probe/verify.sh` went 25 → 32.

| check | where | backs |
|---|---|---|
| `1f-widen-offered` | scenario 1 | spec02 box 5 — the refusal must **offer** `--widen <path>`, not only name the clash |
| `1g-no-stale-clause` | scenario 1 | spec03 box 3 — a claim that **does** hold a `repo` side must never carry the stale-claim clause |
| `7a`–`7e` (new scenario 7) | a board that is **not** its own repo — a plain `.pearde/` inside the code repo, the layout no other scenario builds | spec01 boxes 4 and 5 — no second side is written, `sides` holds `board` only, the top-level alias **is** the board side (identity, not equality), and the code dirt is in that one side |

spec01's block now runs `verify.sh 0 2 6 7` so its own boxes are covered by its
own block; spec02's `1 2 4 5` picks up `1f`/`1g`; spec03 runs the whole set.

**3 — each new check shown red before green.** Three narrow mutations of
`resources/board/collect.py`, each backed up to a scratch dir outside the repo,
run, then restored and `cmp`-proved. A check written from the answer passes on
the answer, so each mutation removes exactly the behaviour the check names:

| mutation | check that fired | quoted |
|---|---|---|
| drop `` `--widen {path}` takes it whole `` from the refusal string | `1f` | `FAIL 1f-widen-offered: expected [`--widen shared.py` takes it whole] in: collect: prds-a: shared.py is in prds-b's footprint too — not only this PRD's edits` |
| `stale = (base is not None and …)` → `stale = True` | `1g` | `FAIL 1g-no-stale-clause: did NOT expect [recorded before the baseline covered] in: … this claim was recorded before the baseline covered /var/folders/…/code …` |
| `if code and code != root:` → `if code:` in `snapshot` | `7b`, `7c` | `FAIL 7b-no-repo-side-written: wrote repo,diff.repo,untracked.repo` / `FAIL 7c-sides-board-only: sides=['board', 'repo']` |

Each restore proved: `RESTORED A: identical`, `RESTORED B: identical`,
`RESTORED C: identical`, and `git diff -U0` back to 13 hunks after C.

The scratch fixtures the first revision leaned on are now redundant and are not
part of the delivery; their assertions live in scenario 7 and in `1f`/`1g`.

## Per-spec box status

### spec01 — the claim baseline records the code repo, not only the board's — 6/6

| box | standing check |
|---|---|
| a claim snapshot names a dirty code-repo path | `0a-board-is-its-own-root`, `0b-baseline-holds-code-path` |
| partly-older/partly-newer file staged by hunk | `2b-dry-splits`, `2c-real-exit`, `2d-a-line-committed`, `2e-b-line-not-committed` |
| older lines still unstaged in the tree | `2f-b-line-still-in-tree` |
| board NOT its own repo: no `repo` side, behaviour unchanged | **new** `7a-board-is-not-its-own-root`, `7b-no-repo-side-written`, `7d-alias-is-the-board-side`, `7e-code-dirt-in-the-one-side` |
| a one-repo claim dir still loads, `sides` has `board` only | **new** `7c-sides-board-only` |
| `hunks-land-where-they-came-from` still all-pass | tally parsed, `47 checks · 47 pass · 0 fail` |

Block (run as collect runs it, `bash -e -o pipefail`): **exit 0**.

```
---- 17 passed, 0 failed
verify.sh exit 0
hunks-land-where-they-came-from: 47 checks · 47 pass · 0 fail
```

The back-compat alias spec01 asked me to reconsider **stays**, and is now
checked rather than argued: `7d` asserts
`baseline()["hunks"] is baseline()["sides"]["board"]["hunks"]` — the same
object, not a copy. `hunks-land-where-they-came-from`'s probe reads that
top-level key directly; dropping it reddens another PRD's probe for nothing.

### spec02 — every contender is seen, and the split is tried before the refusal — 7/7

| box | standing check |
|---|---|
| a `specced` sibling refuses, naming the sibling, exit 1 | `1a`, `1b`, `1c` |
| its line is not in `HEAD`, nothing committed | `1d`, `1e` |
| a `done` sibling refuses nothing | `5a-done-sibling-ok` |
| a file the baseline partly explains is split, not refused | `2a`–`2f` |
| a file the baseline explains no hunk of is refused **with `--widen <path>` offered** | **new** `1f-widen-offered` |
| `commits.md` no longer names `claimed` only, and names the split | `grep -c "no other \`claimed\` PRD writes that footprint"` → `0`; the file reads "every live state but `open` … and `done`" and "split by hunk … refused with `--widen <path>` offered when it explains none — never swept whole in silence" |
| the sibling PRD's probe still all-passing | tally parsed, `23 passed, 0 failed` |

The refusal, verbatim from the real (non-`--dry`) run:

```
collect: prds-a: shared.py is in prds-b's footprint too — not only this PRD's edits; `--widen shared.py` takes it whole
```

Block: **exit 0** — `---- 17 passed, 0 failed`, `collect-commits-only-the-prd-s-own-edits: 23 passed, 0 failed`.

Its line `if grep -q "only this PRD's edits" references/parts/commits.md; then :; fi`
still does not gate, and the needle is absent from `commits.md` (`grep -c` → 0)
— that sentence lives in `collect.py`'s refusal string, where it belongs. Left
as written: the box above it is carried by the two needles that do gate.

### spec03 — a claim taken before the fix says so, and the harness is on the board — 6/6

| box | standing check |
|---|---|
| a claim with no `repo` side refuses, naming the uncovered root and the re-snapshot command | `6a-exit`, `6b-says-why` |
| it commits nothing and leaves the sibling's line | `6c`, `6d` |
| a claim that **does** hold a `repo` side never shows that clause | **new** `1g-no-stale-clause` |
| `probe/verify.sh` exists and exits 0 with none failing | tally parsed; `---- 32 passed, 0 failed`, `verify.sh exit 0`. `probe/run.sh` is gone — the rename spec03 contracted was done in an earlier pass, so the brief's `run.sh` spelling is stale |
| no argument runs every scenario, `1 2` runs only those two | full run 32 labels; `1 2` prints exactly `1a 1b 1c 1d 1e 1f 1g 2a 2b 2c 2d 2e 2f` — `selected run made 13 checks`, no number pinned |
| `commits.md` says the record covers the board's repo and the code repo | "That record covers two roots — the repo the board is in and the code repo the footprint lands in — keyed apart"; `grep -c 'the code repo'` → `2` |

Block: **exit 0** — `---- 32 passed, 0 failed`, `probe tally: 32 passed, 0 failed`.

## Workflow probe-then-spec

| # | step | result |
|---|------|--------|
| 1 | `read-the-contract` | ok — PRD, three specs, no `## Answers`/`## Questions`; `git status --short` recorded before the first command; both footprint paths on disk and dirty |
| 2 | `capture-the-harness-baseline` | ok — 13 harnesses naming `collect.py`/`.claims`/`--snapshot`, plus `index.py check` and `doctor.sh`. Baseline **inherited and confirmed**: the analyst published counts, I re-ran the set on the built tree, every count equal |
| 3 | `attempt-the-build` | **not entered** — build already in the tree, per the route's own row |
| 4 | `re-run-the-harnesses` | ok — set re-run three times (baseline, after ticks, after this revision); every count identical |
| 5 | `write-the-specs` | **not entered** — specs already written; this revision edited three `## Verify and Proof` blocks and four box sentences, which is the implementer's own repair, not spec-writing |

### Edits

Three failures the atomics caused, with replacement text.

**`capture-the-harness-baseline`, step 2 — `timeout` is not on darwin.** The
step says to save each harness's whole output; the natural wrapper
`timeout 900 bash <harness>` exits 127 on darwin with `command not found`, and
a worker that does not read the wrapper's exit code records thirteen empty
files as thirteen baselines. Add to `## Fails when`:

| `command not found: timeout` from a harness wrapper on **darwin** | `timeout` is GNU coreutils and is not on the base system | drop the wrapper, or `gtimeout` where coreutils is installed — and read the exit code of the wrapper, not only the harness's last line |

**`attempt-the-build`, step 4 — the probe's name may already have moved.** The
brief named `probe/run.sh`; the file on disk is `probe/verify.sh`, renamed by
this PRD's own spec03 in an earlier pass. Add to `## Fails when`:

| the brief names `probe/run.sh` and only `probe/verify.sh` is on disk | a spec in this PRD's own set contracted the rename, and an earlier pass did it | take the file that exists as the same probe, name both spellings in the report, and check the spec's box against the file rather than against the brief |

**`write-the-specs`, step 3 and `attempt-the-build`, step 4 — a spec must not
pin its own probe's total.** The board's rule against pinned denominators is
written for a *neighbour's* harness. Turned inward it is worse: a spec asserting
`N passed, 0 failed` about its own probe forbids the probe from ever growing,
so the next worker cannot add the check a missing box needs without reddening
the spec that names it. That is what happened here and it cost a review round.
Add to `write-the-specs` `## Fails when`:

| a box or block asserts a literal total of the PRD's **own** probe | the spec has locked its harness shut: a later pass cannot add the check a thin box needs without reddening the spec that names it | assert the tally *parses* and `failed == 0` — never a total, not even the probe's own. A floor (`>= N`) is honest; an equality is a wall |

And to `attempt-the-build` step 4, after "one line per assertion, a count at
the end": *the count is printed, never asserted by a spec.*

## Harnesses

Baseline **inherited from the analyst's pass and confirmed** — the analyst
published every count, the harnesses are deterministic, and re-running the set
on the built tree reproduced each one. Reverting was rejected deliberately:
`resources/board/collect.py` and `references/parts/commits.md` are shared with
several live sessions, and `git checkout` would have discarded their work.
`git diff -U0 -- resources/board/collect.py` shows **13 hunks, all in
`HELD`/`snapshot`/`baseline`/`sort_paths`** — every one this PRD's; no foreign
hunk is in either footprint file, before or after this revision.

| harness | analyst's | baseline | after ticks | after this revision |
|---|---|---|---|---|
| `an-unknown-flag-refuses` | 196/196 | `196 · 196 · 0` | same | same |
| `filing-refuses-a-file-it-does-not-hold` | 52/52 | `52 · 52 · 0` | same | same |
| `collect-is-a-command` | 133/133 | `133 · 133 · 0` | same | same |
| `hunks-land-where-they-came-from` | 47/47 | `47 · 47 · 0` | same | same |
| `collect-keeps-its-word` | 101/101 | `101 · 101 · 0` | same | same |
| `the-loop-is-commands` | 58/58 | `59 checks · 58 pass · 1 fail` | same | same |
| `transitions-are-commands` | 74/74 | `74 checks · 73 pass · 1 fail` | same | same |
| `the-brief-names-the-verdict-line-collect-requires` | 15/15 | `15 ok · 0 FAIL` | same | same |
| `the-collect-and-brief-harnesses-are-carried-across-the-layou` | 7/7 | `7 · 7 · 0` | same | same |
| `workflow-improve` | 71/71 | `71/71` | same | same |
| `collect-commits-only-the-prd-s-own-edits-not-the-footprint-s` | 23/23 | `23 passed, 0 failed` | same | same |
| `the-line-tells-the-truth` | 85/85 | `85 · 85 · 0` | same | same (did not flake) |
| `collect-stages-a-shared-file-whole` (this PRD's) | 25/25 | `25 passed, 0 failed` | same | **`32 passed, 0 failed`** — this unit added 7 checks; no pre-existing check moved |

`python3 resources/index.py check` **exit 0**, silent, at every one of those
points. `bash resources/doctor.sh` **exit 1**, identical row for row across
runs except the `knowledge` row's note list (a sibling is writing knowledge
notes live).

Two harnesses are red **and neither is mine — both were red before my first
command**, and both name files outside my footprint. Left alone, as instructed:

- `the-loop-is-commands`: `FAIL loop.md is 177 lines` — the check caps
  `references/parts/loop.md` at 170; the file is at 177 and its last commit is
  `49f09b5 the-ramp-asks-before-the-board-runs` (10:54, before my claim). The
  harness also gained a check (58 → 59): a neighbour landed a cap and a file
  that exceeds it.
- `transitions-are-commands`: `FAIL the template's comments survive` — the check
  greps a new PRD for `Ordering reads three axes`, which comes from
  `references/templates/prd.md`. A live session has that file uncommitted at
  −68 lines and the sentence is gone (`grep -c` → 0).

## Findings

Carried forward from the analyst's pass, all still standing:

- **The splitter was alive in exactly one layout, which is why it looked
  tested.** `hunks-land-where-they-came-from` was the only fixture on the tree
  whose board is not its own repo — 47/47 green over a case that could not occur
  on a real board. **Closed this revision**: scenario 7 is a second, deliberate
  instance of that layout inside this PRD's own probe, so the one-repo path is
  now asserted rather than inherited.
- **An ordering defect nothing had named** — the sibling refusal was raised
  before `nh` was consulted. Closed by spec02, proved by `2a`–`2f`.
- **The fix is not retroactive, and a board-wide re-snapshot is not the
  answer.** Twenty `.claims/*/` dirs on this machine carry no code side and will
  refuse rather than split until re-snapshotted on a clean tree. The contract's
  half is closed (spec03 makes the refusal say so); the dirs are untouched,
  deliberately.
- **Residual the design accepts.** A sibling editing a shared file both before
  *and* after the collecting PRD's claim still has its post-claim hunk
  attributed to the collector — the baseline's whole semantics is "dirt at claim
  time is not mine, dirt after is". Already on record from the analyst; this
  build does nothing about it, and the wider `CONTENDING` band does not help,
  because when the baseline explains *any* hunk the split is preferred and the
  refusal never fires. Named for completeness, not as a discovery.
- **A wrong claim in the docs, inside the footprint.** `commits.md` said step 5
  "proved no other `claimed` PRD writes that footprint". **Fixed** — the needle
  is gone and the wider band plus the split outcome are written in its place.
- **Out of scope, not fixed.** `the-line-tells-the-truth`'s `F5` sentinel flake
  — did not reproduce across three runs this pass (85/85 each), still covered by
  `leaked-background-services-outlive-their-fixtures`.

New this pass:

- **`doctor` is red on two rows that are board state, not code.** `origin` —
  "2 derived in flight vs 2 requested, the board is working on itself", a call
  for the user. `knowledge` — `graph.json` behind six notes, and the list
  changed between two doctor runs, so a session is writing notes right now.
  Neither is in my footprint.
- **A spec that pins its own probe's total locks the probe shut.** The board has
  the pinned-denominator rule for a neighbour's harness; nothing said it applies
  to a PRD's own. It cost this PRD a review round: three thin boxes could not be
  covered without reddening the spec that named them. Closed here, and proposed
  as an atomic edit above. `resources/grammar.py` has no word for it.
- **A first revision can be green and still be wrong.** Every command in the
  first revision passed, and three of nineteen boxes still had nothing standing
  behind them. `grep -c '^- \[x\]'` counts ticks, not checks; only reading each
  box against a named, failable assertion catches it. Worth a `## Fails when`
  row somewhere on the implementer route, offered above.

## Health

`resources/board/collect.py` — the one file in my footprint under the floor.

| | score | worst |
|---|---|---|
| brief (at `HEAD` d646168) | 33 | branching, lines |
| working tree, as I found it and as I leave it | 31 | branching, lines |

**Nothing moved, and here is why.** The 2-point cost is pass one's own 135
lines — the two-repo baseline, the `CONTENDING` band and the stale-claim clause
— which the contract requires and which I did not write. The file's `worst` is
`collect_one`: branching 81 (the line is 10), nesting 8, longest 206 lines.
**No spec in this PRD touches `collect_one`.** Every hunk this PRD owns is in
`HELD`, `snapshot`, `baseline` and `sort_paths`. The only change that moves 31
upward is splitting `collect_one` — a refactor of a function this unit does not
touch, in the board's single writer of commit history, in a file three specs
stand on. A defect outside scope: **reported, not done.**

I considered and rejected one in-scope tidy: lifting the 17-line stale-clause
message out of `sort_paths` to module level. It removes one branch from a
function that is not the `worst`, adds no lines back, and `health.py` scores
`branching` at the file's maximum function — predicted movement zero, against a
real risk on a shared file. Churn without a measured gain is not "better than
you found it".

## Grammar

No word in the contract was undefined; `resources/grammar.py` holds 176 terms
and `doctor`'s `grammar` row is `ok`. One word I wanted and it does not define:
a name for **a check that pins its own harness's total** — the pinned-denominator
disease turned inward on a PRD's own probe. The outward case is named on this
board; the inward one is not, and it is what refused this PRD's first DONE.

## Knowledge

Nothing was learned outside this repo — every fact came from the tree, the
probe or a fixture built here — so nothing was written back with
`knowledge.py remember`.
