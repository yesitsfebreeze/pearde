# Progress line

The one line printed on every state change, term by term.

Every transition command — `pearde claim` · `release` · `answer` · `retry` ·
`unblock` · `defer` · `add` · `set` · `sweep` · `specced` · `refine` ·
`collect` — prints the line on stdout, every term computed from the board
after the write. A command run from a shell says `pass file owed` before `as`.
The pass computes none of the terms; the one term the tool cannot know is the
persona, passed as `--as <id>` or `PEARDE_AS` in the environment.

```
▸ <prd>: <from> → <to> · done <rd>/<rn> · <rp>% · derived <dd>/<dn> · open <o>/<n> · <q>% · ready <r> · blocked <b> · collect <c> @<w> workers · as <persona>
```

| term       | is                                                                        |
|------------|---------------------------------------------------------------------------|
| weight     | the PRD's `complexity`; missing counts at the average of scored PRDs, `weight-default` if none |
| `<face>`   | `happiness:` 0-5 as `:?` `:(` `:/` `:|` `:)` `:D` — how well the machine is set up for this repo, @references/parts/ramp.md. `pearde be happy` writes it |
| `<rd>/<rn>`| `done` / all `origin: requested` — **the deliverable**                     |
| `<rp>`     | Σ weight(done, requested) / Σ weight(all requested). `failed` counts as remaining |
| `<dd>/<dn>`| `done` / all `origin: derived`. Counts, never weighted                      |
| `<o>`      | PRDs still `open`, both origins                                             |
| `<q>`      | `<o>/<n>`. A count — an `open` PRD is not scored yet                        |
| `<n>`      | the states in the @references/parts/states.md table only                   |
| a master   | every member's PRDs and its own, one set. A member's PRD is named `@<member>/<prd>` |
| `<r>`      | **ready** — dispatchable right now: `needs:` all `done`. A footprint clash with a `claimed` PRD does not hold the PRD: each worker has a lane of its own, so the plan orders that pair and the merge resolves the clash |
| `<b>`      | **blocked** — not `done`, not ready. Name what holds the largest group      |
| `<c>`      | **to collect** — finished work still open: every acceptance box `[x]`, state not yet `done`. Omitted at zero |
| `as <persona>` | who is working, the id — @references/parts/personas.md. **Always last, never omitted**, because the line is the only record |

## How to read the terms

- **`done` is the answer to "how far along are we".** Derived PRDs enlarge the
  denominator with work the user never requested: a board 90% through its
  deliverable reads 63% combined. Report both or neither.
- Omit the `derived` term on a board with none.
- A live tripwire is said on the line and in the pass.
- `<q>` and `<rp>` do not sum to 100 — untouched board against requested work
  done.
- A parked PRD sits in neither numerator nor denominator. Name a parked PRD in
  the report.
- **`ready` and `blocked` are the actionable pair.** A board with 20 PRDs left
  and `ready 1` is not slow but serial. The pass says which dependency or which
  footprint holds the other 19 — a fact a reader can act on.
- **`collect` above zero is the board waiting on itself.** The work is done and
  the states have not caught up, so `ready` under-reports by whatever those
  PRDs unblock. Close them before reading the rest of the line — step 6 of
  @references/parts/loop.md.

## `as <persona>` is stored nowhere else

Session state written to no file, recorded on this line and nowhere but —
never omitted, not even unchanged, and a `persona <id>` switch prints its own
line in this form though no state moved. @resources/statusline.sh reads the
last one out of the session transcript; a pass leaving the term off leaves the
terminal showing the persona before.

## The continuous rendering is the status line, for a different reader

@references/parts/statusline.md renders the same numbers continuously in the
terminal, and the loop needs none of them. The status line carries one term
this line does not: where the progress line has room for
`derived <dd>/<dn>`, the status line renders `+<dr>d`, the derived PRDs not yet
`done` — the same report-both-or-neither rule, resolved for a row holding one
number.
