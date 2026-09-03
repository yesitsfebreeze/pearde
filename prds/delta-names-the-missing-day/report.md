Verdict: DONE

# delta names the missing day — implementer pass (pass two)

Route `probe-then-spec`, second pass. The analyst's pass one wrote
`specs/spec01.md` and left the build uncommitted in the lane; this pass
re-measured it, closed all seven acceptance boxes against run output, and
repaired one check in the verify block that could not fail.

## Spec status

`specs/spec01.md` — footprint `resources/scout/scout.sh`, complexity 15.
**7 of 7 boxes ticked**, each against output quoted below. The block runs
the way `collect` will (`bash -e -o pipefail`) and exits **0**.

## Workflow probe-then-spec

| # | step | result |
|---|------|--------|
| 1 | `read-the-contract` | pass. PRD, `specs/spec01.md`, pass one's `report.md` read. No `@`/`@@` dangled. `git status --short` recorded in **both** roots (the `Fails when` row for a board inside a code repo). |
| 2 | `capture-the-harness-baseline` | pass. One board harness reads the footprint's code; both repo gates baselined pre-edit and post-edit. |
| 3 | `attempt-the-build` | **not entered** — the `Fails when` row "steps 3 and 5 have nothing to do because the specs already exist and the build is already in the tree" applies. spec01's own footprint checked with `git status --short` and `git diff` before deciding: the build is present. This pass claims no build flip. |
| 4 | `re-run-the-harnesses` | pass. Every recorded count back at or above baseline. No red-to-green flip claimed. |
| 5 | `write-the-specs` | pass, as the second-pass form: the `Fails when` table applied to the block that already stands, no spec authored. One repair, below. |

### Edits

None. No atomic gave a wrong command, a stale path, an unfailable check or
an unlisted shape. Every row this pass leaned on — the second-pass row in
`attempt-the-build`, the two-root row in `read-the-contract`, the
"prove it can fail" row in `write-the-specs` — described the tree exactly.

## Baseline, before the first edit

Recorded in the lane (`.pearde/.lanes/delta-names-the-missing-day`,
HEAD `1be5d2b`, unchanged through the run; dirty list `M
resources/scout/scout.sh` and nothing else). The pre-edit tree was
recoverable — the build is uncommitted, so `git show HEAD:` gave a real
pre-edit `scout.sh`; the baseline is **measured, not inherited**.

The orchestrator's checkout was dirty in 15 tracked files plus `docs/` and
`resources/board/obsidian_register.py` — none of them my footprint, and the
list is longer than the brief's snapshot (siblings wrote during the run).

| harness / gate | pre-edit | post-edit | verdict |
|---|---|---|---|
| `prds/a-check-for-the-reading-list/probe/verify.sh <scout.sh>` — the one board harness that reads this footprint's code | 1 ok / 4 FAIL | 1 ok / 4 FAIL | byte-identical output. **Failing before the first edit** — a finding, not mine |
| `python3 resources/index.py check` | exit 1, 3 lines | exit 1, 3 lines | identical; no line names `resources/scout/scout.sh` |
| `bash resources/doctor.sh` | exit 1 | exit 1 | identical apart from the board census |

The four `FAIL` rows in the reading-list harness (`bare row named in
output`, `archived+active mix exits 0`, `archived row not marked`, and its
exit 2) stood **before the first edit** and are unrelated to `cmd_delta`.

Both gates were red before the first edit on lines outside this footprint:
`resources/common.py is on disk with no row in references/files.md`,
`references/files.md lists @resources/board/hotreload-test.js — not on
disk`, `@@view names @resources/board/hotreload-test.js — not on disk`, and
doctor's `memos.py retag` / missing-memo rows. Inherited, quoted, not fixed.

Doctor's only post-run difference is the live board's own census —
`▸pearde 110/179 61% · open 24 11%` became `110/180 · open 25 12%`,
`223 PRDs` became `224 PRDs`, `72 off` became `73 off`. A sibling filed a
PRD on the shared board mid-run. Same class as the `statusline` row: it is
nobody's finding, and no row moved off `ok`.

## The boxes, with output

- **Box 1** — 90 unbroken daily snapshots, `delta 7`:
  `delta 7 · diffed against 2026-08-27 (7 days back, nearest to 7)`, then
  `BUCKET  REPO  STARS  GAIN  RATE  WHAT`.
- **Box 2** — three snapshots, newest 20 days old, bare `delta`: prints
  exactly `gap: no snapshot within 2× of 7 days — run sweep first`, and
  `grep -c '^BUCKET'` on that output is `0`.
- **Box 3** — young tree of 7 daily snapshots, `delta 60`:
  `delta 60 · diffed against 2026-08-28 (6 days back, nearest to 60)` plus
  the table. `2026-08-28.tsv` is the oldest file on disk, so the line names
  the oldest snapshot and the tolerance refused nothing — the PRD's
  `Fails when` case holds.
- **Box 4** — `delta 0` on all three trees prints the table and neither a
  window line nor a `gap:` line. See the repair below: this box was ticked
  only after its check was made able to fail.
- **Box 5** — `NEW` still marks a repo absent from the chosen base. Added a
  repo appearing only in the last 3 days of the 90-snapshot fixture:
  `agents  new/comer  589  NEW  -  brand new` in the same table as
  `agents  foo/bar  1890  +70  3.8%  some repo`.
- **Box 6** — `bash -n resources/scout/scout.sh` exit `0`.
- **Box 7** — neither gate names `resources/scout/scout.sh`, pre or post
  (`grep -c 'scout/scout.sh'` is `0` in both outputs). Table above.

## Findings

Carried forward from pass one, plus this pass's own.

### 1 — box 4's check could not fail (repaired, this pass)

The block asserted `grep -q '^delta ·\|^gap:'`. The code prints
`delta 7 · diffed against …` — `^delta ·` is `delta`, space, `·`, which the
real line never matches. Proved rather than read: mutated `cmd_delta` to
leak `delta 0 · diffed against yesterday` on the `delta 0` path; the block
still printed `spec01: all checks passed` at exit `0`. Half the box was
dead.

Repaired to aim at the shape the code prints, and in the `if … then exit 1;
fi` form the atomic's table prescribes over `<test> && <action>`:

```sh
if printf '%s\n' "$out" | grep -qE '^delta [0-9]+ · diffed against|^gap:'; then echo "FAIL delta 0 leaked window logic"; exit 1; fi
```

Re-proved both ways: repaired block on the real tree exits `0`
(`spec01: all checks passed`); under the same mutant it exits `1`
(`FAIL delta 0 leaked window logic`). The footprint was restored from a
scratch backup outside the repo and is byte-identical to the pass-one build
(`cmp` clean, twice). The box's own prose is unchanged — only the needle
that reads it. No other box was touched.

### 2 — the verify block's `cd` cannot be run from a lane (reported, not fixed)

`## Verify and Proof` opens `cd /Users/feb/dev/infra/pearde` — the
orchestrator's checkout. Run as written from this lane it fails
immediately (`FAIL clean90 line`), because the checkout's `scout.sh` is
still at HEAD and the build lives only in the lane. This is **correct for
its runner**: `collect` merges the lane before it runs the block, so at
collect time that path holds the build. Deliberately not changed —
repointing it at the lane would break it exactly where it is meant to run.
Every run quoted above was made against the lane by substituting that one
line, and is labelled as the lane's tree.

### 3 — the reading-list harness is red on this tree (pre-existing)

`prds/a-check-for-the-reading-list/probe/verify.sh` is 1 ok / 4 FAIL at
exit 2 against both the pre-edit and post-edit `scout.sh`. It concerns
`scout.sh reading`, not `delta`. Outside this PRD's scope; reported, not
fixed.

### 4 — carried from pass one

No other file in the repo parses `scout.sh delta`'s stdout (grepped across
`*.sh`/`*.py`), so nothing downstream depends on the old unlabelled line
format. The two gate failures pass one named (`resources/common.py`,
`resources/board/hotreload-test.js`) are still standing and still unrelated.

## Health floor

The brief lists nothing under the floor. `resources/scout/scout.sh` is 183
lines after the edit, 151 before. Nothing in the footprint was left worse;
no refactor attempted.

## Knowledge

One fact learned outside this tree, written back: this box's `grep` is
**ugrep 7.8.4**, not BSD grep, so BRE alternation works here and the usual
darwin warning does not bite — the live hazard is a needle written from a
line's prose rather than its printed shape.
`sources/toolchain/260903-5e6d.md`.

No word in the contract was undefined.

## Merge note

The lane holds one uncommitted file, `resources/scout/scout.sh`, and the
checkout's copy of it is untouched at HEAD — no conflict, nothing for the
orchestrator to `checkout --` before the merge.
