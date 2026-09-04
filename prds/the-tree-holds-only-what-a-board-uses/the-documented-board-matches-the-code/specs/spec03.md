---
complexity: 5
footprint:
  - references/parts/doctor.md
---

# spec03 — doctor.md names all twenty-one rows, in the order they print

`doctor.sh` can print twenty-one rows. `references/parts/doctor.md`'s table
listed fourteen, and the seven it omitted are the ones a reader is most likely
to meet unexplained: `plugins`, `guard`, `vault`, `vision`, `knowledge`,
`briefs` and `jstests`. Six of the seven are the rows this repo's own board
reports `broken` or `off` on a normal day, so the page that exists to tell a
broken install from an absent one was silent about most of what it prints.

The table's row order was also its own, not the script's. It is now the print
order, so a reader can follow a report top to bottom against the page.

Three claims in the paragraph above the table were wrong or incomplete and are
corrected with it: `members` prints **no row at all** on a board with no
`members:` rather than an `off` one; `skills`, `index` and `statusline` never
read `off`; `plugins` and `plan` never read `broken`.

**What already stands** (built in the analysis pass, uncommitted in the lane):
the whole table, in print order, with all twenty-one rows and their `off` and
`broken` conditions read out of `doctor.sh`'s own `row` calls, and the
corrected paragraph above it.

**What is left to finish**: review and commit. If a row is added to
`doctor.sh` after this lands, the probe's check 6 fails and names it — that
check compares the table's row names against the script's, so the two cannot
drift apart again silently.

## Acceptance

- [ ] `references/parts/doctor.md`'s table names every row `doctor.sh` can print: skills, plugins, index, statusline, guard, board, vault, vision, members, origin, memos, workflows, grammar, health, knowledge, briefs, questions, view, plan, harnesses, jstests.
- [ ] The table's rows appear in the order `doctor.sh` prints them, with `members` in the position it occupies when a master board prints it.
- [ ] The paragraph above the table says twenty-one rows, that `members` prints no row rather than an `off` one on a non-master board, that `skills`, `index` and `statusline` never read `off`, and that `plugins` and `plan` never read `broken`.
- [ ] Each of the seven added rows carries an `off` and a `broken` cell matching that row's `row <name> off` / `row <name> broken` calls in `doctor.sh` — `plugins` and `plan` carry an em dash for `broken`, `skills`, `index`, `statusline` and `members` an em dash for `off`.
- [ ] The probe's row-parity check passes: every `row <name>` in `doctor.sh` has a table row in `doctor.md`.

## Verify and Proof

```sh
sh .pearde/prds/the-tree-holds-only-what-a-board-uses/the-documented-board-matches-the-code/probe/verify.sh "$PWD" "$PWD/.pearde"
test "$(grep -cE '^\| `[a-z]+`' references/parts/doctor.md)" = 21
grep -q 'twenty-one rows' references/parts/doctor.md
for r in skills plugins index statusline guard board vault vision members origin memos workflows grammar health knowledge briefs questions view plan harnesses jstests; do grep -qE "^\| \`$r\`" references/parts/doctor.md || exit 1; done
bash resources/doctor.sh "$PWD/.pearde" > /tmp/doc.$$ 2>&1; test -s /tmp/doc.$$
```
