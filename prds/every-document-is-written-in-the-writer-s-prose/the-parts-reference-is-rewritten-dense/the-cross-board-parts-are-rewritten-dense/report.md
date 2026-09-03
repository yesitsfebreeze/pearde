# the-cross-board-parts-are-rewritten-dense — implementer pass

Verdict: DONE

Three specs, fourteen boxes, all ticked against output quoted below. The build
was already in the tree and committed when this pass opened: `b17c06a` on
`lane/…-the-cross-board-parts-are-rewritten-dense` is also on the checkout's
`main`, so this is the route's **second** pass, and step 3 was entered for no
spec. What this pass did is step 5's `Fails when` table applied to the blocks
that already stood: one block could not pass, one box carried a stale count,
and both are repaired below.

This report replaces the analyst pass's report at the same path; its findings
are carried forward under `## Findings` by name.

## The two repairs

### spec01's word box was anchored on whichever PRD landed last

`spec01`'s block read the word baseline as `C=$(git log -1 --format=%H -- "$M")`
and compared `C^` against the working tree. `handles.md` is shared, and
`31620bb` — *board-commands-run-in-the-session-s-tree-not-the-checkout* —
widened its `session` row after the rewrite landed. `C` therefore resolved to
that neighbour's commit, `C^` to this PRD's own rewrite, and the block
measured the neighbour's 64-word paragraph against this unit's output:

    $ python3 resources/prose.py stat 31620bb^ | grep '^references/parts/handles.md: '
    references/parts/handles.md: 2113 -> 2177

`2177 <= 2113` is false, so the block exited 1 on a green tree. The rule the
box asserts did not move — the rewrite did cut. The anchor did.

Repaired by finding the rewrite commit by this PRD's slug in the log and
reading `prose.py stat` at that commit and at its parent, so the comparison
is two points in history no later row can move:

    R=$(git log --format=%H --reverse --grep=the-cross-board-parts-are-rewritten-dense -- "$M")
    set -- $R; R=$1
    was=$(python3 resources/prose.py stat "$R^" | awk -v m="$M: " '$0 ~ "^"m {print $2}')
    now=$(python3 resources/prose.py stat "$R"  | awk -v m="$M: " '$0 ~ "^"m {print $2}')
    [ "$now" -lt "$was" ]

`--reverse` with the first field taken by `set --` pins it to the **first**
landing of this PRD, so a later pass committing under the same subject cannot
walk the anchor forward. `spec02` carried the identical shape against
`ramp.md`, which no neighbour has touched yet — it passed by luck, and got the
same anchor.

The line is a live check, not a tautology. Against a commit that grew the file
it fails:

    R=b17c06a  2122 -> 2113  exit=0
    R=31620bb  2113 -> 2177  exit=1

### spec03's violation count was 2 and is 1

