# upgrade-leaves-the-memo-index-stale — implementer report

Verdict: DONE

All nine acceptance boxes in `specs/spec01.md` are ticked, each against output
this run printed. The build the analyst left in `resources/board/init.py` was
read, driven and measured rather than trusted: a pre-build baseline taken in a
clone at `HEAD f3aea95` reads **23 pass · 16 fail** on this PRD's own probe, and
the same probe on the working tree reads **40 checks · 40 pass · 0 fail ·
0 skip**. Every box's predicate was therefore seen red before it was seen green,
on the committed file, not only through section F's mutation — **with one
exemption: box 8's registry half had never been seen red anywhere, because it
could not fail. That is corrected below, and the replacement has been seen
red.**

The whole `## Verify and Proof` block was run the way `collect` runs it —
extracted with `awk`, under `set -o pipefail` — and **exits 0**.

Two checks in this PRD's own probe could not fail. One was real and is repaired;
the other I misdiagnosed and reverted. Both are written up below. Nothing
outside `.pearde/prds/upgrade-leaves-the-memo-index-stale/` was written, and
`resources/board/init.py` was not edited by me at all.

## Numbers

| thing | pre-build (clone at `f3aea95`) | working tree, final |
|---|---|---|
| this PRD's probe | **23 pass · 16 fail · 1 skip** (exit 1) | **40 pass · 0 fail · 0 skip** and **39 pass · 0 fail · 1 skip**, both exit 0 |
| `init-seeds-a-board-doctor-calls-green` | 41/41 | 41/41 (one transient 40/41 under load — below) |
| `guard-on-is-one-command` | 78/78 | 78/78 |
| `readme-in-three-rings` | 74/74 | 74/74 |
| `the-next-line-runs` | 96/96 | 96/96 |
| `init-asks-nothing` | 88/88 | not re-run (no footprint edit of mine) |
| `the-loop-is-commands` | 58/58 | not re-run (same) |
| `python3 resources/index.py check` | — | silent, exit 0 |
| `bash resources/doctor.sh` | — | exit 0, 0 rows `broken`, closes green |
| `.pearde/.state/serve.json` | `77fbcab1…` | `77fbcab1…` — byte-identical |

`HEAD` was `f3aea95` before the first command and `f3aea95` after the last.
Both probe readings are the two the spec names; the skip is section H's
Obsidian stand-down and is never counted a pass.

**One transient red, not mine, and not hidden.** The final `## Verify and Proof`
run read `init-seeds-a-board-doctor-calls-green` at `41 checks · 40 pass · 1
fail`. Re-run alone immediately afterwards it read `41/41` again, twice. No file
in my footprint moved during that window — `resources/board/init.py` mtime
`00:01:55` and `resources/doctor.sh` mtime `00:03:22` against a block that
started at `00:48:08`.

**My first attribution — a shared-vault/port artifact of a loaded harness set —
was too vague, and the real one is worse.** That harness is not a neutral
neighbour: it is *inside the live footprint of a PRD being implemented in
parallel*. `the-harness-sweep-is-capped-so-a-red-is-a-real-red/specs/spec03.md`
declares

```
footprint:
  - .pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe
```

and that PRD is `state: claimed`, `claim: impl-cap 2026-09-02 00:22`, with its
worker's processes live on this machine as I write. So I was reading a harness
whose owner was working it. (One nuance the mtime adds: that `verify.sh` reads
`Sep 2 00:00:11`, *before* my block — so this was not a half-written file caught
between two saves. The interference is the owner **exercising** that footprint —
running the harness, binding its ports, building fixtures under it — while I ran
the same file.)

Quoting the red instead of suppressing it is what surfaced the correlation, so
the general rule holds and is worth restating: **a red inside another PRD's
declared footprint is that PRD's, and a worker cannot tell the difference from
inside its own run — only the board can.** `a-check-decided-by-scheduling.md`
still governs the shape; the cap this very PRD-in-flight exists to add is the
mechanism. The `41/41` re-runs are the honest number for this unit.

## The pre-build baseline, and why it is worth more than section F

The build was uncommitted, so the pre-edit tree was recoverable and I did not
inherit the analyst's numbers. `git clone --no-hardlinks` at `f3aea95`, the
board copied in (it is gitignored, so a clone carries none of it), and the same
seven harnesses run there. The clone's `init.py` holds no
`index_memos(board, "upgrade")` — `grep -c` is `0`.

On that tree this PRD's probe fails sixteen checks, and they are exactly the
sixteen the contract is about:

```
FAIL  B ...and says it regenerated the page
FAIL  B memos/README.md is on the board — got: no · want: yes
FAIL  B memo check exits 0 — got: 1 · want: 0
FAIL  B ...and says nothing — got: 55 · want: 0
FAIL  B the page is the generated one, not a copied one
FAIL  B ...and byte-identical to the example board's own page — got: differs
FAIL  C doctor exits 0 on the upgraded board — got: 1 · want: 0
FAIL  C ...and closes green
FAIL  C the memos row reads ok — got: broken · want: ok
FAIL  C no row reads broken on either board — got: 1 · want: 0
FAIL  C every other row's verdict matches the fresh board's — got: 2 · want: 0
FAIL  C ...and the two boards' index pages are the same bytes — got: differs
FAIL  D ...and the row says the index is already current
FAIL  E ...and says there is nothing to index
FAIL  G the failure is said, not swallowed
FAIL  G ...naming what memos.py reported
```

Section F proves the boxes can fail by mutating a *copy*. This proves the same
thing against `HEAD` itself, which is the stronger statement, and it is what
`memos/one-author-is-not-an-accepted-spec.md` asks for. The four neighbour
harnesses read their spec-named counts on that same pre-build tree, so their
staying at those counts afterwards is a measured non-regression rather than a
coincidence.

## The two checks that could not fail

### Re-aimed — the registry check could not fail, twice over (box 8)

`probe/verify.sh:39` originally read `REG="$ROOT/resources/board/state/serve.json"`.
There is no such file, so `REG_BEFORE` was the empty string, the after-value was
the empty string, and `eq "H the live daemon's registry is untouched"` compared
`''` to `''`.

My first correction pointed `REG` at the real file, `.pearde/.state/serve.json`
(`serve.py:391`, via `planlib.state_dir`). **That was not enough, and a reviewer
was right to send it back.** It turned `'' == ''` into `constant == the same
constant`, because the probe has no causal path to that file at all:

- `save_entry` returns early on an ephemeral path — `serve.py:385` defines
  `EPHEMERAL = ("/tmp/", "/private/tmp/", "/var/folders/", "/private/var/folders/")`
  and `:402` is the guard. Every fixture here is a `mktemp -d` under
  `/var/folders/`, so a fixture registration writes **no file anywhere**.
- `entry_path` is board-local, so even a fixture that did write would write the
  *fixture's* `.state/serve.json`, never this repo's.

The empirical nail is in this report's own findings. During implementation I ran
a live `init` without `PEARDE_PORT=1`, reached the daemon on `127.0.0.1:8443`,
and registered a fixture board — **precisely the failure box 8 exists to catch.**
`.pearde/.state/serve.json` is mtime `Sep 1 13:22:54` through that accident and
through five probe runs. The check read `ok` straight through its own failure
case.

So the check was re-aimed at the only half of the obligation this run can move —
the daemon's in-memory board list — and the replacement **has been seen red**,
by reproducing the accident deliberately:

```
clean:    count=0
after:    count=1   <- non-zero means the check goes RED
  z   synced 0s ago · /var/folders/…/tmp.2fNCDItELi/z/.pearde
--- and the file the old check watched ---
Sep  1 13:22:54  .pearde/.state/serve.json      <- never moved
restored: count=0                                (after `serve.py forget z`)
```

