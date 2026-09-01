---
complexity: 6
footprint:
  - resources/doctor.sh
  - references/obsidian.md
---

# spec01 — the vault row's register read is guarded, so no row below it stops printing

`resources/doctor.sh` runs under `set -uo pipefail`. The vault row added by
c02546f read the home directory bare, so in a shell that holds none the read
did not fail the row — it ended the script, and every row below `vault`
(members, vision, origin, memos, workflows, knowledge, briefs, questions,
view, plan, harnesses, jstests) stopped printing. That is the environment the
committed view-row harness runs doctor in on purpose (`env -i`), which is why
it went red on all four of its live checks 42 minutes after it was written.

This unit guards the read, keeps the row's four real answers intact, and
leaves a probe that pins the whole envelope.

**What already stands** — the whole unit is in the tree, uncommitted, in
three passes:

- Pass one guarded the read. `resources/doctor.sh` resolves the register path
  into `OBSCFG` through `OBSHOME` and a `[ -n "${XDG_CONFIG_HOME:-}" ]` test,
  with a comment saying why, and a new `elif [ -z "$OBSCFG" ]` arm reports the
  row instead of ending the script. That stopped the abort, and boxes 1, 2, 4,
  6, 7 and 8 stand on it. macOS-first precedence is unchanged: the
  `Library/Application Support` file wins when it exists, then
  `XDG_CONFIG_HOME`, then `~/.config`.
- Pass three **resolved the home** rather than reporting its absence. A shell
  that exports no `HOME` still has one — the uid resolves to it in the passwd
  database, which is how doctor's own `plugins` row reads it in the same run.
  Pass one's arm therefore green-washed a true red: on an unregistered fixture
  board `doctor` read `vault broken` with `HOME` and `vault ok · this shell
  holds no home` (exit 0) with the variable unset, two answers about one home
  inside one report.
- Pass three's first attempt resolved that home through
  `python3 -c 'import os,pwd;print(pwd.getpwuid(os.getuid()).pw_dir)'`, and a
  skeptic falsified it: with no `python3` on `PATH` the same fixture board
  still read `vault broken` with `HOME` and `vault ok` scrubbed. The arm had
  been reworded, not removed, and it still converted a true `broken` into
  `ok` — verbatim the criticism this PRD levels at pass one. The environments
  this row exists for are exactly the thin-PATH ones, and on macOS
  `/usr/bin/python3` is a stub that exits non-zero without the Command Line
  Tools. The corrective pass therefore resolves the home **with shell
  builtins first and no subprocess** — `[ -z "$OBSHOME" ] && OBSHOME=$(unset
  HOME; echo ~)`, which bash answers out of the passwd database with no PATH
  and no interpreter. The `unset HOME` is load-bearing: `~` follows `HOME`
  when `HOME` is set but empty, one of the two cases that gets there.
  `python3`/`getpwuid` is demoted to a second fallback.
- The `elif [ -z "$OBSCFG" ]` arm now says only what it can check — that the
  home **could not be resolved** — and reports it `broken`, not `ok`: a row
  that could not perform its check has not passed it, which is the answer
  doctor already gives elsewhere for an interpreter it cannot run (`index
  broken · no python3 to read it`). Because the builtin needs no PATH, that
  arm is unreachable on any host whose uid has a passwd entry, so it is
  asserted at the source rather than driven.
- `references/obsidian.md`: the paragraph under the doctor's-vault-row line,
  saying the home is resolved, why the builtin must come first and `python3`
  second, why one answer per run matters, that precedence does not depend on
  how the home was found, and what the last arm may and may not claim.
- `probe/verify.sh` in this PRD: 12 checks, 12 pass, 0 fail, 0 skip, exit 0.
  It builds a board and four homes under `mktemp -d`, drives doctor through
  ten environments on a scratch port — including three with no usable
  `python3` — and runs the view-row harness unless a sweep or a port holder
  makes that impossible, in which case it records a **skip**, which is not
  counted as a pass.
- A source sweep of every uppercase expansion in `doctor.sh` found `HOME` was
  the only unguarded read of an external variable; `XDG_CONFIG_HOME` sits
  inside its own `-n` test, and every other name is assigned in the script.

**What is left** — nothing in the footprint. The view-row harness this probe
used to invoke unconditionally is another PRD's file and carries two defects
of its own (hard-coded ports 8477-8479 with no bind check, and an
uninitialised `SRVPID3` its `cleanup()` reads under `set -u`); they are
findings in the report, routed to that PRD, and this probe works around them
by standing down when a sweep is running it — and by reporting that
stand-down as a `skip` rather than as a pass, since in the stood-down mode
the check cannot fail. Nothing in `resources/board/` is touched by this unit.

## Acceptance

