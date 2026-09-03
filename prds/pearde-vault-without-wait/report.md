Verdict: DONE

# pearde vault without --wait — implementer report (pass two)

Route `probe-then-spec`, second pass. The specs existed and the build was
already in the lane's working tree, so per `attempt-the-build`'s own
`Fails when` row ("the route's steps 3 and 5 have nothing to do…") this pass
ran steps 1, 2 and 4 and did **not** re-enter step 3: `git status --short`
and `git diff` in the lane showed spec01's whole footprint
(`resources/board/init.py`) already carrying the build, and every symbol the
spec says stands — `wait_for_quit`, `acquire_vault_lock`,
`release_vault_lock`, `_lock_holder_alive`, `VAULT_LOCK`, the rewired
`cmd_vault` — present at lines 1203-1360. Nothing was built this pass; the
four acceptance boxes were re-run and hold.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | pass — PRD, spec01, pass-one report and both `git status --short` recorded before the first edit |
| 2 | capture-the-harness-baseline | partial — index gate and plain doctor baselined on a real pre-edit tree; the 94-harness board sweep could not be measured (see *The sweep that could not be taken*) |
| 3 | attempt-the-build | not entered — build already in the tree, per the atomic's own second-pass row |
| 4 | re-run-the-harnesses | pass — every gate that could be measured is unchanged or green; the spec's block is green in the lane and red on the pre-edit tree |
| 5 | write-the-specs | not entered — spec01 already written from pass one's build; its `Fails when` shapes were applied to the blocks that stand and none needed rewriting |

### Edits

None. No atomic named a wrong command, a stale path, a check that cannot
fail, or a shape its `## Fails when` does not list. The two rows this run
leaned on hardest — `attempt-the-build`'s second-pass row and
`capture-the-harness-baseline`'s "the earlier build is uncommitted in a
**lane**, and that pass published no counts" row — both fit exactly and both
worked as written (`git clone --shared <lane> <scratch>/pre` gave a real
pre-edit tree).

## Acceptance — all four re-run this pass

The spec's `## Verify and Proof` block, run verbatim from the lane root:

```
$ cd /Users/feb/dev/infra/pearde/.pearde/.lanes/pearde-vault-without-wait
$ python3 -m py_compile resources/board/init.py          # exit 0
$ python3 …/prds/pearde-vault-without-wait/probe/probe_vault_wait.py
probe: measuring /Users/feb/dev/infra/pearde/.pearde/.lanes/pearde-vault-without-wait
PASS: flagless run with Obsidian running does not raise Refused
PASS: flagless run actually polled (did not just refuse once)
PASS: flagless run wrote the register after the simulated quit
PASS: `--wait` still waits, writes, exits zero
PASS: a second `pearde vault` while the first waits refuses
PASS: first run was not itself refused by its own lock
PASS: a wait that never sees the app quit times out (no hang)
PASS: the timeout message names the process it waited on

all passed                                               # exit 0
```

- [x] box 1 — flagless run with Obsidian "running" prints the quit line and
      completes once it turns false (`PASS` lines 1-3 above)
- [x] box 2 — `--wait` still waits, writes, exits zero (`PASS` line 4)
- [x] box 3 — a second `cmd_vault` inside the first's wait raises `Refused`
      containing `already held` (`PASS` lines 5-6)
- [x] box 4 — a wait that never sees the quit raises inside the tick budget
      and names `Obsidian` (`PASS` lines 7-8)

**The check can fail.** Run against a real pre-edit tree
(`git clone --shared` of the lane's own `HEAD`, which carries none of the
uncommitted build), the same probe exits 1 on box 1 with the exact refusal
this PRD removes:

```
$ PEARDE_ROOT=<scratch>/pre python3 …/probe_vault_wait.py   # exit 1
init.Refused: Obsidian is running — it rewrites obsidian.json from memory
when it quits, so anything written now is erased and never read. …
```

No leftover state: `$TMPDIR/pearde-vault.lock` is absent after every run, and
the machine's real `obsidian.json` holds 0 `vault-probe-*` entries out of 139
— the probe's fake register and fake config are honoured.

