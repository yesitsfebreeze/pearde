Verdict: DONE

# the-core-board-modules-delegate-to-common — implementer report

Second pass of `probe-then-spec` on this PRD. The analyst's build was already
in the lane and its one spec's whole footprint was dirty, so step 3 was not
entered to build: it was entered to re-measure, per `attempt-the-build`'s
`Fails when` row on the route's second pass. This pass took a real pre-edit
baseline rather than inheriting one, mutation-tested the probe, found one
delegation the probe could not discriminate, and closed it.

Lane: `.pearde/.lanes/the-doctor-refuses-drift-one-primitive-one-definition-the-core-board-modules-delegate-to-common`
(branch `lane/…`, HEAD `1be5d2b`). Work left uncommitted there on purpose —
`collect.land_lane` commits the lane's dirty footprint itself.

## Spec status

`specs/spec01.md` — all four acceptance boxes `[x]`, every one re-run this
pass. Boxes 2 and 4 rewritten to carry this pass's own evidence.

- Box 1 — the four one-line delegations stand. `git diff --stat` in the lane:
  `collect.py | 19 +++++++------------`, `edit.py | 12 ++++++++----`,
  `prdfile.py | 9 +++------`, `specs.py | 7 ++-----` — 20 insertions, 27
  deletions. `boards.py` untouched, as the spec contracts.
- Box 2 — `PEARDE_ROOT=<lane> python3 probe/probe_core_delegate.py`:
  `PASS: every delegated caller in the core board modules reproduced its
  pre-edit contract`. See *The probe could not fail on one of the four*.
- Box 3 — the sibling PRD's `probe/probe_common.py` against the edited tree:
  `PASS: every checked caller contract reproduced`.
- Box 4 — see *Measurements*.

`## Verify and Proof` ran clean, all three lines, `PEARDE_ROOT=<lane>`:
the two probes above plus `all four parse` from the `ast.parse` line.

## The probe could not fail on one of the four

Mutation-tested every delegation, one at a time in the lane, restoring the
file and re-diffing against the saved patch after each (`PATCH RESTORED
IDENTICAL` each time):

| mutation | probe |
|---|---|
| `specs.py` `chomp=True` → `chomp=False` | `FAIL: 2 mismatch(es)` |
| `prdfile.py` `ci=False` → `ci=True` | `FAIL: 2 mismatch(es)` |
| `collect.py` `ci=False` → `ci=True` | `FAIL: 1 mismatch(es)` |
| `edit.py` `common.atomic_write(path, text)` → `open(path,"w").write(text)` | **PASS** |

The fourth is the defect: `write_atomic`'s contract is the *atomicity*, and
the probe asserted only the bytes written and that no `.tmp` was left behind
— both of which a plain truncating write also gives. Delegating to something
that is not atomic at all would have gone unnoticed.

Closed it in this PRD's own probe (three assertions): the file's inode must
change across an overwrite (a write-beside-then-rename replaces it, a
truncate does not), the call must still return `None`, and the post-overwrite
contents must be the new text. The same mutation now gives
`FAIL: 1 mismatch(es) - write_atomic renames over rather than truncating in
place: got False want True`.

Also pinned the one place the delegation is *not* byte-identical to the code
it replaced. `specs.section_text`'s old body matched
`head.strip().lower().startswith(name)` — it lowered the heading and not
`name`, so an upper-case query could never match anything. The delegation
leaves `common.section`'s `ci` at its default `True`, which lowers both, so
`section_text(text, "Acceptance")` now returns the section where the old code
returned `""`. Nothing reaches it: all three call sites in `specs.py` pass a
lower-case literal (`"acceptance"`, `"verify"`, `"split"`). The probe now
asserts that — `(len(names), [n for n in names if n != n.lower()]) == (3, [])`
— so an upper-case call site added later turns it red, and asserts the
divergence itself so it is recorded rather than silent. Verified the check
discriminates: rewriting one call site to `"Split"` gives `(3, ['Split'])`.

A side effect worth knowing: with that assertion the probe now **fails on an
unbuilt tree** (`exit=1` against the orchestrator's checkout, whose four
files are still at `HEAD`), where before it passed everywhere by construction
— an equivalence probe comparing old-vs-old trivially agrees. This is safe
under `collect`, which merges the lane before it runs any verify block
(`collect.py:2208-2217`, "Merge first, then verify the MERGED tree"). A
worker running the block by hand in a lane must pass `PEARDE_ROOT=<lane>`;
the block does not spell it, and does not need to for `collect`.

## Measurements

Baseline taken for real, not inherited: the lane's four footprint files
restored from `HEAD` (`git checkout --`), the whole set run, then the saved
built copies restored and `git diff` re-diffed against the saved patch
(`PATCH RESTORED IDENTICAL`). Safe because no neighbour has hunks in those
four files — `git status --short` in the orchestrator's checkout lists none
of them.

**21 board harnesses** name a footprint path
(`find .pearde/prds -name verify.sh | xargs grep -l -E
'resources/board/(collect|edit|prdfile|specs|boards)\.py|resources/common\.py'`),
each run `PEARDE_ROOT=<lane>`. Exit codes, pre-edit / built / final:

```
0 1 0 0 0 0 0 0 0 1 1 0 1 1 1 0 0 1 0 0 0
```

identical in all three runs. The seven red were red **before the first edit**
— `an-acceptance-box-that-cannot-fail-is-refused`,
`collect-runs-the-invariants-and-red-refuses`, `the-line-tells-the-truth`,
`every-module-finds-its-siblings-by-one-rule`,
`the-board-name-is-one-dotted-constant`,
`a-lane-is-removed-when-its-prd-collects`, `specced-is-a-command`. None is
this unit's.

Output diffs pre-vs-built are all nondeterministic (`mktemp` paths, fixture
commit hashes) but **one**: `every-module-finds-its-siblings-by-one-rule`
prints `ok 32 modules open with the one rule` on the pre-edit tree and
`ok 33` on the built one. That rise is this spec's own — `edit.py` was the
one leaf module with no sibling imports and gained the standard
`pearde_path` two-liner. Same session, same `PEARDE_ROOT`, same harness
(mtime Sep 3 12:18, before this run), and its row is `ok` on both sides;
its `probe: 22 passed, 1 failed` tally is unchanged.

Repo gate, `PEARDE_ROOT=<lane>`:

- `python3 resources/index.py check` — 3 lines, byte-identical before and
  after: `resources/common.py is on disk with no row in references/files.md`,
  `references/files.md lists @resources/board/hotreload-test.js — not on
  disk`, `@@view names @resources/board/hotreload-test.js — not on disk`. All
  three pre-existing, none names a function this PRD touched.
- `bash resources/doctor.sh` — every one of the 21 row statuses identical
  before and after (`skills ok · plugins ok · index broken · claims broken ·
  statusline ok · guard ok · board ok · vault broken · vision ok · origin
  broken · memos broken · workflows ok · grammar ok · health ok · knowledge
  broken · briefs ok · questions broken · view ok · plan ok · harnesses off ·
  jstests off`). Two lines under `claims` shift by one — `collect.py:148` →
  `:149` and `prdfile.py:347` → `:348`, both pre-existing broken memo
  references whose citing line moved down one — and the `statusline` row's
  own workspace dirty-file count moves. Confirmed against a control copy of
  the tree with nothing reverted, so the tree path itself is not the
  difference.

## Findings

The analyst pass's four findings, carried forward unchanged — none was fixed,
none should be, and this report is now the board's only copy:

1. **`boards.py`'s `find_board` is a documented exception, not a gap.** It
   duplicates `common.find_board` but fails through its own `die(msg,
   code=2)`, uniformly across the file; `common.find_board` fails via
   `sys.exit(str)`, which is always exit code 1. A one-line delegation would
   flip every `boards.py` refusal from 2 to 1. Proven by subprocess in
   `probe_core_delegate.py`. Full reasoning in `specs/spec01.md`'s Findings.
2. **`boards.py` duplicates the whole board-resolution family** —
   `is_board_dir`, `board_link`, `named_boards`, `board_scanned`, `board_in`,
   `board_above` all exist in both files. The parent PRD's un-built
   `primitives` doctor row is contracted to watch five named primitives and
   none of these six is on that list, so they will not turn it red. Same
   class of duplication; the row-writer's to weigh, not a spec here.
3. **A corrected claim in the sibling PRD's own probe.** `probe_common.py`
   validates `prdfile._h2_sections` against `common.section(…, all=True,
   prefix=True, word=True)` with `ci` left at its default `True`;
   `_h2_sections`'s original regex has no `re.I` and is case-**sensitive**.
   The sibling's test never tried a case-mismatched query. This PRD's
   delegation passes `ci=False`, and `probe_core_delegate.py` carries the
   case-mismatch test that would have caught it — this pass's mutation run
   confirms it (`prdfile.py ci=False→True` → `FAIL: 2 mismatch(es)`, one of
   them `_h2_sections('questions') (wrong case) count: got 2 want 0`). The
   sibling PRD is already collected, so this stays recorded rather than
   reopened.
4. **`edit.py`'s `split_fm` and `section_span` are not duplicate primitives**
   despite the similar names — round-trip raw lines and body-offset positions
   against `common.py`'s parsed dict and body text. Confirmed in the probe.

New this pass:

5. **The probe's `write_atomic` check could not fail** — see above. Fixed
   inside this PRD's own probe directory.
6. **`specs.section_text`'s case handling widened** — see above. No live
   caller reaches the difference; now asserted rather than assumed.
7. **A neighbour landed mid-run.** The orchestrator's checkout moved
   `77665a3` → `4a94475` (`workers-compact-and-read-less`) while this pass
   ran, adding `resources/board/quiet.py` and `resources/spend.py` among
   others. Not this unit's, and invisible to every number here: every harness
   ran `PEARDE_ROOT=<lane>` and the lane is at its own `HEAD`. Named because
   `resources/spend.py` and `resources/board/quiet.py` are exactly the sort
   of new module that moves `every-module-finds-its-siblings-by-one-rule`'s
   count, and a later pass measuring the checkout will see 35, not 33, for a
   reason that is not this PRD's.

## Health floor

Nothing in the footprint was under the floor; the brief listed none. All four
files got smaller (27 lines deleted, 20 added).

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | ok — `prd.md`, `specs/spec01.md`, the previous pass's `report.md`, no `@`/`@@` in the body to resolve. Lane holds all four footprint paths and no board; the spec's verify block resolves against the checkout, so no symlink was needed. `git status --short` recorded in both roots before the first edit. |
| 2 | `capture-the-harness-baseline` | ok — 21 footprint harnesses + `index.py check` + `doctor.sh`, all `PEARDE_ROOT=<lane>`, whole outputs saved under a run-named scratch dir. Baseline **re-taken**, not inherited: the counts published by the previous pass were confirmed and then re-derived from a genuinely reverted tree. Seven harnesses red before the first edit. |
| 3 | `attempt-the-build` | entered to re-measure, not to build — the one spec's whole footprint was already dirty and its diff matches the spec's stated `--stat` exactly. Per this atomic's second-pass row, no flip is claimed for anything this pass did not build. The only edits this pass made are in the PRD's own `probe/` and `specs/`. |
| 4 | `re-run-the-harnesses` | ok — same set, same order, same `PEARDE_ROOT`, twice (built, and again after the probe edits). No count dropped; one rose and is attributed above against a same-session reverted-tree run. |
| 5 | `write-the-specs` | second pass: no spec authored. Applied this atomic's `Fails when` to the blocks that stand — boxes 2 and 4 rewritten to the numbers this pass measured, and the previous pass's `## Findings` carried forward by name into this report rather than overwritten. |

### Edits

One defect in an atomic, in `read-the-contract`'s `## Fails when`. Its last
row ends:

> symlink the live board in at `<lane>/pearde` (both `/pearde` and
> `/.pearde` are gitignored) **and read the next row before you baseline
> anything**

It is the last row of the table — there is no next row. The rows it means are
in the *next atomic*: `capture-the-harness-baseline`'s
`## Fails when` carries "the harness sweep is baselined with a board
symlinked into the lane, and re-run without it" and "every board harness
computes its own `ROOT` by walking up from `$0`, and the `repo:` root is a
lane". A reader who takes "the next row" literally finds nothing and
baselines with a symlinked board still in the tree, which is the exact
mistake the sentence exists to stop. Replacement text for that cell's tail:

> symlink the live board in at `<lane>/pearde` (both `/pearde` and
> `/.pearde` are gitignored) — **and before you baseline anything, read
> `capture-the-harness-baseline`'s `## Fails when` rows on a symlinked board
> inside the measured tree and on a harness that computes its own `ROOT`
> from `$0`**: a sweep baselined with the symlink present and re-run without
> it compares two different trees.

No other atomic gave a wrong command, a stale path, a check that cannot fail,
or a shape its `## Fails when` does not list.
