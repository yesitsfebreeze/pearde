# report — an-analyst-workflow-does-not-survive-into-specced (implementer)

Verdict: **DONE**. One spec, `specs/spec01.md` — all 6 acceptance boxes
ticked against fresh output. Repo gate passed. Nothing failed.

## What I did

Nothing in the code was left to write. The build already stands uncommitted
in `resources/board/specs.py` (the analyst's pass one): the `read_specs`
six-tuple carrying the specs' `workflow:` slugs, the derivation block after
the size gate (flag absent and PRD key absent — a commented `# workflow:`
counts as absent — one distinct slug written up via `edit.set_key`; two
distinct slugs write none with the stderr note; no slugs, silent), the
`dry · workflow: <slug>` line, and the docstring paragraph. My run was
re-verification: both harnesses, the spec's Verify and Proof block, the repo
gate, then the boxes ticked as I closed them.

## Verify output (2026-08-31 22:31+)

- Verify and Proof block (`bash -e -o pipefail`): `grep -n
  "dict.fromkeys(spec_wfs)"` → `563:        seen = list(dict.fromkeys(spec_wfs))`.
- Probe harness `probe/verify.sh`: **21/21 checks pass**. The "ok" lines are
  quoted into the boxes in `specs/spec01.md` as they were ticked.
- `specced-is-a-command/probe/verify.sh`: **90/90 checks pass**, including
  `--workflow none is refused outright`.
- Repo gate: `bash resources/doctor.sh` → exit 0. `python3 resources/index.py
  check` → rc 0, silent. `python3 resources/workflows.py check .pearde` →
  rc 0, silent.

One cosmetic, inside the probe harness, not the footprint: verify.sh line 88
runs `rm "$B/prds/keeps"` (missing `-rf` first), so the harness prints
`rm: … /prds/keeps: is a directory` on stderr between the flag and
ambiguous sections. Harmless — the next `rm -rf` cleans up and no check
depends on the ordering. Outside my footprint; noted, not fixed.

## Decisions honoured

- **`--workflow none` refuses outright** — the analyst's report flagged it,
  the orchestrator confirmed: dead deletion branches were deliberately
  preserved, so the refusal stands; the flag wins wherever the command
  accepts it at all. Not re-armed.
- The two-slug ambiguity: key left unset, note on stderr naming both slugs
  (box 3, passed).

## Scope notes

- My footprint is `resources/board/specs.py` only; I did not edit it. Dirty
  sibling files (`collect.py`, `plan.py`, `transitions.py`, `doctor.sh`,
  `questions.py`) are other rounds' uncommitted work — HEAD is `7809756`,
  the analyst's baseline note about them still holds.
- `doctor`'s `origin` row reads `broken` (7 derived vs 4 requested) —
  pre-existing, outside my scope, no fix.
- Nothing outside
  `.pearde/prds/an-analyst-workflow-does-not-survive-into-specced/` and the
  footprint was written. Nothing committed. No facts from outside this repo
  were learned; no knowledge record to write.