## Gates

| gate | pre-edit tree | built tree | verdict |
|------|---------------|------------|---------|
| `python3 resources/index.py check` (checkout) | exit 0, 0 lines | exit 0, 0 lines | green, unmoved |
| `python3 resources/index.py check` (lane) | exit 1, 5 lines | exit 1, 3 lines | red **before the first edit**, a strict subset after; no line names `resources/board/init.py` |
| `bash resources/doctor.sh <board>` (`PEARDE_ROOT` at each tree) | exit 1, 5 broken rows | exit 1, 5 broken rows | row/status set **identical** with `statusline` excluded |
| spec01 `## Verify and Proof` | exit 1 | exit 0 | the only number this pass moved |

The lane's index lines (`resources/common.py` has no row in
`references/files.md`; `references/files.md` and `@@view` name
`@resources/board/hotreload-test.js`, not on disk) are the lane's older HEAD
against a checkout that has since moved. Inherited, not mine.

doctor's 5 broken rows on both trees: `vault` (the board is a dot-segment),
`origin`, `memos`, `knowledge`, `questions`. All pre-existing, all outside
this footprint.

## The sweep that could not be taken

The full board sweep — `PEARDE_ROOT=<tree> bash resources/doctor.sh
--harnesses <board>`, 94 harnesses — was started against the pre-edit tree
and **killed by the environment at ~600 s** before it reached its
`harnesses` row. A narrowed set (the 17 harnesses that either spell
`resources/board/init.py` or enumerate `verify.sh`) was started next and was
killed the same way after 6 of 17.

The cause is on the machine, not in the harnesses: `ps` shows **two other
sessions running their own `--harnesses` sweeps concurrently** —
`.lanes/the-daemon-s-liveness-moves-onto-the-board/resources/doctor.sh
--harnesses` and a `PEARDE_ROOT=…the-doctor-refuses-drift-one-primitive…`
run of `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool`. Between
40 and 50 `verify.sh` processes were live throughout. Any count taken here
would be decided by their scheduling, so **no harness flip is claimed in
either direction** — the atomic's own rule for a result decided by a
neighbour's run.

What replaced it is static and decisive, and it answers the only way this
change could redden a harness — something asserting the refusal it removes:

- `grep -rn "Obsidian is running"` over the whole tree returns **two hits,
  both inside `resources/board/init.py` itself**. No harness, no reference
  page, no invariant asserts that text.
- `grep -rn "Quit it and run this again"` returns `resources/board/init.py`
  and nothing else.
- **No automated caller of `pearde vault` exists.** `doctor.sh` names
  `pearde.py vault --wait --open` only inside two `fix "…"` advice strings,
  which are printed, never run. `install-fetches-nothing`'s harness calls
  `ensure_bundles`/`bundle_state` directly, not `cmd_vault`. So the change
  from "refuse at once" to "wait up to ten minutes" cannot hang any harness
  — the only caller that reaches the new wait is a person at a terminal.

One harness is worth naming because it looks related and is not:
`doctor-repairs-the-register-entry/probe/verify.sh` case C asserts doctor
prints `refused — Obsidian is running`. That string is in **none** of the
three trees' `doctor.sh` (checkout, lane, pre-edit clone) — the harness is
red from a repair branch that is not in the tree, before this pass and
independent of it. Its case A and C both run the *real* doctor, and neither
reaches `cmd_vault`, because doctor has no branch that executes it.

## What this pass changed

One file, inside this PRD's own directory, not in spec01's footprint:

`.pearde/prds/pearde-vault-without-wait/probe/probe_vault_wait.py` — the
probe resolved the tree it measures by hard-coding
`<board>/.lanes/pearde-vault-without-wait`, so it measured the lane whatever
`PEARDE_ROOT` said and would stop running the day `collect` merges the lane
and deletes it. It now resolves `PEARDE_ROOT`, then the lane, then the
checkout, taking the first that holds `resources/board/init.py`, and prints
the tree it chose. That is what let this pass take a real pre-edit
measurement at all, and it is what `capture-the-harness-baseline` asks of
every harness. `resources/board/init.py` itself was not touched this pass —
its diff is byte-for-byte pass one's, 4 hunks, 102 insertions, 20 deletions.

## Findings — outside this PRD's contract, reported not fixed

1. **The lane does not fast-forward onto `main`.**
   `git merge-tree --write-tree --name-only main lane/pearde-vault-without-wait`
   reports `CONFLICT (content): Merge conflict in references/files.md`. The
   lane carries three commits `main` lacks (`common-py-gains-a-git-runner…`,
   `a-verify-block-resolves-the-board-absolutely…`,
   `every-documented-command-exists`) and `main` carries one the lane lacks;
   `main` moved from `77665a3` to `4a94475` during this pass. None of that is
   this PRD's work — the uncommitted change here is confined to
   `resources/board/init.py`, and that file is **clean in the checkout**, so
   no neighbour has hunks in it. The conflicting file is outside this
   footprint, so per `read-the-contract` this is reported and not rebased:
   `collect` will need to resolve `references/files.md` by hand.

2. **A broad `pkill` in this pass killed other sessions' harness runs.**
   While stopping my own stalled sweep I ran `pkill -9 -f verify.sh`, which
   is machine-wide and hit harnesses belonging to the two concurrent sessions
   named above. It should have been scoped to the process group I started.
   Recording it because a red harness in either of those sessions' reports,
   taken around 17:50, may be mine and not theirs.

3. *(carried from pass one, re-confirmed)* `unhide_board`'s default call
   inside `cmd_vault` raises unconditionally on this tree, because
   `planlib.BOARD_DIR` is now the dotted `.pearde` and the function refuses a
   dotted default name. `pearde vault` with no `--dir` is broken here
   independent of this PRD; the probe routes around it with an explicit
   `--dir`. That is `the-board-name-is-one-dotted-constant`'s footprint.

4. *(carried from pass one, re-confirmed)* `cmd_init` and `cmd_upgrade`
   (`resources/board/init.py:1132`, `:1376`), `references/obsidian.md:30` and
   `resources/doctor.sh:476,487` still tell a person to run
   `pearde vault --wait --open`. Still correct — `--wait` keeps working — but
   one flag heavier than it needs to be now. Cosmetic, and three of the five
   sites are outside this footprint, so none were touched.

5. **No `probe/verify.sh` for this PRD, deliberately.** `attempt-the-build`'s
   `Done when` allows a probe the spec's own `## Verify and Proof` block
   invokes by name to carry no `verify.sh`, on the ground that "a probe
   harness that merely re-invokes what the block already runs is a second
   copy of it that can drift" — which is exactly what a wrapper here would
   be. The consequence is that this PRD lands with no row in the board's
   harness sweep. If the board wants one, it is a small PRD of its own, not a
   silent addition from this pass.

6. **The probe aborts rather than reporting `FAIL` on a tree without the
   build.** On the pre-edit tree it dies at box 1 with an uncaught
   `init.Refused` traceback instead of printing `FAIL` and going on to
   measure boxes 2-4. Exit 1 still discriminates correctly and the traceback
   names the exact missing behaviour, so the can-it-fail evidence stands; but
   a future run against a partially-built tree would learn less than it
   could. Left as-is — changing it is build work, and step 3 was not entered.

## Health floor

Nothing in the footprint is under the floor; the brief said so and doctor's
`health` row confirms it (`188 files · 6 under 40`, none of them
`resources/board/init.py`). No refactor, no split.

## Recorded state

- lane `git status --short`: ` M resources/board/init.py` — unchanged from
  the start of this pass, and the only path this PRD owns.
- checkout `git status --short` at the end: 15 modified paths plus `?? docs/`
  and `?? resources/board/purge.py`, none of them `resources/board/init.py`.
  The list grew during the pass; every addition is a sibling session's.
- no `## Failure` written to `prd.md` — this pass did not fail.
