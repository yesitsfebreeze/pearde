Verdict: DONE

# the-promotion-rule — implementer, pass two

The rule stands in the lane `lane/the-promotion-rule`
(`/Users/feb/dev/infra/pearde/.pearde/.lanes/the-promotion-rule`), 47 lines
across the three footprint files, nothing in the checkout.

## What the brief said and what was there

The brief said "the tree already holds the probe's uncommitted code —
continue it". It did not. `git status --short` in the lane was **empty**, and
`git -C <checkout> status --short -- <each footprint path>` was empty too —
the analyst's pass one build survived in neither tree, only in `specs/spec01.md`'s
prose and its ticked boxes. So the build was redone from the spec rather than
continued. Every box the analyst ticked was re-run here before it was left
ticked; `pearde specced --check` warns `spec01.md:49: 5 of 5 boxes already
ticked before an implementer ran them`, which is the analyst's tick, not a
claim of mine.

## The build

`resources/workflows.py`:

- `ROUTE_RE = re.compile(r"\brun\s+(?:the\s+)?`([a-z0-9][a-z0-9-]*)`", re.IGNORECASE)`
  — the pattern matches the **routing verb**, never the slug alone, which is
  the PRD's own guard: "compare with the `<slug>` atomic" carries no verb and
  is prose.
- `_routed_atoms(body, slug, lib)` reads only the `## Do` section, and keeps a
  match only where the library holds that slug **as an atomic** and it is not
  the file's own. So a command (`run \`pytest tests/\``), an unknown slug, a
  self-reference and a sentence in `## Fails when` all pass.
- One line in `check()`'s atomic branch, inside the row the doctor's
  `workflows` row already runs — no new row, no new command:
  `` <file>.md: `## Do` routes to `<other>` by slug — route it (a workflow with two atomics) or inline it (prose, one unit again) ``

`references/workflow.md` gains one bullet in `## The check`'s failure list;
`references/templates/atomic.doc.md` gains one paragraph under `## Do`, beside
the sentence that already says an atomic needing "and then" is two atomics.
Each states the rule once, for its own reader.

This was an **edit to existing footprint files**, not new code staged under
`probe/` — a guard inside `check()` has no meaning outside the function it
lives in.

## The census the PRD asks for is empty

`python3 resources/workflows.py check /Users/feb/dev/infra/pearde/.pearde`
prints nothing, before and after. No atomic in the 23-file library routes to
another by slug today, so there is nothing left to inline or promote by hand.
The two `workflows/*.md` lines that contain the words "run `" at all —
`attempt-the-build.md:73` and `write-the-specs.md:120` — are `## Fails when`
table cells, not `## Do` steps, and neither backticks a slug after the verb.

## Per-spec box status

`specs/spec01.md`, all five ticked, each re-run here:

1. **route refused, naming both** — `ok a bare \`Run \`<slug>\`.\` step is
   refused`, `ok a route behind a lead-in clause is refused`, `ok the refusal
   names the atomic, the routed-to slug and both choices`.
2. **prose / absent slug passes** — `ok a prose comparison to a sibling
   passes`, `ok \`Run \`pytest tests/\`.\` passes — not a slug`, `ok a slug the
   library does not hold passes`, plus two the spec did not ask for: `ok an
   atomic naming its own slug passes`, `ok the same sentence outside \`## Do\`
   passes`.
3. **each reference file states it once** — `ok references/workflow.md's
   failure list states the rule once`, `ok
   references/templates/atomic.doc.md states the rule once`.
4. **same counts and `ok` before and after** — the doctor row is byte-identical
   in both runs: `  workflows   ok      7 workflows · 23 atomics · the library
   checks out`. `workflows.py check` prints nothing in both.
5. **the map gains no line** — `index.py check` prints the same three lines
   before and after (`resources/common.py is on disk with no row in
   references/files.md`; `references/files.md lists
   @resources/board/hotreload-test.js — not on disk`; `@@view names
   @resources/board/hotreload-test.js — not on disk`), all pre-existing and
   naming no footprint path.

