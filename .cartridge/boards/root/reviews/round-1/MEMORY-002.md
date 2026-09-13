# Open memory-engine work

What is still open. Finished items are not kept here — the commit that closed
one carries its reasoning, and measured results live in
[tests/bench/RESULTS.md](tests/bench/RESULTS.md).

## MEMORY-002 — Finish consistent memory terminology

Priority: lower. Status: existing work in `codex/memory-terminology`; retain the
`memory-memory-terminology` worktree while used or reserved by its owner.

Why: storage temperature and daemon loading are implementation details that can
confuse the distinction between all persisted memory, its active working set,
and whether a project daemon is loaded. Commits `0d3ce338` and `15862820` contain
useful wording and status work, but also broad API renaming against an older base.

Acceptance:

- Reconcile user-facing status, CLI help and documentation with current `main`:
  stored memory, active memory, and loaded/unloaded project daemons must have
  distinct meanings. Counts must describe the actual sets they measure.
- Preserve current complete hot/cold exports, history, recall diagnostics,
  `check`/`repair`, audit and hot reload. Do not restore older export wording or
  imply that only active memory is backed up.
- Keep existing database keys and frozen layout decoders compatible. An internal
  API rename must not silently create new tables or leave old memory unreadable.
- Review each API change for necessity; prioritize clarity in the CLI over
  mechanical renaming throughout the repository. Validate legacy-store fixtures,
  active/stored counts, CLI/RPC consistency, and `just all` before installation.

## MEMORY-004 — Ranking on a spilled store

Priority: open, unowned. Raised by the mature-store measurement in
[RESULTS.md](tests/bench/RESULTS.md) (`5d003879`), not acted on there.

Cold rows have no resident traversable edges, so on a half- or fully-cold store
the graph legs of the full pipeline contribute nothing while their candidates
still enter the fusion and displace hits that would have answered. Measured
cost: `linked_evidence` MRR 0.53 against plain fusion's 0.92 in the mixed layout,
which is the whole of the full pipeline's deficit there. Hot, the same questions
score 0.967.

Acceptance:

- Decide where the fix belongs: expansion crediting cold rows, fusion weighting
  each leg by what is actually resident, or neither — with the reasoning written
  down either way.
- Measure any change on the mature fixture in all three layouts plus the
  authored replay corpus, and do not trade current/historical recall (perfect
  today in every layout) for linked-evidence rank.
- This is one ranking question, not a default switch. A default for every store
  still needs a real long-lived one; the fixture's maturity is synthesised.

## Not carried forward

Memo/insights/desktop/voice UI, intake workflows, model hosting or routing, MCP
hosting, orchestration, plugin integrations and host lane automation stay out of
this repository.

Removed worktrees are archived outside the repo at
`~/dev/memory-worktree-archives/inactive-20260911/`, with the cleanup record and
per-tree disposition beside them. Archived branches are recovery references, not
a backlog.
