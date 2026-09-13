# Planning templates

PRD owns all planning records and tooling. Create boards under
`prd.ctg/.cartridge/boards/<owner>/`; source cartridges keep their code,
domain documentation and tests. Never install a planning board, workflow,
dispatcher or PeaRDe copy into a source cartridge.

The central [root settings](../boards/root/settings.md) declare all owner
aliases. Each board settings file declares `require-repo: true`, its explicit
source repository, and the shared [workflow library](../workflows/develop-one-cartridge.md)
and [grammar](../grammar.md). Every PRD also declares an absolute `repo:` path:
the repository that owns implementation can differ from the planning repository.
Preserve the original member-qualified PRD identity across relocations.

Create [prd.md](prd.md) under the selected central board's `prds/<slug>/`.
Create [spec.md](spec.md) as `specs/specNN.md` only after investigation;
store [report.md](report.md) and [review.md](review.md) beside that PRD.
Plans, specs, reports and agent checkpoints stay under PRD's `.cartridge/`.
Source tests, fixtures and domain documentation stay with their source owner.

Initial state is `open`; use the engine transitions for `analyzing`, `refine`,
`question`, `specced`, `claimed`, `blocked`, `done` and `failed`.
An authored plan or checked structural validator is not completed work.

Apply [review-plan](../workflows/review-plan.md): an attributed agent review
of the current revision must score at least90/100 with no blockers, within
five rounds. The user delegated ratings to agents. Preserve rounds and history
when splitting or moving work; relocated review bindings remain stale until
the actual current inputs are reviewed. Never invent renewed approval.
