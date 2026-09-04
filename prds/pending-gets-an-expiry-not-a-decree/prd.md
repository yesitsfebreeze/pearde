---
state: specced
origin: requested
priority: 36
complexity: 15
blast-radius: mid
---


# Pending gets an expiry, not a decree

*Source: `docs/content/docs/improvements/knowledge-pending-expiry.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** knowledge · **Axis:** sensibility (6 → 7) · **Pulls the score up
by ~4 points**

## Why now

`pending/` is a priority-tagged queue by shape — files waiting, tagged,
walked by the loop — and *not a backlog* by decree: "a question never needed
again is deleted, not drained to zero; stale rows read as work owed, doctor
naming them". The rule fights the shape. A queue whose entries only ever
leave by hand-deletion *is* a backlog; the decree makes honest users feel
like they are doing it wrong, and the doctor row turns the folder into a
guilt source. A shape whose operating rule is "clean it by hand or feel bad"
is one concept too many.

## The change

Pending entries gain an expiry in their frontmatter — `expires:` set to a
date, defaulted from the `WORKFLOW.md` knob (`pending-expiry-days`, 14). The loop's
ask step reads pending last; an expired entry is *archived in place* — moved
to `pending/.expired/`, named in the response, never deleted — and `doctor`
stops naming stale rows as work owed: it names only rows inside the window.
The decree leaves the reference; the mechanism replaces it.

## Done when

- A pending file with `expires:` past and no `keep:` is moved to
  `pending/.absorbed/`-style storage by the next `query`, and the answer
  names it — the question is retrievable, not gone.
- `doctor`'s pending check counts only unexpired rows; a folder of stale
  files with none unexpired reads `ok`, not `broken`.
- `pending-expiry: 0` in `WORKFLOW.md` keeps nothing — the knob, not the
  rule, decides.

## Fails when

- Expiry deletes a question that was about to be asked. Guard: archive,
  never delete, and the ask step's `gap:` line says "expired on \<date\> —
  re-enqueue with `knowledge.py enqueue`" so the death is named.

## What stays out

No auto-research of expired questions — expiry is retirement, not
rescheduling. The auto_enqueue path already exists for gaps that *should*
run again.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 21:01 — claim impl-pending-expiry 2026-09-03 17:46, silent 3.2h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/pending-gets-an-expiry-not-a-decree`, whose worktree this sweep removed — the branch is kept.

## Blocked

**2026-09-03 21:57 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 02:42 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `session/s85810`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `session/s85810`; 1 file(s) disagree:

- `resources/knowledge.py`

Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 04:12 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.

**2026-09-04 04:20 — the lane will not rebase**

`lane/pending-gets-an-expiry-not-a-decree` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/pending-gets-an-expiry-not-a-decree` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock pending-gets-an-expiry-not-a-decree`.
