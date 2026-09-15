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

# an agent worktree inside the watched root was ingested — 2,911 entities of cargo build output in twelve minutes — because no ignore rule names it and nested .gitignore files are never read

## Do

**This fired on 2026-09-05 and is not hypothetical.** `memory audit` found 20
empty-content thoughts scored 1.00 delete, sourced from
`memos/.claude/worktrees/wf_d81be6e5-d59-1/target/debug/` — cargo `.lock` files
and `build/*/stderr`. The hub registry recorded this root going from 6,179
entities / 156 MB at 23:44 to 9,090 / 213 MB at 23:56
(`the-hub-registry-is-the-machine-inventory`): roughly 2,911 entities of build
output in twelve minutes, while a test run churned `target/` inside the watched
root. The worktree was removed when its workflow finished; the entities were not.

`memos/.claude/worktrees/wf_d81be6e5-d59-1` was a git worktree of the parts repo
— 27,883 files, 3.5 GB, carrying a full copy of the source tree — living inside
the watched root (`the-watcher-watches-parts`).
`git -C parts check-ignore` exits 1 for a file in it: `memos/.gitignore` names
`.DS_Store`, `.obsidian/` and `.memory/`, and nothing names `.claude/`. Add it,
which is one line — but no ignore file stops this on its own, and both reasons
are code:

`IgnoreRules::from_roots` built one matcher per watched root,
`build(&root, ".gitignore")`, and never read a `.gitignore` deeper in the tree.
Git honours nested ignore files; this did not. The worktree carried the memory
repo's own `/target` rule and it was never consulted. **Closed 2026-09-06**:
`RootRules` caches a `Mutex<HashMap<PathBuf, Vec<Gitignore>>>`
(`src/util/src/watcher.rs:60`) built lazily per directory, and `ignored` walks
root-to-parent asking each one, held by
`a_nested_ignore_file_governs_its_own_subtree`
(`src/util/src/tests/watcher_test.rs:120`).

And a rule naming the directory would not fire anyway until
[ignored-directories-keep-their-contents-out](../ignored-directories-keep-their-contents-out/prd.md) lands, because
`matched(rel, false)` matches the directory and never a file inside it. Either
fix alone leaves the other hole open.

Removing what was ingested had no bulk path, and that was the third thing to
fix. **Closed 2026-09-06**: `forget_by_source` takes a `prefix: bool`
(`src/graph/src/graph_ops.rs:142`) wired through the tool, the router and
`memory forget --source ... --prefix`. The cleanup ran the same day — 11,222
thoughts and 22,503 edges in 3.7 s, the store going 14,744 to 3,557 entities —
and cost a defect of its own: `memory doctor`'s dangling reason edges went 110 to
910 (`an-edge-lives-in-one-memory-so-removal-scans-them-all`). A second identical call still
found one row, and by 01:05 the store was back to 10,038 thoughts with nobody
ingesting: the removal was not re-ingested, it was undone
(`a-refused-flush-undoes-another-writers-removals`). The hub merge was named
here first and is wrong — it has no periodic caller.

The reason this went unseen was the disagreement behind it: the record's gate
and the record's watcher did not mean the same thing by "inside `memos/`".
`all_md` skipped any directory whose name starts with `.`, so the copies of the
record's own `.md` files inside that worktree never reached the link check —
which is why `just memos-check` was green with two of every part on disk, while
`IgnoreRules` walked in. **Closed 2026-09-06**: `all_md` (`tests/memos_index.rs`)
builds `IgnoreRules::from_roots` over `memos/` and asks `is_ignored_dir` /
`is_ignored`, so the gate and the watcher are one rule rather than two that
agree.

**The removal did not stick, found 2026-09-06 09:05.** The three legs above are
about *preventing* and *reaching*; none of them makes a removal survive. An
export read at full path depth finds **7,498 of 9,025 `Source::File` rows still
naming `memos/.claude`** — 62% of the store
(`the-worktree-rows-are-still-in-the-graph`). The 11,222 rows this item
records removing came back, by a refused flush absorbing disk rows
(`a-refused-flush-undoes-another-writers-removals`) or by the parked captures
replaying before they were swept, and nothing marks a reverted removal. This
item's fixes hold; its cleanup does not.

## Acceptance
All three legs are closed, each by a test that names a condition only its own
fix satisfies (`the-worktree-check-passes-without-its-fix`):
`a_nested_ignore_file_governs_its_own_subtree`,
`forget_by_source_with_prefix_takes_everything_under_a_path`, and
`the_gate_walks_exactly_what_the_watcher_walks` (`tests/memos_index.rs:223`),
which builds a subtree no root rule mentions carrying its own `.gitignore` and
asserts the gate and the watcher treat it the same. Proved live on 2026-09-06
by three files under one watcher: `memos/wtprobe/.gitignore` ingested 2
thoughts, `memos/wtprobe/target/debug/junk.lock` and
`memos/.claude/x/target/junk.lock` ingested none — same subtree, same scheme,
separated only by the nested rule.
