Verdict: DONE

# a fork reaches the user when it is written — implementer pass

Second pass on `probe-then-spec`: `specs/spec01.md` already stood, written by
the analyst pass from an uncommitted build in the checkout. This pass
re-measured that build, found it **gone** — reverted out of the shared
checkout by a neighbouring session mid-run — restored it from the only
surviving copy, re-ran every check, ticked all five boxes and hardened the
spec's verify block so it can fail.

One spec, all five acceptance boxes `[x]`, each with quoted output.
`## Verify and Proof` run exactly as `collect` will
(`bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec01.md)"`)
→ **exit 0**.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | pass — `prd.md`, its `## Answers` (Q1 answered 14:56), `specs/spec01.md`, `probe/`, and the previous `report.md` read. `@references/drill.md`, `@references/parts/dispatch.md`, `@references/personas/engineer.md` all resolve. `git status --short` recorded before the first edit. The brief's `repo:` root, `.pearde/.lanes/…-a-fork-reaches-the-user-when-it-is-written`, **does not exist** — no such worktree and no such branch — so the work was done in the checkout, `/Users/feb/dev/infra/pearde`, where the one footprint path `resources/board/serve.py` lives. See `### Edits`. |
| 2 | capture-the-harness-baseline | pass — 92 board harnesses enumerated, 15 name `serve.py`, 14 of those honour `PEARDE_ROOT`. Baseline taken as two scratch trees that differ only by this PRD's three hunks (`base` / `mine`), so no neighbour's uncommitted work had to be reverted to measure. 8 harnesses run in both: every count identical. Detail under `## Harness baseline`. |
| 3 | attempt-the-build | pass, after a restore — the build was already in the tree at the start of this run (`git diff` at 17:33 showed all three hunks); at 17:37:29 a neighbouring session reverted `resources/board/serve.py` to `HEAD`, wiping this PRD's hunks and two other PRDs' with them. Re-applied by anchor from the diff this pass had already saved. `## The tree was wiped mid-run`. |
| 4 | re-run-the-harnesses | pass — 8 of the 15 `serve.py` harnesses identical `base` vs `mine`; 1 (`leaked-background-services-outlive-their-fixtures`) not comparable, it kills the process that runs the sweep; 6 left unmeasured under machine contention, named below. Repo gate: `index.py check` exit 0, `doctor.sh` unchanged in every row that could name this footprint. |
| 5 | write-the-specs | pass — second-pass form: no spec authored. `write-the-specs`'s `## Fails when` table applied to the block that already stood; two rows fired ("a block exits 0 while a line in it printed a failure", "the report path already holds a previous pass's report") and both were acted on. |

### Edits

Three shapes this route's atomics do not carry. Replacement rows, not applied
— the brief forbids editing the workflow files.

**1. `attempt-the-build` → `## Fails when`.** The existing row covers a clean
`git status` because *a sibling committed the tree*. It does not cover the
case that actually happened: a sibling **reverted** it. Its remedy ("if the
behaviour is present, the work stands") reads green on a wipe, because the
behaviour is not present and `git log` shows nothing — exactly the reading
that loses the work.

| seen | means | do |
|------|-------|----|
| the brief says the probe's code is uncommitted, `git status --short` is clean, and `git log -1 -- <footprint path>` names no commit carrying it | a sibling session ran `git checkout --`/`reset` on the shared checkout: the work was **discarded**, not committed, and every other PRD with hunks in that file lost them in the same stroke | do not rebuild from memory. Recover in this order: a diff this run saved to scratch, `git stash list` (`git stash show -p stash@{n} -- <path>`), a tree copy under the scratch directory, another session's lane. Re-apply **only your own hunks**, by anchor rather than by `git apply`, since the file has moved under them. Name in the report every neighbour's hunk that went with yours and the path to the diff that still holds them — you are the only copy |

**2. `capture-the-harness-baseline` → `## Fails when`.** A copy of the tree
made before the first edit is the thing that saved this run, and the atomic
only reaches for one as a fallback when the board's own history lacks a file.

| seen | means | do |
|------|-------|----|
| the footprint is a file several sessions have uncommitted hunks in | the pre-edit tree is on disk and nowhere else, and any session may revert it out from under you at any moment | before the first measurement, save `git diff -- <each footprint path>` **and** a tracked-file copy (`git ls-files -z \| rsync -a --files-from=- --from0 . <scratch>/base/`) into this run's own scratch subdirectory. Then build the baseline by stripping *your* hunks from that copy rather than by reverting the live file: neighbours' work stays measured, nothing on the shared checkout moves, and the copy is the recovery if the checkout is wiped |

**3. `capture-the-harness-baseline` → `## Fails when`.** A harness may be
hostile to the sweep that runs it.

| seen | means | do |
|------|-------|----|
| the sweep dies part-way with exit 143/144 and no failing check, on a machine with other sessions running | a harness in the set hunts stray background processes and kills them — `leaked-background-services-outlive-their-fixtures` does — and the runner driving the sweep is one of them | run that harness alone and by hand, never inside a loop or a background job, and record its count separately. A sweep it is inside cannot finish and its exit code is not a finding about the tree |

## The tree was wiped mid-run

At 17:33 `git diff -- resources/board/serve.py` showed 45 insertions in three
independent sets of hunks: this PRD's (`ask_digest`, `Board.ask_stamp`, the
`watch()` per-tick check), a sibling's (`SWEEP_S`, `Board.last_sweep`, the
`translib.tick_sweep` call in `watch()`), and a third's (`obsreg.read()`
replacing the inline `obsidian.json` parse in the vault lookup). At 17:37:29
the file's mtime moved and `git status --short -- resources/board/serve.py`
went **empty**: the file was back at `HEAD` (`d0a8da0`), all 45 lines gone. No
commit carries them (`git log -1 -- resources/board/serve.py` → `d0a8da0`),
and no stash holds them (`git stash show -p stash@{0..4} -- resources/board/
serve.py \| grep -c ask_digest` → `0 0 0 0 0`). The memo
`a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work.md`
is this exact shape, already on the board.

Recovered because this pass had saved `git diff` and a tracked-file tree copy
to scratch before touching anything. This PRD's three hunks were re-applied by
anchor and `py_compile` is clean.

**The other two PRDs' hunks are still lost, and this pass did not carry them
back** — they are outside this footprint's ownership and re-applying a
neighbour's work blind is worse than reporting it. The whole pre-wipe diff,
all three PRDs, survives at:

```
/private/tmp/claude-501/-Users-feb-dev-infra-pearde/1843477b-581c-4854-af0e-e7aad727b949/scratchpad/impl-fork-reaches/serve.full.diff
```

and a copy of the whole pre-wipe tracked tree at `…/impl-fork-reaches/base/`
(with only this PRD's hunks stripped). Scratch is session-scoped; whoever owns
`SWEEP_S` and `obsidian_register` should be told before it is cleaned.

## Manual /wait check

Acceptance box 5. A scratch board registered with the live daemon, its `seq`
read from `/status` (3), a plain `urllib` call parked on
`/wait?board=waitchk&seq=3&boot=0`, and `.state/ask.md` written two seconds
later:

```
start seq: 3
wrote .state/ask.md at t+2.0s
returned in 2.18s  200  b'{"seq": 4, "view": "...", "last_error": null}'
```

2.0s of deliberate delay plus `POLL_S` (1.0s) minus the settle already spent —
the user hears within about a second of the write, at no pass boundary. This
matches the Q1 answer exactly: the existing seq/wait primitive is the whole
mechanism, no hold timer and no batching.

## The control the wipe handed us

The run that measured the reverted tree is a free A/B nobody had to stage. On
the wiped tree (no `ask_digest`) the probe printed

```
ask.md written             3 -> 3   quiet
```

and after the restore, on the same probe and the same daemon,

```
ask.md written             3 -> 4   BUMP
```

with all three `control (nothing)` rows `quiet` in both. That is the proof the
new verify block's `grep -qE` can fail — measured, not argued.

## Harness baseline

Two scratch trees differing **only** by this PRD's three hunks: `base` (a
tracked-file copy of the pre-wipe working tree, this PRD's hunks stripped,
neighbours' kept) and `mine` (`base` plus this PRD's hunks). Both run with
`PEARDE_ROOT=` pointing at them, so the counts measure the tree under test and
not the checkout.

| harness | base | mine |
|---|---|---|
| `a-session-start-brings-the-board-up` | 46 checks · 40 pass · 6 fail · 0 skip | identical |
| `nothing-left-open/the-line-tells-the-truth` | verify: 85 checks · 81 pass · 4 fail | identical |
| `resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule` | probe: 23 passed, 0 failed | identical |
| `resources-are-organised-by-responsibility` | probe: 11 passed, 9 failed | identical |
| `seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green` | 41 checks · 7 pass · 34 fail · 0 skip | identical, and the FAIL lines diff empty |
| `the-board-runs-itself/collect-is-a-command` | 133 checks · 133 pass · 0 fail | identical |
| `the-board-runs-itself/one-command` | 53 passed, 1 failed | identical |
| `one-page-that-says-whats-up` | 31 checks · 26 pass · 5 fail | identical |

Every failing count above was failing **before the first edit** and is
identical on both trees; none is this pass's.

Not measured, and why:

- `leaked-background-services-outlive-their-fixtures` — kills the process
  running the sweep (twice: exit 143, then 144). `### Edits` row 3.
- `resources-are-organised-by-responsibility/every-file-sits-under-what-it-is-responsible-for`
  — the one of the 15 with no `PEARDE_ROOT`; it measures the checkout however
  it is invoked, so it cannot see the lane/scratch tree and no flip on it
  would be this build's.
- `the-board-runs-itself/{the-next-line-runs,init-asks-nothing,the-page-shows-the-round}`,
  `the-tool-keeps-its-word/collect-keeps-its-word`,
  `upgrade-leaves-the-memo-index-stale` — each starts a daemon and takes
  minutes under this machine's contention (five-plus concurrent sessions, two
  earlier sweeps killed part-way). All five only *launch* `serve.py`; none
  reads its contents, and the live daemon on 8443 has been running this exact
  code since the restore.

## Gate

- `python3 -m py_compile resources/board/serve.py` — clean.
- `python3 resources/index.py check` — **exit 0**, no output.
- `bash resources/doctor.sh` — exit 1, on five rows: `vault`, `origin`,
  `memos` (43 of 44 missing `tags:`), `knowledge`, `questions`. None names
  `serve.py`, `.state/ask.md`, or anything in this footprint; `view` reads
  `ok watching http://127.0.0.1:8443/board/pearde`. `memos`, `knowledge` and
  `questions` are the same three the analyst pass recorded before this
  session's first edit; `vault` and `origin` are the live board churn of the
  neighbouring vault session (`vault broken` names the dot-segment board path,
  a decision landed today by another PRD).
- `bash resources/doctor.sh --harnesses` (96 harnesses) not run — the same
  contention that killed two sweeps in this session. The eight-harness
  comparison above is this unit's evidence.

## Findings

Carried forward from the analyst pass, still true, still nobody's:

- **The Q1 answer's own board comment disagrees with the answer.** The
  `<!-- for the board: ask.py settled() and the one-pass-out rule in cmd_wait
  … -->` anchor names a `resources/board/ask.py` with `settled()`/`cmd_wait`
  that does not exist anywhere in the tree, and the answer text then chooses
  the existing `/wait` primitive instead. Prose on an answered question, out
  of this footprint — not fixed.
- **`probe/p2-wake.sh` and `probe/p3-answer.sh` test a superseded design.**
  Both call `$SKILL/resources/board/ask.py wait`/`list`, which does not
  exist, so both fail outright; they assume the dedicated ask/wait CLI with
  batching that the recorded answer says is not needed. Not rewritten — a
  future pass should retire or rescope them rather than build the CLI they
  assume.
- **The brief's `repo:` root does not exist.** No worktree and no branch named
  `lane/the-board-reclaims-dead-work-by-itself-a-fork-reaches-the-user-when-it-is-written`;
  `git worktree list` holds 20-odd lanes and not this one. Work was done in
  the checkout.

New this pass:

- **A neighbouring session discarded 45 uncommitted lines from three PRDs.**
  `## The tree was wiped mid-run`, with the recovery path for the two this
  pass did not restore. This is the single most expensive thing that happened
  in this run and it will happen again.
- **The three probe scripts defaulted `SKILL=` to the lane that was never
  cut**, so every run needed `SKILL=` passed in or ran against nothing. Fixed
  in all three: the default now walks up from the script's own directory to
  the checkout holding `resources/pearde.py`, the repo-root probe the rest of
  the tree uses. `p1-signal.sh` now runs bare and prints the same rows. Inside
  this PRD's own directory, one line each, no behaviour changed.
- **The spec's old verify block could not fail.** It ran the probe and took
  its exit, which is the exit of the `serve.py forget` on the probe's last
  line — green whatever the rows said. Replaced with a block that captures the
  output and asserts the `ask.md written … BUMP` row and all three `quiet`
  controls. `write-the-specs`'s `## Fails when` names this shape; it fired.

## Scores

complexity: 8
blast-radius: mid
workflow: probe-then-spec
