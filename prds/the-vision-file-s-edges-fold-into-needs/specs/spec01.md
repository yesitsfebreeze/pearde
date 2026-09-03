---
complexity: 12
workflow: probe-then-spec
footprint:
  - resources/board/vision.py
  - resources/doctor.sh
  - references/parts/order.md
  - references/templates/vision.doc.md
  - prds/the-vision-file-s-edges-fold-into-needs/probe
---

# spec01 — `edges:` stops feeding the axis and becomes a check on `needs:`

`vision_axis` no longer folds a vision-declared edge into the `after` graph
that `needs:` builds — depth and reach are computed from `needs:` (plus a
parent's children) alone. An edge whose two ends both resolve to real PRDs
but whose `needs:` does not already carry the same hop is reported the way
a dangling terminal is: `"the vision says <to> needs <from>; <to> does
not"`. An edge end naming no PRD is still reported the old way. `doctor`'s
`vision` row and `plan.py vision --check` carry both kinds of report
without claiming a wrong reason for either.

## What stands from the probe

All of it is in the tree, uncommitted:

- `resources/board/vision.py` — `vision_axis`'s `needs:`/children loop
  (building `after`) is unchanged; the `edges:` loop no longer calls
  `after[ra].add(rb)`. Where both ends resolve and `ra != rb`, it instead
  checks `rb not in after[ra]` (built from `needs:` alone, above this loop)
  and appends `f"the vision says {b} needs {a}; {b} does not"` to
  `dangling` when true. The dangling-end case (`bad`) is untouched.
- `resources/doctor.sh` — the `vision broken` row said "N names … resolve
  to no PRD", which was false for the new report (both names *do*
  resolve). The row now reads "N problem(s) in vision.md", and the `fix`
  line covers both causes: a name to spell as `needs:` would, or a
  `needs:` line an edge names.
- `references/parts/order.md` and `references/templates/vision.doc.md` —
  both said depth is computed "over `needs:` plus `edges:`"; both now say
  `needs:` alone, with `edges:` named as the check.
- `prds/the-vision-file-s-edges-fold-into-needs/probe/verify.sh` — 11
  assertions: byte-identical `vision`/`vision --json` output with a fully
  `needs:`-declared edge present or absent; an edge alone no longer
  deepens the axis; an undeclared edge is reported PRD-named by both
  `vision --check` and `doctor`, and a matching `needs:` silences it; a
  dangling edge end is still reported the old way.

## What is left

Nothing — the probe is the whole contract, at the size this PRD asked for.

## Finding — a sibling PRD's committed probe now expects the old behaviour

`prds/the-board-runs-itself/vision-is-first-class/probe/verify.sh` (a
different, already-`done` PRD) asserts the old edges-as-hop semantics
directly: `"an edge is a hop: next at 2"`, `"a needs: is a hop: building at
3"`, `"a done terminal costs no hop: asking at 0"`, and a scan count
(`axis: 5 on · 1 off`) that only held when an edge added a hop `needs:`
had not declared. It also asserts the doctor row's exact old wording
(`"2 names in vision.md resolve to no PRD"`). All five now fail against
this PRD's own footprint — not a regression in what this PRD builds, but
that PRD's test encoding a contract this PRD is explicitly asked to
replace (`## The change`, PRD body). Out of this PRD's footprint and not
touched here; reported for the orchestrator to route (update those five
assertions to the new contract, or fold them into this PRD's probe and
retire the duplicate coverage).

`prds/the-board-runs-itself/vision-is-first-class/probe/verify.sh` also
calls `doctor.sh "$D"` (the fixture's parent dir) rather than `"$B"` (the
actual `.pearde` inside it) in its "dangling names" section — a
pre-existing bug in that same file, unconnected to `edges:`, noted here
only because it happened to flip two long-standing failures
(`doctor: vision ok`, `doctor: vision off`) to passing as a side effect of
this PRD's edit re-ordering axis counts on that fixture. Not this PRD's to
fix.

## Acceptance

- [x] `bash prds/the-vision-file-s-edges-fold-into-needs/probe/verify.sh` ends `verify: 11/11 checks pass`
- [x] A board with `terminals: [leaf]`, `leaf` declaring `needs: [root]`, and `edges: ["root -> leaf"]` prints byte-identical `vision` and `vision --json` output whether the `edges:` line is present or removed
- [x] A board with an edge `"other -> leaf"` and no matching `needs:` on `leaf`: `vision --check` exits 1 and prints `the vision says leaf needs other; leaf does not`; `doctor`'s `vision` row carries the same line; adding `needs: [other]` to `leaf` makes `vision --check` exit 0
- [x] The same board with the edge naming a PRD that does not exist (`"ghost -> leaf"`) still prints `edge ghost -> leaf: ghost names no PRD` and exits 1
- [x] `grep -c 'after\[ra\].add(rb)' resources/board/vision.py` prints `0`

## Verify and Proof

```sh
bash prds/the-vision-file-s-edges-fold-into-needs/probe/verify.sh
grep -c 'after\[ra\].add(rb)' resources/board/vision.py
python3 -c "import py_compile; py_compile.compile('resources/board/vision.py', doraise=True)"
python3 resources/index.py check
```
