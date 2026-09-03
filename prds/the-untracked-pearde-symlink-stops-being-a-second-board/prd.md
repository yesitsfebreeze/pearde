---
state: open
origin: requested
priority: 95
complexity: 0
blast-radius:
---

# the untracked .pearde symlink stops being a second board

The checkout holds an **untracked symlink** `.pearde -> pearde` beside the real
board directory, made 2026-09-02 18:10. `plan.py` reads
`BOARD_DIR = "pearde"` with `LEGACY_BOARD_DIR = ".pearde"` and accepts both, so
one directory answers to two names. It breaks the board two ways at once.

**Double dispatch.** The same board resolves twice (`pearde` and `pearde-2`),
so `run all` hands every PRD out twice. Two workers then write one lane: the
`the-machine-is-the-run-verb` worker found amends and rebases in its reflog it
did not make, and its boxes already ticked when it arrived. Every worker-hour
spent on a twin is wasted, and two writers on one lane is how a lane gets
corrupted.

**Every collect refuses.** In the checkout `.pearde` and `pearde` are one
directory. In a lane or session worktree they are **two separate real
directories**, the `.pearde` one all but empty — the symlink is untracked, so a
worktree materialises the name without the content. `collect` builds probe
paths against `.pearde/`, so they resolve to nothing there:

```
bash: .pearde/prds/<prd>/probe/verify.sh: No such file or directory
python: can't open '<board>/.sessions/s29969/.pearde/prds/<prd>/probe/facts.py'
```

Five finished PRDs are stuck behind this, all reporting DONE with every box
ticked. Collect refuses cleanly and writes nothing, so there is no damage —
only a jam.

**Why this needs sequencing, not just `rm`.** Deleting the symlink is the
obvious fix, but `the-board-is-a-real-directory-at-pearde-never-a-symlink` is
mid-flight and **migrating the board to `.pearde/` as the real directory**. Its
analyst also measured that a real `pearde upgrade` strands every live lane and
session worktree, because they sit at `<board>/.lanes/` with absolute paths.
Removing the link and running that migration are the same decision taken twice.

## Acceptance

- [ ] One name resolves this board. `scan` from the checkout and from a lane worktree names the same directory, and the view daemon lists it once.
- [ ] `collect` runs a PRD's probe from a lane and a session worktree with every path resolving, proved on one of the five stuck PRDs.
- [ ] The choice is recorded as a memo: the link goes now, or it stays until the migration lands and the migration owns its removal.
- [ ] No `pearde upgrade` runs while a lane or session worktree is live — `scan` clean and `session reap --apply` first.
