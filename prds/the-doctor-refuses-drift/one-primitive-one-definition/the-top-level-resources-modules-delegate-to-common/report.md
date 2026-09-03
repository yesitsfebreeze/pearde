Verdict: DONE

# the-top-level-resources-modules-delegate-to-common — implementer report

Four specs built, 16 acceptance boxes ticked against commands run this
session. `git diff --stat` in the lane: 4 files, 39 insertions, 120
deletions. Probe: `PASS: health._git, questions.find_board,
questions.sections (0/226 prds diverge), workflows.find_board,
workflows.section (120 checks), knowledge.parse_frontmatter (1
known/618 wiki notes diverge)`. All four `## Verify and Proof` blocks
exit 0 under `bash -e -o pipefail`.

`guard.py` is named in the PRD title and carries none of the five
primitives — the analyst's pass established that and wrote no spec for
it. Nothing here widened into it.

## Workflow probe-then-spec

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | read-the-contract | passed | `prd.md` body is the title only; the specs are the contract. Footprint clean in the checkout, the four files dirty in the lane |
| 2 | capture-the-harness-baseline | passed | first baseline was taken in a `git clone --shared` of the lane under `/private/tmp` — every board-resolving harness read a different tree there. Re-taken **in the lane itself**, four files reverted; that is the baseline every number below compares against |
| 3 | attempt-the-build | passed | second pass on this route. The probe's uncommitted build was destroyed mid-run (`## Findings`), so all four specs were re-entered and built in place in the footprint files |
| 4 | re-run-the-harnesses | passed | 21 harnesses, same command line, same `PEARDE_ROOT=<lane>`. Every exit code identical to the baseline |
| 5 | write-the-specs | passed | second pass — no spec authored. The `Fails when` table applied to the four standing blocks; one block repaired (`## Spec repair`) |

### Edits

**capture-the-harness-baseline** — `## Done when`, third bullet
("Resuming a killed run…") and the `Fails when` row beginning "the
earlier build is uncommitted in a **lane**, and that pass published no
counts" — replacement text:

> `git clone --shared <lane> <scratch>/pre` recovers the pre-edit
> **files**, never a pre-edit **measurement**: a scratch clone has no
> board above it, so every harness and every module that resolves a
> board by walking up (`knowledge.py`, `questions.py`, `plan.py`,
> `doctor.sh`) reads a different tree there and answers about nothing.
> Measured on this board: the same 21-harness set scored
> `one-definition-of-the-board-not-two` at 7 fail in the scratch clone
> against 5 in the lane, and `a-lane-s-wiki-is-a-stub-…` at 3 against
> 2 — a four-fail difference that is entirely the missing board.
> Take the baseline **in the lane**: save the build to
> `<scratch>/<this run>/build.patch`, `git checkout -- <each footprint
> path>`, run the set, `git apply` it back, and `md5` every file
> against a checksum taken before the revert. Only where a neighbour
> has hunks in a file of yours is that window unsafe — `git diff -U0 --
> <path>` first.

**capture-the-harness-baseline** — `## Do`, step 2, the sentence
"Write them under a subdirectory named for this run — the scratch
directory is shared across sessions, and a bare `grep FAIL
<scratch>/*` sweeps another worker's outputs in with yours" —
replacement text:

> Write **everything this step writes** under a subdirectory named for
> this run — outputs, and the build patch above all. The scratch
> directory is shared across sessions: a bare `grep FAIL <scratch>/*`
> sweeps another worker's outputs in with yours, and a bare
> `<scratch>/build.patch` is overwritten by the next session that
> saves one. Measured on this board: a neighbouring session rewrote
> `<scratch>/build.patch` 2m23s after it was saved and before it was
> applied, and the revert it was insurance for became permanent.
> Verify the round trip, never assume it: `md5` the footprint files
> before the revert and diff the checksums after the restore.

## Specs

### spec01 — `health.py`'s git runner is a one-line call into `common.run_git`

- [x] `health.py` defines no `subprocess.run` of its own; `_git` is the
  one-line delegation. `grep -n subprocess resources/health.py` prints
  nothing — `import subprocess` removed with it.
- [x] `head_commit` / `commits_behind` return the same values as before
  the edit. Both readers run over the same repo, a bad commit id, the
  literal `"none"`, a real commit and a missing root; the two output
  files diff clean:
  `'1be5d2b' / None / None / 0 / None / ' M resources/health.py\n'`.
- [x] `python3 resources/health.py score <board>` runs to completion:
  `189 scored · 189 on the ranking · 74 skipped · 6 under 40 · graph
  4a94475`, exit 0.

Block exit 0.

### spec02 — `questions.py`'s board walk and section reader are one-line calls into `common.py`

- [x] No `board_scanned`/`board_in`/`board_above` and no line-scanning
  `## <name>` reader left; `find_board` and `sections` are the
  delegations the spec names. `Q_RE`, `A_RE` and `H2_RE` removed as
  unused.
- [x] `find_board` resolves the same board from the board itself, from
  the project holding it, and from `None` walking up from the cwd, and
  refuses the same way. Both refusals byte-identical to the pre-edit
  reader: `questions: no .pearde/ board at <tmpdir>` and `questions: no
  .pearde/ board found walking up from the cwd`, exit 1 each.
- [x] `check <board>` and `list <board>` print byte-identical output to
  the pre-edit implementation — diffed against the lane's own `HEAD`
  copy, both clean. `check` exit 1 on both sides on the board's three
  pre-existing `## Answers` with no `## Questions`; `list` 11 lines
  both sides in the lane, 13 both sides in the merged tree.

Block exit 0 after the repair below.

### spec03 — `workflows.py`'s board walk and section reader are one-line calls into `common.py`

- [x] No line-scanning `## <name>` reader and no `memos.find_board`
  wrapper left; both are the one-line delegations. `import memos`
  stays — `memos.retag_text` still called.
- [x] Same library state as before the edit. `workflows.py check
  <board>` prints nothing and exits 0 on both sides — the string the
  box quotes is doctor's row, and doctor reads `workflows   ok      7
  workflows · 23 atomics · the library checks out` on the built tree.
- [x] 120 `section(body, name)` checks for `Do`, `Done when`, `Use
  when` and `Steps` across the live library, same truth value each —
  `probe/verify.py`, `workflows.section (120 checks)`.
- [x] `workflows.py brief probe-then-spec <board>` prints the same
  page: 58766 bytes, diff clean against the pre-edit reader.

Block exit 0.

### spec04 — `knowledge.py`'s frontmatter reader delegates to `common.split_frontmatter`

- [x] No fence/key/list line-scanner left; `parse_frontmatter`
  delegates and keeps only the bracket-list re-read. `FM_RE` removed,
  `WIKILINK_RE` kept (5 call sites, all body-link extraction).
- [x] 618 wiki notes parse to the same `(meta, body)` as the frozen
  pre-delegation reader — `1 known/618 wiki notes diverge`, the one
  being `wiki/graphs/community-01-260831-2cdf.md`, which reads two more
  top-level keys, never fewer or wrong ones.
- [x] `knowledge.py query` behaves the same: `query: 104 hit(s), 50
  strong · 104 notes on record` and every hit line byte-identical to
  the same query run from the checkout's unmodified `knowledge.py`.
  Doctor's `knowledge` row reads `broken  the research layer does not
  check out` on both trees — the row's own pre-existing finding.

Block exit 0.

## Harnesses

21 harnesses read a footprint path or enumerate the board. All honour
`PEARDE_ROOT` (`grep -L PEARDE_ROOT` names none). Baseline taken in the
lane with the four files reverted to `HEAD` (1be5d2b), re-run in the
lane with the build in place, same order, same command line.

**21 of 21 exit codes identical** — 3 green, 18 red, every red red
before the first edit. `diff` of the two exit-code tables is empty.
`seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` outruns a
ten-minute window and was run on its own to the end: `35 checks · 30
pass · 5 fail`, exit 1, on both trees, and its 35 `ok`/`FAIL` lines
diff clean.

Every output difference between the two runs is the live board growing
under both — `103 → 104` wiki notes, `223 → 226` PRDs, `94 → 97`
harnesses — plus wall-clock. No `ok`/`FAIL` verdict moved.

Repo gate, both roots, before and after:

| gate | lane (pre) | lane (built) | checkout |
|---|---|---|---|
| `index.py check` | 3 lines, exit 1 | 3 lines, exit 1, diff clean | 0 lines, exit 0 |
| `doctor.sh` | exit 1 | exit 1, every row identical | — |

The lane's three `index.py check` lines (`resources/common.py is on
disk with no row in references/files.md`, and two naming
`@resources/board/hotreload-test.js`) are the lane's base commit, not
this build: identical on the reverted tree, and green in the checkout
because a sibling already fixed `references/files.md` there. Doctor
differs between the two runs only in the absolute path it echoes into
its own fix lines.

## Spec repair

`spec02.md`'s `## Verify and Proof` block ran `python3
resources/questions.py check .pearde` bare. That command exits 1 on the
board's three pre-existing question-pass problems, which this unit
neither made nor fixes, and under `bash -e` it killed the block —
`collect` would have refused the spec with `spec02 exit 1 — nothing
written` with every box green. Repaired to capture the status and read
the output:

```sh
out=$(python3 resources/questions.py check .pearde 2>&1) || true
printf '%s\n' "$out" | tail -3
```

The claim the box makes is unchanged, and is proved above by diffing
the command's output against the pre-edit implementation. No other spec
text was touched; no frontmatter was touched.

## Findings

Carried forward from the analyst's pass, unchanged and still true:

- **`resources/board/refuse.py`'s `_run` also runs `ps`, not only
  `git`** — not this PRD's footprint (`resources/board/*` is
  `the-lane-and-repo-modules-delegate-to-common`).
- **`health.py`'s `I3 health.py imports stdlib only` check was already
  red before this PRD touched anything.** Confirmed again this pass:
  `FAIL  I3 health.py imports stdlib only — got [3] want [0]`,
  identical on the reverted tree and the built one. Removing `import
  subprocess` did not move it — `subprocess` is on the check's
  whitelist. Not this PRD's fix to make.
- **`guard.py`'s board walk is a real, intentional duplicate of
  `common.py`'s internals**, kept because its failure shape differs
  (silent `None` where `common.board_scanned` refuses). Whether that
  stays a named exception or `common.py` grows a non-exiting variant is
  a call for whoever plans the next round on this doctor row.

New this pass:

- **A neighbouring session overwrote `<scratch>/build.patch` and the
  probe's uncommitted build was lost.** The scratch directory is shared
  across sessions on this machine — 125 entries, most from other runs.
  This pass saved the lane's build to a bare `<scratch>/build.patch`,
  reverted the four files to take an honest baseline, and 2m23s later
  another session wrote its own `build.patch` and `build-backup/` to
  the same paths. `git apply` then applied **that session's** hunks
  (`references/obsidian.md`, `resources/doctor.sh` — a `doctor --fix`
  vault repair) into this lane. Both were reverted with `git checkout
  --`; the neighbour's work is intact in its own tree, and this lane's
  `git status --short` names only the four footprint files. The build
  was re-made from the specs, which carry the replacement text for all
  four functions verbatim. The atomic edit above closes the hole.
- **The lane's base commit 1be5d2b is not an ancestor of `main`.** It
  is the tip of
  `lane/…-common-py-gains-a-git-runner-and-a-section-extractor`, this
  PRD's `needs:`, and it is where `common.run_git` and `common.section`
  live. Every one of these four delegations raises `AttributeError` on
  a tree without it — proved by running all four blocks in a merged
  tree built from `main` alone: four blocks, four `AttributeError:
  module 'common' has no attribute run_git/section`. The lane carries
  that commit, so landing this lane lands both; a rebase that drops it,
  or a collect of this PRD before its `needs:`, breaks all four modules
  at import time.
- **`main` moved to 4a94475 during this run**, and that commit touches
  `resources/workflows.py` — `brief(board, slug, inline=True)`, a hunk
  disjoint from this build's. `git apply` of this lane's diff onto a
  clone of 4a94475 succeeds cleanly; the merge needs no hand
  resolution.
- **The specs' `## Verify and Proof` blocks cannot run in the lane.**
  `lanes.create` gives the lane its own `.pearde/` holding `graphify/`
  and no `prds/`, so `python3 .pearde/prds/…/probe/verify.py` is a
  missing file there. `collect`'s `repo_of` returns the checkout for a
  PRD with no `repo:` key — which is this PRD — so the blocks do
  resolve at collect time. They were run here in that tree: `git clone
  --shared <checkout>`, the checkout's uncommitted diff applied, the
  `needs:` commit's `common.py` diff applied, this lane's diff applied,
  `ln -s <board> <tree>/.pearde`. A worker whose session ledger names a
  lane as its repo would get the lane instead, and every one of these
  blocks would fail on a missing path.

## Left

Nothing in the four footprint files. `resources/questions.py`'s `die`
helper became dead the moment its only callers — `board_scanned`,
`board_in` and `find_board`'s refusals — moved into `common.py`; it was
removed in the same edit, and nothing in the tree calls `qlib.die`. The
spec does not name that removal: it is four lines of dead refusal
helper inside the spec's own footprint, not a change to the contract.
