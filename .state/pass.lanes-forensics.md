# Forensics — destructive git paths · pearde-ca · 2026-09-02 19:10

Written as a SIDE FILE, not into `pass.md`: a second pass window rewrote
`pass.md` whole at 18:35 while this window was live. Do not merge this by
overwriting that file.

## 1. Nothing reverted the main checkout. The cause is benign.

`git reflog -30` holds **no destructive move after the 17:45 merge**:
`checkout main→wip` (18:06), `commit d3b72b9` (18:06), `checkout wip→main`
(18:06), `commit 92e318c` (18:10), `merge --ff` (18:15). Last
`reset: moving to` is **17:08**, before the window. `git reflog stash`: 5
entries, **none after 17:51**.

Peer `dev-c1` committed the vault work to `wip/board-dir-pearde-not-hidden`
and checked `main` back out. **`git checkout` cannot discard uncommitted
changes it would overwrite — git refuses.** The files left the tree because
they had become a commit on another branch. To a session that only re-reads
its own files, that is indistinguishable from destruction. **There is no
unfound destructive path behind this incident.**

`d3b72b9` carries all 22 files (+565/−243). `92e318c` on main carries 20;
`references/personas/writer.md` (+64) and its `references/files.md` row (+1)
are on `d3b72b9` only. **`run-*.log` does not exist on this board** — that
avenue is empty, not unexamined.

## 2. Two live paths that destroy uncommitted work in a tree the caller may not own

**`resources/board/lanes.py:180` — `merge()`, on rebase conflict:**

    git(wt, "rebase", "--abort", check=False)
    git(wt, "reset", "--hard", was, check=False)     # ← :180

The `reset --hard` is **unconditional**; the abort's failure is swallowed by
`check=False`, so it fires even when the abort did not happen. `wt` is
`worktree_of(repo, br)` — **whatever worktree holds the lane branch.** When
that is a shared checkout rather than a lane dir, this destroys every
uncommitted file in it. `e5abc5b` fixed `collect.unland` and **does not touch
`lanes.merge`** — that blind spot is why the danger outlived the fix.
Repair returned DONE this pass, unmerged, in
`lane/a-refused-rebase-must-not-destroy-the-lane-it-was-left-in`.

**`resources/board/lanes.py:127` — `remove()`, `force=True` by default:**
`git worktree remove --force`, reached from `transitions.py:1000`
(`drop_lane`), sole caller `cmd_sweep` (`transitions.py:940`). Its docstring
states the intent: *"Uncommitted dirt in the lane dies with the worktree,
which is what a sweep means."* **A sweep silently destroys a worker's
uncommitted work** — and sweep's liveness clock is provably wrong (§3). A
wrong clock plus a forced remove deletes a *live* worker's lane. **The
rebuilt run-verb work is uncommitted in a lane right now and is one such
call away from being lost a second time.**

**Latent, third of the class:** `analyst-verify-block` found `_foot_in`
rebasing footprints against `board_root` rather than the repo; **parking at
`board_root` would reach into other live sessions' dirt once a `gate:` key
exists.** No `gate:` here, so latent. Same bug class: a path computed against
the wrong root, applied with a destructive verb.

**Cleared:** `collect.py:1242` is a docstring; `collect.py:483` is a
path-scoped index-only `reset -q -- <paths>`. No `git clean`, no real
`git stash`, no `git restore` anywhere in `resources/`.

## 3. `sweep`'s liveness clock is wrong

`sweep` reported "no claim silent past claim-ttl 30m" for three claims whose
workers were dead: no `claude` process for this board, no transcript written
since 17:49 (checked 18:19); one had been claimed 59 minutes earlier. **Do not
trust `sweep --apply` on this board until §2 is fixed.**

## 4. On calling a worker dead

An `API Error: 402` in a transcript is **not** proof of death —
`analyst-run-verb` showed one and still returned SPECCED. And `API Error`
matched in two other transcripts purely because those workers had *read*
`workers.md`/`loop.md`, which quote the phrase. Grep `API Error: 402` **and**
confirm the transcript stopped growing.

## 5. Two defects confirmed independently, and a parent target that cannot be met

Three analysts, working in separate lanes, converged on the same two facts.
Neither is one worker's opinion.

**`resources/prose.py` reads frontmatter as prose.** A skill's `description:`
— the line that decides when the skill fires — is measured as if it were
body text. All 19 skill bodies are green; **every remaining violation in
`references/skills/` sits on that one line, across 6 files.** A second analyst
independently names the same defect plus a second one: **restrictive relative
clauses flagged as vague subjects.** This is a defect in the checker that
landed as `done` this pass (`3664de0`), found by the first workers to point it
at frontmatter. `analyst-skills-dense` returned **QUESTION** on it — one fork,
green under `questions.py check`, written to its `prd.md` and **not yet in
`.state/ask.md`.** It is owed to the user in the SAME drill pass as the three
already open, not a second one.

**`every-document-is-written-in-the-writer-s-prose`'s 30% target is
arithmetically impossible**, measured twice over different footprints:

| footprint | prose share | ceiling | achieved |
|---|---|---|---|
| skills + scout | 37% (4,619 / 12,421 w) | — | −7.1% prose, −2.2% total |
| templates + personas + agents | 49% (51% non-prose) | **25.6%** even halving every cuttable word | 6–10% |

A 30% cut of *total* words cannot come out of prose alone. **Restate the
parent against prose words, not total words, before collecting the SPECCED
siblings** — otherwise six children get specced against a figure none can
hit. One analyst has already worked around it by writing absolute word
ceilings into its specs instead.

**`references/personas/writer.md` is absent from main** — third independent
flag, and `index.py check` is **red at baseline** because of it. One sibling
report claims it is on disk with a manifest row; **that claim is false.** The
file exists only in `d3b72b9`. **No child PRD owns writing it**, so no worker
on the board will fix the red. That is an orchestrator's call, not a worker's.

## 6. Two pass windows are writing this board at once

`pass.md` was rewritten whole at 18:35 by a second pass window while this one
was live. That window records the eight workers dispatched 17:20–18:17 as
belonging to "a pass window that is gone" — **they are this window's, and they
returned normally.** It has since dispatched its own three, including
`analyst-resources-org` on `resources-are-organised-by-responsibility`, **the
PRD this window deliberately held back because three unanswered user forks
gate it** and each answer changes what the other two mean.

This is the same failure class as the afternoon's incidents: two writers, one
shared piece of state, neither aware of the other. It needs a person, not a
retry.
