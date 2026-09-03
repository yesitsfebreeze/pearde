---
complexity: 12
footprint:
  - resources/workflows.py
  - references/workflow.md
  - references/templates/atomic.doc.md
---

# spec01 — an atomic that routes to another atomic by slug is refused, inline it or promote it

`workflows.py check()` now flags an atomic whose `## Do` section hands off to
another atomic by name — `run \`<slug>\`` or `then run the \`<slug>\` atomic`
— with `` `## Do` routes to `<slug>` by slug — route it (a workflow with two
atomics) or inline it (prose, one unit again) ``. The doctor's `workflows` row
carries the refusal as it already carries every other library problem — no
new row, no new command. A slug named in a sentence with no routing verb
("compare with the `<slug>` atomic") is left alone: the new `ROUTE_RE`
pattern matches the verb, not the slug, so a comparison never trips it.
`references/workflow.md`'s `## The check` list and
`references/templates/atomic.doc.md` each carry the rule once, so an author
and the doctor row read the same sentence.

Already built and proven in
`.pearde/prds/the-promotion-rule/probe/probe_promotion_rule.py`, run against
throwaway `workflows/` libraries built at run time (never under
`.pearde/prds/`):

- A bare `1. Run \`reproduce-the-failure\`.` step in an atomic's `## Do`
  fails the check, naming the routed slug.
- `1. First set up the fixture, then run the \`reproduce-the-failure\`
  atomic.` fails the same way — the routing verb is found anywhere in the
  step, not only as the step's first word.
- `1. Compare with the \`reproduce-the-failure\` atomic to see the shape.`
  passes clean — a mention with no routing verb is prose, not a route.
- A step naming a command that happens to share no atomic's slug (`1. Run
  \`pytest tests/\`.`) passes clean.

Run against the real board's library (`/Users/feb/dev/infra/pearde/.pearde`,
7 workflows, 23 atomics) both before and after the edit, `workflows.py check`
prints nothing new — the census this PRD's `## Done when` asks for is empty:
no existing atomic currently routes to another by slug, so there is nothing
left to inline or promote by hand.

## Acceptance

- [x] An atomic `## Do` step matching the routing verb (`run`, `then run`,
  optionally `the … atomic`) followed by a backtick slug that names another
  atomic in the same library fails `workflows.py check()`, naming both the
  atomic and the routed-to slug.
- [x] The same step rewritten as prose with no routing verb, or naming a
  slug absent from the library, passes clean.
- [x] `references/workflow.md`'s `## The check` list and
  `references/templates/atomic.doc.md` each state the rule once, in the
  file's own words for its own reader (the check's failure list; the
  template's fill-in guidance).
- [x] `workflows.py check(/Users/feb/dev/infra/pearde/.pearde)` and the
  doctor `workflows` row report the same counts and `ok` before and after
  this change — the real library holds no pair the rule catches yet.
- [x] `python3 resources/index.py check` on the changed tree names no line
  beyond the two pre-existing ones inherited from before this PRD
  (`resources/common.py` with no manifest row; `hotreload-test.js` listed
  but absent) — this PRD's edit touches no manifest-relevant path.

## Verify and Proof

```sh
cd <repo>
python3 .pearde/prds/the-promotion-rule/probe/probe_promotion_rule.py

python3 resources/workflows.py check /Users/feb/dev/infra/pearde/.pearde
PEARDE_ROOT="$PWD" bash resources/doctor.sh | grep -A1 '^  workflows'
python3 resources/index.py check
```
