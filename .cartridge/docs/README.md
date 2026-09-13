# PRD cartridge

The planning engine runs natively on Bun. `src/` contains the maintained engine;
`.cartridge/boards/` contains the planning records and `.cartridge/tests/` its tests.
No installed Pearde or Python interpreter is required.

From the composition root, run `just prd help`, `just prd scan`,
`just prd plan --json`, or `just prd check`. Select a source owner with
`--board memory` (or another registered board). The root board composes members.
The `run` launcher exposes the Cartridge JSON-line process protocol.

The engine supports dependency planning, bounded work waves, Gantt output,
record edits and refinement, specification publication, claims, isolated Git
lanes, verified collection, and rolling execution through configured adapters.
A successful worker exit alone cannot mark work done: collection checks the
acceptance state, declared footprint, verification commands and integrated Git
revision. Record edits preserve prose and use revision guards and process locks.

Adapter execution is explicit: `run --dry` needs no agent; a real run requires a
configured adapter in `.cartridge/adapters/`. Cancellation and deadlines stop
owned worker processes. The host service limits jobs, input and output, scopes
journals to sessions, and publishes verified evidence with bounded retries.

This is the Cartridge planning surface, not command-for-command compatibility
with the former vendored CLI. Ancillary memo, grammar and workflow authoring stays
in the memo system; the engine exposes inspection and validation of those records.
Historical upstream work remains separate from the active registered boards.

Run `bun run check` and `bun run test`. Set `CARTRIDGE_TEST_BIN` to the built runtime
to include the real host integration test. Fixtures use temporary repositories and
local processes. External agent and model calls are not needed for these tests.

Use [the review workflow](../workflows/review-plan.md) before implementation.
Keep PRDs small, bind scores to their reviewed revisions, require at least 90/100,
and allow at most five substantive rounds. Existing migration reviews marked
stale require review before they authorize new work.
