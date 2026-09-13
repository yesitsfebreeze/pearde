---
kind: work
level: 10
status: done
description: the watcher's ignore check tests only the path itself, so a directory pattern never covers what is inside it and `memos/.obsidian/` is in the graph
read_when: "judging whether the watcher honours a directory rule"
---

# ignored-directories-keep-their-contents-out

Done 2026-09-06, but not where the first note said. `9b0862e9` landed the boot
walk and the `is_ignored_dir` split; it did not change the matcher — `git show
9b0862e9:src/util/src/watcher.rs` and HEAD both still read `g.matched(rel,
is_dir)`. The matcher change is separate: both calls now ask
`matched_path_or_any_parents(rel, is_dir)`, so a directory pattern covers what
is beneath it on the event path and on the walk alike. It passes the caller's
`is_dir` rather than the `path.is_dir()` the Do names, because that is a
syscall per check and answers false for a deleted directory, which would
change what `is_ignored_dir` means on a Deleted event.
`gitignore_patterns_match_relative_to_root` carries the missing half and was
checked in both directions — red against `matched`, green against
`matched_path_or_any_parents`.

What already leaked is gone: `memory forget --source
"file://Users/feb/dev/memory/memos/.obsidian/workspace.json"` removed 20 thoughts
and 131 edges on 2026-09-06, dry-run first, and a second dry-run matches
nothing. The daemon holding the writer lock was stopped for it and brought
back.

The other half of the same incident, nested `.gitignore` files never being
read, is not closed and stays with [[@prd/work/memory--keep-agent-worktrees-out-of-the-record.md]] —
and that half is the larger one: `workspace.json` was 20 rows against the
thousands a worktree under `memos/.claude/worktrees/` put in.

## Do

`IgnoreRules::is_ignored` (`src/util/src/watcher.rs:136` and `:141`) asks both
matchers `g.matched(rel, false)`. `Gitignore::matched` weighs the path against
the patterns and nothing else — the crate's own contract points a caller who
needs parent directories at `matched_path_or_any_parents`. So a trailing-slash
pattern matches the directory and never a file beneath it: `memos/.gitignore`
carries `.obsidian/`, the watched root is `memos/`
(`the-watcher-watches-parts`), and the store holds 14 revisions of
`memos/.obsidian/workspace.json` — a file Obsidian rewrites on every pane move.
Measured in the 2026-09-05 21:49 export, where it is the only leak, because it
is the only frequently-written file under an ignored directory.

Replace both calls with `matched_path_or_any_parents(rel, path.is_dir())`. Then
remove what is already in:
`memory forget --source "file://Users/…/memos/.obsidian/workspace.json"` — the
object_id has no leading slash (`watched-file-paths-lose-their-root`), so
`--dry-run` first and read the count back before removing.

The gate that should have caught this tests the wrong side.
`gitignore_patterns_match_relative_to_root`
(`src/util/src/tests/watcher_test.rs:71`) writes `target` to a `.gitignore` and
asserts `is_ignored(root/target)` — the directory itself, never a path under
it. Extend that test rather than adding a new one.

## Check

`cargo test -p util watcher` — the extended test asserts
`is_ignored(root/"target/debug/app")` is true with `target` as the only pattern,
and goes red against the current `matched(rel, false)`.
