---
state: deferred
origin: derived
from: no-work-is-lost-on-the-board/a-lane-rebases-before-collect
priority: 60
complexity: 0
blast-radius:
---

# a session worktree lacks the pearde symlink a lane gets

`lanes.create` symlinks the live board in at `<lane>/.pearde` (both
`/pearde` and `/.pearde` are gitignored) — @references/parts/workers.md's
`probe-then-spec` `Fails when` table names this explicitly: "the `repo:`
root is a lane, and a spec's `## Verify and Proof` block spells
`pearde/prds/…`... symlink the live board in at `<lane>/pearde`." A session
worktree taken by `pearde session take` (`.pearde/.sessions/<id>`) gets no
such symlink — measured on `.pearde/.sessions/s98669`: `ls
.pearde/.sessions/s98669/.pearde` is `No such file or directory`, while
every `.pearde/.lanes/<slug>` does carry one.

Consequence for a requested PRD: `collect`'s guarded verify
(`resources/board/collect.py`, `verify_blocks`/`guarded_run`) runs a spec's
`## Verify and Proof` block with `cwd` set to `repo_of(prd, ...)` —
`repo_of` prefers the running session's own worktree once one is taken
(`session.instead_of`). A verify block that spells a board-relative path
the recommended way (`.pearde/prds/<prd>/probe/...`, no `cd`, no
`PEARDE_ROOT`) resolves it against `cwd` and finds nothing there, because
that `cwd` — the session tree — has no `.pearde` to find it under. Measured
live on `no-work-is-lost-on-the-board/a-lane-rebases-before-collect`, a
DONE implementer report `collect` cannot land: `spec01` block opens with
`bash .pearde/prds/no-work-is-lost-on-the-board/a-lane-rebases-before-collect/probe/run.sh`
and `collect` (verify running with `cwd` = the session tree) gets `bash:
…/probe/run.sh: No such file or directory`, exit 127 — while running the
identical line by hand from the outer checkout (which does hold the real
`.pearde`) exits 0. The lane itself also carries this same file, reachable
the same relative way, because `lanes.create` gave the lane the symlink the
session tree lacks.

Sibling to `a-verify-block-resolves-the-board-absolutely-not-from-its-cw`
(now `specced`/`claimed`, `resources/board/specs.py`) but the opposite
shape: that PRD's fix refuses a spec baking in a machine-absolute `cd`:
this is a spec doing the *recommended* relative-path thing, and the
*session's own tree* is what is missing the piece every lane already gets.
Likely fix: `pearde session take` (`resources/board/session.py`) symlinks
`.pearde` into the tree it cuts, the same way `lanes.create` already does —
or `repo_of`/`verify_blocks` resolve the board's path for the block some
other way that does not depend on the cwd holding a stub. Not measured
against every verify block on the board, only the one instance above.
