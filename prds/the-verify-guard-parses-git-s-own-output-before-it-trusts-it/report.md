# report — the-verify-guard-parses-git-s-own-output-before-it-trusts-it

Verdict: DONE

worker: impl-verify-guard (implementer, pass three — pass two was the analyst
that specced from the build; the implementer before me died at an account
session limit with 0 of 16 boxes ticked and the lane untouched)
workflow: probe-then-spec

Boxes: **16/16** — spec01 8/8, spec02 8/8.
Footprint: `resources/board/collect.py`, built and uncommitted in
`pearde/.lanes/the-verify-guard-parses-git-s-own-output-before-it-trusts-it`
(`git status --short` there is one line, `M resources/board/collect.py`).

Both spec blocks were run the way `collect` runs them
(`bash -e -o pipefail`, the fence awked out) on the **merged** tree, not the
lane: a `git clone --shared` of the checkout at `8bbb4c1`, the checkout's 24
uncommitted paths applied on top, the lane's `collect.py` overlaid, `.pearde`
symlinked to the live board, run with `PEARDE_ROOT` at that merge. Both
exit **0**.

| block | exit | last line |
|---|---|---|
| `specs/spec01.md` | 0 | `46 passed, 0 failed` |
| `specs/spec02.md` | 0 | `ALL PASS` (24 unit cases) then `46 passed, 0 failed` |

## The regression this pass found and closed

The guard as recovered from `6ea9c20` broke a neighbouring PRD's harness.
`filing-refuses-a-file-it-does-not-hold` went **52 checks · 52 pass · 0 fail**
on the guard-less tree to **52 checks · 45 pass · 7 fail** with the guard in
it — sections D and I, both of which run `collect` from a subdirectory of the
checkout (`runat "$D/away"`). The failure:

    File ".../collect.py", line 149, in also_places
        cwd = os.path.abspath(a)
    FileNotFoundError: [Errno 2] No such file or directory

`_park` stashes the foreign dirt with `git stash push -u`, and git **removes**
a directory whose last untracked entry it took. `away/rider.md` was foreign,
so `away/` went — and `away/` was the process's own cwd. The pop makes the
path again as a new inode; the process still holds the deleted one, so
`os.getcwd()`, `os.path.abspath()` and every relative open raise for the rest
of the run. `collect --also <relative path>` resolves against the caller's
cwd, so this took out the whole call: a green verify block, a traceback,
nothing committed, the PRD left `claimed`.

Repaired in the footprint file, inside the guard, in the same `finally` that
puts the rest of the checkout back — `_reattach(here)`, with `here` captured
by `guarded_run` before `_park` runs. No design was reopened: nothing about
the ordering the contract froze moved.

Proven both ways, as a behavioural mutation and not a wired counter:

- with the fix — `filing-refuses-a-file-it-does-not-hold` back to
  `52 checks · 52 pass · 0 fail`, exit 0.
- without it — a copy of the same tree with the single line `_reattach(here)`
  stripped: `probe_unit.py` dies on the new case with
  `FileNotFoundError: [Errno 2]` at `assert os.getcwd() == real`.

The check that guards it is new in this PRD's own probe, so no spec asserts a
literal total that it breaks: `probe_unit.py`'s
`the caller's cwd survives the park that emptied it`. That is the one test
this pass added — probe_unit went 23 cases to 24, and every pre-existing case
is individually unchanged.

## Harnesses — baseline and re-run

Baseline taken on a second `git clone --shared` of the same checkout with the
same 24 uncommitted paths and **HEAD's** `collect.py` (the reverted,
guard-less one), so the comparison is exactly
`git show HEAD:resources/board/collect.py` against the lane's. Every one run
with `PEARDE_ROOT` at its own root.

| harness | baseline (no guard) | re-run (guard) | whose |
|---|---|---|---|
| `a-verify-block-must-not-destroy-the-checkout-it-runs-in` | 16 passed, 8 failed | **24 passed, 0 failed** | **this PRD's flip** — the predicate fails on HEAD's file and passes on the lane's; this PRD re-lands the guard `8bbb4c1` reverted |
| `filing-refuses-a-file-it-does-not-hold` | 52 · 52 pass · 0 fail | 52 · 52 pass · 0 fail | mine, regressed to 45/7 and closed above |
| `collect-stages-a-shared-file-whole` | exit 0 | exit 0 | unchanged |
| `collect-must-not-reset-the-checkout-it-did-not-write` | 31 · 31 pass · 0 fail | same | unchanged |
| `the-tool-keeps-its-word/collect-keeps-its-word` | 101 · 101 pass · 0 fail | same | unchanged |
| `the-board-runs-itself/collect-is-a-command` | 133 · 133 pass · 0 fail | same | unchanged |
| `the-board-runs-itself/hunks-land-where-they-came-from` | 47 · 47 pass · 0 fail | same | unchanged |
| `the-brief-names-the-verdict-line-collect-requires` | 13 ok · 2 FAIL | same | red before the first edit, not mine |
| `resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule` | 3 passed, 20 failed | same | red before the first edit, not mine |
| `nothing-left-open/the-line-tells-the-truth` | 85 · 44 pass · 41 fail | same | red before the first edit, not mine |

