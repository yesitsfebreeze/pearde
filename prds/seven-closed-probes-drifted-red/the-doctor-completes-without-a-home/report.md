# report — the-doctor-completes-without-a-home · implementer · as engineer

Verdict: **DONE** — spec01, 8/8 boxes ticked against quoted output. Box 3 was
falsified by a skeptic and is closed here on the case that broke it; box 5's
manufactured pass is replaced by an honest `skip`; boxes 1, 4, 6, 7 and 8 are
reworded to match what they actually prove. Every tick stands on a check seen
red by mutation this run.

This file replaces pass three's first report. Its `## Findings` are carried
forward by name — all nine — and its two `### Edits` are carried forward
unchanged; both had already landed in the workflow files I was handed and are
not re-proposed. Findings 10 and 11 are new.

## What was falsified, and what closes it

Pass three's first attempt resolved the home through
`python3 -c 'import os,pwd;print(pwd.getpwuid(os.getuid()).pw_dir)'`. A
skeptic showed that on the same fixture board and the same machine, with no
`python3` on `PATH`:

```
with HOME=/Users/feb  rc=1: vault broken  … is not in Obsidian's vault register
HOME scrubbed         rc=1: vault ok      … this shell exports no HOME and its uid
                                            resolves to no home directory
```

Reproduced here before the first edit, on a fixture board with a curated thin
PATH holding no `python3`:

```
thin PATH, with HOME  rc=1: vault broken  /tmp/pearde-repro.Bydw2e/repo/.pearde/.obsidian
                                          is not in Obsidian's vault register …
thin PATH, scrubbed   rc=1: vault ok      … this shell exports no HOME and its uid
                                            resolves to no home directory …
```

The uid resolves fine; `python3` was simply absent. The arm was reworded, not
removed: it still asserted something it cannot check and still converted a true
`broken` into `ok`, which is verbatim the criticism this PRD levels at pass
one. And it is not exotic — `env -i`, launchd and containers are precisely the
thin-PATH environments this row exists for, and on macOS `/usr/bin/python3` is
a stub that exits non-zero without the Command Line Tools.

Four things close it.

**1 — the home is resolved in-shell first, with no subprocess.**
`resources/doctor.sh`:

```sh
  OBSHOME="${HOME:-}"
  [ -z "$OBSHOME" ] && OBSHOME=$(unset HOME; echo ~)
  # bash leaves `~` literal when it cannot resolve one; that is not a home
  [ "$OBSHOME" = "~" ] && OBSHOME=""
  if [ -z "$OBSHOME" ]; then
    OBSHOME=$(python3 -c 'import os,pwd;print(pwd.getpwuid(os.getuid()).pw_dir)' 2>/dev/null || true)
  fi
```

`python3`/`getpwuid` is kept, demoted to a second fallback. The `unset HOME` is
load-bearing, verified in four shapes:

```
no PATH, no HOME:              [/Users/feb]
no PATH, HOME empty:           [/Users/feb]
without the unset, HOME empty: []          ← `~` follows HOME when HOME is set-but-empty
thin PATH:                     [/Users/feb]
```

**2 — the last-resort arm says only what it can check.** It no longer claims
the uid has no home — a claim it has no way to make, and the same defect one
layer down. It says the home could not be resolved.

**3 — it stops answering `ok` for a board it did not read.** It reports
`broken`, the shape doctor already uses for an interpreter it cannot run
(`index broken · no python3 to read it`, `guard broken · python3 not on PATH —
the guard cannot run`):

```sh
    row vault broken "$BOARD/.obsidian · this shell's home directory could not be resolved, so the vault register cannot be read — this row did not run"
    fix "export HOME=<your home> and re-run doctor — the register lives under it"
```

Because the builtin needs no PATH, that arm is now unreachable on any host
whose uid has a passwd entry. It is asserted at the source, and this report
says so rather than pretending it was driven.

**4 — the probe check this PRD was missing.** New check 10 runs the
same-verdict predicate with no usable `python3`, in three shapes: a `python3`
first on PATH that exits 1 (the macOS stub), a thin PATH holding the tools
doctor needs and no `python3` at all, and no PATH exported. Check 10 sits
beside the fixture that produces the failure — where the old check 9 asserted
the arm's *text* under a `python3` stub and never asserted the same-verdict
property there.

After the fix, all four thin/no-PATH shapes agree:

```
thin PATH, with HOME   rc=1: vault broken … is not in Obsidian's vault register
thin PATH, scrubbed    rc=1: vault broken … is not in Obsidian's vault register
HOME set-but-empty     rc=1: vault broken … is not in Obsidian's vault register
no PATH at all         rc=1: vault broken … ; rows=4; unbound=0
```

### Seen red — three mutations, each restored and proved

`resources/doctor.sh` is an uncommitted footprint file, so every mutation was
made after copying it to `<scratch>/nohome-pass3b/doctor.sh.bak` **outside the
repo**, mutated in place, run, `cp`ed back, and the restore proved with `cmp`.

**M1b — the whole tree the skeptic falsified** (builtin removed, arm back to
`ok`). This is the red the new check exists for:

```
FAIL  with no usable python3 the no-HOME run disagrees with the with-HOME run
      — [stub] with HOME: vault broken … is not in Obsidian's vault register
        // scrubbed: vault ok … exports no HOME and its uid resolves to no home directory
        [thin] with HOME: vault broken …
        // scrubbed: vault ok … exports no HOME and its uid resolves to no home directory
FAIL  the last-resort arm must report broken and claim only an unresolved home
      — got:     row vault ok "$BOARD/.obsidian · this shell exports no HOME and its uid resolves to no home directory, …"
12 checks · 10 pass · 2 fail · 0 skip            rc=1
RESTORED identical
```

The `nopath` leg does **not** fire under M1b, and the check says why: `env -i`
with no PATH makes bash supply its own default PATH, on which this machine's
`python3` works. That leg is about the scrubbed environment, not about a
missing interpreter, and it is labelled that way in the harness rather than
counted as evidence it is not.

**M1 — the resolution alone reverted** (arm kept honest): `12 checks · 11 pass
· 1 fail`, the same-verdict FAIL. **M2 — the arm alone reverted to `ok`**
(resolution kept): `12 checks · 11 pass · 1 fail`, the arm FAIL. Both
`RESTORED identical`. Each half of the fix is separately load-bearing.

## Box 5 — the stood-down check counted itself as a pass

The stand-down is the right engineering move and stays; the neighbour's
harness was not edited. What was wrong is that the stood-down check incremented
`pass`. In the exact mode box 5 measures, that check cannot fail, so the
`11 pass` the box quoted as proof was produced by the fix — and the stand-down
fires on *any* holder of 8477-8479, a bare unrelated socket included, so one
leaked listener (finding 7 — that harness never initialises `SRVPID3` and so
leaks on every early exit) would retire the check forever while it still read
green.

The probe now has a third bucket:

```sh
skp() { skip=$((skip+1)); echo "  skip  $1"; }
…
echo "$((pass+fail+skip)) checks · $pass pass · $fail fail · $skip skip"
```

Demonstrated in both stand-down modes on one unchanged tree:

```
PEARDE_HARNESSES=1        skip  the view-row harness is left to the sweep's own run of it …
                          12 checks · 11 pass · 0 fail · 1 skip     rc=0
bare socket holding 8477  skip  the view-row harness could not be run — 8477-8479 are held elsewhere (: 8477) …
                          12 checks · 11 pass · 0 fail · 1 skip
standalone                12 checks · 12 pass · 0 fail · 0 skip
```

Box 5's text now claims only that. The concurrent assertion it used to claim
survives in box 6 (that harness run alone, `6 checks · 6 pass · 0 fail`) and in
the sweep's own run of it, and the box says so instead of claiming more.

## The three smaller corrections

**Box 4's sentence was wider than what it proves.** Check 9's "no home at all"
leg only reached `XDG_CONFIG_HOME` because `python3` was forced to fail; with
the home resolved by a builtin there is no such shell on this host, and where a
real macOS register exists it outranks `XDG_CONFIG_HOME` — the committed
precedence. That removes a divergence rather than adding one, so it is not red.
The leg is gone, and the box now says `XDG_CONFIG_HOME` is honoured over a home
that holds no macOS register.

**Box 1's oracle was one character wide.** `(^|[^{A-Za-z_])\$HOME` does not
match `${HOME}`, which is equally fatal under `set -u`. Widened to
`(^|[^{A-Za-z_])\$HOME|\$\{HOME\}` in both the probe and the spec's block. No
such spelling exists today, so the box was true before; the widened oracle was
seen red by writing `OBSHOME="${HOME}"` in place — M3:

```
FAIL  doctor.sh still reads $HOME bare  — 357:  OBSHOME="${HOME}"
FAIL  doctor trips over an unset variable — … line 357: HOME: unbound variable
FAIL  doctor stopped before these rows: vault view plan
RESTORED identical
```

**The transcription that did not reproduce is fixed.** Pass three's first
report quoted `git diff --stat` as `references/obsidian.md +20 -7`,
`resources/doctor.sh +38 -3`. `git diff --numstat` said `20 0` and `32 2` and
nobody had touched either file. The real numbers, now, after this pass's edits:

```
38  0   references/obsidian.md
45  2   resources/doctor.sh
```

`references/obsidian.md` is still a pure insertion. `doctor.sh` is three hunks,
`@@ -332,0 +333,23 @@`, `@@ -334,2 +357,19 @@`, `@@ -343,0 +384,3 @@` — all
inside the vault block.

## What stands from the skeptic's audit — cited, not re-derived

- **Box 1 true.** `HOME`, `XDG_CONFIG_HOME`, `PEARDE_HARNESSES`, `PEARDE_PORT`
  are the only external names in `doctor.sh`, all guarded at first read.
- **Box 2 true**, and more strongly than the earlier report claimed: eleven
  environments the probe does not cover — bare `env -i` with no PATH, `python3`
  absent, `python3` returning junk, `HOME=/no/such/dir`, `HOME=/etc/hosts`,
  `HOME=/`, `HOME` with a space, `HOME=''`, `XDG_CONFIG_HOME=/no/such`,
  `XDG_CONFIG_HOME=''`. All fifteen rows every time; zero `unbound variable`.
- **Box 3's predicate is a real predicate**, its red genuine (rebuilt in a
  shadow root with the `getpwuid` block removed: exactly one check flipped, and
  it is check 5 itself), and it **generalises across fixtures** — registered
  `ok`/`ok`, no-Obsidian-config `ok`/`ok`, unregistered `broken`/`broken`, all
  three diverging under the mutation. The agreement is structural: both legs
  compute the same `OBSHOME` and read the same file. That objection is closed.
- **Box 6 verified**, `6 checks · 6 pass · 0 fail`.
- **The HOME × XDG_CONFIG_HOME sweep**, all sixteen combinations, 14 of 16
  identical, the 2 that differ both `HOME` empty/unset. Not re-run.
- **Tree honesty**: repo HEAD `e15dd0c` unmoved, `git log -1` on
  `resources/doctor.sh` still `e15dd0c`, `references/obsidian.md` a pure
  insertion, nothing written outside `resources/doctor.sh`,
  `references/obsidian.md` and this PRD's own folder. Re-checked at the end of
  this run and still true.

## Boxes

| # | box | evidence |
|---|-----|----------|
| 1 | no unguarded home expansion, oracle widened to the braced spelling | `guarded`; M3 red on `OBSHOME="${HOME}"`, restored `cmp` identical |
| 2 | vault and every row below it print, no `unbound variable` | probe checks 2-3; `rows=4; unbound=0` with no PATH at all |
| 3 | **same verdict with and without HOME, with no usable `python3`** | probe checks 5 and 10; M1b red quoted above, `12 checks · 10 pass · 2 fail`, restored |
| 4 | the register answers still separate | probe checks 6-9; the "no home at all" clause removed as unprovable |
| 5 | **the probe under a concurrent sweep, honestly counted** | `12 checks · 11 pass · 0 fail · 1 skip` in both stand-down modes; `12/12/0/0` standalone |
| 6 | the view-row harness alone | `6 checks · 6 pass · 0 fail`, exit 0 |
| 7 | doctor's rows unmoved by this unit | `diff` of the `ok`/`broken`/`off` rows before and after, `statusline` excluded: **identical**. The only non-`ok` rows are the neighbour's `index broken` and the opt-in `harnesses off` / `jstests off` |
| 8 | the harness census unmoved | `57 checks · 55 pass · 2 fail` before **and** after; both failures index-downstream |

