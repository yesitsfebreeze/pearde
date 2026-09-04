Verdict: REFINE

# the-parts-reference-is-rewritten-dense — analyst report, pass two

workflow: `probe-then-spec`

28 files, 31,185 prose-counted words. The build went through on three more
files — `references/parts/order.md`, `references/parts/pass.md`,
`references/parts/commits.md` are rewritten dense in the lane, `prose.py check`
green on each and zero facts lost against `HEAD`. Nothing the build touched is
undefined. The split below is a size split, not a fork: 28 files of this kind
cannot be six specs summing 40.

This pass reproduced pass one's verdict from its own build rather than from its
report, and reaches the same four children. Two of pass one's findings are
confirmed against fresh evidence, and one new finding is added — the standard's
named source is not on disk.

## What the build did

Route: rewrite the file whole, `prose.py check` it, locate every remaining
unbound hit, diff the fact set against `HEAD`, repeat.

| file | words before | after | cut | `prose.py check` | facts |
|---|---|---|---|---|---|
| `references/parts/order.md` | 1069 | 1006 | 5.9% | `0` | 46 -> 46, 0 lost |
| `references/parts/pass.md` | 545 | 474 | 13.0% | `0` | 24 -> 24, 0 lost |
| `references/parts/commits.md` | 1568 | 1526 | 2.7% | `0` | 78 -> 78, 0 lost |

3,182 words in, 3,006 out: 5.5% over the three, with every fact intact and the
checker green. `commits.md` was chosen as the best case for a deep cut — 85% of
its words sit in paragraph lines, the highest share in the directory bar
`derived.md` — and it cut least of the three, because the paragraphs are
argument and the contract keeps argument.

Probe, all under `probe/`, left uncommitted for the children:

- `facts.py` — pass one's fact set: every inline-code span, every non-blank
  line in a fence, every `@path` and `@@keyword`, every table row's cells.
  `diff HEAD <path>` exits 1 on any loss. Re-run over all 28 files after this
  build: `0` losses.
- `cuttable.py` — new. Per file, the `prose.py` word count against the words in
  paragraph-shaped lines, the only lines a rewrite may shorten. The share is
  the ceiling on any cut before a word is saved.
- `where.py` — new. Prints the text around every unbound waste word, which
  `prose.py check` does not.

Harnesses after the build, against the same three lines before it:
`python3 resources/index.py check` unchanged, and none of its three lines names
a file under `references/parts/`. `python3 resources/memos.py check` exits 0.
`prose.py check references/parts/*.md` goes from 27 violating files to 24.

## Findings

**The parent's 30% cut is unreachable on `references/parts/`, and the ceiling
is measured, not guessed.** `cuttable.py` puts 18,947 of the directory's 31,122
words in paragraph lines — 61%. A 30% cut of the whole therefore needs half of
every paragraph deleted, and the paragraphs are the argument the contract
protects. Three careful rewrites this pass returned 5.5%; pass one's three
returned 4.6% to 11.6%. Six files, two workers, no rewrite near 30%. Not
repaired here — the claim is the parent's `## Verify`, not this PRD's.

**`references/personas/writer.md` is not on disk.** The parent's contract is
"written in the `writer` persona's prose — @references/personas/writer.md, Vera
Lindqvist", the landed sibling wrote that handle into `references/language.md`,
and `references/personas/` holds designer, engineer, mentor and skeptic only.
`resources/index.py check` has been printing the dangling handle since that
sibling landed, which is the parent's own verify line `index.py check` silent
failing today. The prose standard a rewriter is meant to write in is a memory
and not a file; only the nine mechanical rules under `## Density` exist. Not
repaired here — `references/personas/` and `references/language.md` are outside
this PRD's footprint. It is the parent's to place, and it gates nothing this
build needed: `prose.py` is the standard a rewrite is checked against.

**The unbound-waste rule fires on bound relative clauses — confirmed on fresh
text.** `resources/prose.py` tests the word after `it`, `this`, `that` or
`there` against a linking-verb set, so a relative pronoun reads as a vague
subject. My own rewrite of `commits.md` was green on everything else and still
carried five: `prints what it would add`, `back to the commit it was on` twice,
`a board that is its own repo`. All four are correct English and all four had
to be reshaped — `the paths to add`, `its previous commit`, `a board being its
own repo`. Reshaping is per occurrence and is not a substitution, so the count
`prose.py check` prints is the real remaining work on a file. 24 of 28 files
still fail on this class and nothing else. Not repaired here —
`resources/prose.py` is the landed sibling's footprint.