That is every board harness naming `resources/board/collect.py`, found by
grepping the footprint path across `find <board>/prds -name verify.sh`.

## The repo's own gate

`resources/index.py check`, `resources/memos.py check`, `resources/doctor.sh`
— run in both roots, identical output in both.

- `index.py check` exit 1, three lines, **before the first edit and after**:
  `references/skills/pearde-machine.md is on disk with no row in
  references/files.md`; `references/language.md references
  @references/personas/writer.md — not on disk`; `resources/board/edit.py
  references @questions.py — not on disk`. None names my footprint.
- `memos.py check` exit 0. The previous pass reported five memos carrying an
  undefined `tags:` key; that line is **gone** on my own baseline — a sibling
  closed it between the two passes.
- `doctor.sh` exit 1, `index`, `origin`, `health` and `knowledge` broken, all
  four red in both roots. The only rows that differ between the two runs are
  `statusline`'s dirty count (`*24` vs `*25` — my one file) and the
  `knowledge` row's list of notes behind the graph, which moved while I ran
  because other sessions were writing the live board. Neither is a finding.

## Contract coverage

Every line of `## Acceptance` in `prd.md` is closed and evidenced:

- `_dirty` reads `git status --porcelain -z --untracked-files=all` and a
  spaced path comes through like its unspaced twin — `probe_unit`
  `a path with a space is classified, parked, healed and unerased`.
- a foreign **untracked** file created inside the window survives, moved
  aside rather than cleaned — `probe_unit` `a peer's new file is moved aside,
  not deleted`, plus `verify.sh` F3 (survives here) against F4 (destroyed on
  pass one's collect, which claims `put back: other/peer-new.txt` while the
  file is gone). The `git clean -f -d` needle finds nothing in the healing.
- every git call in `_heal` has its returncode read (`_aside`, `_take_aside`,
  `_head_blob` all check), `put back:` names only `back`, and `failed` gets
  its own `NOT put back in <cwd> — restore by hand:` line — `probe_unit`
  "`put back:` names only what was actually put back" and "a restore that
  fails says so".
- a foreign **staged** entry is left alone, worktree and index both, and
  named on a `left staged in <cwd>` line — `probe_unit` `a peer's staged
  entry is not wiped`. There is no blanket `git reset -q HEAD --` left.
- `spec02`'s destructive-block claim is honest: `git reset --hard HEAD` on the
  laneless path is caught and the pre-block bytes restored and committed —
  `verify.sh` F1, against F2 where pass one's collect commits the revert
  silently.
- `_owned_files` handles a footprint **symlink**, dangling one included —
  `probe_unit` `a footprint symlink comes back, target and all` and
  `a dangling footprint symlink is snapshotted and restored`.
- the hardcoded `cd /Users/feb/dev/infra/pearde` is gone: both blocks hold
  zero `cd`.
- `probe/verify.sh` is green on the **merged** tree with `PEARDE_ROOT` at the
  merge, and red where it should be — the same harness with `PEARDE_ROOT` at
  a tree carrying HEAD's guard-less `collect.py` prints
  `29 passed, 17 failed` and exits **1**. That is the same pair of numbers the
  analyst pass published, so its baseline is inherited **and confirmed**, not
  assumed.

## Findings

### 1 — a line in spec01's own verify block cannot fail

The line is the `test -z "$(grep -n ...)" && echo "no line[3:] left"` one. It
printed nothing on every run of this pass and the block still exited 0. Two
separate reasons, either alone enough:

- `bash -e` does **not** abort on a failing `<test> && <action>`. Measured:
  `bash -e -c 'test -z "x" && echo yes; echo after'` prints `after` and exits
  0. So the line can never redden the block.
- the needle now matches the guard's own prose. `_dirty`'s docstring explains
  the bug it fixes and spells the slice at `collect.py:438`. The rule the line
  asserts is intact — no executable occurrence remains — but the check is
  measuring the explanation.

Not edited: the block exits 0, `collect` will run it unchanged, and
redefining a spec is not the implementer's act. What would assert the rule and
be able to fail is a check aimed at the content rather than the count — parse
`collect.py`, take `_dirty`'s source with its docstring removed, and exit 1
when the slice appears in what is left, written `if <test>; then exit 1; fi`
so `set -e` cannot be dodged.

`spec02`'s block carries the same un-failable shape twice (the `git clean`
needle and the `reset -q HEAD` one). Both happen to print today, so both are
green for the right reason — but neither could go red if it were not.

### 2 — the machine ran out of disk twice during this run, and a harness reads ENOSPC as a red check

`/System/Volumes/Data` had **141Mi** free when this pass started; every Bash
call failed with `ENOSPC` before it ran. The cause on this board's side:
`$TMPDIR` held **12,351** `tmp.*` directories, 3.1G, left by harness runs
whose `trap … EXIT` never fired because the session was killed. I removed only
those untouched for over two hours (10,767 of them) and freed **8.7Gi**;
nothing newer, and no lane, board or repo path was touched. It filled again
within the hour and I cleared the 45-minute-old set a second time. The volume
is at 419Gi of 460Gi from something outside this board.

