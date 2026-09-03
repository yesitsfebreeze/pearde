# vision.md — how to fill it, and why each line is there

The template is @references/templates/vision.md. `pearde init` copies it to
`.pearde/vision.md` as is, `terminals:` and `edges:` commented out, for the
user to fill. `plan.py vision --check` reads it, and `doctor`'s `vision` row
runs that.

## Frontmatter

The plan reads only the frontmatter: `vision` prints on the scan, and
`terminals` plus `edges` place every live PRD by the serial hops between it and
a terminal. @references/parts/order.md.

| key | is |
|---|---|
| `vision` | one sentence — the destination |
| `terminals` | the PRDs whose completion IS the vision. `<prd>`; `@<member>/<prd>` on a master; `@<name>/<prd>` for the master's own. None means no axis: the board orders by dependency, weight and priority alone |
| `edges` | `"<from> -> <to>"` — a dependency nobody wrote as `needs:`, usually across boards. The same addresses as terminals |

A terminal or edge end naming no PRD is reported by the check; name it as
`needs:` would, or drop the line.

## The body

What the board adds up to when every terminal is done, for the person opening
it and asking what the work is FOR. A paragraph, or a bullet per terminal. No
dates.
