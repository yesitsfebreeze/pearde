# report — init-seeds-a-board-doctor-calls-green · implementer · as engineer

Verdict: **DONE** — spec01 10/10 boxes, spec02 7/7 boxes, 17/17. Both
`## Verify and Proof` blocks exit **0** under `pipefail`, the way `collect`
runs them. This PRD's probe reads `41 checks · 41 pass · 0 fail · 0 skip`;
the quickstart `37 checks · 37 pass · 0 fail`, up from a `31 checks · 30 pass
· 1 fail` I re-derived myself rather than inherited.

This pass was an **attack**, not a re-run. The analyst wrote the code, the
probe, the boxes and the proof block, which is the shape
`.pearde/memos/one-author-is-not-an-accepted-spec.md` refuses. Re-running its
four mutations would only have proved its four mutations still work. So each
box was asked the question its author could not ask it — *what environment,
input or ordering makes this check pass while the thing it names is false?* —
and that question was then built and fired.

**Seven boxes survived. One did not, and the hole behind it is now closed.**
`index_memos` swallowed a failing `memos.py index` in silence: `init` exited
`0`, printed **nothing at all**, and left a board whose very next line of
output — its own `doctor` call — read `memos broken`. The one obligation in
this PRD's title could go unmet while the command that owed it reported
success. Fixed in the footprint, with a check, a box, and its own red.

