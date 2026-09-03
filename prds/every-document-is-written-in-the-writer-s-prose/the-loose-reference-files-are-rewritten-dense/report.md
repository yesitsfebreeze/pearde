# the-loose-reference-files-are-rewritten-dense — implementer report

Verdict: BLOCKED

**The wall: this PRD is dispatched twice, and the first worker is still
running.** A second `impl-loose-refs` implementer — Claude session PID 50577,
started `Wed Sep 2 21:27:39 2026`, the session holding the `claim:
impl-loose-refs 2026-09-02 20:40` on `prd.md` — is alive now and rewriting the
same fifteen `references/*.md` files in the same lane. This session stood down
rather than write into them.

**The question for the orchestrator:** which of the two runs owns this PRD?
No worker can answer it. Let session 50577 land, and read this report as a
collision notice, never as the PRD's outcome.

## How the collision was established

Three independent measurements, in order.

| evidence | showed |
|---|---|
| `md5 -q references/*.md` twice, 45 s apart | four of the fifteen changed content between `09:19:42` and `09:20:27` while this session wrote nothing |
| `ls -lT references/*.md` | thirteen of the fifteen carry an mtime inside the last ten minutes; `graph.md`, `knowledge.md` and `obsidian.md` all at `09:20:19` |
| `lsof +D <lane>` then `ps -o pid,ppid,lstart,command` | two live `zsh` polling loops, PIDs `47632` (started `09:16:01`) and `54191` (started `09:02:21`), both children of PID `50577` = `/Users/feb/.local/bin/claude --dangerously-skip-permissions` |

Both loops poll **this PRD's own ceilings**. `54191` runs `until … sys.exit(0
if ok else 1) … do sleep 45; done; echo "ALL FIVE GROUPS UNDER CEILING"` over
the exact five groups and the exact five numbers — `2621`, `1737`, `2531`,
`1611`, `2904` — that `spec01`–`spec05` assert. `47632` prints `remaining under
ceiling N/3` over specs `02`, `03` and `04`.

`prds/…/probe/rows.py` was rewritten under me mid-run — mtime `09:18`, between
my first block sweep and my second — from first-cell keying to
header-and-count keying. Its new docstring argues the case: keying a row by its
first cell fails a rewrite that tightens `more than 60 words in the fork` to
`over 60 words in the fork`, which keeps the row and loses the key. That is the
other session repairing its own probe, and it is why `spec02` went red to green
between my two sweeps with no byte of `drill.md` moving.

## Why not merge instead of stopping

`attempt-the-build`'s `## Fails when` covers *a patch's anchor text no longer
matches* — re-read, merge, keep the hunk disjoint. That row is one hunk against
one moved file. This is not that. Both workers perform the same contracted act,
a whole-file prose rewrite, on the same fifteen files toward the same five word
ceilings. A prose rewrite has no disjoint hunk: the compressible text is the
whole paragraph set, and two whole-file writes land last-writer-wins.
Continuing would have destroyed the other session's work with no way to tell
which sentences were lost, because a dropped sentence fails no command — the
analyst pass's own finding, *Facts get lost quietly*.

## State of the five specs at `09:21:39`

Measured with `python3 resources/prose.py stat ba69efa` in the lane, each
block run the way `collect` runs it — `bash -e -o pipefail -c "$(awk
'/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"`.

| spec | files | words / ceiling | block exit |
|---|---|---|---|
| `spec01` | `install.md` `system.md` `update.md` `plugins.md` | 2616 / 2621 | **0** |
| `spec02` | `drill.md` `report.md` | 1731 / 1737 | **0** |
| `spec03` | `memo.md` `workflow.md` `grammar.md` | 2973 / 2531 — over by 442 | 1 |
| `spec04` | `obsidian.md` `graph.md` `knowledge.md` | 1674 / 1611 — over by 63 | 1 |
| `spec05` | `settings.md` `health.md` `archive.md` | 2901 / 2904 | **0** |

