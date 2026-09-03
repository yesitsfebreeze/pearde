Verdict: SPECCED

## Summary

Built the contract in `resources/board/vision.py`: `vision_axis` no longer
folds `edges:` into the `after` graph that decides depth/reach — that graph
is `needs:` (plus a parent's children) alone now. An edge whose two ends
both resolve to real PRDs but whose `needs:` does not already carry the
same hop is reported the way a dangling terminal is: `"the vision says
<to> needs <from>; <to> does not"`, read by `plan.py vision --check` and
`doctor`'s `vision` row. An edge end naming no PRD is still reported the
old way, unchanged. Updated `doctor.sh`'s `vision broken` row wording (it
said "N names … resolve to no PRD", false for the new report type),
`references/parts/order.md` and `references/templates/vision.doc.md` (both
said depth reads "`needs:` plus `edges:`"; both now say `needs:` alone).
11/11 new probe assertions pass; `resources/index.py check` shows the same
3 pre-existing, unrelated findings as before the edit.

## Finding

A different, already-`done` PRD's committed harness
(`prds/the-board-runs-itself/vision-is-first-class/probe/verify.sh`)
encodes the old edges-as-hop contract directly and now fails 5 of its 52
assertions against this PRD's own footprint — not a regression this PRD
caused, but that file testing a contract this PRD was explicitly asked to
replace. Left untouched (out of this PRD's scope/footprint); full detail
and the exact failing lines are in `specs/spec01.md` under "Finding". That
file also has a pre-existing, unrelated bug (`doctor.sh "$D"` instead of
`"$B"`) that happened to flip two long-standing failures to passing as a
side effect of this edit re-ordering axis counts on its fixture — also not
this PRD's to fix.

Spec list: `specs/spec01.md` (complexity 12) — the whole contract.

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec
