# a-pass-holds-its-turn-until-its-workers-are-in — analyst report

Verdict: SPECCED

Persona: engineer. Board language: English. Lane:
`/Users/feb/dev/infra/pearde/.pearde/.lanes/a-pass-holds-its-turn-until-its-workers-are-in`.

The build went through end to end. All five `## Done means` boxes are met in
the lane's working tree, uncommitted, and every check that could catch the
change was run and flipped. Two specs, `specs/spec01.md` and `specs/spec02.md`,
are written from what the build stands up; each says what already stands and
what is left.

## What the build did

Four prose edits and one harness:

| file | what changed |
|---|---|
| `references/parts/loop.md` | the intro rule list grows four → five, the fifth being the hold rule; the guard sentence after it narrows to `the first four` and names the verdict table as what holds the fifth |
| `references/parts/dispatch.md` | a paragraph under `## Why the pass is not worked here` saying a pass worker's return ends its children; step 2's `Anything else` note says why `waiting on workers` is the worst of the non-verdicts |
| `references/parts/workers.md` | the `A launch is not a life` paragraph closes by saying the check tells a dead worker from a live one and does not license returning over a live one |
| `references/agents/pearde-pass.md` | the verdict table gains a first row: worker in flight → `hold the turn`, never read by the dispatcher |
| `resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh` | new, untracked; seven phrase assertions over those four files, `ROOT=` to re-aim the run |
| `references/files.md` | the manifest row for the new script |

The invariant memo is drafted at `probe/memo-draft.md`, unplaced — placing a
file on the live board is the orchestrator's, not a probe's.

The ceiling and the liveness check were left exactly as they were, per the
PRD's `What must not change`. The hold and the ceiling compose rather than
compete: the pass holds, then hands back `MORE`. `references/parts/guard.md`
already allows dispatching, asking the user and the board's own commands at the
ceiling, so a pass at `context-budget` can still hold and collect — there is no
fork here to put to a person.

## What was proved

- `bash resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh`
  — 7 assertions, all held, exit 0.
- Flip proof on a copy under `ROOT=`: deleting each of the seven phrases in
  turn exits 1, and so does removing one of the four files. 8 of 8 red.
- The harness caught one of my own edits mid-build — a rewording of
  `workers.md` for `prose.py` broke an assertion and the script said so. It is
  not a check that cannot fail.
- `python3 resources/memos.py verify <slug>` runs the script and prints
  `holds`; with `return ends its children` reworded in `dispatch.md` it prints
  `BROKEN (exit 1)` and returns non-zero. Tested against a board copy in a
  temp dir, then reverted.
- `python3 resources/memos.py check` on a board copy carrying the drafted memo
  reports nothing against it beyond the `prds:` row, which resolves on the live
  board and not in the copy.
- `python3 resources/prose.py check`: `loop.md`, `dispatch.md`, `workers.md`
  clean; `pearde-pass.md` 6 unbound waste words, which is its baseline
  unchanged. My first draft added two violations and they were fixed.
- `python3 resources/index.py check`: 4 lines before the change, the same 4
  after — the new script's manifest row adds no fifth.

Per `a-harness-that-reads-the-whole-checkout-is-not-a-harness`, the harness
reads four tracked files and nothing else: no `git`, no repo-wide command, no
live board.

## Findings

**1 · The rule was already half-written, in two places nobody reads for it.**
`references/agents/pearde-pass.md` already said *"Workers still in flight means
you are still working — hold the turn … and return only when they are in or
dead"*, and `references/settings.md`'s `transitions-per-pass` row already said
*"`MORE` going out once spent, with nothing in flight"*. The PRD's diagnosis is
exact: the gap is `loop.md`, `dispatch.md`, and the verdict table itself. A
pass reading the loop and the settings table finds the rule in the settings
row's fine print and nowhere in the loop it is working. That is why the harness
asserts on the verdict *table* and not only on the prose above it.

**2 · The underlying decision was already taken, so no question was owed.**
`the-board-assumes-unlimited-agents` lists *"Let workers outlive their pass"*
under `## Alternatives considered` and refuses it: *"a background agent's life
past its parent's return is not something this harness promises. The pass holds
instead, and dispatches on every return."* This PRD is that memo's rule reaching
the files that govern a pass.

