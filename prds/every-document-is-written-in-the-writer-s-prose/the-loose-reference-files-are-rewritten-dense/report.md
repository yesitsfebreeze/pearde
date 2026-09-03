# the-loose-reference-files-are-rewritten-dense — implementer report

Verdict: DONE

Five specs, 35 acceptance boxes, all ticked. Every `## Verify and Proof` block
exits 0 under `bash -e -o pipefail`, run the way `collect` runs it.

Fifteen files, 14,538 -> 11,396 words — a 21.6% cut with no backtick-quoted
token, fenced line, `@`-address or table row lost.

| spec | files | words | ceiling |
|---|---|---|---|
| `spec01` | `install.md` `system.md` `update.md` `plugins.md` | 3134 -> 2614 | 2621 |
| `spec02` | `drill.md` `report.md` | 2296 -> 1737 | 1737 |
| `spec03` | `memo.md` `workflow.md` `grammar.md` | 3318 -> 2531 | 2531 |
| `spec04` | `obsidian.md` `graph.md` `knowledge.md` | 2399 -> 1611 | 1611 |
| `spec05` | `settings.md` `health.md` `archive.md` | 3389 -> 2901 | 2904 |

Per file: `archive` 660->473, `drill` 1686->1196, `grammar` 1038->805, `graph`
366->316, `health` 1037->963, `install` 1704->1519, `knowledge` 626->472,
`memo` 1074->820, `obsidian` 1407->823, `plugins` 421->336, `report` 610->541,
`settings` 1692->1465, `system` 505->427, `update` 504->332, `workflow`
1206->906.

`git diff --stat -- references/` is 15 files changed, 776 insertions, 1039
deletions; `git diff --name-status` is 15 `M` lines and nothing else — none
renamed, none deleted, none split.

## Verification

Every command below run from the lane, with the base pinned to `3b4114d`.

| check | result |
|---|---|
| `prose.py check` over all 15 | silent, exit 0 — the 36 unbound waste words at the base are gone |
| `probe/tokens.py 3b4114d` over all 15 | silent, exit 0 |
| `probe/rows.py 3b4114d` over all 15 | exit 0 — no table and no row lost in any file |
| the five `## Verify and Proof` blocks | exit 0, 0, 0, 0, 0 |
| `index.py check` | 1 problem, inherited, outside the footprint |
| `memos.py check` `workflows.py check` `grammar.py check` | silent, exit 0 each |

**Blocks proved able to fail.** A block that cannot go red is not evidence, so
each kind of check was mutated on a scratch-backed copy and restored with
`cmp`:

| mutation | block exit | what it proves |
|---|---|---|
| a uniquely-occurring backtick token unquoted in `memo.md` | 1 — `1 lost: 'invariant'` | the token counter is wired |
| a table row deleted from `memo.md` | 1 — `1 row(s) gone` | the row check is wired |
| a sentence added to `workflow.md`, pushing the group over its ceiling | 1 | the block **detects a regression** — a computed number, not a string |
| a doubly-occurring token unquoted (`superseded`) | 0 | honest limit, recorded below |

Restores proved: `cmp <scratch>/<name>.bak <file>` clean in every case, and
the block back to exit 0 after each.

## What the specs' own blocks could not do, and now can

The specs stood before this pass. Three of their checks could not have failed
as written, so they were re-aimed — never weakened — and the report says so
rather than letting a tick imply evidence that was not there.

**1 — `collect` runs the block after the merge, so `HEAD` is the wrong ref.**
`land_lane` commits the lane and merges it, and only then does step 2 run each
`## Verify and Proof` block in the checkout. By then `tokens.py HEAD` compares
the merged file against itself and passes vacuously, and `git diff` is empty.
Both refs are now pinned to the pre-rewrite commit, which stays reachable
after the merge, so the check runs against the tree that does **not** hold the
build. The `git diff --name-only ... = N` count I first wrote has the same
flaw in reverse — it is only true before the merge — so it is now
`[ -f <path> ]` per footprint file, which is what "none renamed, none deleted"
actually asserts and holds on both sides of the merge.

**2 — the `index.py check` line could never fire.** Each block ended

```sh
python3 resources/index.py check | grep -E 'references/(...)\.md' && exit 1
```

`index.py check` exits 1 on inherited dangling references, so under `pipefail`
the pipeline carries **1** whether or not `grep` matched, the `&& exit 1` tail
was dead, and the check could not fail. Replaced with capture-then-grep, a
guard refusing a producer that dies silently, and the grep inside an `if`, so
the exit is decided only by lines naming this footprint.

**3 — the row box was backed by a command that cannot measure it.** The box
asked that `git diff -- <files> | grep -c '^-|'` equal "the count of rows
deliberately merged". A *re-worded* row shows as one removal and one addition,
so that count is the number of rows touched, never the number lost. Written
`probe/rows.py` instead. Two stricter keys were tried first and both
false-positive on the real rewrite:

| key | false positive |
|---|---|
| row keyed by its first cell | `more than 60 words in the fork` -> `over 60 words in the fork` — same row, three flagged in `drill.md` |
| table keyed by its header row | `why it fits pearde` -> `why it fits`, `why reject` -> `why` — same table, two flagged in `plugins.md` |

It settles on what the constraint says: per file the table count and the row
count may rise and may never fall. It does not catch a row swapped for a
different row of the same shape; `tokens.py` covers the backticked half of
that and the rest is read.

## The probe defect that was pinning 617 words

`probe/tokens.py` paired backticks with a naive one-backtick regex.
`references/workflow.md` carries one line using markdown's double-backtick
escape for a literal backtick — the `atomic` slug line in its steps grammar.
That leaves one backtick unpaired, and because `tokens()` joins every body
line before matching, the offset **inverted every code span after it** — 49
stretches of ordinary prose were held character-identical as though they were
commands, pinning 617 of `workflow.md`'s 1206 words and putting `spec03`'s
ceiling out of reach. The spec03 rewriter found it, reported the group as
unreachable at 2887, and was right.

`spans()` now implements the CommonMark rule: a run of N backticks opens a
span, the next run of exactly N closes it. On that line it now yields the
`atomic` slug and the escaped literal, where before it yielded two stray
spaces and left a backtick dangling.

The corrected check passes on all fifteen files, so nothing any rewriter did
was a real loss — and it still fails on a genuinely dropped token. With the
tail unfrozen `workflow.md` went 1128 -> 906 and the group closed at 2531.

## Four cross-file pinned phrases restored

Re-running the harnesses caught four needles into `drill.md` and
`workflow.md` going red. In every case the **rule was intact** and only the
literal wording had moved — but `prds/workflows-on-the-board/workflow-seed`
names two of them "the carried obligation ... the four named sites carry the
settled reading", so they are contract across files in the same way a refusal
string is, and the rewrite should have kept them. Restored inside the
footprint rather than left red:

| file | phrase | harness |
|---|---|---|
| `drill.md` | `second entry point` | `two-questions-start-a-drill` |
| `drill.md` | the attach sentence naming `workflow: <slug>` on that child | `workflow-attach` |
| `workflow.md` | `one collect, one count` | `workflow-seed` |
| `workflow.md` | `not the traversals inside one` | `workflow-seed` |

Restoring cost 5 words and put `spec03` one over its ceiling; one redundant
word came out of `grammar.md` (`on the transition that introduces the word` ->
`on the transition introducing the word`) to land at exactly 2531. Both
harnesses are back to their baselines: `workflow-attach` 44/47,
`workflow-seed` 65 pass, 7 fail.

## Harnesses

Twelve board harnesses name a footprint path; all twelve were baselined before
the first edit of this pass and re-run after, with `PEARDE_ROOT` set to the
lane both times. Ten are byte-identical to their baseline. Nine of the twelve
were **already failing before the first edit** and are recorded as inherited.

Two moved, neither mine:

| harness | base | now | why |
|---|---|---|---|
| `two-questions-start-a-drill` | 24 pass, 1 fail | 23 pass, 2 fail | `questions.py check` sweeps the whole board; the untracked sibling PRD `resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule` carries `## Answers` with no `## Questions`. `git status` shows it untracked and it appeared mid-run |
| `workflow-skill` | 49 pass, 6 fail | 45 pass, 10 fail | all four name `SKILL.md`, `skills/` or a `/private/var` realpath — every one explained by commit `0ed24e1 every-link-resolves`, which moved `skills/` to `references/skills/` and gave `install.sh` a `pwd -P` |

Neither harness reads a file in this footprint. Cited for the first:
`.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md` —
the repair is owed to that harness's own PRD, not to this one.