Each was ticked as it closed, not in a batch.

## The neighbour's red — separated out, not repaired

A sibling session installed playwright at ~13:56, after this PRD was claimed.
`resources/board/node_modules/` is untracked, so:

```
python3 resources/index.py check    → 115 lines, exit 1
bash resources/doctor.sh .          → index broken · 115 problems
                                      "pearde: something is installed and not working"
the-gate-runs-the-harnesses         → 57 checks · 55 pass · 2 fail
```

All 115 name `resources/board/node_modules/…`, `package.json` or
`package-lock.json`:

```
index problems not naming the neighbour's drop: 0 · naming this footprint: 0
```

The gate's two failures are `FAIL A the fixture board is otherwise green — so
exit 1 later means this row — got: 1 · want: 0` and `FAIL L index.py check is
silent — got: 115 · want: 0`, both downstream of that one index row. **Not this
footprint, not repaired.** Boxes 7 and 8 are re-baselined against it and assert
what this unit is answerable for: doctor's rows identical before and after, and
no index problem naming `resources/doctor.sh` or `references/obsidian.md`.

## The block as `collect` will run it

```
BLOCK exit=0
```

`guarded` · `builtin-first` · `arm-broken` · probe `12 checks · 12 pass · 0
fail · 0 skip` · under a sweep `12 checks · 11 pass · 0 fail · 1 skip` ·
view-row `6/6` · `index problems not naming the neighbour's drop: 0 · naming
this footprint: 0` · `index is the only broken row` · `vault ok · registered
with Obsidian`.

Two assertions in the previous block **silently did not run** and were fixed:
`grep -vc … | grep -qx 0 && echo …` — `grep -c` exits 1 when the count is 0, so
under `pipefail` the pipeline failed and the `&&` never fired. Counts are now
captured into variables and tested with `[ … ]`. That is a check that could not
fail, inside the block that proves this unit; it is fixed, not carried.

No line in the block is a board-wide gate: `doctor .` and `index.py check` are
captured with `|| true` and grepped, and the greps assert only about this
footprint.

## Tree state — the baseline is INHERITED, and re-baselined against the neighbour

The footprint already carried three passes of build, so no pre-edit baseline
was takeable. Per `capture-the-harness-baseline`'s resume clause, the tree as
it stands is the measurement, recorded before this run's first edit:

```
probe   rc=0 :: 11 checks · 11 pass · 0 fail
viewrow rc=0 :: 6 checks · 6 pass · 0 fail
gate    rc=1 :: 57 checks · 55 pass · 2 fail      ← the neighbour's, before the first edit
index   rc=1, 115 lines                            ← the neighbour's, before the first edit
doctor  rc=1 :: "something is installed and not working" on index broken · 115 problems
```

After: probe `12 checks · 12 pass · 0 fail · 0 skip` (one check added
deliberately, and the summary gained a skip field), viewrow `6/6`, gate `55/57`
unmoved, index 115 unmoved, doctor's rows identical with `statusline` excluded.
Nothing this run moved a count on any file outside the footprint.

`HEAD` = `e15dd0c` at the first command and at the last; `git log -1 --
resources/doctor.sh` is the same commit. The repo's dirty list is unchanged
from the brief's: `references/drill.md`, `references/parts/doctor.md`,
`references/parts/view.md`, `references/templates/prd.md`,
`resources/board/edit.py`, `render.py`, `serve.py`, `view.css`, `viewtest.js`,
`resources/questions.py` — none mine — plus the three untracked playwright
paths. Mine are exactly `resources/doctor.sh`, `references/obsidian.md` and
this PRD's untracked `probe/`, `specs/`, `report.md` in the board worktree.

The full sweep, run once: `harnesses broken · 6 of 47 green · 39 unpinned · 75s
· 10 failed`. This probe is not among them. It was 11 failed on the previous
pass; `an-acceptance-box-that-cannot-fail-is-refused` is no longer listed. That
flip is not this footprint's — see finding 9.

No `?? prds/<slug>/` this run did not make; `serve.py status` names no `/tmp`
fixture board (`grep -c /tmp` → 0); `lsof -iTCP:8477-8479 -sTCP:LISTEN` is
empty after the run; no `resources/board/state/guard/` exists. All mutations
restored, each proved with `cmp`.

## Workflow probe-then-spec

| # | step | verdict |
|---|------|---------|
| 1 | `read-the-contract` | done — `prd.md`, `specs/spec01.md`, `probe/verify.sh` and the previous pass's report read; both roots' `git status --short` recorded before the first edit; both `footprint:` paths exist and were opened. No `@`/`@@` in the body dangles |
| 2 | `capture-the-harness-baseline` | done (inherited) — the resume clause applies: the footprint already carried three passes. The tree as it stands is the measurement, quoted above. The `index`/`gate`/`doctor` red was recorded **before the first edit** and named as the neighbour's playwright drop |
| 3 | `attempt-the-build` | done — built **in place in the footprint file** per clause 2 (a fallback order and a row's status have no meaning outside the function they live in). Fixtures under `mktemp -d`; every doctor call on scratch port 9147 with no listener; nothing at the repo root |
| 4 | `re-run-the-harnesses` | done — probe, view-row, gate, `doctor .`, `index.py check`, plus the full `--harnesses` sweep. No count dropped that this unit moved. The flip claimed is shown by mutating the file itself, not by `git show HEAD:` — HEAD's `doctor.sh` aborts before the row and cannot separate the defects |
| 5 | `write-the-specs` | done — spec01's "what already stands / what is left" rewritten for the corrective pass; boxes 1, 3, 4, 5, 6, 7, 8 reworded to match what they prove; the `## Verify and Proof` block re-aimed at the skip assertion and at separating the neighbour's index red, and two silently-dead assertions in it fixed. 8 boxes, 0 open |

