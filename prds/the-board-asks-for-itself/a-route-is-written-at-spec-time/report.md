# Report — a route is written at spec time

Verdict: **DONE**

12 of 12 acceptance boxes ticked, each re-run independently against a fixture
I built myself — the analyst left every box unticked, so nothing was inherited
on trust. All three `## Verify and Proof` blocks exit 0 and end on an explicit
`echo`. Repo gate: `py_compile` clean, `workflows.py check .pearde` green
(5 workflows, 13 atomics), `guard.py` exit 0.

## Boxes

| spec | boxes | verify | what I re-ran |
|------|-------|--------|----------------|
| spec01 `workflows.py add` | 3/3 | `spec01 ok` | cross-kind refusal with a before/after file-set snapshot, workflow *and* atomic frontmatter, CLI exit 1 |
| spec02 `specced --route -` | 5/5 | `spec02 ok` | my own fixture board, exact added/removed file-set deltas per case, not the analyst's assertions |
| spec03 the four docs | 4/4 | `spec03 ok` | content read, not greps alone — one box did not hold, see below |

## The one box that did not hold

spec03 box 1 requires `references/parts/workers.md` to carry **no `none fit`
text**. It still did — line 158 read ``` `workflow: none fit` is not a verdict
this board accepts any more ```. The spec's own verify block greps only for
`| none fit` (the `## Scores` alternation, correctly gone) and for the phrase
`not a verdict this board accepts any more`, so the block passed while the box
was false. The box and the block contradicted each other.

Resolved by rewriting the one sentence to satisfy both — the retired verdict is
no longer named, the phrase the block greps for survives:

> draft one from the build you just ran, `## Route` below — a report
> naming no workflow is not a verdict this board accepts any more.

`none fit` now appears nowhere in the repo outside `.pearde/`. This also clears
a @references/language.md violation: the old sentence was a deprecation note,
and *Delete, do not deprecate* forbids it. One sentence, inside the footprint.

## `## Done when` — bullet 5 is not met

Bullets 1-4 hold, re-run directly:

| bullet | result |
|--------|--------|
| 1 · two new atomics + one existing → three files | exactly 3 written (`three-route`, `brand-new-a`, `brand-new-b`), existing step got no file, `runs: 0`, check green |
| 2 · `## Route` on a slug the library holds | refused, library byte-identical |
| 3 · `--workflow none` | refused, message names `## Route` literally |
| 4 · a route failing `workflow check` | refused, nothing written, `state: analyzing` unchanged |
| 5 · every PRD `specced` after this carries `workflow:` | **not met** |

`pearde specced <prd> --blast low` with `--workflow` **omitted entirely** still
succeeds, exit 0, and writes no `workflow:` key. `scan` then shows the PRD with
no `wf`:

```
specced   · d1 · p50 · w5 · wf three-route · boxes 0/1
specced   · d5 · p50 · w5 · boxes 0/1 · after d1
```

`specced()` in `resources/board/specs.py` gates `workflow == "none"` and gates a
slug that names nothing, but never gates `workflow is None`. The PRD's opening
sentence — *no PRD is specced without a `workflow:`* — therefore does not hold.

I did not fix it. No spec asked for it, and making `--workflow` mandatory
refuses every `specced` call that omits it, board-wide, on the gate every PRD
passes through. That is a scope decision for the orchestrator, not a call I
make inside an implementer run. The change is one condition beside the existing
`--workflow none` refusal; it wants its own PRD, or a line added to spec02.

## Findings outside scope — reported, not fixed

| row | what | whose |
|-----|------|-------|
| `doctor: skills broken` | `skills/` does not exist; the tree moved to `references/skills/` (14 files) in aea6dae, `resources/doctor.sh` still looks for the old path | the skill-tree rename PRD |
| `doctor: guard broken` | `guard.py` does not refuse a hand-walked board; the file carries another PRD's uncommitted work (+22 lines) | the guard PRD |
| `doctor: origin broken` | 15 derived PRDs, 3 with no `from:` | board data |

None is in this PRD's footprint and none is caused by this work — `doctor`'s
`briefs`, `workflows` and `board` rows, the ones this PRD could break, are all
green.

Carried over from the analyst, still true: `## Route` must be the report's
**last** section — `route_text()` reads raw text after the heading, so anything
added after `## Route` is silently swallowed into it. That rule is written in a
code comment in `specs.py` and nowhere a report author would look. A memo, not
a fix.

## Concurrency

`references/parts/workers.md` and `references/parts/loop.md` carry another
worker's `knowledge.py` PRD in the same tree. Verified intact after my edit:
the `knowledge.py query` analyst line, loop step 7, and the `brief --worker`
text all still stand. My single edit touched one sentence this PRD itself
added. Nothing reverted, no conflict.