Three boxes were added (two to spec01, one strengthening spec02's tripwire),
each against a predicate I saw fail. The probe grew from 36 checks to 41.

## What I attacked, and what happened

| # | attack | result |
|---|---|---|
| A1 | is the regenerated index the **same bytes** the source board had, or just a file with the right name? | **identical.** `cmp` silent against `resources/board/example/memos/README.md`. The analyst claimed a generated page; it is byte-for-byte the committed one. Now a box, falsifiable under M6 |
| A2 | `init --example` twice into the same target | idempotent. Second run exits 0, prints the board line, doctor still green |
| A3 | `upgrade` twice over an `init` board | exits 0 both times, doctor green, index unchanged. The two runs' output differs by one line — `board-git +=`, upgrade's own gitignore step having nothing left to add. Correct, and outside this footprint |
| A4 | a board whose index and graph were deleted: does `init` or `upgrade` repair it? | **the graph, yes; the index, no.** See finding 2 — the analyst asserted this, I have the red |
| B1 | build my own no-Obsidian home and drive the leg from it | `vault ok · … · Obsidian not installed here, so nothing to register`, doctor exit 0, green, 18 rows read. Confirmed independently of the analyst's fixture |
| B2 | can the leg pass because the fixture has **no board**, rather than because the row answered? | **no — but only just.** See finding 9 |
| B3 | make `memos.py index` fail and watch `init` | **the defect.** Silent. Fixed |
| — | ports | every port in both footprint files and the probe is bound at 0 and read back from the kernel. The only literal is `27124` in a docstring, which nothing binds. `.pearde/memos/a-check-decided-by-scheduling.md` rule 1 is met |
| — | the `skip` | 41 pass standalone vs 36 pass + 1 skip under `PEARDE_HARNESSES=1`. A skip is never counted a pass, and the number printed is not the number it would have printed had it run — rule 2 met. And the stand-down does not retire the check board-wide: `readme-in-three-rings/probe/verify.sh` runs `quickstart.sh` **unconditionally** (line 105, guarded only by `--no-run`, which the sweep never passes), so the sweep does run it |

## The defect I found, and the fix

`index_memos` ended:

```python
    if out.returncode != 0:
        return None
```

`cmd_init` then prints only `if indexed:`. So a `memos.py index` that fails
for any reason — an unwritable board, a memo it chokes on — produces an
`init` that exits `0`, says nothing about the index and nothing about the
failure, and hands back a board holding memos and no index. Driven, not read:
with the *copy's* `memos.py index` made to exit 1, `init` exit `0`, zero
lines mentioning the index, zero mentioning any failure, `memos/README.md`
absent, and `doctor` exit `1` on `memos broken · 1 memos · 1 problem`.

None of the eight original boxes could see it. Every one reads the happy
path. This is the failure mode the memo names exactly — *an author writes the
check around the behaviour they built, so the check describes the build
instead of the contract.*

The fix says what failed, in `init:`'s voice, and names the repair. The happy
path is byte-for-byte unchanged; `written[-1]` also removes an unguarded
`splitlines()[-1]` that would have raised `IndexError` on empty stdout.

## The two numbers, re-derived rather than inherited

The brief said the pre-fix count could not be recovered after an edit. It
can, and I did — the footprint is **uncommitted**, so repo `HEAD` still holds
the pre-fix text. `git clone --no-hardlinks` of the repo at `5ebefc7` into
scratch, plus `git -C .pearde show HEAD:…/quickstart.sh` written into it at
the depth the script resolves `ROOT` from, and the committed quickstart ran
against a genuinely pre-fix tree:

```
FAIL: 2 doctor closes green — missing 'pearde: every part this repo owns checks out.'
31 checks · 30 pass · 1 fail          (exit 1)
```

with, inside that run, `memos broken · README.md: the kind index is stale —
run 'memo index'` and `knowledge broken · graph.json missing — run relink` —
obligations 1 and 2 verbatim. Post-fix, on the live tree: `37 checks · 37
pass · 0 fail`, exit 0. Box 1 of both specs is falsifiable against a red I
took myself. This is a `capture-the-harness-baseline` edit, below.

## Mutations — mine, on top of the analyst's four

Each applied to the working tree, run, restored by `cp` from a scratch dir
**outside** the repo, `cmp` identical after every restore. `git checkout` was
never used: it would have discarded the analyst's uncommitted build.

| id | mutation | red it produced |
|---|---|---|
| **M5** | `index_memos` reverted to the bare `if out.returncode != 0: return None` | `41 · 39 pass · 2 fail`, exit 1 — `B a failing memo index is said, not swallowed`, `B ...naming what memos.py reported` |
| **M6** | one comment line appended to `resources/board/example/memos/README.md` **in a scratch repo copy**, `init --example` rerun there | `cmp` reports `differs` — the byte-identity box is falsifiable. The repo was never written to |
| **M7** | the probe's own replace-anchor broken so its `memos.py` mutation lands nowhere | `41 · 38 pass · 3 fail` — `B the failing-index mutation reached the copy — got: 0 · want: 1`, and the two boxes it guards go red with it. Without this tripwire an anchor that stopped matching would leave a check that cannot fail |
| **M1** (the analyst's, re-run on **my** tree) | both calls removed from `cmd_init` | `41 · 17 pass · 24 fail`, exit 1 — every A, B, C, D box, plus `E ...and closes green`, `F doctor calls the empty board green too`, `G doctor is still green after it`, and both `H` rows |

## Counts

| harness | before | after |
|---|---|---|
| `readme-in-three-rings/probe/quickstart.sh` | `31 · 30 pass · 1 fail`, exit 1 — **re-derived by me at `HEAD` 5ebefc7** | `37 · 37 pass · 0 fail`, exit 0 |
| `readme-in-three-rings/probe/verify.sh` | `74 · 73 pass · 1 fail` (my own baseline, before my first edit) | `74 · 73 pass · 1 fail` — unmoved. The one FAIL is `G index.py check is silent — got '115'`, the neighbour's. **No `H` row fails** |
| this PRD's `probe/verify.sh` | `36 · 36 pass · 0 fail · 0 skip` (analyst's) | `41 · 41 pass · 0 fail · 0 skip`, exit 0 |
| the same under `PEARDE_HARNESSES=1` | `32 · 31 · 0 · 1 skip` (analyst's) | `37 · 36 pass · 0 fail · 1 skip`, exit 0 |
| `python3 resources/index.py check` | 115 problems, exit 1 | 115 problems, exit 1 — **unmoved, and not mine** |
| `bash resources/doctor.sh .` | `index broken · 115 problems`, exit 1 | identical, exit 1 — the same single row |

`index.py check`, separated exactly as the brief specifies: lines **not**
naming `node_modules`/`package.json`/`package-lock.json` = `0`; lines naming
`init.py`, `memos.py` or `knowledge.py` = `0`.

Nothing was running against a fixed port in any of these runs. `HEAD` did not
move in either root during the run: `5ebefc7` (repo) and `8b7468b` (board) at
first command and at last.

## Findings

The analyst's six, carried forward by name, then mine.

1. **`ignore_patterns("README.md")` is broader than it reads.** Stands, and
   is now sharper: a sibling has since **committed**
   `resources/board/example/memos/README.md` (tracked at `HEAD`, absent from
   the untracked list). The pattern still eats it at copy time, so that
   committed file reaches no board `init` ever makes — only the regeneration
   puts a page there. It happens to be byte-identical to what
   `memo index` writes (A1), which is why nobody has noticed. The next
   `README.md` added at any depth of the example board will be eaten the same
   way and will not have a generator behind it.
2. **`upgrade` does not regenerate the memo index.** Asserted by the analyst;
   **demonstrated here.** On a board whose `memos/README.md` and
   `wiki/.graphify/` were deleted: `init --example` again → both still
   absent (it no-ops on an existing board); `upgrade` → `graph.json`
   restored, `memos/README.md` **still absent**; `doctor` exit `1`,
   `memos broken · 1 memos · 1 problem`. So `plant_graph` being shared
   repairs one half and the unshared `index_memos` leaves the other, and
   **no command on the board repairs a stale index except `memo index`
   itself.** One line in `cmd_upgrade` closes it. Not taken: widening the
   contract is REFINE, not initiative — and the asymmetry is now on record
   with a red rather than a sentence.
3. **`index broken · 115 problems` is the neighbour's and is untouched.**
   Re-verified above, both counts `0`. Sole remaining failure in the
   `readme-in-three-rings` harness. Not repaired here.
4. **The parent's `probe/run-all.sh` is still broken** (`printf "" "$out"`
   twice). Every number in this report comes from an exit code and a
   harness's own tail line, never from that file.
5. **The knowledge query enqueued no gap.** Nothing was learned outside this
   repo this pass, so nothing new was written back. The analyst's
   `wiki/sources/260901-a7d3.md` (BSD `sed` alternation) stands.
6. **`probe-then-spec` fitted the run.** Two `### Edits` below — both real,
   both cost time, neither needs a new atomic.
7. **`index_memos` swallowed a failing `memos.py index`.** Found by attack,
   **fixed** in the footprint, boxed, and seen red under M5. Detail above.
8. **`plant_graph` does not check `returncode` either.** Deliberately left.
   Unlike `index_memos` it is not silent — it prints the failing verb's first
   stderr line as `init: knowledge <verb> — <line>` — and it is now shared
   with `cmd_upgrade`, where that exact behaviour has always stood. Changing
   it changes both commands, which is the `blast-radius: mid` the spec names.
   A defect for whoever next opens that function, not for this contract.
9. **`doctor` over a directory holding no board closes green.** Exit `0`,
   `pearde: every part this repo owns checks out.`, under the same scrubbed
   home. So spec02's box 1 (*exits 0 and closes green*) and box 4 (*no row's
   verdict moves*) would **both pass on a fixture that never had a board**.
   Three checks refuse it and only three: the `vault` verdict field comes
   back empty (`[]`, not `ok`), `Obsidian not installed here` is absent, and
   the row reader reads `7` rows instead of `18`. The leg is safe, and it is
   safe because of the tripwire and the naming box — not because of the two
   boxes that read most like the contract. Recorded on spec02's box 5.
10. **Both `## Verify and Proof` blocks exited 1 under `pipefail`.** spec01's
    on `grep -c` returning exit 1 for a count of **zero** — the very number
    that proves the neighbour's red is not ours; spec02's on the neighbour
    harness's own exit. Either would have had `collect` refuse with
    `spec<NN> exit 1 — nothing written` while every command passed by hand.
    **Fixed in both.** The `write-the-specs` atomic covers the second shape
    and not the first — edit below.
11. **`resources/board/state/serve.json` does not exist on this machine**, so
    `I the live daemon's registry is untouched` (this probe) and `the real
    registry is untouched` (the committed quickstart) currently compare `""`
    to `""`. Not unfailable — either would go red if a fixture created the
    file, which is what they are for — but the sentinel is weaker than it
    reads, and it is the same empty-string shape the analyst caught in
    `rows()`. Named, not changed: the quickstart's is committed and
    pre-existing, and hardening it is not this contract.

## Boxes

**spec01 — 10/10.** The eight the analyst wrote all survived attack; each is
ticked against a red I reproduced (M1 on my own tree, above). Two added:
byte-identity of the regenerated index (M6), and the silent-swallow box (M5,
with M7 pinning its tripwire).

**spec02 — 7/7.** All survived. Box 5 (the 18-row tripwire) carries the
vacuous-fixture red from finding 9; boxes 1 and 4 are ticked knowing they
alone would not have caught it.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | pass. Both specs, the analyst's report, the two memos the brief named. `git status --short` recorded in **both** roots before the first edit. Footprint spans the code repo and the board, per that step's own row |
| 2 | `capture-the-harness-baseline` | pass, **and better than the atomic allows.** The footprint already held another worker's build, which the atomic says leaves no recoverable baseline. It was recoverable — see `### Edits` |
| 3 | `attempt-the-build` | pass, one loop back. The build here is an attack; it found one defect (finding 7), which was built **in place in the footprint file**, since a guard has no meaning outside the function it lives in. Every fixture under a `mktemp -d` removed at exit; no `?? prds/<slug>/` appeared |
| 4 | `re-run-the-harnesses` | pass. Every count ≥ baseline; the one red is the neighbour's and was recorded red before my first edit. No harness edited. No flip claimed that `git show HEAD:` did not back — the pre-fix clone *is* that check, run end to end |
| 5 | `write-the-specs` | pass, one loop back — the `pipefail` refusal in finding 10, caught by running the blocks the way `collect` will rather than by hand |

Back-edges: one into `attempt-the-build` (the M5 defect), one into
`write-the-specs` (the `pipefail` exits). Neither taken twice.

### Edits

**`capture-the-harness-baseline` → `#### Done when`.** The third bullet says a
baseline cannot be reconstructed once a previous worker's build is in the
footprint, and prescribes citing their numbers as inherited. That is right
when the build is *committed* and wrong when it is not — the case this route
produces most often, since `probe-then-spec` ends with the analyst's build
uncommitted by design. Replacement text for that bullet:

> - **Resuming a killed run, or taking a second pass at a footprint another
>   worker already built:** if the earlier build is **uncommitted**, the
>   pre-edit tree is still on disk and the baseline is recoverable — do not
>   inherit it. `git clone --no-hardlinks <repo> <scratch>/prefix` gives the
>   tree at `HEAD` without the build; write any harness that lives in a
>   sibling worktree in at the depth its `ROOT` resolves from
>   (`git -C <board> show HEAD:<path>`), and run it there. Quote that count
>   as yours. Only when the earlier build was **committed** is there no
>   pre-edit baseline: then record the tree as it stands, cite the earlier
>   worker's numbers, and say in the report that the baseline is inherited. A
>   number honestly labelled inherited is worth something; a number that
>   could have been re-taken and was not is worth less than it looks.

**`write-the-specs` → `#### Fails when`, a new row.** The existing `pipefail`
row names board-wide gates. A `grep -c` that legitimately counts **zero** is
not a gate and exits 1 all the same, and it is the commonest last line in a
block that separates a neighbour's red from your own:

> | `collect` refuses with `spec<NN> exit <n> — nothing written`, and the block's last line is a `grep -c` printing `0` | `grep` exits 1 when it matches nothing, and a count of zero is the *expected* answer for a line that proves a red is not yours — so the block's happiest number is also its failing exit | append `\|\| true` to any `grep -c`/`grep -vc` whose passing value is `0`; the count still prints. Then check it the way collect will — extract the block with `awk` and run it under `set -o pipefail`; it must exit 0. Running the lines by hand will never show this |

Neither `attempt-the-build` nor `re-run-the-harnesses` needed an edit: the
rows added to them this afternoon — the uncommitted-footprint `cp`/`cmp`
protocol, and the neighbour-harness stand-down — both covered what I hit,
exactly as written.

## Nothing was committed

`resources/board/init.py` modified in place;
`prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh`
modified in place (the disclosed neighbour write, unwidened — it is still the
only file this PRD touches outside its own directory); `probe/`, `specs/` and
this report untracked under this PRD. Nothing at the repo root. No file owned
by the parallel session was opened.

## Scores

complexity: 12
blast-radius: mid
workflow: probe-then-spec