**A count that went up, and is not mine.** `index.py check` was 2 problems at
baseline and is 1 now: the `references/language.md` reference to a missing
writer persona is gone, closed by commit `0ed24e1` ("the dead writer persona
ref goes"), not by this unit. That also closes half of the previous pass's
third finding.

`doctor` rows against baseline: `index` 2 -> 1 problem (the sibling's flip
above); `board` 142 -> 148 PRDs; `origin` 33 derived / 1 without `from:` ->
36 / 4; `health` ok -> broken; `questions` ok -> broken. None is this unit's.
The `health` row names four files a sibling deleted —
`references/parts/machine.md`, `references/skills/pearde-machine.md`,
`resources/board/hotreload-test.js`, `resources/board/machine.py` — and no
file in this footprint. `knowledge` was broken before the first edit and is
broken now, unchanged.

## The board moved under the run

Mid-run the board directory was renamed `pearde/` -> `.pearde/` (previously a
symlink to `pearde/`, now the real directory) by the sibling PRDs
`board-commands-run-in-the-session-s-tree-not-the-checkout` and
`every-link-resolves`. Every lane worktree moved with it, so
`<board>/.lanes/<slug>` briefly resolved to nothing and `prose.py stat`
aborted mid-stream on a tracked file a sibling had deleted. No work was lost —
the lane is intact at the new path with all fifteen files modified — but a
worker holding an absolute lane path across a rename sees its tree vanish, and
the first reading of that is "my uncommitted work is gone". `git worktree
list` is what answers it.

The lane was also cut off a **stale** HEAD twice and was fast-forwarded twice,
before the first edit and again at the end:

- at the start it was 33 commits behind, with `memo.md` and `obsidian.md`
  already moved in `main`;
- at the end it was 3 commits behind, with `install.md` and `system.md` moved
  by `every-link-resolves`.

For the second, my rewrites of those two were saved to scratch, the two files
put back to lane `HEAD` with `git show HEAD:<path> >`, the lane
fast-forwarded, and the rewrites restored **with the sibling's rename folded
in** — six backticked `skills/` tokens became `references/skills/`, and the
`system.md` heading became `## Pearde`. So the merge carries both changes and
neither side's work is dropped. `git show HEAD:<path> >` was used in place of
`git checkout --`, which the new invariant
`no-destructive-git-runs-in-a-tree-the-session-does-not-own` refuses.

Because that rename touched two footprint files, the specs' pinned base moved
from `ba69efa` to `3b4114d` and every check above was re-run against it.

## Findings

The previous pass's four findings, carried forward by name, then what this
pass added. None is fixed here except the one in this PRD's own probe.

### `prose.py`'s mean-sentence-length check cannot fail on this tree

Carried forward, unchanged and still true. `sentences()` splits each *line* on
sentence punctuation, and every file here is hard-wrapped near 78 columns, so
one sentence counts as three or four short ones. All fifteen files score far
under the limit of 24 and no realistic file can reach it. The check is inert.
`resources/prose.py` belongs to
`a-density-checker-and-the-root-docs-are-rewritten`.

Measured again this pass: the rule never fired once across fifteen full
rewrites, including `obsidian.md` losing 41% of its words.

### `prose.py` flags correct prose as an unbound waste word

Carried forward, unchanged. `unbound_hits()` matches `it`/`this`/`that`/`there`
followed by a linking verb, which is also a relative clause and an adverbial,
both correct. Confirmed again this pass at scale: the rewriters cleared 36
flagged hits across ten files and several were relative clauses reworded only
to satisfy the regex, costing words the rule in `@references/language.md` does
not ask for.

### The standard fails its own check, and its source is a dangling address

Carried forward, **half closed by a sibling**. The dangling writer-persona
address is gone as of commit `0ed24e1` — not this unit's doing.
`references/language.md` failing its own `prose.py check` on an unbound waste
word is unverified this pass; `language.md` is outside this footprint and was
not read for it.

### A lane worktree does not contain the board

Carried forward and now **wrong in its particulars**, which is worth more than
the original. After the rename the lane sits at `<board>/.lanes/<slug>` where
the board is a real `.pearde/` directory, and from a lane root `../..`
resolves to the board. Every spec block here opens by resolving `../..` and
falling back to `.pearde`, and both arms now work — the fallback because the
checkout root has a real `.pearde/`. The finding should be re-read as: a lane
holds no board *of its own*, and a block must resolve one rather than assume
it.

### New — a "row survives" box cannot be backed by a diff line count

Written up under **What the specs' own blocks could not do**. The repair is in
this PRD (`probe/rows.py`), but the same box shape is likely in the sibling
rewrite PRDs' specs, where it is equally unable to measure what it claims.
Worth a sweep across
`every-document-is-written-in-the-writer-s-prose`'s other children.

### New — a set-based token check misses a duplicated token

`probe/tokens.py` compares *sets*, so unquoting one of two occurrences of the
same token leaves the set unchanged and the check silent. Measured: unquoting
`superseded` in `memo.md` (present backticked twice) left the block at exit 0;
unquoting `invariant` (present once) failed it. Making it a multiset would
flag every deliberate de-duplication a dense rewrite performs, so the trade is
deliberate — but a reader should not take a silent `tokens.py` as proof that
every *instance* survived.

### New — an `@` address carries its trailing punctuation

`AT` matches an address plus any trailing full stop, so `@index.md.` at the
end of a sentence is one token, and re-punctuating around it reads as a lost
address rather than a changed one. Correct for a strict probe — the sentence
is the address's only delimiter — and now named in the probe's docstring so
the next reader does not put a fact back that was never gone.

## Workflow probe-then-spec

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | `read-the-contract` | passed, passed | run twice — the contract's base moved when a sibling renamed the board directory and changed two footprint files mid-run; both reads named above |
| 2 | `capture-the-harness-baseline` | passed | 12 harnesses naming a footprint path, `index.py check`, `doctor`, and per-file word counts, all recorded before the first edit of this pass; 9 of the 12 already failing and recorded as inherited |
| 3 | `attempt-the-build` | passed | second pass on this route: the analyst had built `install.md` and `archive.md`, and the remaining thirteen files were entered here. Edits are in place in the footprint files, not staged under `probe/` — a prose rewrite has no meaning outside the file it lives in |
| 4 | `re-run-the-harnesses` | failed -> 3, passed | four needles into `drill.md` and `workflow.md` went red; back-edge taken once, the four pinned phrases restored, both harnesses back to baseline |
| 5 | `write-the-specs` | passed | specs already existed; this pass applied the `Fails when` table to the blocks that stand — three re-aimed checks and one new one, all above |

### Edits

**probe-then-spec** — `### 4 — re-run-the-harnesses` -> `#### Fails when` —
add the row below. The section has a row for a needle re-wrapped across a line
and a row for a needle whose sentence the contract deleted, and neither covers
the commonest case in a rewrite PRD: the sentence is still there and still
says the same thing, in different words. Left to the two existing rows a
worker either leaves four honest checks red or edits a neighbour's harness,
and both are wrong.

| a needle fails on a sentence you re-worded, and the rule it asserts is intact in the new wording | the phrase is contract across files, not prose — another PRD's harness pins it the way a refusal string is pinned, and a rewrite is content-only | restore the literal phrasing inside your own footprint and say so; do not edit the neighbour's harness, and do not leave it red. Where the harness names the phrase as a carried obligation across several files, that naming is the tell. Re-check any ceiling the restored words push you over, and take the words back out of prose that is genuinely redundant |

**probe-then-spec** — `### 5 — write-the-specs` -> `#### Fails when` — add the
row below. Step 5 tells you to run each block the way `collect` runs it, and
step 3's table tells you `land_lane` commits the lane before the merge, but
nothing says the block runs **after** that merge — so a block written against
`HEAD` or `git diff` passes for the author and is vacuous for `collect`.

| a block compares the working tree against `HEAD`, or asserts on `git diff`, and passes in the lane | `collect` merges the lane first and runs the block second, so by then `HEAD` holds the build and `git diff` is empty — `git show HEAD:<file>` is the built file, and every such check passes vacuously or fails on an empty diff | pin the ref to the pre-build commit (`git rev-parse --short HEAD` before the first edit) and spell it literally in the block; it stays reachable after the merge. Assert existence (`[ -f <path> ]`) rather than a `git diff` line count, which is only true before the merge. Re-pin when the base moves and re-run every check against the new one |

## Scores

complexity: 37
blast-radius: mid
workflow: probe-then-spec