**Rewrite the file whole; never patch it by line number.** Pass one lost two
lines of surviving content to a line-indexed patch, invisible to
`prose.py check`. This pass wrote every file whole from a heredoc and used
`str.replace` with an asserted match for the five repairs, and lost nothing.
The assertion is the point: the first repair batch failed its assert on a
wrapped line and wrote nothing, rather than writing four of five.

**Words the grammar does not define.** `python3 resources/grammar.py show`
carries no row for `dense`, `density`, `fact`, `cut` or `prose` — the words this
PRD's contract is written in, and `fact` now has a mechanical meaning on this
board, the one `probe/facts.py` implements. Reported, not written: a row is
written from use.

**Knowledge gap.** `knowledge.py query` on the contract returned 0 hits and
enqueued `pending/260902-5c71.md` at priority med. Nothing on record.

## Why not SPECCED

The board's own calibration is the landed sibling: `references/files.md` at
2,721 words is one spec at `complexity` 6. At that rate 31,185 words is
`complexity` 69 and 15 to 20 specs. Nothing in this build argues the rate down —
the three files above each needed a whole-file rewrite plus a located repair
round, and the two smallest still took a full pass each. Six specs summing 40
would mean five files and 5,200 words per spec at `complexity` 6.6, which is
`references/files.md` twice over for the same number. `settings.md` caps the set
at 6 specs and 40.

## The split

Four children, one disjoint file set each, none consuming another's output —
they run at once. Grouped by subject, so one rewriter holds one subject and the
cross-references inside a group land in the same pass.

| child | files | words |
|---|---|---|
| `the-loop-parts-are-rewritten-dense` | loop, guard, commits, states, pass, dispatch, contract, derived, solo, roles, board | 8,226 |
| `the-worker-parts-are-rewritten-dense` | workers, workflows, personas, consult, health, grammar, memos | 7,589 |
| `the-surface-parts-are-rewritten-dense` | view, doctor, order, progress, statusline | 8,254 |
| `the-cross-board-parts-are-rewritten-dense` | machine, handles, ramp, all, master | 7,116 |

11 + 7 + 5 + 5 = 28, and the four word counts sum to 31,185. By the sibling's
rate each child lands at `complexity` 16 to 19 and 5 or 6 specs.

Each child declares its footprint as its own files — `references/parts/loop.md`
and the rest, never `references/parts` — so the four are disjoint and no
`after … (footprint)` edge orders them. The board's `## Footprints` section
names `references/parts` as a written-whole root; that spelling would put all
four children on one footprint, and this is the case it does not fit.

Three files are rewritten in the lane and stay uncommitted for the child that
owns them: `pass.md` and `commits.md` under the loop child, `order.md` under
the surface child. Pass one's three rewrites are gone — the lane was cut fresh
from the sibling's commit before this pass, so `roles.md`, `board.md` and
`doctor.md` are at `HEAD` again. Each child's first spec picks up `probe/facts.py`, `probe/cuttable.py`
and `probe/where.py` rather than rebuilding them.

## Split

| child | contract | needs |
|---|---|---|
| the-loop-parts-are-rewritten-dense | `references/parts/` loop, guard, commits, states, pass, dispatch, contract, derived, solo, roles and board rewritten dense, `prose.py check` green on each and no fact lost against `HEAD` | — |
| the-worker-parts-are-rewritten-dense | `references/parts/` workers, workflows, personas, consult, health, grammar and memos rewritten dense, `prose.py check` green on each and no fact lost against `HEAD` | — |
| the-surface-parts-are-rewritten-dense | `references/parts/` view, doctor, order, progress and statusline rewritten dense, `prose.py check` green on each and no fact lost against `HEAD` | — |
| the-cross-board-parts-are-rewritten-dense | `references/parts/` machine, handles, ramp, all and master rewritten dense, `prose.py check` green on each and no fact lost against `HEAD` | — |
