# skills-and-scout-docs-are-rewritten-dense — implementer report

Verdict: DONE

Twelve acceptance boxes, twelve ticked, none newly ticked. `main` moved seven
commits since pass five, so every box was re-measured against a merged tree
nobody had seen before: `probe/verify.sh` scores **14/14, exit 0**, `REF=main`
scores **9/14, exit 1**, and a mutation reddens each of the five boxes the
control leaves green. Both `## Verify and Proof` blocks exit **0** green and
**1** with one footprint file mutated, run the way `collect` runs them.

One thing was written, and it is the reason this PRD kept coming back: the
lane was **five commits behind `main`**, so `lanes.merge --ff-only` could not
land it however green the boxes were. The lane is rebased onto `main`, its
tree is `2e17d05` — byte-for-byte the tree every box above was measured on —
and `git merge-base --is-ancestor HEAD lane/…` now passes. No file content
changed in the rebase; no conflict arose.

workflow: probe-then-spec (second pass — steps 3 and 5 not entered as
build-and-spec work; see `## Workflow probe-then-spec`)

## What this pass adds to pass five

| what | result |
|---|---|
| re-measured all 14 verify lines against **today's** `main` | 14/14, exit 0 |
| re-took the negative control | `REF=main` 9/14, exit 1 |
| re-proved every box the control cannot redden | 6 mutations, 6 `cmp`-clean restores |
| ran both spec blocks as `collect` runs them, both directions | 0 green, 1 mutated |
| **new:** actually *ran* the five foreign harnesses, on like-for-like trees | identical counts and identical FAIL sets |
| **new:** rebased the lane onto `main` | `--ff-only` will now succeed |
| **new:** cleared 8 dead fixture boards from the live daemon | registry back to 10 real boards |
| re-ran the repo gate | 2 `index.py check` rows, both outside the footprint |

## Boxes

Every line below was run by this pass, not read off pass five's report.

### spec01 — the nineteen skill files read dense, frontmatter included

| box | verify line | proof it can fail, this pass |
|---|---|---|
| `[x]` `prose.py check references/skills/*.md` exits 0 | `PASS spec01.1` | `REF=main`; and a padded sentence in `pearde-report.md` |
| `[x]` every `name:` byte-identical to `main` | `PASS spec01.2` | `"/drill"` to `"/DRILL-MUTANT"` in `pearde-drill.md` |
| `[x]` no `description:` over 1,024 characters | `PASS spec01.3` | `REF=main` — `pearde-all.md` is over on `main` |
| `[x]` doctor reports `skills ok 19 well-formed` | `PASS spec01.4` | `name: pearde-view` to `pearde-viewx` |
| `[x]` 18+ files changed in scope, every line `M` | `PASS spec01.5` | `REF=main` |

`spec01.2` carries the trigger-phrase and code-span lists as well as `name:` —
one box, one verify line. Six boxes, five verify lines: `spec01.2` covers two.

### spec02 — the four scout documents read dense, every route id intact

| box | verify line | proof it can fail, this pass |
|---|---|---|
| `[x]` `prose.py check resources/scout/*.md` exits 0 | `PASS spec02.1` | a padded sentence in `findings.md` |
| `[x]` `route.sh list` returns 45 | `PASS spec02.2` | demoting `### hn` to `## hn` in `routes.md` |
| `[x]` the route id set is unchanged | `PASS spec02.3` | renaming `### hn` reddens 02.3 alone; demoting it reddens 02.2 and 02.3 |
| `[x]` each file keeps its table rows | `PASS spec02.4` four times | dropping the first row of `reading-list.md` |
| `[x]` `index.py check` says what it says on `main` | `PASS spec02.5` | `@references/nope-mutant.md` in `resources/scout/README.md` |
| `[x]` the scope's word count is below `main`'s | `PASS spec02.6` | `REF=main` — 13115 against 13115 |

Two of the six mutations are behavioural: `spec02.1`'s and `spec01.1`'s put a
sentence back that `prose.py` **computes** a violation from, and `spec02.5`'s
makes `index.py` resolve a reference that does not exist. The other four aim
at strings the harness greps, so they prove the counter is wired rather than
that a regression is detected — said plainly rather than left for the tick to
imply.

Every mutation was made on the lane's working file, backed up to a scratch
directory outside both repos, restored by `cp` and proved with `cmp`:
`restore cmp-clean` on all eight (six box mutations, two block mutations).
`git status --short` is empty in the lane afterwards.

## Verify output

```
merged tree 2e17d05cb0fe60c3c51e959cc17d05dfcb780651  (main + 64ed54a + uncommitted)
PASS  spec01.1 prose.py names no file in references/skills/
PASS  spec01.2 every name: and every trigger phrase byte-identical to main
PASS  spec01.3 no description: exceeds 1024 characters
PASS  spec01.4 doctor reports 19 well-formed skills
PASS  spec01.5 18+ files changed in scope and every line is M
PASS  spec02.1 prose.py names no file in resources/scout/
PASS  spec02.2 route.sh list returns 45 routes
PASS  spec02.3 the route id set is unchanged
PASS  spec02.4 findings.md keeps every table row
PASS  spec02.4 reading-list.md keeps every table row
PASS  spec02.4 README.md keeps every table row
PASS  spec02.4 routes.md keeps every table row
PASS  spec02.5 index.py check says exactly what it says on main
scope words 13115 -> 12928
PASS  spec02.6 the scope's word count is below main

boxes 14/14
```

`REF=main bash …` prints `boxes 9/14` and exits 1, reddening `spec01.1`,
`spec01.3`, `spec01.5`, `spec02.1` and `spec02.6`.

Both blocks were awked out of their fences and run under `bash -e -o
pipefail` from the checkout root, never from the lane: **spec01 exit 0,
spec02 exit 0**. With a sentence padded into
`references/skills/pearde-report.md` spec01 exits **1** on `spec01.1`; with
the same done to `resources/scout/findings.md` spec02 exits **1** on
`spec02.1`. Both directions, both blocks, both restores `cmp`-clean.

## The five harnesses outside this PRD that read the footprint

Pass five checked their needles on two archived trees and did not run them,
citing the fixture hazard. This pass ran all five — on **two archive trees
built the same way**, `main` and merged, so the comparison is like for like:

| harness | main archive | merged archive | FAIL set |
|---|---|---|---|
| `nothing-left-open/the-skill-tree-is-guarded` | 36 pass · 5 fail | 36 pass · 5 fail | identical |
| `the-board-runs-itself/an-example-board` | 29 pass · 8 fail | 29 pass · 8 fail | identical but for `mktemp` paths |
| `the-board-runs-itself/readme-in-three-rings` | 70 pass · 5 fail | 70 pass · 5 fail | identical |
| `the-round-runs-in-a-window-that-ends` | 25 pass · 1 fail | 25 pass · 1 fail | identical |
| `workflows-on-the-board/workflow-skill` | 21 pass · 34 fail | 21 pass · 34 fail | identical but for `mktemp` paths |

Not one line moves across the merge. The failures in both columns are the
scratch tree having no board directory — see finding 8's neighbour in
`### Edits`, which is a trap in the route's own step 2 and the reason the
first reading of this table was wrong.

## The board gate

| gate | before the first edit | after |
|---|---|---|
| `index.py check` in the checkout | 2 rows — `resources/board/refuse.py` has no `files.md` row, `references/language.md` cites `@references/personas/writer.md` not on disk | identical |
| `doctor.sh` in the checkout | `skills ok 19 well-formed`; `index broken 2 problems`; `origin broken 33 derived`; everything else `ok` or `off` | identical but for `statusline` |
| `spec02.5` — `index.py check` on `main` against merged | line for line equal | equal |

