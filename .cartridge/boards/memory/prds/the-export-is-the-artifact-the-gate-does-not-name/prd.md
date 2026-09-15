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

# `memory export` defaults to `memory-export.json` at the project root, which `.gitignore` had to add after it happened once at 168 MB — and it is in neither of `tracked_artifacts`' two lists, which is exactly the invisible-artifact case that gate's header describes

## Do

`memory export`'s `--out` defaults to `memory-export.json`, and the binary chdirs
to the project root before clap parses ([[relative-paths-mostly-ignored]]), so
a bare `memory export` writes it into the repo. It happened: `.gitignore:112-113`
carries the line and the reason —

```
# a store export dumped in the tree — 168 MB of vectors, regenerable by `memory export`
/memory-export.json
```

That file is 611 MB on this store today, measured on 2026-09-06 — 3.6x the
number in the comment, for 75 memories and 11,737 thoughts
([[the-cleanup-could-only-reach-one-scheme]] is the same export read for its
source schemes).

`tests/tracked_artifacts.rs` does not name it. Its two lists are
`RUNTIME_DIRS` — `.memory`, `.relay`, `.mesh`, `.git-fs`, `.splinter` — and
`RUNTIME_FILES` — `data.mdb`, `lock.mdb` — and both assertions test only those.
So the export satisfies assertion 1 by being ignored and is invisible to
assertion 2, which is precisely the case the gate's own header argues it exists
for: "the check `.gitignore` cannot make, since an ignored store is an
invisible store, and invisible is how it survives long enough to be swept in
with a force-add."

The smaller fix is one entry: add `memory-export.json` to `RUNTIME_FILES`, and
the working-tree assertion covers it. The better one is to stop writing it
there — default `--out` to a path inside `data_dir`, which is already ignored,
already memory's to own, and already where `log_dir()` puts a detached child's
output for the same reason. That changes a default, so it is the caller's
choice to make, not this item's.

**Done 2026-09-06, and the part's smaller fix would not have worked.** It says
"add `memory-export.json` to `RUNTIME_FILES`, and the working-tree assertion
covers it". It does not: `no_crate_directory_holds_a_store` walks `src` and
`tests` only, deliberately, because the repo root's own `.memory/` is where a
developer's daemon legitimately lives. The export lands at the **root**, so the
walk never visits it and the list entry alone changes nothing for assertion 2.

Both halves are in. `RUNTIME_FILES` gains the name, which is what assertion 1
needs to catch a force-add of an ignored file. And `ROOT_RUNTIME_FILES` is a
second, non-recursive check of the root by exact name — files only, so `.memory/`
there stays legitimate while a stray export does not. That closes the hole the
gate's own header describes: "an ignored store is an invisible store, and
invisible is how it survives long enough to be swept in with a force-add".

Proved red: `touch memory-export.json` fails `no_crate_directory_holds_a_store`
with "1 runtime store(s) left inside the source tree"; removing it passes.

The better fix the part names — defaulting `--out` inside `data_dir` — is
untouched, and remains the caller's to make. This item makes the accident
visible; it does not stop the accident.

## Acceptance
`no_crate_directory_holds_a_store` fails when a `memory-export.json` sits in the
tree, and `just test` is green with none there. Both observed; suite 1,255
passed.
