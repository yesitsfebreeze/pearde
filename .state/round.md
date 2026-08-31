# round

**Everything last round owed as point 1 is done: committed and pushed, both
halves.** `main` carries the source tree at `3114ee8`; the board carries its own
history on the orphan branch `pearde` at `c624a16`, checked out as `.pearde/`
through a worktree. Working tree clean on both.

## how to resume

Read this file, then `python3 resources/pearde.py scan`. 56 PRDs, 13 open,
9 ready, nothing blocking, no question open. The page daemon is up and
watching this board — `pearde view status` says so.

## done this round

**Pushed, in three commits on `main`** (remote is
`https://github.com/yesitsfebreeze/pearde.git`; the history commits straight to
`main`, so the `merge PR N:` subjects are local merges, not a PR flow):

    7b88100  the board moves to .pearde/, and the knowledge layer lands
    3b829fd  skills/ and agents/ move under references/
    3114ee8  the board leaves the index — .pearde/ is ignored

The last one carried 245 `prds/*` deletions out of the index plus two session
artifacts that were gone from disk and never mentioned last round: `TODO.md`
and `improvements-report.md` — the second added in the previous commit and
deleted by another session. They are of the kind `/report*.md` and
`/handover.md` now ignore, so they went with the board.

**The orphan worktree stands.** `git worktree add --orphan -b pearde .pearde`
(git 2.55, so the modern form worked), board copied back in, first commit
pushed with `-u`. Both gates the plan named pass:

- `scan` from the repo root finds the board — 55 PRDs at the time, 56 now.
- `git status -sb` on `main` is `## main...origin/main` and nothing else.

`git worktree list` shows the two, and the temporary copy at
`../pearde-board-tmp` is deleted.

**What the board branch ignores**, decided against the disk rather than from
last round's note: `.claims/`, `.state/plan.json`, `.state/view.html`,
`graphify/`, `wiki/graphs/` and `wiki/board/`. Last round's note said the whole
of `wiki/` was regenerable; it is not — `wiki/sources/`, `wiki/conclusions/`,
`wiki/pending/`, `Dashboard.md` and `WORKFLOW.md` are the knowledge base and
are tracked. Only `wiki/board/` (a mirror of the PRDs) and `wiki/graphs/` are
written by a tool. `.state/round.md`, `history.jsonl` and `transitions.jsonl`
are tracked — the board's own record, which nothing rebuilds.

**The page daemon was restarted, on the user's word mid-round.** It was up on
the old registrations and did not know this board at all — every entry pointed
at some other repo's `prds/`. `view stop` then `view --no-open` registered
`pearde · /Users/feb/dev/infra/pearde/.pearde`. It was stopped again for the
worktree move and started after it. The other eight boards re-register on their
own next sync.

**One PRD added** — `the-guard-finds-the-board-the-way-the-scan-does`, p72,
last round's owed point 4 with its owed point 5 folded in (the guard's stale
`prds/.round.md` message belongs to the same file, not to the docs sweep).

## the user's instructions this round

1. **"resume the round."** Read as: the owed list, first point first. Done
   through the push and the worktree.
2. **"we also need to restart the page daemon."** Done, above.

## owed

1. **Run the loop.** The standing instruction from two rounds ago — create the
   PRDs, then use subagents — is now unblocked in full. Nine are ready:

       p80  init-writes-a-board-on-the-pearde-layout
       p75  every-document-names-the-path-the-board-is-on
       p72  the-guard-finds-the-board-the-way-the-scan-does
       p70  the-doctor-checks-the-path-a-board-is-on
       p65  the-vault-ignores-the-paths-the-board-writes
       p60  the-board-asks-for-itself/a-route-is-written-at-spec-time
       p60  the-graph-lands-inside-the-board
       p40  the-sweep-leaves-nothing-unregistered
       p0   the-knowledge-loop-runs-in-the-round

   The orchestrator dispatches `pearde-analyst` and `pearde-implementer` at
   loop steps 4 and 5 with `pearde brief <prd>` as the whole prompt — never by
   hand. Two are already `analyzing` and one of those has been silent since
   2026-08-29; `sweep` has not run this session.

2. **The manifest still names the old paths.** `references/files.md`'s
   `agents/` section and its two `@agents/...` rows, `index.md`'s `@@workers`
   row, `references/parts/workers.md` in prose, and nothing registering
   `references/skills/`. `pearde index` is loud until
   `every-document-names-the-path-the-board-is-on` runs. Expected, named in
   that PRD's body, not a regression.

3. **Sweep for more relayout misses.** Two `os.path.join(board, ...)` calls
   that should have been `prds_dir(board)` have been found in two different
   files (`init.py`, then `transitions.py` `add()`). Assume a third.

4. **The workflow finding on `.history.jsonl` vs `.transitions.jsonl`** is
   still unread. It lives in `the-sweep-leaves-nothing-unregistered`, whose
   body carries the path to the output file.

5. **4.9M of vendored Obsidian plugin bundles are now in `main`** —
   `resources/board/obsidian/plugins/dataview/main.js` (1.2M) and
   `obsidian-local-rest-api/main.js` (3.6M). Deliberate as far as this round
   can tell: the vault template opens with nothing to install. Nobody has been
   asked whether that is the trade they want, and a clone pays it forever.
   Worth a memo or a submodule, not a silent decision.

## still true, and easy to forget

Several sessions write this board. Check whether a file is already changed
before assuming an edit is yours — two of last round's directory moves had
already been made elsewhere. One git identity, one writer per file, never
amend a HEAD that is not yours.