## Verify output

`bash prds/the-promotion-rule/probe/verify.sh` with `PEARDE_ROOT=<lane>`:
`11/11 passed`, exit 0. The same harness run with
`PEARDE_ROOT=/Users/feb/dev/infra/pearde` — the pre-edit checkout — prints
`6/11 passed`, exit 1, so it is a harness that can fail rather than one that
always reads green.

`probe_promotion_rule.py`: four `[ok]` lines, no `MISMATCH`.

## The spec's `## Verify and Proof` block could not run — rewritten

The block as written was:

```
cd <repo>
python3 .pearde/prds/the-promotion-rule/probe/probe_promotion_rule.py
python3 resources/workflows.py check /Users/feb/dev/infra/pearde/.pearde
PEARDE_ROOT="$PWD" bash resources/doctor.sh | grep -A1 '^  workflows'
python3 resources/index.py check
```

Run the way `collect` runs it — `bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec01.md)"` —
it dies immediately: `bash: -c: line 0: syntax error near unexpected token
'newline'`. Unquoted `<repo>` parses as a redirect. Every box above it was
already ticked, so nothing on the board said the proof had never been run.
Three further breaks sat behind it: `.pearde/prds/…` does not exist in a lane;
`doctor.sh` exits non-zero on rows outside this footprint and under `pipefail`
that kills the block; `index.py check` exits 1 on its three pre-existing lines.
And nothing in the block asserted anything — it printed and moved on.

The block now resolves its root (`PEARDE_ROOT`, else the code repo via
`git rev-parse --path-format=absolute --git-common-dir`), runs the harness,
and asserts four things that can each fail: the census is empty, the doctor's
`workflows` row still reads `7 workflows · 23 atomics`, the map names no
footprint path, and the map holds no line beyond the two pre-existing ones.
Proven in a merged tree built per `write-the-specs`' own instruction
(`git clone --shared <lane>` + `git apply` the lane diff + `ln -s <board>
<scratch>/.pearde`, census 127 PRDs, not a vacuous sweep): exit **0** intact,
exit **1** with `ROUTE_RE` neutered.

`prds/the-promotion-rule/probe/verify.sh` is new — the PRD had a probe script
but no harness, so the doctor's `harnesses` row could not see this work. It
pins its denominator (`11 checks`).

## Harness baseline and re-run

Ten of the board's harnesses invoke `workflows.py`; none spells a footprint
path, so this is the set. All run `PEARDE_ROOT=<lane>` both times. Every one
was **already failing before the first edit** and every count is unchanged
after it:

| harness | before | after |
|---|---|---|
| check-crosses-member-boundaries | `verify: 16/18 checks pass` | same |
| one-definition-of-the-board-not-two | `verify.sh done, fail=5` | same |
| every-module-finds-its-siblings-by-one-rule | `probe: 22 passed, 1 failed` | same |
| the-board-runs-itself/an-example-board | `37 checks · 36 pass · 1 fail · 1 skipped` | same |
| the-board-runs-itself/specced-is-a-command | `verify: 89/90 checks pass` | same |
| tags-are-derived-when-the-vault-is-written | `probe: FAIL` | same |
| workflow-attach | `44/47 checks pass` | same |
| workflow-improve | `62/71 checks pass` | same |
| workflow-reader | `verify: 23/39 checks pass` | same |
| workflow-seed | `76 checks · 68 pass · 8 fail` | same |

The doctor's row set is otherwise unchanged except for rows a sibling session
moved while this ran (`statusline *435 ↑160` → `*445 ↑163`, `vision 71 off` →
`70 off`, `knowledge broken` → `ok`, `health` gained `stale`). None touches
this footprint.

## Findings

Carried forward from pass one, still true:

