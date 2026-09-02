Verdict: DONE

# the surface parts are rewritten dense — implementer report

Second pass of `probe-then-spec` on this PRD. The specs already existed and the
build already stood in the lane, so steps 3 and 5 were not entered — the route's
own `Fails when` row covers exactly this case. Steps 1, 2 and 4 ran. All 22
acceptance boxes across the five specs are `[x]`, none open, and every one was
re-verified in this pass by running its spec's `## Verify and Proof` block the
way `collect` runs it.

An earlier implementer pass rewrote the five files and ticked the boxes but died
at an account session limit before writing this report. Nothing in the tree was
changed by this pass except the mutation-and-restore proofs below, each proved
back with `cmp`.

Lane: `pearde/.lanes/every-document-is-written-in-the-writer-s-prose-the-parts-reference-is-rewritten-dense-the-surface-parts-are-rewritten-dense`
Lane HEAD `fc75bcf`; checkout HEAD `8bbb4c1` (the lane is two commits behind).

## Boxes

| spec | file | boxes | block exit |
|---|---|---|---|
| spec01 | `references/parts/view.md` | 5 `[x]` | `0` |
| spec02 | `references/parts/doctor.md` | 4 `[x]` | `0` |
| spec03 | `references/parts/order.md` | 4 `[x]` | `0` |
| spec04 | `references/parts/progress.md` | 4 `[x]` | `0` |
| spec05 | `references/parts/statusline.md` | 5 `[x]` | `0` |

22 ticked, 0 open — `grep -c` for a ticked box per spec: 5, 4, 4, 4, 5.

Each block run from the lane root as `bash -e -o pipefail -c "$(awk …)"`:

```
spec01 exit=0 :: spec01: rows 46->46 fences 12->12 refs kept, check green
spec02 exit=0 :: spec02: part rows 14->14, 7 harness pins intact, check green
spec03 exit=0 :: spec03: two-line pin, vision pin intact; vision.py absent
spec04 exit=0 :: spec04: table rows 14->14, format string intact, check green
spec05 exit=0 :: spec05: 7 term rows, format block intact; growth bounded, refs kept
```

## The blocks can fail

Each of the five was mutated by appending one unbound-pronoun sentence to its
footprint file, its block re-run, and the file restored by `cp` from a scratch
dir outside the repo:

```
spec01 mutated exit=1 restore=same
spec02 mutated exit=1 restore=same
spec03 mutated exit=1 restore=same
spec04 mutated exit=1 restore=same
spec05 mutated exit=1 restore=same
```

`git status --short` in the lane after the proofs lists the same five modified
files and nothing else.

This mutation is behavioural, not a string swap: it aims at what
`resources/prose.py` **computes** — its unbound-pronoun verdict — rather than at
a literal a `grep` reads. The word-count, pin and table boxes in the same blocks
are the wired-counter kind, and this report says so rather than letting one tick
imply the other.

## Word counts

`python3 resources/prose.py stat HEAD`, run in the lane:

| file | words at `HEAD` → now | box |
|---|---|---|
| `references/parts/view.md` | 4380 → 4317 | at or below |
| `references/parts/doctor.md` | 1784 → 1775 | at or below |
| `references/parts/order.md` | 1069 → 1046 | at or below |
| `references/parts/progress.md` | 591 → 580 | at or below |
| `references/parts/statusline.md` | 430 → 437 | **+1.63%**, inside spec05's 2% |
| total | 8254 → 8155 | −1.2% |

`statusline.md` ending 7 words longer is the contract met, not missed. The
Density rule "a fact set is a table" turns its seven-term bullet run into a
table, and the row scaffolding costs more characters than the bullets. On a
430-word file that cost is not amortised by any prose cut. `spec05` bounds the
growth at 2% instead of hiding it, and no fact was cut to make the number look
better.

## No fact lost against `HEAD`

Checked beyond what the blocks assert, on all five files at once:

| check | result |
|---|---|
| table rows — first-column key of every row at `HEAD` still present | none lost, all five |
| fenced-block contents, sorted and whitespace-trimmed, vs `HEAD` | byte-identical, all five |
| every `@reference` at `HEAD` still present | none lost, all five |
| every backticked literal at `HEAD` still present | one apparent loss in `doctor.md`, explained below |

