# vision.md — how to fill it, and why each line is there

The template is @references/templates/vision.md. `pearde init` copies it to
`.pearde/vision.md` as is, `terminals:` and `edges:` commented out; the user
fills it. `plan.py vision --check` is the reader, and `doctor`'s `vision` row
runs it.

## Frontmatter

The plan reads only the frontmatter: `vision` prints on the scan, and
`terminals` plus `edges` place every live PRD by how many serial hops separate
it from one terminal. @references/parts/order.md.

| key | is |
|---|---|
| `vision` | one sentence — the destination |
| `terminals` | the PRDs whose completion IS the vision. `<prd>`; `@<member>/<prd>` on a master; `@<name>/<prd>` for the master's own. None means no axis: the board orders by dependency, weight and priority alone |
| `edges` | `"<from> -> <to>"` — a dependency nobody wrote as `needs:`, usually across boards. The same addresses as terminals |

A terminal or an edge end that names no PRD is reported by the check; the fix
is to name it as `needs:` would, or drop the line.

## The body

What the board adds up to when every terminal is done — for the person who
opens the board and asks what the work is FOR. A paragraph, or a bullet per
terminal. No dates.
