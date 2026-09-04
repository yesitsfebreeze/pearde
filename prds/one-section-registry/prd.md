---
state: done
origin: requested
priority: 45
complexity: 18
blast-radius: mid
workflow: probe-then-spec
commit: 6fb70b0 d302062
---

# One section registry

*Source: `docs/content/docs/improvements/view-section-registry.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** view · **Axis:** sensibility (5 → 7) · **Pulls the score up by
~5 points**

## Why now

The page's shape — seven sections, one visible, the bar in the header, ⌘1–7,
the fold rules on list/memos/report, the now strip above whichever is open,
the URL naming it — is stated in the reference and *re-derived* by the
renderer: every section's show/hide, keyboard and fold state is wired by
hand, so "the bar is tabs" is true because the code agrees, not because
anything checks. The fold rule ("three of those fold, every section draws on
first paint") is the most-read paragraph in the reference and the least
provably true one in the tree.

## The change

One registry names the sections: id, key, title, the band of the plan it
reads, `folds:` (yes/no), the URL fragment it answers to. The header bar,
the keyboard map and the fold summaries render *from* the registry, so a
ninth section is one row and the fold rule is a field, not a paragraph.
`viewtest.js` gains one check: every registry row renders, folded or
hidden, on first paint.

## Done when

- The registry is the only place a section id appears outside its own
  renderer — `grep -c 'data-view='` over the render tree agrees with the
  registry's length.
- Adding a stub row to the registry makes the bar show eight sections with
  no other edit, and the first-paint check fails until the stub renders.
- ⌘1–7 and `#view=` routing come from the same table — one mapping, provable
  by reading it once.

## Fails when

- `all`'s boards section is a *different* registry — it is a different page;
  forcing one table over both reintroduces the merge `all` deliberately
  leaves out.

## What stays out

No visual change. The page renders identically; the diff is structure only,
which is what makes it reviewable in one sitting.

## Blocked

**2026-09-03 20:42 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s27323`; 3 file(s) disagree:

- `resources/board/render.py`
- `resources/board/view.js`
- `resources/board/viewtest.js`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-03 21:00 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s27323`; 3 file(s) disagree:

- `resources/board/render.py`
- `resources/board/view.js`
- `resources/board/viewtest.js`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-03 21:00 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s27323`; 3 file(s) disagree:

- `resources/board/render.py`
- `resources/board/view.js`
- `resources/board/viewtest.js`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-03 21:23 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s27323`; 3 file(s) disagree:

- `resources/board/render.py`
- `resources/board/view.js`
- `resources/board/viewtest.js`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-03 21:34 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-03 21:35 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/one-section-registry` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-04 02:42 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s85810`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-04 02:45 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s85810`; 3 file(s) disagree:

- `resources/board/render.py`
- `resources/board/view.js`
- `resources/board/viewtest.js`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/one-section-registry` does not land on `session/s85810`; 3 file(s) disagree:

- `resources/board/render.py`
- `resources/board/view.js`
- `resources/board/viewtest.js`

Nothing is lost: the worker's commits are on `lane/one-section-registry` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-section-registry`.

## Report

spec01: exit 0
  ok   the example board renders
  ok   registry length (9) == rendered <section data-view=…> count
  ok   registry length (9) == rendered nav <a> count
  ok   render.py restored byte-identical after the stub probe
  ok   the stub row alone raises the section count by one (9 -> 10)
  ok   the stub tab and section exist with no other file touched
  ok   viewtest.js --example (real shape): 50/50 passed
  ok   viewtest.js on a merged (all) page: 50/50 passed
  ok   render.py restored byte-identical after the viewtest stub run
  ok   viewtest.js's first-paint check catches the un-rendered stub
10/10 passed, 0 skipped
29 checks · 29 pass · 0 fail

spec01: exit 0
  ok   the example board renders
  ok   registry length (9) == rendered <section data-view=…> count
  ok   registry length (9) == rendered nav <a> count
  ok   render.py restored byte-identical after the stub probe
  ok   the stub row alone raises the section count by one (9 -> 10)
  ok   the stub tab and section exist with no other file touched
  ok   viewtest.js --example (real shape): 50/50 passed
  ok   viewtest.js on a merged (all) page: 50/50 passed
  ok   render.py restored byte-identical after the viewtest stub run
  ok   viewtest.js's first-paint check catches the un-rendered stub
10/10 passed, 0 skipped
29 checks · 29 pass · 0 fail
