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

Proven by `.pearde/prds/the-promotion-rule/probe/verify.sh` — 11 pinned
checks, the harness the doctor's `harnesses` row runs — and by
`.pearde/prds/the-promotion-rule/probe/probe_promotion_rule.py`, both run
against throwaway `workflows/` libraries built at run time (never under
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
- A slug the library does not hold, an atomic naming its **own** slug, and the
  same sentence sitting in `## Fails when` rather than `## Do` all pass clean —
  the refusal reads one section and asks the library, so it names only a pair
  a reader could actually confuse for a route.

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
  doctor `workflows` row report the same counts before and after this
  change — the real library holds no pair this rule catches yet. Quoted:
  `  workflows   broken  7 workflows · 23 atomics · 4 problems`, identical
  on the tree without this change; the `broken · 4 problems` tail is the
  inherited `report_workflow_counts` check a later pass on main added (4
  lines naming `implementer-continue.md`, `probe-then-spec.md` and two
  `report.md` headings), not this rule — this rule's lines
  (`routes to … by slug`) are 0 in that output.
- [x] `python3 resources/index.py check` on the changed tree names no line
  beyond the two pre-existing ones inherited from before this PRD
  (`resources/common.py` with no manifest row; `hotreload-test.js` listed
  but absent) — this PRD's edit touches no manifest-relevant path. Quoted:
  pre/post scratch trees (main, main+this change) print identical maps
  (`diff` empty), none naming `workflows.py`, `workflow.md` or
  `atomic.doc.md`; in the lane the extra lines name `docs/` and
  `purge.py` paths untracked in the checkout, absent from the lane.

## Verify and Proof

```sh
ROOT="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"
BOARD=/Users/feb/dev/infra/pearde/.pearde
cd "$ROOT"

# the rule itself: a route refused with both names, every mention passing,
# the census empty, each reference file stating it once — 11 pinned checks
PEARDE_ROOT="$ROOT" bash "$BOARD/prds/the-promotion-rule/probe/verify.sh"
REPO="$ROOT" python3 "$BOARD/prds/the-promotion-rule/probe/probe_promotion_rule.py" \
  | grep -c '^\[ok\]' | grep -qx 4

# the library carries no pair this rule catches — the census of OUR refusals
# is empty. The check as a whole is a board-wide gate: it now also carries
# `report_workflow_counts` problems (4, inherited from a later pass on main
# that is not this PRD's), so capture and gate on this rule's lines only
CENSUS="$(PEARDE_ROOT="$ROOT" python3 resources/workflows.py check "$BOARD" 2>&1 || true)"
[ "$(printf '%s\n' "$CENSUS" | grep -c 'routes to .* by slug')" = 0 ]

# the doctor's `workflows` row reads the same counts as before this change —
# captured, then asserted from its text (the row's `ok`/`broken` word and the
# 4-problem tail belong to the inherited report-count check, not this rule)
DOC="$(PEARDE_ROOT="$ROOT" bash resources/doctor.sh "$BOARD" 2>&1 || true)"
printf '%s\n' "$DOC" | grep -qE '^  workflows +\w+ +7 workflows · 23 atomics'

# the map gains no line naming a path in this footprint (a board-wide gate:
# other lines name untracked-checkout files the lane does not hold — capture,
# then gate on this footprint only)
MAP="$(PEARDE_ROOT="$ROOT" python3 resources/index.py check || true)"
[ "$(printf '%s\n' "$MAP" | grep -c 'workflows\.py\|workflow\.md\|atomic\.doc\.md')" = 0 ]
```
