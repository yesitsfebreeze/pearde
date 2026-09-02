# the-loop-parts-are-rewritten-dense — implementer report

Verdict: DONE

30 of 30 boxes ticked across five specs. All five `## Verify and Proof` blocks
exit 0 the way `collect` runs them, and each was proved able to fail on a
mutated footprint file and restored with `cmp`.

Lane: `<board>/.lanes/every-document-is-written-in-the-writer-s-prose-the-parts-reference-is-rewritten-dense-the-loop-parts-are-rewritten-dense`,
HEAD `fc75bcf`, ten of the eleven parts modified, nothing staged, nothing
committed. `contract.md` is unmodified by design — 13% prose, already green,
a word cut there is a fact cut.

## This pass in one line

A killed predecessor left the eleven files rewritten and no box ticked. This
pass measured every claim, repaired three re-wrapped code spans and five verify
blocks whose exit was decided by a board-wide gate, and ticked what it ran.

## Boxes

| spec | boxes | state |
|---|---|---|
| `spec01` — roles, solo, derived, contract, board | 6 | all ticked |
| `spec02` — states, pass, dispatch | 6 | all ticked |
| `spec03` — commits | 5 | all ticked |
| `spec04` — loop | 6 | all ticked |
| `spec05` — guard | 7 | all ticked |

## Verify output

`python3 resources/prose.py check` on all eleven parts: silent, exit 0.
`probe/facts.py fc75bcf <each>`: silent, exit 0 on all eleven.

`prose.py stat fc75bcf`, before to after:

| file | before | after |
|---|---|---|
| `roles.md` | 146 | 128 |
| `solo.md` | 225 | 209 |
| `derived.md` | 265 | 265 |
| `contract.md` | 527 | 527 |
| `board.md` | 653 | 621 |
| `states.md` | 676 | 646 |
| `pass.md` | 545 | 504 |
| `dispatch.md` | 542 | 523 |
| `commits.md` | 1568 | 1497 |
| `loop.md` | 1713 | 1696 |
| `guard.md` | 1879 | 1850 |

Total 8,739 to 8,466, a 3.1% cut. `git diff --name-status fc75bcf --
references/parts` prints ten rows, every one `M`: no rename, no delete.
`grep -c '^| a' references/parts/board.md` prints `4`. `loop.md`'s seven step
rows are string-identical to the base commit's. `guard.md`'s fenced `json`
block is byte-identical, and all nine measurements are present.

## Harnesses

Baseline and re-run are the same tree — the footprint is eleven markdown files
and no code, so no board harness reads it. `python3 resources/index.py check`
prints the same three lines before and after, none of them in this footprint:

```
references/skills/pearde-machine.md is on disk with no row in references/files.md
references/language.md references @references/personas/writer.md — not on disk
resources/board/edit.py references @questions.py — not on disk
```

`PEARDE_ROOT=<lane> bash resources/doctor.sh` exits 0 with `index broken 3`
(those three), `origin broken 33 derived · 1 with no from:` and `memos broken
37 problems` — all three rows were red before the first edit and all name
files outside this footprint.

## What this pass changed

**Three code spans re-wrapped so they read whole on one line.** The predecessor's
rewrite split backticked spans across a line break, which leaves the fact
present to `facts.py` (it flattens the text before deciding) and absent to any
line-based reader. Fixed in `states.md` (`leaf: … held by <child> (parked)`),
`solo.md` (`pearde workflow check`), `board.md` (`pearde upgrade`) and
`guard.md` (`already wired, nothing changed`). A per-file check now confirms
every backtick span at `fc75bcf` is present character-identical in all eleven
files: 426 spans, 0 missing. Word counts are unmoved by these edits.

**Five verify blocks repaired.** Every block ended on
`python3 resources/index.py check | grep <this spec's files> && exit 1`. Under
the `bash -e -o pipefail` that `collect` uses, `index.py check` exits 1 on the
three inherited problems, so the pipeline's exit was 1 whether or not the grep
matched: `spec02` and `spec03` failed outright, and in the other three the
`&& exit 1` could never fire — a check that cannot fail. Each is now

```
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
case "$rc" in 0|1) ;; *) echo "index.py check crashed: $rc"; exit 1;; esac
if printf '%s\n' "$out" | grep <this spec's files>; then exit 1; fi
```

which prints the rows, refuses a crashed producer, and lets only a row naming
this spec's own files decide the exit. This is the route's own step 5 remedy
for a board-wide gate under `pipefail`, applied to blocks that already stood.

Three boxes were asserted in prose and unbacked by any command; each now has
one. `spec02` gained the character-identity check over every backtick span in
`states.md`, `pass.md` and `dispatch.md`; `spec04`'s two step-row counts became
a string comparison of the rows themselves, which the bare pair of counts could
not make; `spec05` gained the byte-identity check on the fenced `json` block.
`spec04` also had `$BASE:references/...` — correct under `bash`, but `:r` is a
modifier under `zsh`, so the line is now `${BASE}:` and reads the same under
both.

## Proof the blocks can fail

Each block was run against one mutated footprint file, the file restored from a
backup in a scratch directory outside the repo, and the restore proved with
`cmp`:

