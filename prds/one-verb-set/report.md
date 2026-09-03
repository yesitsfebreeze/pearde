Verdict: SPECCED

## Summary

Built the whole contract in the lane (`.pearde/.lanes/one-verb-set`):
`scout.sh` now dispatches all seven verbs — `sweep`, `delta`, `trending`,
`tool`, `find`, `reading`, `quality` — from one `registry` function that also
prints when it is run with no argument. `toolscout.sh` is now a one-line
compat entry (`exec scout.sh tool "$@"`); a direct query with no args to
either produces byte-identical stdout/stderr/exit code. `find` forwards to
`route.sh` (`route.sh list` still reports 45 routes, unchanged), `reading`
prints `reading-list.md`, `quality` lists `templates/` and what each gate
wires in. Every verb's last line names its landing file, or says plainly
that none is kept. Wrote `resources/scout/check.sh`, the doctor-style guard
the PRD's `Fails when` box asks for: it diffs `scout.sh`'s own table against
README.md's new Commands table and fails loudly on drift — mutation-tested
against both `scout.sh` and README.md.

One real defect surfaced and was fixed: `delta`'s pipeline into `head -40`
died of `SIGPIPE` on any diff over 40 rows, and `pipefail` turned that
ordinary truncation into a `set -e` abort that skipped the line printed
after it. `pipefail` is now off around that one pipeline only. Reproduced on
this repo's own `2026-08-25 -> 2026-08-28` snapshots (exit 141 before, 0
after) before writing the spec.

All acceptance boxes pass now; `pearde specced one-verb-set --check --as
an-one-verb-set` returns ok, complexity 12.

## Finding — a live collision on the same file

`.pearde/prds/every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh`
is an already-built harness for a **different, sibling PRD** whose contract
requires `resources/scout/README.md` (and other `resources/scout/*.md` +
`references/skills/*.md`) to keep the *exact same* table-row count as commit
`9889e78` and to *shrink* in total word count. Run against this lane
(`LANE=<this lane> bash <that verify.sh>`) it now fails three of its boxes
(`spec02.4` README row count, `spec02.5` index.py output, `spec02.6` word
count) — because this PRD's Done-when literally requires a *new* Commands
table in that same README, which that sibling's contract forbids adding.
These two PRDs cannot both fully pass as written; whoever sequences them
needs to either run the densifying PRD after this one lands (so it
densifies the merged README, table included) or explicitly except the new
table from its row-count check. Not something I can resolve from inside
this PRD's footprint — reported, not fixed.

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec
