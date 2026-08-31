---
complexity: 15
footprint:
  - resources/board/specs.py
---

# spec02 — `pearde specced --workflow <new-slug> --route -` drafts and gates the route

Already stands: `resources/board/specs.py` gained `--route` on `specced`,
`route_text`/`route_parts` (reading `## Route` as the report's raw last
section — split on `### atomic <slug>` boundaries rather than the file's flat
`##` splitter, so the workflow's own `## Use when`/`## Steps` and each
atomic's `## Do`/`## Done when`/`## Fails when` stay nested instead of being
read as siblings), and `draft_route()`, which writes the workflow and every
new atomic via `workflows.py add`, runs `workflow check` over the whole
library, and deletes every file it wrote — refusing with nothing changed on
disk — on red or on a name already in the library. `specced()` calls it after
the spec-limit gates (so a route is never drafted for a call that was going
to be refused anyway), refuses `--workflow none` outright naming `## Route`,
refuses `--route` naming a slug already a workflow, and removes the drafted
files again for `--check` and `--dry` (both write nothing) while still
proving the route is green before returning. A new atomic's `subject` is
lifted from its step's `why` cell in `## Steps`. Nothing left to finish —
probed end to end at
`.pearde/prds/the-board-asks-for-itself/a-route-is-written-at-spec-time/probe/route.sh`.

## Acceptance

- [x] a fresh `## Route` naming two atomics, one already in the library and
      one not: `specced --workflow <new> --route -` writes the workflow file
      and only the one new atomic, sets `workflow: <new>` on the PRD, and
      `workflow check` is green after
- [x] `--workflow none` with no `--route` is refused, the message naming
      `## Route`
- [x] `--route` with `--workflow <slug>` already a workflow in the library is
      refused before any file is touched
- [x] a `## Route` whose `## Steps` names an atomic slug found nowhere fails
      `workflow check`: the call is refused, the library holds no new file,
      and the PRD's `state:` is unchanged
- [x] `--dry` with a valid `--route` prints the dry line and leaves the
      library exactly as it was

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 -m py_compile resources/board/specs.py
bash .pearde/prds/the-board-asks-for-itself/a-route-is-written-at-spec-time/probe/route.sh
echo spec02 ok
```