- `docs/content/docs/improvements/workflows-promotion.mdx` is on disk and is
  word-for-word this PRD's body. The PRD's italic recovery note ("it left the
  working tree mid-pass … recover at git 6839a9b") is stale. Not fixed — the
  PRD body is frontmatter-adjacent prose this pass does not own.

New this pass:

- **The brief's "the tree already holds the probe's uncommitted code" was
  false in both trees.** A lane is cut from the code repo's HEAD; pass one
  built in a tree that no longer exists. The board's only record of that build
  was the spec's prose. This cost a full rebuild, and it is the second-order
  reason the spec's verify block was never run.
- **`prds/**/probe/` is gitignored on the board** (`.gitignore:61`), so this
  PRD's harness and probe script are machine-local. `pearde collect` merges the
  lane's code but carries no probe, and a fresh clone of the board cannot run
  the block this spec now contracts. Board-wide, pre-existing, outside this
  footprint — reported, not fixed.
- **`bash resources/doctor.sh --harnesses <board>` does not finish.** It was
  killed at 600 s having reached the `plan` row and not the `harnesses` row.
  The row's own text says "this row costs tens of seconds"; the board now
  carries 100 harnesses and it costs minutes. The baseline was taken from the
  named subset instead. See the Edit below.
- `resources/plan.py` does not exist in this tree — `specced` is
  `python3 resources/pearde.py specced`. Anything still spelling `plan.py` is
  stale; `write-the-specs.md:120` does (`python3 resources/memos.py index` is
  fine, but `plan.py`'s `cmd_status` is named in `workflows.py:check`'s own
  comment). Reported, not fixed.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | passed · the `## Fails when` row for "a lane whose `git status` is empty" was taken, the checkout was read, and **neither** tree held the build — see Edit 1 |
| 2 | capture-the-harness-baseline | passed · the full `--harnesses` sweep timed out at 600 s, the ten `workflows.py` harnesses plus `index.py check`, `workflows.py check` and the doctor rows were recorded instead — see Edit 2 |
| 3 | attempt-the-build | passed · an edit in place to three footprint files, plus `probe/verify.sh` written as it went, per step 4 |
| 4 | re-run-the-harnesses | passed · every one of the ten counts identical, same `PEARDE_ROOT` both times |
| 5 | write-the-specs | passed · no spec authored (second pass); its `## Fails when` rows for a placeholder block and for a lane block reading `.pearde/prds/…` both fired on the block that already stood, and both were closed as those rows instruct |

### Edits

**Edit 1 — `workflows/read-the-contract.md`, `## Fails when`, new row after
the row beginning "the `repo:` root is a worktree under `<board>/.lanes/`".**
That row assumes the checkout holds the hunks the lane lacks. It has no shape
for the case where neither does, which is what happened here. Replacement text
(one new row):

```
| the `repo:` root is a lane, `git status --short` is empty in **both** the lane and the checkout, and the brief still says the probe's code is there | pass one built in a tree that has since been discarded — a lane deleted and recut, or a `checkout --` over the footprint. The board's only surviving record of that build is the spec's prose and its ticked boxes | rebuild from `specs/`, which is a complete description by contract, and re-run every ticked box before leaving it ticked. Say in the report that the boxes were the analyst's tick and not evidence: a spec whose build vanished is very often a spec whose `## Verify and Proof` block was never run either, so run that block the way `collect` runs it before anything else |
```

**Edit 2 — `workflows/capture-the-harness-baseline.md`, `## Fails when`, new
row.** Step 1 tells the worker to run the board's harness set, and on a board
this size the sweep outlives the worker. Replacement text (one new row):

```
| `bash resources/doctor.sh --harnesses <board>` is killed by a timeout before the `harnesses` row prints | the row's "costs tens of seconds" was written when the board held a dozen harnesses; a board of a hundred costs minutes, and the whole baseline is lost with the run | do not sweep. Name the subset first — `grep -l '<the module your footprint edits>' $(find <board>/prds -name verify.sh)` — and run those by hand with `PEARDE_ROOT=<lane>`, recording each one's last line. Run `doctor.sh <board>` **without** `--harnesses` for the rows; the `harnesses` row then reads `off` in both baseline and re-run, which compares honestly |
```

No other atomic sent a wrong command, a stale path, or a check that cannot
fail.

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec
