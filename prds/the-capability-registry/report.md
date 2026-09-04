Verdict: DONE

Second pass on `probe-then-spec`: the specs existed and the build was already
in the lane (pass one's uncommitted work), so this pass re-measured rather
than re-built — every box in both specs run against the lane tree, quoted
below, plus the repo gate and a harness comparison against the lane's own
pre-edit `HEAD`. One thing did change in the tree: the two new files are now
**staged** in the lane, for the reason under *One edit this pass made*.

Lane: `/Users/feb/dev/infra/pearde/.pearde/.lanes/the-capability-registry`
(HEAD `1be5d2b`). `git status --short` at the end:

```
A  capabilities.md
 M references/files.md
A  resources/capabilities.py
 M resources/index.py
 M resources/pearde.py
```

## spec01 — `pearde capabilities` — all three boxes green

- [x] box 1 — count parity. `python3 resources/pearde.py capabilities` exits
      0; `n_rows=45 n_live=45` → `COUNT_OK` (45, not the spec prose's 44:
      `capabilities` is itself a `FORWARD` verb and gets its own row).
- [x] box 2 — a stub verb needs no hand edit. With `cmd_zzstub` added to
      `resources/board/orphans.py`'s `COMMANDS`, regeneration prints
      ``| `zzstub` | probe stub. | — | — | python |`` → `STUB_FOUND`; the
      stub was reverted and `git status` shows `orphans.py` clean.
- [x] box 3 — `check` convicts all three drifts and nothing else:
      clean file `clean_rc=0` and silent; hand-edited `scan` row →
      `rc=1 capabilities.md is stale — run 'pearde capabilities'`; an added
      `zzdead` row → ``rc=1 capabilities.md names `zzdead` — no such verb``;
      the `scan` row deleted → ``rc=1 `scan` is a verb with no row in
      capabilities.md``; regenerated → `restore_rc=0`.

## spec02 — doctor's `index` row convicts verb drift — all three boxes green

- [x] box 1 — dead verb: `pearde index check` prints
      ``capabilities.md names `zzdead` — no such verb`` → `DEAD_VERB_CAUGHT`.
- [x] box 2 — rowless live verb: it prints ``` `zzstub` is a verb with no row
      in capabilities.md ``` → `MISSING_ROW_CAUGHT`.
- [x] box 3 — no new noise. With the registry fresh, `pearde index check`
      prints exactly the three pre-existing manifest problems and nothing
      about verbs → `CLEAN_ADDS_NO_NOISE`:

```
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk
```

Those three were red **before the first edit** of either pass (identical
three lines from the lane's pre-edit `HEAD` clone, below). They are not this
PRD's.

## One edit this pass made: the two new files are staged

`index.py check()` imports `capabilities` at call time. Several board
harnesses build their fixture from `git ls-files`, which copies tracked
files only — so while `resources/capabilities.py` was untracked, every such
fixture got a modified `index.py` without the module beside it. Simulated
directly (`git ls-files -z | rsync --files-from=- …`, then
`python3 resources/index.py check`):

```
ModuleNotFoundError: No module named 'capabilities'
```

`git add resources/capabilities.py capabilities.md` closes it — the same
fixture then prints the three pre-existing manifest lines and nothing else.
Both files are tracked-by-contract anyway: `capabilities.md` sits at the repo
root beside `index.md` and `references/files.md` names both, so an untracked
pair would redden the manifest check the moment it landed. No content was
changed by this pass.

## Gate and harnesses

Baseline tree: `git clone --shared` of the lane → pre-edit `HEAD`, measured
with `PEARDE_ROOT=<clone>`; re-run on the lane with `PEARDE_ROOT=<lane>`.

| check | pre-edit clone | lane |
|---|---|---|
| `resources/index.py check` | 5 problems (3 manifest + 2 artifacts the doctor run wrote into the clone: `references/.state/parse-cache.json`, `references/wiki/pending/260903-fa5f.md`) | 3 problems, the same three |
| `resources/claims.py check` | 6 drifted names | the same 6, none naming `capabilities` |
| `doctor.sh` rows | index broken 3 · claims broken 6 · vault/origin/memos/knowledge/questions broken · rest ok | identical row set, identical verdicts; no new row, no row flipped |
| `the-gate-runs-the-harnesses` | 57 checks · 53 pass · 4 fail | 57 checks · 54 pass · 3 fail |
| `resources-are-organised-by-responsibility` | probe: 11 passed, 9 failed | identical |
| `the-round-runs-in-a-window-that-ends` | 26 checks · 25 pass · 1 fail | identical |
| `readme-in-three-rings` | 75 checks · 72 pass · 3 fail | identical |
| `an-example-board` | 37 checks · 36 pass · 1 fail · 1 skipped | identical |

The one moved count is **not claimed as a flip**: the FAIL that vanished is
`I the opt-out path costs under a second more than HEAD's doctor`, a wall-clock
assertion, on a machine that was running a dozen sibling `doctor --harnesses`
sweeps. The other difference inside that harness is `L index.py check is
silent — got: 5 · want: 0` against `got: 3 · want: 0` — red on both sides, and
the 5 is the clone's two runtime artifacts, not a behaviour this pass changed.

Harness set measured: the 5 board harnesses that both spell a footprint path
(`resources/index.py`, `resources/pearde.py`, `references/files.md`,
`capabilities`) **and** honour `PEARDE_ROOT`, out of the board's 98. Not the
full sweep — see the first Edit below. Two harnesses that spell a footprint
path ignore `PEARDE_ROOT` entirely
(`resources-are-organised-by-responsibility/every-file-sits-under-what-it-is-responsible-for`,
`every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense`);
every count from those is the orchestrator's checkout's, never the lane's,
so no claim is made about them.

Board state moved under this run — 223 PRDs at baseline, 226 at the re-run,
and the `statusline` row's dirty count changed both times. Sibling sessions,
not this pass.

## Findings (not fixed — outside scope)

- `resources/index.py check` reports three pre-existing manifest problems on
  this tree (`resources/common.py` with no row; `references/files.md` and
  `@@view` both naming `resources/board/hotreload-test.js`, not on disk).
  Present before the first edit of either pass.
- spec01's prose says "44 today, `add` through `workflow`". It is 45: the
  `capabilities` row the spec itself adds. The box asserts parity with
  `discover() + FORWARD`, which holds, so no box is wrong — only the prose.
- Six verbs (`add`, `answer`, `defer`, `release`, `set`, `unblock`, all in
  `resources/board/transitions.py`) have no docstring and so print `—` as
  their contract. Reported by pass one; still true, still the tool's own
  silence rather than a registry defect.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | done — PRD, both specs, `git status --short` in lane and checkout recorded before the first command. No `@`/`@@` in the body dangles. All five footprint paths exist in the lane; the lane row of the atomic's `Fails when` ("the `repo:` root is a worktree … the probe's uncommitted code is already there") did **not** apply: the lane already carried pass one's build, nothing had to be copied in from the checkout |
| 2 | capture-the-harness-baseline | done, narrowed — `git clone --shared` of the lane gave a real pre-edit tree (the atomic's row for "the earlier build is uncommitted in a lane and that pass published no counts"). The full `doctor.sh --harnesses` sweep was started against it and killed twice by the 10-minute tool window; the baseline was taken on the footprint-spelling subset instead. See Edit 1 |
| 3 | attempt-the-build | second pass — the atomic's first `Fails when` row applies: both specs' builds were already in the tree (`git status --short` and `git diff` per spec footprint), so no spec was entered to build. Only the staging edit above was made |
| 4 | re-run-the-harnesses | done — same set, same command lines, same `PEARDE_ROOT` discipline on both trees. No count dropped; the one that rose is timing noise and is not claimed |
| 5 | write-the-specs | second pass — no spec authored. Both specs' `Fails when` shapes were applied to the blocks that stand: every box run, every drift case convicted, and the two shapes the atomics do not list are filed as Edits below |

### Edits

**1 — `capture-the-harness-baseline` and `re-run-the-harnesses`: a board-wide
sweep that cannot finish because every sibling is running it too.** Both
atomics assume the recorded set can be re-run. On this board `doctor.sh
--harnesses` runs 98 harnesses at `HCAP=4`, several of which run `doctor`
themselves, and `pgrep -f 'doctor.sh --harnesses'` named 33 concurrent runs
from sibling sessions during this pass. Two full sweeps were killed at the
tool's window with the `harnesses` row still unprinted. Add to
`capture-the-harness-baseline`'s `## Fails when`:

| seen | means | do |
|------|-------|----|
| a full `doctor.sh --harnesses` sweep does not print its `harnesses` row inside the window, and `pgrep -f 'doctor.sh --harnesses'` names runs that are not yours | every live session on this board is sweeping the same 90+ harnesses, and each harness that runs `doctor` multiplies the load — the sweep is contending with itself, not hanging | do not wait for it. Baseline the subset that both spells a footprint path (`grep -l -E '<path>\|<path>' $(find <board>/prds -name verify.sh)`) and honours `PEARDE_ROOT`, run them one at a time on both trees, and say in the report which subset was measured and how many of the board's harnesses it is. A named subset measured on both trees is evidence; a full sweep that never finished is none |

**2 — `re-run-the-harnesses`: a module this pass added is invisible to every
fixture built from `git ls-files` until it is staged.** No row covers it, and
the failure does not look like a missing file — it is a `ModuleNotFoundError`
inside a gate the harness runs, which reads as the gate being broken. Add:

| seen | means | do |
|------|-------|----|
| a harness fixture crashes with `ModuleNotFoundError` naming a module this pass added, while the same command is green in the tree you built in | the harness builds its fixture from `git ls-files`, which copies tracked files only: your **modified** file that imports the new module is copied, the **untracked** new module beside it is not | `git add` the new file in the lane before the re-run — an untracked file in a footprint is invisible to every fixture in the set. Reproduce it in one line before and after: `git ls-files -z \| rsync -a --files-from=- --from0 . <scratch>/` then run the gate there |
