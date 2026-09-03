# scout's research leaves the tree — analyst report

Verdict: SPECCED

Two specs, `complexity` 12 + 8 = 20, under both board limits. `spec01` is
already green in the lane; `spec02` is proved in a scratch copy of the wiki and
is what an implementer still has to do.

- `specs/spec01.md` — `resources/scout` holds only tool files, and every
  document that named a departing file names its new home
- `specs/spec02.md` — the 1,847 lines land in the board's wiki as notes and
  attachments, and the four wiki citations that named the old paths resolve

Union of the footprints:

```
resources/scout
references/files.md
references/knowledge.md
references/plugins.md
references/skills/pearde-scout.md
index.md
.pearde/wiki/sources/scout
.pearde/wiki/conclusions/scout
```

`resources/scout` is named as a directory because spec01 writes 13 of the 16
paths under it. Both other PRDs whose specs name a path in this union —
`the-loose-reference-files-are-rewritten-dense` (`references/plugins.md`) and
`skills-and-scout-docs-are-rewritten-dense` (`resources/scout/*`) — are `done`,
so nothing live clashes.

## What the build did

Followed `probe-then-spec`. The knowledge query ran first and hit 90 notes, 86
strong — no gap, so nothing enqueued into `pending/`.

The lane already held a first pass: the nine research files staged as deletions,
`snapshots/README.md` added, and `index.md`, `references/files.md`,
`references/knowledge.md` and `references/plugins.md` rewritten. That pass left
the tree inconsistent, and this pass finished it:

- `resources/scout/README.md` — four layers cut to two. The `curate` and `wire`
  layers went with the files they described; the research loop's index two is
  now `knowledge.py remember` / `conclude` / `enqueue`, matching what the first
  pass had already written into `references/knowledge.md`.
- `resources/scout/routes.md` and `resources/scout/buckets.txt` — no longer
  cite `findings.md`.
- `references/skills/pearde-scout.md` — the description no longer advertises
  the reading list, the quality gates, `/scout reading`, `/scout quality` or
  "wire the quality gates".

`python3 resources/index.py check` prints the same four lines it printed before
the pass, none naming `resources/scout`. `resources/prose.py check` is silent
on both rewritten scout documents. `doctor.sh` reports the same rows as the
baseline, `skills ok · 19 well-formed` included.

The move itself was run against a scratch copy of `.pearde/wiki`, never the live
board. `probe/move-to-wiki.sh` is that run, left in the tree: it copies the live
wiki to a scratch directory, reads the departing files out of git history, writes
the two research indexes as `sources/scout/` notes and the five configs and two
TSVs as `sources/scout/attachments/`, rewrites the four citations as wikilinks,
then relinks. `knowledge.py doctor` goes from one problem to `doctor: clean`, and
`query "which tool won recursive search over a source tree"` returns the moved
index among its hits. Re-run it against the lane and it still passes.

Spec01's verify block was proved falsifiable: appending `<!-- see findings.md -->`
to `routes.md` makes it exit non-zero at the second command. Reverted.

## Findings

**The advertised verb goes with the files.** `templates/` was the only material
behind `/scout quality` and "wire the quality gates", and `reading-list.md` the
only material behind `/scout reading`. Leaving those triggers in a shipped skill
description after the files go is a claim that cannot be met, so spec01 removes
them. This is the contract's consequence, not a widening of it — but it does
retire a verb a user could have been using, and it is worth the person knowing.

**The board's wiki is the same GitHub repository.** `.pearde/` is its own git
repo whose `origin` is `github.com/yesitsfebreeze/pearde.git` — the same remote
as the code repo, on the `pearde` branch. So the destination this build could
actually reach takes the research out of the shipped tree but leaves it in the
same public repository under another branch. The PRD's other option, "a separate
repo", names no path the build could resolve, and inventing one would have been
a guess about the author's other project. If leaving the repository was the
intent rather than leaving the tree, spec02 is the wrong destination and the
right one is a path only the author can name.

**Measured, about the wiki as a destination.** A `.md` file dropped into
`wiki/sources/` with no frontmatter reddens `knowledge.py doctor` with
`<name>: no frontmatter`; the same file with a `type: source` fence is accepted
and only leaves `graph.json` behind until `relink`. Files under a subdirectory
that are not `.md` are not scanned at all, which is why the configs and the TSVs
go to `attachments/` and the two indexes do not.

**Four wiki notes cite paths that are about to vanish.**
`sources/scout/260831-2cdf.md`, `260831-3e48.md`, `260831-cbe9.md` and
`conclusions/scout/scout-feeds-knowledge-knowledge-feeds-the-rou.md` each name
`resources/scout/findings.md` or `reading-list.md`. They live in the board repo,
not the code repo, which is why spec02 has a board footprint and spec01 does
not.

**A wrong claim outside this scope.** `references/knowledge.md` says every verb
takes "`--root` per board". It does not: `--root` is the **wiki** directory —
`store.root / "sources"`, `store.root / "WORKFLOW.md"` — and argparse rejects it
after the verb, so `knowledge.py doctor --root <board>` fails twice over, once
on placement and once on the level. Three probe runs were lost to this. Not
fixed here; no spec of mine owns that file's prose.

**A defect outside this scope.** `resources/index.py check` carries four
problems at HEAD that no scout change touches: `resources/common.py` has no row
in `references/files.md`; `references/files.md` and `@@view` both name
`@resources/board/hotreload-test.js`, deleted in `b1d3f5d`; and
`references/parts/commits.md` references a memo that is not on disk. The
container PRD's `done` wants `index.py check` clean, so these belong to some
sibling or to nobody.

**The PRD's arithmetic checks out.** The departing files are 1,847 lines at
HEAD, which is the PRD's "1,900".

## Scores

complexity: 20
blast-radius: mid
workflow: probe-then-spec