It stands down to `skip` when the daemon is not running, beside the Obsidian
check three lines below it and for the same reason — `a-check-decided-by-
scheduling.md`: a down daemon is not the same answer as a clean one, and
without the stand-down the check could go red merely because someone restarted
the service. `PEARDE_PORT=1` is exported at `:63` and would make every probe
answer "not running", so it is cleared for this one question.

The box's other half — `grep -cF -- "$TOP" "$OBS"` — is honest, can fail, and
is unchanged.

### Reverted — the vault-list needle is fine, my diagnosis was not

I also "fixed" `MINE="$(grep -cF -- "$TOP" "$OBS")"` on the theory that darwin's
`mktemp -d` hands back `/var/…` while Obsidian records `/private/var/…`, so the
needle could never match. **That is wrong, and I measured it rather than shipping
it.** `grep -F` is a substring match, and `/private/var/folders/…/x/.pearde`
contains `/var/folders/…/x/.pearde` as a substring:

```
old needle ($TOP only)      : 1
new needle ($TOP + realpath): 1
```

The needle can fail and does what it claims. The edit was reverted and the file
is back to the analyst's line. Recorded because a comment asserting a false
mechanism is worse than no comment, and because the workflow's own darwin row
invites this mistake — see `### Edits`.

## Findings

The pass-one report's findings are carried forward by name below. Three are
unchanged, one is **corrected**, and two are new.

### CORRECTED — there *are* concurrent sibling sessions, and the brief says there are not

A reviewer re-measured this one and found it worse than I reported: **eleven**
`serve.py` processes, seven from this session lineage's fixtures about nine
hours old pointing at temp boards that no longer exist, two over a day old. The
count below is my own reading and is the smaller one. Left as a finding; the
reviewer is routing it.

The brief's board-facts block states: "There is **no sibling session** — earlier
reports that warned about one were seeing each other." That is false as measured
at `2026-09-02`. `ps` during my run:

```
25090     02:25  bash …/f54db065-…/scratchpad/impl-cap/spec01.sh
60961     00:02  bash .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh
44302  08:54:40  python …/5ba5c4b5-…/scratchpad/init/copy/resources/board/serve.py run …/b-baseline/.pearde …(6 boards)
48423  08:52:53  python …/5ba5c4b5-…/scratchpad/init/copy/resources/board/serve.py run …/i2/.pearde
49977  08:52:20  python …/5ba5c4b5-…/scratchpad/init/copy/resources/board/serve.py run …/g1/.pearde …
50658  08:51:56  python …/5ba5c4b5-…/scratchpad/init/copy/resources/board/serve.py run …/lines/.pearde
51225  08:50:51  python …/5ba5c4b5-…/scratchpad/init/copy/resources/board/serve.py run …/m5/.pearde
```

Two consequences the orchestrator should have:

- **Five `serve.py run` daemons have been leaked by session `5ba5c4b5` for over
  eight hours**, each holding fixture boards under a scratch directory. They are
  not mine to kill. They are the likeliest explanation for anything on this
  board that reads a bound port as taken.
- `references/parts/doctor.md` was **clean** in my step-1 `git status --short`
  and **modified** in my final one. The brief listed it as already modified; at
  my first read it was not. A live session wrote it mid-run. My own footprint
  file's hunks are intact and `HEAD` never moved.

This is also the whole explanation of section H's `skip`. It fired on my first
two probe runs and not on the third; the vault list gained 32 entries during my
clone baseline and more during the probe, in fixture shapes (`tmp.*/{a,c,e,f,g,
h,i}/.pearde`) that are **not** mine — my probe uses `a,e,f,g` under a single
`$TOP` and `MINE` read a true `0` each time. `a-check-decided-by-scheduling.md`
applied exactly as the spec anticipated; both readings the spec names were
observed, `39 pass · 1 skip` and `40 pass · 0 skip`.

### NEW — `upgrade` contradicts itself on the failing-index path

In `cmd_upgrade`, `index_memos` returns `None` for **two** different reasons —
the board has no `memos/` directory, and the regeneration failed — and the new
row cannot tell them apart:

```python
indexed = index_memos(board, "upgrade")
if indexed:
    ...
else:
    print("  memos     no memo on this board — nothing to index")
```

