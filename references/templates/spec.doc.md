# specNN.md — how to fill it, and why each line is there

The template is @references/templates/spec.md. The analyst writes one file per
implementable unit by hand from it; `pearde specced` is the reader and refuses
a file that breaks the contract, naming the line.

## Frontmatter

| key | why |
|---|---|
| `complexity` | analyst — 1-100, this unit's share of the PRD's weight. Summed into the PRD's `complexity`. Outside 1-100 is refused |
| `footprint` | analyst — every dir or file this spec touches. The orchestrator unions a PRD's footprints to avoid dispatching overlapping PRDs. Missing is a warning; the PRD's own stands for it |

Optional, read when present:

| key | is |
|---|---|
| `est` | a record. Nothing schedules on time; do not estimate duration. Price compute cost here, in the units it is spent in, when it changes scope |
| `workflow` | a slug in `.pearde/workflows/`, overriding the PRD's for this unit only. Naming no workflow is refused. @references/workflow.md |

Add your own keys freely; nothing outside these is read.

## The body

ONE implementable unit per spec file: an implementer finishes it in one sitting
from this file plus the PRD, without reading the sibling specs.

**`## Acceptance`** — boxes, each a concrete, observable check that can FAIL:
behavior, not effort. A file with no box is refused. Never write a box that
asks for a commit or a commit message — the orchestrator commits the PRD on
the transition that lands it, and such a box is refused.

The implementer ticks a box `[x]` only for a check it actually ran, quoting the
output in its report — and ticks it WHEN it runs it, not in a batch at the
end: these boxes are the only thing on the board that moves while a run is in
flight, and the plan is drawn from them.

**`## Verify and Proof`** — one `sh` block (no block is refused) of commands
that exercise the boxes. The implementer runs them and quotes the output.
Scope them to this PRD's footprint: a whole-workspace command inherits every
other node's flake, and `pearde specced` warns when no path here is under it.