| spec | mutation | exit | restore |
|---|---|---|---|
| `spec01` | `derived.md`: `state: deferred` to `state: defered` | 1 | `cmp` ok |
| `spec02` | `pass.md`: `pass file owed` to `pass file due` | 1 | `cmp` ok |
| `spec03` | `commits.md`: `git reset --keep` to `git reset --kept` | 1 | `cmp` ok |
| `spec04` | `loop.md`: step row 4 renamed | 1 | `cmp` ok |
| `spec05` | `guard.md`: `318,584` to `318,585` | 1 | `cmp` ok |

The failing line is `references/parts/derived.md: lost code — state: deferred`
and its shape per file. These are behavioural mutations, not string-wiring
ones: each removes a fact the rewrite promised to carry, and the block detects
the loss. Two mutations that did **not** redden a block are worth recording,
because both are the checker behaving correctly: stripping the backticks off a
span leaves the words in the flattened text, and renaming one of two
occurrences of `pearde upgrade` leaves the shorter string as a substring of the
longer. `facts.py` asks whether a fact is gone, not whether its markup moved.

## Findings

Carried forward from the analyst pass, none closed by this one:

1. **These files hold nothing like a 30% cut.** The measured total is 3.1%,
   with both gates green and every fact intact. 71% of the 8,739 words are
   paragraph prose, so the root PRD's tree-wide 30% would need ~42% off the
   prose here; the observed ceiling on already-dense argument prose is 8–16%
   per paragraph, and `commits.md` — 85% prose, the loop part with the most
   room — yielded 4.5%. The root PRD's target will not be met from
   `references/parts/`. This contract names no percentage and the root PRD
   settles the conflict in the facts' favour, so it is a finding about the
   target, not a question.
2. **`prose.py` reads a numbered list as prose.** `prose_lines` skips lines
   opening `#`, `|`, `-`, `*`, `>` but not `1.`. Owner:
   `a-density-checker-and-the-root-docs-are-rewritten`.
3. **`prose.py` flags bound relative pronouns.** `one that is free` is correct
   prose and is refused, because the rule tests only the following word. Same
   owner.
4. **`references/personas/writer.md` is not on disk.** The standard's stated
   author is missing and `index.py check` says so. Owner:
   `templates-personas-and-agents-are-rewritten-dense`.
5. **`index.py check` was already red at `fc75bcf`,** on the three lines quoted
   above. No spec here can require a silent `index.py check`.
6. **Four sibling PRDs need the same no-fact-lost check.** `probe/facts.py` is
   one copy in one PRD's probe directory. Promoting it into `resources/` is the
   parent's call — it would touch `references/files.md`, which every sibling
   also touches.
7. **The analyst brief was dispatched with a truncated worker id**
   (`analyst-loop-parts` against the claim's `analyst-the-loop-parts`). This
   pass was dispatched with `impl-the-loop-parts` and the claim matched.

New this pass:

8. **A dense rewrite can lose a fact to a line break, and `facts.py` cannot
   see it.** The checker flattens whitespace before deciding, so a code span
   wrapped across two lines reads as present. It is present to a human and
   absent to every line-based tool downstream — a `grep` in a harness, a
   `## Verify and Proof` needle. The four sibling parts PRDs run the same
   checker and are exposed to the same class. The cheap repair is a second
   pass in `facts.py` over spans only, comparing the unflattened text; the
   owner is whoever promotes `facts.py` into `resources/` under finding 6.
9. **The machine's disk filled mid-run.** `df -h /` reported 256Mi free on a
   460Gi volume and the `Bash` tool could not write its own output file for
   several minutes. Nothing in this footprint caused it and nothing here fixes
   it, but a worker that dies with no report on this board may have died of
   this rather than of its contract.

## Workflow probe-then-spec

| step | atomic | result |
|---|---|---|
| 1 | `read-the-contract` | pass — PRD, five specs, the prior report and `probe/facts.py` read; `git status --short` recorded in the lane before the first edit |
| 2 | `capture-the-harness-baseline` | pass — no board harness reads this footprint; `index.py check` and `doctor.sh` recorded with `PEARDE_ROOT=<lane>` before the first edit, three inherited reds named |
| 3 | `attempt-the-build` | not entered as build-and-spec work — the route's second pass, per its own `Fails when` row: the specs exist and the predecessor's build is in the lane. No red-to-green here is claimed as this pass's |
| 4 | `re-run-the-harnesses` | pass — same commands, same `PEARDE_ROOT`, same three inherited lines, no count moved |
| 5 | `write-the-specs` | pass as the second-pass form — no spec authored; the `Fails when` table applied to the five blocks that already stood, and the two exits it names were repaired |

### Edits

The route's `read-the-contract` step tells a worker to resolve every `@<path>`
in the PRD body. This PRD's body is one sentence and cites none, and its specs
carry the paths instead. No edit is owed — the step passed as written.

One shape the route's step 5 `Fails when` table does not list, offered as a new
row for it:

| seen | means | do |
|------|-------|----|
| a block ends on `<board-wide gate> \| grep <own files> && exit 1`, and the gate is red on rows outside the footprint | under `pipefail` the pipeline carries the gate's exit, so the `&& exit 1` never fires and the block's own exit is the gate's — the check cannot fail, and where the line is last the block fails for a reason outside its footprint | capture the gate (`out=$(<gate> 2>&1) && rc=0 \|\| rc=$?`), refuse a crashed producer by exit code, and put the grep in an `if … then exit 1; fi`. The existing row names the capture; it does not name that the `&& exit 1` tail is dead in the same breath |

## Scores

complexity: 36
blast-radius: mid
workflow: probe-then-spec