No back-edge was taken.

### Edits

Both Edits proposed by the previous pass are **already applied** in the
workflow files I was handed — step 4's "a check backing an already-ticked box
in your own spec goes red on the change the contract asked for" row, and step
3's "your probe invokes another PRD's harness and its result is decided by that
harness's own defect" row. They are carried forward as landed and not
re-proposed. The workflow files were not touched this run.

No new Edit. The two shapes this pass hit — a check that stands down and counts
itself as a pass, and a box ticked on a predicate that never runs in the
environment the unit exists for — are both already covered by step 3's
stand-down row (which says *demonstrate* the box under the racing condition,
never assert it) and by step 5's "an implementer reports a box whose command
prints a different number than the box asserts" row. What the route did not
prevent was a worker reading those rows and still counting a stand-down as a
pass; that is a discipline failure, not a missing row, and a route edit would
not have caught it.

## Findings

Carried forward by name; re-checked where cheap.

1. **The parent PRD's sweep runner miscounts every harness.**
   `.pearde/prds/seven-closed-probes-drifted-red/probe/run-all.sh` uses
   `printf "" "$out"` where it means `printf '%s\n' "$out"`, twice. Every row
   reads `pass=0 fail=0` and every `FAIL` excerpt is empty; only the exit code
   carries information. The parent's file. Still stands — this run relied on
   exit codes throughout and never on its rows.
2. **`doctor` swallows a traceback into a false headline.** A transient
   `NameError: MACHINE_DIR` from `plan.py` surfaced as `vision broken — 5 names
   in vision.md resolve to no PRD`, with the traceback as detail lines. A
   checker that crashes and a checker that finds a fault are indistinguishable
   from the report. Still stands. (Memo on the board:
   `memos/a-crashing-checker-reads-as-a-failing-check.md`.)
3. **A harness four directories deep is easy to miscount.** This PRD's probe
   walks up to the directory holding `resources/doctor.sh` rather than counting
   `..`; existing probes hard-code the chain — the view-row harness's
   `cd "$(dirname "$0")/../../../.."` is one. Worth generalising.
4. **The view-row harness leaks job-control noise past its summary.** After
   `6 checks · 6 pass · 0 fail` it prints three `Terminated: 15` lines. Exit
   code 0 and the count honest, but a caller grepping the tail for a failure
   word sees them. Confirmed again this run in the `## Verify and Proof`
   output.