Both `index.py check` rows were red before the first command of this pass and
neither names a footprint path. `refuse.py` is a live sibling's untracked
file: absent at 23:05 when the baseline was taken, present at 23:09. The
`writer.md` row has stood for five passes.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | ran. PRD, both specs, pass five's report, `git status --short` in both roots before the first command. Footprint resolved to the **code** repo at `/Users/feb/dev/infra/pearde`, not the board at `pearde/` — the row about a footprint spanning two roots. The brief says the probe's code is uncommitted and `git status` was clean: step 3's row for that is exactly right, `collect` had committed the lane |
| 2 | `capture-the-harness-baseline` | ran. 73 board harnesses at 23:05, 74 at 23:09 — a sibling landed one mid-run, recorded as new with no baseline. Six name a footprint path, one of those is this PRD's own. Gates recorded above, before the first edit |
| 3 | `attempt-the-build` | **not entered as build-and-spec work** — the specs exist and the build stands. That is the row `## Fails when` names for this route's second pass. No flip is claimed; every red-to-green was earned by the pass that built it. The step's lane row *was* entered, and it is what produced the rebase |
| 4 | `re-run-the-harnesses` | ran. Every recorded count re-measured, none moved on a path of mine, and the five foreign harnesses run on matched trees |
| 5 | `write-the-specs` | **not entered as authoring** — its `## Fails when` table applied to the two blocks that stand: both run under `bash -e -o pipefail`, both exit 0 green and non-zero mutated, no block runs the whole workspace, every path literal, no box asks for a commit |

Back-edges taken: none.

### Edits

One atomic has a gap that cost this pass a wrong reading, and one has a
command that damages a live machine. Both replacements are below.

**Step 2, `capture-the-harness-baseline` — a new `## Fails when` row.** The
route tells a lane worker to run each board harness under `PEARDE_ROOT=<lane>`
or against a merged tree built in scratch. On this board the merged tree can
only be built from `git archive` or `git clone`, and the board directory
(`pearde/` here, `.pearde/` elsewhere) is **gitignored** — so it is not in the
archive. Every harness that reads the board then fails in the scratch tree for
a reason that is not the build's, and a worker comparing that scratch tree to
the live checkout reads those failures as its own regression. This pass read
one that way for a minute: `the-skill-tree-is-guarded` scored 37 pass against
the checkout and 36 against the merged archive, which looked like a landing
until both were re-run as archives. The row the section does not carry:

| seen | means | do |
|------|-------|----|
| a harness scores worse on a merged tree built by `git archive`/`git clone` than on the live checkout, and the extra failures name a board path | the board directory is gitignored, so it is in the checkout and not in the archive — the difference is the missing board, not the build | never compare an archive tree to the checkout. Build **both** sides the same way — `git archive main` into one scratch dir and the merged tree into another — and compare those. Do not symlink the live board into the scratch tree to close the gap: `pwd -P` resolves it straight back to the live board and the score gets *worse*, measured here at 35 pass against 36 |

**Step 3, `attempt-the-build` — the fixture-registry row needs its repair
narrowed.** The row already says a fixture board can land in the live
daemon's registry and names `serve.py forget <name>` as the repair. It does
not say how to tell a dead registration from a live one, and `forget` takes a
*name*, so a worker reaching for it against the wrong name unwatches a real
board — which happened here, to `kern`, and was restored by
`serve.py ensure .` from that board's own root, same name, same path. Replace
the row's `do` cell with:

> never run a `--fix`-shaped command against a fixture while a real service is
> up; point it at a dead port (`PEARDE_PORT=1`) so the repair cannot connect,
> and check `serve.py status` at the end. To remove one already landed, test
> the **path** first — `[ -d <path> ] || serve.py forget <name>` — because
> `forget` takes a name and a mistyped one unwatches a live board; if that
> happens, `serve.py ensure .` from the board's own root restores it under the
> same name.

## Findings

Pass five's seven findings, carried forward by name, plus two new.

### 1. `main` moved under this lane — reopened, and now closed differently

Pass five recorded the lane one ahead and zero behind. `main` has since taken
**seven** commits (`58c92e6` to `9889e78`), three of them during this pass's
own hour, and the lane fell five behind — which is why `--ff-only` refused and
why this PRD is on its sixth pass. `git merge-tree --write-tree` exited 0
throughout, so there was never a conflict, only a stale base. Rebased onto
`9889e78`; the resulting tree `2e17d05` is the merged tree every box was
measured on, so the rebase is provably content-free.

### 2. A board landing every few minutes outruns a lane's rebase — new, and the real defect

`main` moved **twice inside three minutes** of this pass: `9a98fae` at 23:09,
`191bedc` and `9889e78` by 23:14. The lane was rebased, went behind again in
under sixty seconds, and was rebased a second time. No worker can win that
race from outside: whichever way it ends, `land_lane` commits the lane and
then finds its `--ff-only` refused by whatever landed in between, leaves the
work committed on `lane/<slug>` and the PRD `claimed`, and nothing on the
board says so. The repair belongs inside `land_lane`: rebase onto the
checkout's branch **immediately before** the `--ff-only` merge, in the same
critical section, and retry the pair on refusal. Reported, not fixed —
`resources/board/lanes.py` is not this PRD's footprint, and a live sibling has
it modified right now.

### 3. `serve.py forget` on a dead board removes the entry and then crashes — new

Reproduced on a fixture registered and then deleted: the entry **is** removed,
and the client dies on `http.client.RemoteDisconnected: Remote end closed
connection without response` — the daemon closes the socket on `/unregister`
without answering, apparently while touching the path that is gone. A caller
reading the traceback concludes the removal failed and tries again. Eight dead
fixture boards had accumulated in the live registry, and the `all` master was
listing them as members; all eight are cleared and the registry is back to its
ten real boards.  Reported, not fixed: `resources/board/serve.py` is another
PRD's footprint.

### 4. A lane's `pearde/wiki` is empty, so every worker's knowledge query lies — still open

Unchanged. There is a PRD for it —
`a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re`. The fix
belongs where lanes are made.

### 5. `pearde-all.md`'s description was over 1,024 characters on `main` — still a guard, still unmeasured

Unchanged. No harness in this tree enforces the length; `spec01.3` is a guard
against regrowth, and `REF=main` reddening it is the control working.

### 6. Pass two's findings 4 to 10 — still open, none touched

`prose.py stat` counting table pipes as words; `UNBOUND_FOLLOW` firing on
bound restrictive clauses; `resources/scout/README.md` naming a `SKILL.md`
that does not exist; `references/skills/pearde-machine.md` being an
unregistered stale duplicate; `references/personas/writer.md` missing from
disk. The last is still one of the two `index.py check` rows in the checkout.

### 7. Probe snapshots must be whole files, and are stale as soon as the base moves — reopened by the rebase

`probe/skills/` and `probe/scout/` were re-taken by pass four against base
`58c92e6`. This pass moved the base twice. The snapshots are still
byte-correct — nothing outside the footprint changed the files — but
`restore.sh` restores text taken against a base two rebases old, and the next
pass should re-take them rather than trust them. Not re-taken here: no reset
happened and re-taking them would be the only write this pass made to no
purpose.

### 8. A spec's `## What is left` can name work no implementer can reach — still open, now stale in both directions

spec01 says *"land the lane and re-run"* and spec02 names *"one sentence"* to
rewrite after `collect` merges. Both are done and both sections now describe
work that no longer exists. Reported, not fixed: the boxes are green and
rewriting a spec's prose is not this role's act.

### 9. `collect` dispatches an implementer onto a lane it has already sealed — still open

Pass five's finding 7, unchanged and now seen twice. Worth reading together
with finding 2: they are the same seam.

## Record

Nothing was learned outside this repo — every number here was measured in this
tree — so `knowledge.py remember` had nothing to take.

## Grammar

No undefined word hit.

## Questions

None. `prd.md`'s one question is answered, built and proved: the six rewritten
`description:` lines keep every trigger phrase and every backticked span
character-identical to `main`, which `spec01.2` measures and a mutation
reddens.

## Health

The brief named no footprint file under the health floor, and this pass
changed no file's content.

## Scores

complexity: 12
blast-radius: mid
workflow: probe-then-spec
