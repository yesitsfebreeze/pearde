# Central cartridge development board

This board coordinates the source-owner boards stored beside it in
`prd.ctg/.cartridge/boards/`. PRD owns planning, specifications, dependencies,
Gantt scheduling, reviews and orchestration. Source cartridges own implementation,
tests and domain documentation; they contain no planning engine or board.

The [settings](settings.md) preserve the existing member aliases and declare
explicit source repositories. Every PRD declares its implementation `repo:`.
Cross-owner dependencies resolve from this root board. Run planning through
the PRD cartridge entry point; a scan only observes the board.

The [source map](work-map.json) preserves180 reviewed inventory entries.
The complete migration contains182 actual PRDs, including two records outside
that inventory. [Migration evidence](../../reports/record-migration/README.md)
records all original IDs, metadata and digests, plus385 native work records and
one question. Original review scores remain historical; moving inputs makes
their bindings stale and does not authorize implementation.

Use the shared [development workflow](../../workflows/develop-one-cartridge.md),
[plan review](../../workflows/review-plan.md), and [templates](../../templates/README.md).
The agent rates plans. Code lands in its source repository after independent
verification; planning evidence and transitions remain centrally owned.

## Keep cartridge roots small

Keep authored Markdown and development support inside their owner's
`.cartridge/`. Planning artifacts belong to PRD. Source-specific tests, fixtures,
scripts and domain documentation belong to their source cartridge. Keep required
root entry points minimal. Preserve unrelated changes and existing claims.

Historical assessment and review documents retain their evidence and dates;
the current PRD contracts, source mappings and observed results govern execution.