5. **The sibling commit `e15dd0c` touched `resources/doctor.sh`** while this
   PRD held uncommitted hunks in it. Nothing collided; the footprint is shared
   and the next writer should re-read before editing. Re-checked: HEAD is still
   `e15dd0c` and the hunks are intact.
6. **The view-row harness binds hard-coded ports 8477-8479 with no bind check**
   (`.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh`,
   lines 82, 97, 111). Two runs on one machine fight over the ports and the
   loser's fixture server never comes up, so its `view` rows read `broken` and
   `off`. It needs an ephemeral port (bind 0 and read back what the kernel
   gave) or a bind-or-fail with a clear message. Reproduced on the previous
   pass: `6 checks · 4 pass · 2 fail` from a second concurrent run. Route to
   that PRD; this probe stands down rather than racing it — and now records
   that stand-down as a `skip`.
7. **`SRVPID3` is never initialised in that harness.** Line 27 is
   `SRVPID=""; SRVPID2=""`; line 31 in `cleanup()` reads `[ -n "$SRVPID3" ]`.
   Under `set -u` (line 16) any exit before line 112 kills the trap at that
   line, so `rm -rf "$D"` is never reached **and the first two servers are
   never killed** — two listeners leak machine-wide, which makes finding 6
   permanent. Demonstrated: `bash: line 2: SRVPID3: unbound variable`. One-line
   fix, in that PRD: `SRVPID=""; SRVPID2=""; SRVPID3=""`. This finding is now
   also the reason box 5's stand-down must be a `skip`: one leaked listener
   would otherwise retire that check forever while it still counted as a pass.
8. **`doctor --harnesses` launches all 47 harnesses at once with no job cap**
   (`resources/doctor.sh:722`). Any harness pair sharing a port, a fixture path
   or a machine-wide resource is decided by scheduling. A `-P`-style cap, or a
   declared "serial" set, would make the sweep reproducible. In this unit's
   footprint file but not in its contract — a finding, not a hunk.
9. **The full sweep is 10 red of 47** (`6 green · 39 unpinned · 75s`), and this
   probe is not among them: `nothing-left-open/the-line-tells-the-truth` ·
   `one-page-that-says-whats-up` ·
   `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` ·
   `the-board-runs-itself/collect-is-a-command`, `/init-asks-nothing`,
   `/readme-in-three-rings` ·
   `the-collect-and-brief-harnesses-are-carried-across-the-layou` ·
   `the-gate-runs-the-harnesses` · `workflows-on-the-board/workflow-improve`
   and `/workflow-skill`. The previous pass recorded 11, including
   `an-acceptance-box-that-cannot-fail-is-refused` (case suite and
   differential), which is no longer listed — a neighbour's flip, not this
   footprint's. None of the 10 reads the vault row.

New this run:

10. **The neighbour's untracked playwright drop reddens the repo's own gates.**
    `resources/board/node_modules/`, `package.json` and `package-lock.json` are
    untracked, so `index.py check` prints 115 problems and exits 1, doctor ends
    `something is installed and not working` on `index broken · 115 problems`,
    and `the-gate-runs-the-harnesses` reads `57 checks · 55 pass · 2 fail` with
    both failures downstream of that one row. Landed at ~13:56, after this PRD
    was claimed. Every one of the 115 lines names those three paths. Not this
    footprint, not repaired. Either the drop is committed, or `node_modules/`
    is excluded from whatever `index.py check` walks.
11. **A stand-down that counts itself as a pass is manufactured evidence, and
    the board has now paid for it twice.** In the exact mode a check stands
    down, it cannot fail; a count taken there is produced by the stand-down.
    This unit's box 5 quoted such a count as proof. The generalisable rule is
    that a harness needs three buckets — pass, fail, skip — and that a box may
    never cite a count taken in the mode where its own check stood down. A memo
    exists on the board (`memos/a-check-decided-by-scheduling.md`); it covers
    the racing half but not the counting half.

## Knowledge

Nothing was learned outside this tree. Every fact here came from files in this
checkout or from commands run against it. Nothing to write back with
`knowledge.py remember`.

## Scores

complexity: 6 (unchanged — the corrective pass cost about what the build did)
blast-radius: mid
workflow: probe-then-spec
