# report — the-fixtures-meet-the-tool · implementer · as engineer

Verdict: **DONE** — 18 of 18 acceptance boxes ticked, every one against output
quoted below. One box (`spec02` box 2) asserted a number the command it named
had never printed. I did not tick it and did not repair it on my own judgement;
I handed it back as a question, and the orchestrator authorised re-aiming it
off the count and onto the content. That re-aim is recorded in full below,
with who authorised it and the evidence that warranted it.

Pass one's build was continued, not restarted. Every one of the four fixture
edits was re-proved in **both** directions from `git show HEAD:` — no flip in
this report is claimed on a re-run alone.

## Per-spec box status

| spec | boxes | verdict |
|---|---|---|
| `spec01` — the "wrote nothing" harnesses stop counting the parse cache | 5/5 | closed |
| `spec02` — the transitions fixture pays the drill gate | 4/4 | closed; box 2 re-aimed, below |
| `spec03` — the last harness that only forwarded an exit code | 4/4 | closed |
| `spec04` — the README harness reads the round table at its new header | 5/5 | closed |

## The harnesses, baseline against final

The baseline is **inherited**: pass one's edits were already on disk when I
arrived, so no pre-edit tree existed to measure. Where a baseline column reads
"at HEAD" it is a number I took myself, by restoring that footprint file to its
committed text in place, running, and restoring — never a number re-derived
from the analyst's report.

| harness | at HEAD | final | rc |
|---|---|---|---|
| `an-unknown-flag-refuses` | 196 checks · 193 pass · **3 fail** | 196 · 196 · 0 | 0 |
| `the-tool-keeps-its-word/one-predicate-for-dispatchable` | 53 · 51 · **2 fail** | 53 · 53 · 0 | 0 |
| `the-board-runs-itself/specced-is-a-command` | **88/90** | 90/90 | 0 |
| `the-board-runs-itself/transitions-are-commands` | 74 · 64 · **10 fail** | 74 · 74 · 0 · 0 pending | 0 |
| `the-board-runs-itself/readme-in-three-rings` | 74 · 71 · **3 fail** | 74 · 72 · 2 fail | 1 |
| `scan-parses-…-by-mtime` | forwarded python's code | `parse-cache verify: pass` | 0 |
| `graph-probe-makes-harness-sweep-unaffordable` | untouched | 4 · 4 · 0 | 0 |
| `the-gate-runs-the-harnesses` | — | 57 · 57 · 0 | 0 |
| this PRD's own `probe/verify.sh` | — | 35 · 35 · 0 | 0 |

`readme-in-three-rings` is the one harness still red, at exactly the two rows
`spec04` predicted: `FAIL: H quickstart.sh exits 0` and `FAIL: H …and every
check passed`. Both are `init-seeds-a-board-doctor-calls-green`'s. Nothing
outside `H` fails — `grep -c '^FAIL: [^HG]'` reports 0.

Every footprint file was restored after its direction test and proved restored
with `cmp`: seven files, seven `IDENTICAL`.

## Each flip, shown against HEAD — not assumed (E5)

- **spec01 · the parse-cache filter.** Restoring `an-unknown-flag-refuses` to
  HEAD gives 3 failures; restoring `one-predicate-for-dispatchable` gives 2.
  The `clean()` / `git status --short | grep -v` hunks are the whole of the
  difference, and both files are in my footprint.