`spec03`'s fourth box says the block prints how many files under
`references/parts/` still violate, and named 2. A sibling closed one between
the analyst pass and this one:

    $ python3 resources/prose.py check references/parts/*.md
    references/parts/commits.md: 3 unbound waste word(s) (it, that)
    violating files under references/parts/: 1

The box now names the count and the file. The block already gated only on this
PRD's five files, so the count is printed and decides nothing.

## Per-spec box status

### spec01 — `handles.md`, 419 facts intact

| box | status | evidence |
|---|---|---|
| `prose.py check` silent, exit 0 | `[x]` | no output, block exit 0 |
| fact probe `0 lost` against `fc75bcf` | `[x]` | `419 -> 468 facts, 0 lost, 49 new` |
| no `fc75bcf` table row removed or reworded | `[x]` | the `grep -c` of removed row lines is `0` |
| the rewrite carries fewer words than the text it replaced | `[x]` | `references/parts/handles.md: 2122 -> 2113 at the rewrite` |
| `index.py check` names no dangling reference in the file | `[x]` | the gate's one red line names `references/language.md` |

Block exit 0. Mutation: `grep -v '^| one pass, then stop '` drops a row present
at the fact baseline — block exit **1**, `419 -> 464 facts, 4 lost`. Restored
by `cp` from a scratch dir outside the repo, `cmp` identical, block exit 0
again. A behavioural mutation, not a renamed string: it removes a fact.

### spec02 — `ramp.md`, 69 facts intact

| box | status | evidence |
|---|---|---|
| `prose.py check` silent, exit 0 | `[x]` | no output, block exit 0 |
| fact probe `69 -> 69 facts, 0 lost` | `[x]` | `references/parts/ramp.md: 69 -> 69 facts, 0 lost, 0 new` |
| the rewrite carries fewer words than the text it replaced | `[x]` | `references/parts/ramp.md: 1157 -> 1140 at the rewrite` |
| fenced blocks byte-identical to `fc75bcf` | `[x]` | the `diff` of the two fence extractions is empty |
| `index.py check` names no dangling reference in the file | `[x]` | the gate's one red line names `references/language.md` |

Block exit 0. Mutation: `happiness: 0` to `happiness: 1` inside the quoted yaml
— block exit **1**, `1 lost: happiness: 0`. `cmp` identical after restore,
block exit 0 again.

### spec03 — `machine.md`, `all.md`, `master.md` held green

| box | status | evidence |
|---|---|---|
| `prose.py check` silent, exit 0 on all three | `[x]` | no output, block exit 0 |
| fact probe `0 lost` on all three | `[x]` | `171 -> 171`, `91 -> 94`, `79 -> 79`, each `0 lost` |
| the rewrite is committed, `git status --short` names none of them | `[x]` | the emptiness test passes; `b17c06a` is on `main` |
| the block names none of the five, and prints the remaining count | `[x]` | `violating files under references/parts/: 1` — `commits.md` |

Block exit 0. Mutation: the `needs:` row dropped from `master.md` — block exit
**1**, `79 -> 73 facts, 6 lost`. `cmp` identical after restore, block exit 0
again.

Every block was run the way `collect` runs it —
`bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"` —
from the orchestrator's checkout, which is the root `collect` will use.

## Baseline and re-run

Taken from `/Users/feb/dev/infra/pearde` before the first edit of this pass,
re-taken after the last. Every harness naming a footprint path:

| harness | baseline | re-run |
|---|---|---|
| `one-page-that-says-whats-up` | `31 checks · 29 pass · 2 fail` | same |
| `a-parked-prd-comes-back` | `44 checks · 6 pass · 38 fail` | same |
| `the-board-runs-itself/vision-is-first-class` | `52/52 checks pass` | same |
| `the-board-runs-itself/readme-in-three-rings` | `75 checks · 70 pass · 5 fail` | same |
| `the-board-runs-itself/the-next-line-runs` | `96 checks · 94 pass · 2 fail` | same |
| `the-board-runs-itself/the-loop-is-commands` | `61 checks · 32 pass · 29 fail` | same |
| `workflows-on-the-board/workflow-skill` | `55 checks · 50 pass · 5 fail` | same |
| `…/skills-and-scout-docs-are-rewritten-dense` | `boxes 14/14` | same |

No count moved. Every failing harness above was failing **before the first
edit** of this pass, on lines naming files outside this footprint; none is
this unit's and none is claimed as a flip.

Repo gate, both times:

    python3 resources/index.py check   rc=1
    references/language.md references @references/personas/writer.md — not on disk

    bash resources/doctor.sh           rc=1
      origin      broken  34 derived · 2 with no from:
      knowledge   broken  graph.json is behind the files: 260902-4f91, 260902-aae0

All three red lines are inherited and outside this footprint.

`git status --short` in the checkout, both times: `M references/system.md`, a
neighbour's. `git status --short -- references/parts/` is empty at the end, so
the three mutation restores took.

No flip is claimed by this pass. The rewrite landed in `b17c06a`, which was on
`main` before this pass opened; the only files this pass wrote are the three
spec files and this report, all inside `prds/<prd>/`, and no harness in the set
reads them.

## Findings

### `prose.py stat` has no two-commit form

`stat [ref]` diffs one commit against the working tree and nothing else, so a
question about what an edit did to a shared file — the question every word box
in this PRD asks — is answered by calling it twice and reading field 2 out of
each. A `stat <a> <b>` form would make the anchor one expression instead of a
five-line preamble repeated in two specs. Outside this footprint, reported not
fixed.

### `references/language.md` references a persona that is not on disk

`python3 resources/index.py check` is red on `references/language.md
references @references/personas/writer.md — not on disk`, the only line the
gate prints. Carried forward from the analyst pass, still open, outside this
footprint. Every block in this set captures the gate and greps its own file out
of the output rather than letting the exit decide.

### `references/parts/commits.md` violates the density rule

`3 unbound waste word(s) (it, that)`. The last file under `references/parts/`
still red, owned by no PRD in this set. It was one of two; the other closed
between the analyst pass and this one.

### the volume filled mid-run

Between the baseline and the re-run every `Bash` call in this session returned
`ENOSPC: no space left on device` before the command started — `df` and `rm`
included, so the session could measure neither the disk nor free its own
scratch. Space came back on its own and step 4 completed. Recorded because the
next session to hit it will have no way to diagnose it from inside the harness.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass — `prd.md`, three specs, `git status --short` in both roots, `fc75bcf`, `b17c06a` and `31620bb` resolved |
| 2 | `capture-the-harness-baseline` | pass — eight harnesses plus `index.py check` and `doctor.sh`, quoted above, taken before the first edit |
| 3 | `attempt-the-build` | not entered — the build is committed on `main` at `b17c06a` and every spec's footprint is clean; the route's own second-pass row covers this |
| 4 | `re-run-the-harnesses` | pass — every count identical to its baseline, no harness edited |
| 5 | `write-the-specs` | pass as a second pass — no spec authored; the `Fails when` table applied to the three blocks that stood, two repairs made and quoted above |

### Edits

Two rows the atomics do not carry.

**`write-the-specs`, `Fails when`** — add:

| seen | means | do |
|------|-------|----|
| a spec's word or size box reads its baseline as `git log -1 -- <file>` and the file is shared across PRDs | `-1` names whichever PRD landed most recently, not the one the box is about — so once a neighbour lands, `<commit>^` is your own output and the box measures the neighbour's addition against it | anchor on the commit whose subject names **this** PRD, taken with `--reverse` so a later pass under the same subject cannot walk it forward: `R=$(git log --format=%H --reverse --grep=<slug> -- <file>); set -- $R; R=$1`, then compare `prose.py stat "$R^"` against `prose.py stat "$R"`. Measured here: `git log -1` gave `2113 -> 2177` and exit 1 on a green tree; the slug anchor gives `2122 -> 2113` and exit 0 |

**`capture-the-harness-baseline`, `Fails when`** — add:

| seen | means | do |
|------|-------|----|
| a `Bash` call fails with `ENOSPC: no space left on device` naming the harness's own output file, and `df` and `rm` fail the same way | the volume filled mid-run, and the tool writes each command's output file before the command runs — so no command can be issued, the cleanup that would free space least of all | do not retry in a loop: each retry writes another output file. Take the counts already recorded as the run's evidence, name the step the run stopped in, and name the files this run wrote so the next reader can bound it without re-running anything. Retry once after real work elsewhere; a shared volume often frees on its own, as it did here |

**A footnote for the mutation rule, not a row.** A behavioural mutation aimed
at a fact set must remove a fact **present at the fact baseline**. The first
attempt here dropped a table row that landed after `fc75bcf`, and the block
stayed green at exit 0 — correctly, since neither the fact diff nor the
removed-row count reads a row the baseline never held. A mutation that proves
nothing looks exactly like a check that cannot fail.
