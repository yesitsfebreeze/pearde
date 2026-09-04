---
complexity: 7
footprint:
  - references/parts/commits.md
  - references/parts/order.md
  - references/parts/contract.md
  - references/settings.md
  - references/templates/prd.doc.md
  - references/templates/grammar.md
---

# spec02 — three settings claims say what their readers actually do

Three documented knobs promised behaviour no module carries.

`commits.md` closed with `commits: off` in `settings.md` holding all of it.
No key by that name is declared in `references/settings.md` and nothing under
`resources/` reads one, so a reader who set it got a silently ignored line and
a board that kept committing. The page now says there is no off switch and
reads a climbing `*<dirty>` count as a fault rather than a mode.

`blast-radius` was documented in four places as breaking ties and deciding
what a pass leads with. `compute_plan` never reads it: the only readers are
`specs.py`, which writes it from `--blast`, and `collect.py`, which lifts it
off a report's `## Scores` block. It is a label a person reads — on the card,
and as the `blast/<blast>` tag `knowledge.py board` puts on the PRD's wiki
note. `order.md`, `contract.md`, `templates/prd.doc.md` and
`templates/grammar.md` each carried a copy of the wrong sentence.

`pipeline` was documented as analyst slots at loop step 4. Unlike `workers` —
which `schedule.py` and `mapfile.py` read and the plan sizes waves by — no
module reads `pipeline` at all: `init.py` writes the default, `run.py` cites it
in a comment for the `0 means unlimited` convention, and the orchestrating
session honours the number itself. A worker over the cap is refused by nothing.

**What already stands** (built in the analysis pass, uncommitted in the lane):
all six files. `order.md`'s third axis is renamed **Complexity** and says
`blast-radius` breaks no tie; the other three copies are swept; `settings.md`'s
`pipeline` row names its non-readers and contrasts `workers`; `commits.md`'s
closing paragraph is replaced.

**What is left to finish**: review and commit. The alternative for each line
was to implement the code instead — a `commits:` reader in `collect.py`, a
`blast-radius` term in the plan's sort, a `pipeline` gate in `claim`. All three
were rejected: none has a caller asking for it, and `settings.md` declares no
`commits` key for a reader to read.

## Acceptance

- [ ] `references/parts/commits.md` contains no `commits: off`, and states that no key in `settings.md` turns committing off.
- [ ] No file under `references/` says `blast-radius` breaks ties or decides what a pass leads with — checked in `order.md`, `contract.md`, `templates/prd.doc.md` and `templates/grammar.md`.
- [ ] `references/parts/order.md`'s third axis names `complexity` as the weight code sorts on and says `compute_plan` never reads `blast-radius`.
- [ ] `references/settings.md`'s `pipeline` row states that no module reads it and names `workers` as the one that is read, by `@resources/board/schedule.py`.
- [ ] Nothing under `resources/` (excluding `__pycache__`) reads a `commits` or `pipeline` settings key — so the corrected text is still true after the change.
- [ ] `references/parts/order.md` still says `priority` breaks ties within a depth; that claim is correct and unchanged.

## Verify and Proof

```sh
sh .pearde/prds/the-tree-holds-only-what-a-board-uses/the-documented-board-matches-the-code/probe/verify.sh "$PWD" "$PWD/.pearde"
test -z "$(grep -rn 'commits: off' references)"
test -z "$(grep -rnE '\`blast-radius\` breaks ties|blast-radius. Breaks ties|Breaks ties, and decides what a pass leads with' references)"
test -z "$(grep -rn 'get("commits"\|get("pipeline"' resources --exclude-dir=__pycache__ --exclude-dir=node_modules)"
grep -q 'No module reads it' references/settings.md
grep -q '`priority` breaks ties' references/parts/order.md
test -n "$(grep -rn 'get("workers"' resources --exclude-dir=__pycache__)"
```
