---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `compact` deletes every intake part it folds and the daemon runs it hourly-until-daily, but 162 of this clone's 272 intake parts are untracked — for those the model's condensed rewrite is the only copy, and git, the archive the frontier law names, has nothing to restore

## Do

`compact` (`src/commands/src/commands_compact.rs:95-190`) folds
`memos/intake/` by kind: it sends each batch to the reason model with the
claims carried from the previous batch, takes the model's answer as the new
claim set (`claims = next`, `:129`), writes one file per claim under
`memos/insights/<kind>/`, and then deletes every intake part it read
(`:168-171`) and every previously condensed file (`:146-149`). What the model
dropped between one claim set and the next is gone from the tree in the same
pass that dropped it.

`spawn_daily_compact` (`:72-93`) runs it from the daemon: a one-hour interval,
skipped only while `memos/insights/.compacted` names today, `dry_run: false`.
No operator confirms a run; the first hour after a fresh clone's midnight
rewrites the record.

The record's answer to destruction is `the-registers-collapse` — "`memos/`
the whole record, git the archive". Measured in this clone on 2026-09-06:

```
272   parts in memos/intake/
162   untracked (git status ??)  — no blob, no reflog, nothing to restore
 82   staged, added, never committed
 27   staged with further modifications
```

So the archive covers none of the 162 and only the index-state of the 109
staged ones. Five sessions write this record at once
(`the-parts-gate-is-red-in-both-directions`), each leaving its parts
uncommitted for the curator, which is exactly the population `compact`
deletes. A daemon that ran tonight would take every finding written today
that nobody committed, and the only trace would be whatever the model chose
to carry into a condensed claim.

Make the deletion safe rather than forbidding the fold:

1. Refuse to delete a part git does not have. `git status --porcelain` over
   `memos/intake/` before the fold, and skip (do not delete, do not fold) any
   path reported `??`; report the count as a line so the operator sees what
   was held back.
2. Make the daemon's automatic run `dry_run: true` — write the condensed
   files nowhere, log the plan — until a human has looked at one real
   `memory compact` output. The verb by hand keeps deleting, because the person
   typing it is the confirmation.

The mid-run failure is the second half and stays in this item because it has
the same fix site: a failed `complete` on the second kind returns `Err`
(`:120-122`) after the first kind's files were already deleted, and the index
rewrite (`:177-179`) never runs — so the tree is left with deleted parts whose
rows are still in `SYSTEM.md`. Do the deletions after the index write, not
before it.

## Acceptance
`memory compact --dry-run` in a clone holding one untracked intake part reports
it as held back and leaves it on disk; a `compact` run whose second kind fails
its completion leaves every part it read still on disk; and after a successful
run, `just memos-check` is green with no row naming a deleted file.

**Done 2026-09-06 by the session that owns the file, verified here against the
code rather than taken on report.** `archived_stems` (`:232-263`) runs
`git -C parts ls-files intake` and subtracts everything `git status
--porcelain -- intake` names, so a part that is untracked *or* modified since
its last commit is partitioned out and left in the intake for a later run
(`:106-111`). Every model call now completes into a `Fold` list before any
file is touched (`:129-171`), and only then does the write phase run
(`:176-215`), so a failed completion changes nothing on disk. The index write
and the body de-link follow the deletions (`:216-219`).

Read a second time by another session, which also probed the one edge that
looked fragile: a staged rename prints as `R  intake/old.md -> intake/new.md`,
and the guard's stem helper (`:248-252`) takes `Path::file_stem` of the whole
line, which is the segment after the last slash — the rename *target*. That is
the right exclusion, and the source name is already absent from `git ls-files`
once the rename is staged. The guard is also fail-closed: `archived_stems`
returns `Err` if git itself fails, which aborts the fold rather than treating
an unreadable repo as an empty one.

What is left is narrower than the item was: a filesystem error *inside* the
write phase — a failed `remove_file` or `write` — still returns before the
index is rewritten and leaves deletions behind rows. That is an I/O failure
rather than a model failure, and it is what [[the-first-compact-run-destroyed-25-parts]]
would have looked like had the fix been in place.

**Proven live 2026-09-06, on real state rather than a fixture.** `memory compact
--dry-run` against the installed binary reported "12 intake parts not committed
in memos/, left for a later run" and folded only the one remaining kind;
`git status --short intake/*.md` reported exactly 12 dirty or untracked of 13
files, four modified and eight untracked. So the guard selects the right set
and holds all of it back. A dry run returns before the write phase, so nothing
moved.

One thing it does not cover, found by another session reading the same file:
`STAMP` is read in `spawn_daily_compact` and nowhere else, so `memory compact`
typed by hand folds whatever the guard allows regardless of the day stamp and
then rewrites it. The stamp is a cadence for the daemon, never a block, and a
session that wrote today's date into it to stop a retry had not stopped
anything a person could type.

**The recovery inverts the same defect, seen 2026-09-06.** The write order was
fixed so the index stops naming a part before the part dies. A partial recovery
runs it backwards: 268 folded parts were restored from the index while their
rows stayed struck, so every one of them was alive with the record having
forgotten it — 388 parts in the scanned directories, 268 without a row. Neither
state is worse than the other and the gate reports both, which is what
"red in both directions" is for. It is also why a restore is not the inverse
of a fold: the fold writes files and rewrites the index, so undoing it means
undoing both, and the halves are held by different tools.
