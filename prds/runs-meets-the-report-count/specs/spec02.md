---
complexity: 1
footprint:
  - references/workflow.md
---

# spec02 — document the new failure in the workflow format's own page

`references/workflow.md`'s `## The check` bullet list is the format's own
account of every way `workflows.py check()` can fail; spec01 adds two ways
that list did not carry. Already stands (built during the probe pass,
uncommitted): two bullets appended after "a board in `members:` that is not
on disk" — one for the report-count comparison (naming the asymmetry so a
reader does not mistake it for an equality check), one for the unparseable
heading. Nothing left to finish.

## Acceptance

- [x] `## The check` names both new failures spec01 implements, in the same
      one-bullet-per-failure shape as every other line in that list.
- [x] The new text states the comparison is one-directional (more reports
      than `runs:` only) so a reader does not read it as an equality check.

## Verify and Proof

```sh
grep -n "outnumber its own \`runs:\`" references/workflow.md
grep -n "report-section heading naming no slug" references/workflow.md
```