- [x] `resources/doctor.sh` holds no unguarded home expansion on any
      non-comment line — the guarded spelling and the `XDG_CONFIG_HOME` test
      are the only reads of either name. The oracle now catches `${HOME}` as
      well as `$HOME`: it is one brace away and equally fatal under `set -u`.
      No such spelling exists in the file, so the box was true before the
      widening; the widened oracle was seen red by writing
      `OBSHOME="${HOME}"` in place, which printed
      `FAIL doctor.sh still reads $HOME bare — 357:  OBSHOME="${HOME}"` and,
      two checks later, `doctor trips over an unset variable — line 357:
      HOME: unbound variable` and `doctor stopped before these rows: vault
      view plan`. Restored from a backup outside the repo, `cmp` identical.
- [x] Doctor run against a board in a shell with no home prints a `vault`
      row and every row below it (`view` and `plan` at minimum), and its
      output holds no `unbound variable` line.
- [x] With no `HOME` exported, the vault row reaches the **same verdict** as
      the with-home row on the same fixture board — same row text, same exit
      code — **and it does so with no usable `python3`**. Unticked twice: on
      pass two where the arm converted a true red to green, and again when a
      skeptic falsified pass three's first attempt, which resolved the home
      through `getpwuid` and so still read `vault broken` with `HOME` and
      `vault ok` scrubbed on a thin PATH. Closed by resolving the home with
      shell builtins first (`[ -z "$OBSHOME" ] && OBSHOME=$(unset HOME; echo
      ~)`), `python3` demoted to a second fallback.
      Two probe checks carry it: check 5 on a full PATH, and check 10, which
      runs the same predicate in three shapes with no usable interpreter — a
      `python3` stub that exits 1, a thin PATH holding no `python3` at all,
      and no PATH exported. Check 10 is the check this PRD was missing and it
      has been **seen red** on the tree the skeptic falsified: with the
      builtin removed and the arm restored to `ok`, it prints
      `FAIL with no usable python3 the no-HOME run disagrees with the
      with-HOME run — [stub] with HOME: vault broken … is not in Obsidian's
      vault register // scrubbed: vault ok … exports no HOME and its uid
      resolves to no home directory [thin] with HOME: vault broken … //
      scrubbed: vault ok …`, `12 checks · 10 pass · 2 fail · 0 skip`, exit 1.
      Restored from a backup outside the repo, `cmp` identical. On the tree as
      it stands all six legs read `vault broken … is not in Obsidian's vault
      register`, and check 5 reads exit 1 both.
- [x] The register answers still separate: a home whose register names the
      board reads `ok … registered with Obsidian`; a home with no Obsidian
      config reads `ok … Obsidian not installed here`; a home whose register
      names some other path reads `broken`; `XDG_CONFIG_HOME` is honoured
      over a home that holds no macOS register. The old fourth clause said
      `XDG_CONFIG_HOME` is honoured "with no home at all" — that leg reached
      XDG only because `python3` was forced to fail, and once the home
      resolves without an interpreter there is no such shell on a host whose
      uid has a passwd entry. Where a real macOS register exists it outranks
      `XDG_CONFIG_HOME`, which is the committed precedence: this removes a
      divergence rather than adding one. The box now says what it proves.
      Probe checks 6-9.
- [x] This PRD's probe exits 0 **when run concurrently with the board's own
      sweep**, and says honestly what it did not check there:
      `12 checks · 11 pass · 0 fail · 1 skip`. Unticked on pass two: the
      view-row harness this probe invoked as its last check binds hard-coded
      ports 8477-8479 with no bind check, and `doctor --harnesses`
      (doctor.sh:722, no job cap) launches every harness at once, so the probe
      was green or red by scheduling. Reproduced before the fix — both
      harnesses launched together gave the probe `10 checks · 9 pass · 1
      fail`, exit 1, on `view broken … not registered` and `view off` from a
      fixture server that never got its port. The stand-down closes it inside
      this footprint, without editing the neighbour's file.
      What the stand-down may **not** do is count itself as a pass. In the
      exact mode this box measures the check cannot fail, so a green count
      taken there is produced by the stand-down, not by the harness; and the
      stand-down fires on any holder of 8477-8479, including a bare unrelated
      socket, so one leaked listener from that harness's own uninitialised
      `SRVPID3` would retire the check forever while it still read as a pass.
      It is therefore reported as a `skip` and a skip is not counted as a
      pass. Demonstrated in both stand-down modes on the same tree:
      `PEARDE_HARNESSES=1` → `skip the view-row harness is left to the sweep's
      own run of it …`, `12 checks · 11 pass · 0 fail · 1 skip`, exit 0; with
      an unrelated Python socket holding 8477 → `skip the view-row harness
      could not be run — 8477-8479 are held elsewhere (: 8477) …`, the same
      count; standalone → `12 checks · 12 pass · 0 fail · 0 skip`.
      The concurrent assertion this box used to claim survives in box 6, which
      runs that harness alone, and in the sweep's own run of it — this probe
      is not among the sweep's failures. It is not claimed here.
- [x] The committed view-row harness, run alone, reports
      `6 checks · 6 pass · 0 fail` and exits 0. This is where the concurrent
      assertion box 5 used to claim actually lives.
- [x] `bash resources/doctor.sh .` prints the same rows before and after
      this unit's edits, and no row it prints names this footprint as a
      problem. **Re-baselined**: a sibling session installed playwright under
      `resources/board/node_modules/` after this PRD was claimed, so
      `python3 resources/index.py check` now prints 115 problems and exits 1,
      and doctor ends `pearde: something is installed and not working` on
      `index broken · 115 problems`. All 115 name
      `resources/board/node_modules/…`, `package.json` or `package-lock.json`
      — `grep -vc 'node_modules\|package.json\|package-lock.json'` over them
      is `0`, and `grep -c 'doctor.sh\|obsidian.md'` is `0`. That is the
      neighbour's untracked drop, not this footprint, and it is not repaired
      here. What this unit is answerable for is checked instead: `diff` of
      doctor's `ok|broken|off` rows before and after these edits, `statusline`
      excluded, is **identical**, and the only non-`ok` rows are `index
      broken` (the neighbour's) plus `harnesses off` and `jstests off`, which
      are opt-in.
- [x] `the-gate-runs-the-harnesses` reports the **same** count before and
      after this unit's edits — `57 checks · 55 pass · 2 fail` — and both
      failures are downstream of the neighbour's index row, not of this
      harness: `FAIL A the fixture board is otherwise green — so exit 1 later
      means this row — got: 1 · want: 0` and `FAIL L index.py check is silent
      — got: 115 · want: 0`. Its pass-two baseline of `57/57` is stale: the
      playwright drop landed between that run and this one. This PRD's
      harness ends on an exit-code-carrying check and moved nothing in that
      census.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# the guard itself: no bare home expansion on an executable line. `${HOME}`
# is caught as well as `$HOME` — one brace apart, equally fatal under `set -u`
BARE=$(grep -nE '(^|[^{A-Za-z_])\$HOME|\$\{HOME\}' resources/doctor.sh \
       | grep -vE '^[0-9]+:[[:space:]]*#' || true)
[ -z "$BARE" ] && echo "guarded" || { echo "UNGUARDED: $BARE"; false; }

# the home is resolved by a shell builtin BEFORE any subprocess, and the
# last-resort arm reports broken rather than ok
grep -qF 'OBSHOME=$(unset HOME; echo ~)' resources/doctor.sh && echo "builtin-first"
grep -A2 -F 'elif [ -z "$OBSCFG" ]; then' resources/doctor.sh \
  | grep -qE '^[[:space:]]*row vault broken .*could not be resolved' && echo "arm-broken"

# the whole envelope — ten environments, the register answers, the
# same-verdict predicate on a full PATH and again with no usable python3,
# the last-resort arm, and the view-row harness
bash .pearde/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh

# box 5: the probe as the sweep itself invokes it (doctor.sh:722 exports
# PEARDE_HARNESSES=1), racing the harness whose hard-coded ports 8477-8479
# used to decide this unit by scheduling. The stood-down check must read
# `skip`, and the skip must not be counted as a pass.
PEARDE_HARNESSES=1 bash .pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh \
  >/dev/null 2>&1 </dev/null &
sweep=$(PEARDE_HARNESSES=1 bash .pearde/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh </dev/null)
wait || true
printf '%s\n' "$sweep" | tail -3
printf '%s\n' "$sweep" | grep -q '^  skip  the view-row harness is left to the sweep' || \
  { echo "the stood-down check did not report a skip"; false; }
printf '%s\n' "$sweep" | grep -qE '^12 checks · 11 pass · 0 fail · 1 skip$' || \
  { echo "a skip is being counted as a pass"; false; }

# the harness the defect reddened, alone — where box 6's assertion lives
bash .pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh

# the neighbour's index red is separated out, not repaired: every one of the
# 115 problems names resources/board/node_modules, package.json or
# package-lock.json, and none names this footprint
IP=$(python3 resources/index.py check 2>&1 || true)
NOTNM=$(printf '%s\n' "$IP" | grep -vc 'node_modules\|package.json\|package-lock.json' || true)
MINE=$(printf '%s\n' "$IP" | grep -c 'resources/doctor.sh\|references/obsidian.md' || true)
echo "index problems not naming the neighbour's drop: $NOTNM · naming this footprint: $MINE"
[ "$NOTNM" = 0 ] && [ "$MINE" = 0 ] \
  || { echo "an index problem is not the neighbour's"; false; }

# doctor's rows are unmoved by this unit: the vault row is ok and the only
# broken row is the neighbour's index
DOUT=$(bash resources/doctor.sh . 2>&1 || true)
printf '%s\n' "$DOUT" | grep -E '^ +(vault|index) '
printf '%s\n' "$DOUT" | grep -E '^ +[a-z]+ +broken ' | grep -vq '^ *index ' \
  && { echo "a row other than index is broken"; false; } || echo "index is the only broken row"
```
