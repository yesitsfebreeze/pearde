---
state: specced
origin: requested
priority: 0
complexity: 18
blast-radius: low
workflow: probe-then-spec
---


# The capability registry

*Source: `docs/content/docs/improvements/integration-registry.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Layer:** index · **Tool:** all · **Unblocks:** suggest, usage, rank

## Why now

The machine's capabilities are indexed in three places that answer three
different questions and none of them the agent's: @index.md maps *files* for
a human reading the repo, the skills' frontmatter maps *entry points* that
fire on their description, and `pearde.py` discovers `COMMANDS` in every
directory under `resources/` at runtime. What is missing is the union, in
the shape an agent is handed: not "where does this live" but "what can I do
right now, with what, at what cost". `pearde help` prints docstrings to a
human; a mid-pass worker is handed a brief, and the brief names files and
workflows — never the verbs that could do the work.

## The change

One registry file, **generated from the tools, never hand-written**:
`pearde.py` already walks `resources/` for `COMMANDS`; the generator writes
one row per verb — name, one-line contract (the docstring's first line),
reads, writes, cost class (shell / python / network / human) — beside the
command that owns it. Skills map onto rows; the vault's verbs and the view's
sections get rows the same way (see the fire check and the vault pages).
Doctor's `index` row gains a line: a verb on disk with no row, or a row
naming no verb, is `broken` — the same drift check the manifest already
runs on files, run on verbs.

## Done when

- `pearde capabilities` prints the registry, one row per verb, and the count
  equals what `pearde.py` discovers at runtime — provable by diffing the two
  in one command.
- A verb added to any tool's `COMMANDS` appears in the registry on the next
  generation, with no hand edit — the check is adding a stub verb and
  finding it there.
- Doctor's new row reads `broken` when a registry row names a verb that no
  longer exists, the way the index check convicts a dead `@` anchor.

## Fails when

- The registry drifts from the tools the moment someone hand-edits it.
  Guard: it is **never written by hand** — regeneration is the only write
  path, and doctor refuses a registry whose mtime is older than the tools
  it covers, the way `scan`'s mtime cache refuses staleness.

## What stays out

No routing decision in the registry — it says what exists, never what to
run. Suggestion is the next page's job; the registry is only the inventory,
and a registry that decides is the second orchestrator this repo refuses to
grow.

## History

**failed, retried 2026-09-03 21:13**

**2026-09-03 21:0x — spec02 `DEAD_VERB_MISSED` on the merged tree**

spec01 green after the step-6 repair (the `bash -e` capture, recorded below in
this pass's memory). spec02 fails `DEAD_VERB_MISSED` on the tree the collect
merges — a verb the registry should refuse still resolves. The implementer's
report (18:16) predates this failure; its worker is gone. The work stands on
`lane/the-capability-registry`, 6 commits; nothing re-implemented, the next
implementer continues the lane.

## Blocked

**2026-09-03 21:19 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-03 21:41 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-03 21:47 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-03 21:47 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-03 21:57 — the lane will not rebase**

`lane/the-capability-registry` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/the-capability-registry` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 02:48 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/the-capability-registry` does not land on `session/s85810`; 1 file(s) disagree:

- `resources/board/init.py`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 04:03 — the lane will not rebase**

`lane/the-capability-registry` does not land on `main`; 1 file(s) disagree:

- `resources/common.py`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 04:06 — the lane will not rebase**

`lane/the-capability-registry` does not land on `main`; 1 file(s) disagree:

- `resources/common.py`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.

**2026-09-04 04:20 — the lane will not rebase**

`lane/the-capability-registry` does not land on `main`; 1 file(s) disagree:

- `resources/common.py`

Nothing is lost: the worker's commits are on `lane/the-capability-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-capability-registry`.