Driven on a board that holds a memo, with `memos.py`'s index branch mutated to
fail:

```
upgrade: could not regenerate memos/README.md, the memo index by kind — memos: cannot write the index · the board holds memos and no index, which doctor reads as stale; run `memo index` once that is fixed
  memos     no memo on this board — nothing to index
```

The second line is false and it contradicts the first. Box 7 asks only that the
failure be *said*, and it is said, so the box is honestly ticked — but the
aligned row a reader scans is wrong on precisely the path where being wrong
costs most. This is inside my footprint and inside this unit's own code, and I
did **not** fix it: no box asserts it, section G does not `lacks` it, and
changing behaviour no box names is initiative. The fix is one line — have
`index_memos` distinguish "no memos dir" from "failed", or read
`os.path.isdir(os.path.join(board, "memos"))` in the `else`. Suggested derived
PRD: `upgrades failing memo index says the board has no memos`, footprint
`resources/board/init.py`.

### Unchanged — the `vision` row is a second divergence of exactly this shape

`write_board` seeds `vision.md` on `init` and `cmd_upgrade` never calls it, so
an upgraded board reads `vision off` where a fresh one reads `vision ok`. Doctor
calls that `off`, not `broken`, so both boards are green and the harness excludes
the row by name. **Explicitly out of my contract and untouched.** Its own
contract, footprint `resources/board/init.py`.

### Unchanged — `knowledge.py board` counts the generated index page as a memo

Observed again this run on a board holding exactly one memo:

```
  board     board: 8 PRD note(s), 2 memos scanned
```

Pre-existing on both `init` and `upgrade`, cosmetic, doctor's `knowledge` row
reads `ok` either way. **Explicitly out of my contract and untouched.** It lives
in `resources/knowledge.py`'s memo scan, not in this footprint.

### Unchanged — `init-seeds-a-board-doctor-calls-green`'s probe writes this machine's real Obsidian vault list

Named more precisely than pass one could. That harness makes three fixtures —
`$TOP/proj` (`:82`), `$TOP/ro` (`:125`), `$TOP/bare` (`:167`) — and isolates
`HOME` only for the `doctor` call at `:152`. Every `init` it runs therefore
reaches `register_vault` with the real home, and the list is thick with entries
pointing at temp directories that no longer exist. **The count I first reported
here — "859 entries" — is withdrawn: it does not reproduce.** `len(vaults)` read
`832`, `845` and `859` during my run, a reviewer read `82`, and it reads `96` as
I write this. Obsidian prunes the file, and a neighbour harness adds to it in
bursts, so any single number is a reading of one moment and not a fact about the
machine. The mechanism is the finding; the count is not evidence and should not
be quoted. My own probe is clean here by construction: it exports
`PEARDE_AS=engineer PEARDE_PORT=1` at `:63` and wraps every board command in
`R() { env -u XDG_CONFIG_HOME HOME="$NOOBS" "$@"; }` at `:65`. Verified directly
— under an empty `HOME`, `init` prints `Obsidian not installed here, so nothing
to register` and the file's md5 does not move. Not this PRD's footprint.

### Unchanged — `.pearde/` is gitignored whole, so no board file shows in `git status`

`.gitignore:16`. Confirmed with `git check-ignore -v`. Consequences for the
workflow are in `### Edits`.

### NEW — a stray registration of mine, and what it exposed