Both reds are converging under the other session: `spec03` over by 466 at
`09:18` and 442 at `09:21`; `spec04` by 145 at `09:17`, 112 at `09:19`, 63 at
`09:21`. `spec03`'s other failure — `references/workflow.md: 4 unbound waste
word(s) (that)` from `prose.py check` at `09:17` — that session closed by
`09:18`, and `prose.py check references/*.md` in the lane is now silent on all
fifteen.

## What this session wrote

One file, disclosed rather than hidden: `specs/spec02.md`, seven boxes moved
from `- [ ]` to `- [x]`. The block exits 0 and every box is backed by a command
run here — but **the build behind those ticks is the other session's.** The
route's own rule is that a worker who only re-runs checks takes credit for a
neighbour's landing. Read those seven ticks as "verified green at 09:20", never
as work done here. Nothing else in the lane, the board or the checkout was
written by this session.

## Baseline, for the record

Taken before that single write.

| gate | root | result |
|---|---|---|
| `python3 resources/index.py check` | lane | exit 0, two inherited lines, neither in this footprint: `references/language.md references @references/personas/writer.md — not on disk` and `references/parts/commits.md references @pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md — not on disk` |
| `python3 resources/prose.py check references/*.md` | lane | silent, exit 0 |
| `git status --short` | lane | the fifteen footprint files, all ` M`, all the other session's |
| `git status --short` | checkout `/Users/feb/dev/infra/pearde` | ` M references/system.md` only |

Twelve board harnesses name a footprint path, and `grep -L PEARDE_ROOT` names
every one of the twelve — each computes its own root and measures the
orchestrator's checkout, never this lane. No count from that set can see this
PRD's build, and none is quoted as a flip here.

## Findings

The analyst pass's four are carried forward unchanged and unfixed — `prose.py`'s
mean-sentence-length check cannot fail on this tree; `prose.py` flags correct
prose as an unbound waste word; the standard fails its own check and its source
is a dangling address; a lane worktree does not contain the board. All four
belong to `a-density-checker-and-the-root-docs-are-rewritten`.

Two more, from this pass.

### The board double-dispatched one PRD onto one lane

`claim: impl-loose-refs 2026-09-02 20:40` names one worker id and two live
sessions answer to it. Nothing on the board says a claim is held by a running
process, so a second dispatch under the same id is indistinguishable from a
first. The lane makes it worse rather than better: both workers get the same
worktree, so the isolation a lane exists for does not apply between two holders
of one claim. A claim carrying a pid, or a lock file in the lane a second
dispatch would find, refuses this run in its first command instead of after
twenty minutes of measurement.

### `spec04`'s box prose names a "from" total that is not the tree's

`spec04`'s third box reads *sums the 3 files to 1611 words or fewer, from
2170*. At `ba69efa` those three files are 1407 + 366 + 626 = **2399**, and the
block's own `awk` prints `2399 -> …`. The ceiling, 1611, is what the block
asserts and is unaffected, so no check is wrong — but `2170` is a recollection
rather than quoted output, the shape `write-the-specs` warns about under *a
count in a box is quoted output, never a recollection*. The replacement text is
`from 2399`. It sits in a file the other session holds, so it is left for
whichever run lands.

## Workflow probe-then-spec

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | `read-the-contract` | passed | `prd.md`, five specs, the analyst `report.md`, `probe/rows.py`, `probe/tokens.py`; `git status --short` in lane, checkout and board recorded before any write |
| 2 | `capture-the-harness-baseline` | passed | all twelve footprint-naming harnesses fail `grep -L PEARDE_ROOT`, so all measure the checkout; the lane gates recorded instead |
| 3 | `attempt-the-build` | stopped | not entered — the build is another live session's and this one stood down |
| 4 | `re-run-the-harnesses` | passed | five blocks run twice under `bash -e -o pipefail`; three green, two red and converging under the other session |
| 5 | `write-the-specs` | passed | the specs exist; this is the route's second pass, so step 5 applied its `Fails when` table to the blocks that stand and authored nothing |

### Edits

**`probe-then-spec`** — `### 3 — attempt-the-build`, `## Fails when` — add this
row. The section's nearest row, *a patch's anchor text no longer matches a file
you read in step 1*, tells a worker to merge; it is written for one hunk and is
the wrong instruction when the neighbour performs the same whole-file act,
which is the case a lane cannot isolate because both workers hold one claim on
one worktree.

```
| the footprint files change content while you write nothing, and `lsof +D <lane>` names a live process that is not yours | this PRD is dispatched twice — a claim names a worker id and nothing on the board says the id is held by a running process, so a second dispatch is indistinguishable from a first, and a lane isolates nothing between two holders of one claim | `md5` the footprint twice a minute apart to prove the tree is moving, then `lsof +D <lane>` and `ps -o pid,ppid,lstart,command` on each pid **and on its ppid** — a `Monitor` loop is a child shell and the parent is the session. Where the loop's own text names this PRD's ceilings, the other session is on your contract: write nothing and report BLOCKED naming the pid and its start time. Merging is only for one hunk against one moved file; two whole-file rewrites of prose land last-writer-wins, and a dropped sentence fails no command |
```

**`probe-then-spec`** — `### 1 — read-the-contract`, `## Do` — the step's first
command should establish the claim is yours before anything is read, so the
collision above costs one command rather than twenty minutes:

```
0. `lsof +D <repo root>` and `md5 <footprint> && sleep 45 && md5 <footprint>`
   before `cat prds/<prd>/prd.md`. A footprint whose bytes move while you have
   written nothing is another live worker on your contract, and every
   measurement after it is taken against a tree somebody else is editing. Stop
   there — `attempt-the-build`'s `Fails when` names the shape.
```

## Scores

complexity: 37
blast-radius: mid
workflow: probe-then-spec