- **spec01 · `specced-is-a-command` is a correction to the spec's prose.** The
  spec calls that third edit "hardening — that harness was green before and
  after". It is not: at HEAD it reports **88/90**, so the `tree_sum`
  `-not -path './.state/*'` hunk closed a real red. The spec's *box* only
  demands `exits 0` and the grep reporting 1, both of which hold, so the box is
  honestly ticked — but the reasoning above it understates what the edit did.
  The false-red the spec anticipated ("its checksum would have gone false-red
  the first time a scan landed between two `tree_sum` calls") had already
  happened by the time I measured.
- **spec02 · the drill gate.** Restoring `fixture.py` alone to HEAD: 8
  failures. Restoring `fixture.py` *and* `verify.sh`: 10 — the number the box
  names. The gate's own words appear in the HEAD run. `resources/board/plan.py`
  is clean in `git status`; `resources/board/transitions.py` carries exactly one
  added line, a docstring from the memo session, and `git diff` over both files
  matches `drill|gate_claim|asking` **zero** times. The gate was not weakened.
- **spec03 · the exit-code tail.** Proved by mutation rather than by HEAD,
  because the box asks whether the tail *carries* a code: injecting
  `sys.exit(3)` into the harness's python makes the harness exit **1** — so the
  new tail both fails on a failure and normalises a non-1 code, which
  `exit $RC` could not do. Restored, `cmp` identical, re-run exits 0.
- **spec04 · the README anchor.** At HEAD the harness prints
  `FAIL: D seven rows in the README — got '0', want '7'`. The re-aimed anchor
  reads 7 and diffs empty against `loop.md`'s 7. `grep -c '| step | command'`
  on the harness reports 0; `grep -c '^| step | the orchestrator decides |'`
  reports 1 in both `README.md` and `references/parts/loop.md` — the fixture
  moved to meet the tree, and the tree was not moved to meet the fixture.

## Two green rows that are NOT mine (E5, in the other direction)

The brief told me `resources/index.py check` exits 0 while printing
`resources/invariants/every-artifact-lands-inside-the-board.sh is on disk with
no row in references/files.md`, and to record it as inherited. **By the time I
took my baseline it was already silent, rc 0**, and doctor's `index` row reads
`ok · 125 files · 32 keywords · every anchor resolves`. A sibling session landed
the row — `references/files.md` is modified in the outer repo and
`resources/invariants/` is untracked there, neither of them mine.

That closure, not any edit of mine, is what turned two rows green:

- `the-gate-runs-the-harnesses` is **57/57, rc 0**. The analyst recorded it red
  on rows A and L. I did not close those rows.
- `readme-in-three-rings` lost its `G index.py check is silent` row. Its HEAD
  run shows 3 failures (D + two H); the D row is mine, the G row is not.

`spec04`'s fourth box passes partly because of that sibling's landing, and I
would have ticked it either way — `grep -c '^FAIL: [^HG]'` reports 0 whether or
not G is present, since G is one of the two letters it excludes. Recorded so
nobody later reads the green `the-gate` row as this PRD's work.

## The one box that was re-aimed, and on whose authority

**Acceptance text moved in this run.** It was not my call and I did not make
it: I reported the box unticked, stated the fork, and the orchestrating session
(`a16d4abceb3b4e9f1`) authorised this specific change. A later reader must be
able to see that a box changed and on whose authority, so it is recorded here
rather than left to the diff.

`spec02` box 2 read:

> `grep -c '## Asked' .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/fixture.py` reports 1, and the section lists the four question titles the fixture's own PRDs carry

**The evidence that warranted the re-aim.** The command reports **2**, and
always has. Pass one's hunk added eleven lines: a three-line explanatory
comment whose first line contains the words `` `## Asked` `` in prose, and then
the `w(f"{board}/.state/round.md", ...)` call whose body opens with
`## Asked`. `grep -c` counts matching *lines*, so it counts the prose and the
content alike. The number was written without running the command.

The count was never the promise — it was a proxy for "the fixture writes one
`## Asked` section and that section holds the right four titles", and it had
stopped tracking the thing it proxied. Correcting `1` to `2` would have
re-hardened the same brittle proxy one notch along. I measured that directly:
appending one more comment containing the words to the fixture makes
`grep -c` report **3**, while the content check below is unmoved. On a board
where `## Asked` is a section name people discuss in prose, the proxy breaks
again on the next comment.

**The box now reads:**

> the `## Asked` section the fixture writes lists exactly the four question titles the fixture's own PRDs carry: the titles under `^## Asked` in `…/probe/fixture.py` diff empty against that same file's `^### Q<n>: ` titles, four of each

Its command is in `spec02`'s own `## Verify and Proof` and names a path from
`spec02`'s own `footprint:` — the fixture itself, both sides of the diff:

```sh
F=.pearde/prds/the-board-runs-itself/transitions-are-commands/probe/fixture.py
diff <(awk '/^## Asked$/{f=1;next} f&&/^- /{print substr($0,3)} f&&/^"""/{exit}' "$F" | sort) \
     <(grep -E '^### Q[0-9]+: ' "$F" | sed 's/^### Q[0-9]*: //' | sort) && echo "the four titles match"
```

It prints `the four titles match`. **It can still fail, proved both ways:**

- mutating one written title (`- Which size?` → `- Which SIZE?`) makes the diff
  non-empty and the check fail. Restored, `cmp` identical.
- appending a stray comment naming `## Asked` twice — the exact drift that
  broke the count, which would push `grep -c` to 3 — leaves the check
  matching. The `^## Asked$` anchor cannot see an indented comment, so the new
  check is immune to the failure mode that retired the old one.

The four titles are `Which colour?`, `Which size?`,
`Which name for the command?` and `Which way?`, and the fixture's own PRDs
carry exactly those at `### Q1: Which colour?` (117), `### Q2: Which size?`
(125), `### Q3: Which name for the command?` (133) and `### Q1: Which way?`
(304). Nothing else in `spec02` changed and no other box moved. The fixture
itself was not touched to make the box pass: `git diff` on `fixture.py` is
still pass one's single 11-line hunk.

## Findings — outside this contract, not fixed

1. **`.state/parse-cache.json` is ignored nowhere.** Confirmed by box:
   `grep -c 'parse-cache' resources/board/init.py .pearde/.gitignore` reports 0
   for both, while `.state/plan.json` — which the cache PRD called it "exactly
   like" — is named in both. This is the root the four fixture edits work
   around. Closing it means editing `resources/board/init.py`, which this
   contract forbids. Still nobody's PRD; the analyst's finding 3 stands
   unchanged.
2. **The `clean()` filter stays wider than the defect.** Filtering all of
   `.pearde/.state/` also hides `transitions.jsonl` and `history.jsonl` from
   those assertions. I verified coverage survives — `an-unknown-flag-refuses`
   pins the transition count separately with `rows()`, and
   `transitions-are-commands` keeps its `.history.jsonl byte-identical` check —
   so nothing went unwatched. Once finding 1 lands, the filter should narrow to
   the cache file alone. The analyst's finding 4, re-checked, not re-fixed.
3. **Three modified harnesses outside my footprint are inherited.**
   `prds/one-page-that-says-whats-up/probe/verify.sh`,
   `prds/the-board-runs-itself/brief-is-printed/probe/verify.sh` and
   `prds/the-graph-lands-inside-the-board/probe/verify.sh` were already ` M` in
   the board worktree at my baseline and are ` M` at the end, untouched by me.
4. **The workflow library moved under me and I did not touch it.**
   `workflows/probe-then-spec.md` and four of its atomics are ` M` in the board
   worktree — the E1–E6 edits from the neighbouring run. I read the library
   fresh via `workflows.py brief` as instructed and edited none of it.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass — `prd.md` and all four specs read; both roots' `git status --short` recorded before the first edit; the footprint's seven paths all on disk and all ` M` from pass one |
| 2 | `capture-the-harness-baseline` | pass — 46 harnesses via `find`; the three board-enumerating ones found with the `grep -l 'find.*verify\.sh'` rule; baseline recorded as **inherited** per the resume rule; `index.py check` and `doctor.sh` recorded with exit codes |
| 3 | `attempt-the-build` | pass, as a continuation — pass one's build stood; every edit is an **edit in place to an existing footprint file**, none staged under `probe/`, which is what the atomic's second bullet prescribes for a guard or a re-aim |
| 4 | `re-run-the-harnesses` | pass — nine harnesses re-run after the mutation tests; every count ≥ its baseline; two green rows attributed to a sibling rather than claimed |
| 5 | `write-the-specs` | n/a — the analyst wrote them; this run implements and ticks. One defect found in the set and re-aimed on the orchestrator's authority, above |

No back-edge was taken. Both mutation-and-restore rows the library added (the
`cp` to a scratch dir outside the repo, the `cmp` proof) were used exactly as
written and both worked; the spec-collision row (E6) fired once when my tick
helper's assert refused a bad anchor on `spec03`, which is the row working.

### Edits

Two shapes the atomics do not list. Neither cost me a back-edge, but both cost
a re-derivation that the text could have saved.

**Edit A — `capture-the-harness-baseline`, `## Fails when`.** The table has a
row for `index.py check` or `doctor` printing lines at step 4 that were *not*
there at step 2. It has no row for the mirror, which is what happened here: a
line the brief named as inherited had **disappeared** by baseline time, and the
harness rows that line was reddening were green before I started. A worker who
reads only the existing row will bank those rows as its own. Add:

| seen | means | do |
|------|-------|----|
| a failing line the brief names as inherited is **absent** when you take your own baseline, and harness rows it was reddening are green | a sibling closed it between the brief being composed and your first command; the brief's baseline is older than the tree | take your own baseline as the measurement and say in the report that the brief's line is gone and who closed it — `git status` in both roots names the file. Every harness row that line was reddening is that sibling's flip, not yours: the same rule as a count that went up |

**Edit B — `write-the-specs`, `## Fails when`.** The table has one row. The
defect that cost this run its only open box is that an acceptance box asserted
a count the command it names had never printed — a check that cannot *pass*,
the mirror of the box that cannot fail this board already refuses. Add:

| seen | means | do |
|------|-------|----|
| an implementer reports a box whose command prints a different number than the box asserts | the number was written from the build's memory rather than from running the command **as the box spells it** — a `grep -c` counts every matching line, and a word quoted in a comment beside the code counts too | run each box's own command line verbatim, from the repo root, and paste what it prints into the box. A count in a box is quoted output, never a recollection; when a literal appears in both prose and code, aim the box at the content instead of at the count |

## Scores

complexity: 17
blast-radius: mid
workflow: probe-then-spec
