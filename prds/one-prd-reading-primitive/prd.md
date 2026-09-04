---
state: done
origin: requested
priority: 26
complexity: 22
blast-radius: mid
workflow: probe-then-spec
commit: fe75b91 638b38b
---

# One PRD-reading primitive

*Source: `docs/content/docs/improvements/board-prd-primitive.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** board · **Axis:** complexity (6 → 7) · **Pulls the score up by
~4 points**

## Why now

What a PRD *is* — a directory holding `prd.md`, state in frontmatter, specs
under `specs/` — is decided by four modules: transitions, guard, collect and
the plan. Each parses or validates the shape its own way, and each carried
its own refusal for the same malformed file. The reference can say "one
function, `plan.dispatchable`, tests leaf, container, parked child, `needs:`,
footprint and `workflow:`" — but that function is the gate, not the *reader*;
the reading happens four more times, four more ways. A malformed PRD is
reported four different ways depending on who meets it first.

## The change

`resources/common.py` — the advisors' shared-primitives home — gains the
PRD reader: parse the frontmatter, resolve the specs list, walk children,
return the errors. Transitions, guard, collect and plan import it instead of
their own parse. The board scan keeps its mtime cache; the primitive is what
*behind* the cache, not a second one.

## Done when

- Transitions, guard, collect and plan each import the one reader — a
  `grep` for the frontmatter parse over those four modules finds imports,
  not implementations.
- A malformed PRD (state key nobody declared, a spec with no `subject:`) is
  named identically by all four paths — the check is one malformed fixture
  walked through each.
- `plan.dispatchable` still reads the same inputs; its gate logic is
  untouched.

## Fails when

- The reader grows the *deciding* too — state transitions, dispatch rules —
  and becomes a second orchestrator. Guard: the module returns facts and
  problems; verbs decide. The docstring draws exactly that line.

## What stays out

No layout change, no state change — the board parses the same. The page's
win is one reader of the shape, where four exist.

## Blocked

**2026-09-03 18:48 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s34612`; 1 file(s) disagree:

- `resources/guard.py`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-03 21:00 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/guard.py`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-03 21:35 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-03 21:42 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

**2026-09-04 02:48 — the lane will not rebase**

`lane/one-prd-reading-primitive` does not land on `session/s85810`; 1 file(s) disagree:

- `resources/guard.py`

Nothing is lost: the worker's commits are on `lane/one-prd-reading-primitive` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-prd-reading-primitive`.

## Report

spec01: exit 0
spec01: ok

spec02: exit 0
spec02: ok
41 checks · 38 pass · 3 fail

spec03: exit 0
imports ok, plan.KEY_RE = re.compile('^\\s*([A-Za-z][A-Za-z0-9_-]*):\\s*(.*?)\\s*$')
  open      · the-tree-holds-only-what-a-board-uses · p65 · w0 · off-axis · needs a-board-s-grammar-holds-only-its-own-words,scout-s-research-leaves-the-tree,the-persona-layer-is-one-file,the-obsidian-vault-is-opt-in,the-documented-board-matches-the-code,legacy-migrations-retire,tags-are-derived-when-the-vault-is-written,the-template-twins-fold-into-the-reference,knowledge-s-repo-only-verbs-move-out-of-the-product

round: /Users/feb/dev/infra/pearde/.pearde/.state/pass.md
spec03: ok