The visible damage is a *false red*: mid-run, `spec01`'s block reported
`44 passed, 2 failed` with both failures reading
`fatal: could not open '.git/COMMIT_EDITMSG': No space left on device` and
`OSError: [Errno 28] No space left on device`. A worker who quoted that count
would have reported a regression that does not exist. The clean re-run after
freeing space is `46 passed, 0 failed`. Both numbers are in this report on
purpose.

Two things are owed to someone, neither of them mine to do here: a harness
that cleans its own `mktemp -d` after a kill (a `trap` does not survive
`SIGKILL`, so the sweep needs a reaper by age and prefix, the way `.lanes` has
one), and a `doctor` row for free disk — every harness on this board writes
fixtures, and none of them can say why they died.

### 3 — carried forward from the analyst pass, still open, still not mine

- The board gate is red in the lane on things this PRD does not touch:
  `index.py check`'s three lines above. `memos.py check`'s five `tags:` memos
  are **closed** since that report. `doctor.sh` reports `knowledge broken`
  (`graph.json` behind six notes), `origin broken` (one derived PRD with no
  `from:`) and `health broken` (two `health/files/` notes for paths no longer
  tracked, and the ranking stale against the graph).
- `resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh`
  is still untracked in the shared checkout. Harnesses copy from
  `git ls-files`, so it is invisible to a doctor run until someone stages it.
  I carried it into both scratch trees by hand so the two roots compare.

## Knowledge

`knowledge.py remember` — `sources/260902-c351.md`,
`git stash push -u removes a directory it empties, and takes the process cwd
with it`. That is the mechanism behind the regression above and it is git's,
not this repo's, so it belongs on the record rather than only in this report.
One source, so no `conclude` — the second source is owed.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass. `prd.md`, both specs and the previous pass's `report.md` read; `git status --short` recorded in **both** roots before the first edit — lane one line, checkout 23 modified and one untracked. Footprint `resources/board/collect.py` exists in both. |
| 2 | `capture-the-harness-baseline` | pass. Board harness set found by grep for the footprint path (11, one of them mine); the repo's own gate is `index.py check` + `memos.py check` + `doctor.sh` per `settings.md`. Baseline taken on a guard-less clone rather than inherited, and the analyst pass's published pair (`46 passed, 0 failed` green / `29 passed, 17 failed` red) reproduced exactly. |
| 3 | `attempt-the-build` | entered once, on the back-edge from 4. The change is an **edit to an existing footprint file**, not new code under `probe/`: `_reattach` has no meaning outside `guarded_run`'s `finally`. The new assertion went into this PRD's own `probe/probe_unit.py`. |
| 4 | `re-run-the-harnesses` | fail, then pass. First re-run: `filing-refuses-a-file-it-does-not-hold` 52 pass to 45. Back-edge to 3 (once, of the two allowed). Second re-run: every harness at or above its baseline, one flip claimed and shown against HEAD's file. |
| 5 | `write-the-specs` | **not entered** — the route's second pass. The specs were written by the analyst from this same build; this pass applied step 5's `Fails when` table to the blocks that already stand and reports what it found there as finding 1, rather than authoring anything. |

### Edits

Two failures the atomics caused, with replacement text. Neither workflow file
was touched by me.

**`write-the-specs`, `## Do` item 4 — the `<test> && <action>` claim is
backwards on bash.** It reads:

> And a bare `<test> && <action>` aborts when the test is false, which is its
> passing case whenever the test is looking for something that should not be
> there — write it `if <test>; then <action>; fi`.

Measured on bash 5 (`bash -e -c 'test -z "x" && echo yes; echo after'` prints
`after`, exit 0): `set -e` exempts every command in an `&&` list except the
last, and the list's own non-zero status does not abort either. So the shape
does not abort — it silently does nothing, which is the worse failure and the
opposite of what the sentence warns about. Replacement:

> And a bare `<test> && <action>` cannot fail: `set -e` exempts every command
> in an `&&` list but the last, so a false test aborts nothing, prints
> nothing, and leaves the block's exit to the next line. It is the same class
> as the `!` shape below — a check that reads green forever. Write it
> `if <test>; then <action>; fi`, or put the bare test last.

**`attempt-the-build` and `re-run-the-harnesses`, `## Fails when` — no row for
a full disk.** Every harness on this board builds fixtures under `mktemp -d`,
and an ENOSPC surfaces as an ordinary red check with a plausible message. Row
to add to both tables:

| seen | means | do |
|------|-------|----|
| a count drops and a failing line reads `No space left on device`, `[Errno 28]`, or `could not open '.git/…'` | the machine is out of disk, not the tree out of contract — every harness here writes fixtures under `mktemp -d`, and a killed run's `trap … EXIT` never fires, so the litter accumulates | `df -h` on the data volume before quoting any count. Free only `$TMPDIR/tmp.*` older than the longest run on the board — a fresh one is a live sibling's fixture — then re-run and quote the second number, naming both |
