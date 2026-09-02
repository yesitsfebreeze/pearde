# Without parallel workers

`workers=1`, `pipeline=1`, and the brief followed by hand. The seven steps do
not change — read the table at @references/parts/loop.md. Four rows are
already what a solo pass does; these three change.

| step | by hand |
|---|---|
| 3 refine | the `## Split` table is yours to write, then `pearde refine <prd> < split` |
| 4 spec ahead | after `pearde claim` and `pearde brief`, run the analyst's brief as a checklist, then `pearde collect <prd> --report <the report's path>` — or `pearde specced <prd> --blast <x>` by hand when there is no report |
| 5 implement | the same two commands, then run the implementer's brief; tick each box as you close it |

A `workflow:` on the PRD is a route you follow yourself, so you write the edit
at the failing step instead of collecting it: no report to read, no second
reader to hand one to. Apply or refuse per whose fault the failure was,
as the loop does — applied for the atomic's fault, refused for the code's or
the PRD's; `runs` +1 on the workflow and every atomic that ran; the text you
wrote at the step: paste it or refuse it, never rewrite it;
`pearde workflow check`, then the collect — @references/parts/workflows.md.

Every rule holds: one writer per file, the gate is the command, work flows to
the leaves.
