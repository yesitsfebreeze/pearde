---
state: done
origin: requested
priority: 26
complexity: 15
blast-radius: mid
workflow: probe-then-spec
---


# Enforce pointer-not-verdict

*Source: `docs/content/docs/improvements/health-pointer-verdict.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** health · **Axis:** sensibility (7 → 8) · **Pulls the score up by
~3 points**

## Why now

"A score is a pointer, never a verdict: where to look and what pulls the
file down. Whether the file changes is the PRD's call." The reference states
it, the note format follows it, the ranking keeps it — and one part of the
machine contradicts it: the brief *names the unhealthy*, and the brief is a
worker's instruction. A file named in the brief is a file the worker is
pushed to change, verdict-shaped, whatever the prose says. The enforcement
the rule asks for — that the score never promotes work by itself — exists
nowhere.

## The change

The brief keeps naming the unhealthy file, and gains the pointer's shape:
the one line names *why* — the file's worst axis and its note's path —
never "fix this". The health page drops the phrase "worst first on one page
— so a monolith is named before a worker meets it" wherever it implies
score-ordered dispatch: the plan's order is untouched by scores, and the
reference says so once, in the one place. What was three statements becomes
one mechanism (the note in the brief) and zero decrees.

## Done when

- A brief for a PRD whose footprint includes an unhealthy file names the
  file with its note path and worst axis — and the plan's ordering is
  byte-identical before and after (scores never reorder).
- The reference carries the rule once, where the brief's contract is
  written — the other two statements are gone, not weakened.
- A board with `health-floor: 100` (everything named) still plans
  identically to `health-floor: 1` — the check is the byte-diff.

## Fails when

- The pointer keeps its weight but loses its anchor — naming the file
  without the note path. Guard: the brief refuses to name a file whose
  note is missing, the same way it refuses a missing spec.

## What stays out

No change to the six axes, the weights or the floor — the scoring is
sound; only the one contradiction between the rule and its one
score-shaped use is resolved.

## History

**failed, retried 2026-09-03 21:37**

**2026-09-03 21:4x — the claim is dead; the report is the analyst's**

The report on disk is the analyst's SPECCED (mtime earlier than the claim's
`since`), so no implementer ever returned. The worker's session was reaped —
no process on this machine holds it. The claim only reads live because its
footprint names shared files other sessions keep writing
(`silence-measures-the-workers-own-tree` names the artefact). The analyst's
work stands in `specs/`; the next implementer continues from it.

## Blocked

**2026-09-03 21:56 — the lane will not rebase**

`lane/enforce-pointer-not-verdict` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/enforce-pointer-not-verdict` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock enforce-pointer-not-verdict`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/enforce-pointer-not-verdict` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/enforce-pointer-not-verdict` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock enforce-pointer-not-verdict`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/enforce-pointer-not-verdict` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/enforce-pointer-not-verdict` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock enforce-pointer-not-verdict`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/enforce-pointer-not-verdict` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/enforce-pointer-not-verdict` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock enforce-pointer-not-verdict`.

**2026-09-04 02:43 — the lane will not rebase**

`lane/enforce-pointer-not-verdict` does not land on `session/s85810`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/enforce-pointer-not-verdict` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock enforce-pointer-not-verdict`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/enforce-pointer-not-verdict` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/enforce-pointer-not-verdict` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock enforce-pointer-not-verdict`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/enforce-pointer-not-verdict` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/enforce-pointer-not-verdict` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock enforce-pointer-not-verdict`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/enforce-pointer-not-verdict` does not land on `session/s85810`; 1 file(s) disagree:

- `references/skills/pearde-health.md`

Nothing is lost: the worker's commits are on `lane/enforce-pointer-not-verdict` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock enforce-pointer-not-verdict`.

## Report

spec01: exit 0
== 1/3 score + list names axis and note path ==
 63  small.py  branching, longest
1 scored · 1 on the ranking · 0 skipped · 1 under 90 · graph none (no .pearde/graphify/graph.json)
 63  small.py  branching, longest  .pearde/health/files/small.py.md
PASS: score, worst axis and note path all on one line
== 2/3 missing note is named as missing, never silently dropped ==
 63  small.py  no note at .pearde/health/files/small.py.md — `pearde health score` writes one
PASS: a file whose note is gone is named as missing its note, not silently
== 3/3 plan.py scan is byte-identical across health-floor 1 and 100 ==
PASS: plan.py scan is byte-identical, health-floor: 1 vs 100

ALL PASS
workers.md sound
pointer rule stated once, in references/health.md
.gitattributes is on disk with no row in references/files.md
resources/board/obsidian_register.py is on disk with no row in references/files.md
references/files.md lists @docs/.gitignore — not on disk
references/files.md lists @docs/next.config.mjs — not on disk
references/files.md lists @docs/package-lock.json — not on disk
references/files.md lists @docs/package.json — not on disk
references/files.md lists @docs/postcss.config.mjs — not on disk
references/files.md lists @docs/tsconfig.json — not on disk
references/files.md lists @resources/board/purge.py — not on disk
references/files.md lists @docs/app/ — no such directory
references/files.md lists @docs/components/ — no such directory
references/files.md lists @docs/content/ — no such directory
references/files.md lists @docs/content/docs/board/ — no such directory
references/files.md lists @docs/content/docs/health/ — no such directory
references/files.md lists @docs/content/docs/improvements/ — no such directory
references/files.md lists @docs/content/docs/knowledge/ — no such directory
references/files.md lists @docs/content/docs/obsidian/ — no such directory
references/files.md lists @docs/content/docs/scout/ — no such directory
references/files.md lists @docs/content/docs/view/ — no such directory
references/files.md lists @docs/content/docs/workflows/ — no such directory
references/files.md lists @docs/lib/ — no such directory
@@view names @resources/board/hotreload-test.js — not on disk
capabilities.md names `zzdead` — no such verb
`be` is a verb with no row in capabilities.md
references/files.md references @@docs — no such keyword
references/files.md references @resources/board/purge.py — not on disk
references/parts/handles.md references @@purge — no such keyword
references/parts/handles.md references @resources/board/purge.py — not on disk
stale: graph d8b509c is newer than the ranking's 16b0f5b — `pearde health score`
