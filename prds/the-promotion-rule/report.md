Verdict: SPECCED

## Route

workflow: probe-then-spec (no new workflow needed — the library already
holds the fit: "an open PRD, from its contract to specs written from a
build")

## What the build did

Followed `probe-then-spec`. `python3 resources/knowledge.py query` against
the contract's own text returned no gap-closing hit (104 loose matches, none
on point) — nothing auto-enqueued. Read `.pearde/prds/the-promotion-rule/prd.md`
(no `## Answers`) and the source page it names,
`docs/content/docs/improvements/workflows-promotion.mdx` — still on disk,
word-for-word the PRD's own body, so no recovery from git 6839a9b was
needed.

The build target is `resources/workflows.py`'s `check()`, the function the
doctor's `workflows` row already runs. Added `_routed_atoms()` and a
`ROUTE_RE` pattern: a `## Do` step containing a routing verb (`run`, `then
run`, optionally `… the <slug> atomic`) followed by a backtick slug that
names another atomic in the same library is a route, refused with "route it
… or inline it". A slug merely mentioned in prose with no routing verb
("compare with the `<slug>` atomic" — the PRD's own guard example) is left
alone, because the pattern matches the verb, not the slug.

Proved in `.pearde/prds/the-promotion-rule/probe/probe_promotion_rule.py`
against throwaway `workflows/` libraries built at run time: a bare route, a
route with a lead-in clause, a prose comparison, and an unrelated command all
land on the expected side of the rule.

Ran the check against the real board's library
(`/Users/feb/dev/infra/pearde/.pearde`, 7 workflows, 23 atomics) before and
after: `ok`, same counts, nothing new — the census the PRD's `## Done when`
asks for is empty today, so there is no existing pair to decide by hand.
`python3 resources/index.py check` and `PEARDE_ROOT=<lane> bash
resources/doctor.sh` were run before and after; the only broken rows
(`index`, `claims`, `vault`, `origin`, `memos`, `knowledge`, `questions`) are
pre-existing, board-wide, and outside this PRD's footprint — unchanged by
the edit.

Wrote the rule once into the template's doc (`references/templates/atomic.doc.md`,
under `## Do`, next to the existing "and then is two atomics" sentence) and
once into the check's own failure list (`references/workflow.md`'s `## The
check`), per the contract's "checked by the doctor row and written once into
the template's doc."

## Findings (not specced)

- `docs/content/docs/improvements/workflows-promotion.mdx` still carries the
  page this PRD files from; the PRD's italic recovery note ("it left the
  working tree… recover at git 6839a9b") is stale — the file was present the
  whole time. Not a spec: nothing to build from a correction to a comment.

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec
