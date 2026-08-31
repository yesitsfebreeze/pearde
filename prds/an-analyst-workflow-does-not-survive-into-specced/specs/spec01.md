---
complexity: 8
footprint:
  - resources/board/specs.py
---

# spec01 — a spec's `workflow:` survives onto the PRD

`pearde specced` no longer drops the route an analyst wrote into a spec file:
when the command runs with no `--workflow` flag and the PRD frontmatter
carries no `workflow:`, one distinct slug across `specs/*.md` is written up
onto the PRD by `edit.set_key`, the same way `refine` hands a parent's slug
down to children. Two specs naming two different slugs write nothing, and a
stderr note names both. The explicit flag wins in every case where it is
present, and nothing overwrites a key the PRD already carries.

## What already stands

The behaviour is built and uncommitted in
`resources/board/specs.py`: `read_specs` also returns the spec
frontmatter `workflow:` slugs in file order (six-tuple now), and `specced`
— after the size-limit gate, before the write — sets the PRD's slug from the
specs when the flag is absent and the key is not on the PRD (a commented-out
`# workflow:` counts as absent), prints the ambiguity note on stderr, and the
`--dry` branch prints a `dry · workflow: <slug>` line for any slug a real
write would set. The module docstring documents it. A 21-check harness at
the probe exercises all of it and passes: 21/21. The committed
`specced-is-a-command` harness still prints 90/90 after the change.

## What is left

Nothing in the code. The implementer re-runs both harnesses, ticks the boxes
below against fresh output, and reports. A failure here is a regression,
not spec-from-scratch work.

## Acceptance

- [x] On a fixture PRD in `analyzing` with no `workflow:` and one
  `specs/*.md` naming a real workflow, `specs.py specced <prd> --blast low`
  (no flag) exits 0 and the PRD frontmatter afterwards holds `workflow:`
  set to that slug.
  `  ok   one spec naming a workflow → exit 0` · `  ok   …workflow: fix-a-line written up` ·
  `verify: 21/21 checks pass`
- [x] A PRD that already carries a `workflow:` keeps its own value when a
  spec names the same or a different one, and the derived write never fires
  for it.
  `  ok   PRD key kept when a spec names one` · `  ok   a carried key is not overwritten`
- [x] Two specs naming different real workflow slugs: exit 0, the PRD is
  `specced`, no `workflow:` key is written, and stderr carries a note naming
  both slugs and telling the operator to pass `--workflow`.
  `  ok   two slugs → exit 0, PRD still specced` · `  ok   …no workflow key written` ·
  `  ok   …the note names both slugs on stderr`
- [x] `--dry` prints a `dry · workflow: <slug>` line in the same cases the
  real run would write the key, and changes no file; `--check` exits 0
  printing the sum and writes nothing.
  `  ok   --dry exit 0, shows the derived slug` · `  ok   …and changes no file` ·
  `  ok   --check exits 0, prints the sum` · `  ok   …and writes no workflow key`
- [x] A spec naming an atomic or an unknown slug is still refused by file
  and line with the wording `names an atomic, not a workflow` / `names no
  workflow in the library`, and the PRD is not written.
  `  ok   unknown slug refused, file and line` · `  ok   …and the PRD is not written` ·
  `  ok   workflow naming an atomic` (90/90 harness)
- [x] After a derived write, `pearde brief <prd>` prints the slug in its
  `wf <slug>` head line for an analyst brief and an implementer's.
  `  ok   analyst brief head carries wf fix-a-line` ·
  `  ok   implementer brief head carries wf too`

<!-- Verify that the probe harness —
     .pearde/prds/an-analyst-workflow-does-not-survive-into-specced/probe/verify.sh
     — still passes after any further edit; it reads the footprint file
     `resources/board/specs.py` through SPECS_PY. -->

## Verify and Proof

```sh
grep -n "dict.fromkeys(spec_wfs)" resources/board/specs.py
bash .pearde/prds/an-analyst-workflow-does-not-survive-into-specced/probe/verify.sh
bash .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh
```