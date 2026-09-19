---
state: open
origin: derived
priority: 55
repo: "/Users/feb/dev/cartridge"
footprint:
  - ".cartridge/memos/decision/the-trunk-checkout-is-a-landing-pad.md"
  - ".cartridge/memos/decision/gitfs-overlay-and-ship.md"
---

# The landing-pad decision describes this repository's lanes, not a checkout that no longer exists

## Outcome

`memo resolve` stops handing a worker instructions for a repository that is not
this one. The landing-pad decision either describes how work is isolated here —
PRD lanes cut by `prd claim`, record edits committed by path on the shared
checkout — or it is gone, and every memo that cites it is corrected in the same
change.

## Acceptance

- [ ] `.cartridge/memos/decision/the-trunk-checkout-is-a-landing-pad.md` names
      no path, command or `just` target that does not exist in this repository.
      One check proves it, by resolving each named command against
      `.cartridge/justfile` and each path against the working tree.
- [ ] The two hazards the memo exists to record survive the rewrite in some
      form: a `git add -A` on a shared checkout sweeping another session's
      in-flight edit into an unrelated commit, and uncommitted work being read
      as abandoned because mtime is the only available evidence.
- [ ] `.cartridge/memos/decision/gitfs-overlay-and-ship.md`, which cites this
      memo, still resolves and still says something true after the change.
- [ ] Every relative link in both files resolves. A link check over the whole
      record is landing separately (see Coordination) and will turn red
      otherwise.

## Evidence

Reported 2026-09-19 by cartridge-5c while analysing
`@root/the-isolation-gate-reads-the-composition-profile`, and confirmed here by
reading the file and the tree.

The Decision names `/Users/feb/dev/sys` as the trunk; that directory does not
exist on this machine. It names `just lane <name>`, `just land` and
`just lane-rm`; none is a target in `.cartridge/justfile`. Work here is isolated
by PRD lanes, which `prd claim` creates as
`git worktree add -b lane/<board>-<slug> <board>/.lanes/<slug> HEAD`, and which
`prd collect` removes.

What makes this more than an untidy file is the frontmatter: `status: accepted`
with `uses: [[read-usage]]` and a `when` of "Writing code or record while
another session may be working in the same checkout". Six sessions are in
exactly that situation continuously, so the resolver surfaces this memo
constantly, and what it hands them is a procedure for a layout that no longer
exists.

The reasoning inside it is not stale, which is why this is a rewrite rather than
a deletion. Its two recorded failures are the hazards this board still meets
daily, and PROMPT.md's rule that a shared checkout is only ever committed with
`git commit --only -- <paths>` descends from them.

## Coordination

`.cartridge/memos/decision/` is also touched by
`@root/the-shared-record-describes-only-this-repository/every-link-in-the-record-resolves-and-a-test-says-so`,
run by cartridge-5c, whose footprint names three decision memos —
`desktop-is-a-later-client-over-the-same-core.md`,
`the-terminal-grid-lives-in-pty.md` and
`the-agent-surface-preserves-the-visible-shell.md` — and none of this PRD's two.
This footprint therefore lists its files explicitly rather than claiming the
directory, so the two can run at once.

That sibling also lands a test that walks every link in the record. Whichever of
the two lands second must leave no unresolvable relative link behind.

Two citations live outside the footprint and are not this PRD's to edit:
`@runtime/an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one` and
cartridge-5c's own routines child. If the rewrite changes what those citations
mean, say so in the collection rather than editing another board's records.