Proving the `HOME` isolation claim, I ran the **live** `resources/board/init.py
init` against a `mktemp -d` board without `PEARDE_PORT=1`. It reached the live
daemon on `127.0.0.1:8443` and registered `x` on a path that then ceased to
exist. Caught by `serve.py status`, removed with `serve.py forget x`, and
`serve.py status` now lists zero fixture boards. Recorded because the workflow's
row on this is right and I walked into it anyway: **the guard belongs on every
fixture invocation, not only on the harness's.** It also turned out to be the
evidence that condemned box 8's original check — the accident is exactly what
that box exists to catch, and the check read `ok` through it. An accident worth
writing down twice.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | ok — `prd.md`, `specs/spec01.md`, the pass-one `report.md`; `git status --short` recorded before the first command; footprint `resources/board/init.py` opened, present, already carrying the build |
| 2 | `capture-the-harness-baseline` | ok, and stronger than the atomic requires — genuine pre-build baseline in a clone at `f3aea95`, not inherited. Seven harnesses, `index.py check` and `doctor.sh` with exit codes. One gap in the atomic, below |
| 3 | `attempt-the-build` | nothing to build — the contract's build stood. Two vacuous checks found in this PRD's own probe; one repaired in place, one reverted after measurement |
| 4 | `re-run-the-harnesses` | ok — every count at or above baseline, none moved. Flips shown against the pre-build tree, not merely re-run |
| 5 | `write-the-specs` | n/a for this role; the specs existed. Boxes ticked as closed, box 8's stale path corrected, pass-one findings carried forward by name |

No back-edge was taken.

### Edits

Two replacements. Both are for `capture-the-harness-baseline` and
`attempt-the-build`; neither workflow file was edited by me.

**1. `capture-the-harness-baseline`, the resume/second-pass bullet.** Its recipe
is `git clone --no-hardlinks <repo> <scratch>/prefix`, then
`git -C <board> show HEAD:<path>` for a harness in a sibling worktree. On this
board **both halves fail**: `.pearde/` is gitignored, so the clone carries no
harness at all and `show HEAD:` returns nothing for any board file. The recipe
looks like it worked — the clone is there, it just has nothing to run. Replace
the sentence beginning "`git clone --no-hardlinks`" with:

> `git clone --no-hardlinks <repo> <scratch>/prefix` gives the tree at `HEAD`
> without the build. **Check first whether the board is tracked:
> `git check-ignore -v <board>`. A board that is a gitignored `.pearde/` inside
> the code repo is in no clone and in no `show HEAD:` — copy it in
> (`cp -R <repo>/.pearde/prds <scratch>/prefix/.pearde/prds`) before running
> anything, or the baseline is an empty directory reporting nothing.** For a
> harness that does live in a sibling worktree, write it in at the depth its
> `ROOT` resolves from (`git -C <board> show HEAD:<path>`), and run it there.

**2. `attempt-the-build`, the darwin `/private/var` row.** As written —
"an assertion on a path printed by a Python command fails on **darwin** with
`/private/var/…` against `/var/…`" — it reads as a general darwin path hazard,
and I applied it to a `grep -F` needle where it does not hold and briefly shipped
a false comment. `grep -F` substring-matches, and `/private/var/X` **contains**
`/var/X`, so a `mktemp`-spelled needle finds a realpath-spelled hit. Replace the
row's `do` cell with:

> compare against `$(cd "$D" && pwd -P)` — portable on both. **This is an
> equality hazard only. A `grep -F` needle is unaffected: `/private/var/X`
> contains `/var/X` as a substring, so a `mktemp`-spelled needle matches a
> realpath-spelled hit and "repairing" it adds a false claim to the file.
> Measure before you widen a needle on this ground.**

## Knowledge

Nothing was learned outside this tree; every fact above was measured in this
repo, so nothing was written back with `knowledge.py remember` and doctor's
`knowledge` row is untouched (`ok`, and the final `doctor` run is green).

## What is in the tree

`resources/board/init.py` — the analyst's build, unchanged by me.
`.pearde/prds/upgrade-leaves-the-memo-index-stale/probe/verify.sh` — one line
and its comment (`REG`). `.pearde/prds/upgrade-leaves-the-memo-index-stale/specs/spec01.md`
— nine boxes ticked and box 8's registry path corrected.

`git status --short` at the end lists `references/parts/doctor.md`,
`references/parts/workers.md`, `resources/board/brief.py`,
`resources/board/collect.py`, `resources/board/init.py` and `resources/doctor.sh`.
Only `resources/board/init.py` is this PRD's. Committing is not my act.