The one apparent loss is an artifact of naive backtick pairing, not a fact. At
`HEAD` the line ran `question`, or any parked state or `mode:` and the rewrite
spells the first as `state: question`, which shifts where the pairs open and
close. Both literals and the whole sentence survive at `doctor.md:74`:

```
4. a PRD parked on the user — `state: question`, or any parked state or `mode:`
```

## Harnesses

Four harnesses read a footprint path — the whole set, found by grepping all 69
`verify.sh` on the board for the five paths. All four honour `PEARDE_ROOT` (two
hits each, no `pwd -P`), so all four were run as `PEARDE_ROOT=<lane>`.

| harness | analyst's published count | this pass |
|---|---|---|
| `one-predicate-for-dispatchable` | 24 pass · 29 fail | 53 checks · **20 pass · 33 fail** |
| `vision-is-first-class` | 52 pass · 0 fail | 52/52 pass |
| `the-gate-runs-the-harnesses` | 27 pass · 30 fail | 57 checks · 27 pass · 30 fail |
| `one-page-that-says-whats-up` | 27 pass · 4 fail | 31 checks · 27 pass · 4 fail |

Three of the four confirm the inherited baseline exactly.
`one-predicate-for-dispatchable` moved four checks from pass to fail since the
analyst's run, and a control run settles that it is not this unit's: the five
footprint files were backed up outside the repo, restored to `HEAD` with
`git checkout --`, the harness re-run, and the rewrite copied back and proved
with `cmp`. The reverted tree prints the **identical** `53 checks · 20 pass ·
33 fail`. The build moves nothing in that harness in either direction.

No failing line in any of the four names a footprint file — grepped over all
four saved outputs. Fourteen `ok` lines do name them. The failures are
`resources/board/schedule.py` absent under the lane root (a sibling PRD is
cutting that module) and fixture boards that fail to build under `mktemp`; both
predate this build and neither is in this PRD's scope.

## The repo's own gate

`python3 resources/index.py check` in the lane: exit `1`, three lines, none in
this footprint — all three carried over from the analyst's pass.

```
references/skills/pearde-machine.md is on disk with no row in references/files.md
references/language.md references @references/personas/writer.md — not on disk
resources/board/edit.py references @questions.py — not on disk
```

`bash resources/doctor.sh` in the lane, with `PEARDE_GUARD_STATE` pointed at a
scratch path so the shared guard state was not written: exit `1`. Rows `broken`:
`index` (the three above), `origin`, `memos`, `workflows`, `health`,
`knowledge`. No doctor line names a footprint file — grepped for all five paths,
zero hits. The `view` row is still `ok · watching` after the run: nothing in
this pass touched the live service. The `statusline` row carries the tree's
dirty-file count (`*5`) and is nobody's finding.

## Findings

The analyst's findings are carried forward by name, none of them fixed — each is
outside this PRD's contract. The first is new to this pass.

### The lane's `view.md` rewrite would discard a neighbour's uncommitted hunk

**This one needs the orchestrator before `collect` runs.** The shared checkout
carries an uncommitted 12-line addition to `references/parts/view.md` — the
bullet beginning `**A write that half-landed is not a failure.**`, about `/edit`
reporting `wrote` before `error` — and it belongs to another PRD, not to this
one. The lane was cut off `HEAD` and never saw it, and this PRD rewrote
`view.md` whole. `grep -c` for that sentence: `1` in the checkout's copy, `0` in
the lane's. A whole-file merge of the lane over the checkout drops the
neighbour's work silently. The hunk must be re-applied onto the rewritten file
after the merge; it does not conflict with anything this unit changed, since the
rewrite is prose density and the hunk is new prose in a bullet list.

### `prose.py check` flags bound relative `that`

`resources/prose.py`'s docstring says it flags the vague-subject shape (`it is`,
`this means`) and "never the bound one". It also flags a relative pronoun
opening a restrictive clause — `a number that can only go up`, `a repo that is a
vault too`, `the only thing that would enforce a pin` — none of which is a vague
subject. Five correct sentences across these five files were reworded to satisfy
it. The rule the checker implements is "`that` followed by a linking verb",
which is not the rule `## Density` states.

### `prose.py check` reads a numbered list item as prose

`prose_lines` skips a line starting `#`, `|`, `-`, `*` or `>`, so a bullet is
structure and a numbered item is not. `## Density` names both forms as
structure — "a fact set is a table, a sequence a numbered list". A sequence
written in the prescribed numbered form is therefore held to the
sentence-length and waste-word rules that the same content in bullets escapes.
One hit in `doctor.md` came from exactly this.

### `prose.py check` is sensitive to where a line wraps

`prose_lines` works per physical line, so `it`, `this`, `that` or `there`
landing at the end of a wrapped line is read as "followed by nothing" and
flagged. Five of `view.md`'s twenty-nine hits were this, and each cleared by
re-wrapping with no word changed. The check partly measures wrap position rather
than prose.

### A multi-line `has()` needle asserts far less than it reads

`one-predicate-for-dispatchable/probe/verify.sh:170` pins a two-line string in
`order.md` through `has()`, which runs `grep -F -- "$needle"`. `grep -F` reads a
multi-line pattern as one pattern **per line**, so the check passes when
*either* half appears anywhere in the file. Measured: re-wrapping the clause —
one word across the break, no word changed — left the check at `ok` and the
harness totals unmoved. The assertion reads as "this block is present" and tests
"one of these lines is present". `spec03`'s box is deliberately stricter and
catches the re-wrap the harness waves through. Recorded as
`.pearde/wiki/sources/260902-376b.md`.

### `index.py check` reports three problems outside this footprint

Quoted above. All three predate this build and none names a footprint file.

### These five files were already dense

The contract's "cut twice" did not apply: the total came down 1.2%, not by half.
The prose here was already close to the rule, and the gain was structural —
bullet runs became tables, long paragraphs split at their seams, and every
heading now states its finding.

### The dispatch claim and the `--worker` name disagreed

On the analyst's pass, `pearde brief` was refused because this PRD carried
`claim: analyst-the-surface-parts` while the dispatch named
`--worker analyst-surface-parts`. Worth settling in the dispatcher so a worker
does not have to reconcile its own name. This pass, dispatched as
`impl-surface-parts` against `claim: impl-surface-parts`, was not refused.

### The machine ran out of disk mid-pass

Between two commands every write on the volume returned `ENOSPC` — the Bash
tool could not open its own output file, and neither a write to the scratchpad
nor a write to the board succeeded. It cleared on its own within a minute.
`df -h /` immediately after: `255Mi` free of 460Gi, 99% used. Every number in
this report was taken after it cleared. Not this PRD's to fix, but a board
running several worktrees and fixture boards under `mktemp -d` is close enough
to the wall that a worker can lose a pass to it — which is one plausible reading
of how the predecessor pass ended without a report.

## Workflow probe-then-spec

| step | atomic | result |
|---|---|---|
| 1 | `read-the-contract` | ok — `prd.md`, five specs, previous `report.md`, `git status --short` in lane and checkout recorded before the first command |
| 2 | `capture-the-harness-baseline` | ok — baseline inherited from the analyst's published counts and confirmed by re-run; the one disagreement settled by a control run |
| 3 | `attempt-the-build` | **not entered** — second pass, the specs exist and the build stands; the step's own `Fails when` row contracts this |
| 4 | `re-run-the-harnesses` | ok — four harnesses, `index.py check`, `doctor.sh`, all quoted against baseline |
| 5 | `write-the-specs` | **not entered** — same row; the five specs were written by the analyst's pass |

### Edits

None. Every command in the route ran as written, every path resolved, and no
`Fails when` row was met that the atomic does not already list. The two rows
that fired — step 3's "the route's steps 3 and 5 have nothing to do" and step
5's "the report path already holds a previous pass's report" — both behaved
exactly as written.

## Scores

complexity: 32
blast-radius: low
workflow: probe-then-spec