**3 · `hold` and `turn` are undefined in the board's grammar, and `hold`
collides with a PRD state.** `python3 resources/grammar.py show hold` and `show
turn` both answer *not defined on this board*, while `held` is a PRD state the
loop already names (`pearde claim` refuses *"held, not a leaf"*). After this
PRD, `hold` is a verb about a pass's turn and `held` an adjective about a PRD,
one letter apart. Two rows are owed to the grammar. Not written here: a row is
written from use, and this use is not committed yet.

**4 · Defect outside scope — `resources/index.py check` is red on `main`.**
Four lines, before I touched anything:

```
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk
references/parts/commits.md references @pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md — not on disk
```

The first is from `7e4d610`, which created `resources/common.py`; the second
and third from `b1d3f5d`, which deleted `hotreload-test.js`; the fourth is a
`@pearde/` prefix that stopped resolving when the board directory was renamed
(`c88a64a`). Every PRD whose acceptance box says *"`index.py check` is silent"*
fails today for reasons that are none of its own — which is exactly the disease
`a-harness-that-reads-the-whole-checkout-is-not-a-harness` was written about.
Both my specs assert *"the same four lines and no fifth"* rather than silence,
for that reason.

**5 · Defect outside scope — `bash resources/install.sh --check` misparses its
own flag.** It reads `--check` as the target directory: every skill reports
`missing  --check/<skill> — 5 of 5 links`, and it emits `dirname: illegal
option -- -` before the agent rows. The install check named by
`run-the-repo-gate` cannot be run in that spelling.

**6 · A recurring job the workflow library does not hold.** Adding an invariant
is three coupled files — the script under `resources/invariants/`, a `kind:
invariant` memo whose `verify:` names it, and a `references/files.md` row —
plus a `retag` to write the memo's `tags:` block, plus a flip proof per
assertion. Six invariants on this board were built that way and no workflow
file describes it; `add-a-file-to-the-skill` covers placing the file and the
manifest row, and stops there. Reported, not written: `probe-then-spec` fit the
job I was actually handed, and a second file is not mine to add.

**7 · Knowledge.** `python3 resources/knowledge.py query` on the contract
returned 90 hits, 51 strong, so no gap was enqueued for it. The strongest,
`260902-b296` — *"An adapter launch is not a live worker: two tests separate
them"* — is the liveness half of this rule, measured one level up at the
dispatcher. Nothing was learned outside this repo, so nothing was `remember`ed.

## Numbers

`complexity: 11` — the whole change is four prose paragraphs, one leaf shell
script and one memo. No code path moves, no schema, no state transition, no new
command. The cost that is not zero is judgment about wording in the two
highest-traffic reference files on the board, and the flip proof, which is
seven deletions against a copy.

`blast-radius: mid` — the footprint is seven files and every one is prose or a
new leaf. No existing script changes behaviour and nothing imports the new one
but a memo's `verify:`. It is not `low` because `loop.md` and `dispatch.md`
govern every pass on every board this machine watches, so a sentence that reads
wrong changes how every future pass terminates. It is not `high` because the
change is additive: the ceiling, the liveness check and the four verdicts all
keep exactly the behaviour they had.

Union of the footprints, seven files:

```
references/parts/loop.md
references/parts/dispatch.md
references/parts/workers.md
references/agents/pearde-pass.md
references/files.md
resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh
.pearde/memos/a-pass-holds-its-turn-until-its-workers-are-in.md
```

`.pearde/memos/…` resolves inside the board, which is its own git repo — the
invariant `a-board-s-own-file-commits-in-the-board-repo` is what makes that
footprint path commit in the right place.

## Workflow probe-then-spec

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | `read-the-contract` | passed | the PRD carries no `## Answers`; `the-board-assumes-unlimited-agents` closed the one fork the build would have hit |
| 2 | `capture-the-harness-baseline` | passed | `index.py check` 4 lines, `prose.py check` 6 unbound in `pearde-pass.md` — both red before the first edit, which is why both specs assert on the baseline rather than on silence |
| 3 | `attempt-the-build` | passed | four edits and one harness; the build hit nothing undefined |
| 4 | `re-run-the-harnesses` | passed | the probe added two `prose.py` violations and they were fixed; every other count is its baseline |
| 5 | `write-the-specs` | passed | two specs, footprints disjoint |

## Scores

complexity: 11
blast-radius: mid
workflow: probe-then-spec
