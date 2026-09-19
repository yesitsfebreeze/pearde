---
state: "analyzing"
origin: requested
priority: 35
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: repo-checks-cartridge-exists
footprint:
  - "checks.ctg"
claim: "coordinator-78-6 2026-09-19T12:31:08.562Z"
---

# The checks cartridge exists and runs a repository's declared checks

## Outcome

`checks.ctg` exists as a cartridge in its own right: it discovers the checks a
repository already declares, records them, selects the ones a change warrants,
and runs that selection. Everything lives under `checks.ctg` and nothing outside
it is touched, so this child can land while the superproject's own files are
held by other work.

Discovery reads what is already there — package scripts, Makefile and justfile
targets, cargo, go and pytest markers, and a repository's own probe script — and
records the result so a later session reads the set instead of rediscovering it.
The post-pass after a change runs the change's own verify plus the checks
reaching the changed files, never the whole suite. A full run is a separate,
explicit operation that the post-pass never triggers.

This is the parent's port of pi's `rigor`, reimplemented rather than copied. The
two deliberate divergences from upstream stand: the discovered set is recorded
through the composition's own record ownership rather than a second project-local
JSON store, and the checks run in-process instead of dispatching a sub-agent.

## Acceptance

- [ ] Discovery run against fixture repositories carrying a justfile, a package.json scripts block, a Makefile, a Cargo manifest and a pytest layout records each declared check with the command that runs it and the source file it was discovered from.
- [ ] A repository declaring no check at all records an empty set and reports that, rather than inventing a command.
- [ ] The post-pass for a change selects only the checks reaching the changed files plus the change's declared verify, and the selection is reported before anything runs.
- [ ] A failing check reports the check name, its command, and its output, and the post-pass stops at the first failure rather than running the remainder.
- [ ] The full gate is reachable as an explicit operation and is never run by the post-pass.
- [ ] Discovery and selection are tested offline, against fixtures built inside the test with no network reachable from any of them, and the tests are run here through `cargo` against the manifest path directly.
- [ ] The cartridge ships its own `README.md` and `.cartridge/help.md`, and `cartridge.json` declares its whole surface.

## Proof and recovery

Port from `/Users/feb/dev/pi/packages/coding-agent/src/core/rigor/` (542 lines at
survey). Read and reimplemented; no upstream file is copied into this repository,
and no path reaching a sibling `*.ctg` appears anywhere under `checks.ctg`.

The gates named on the parent — `just test checks`, `just check checks`,
`just audit checks` — do not resolve until the sibling child
`the-checks-cartridge-is-registered-in-the-composition` lands, because the owner
target lists, the composition profile and the submodule registration all live in
superproject files outside this footprint. That is why this child is gated by
`cargo` against `checks.ctg/Cargo.toml` directly, which needs no registration,
and why the parent's `just test checks` acceptance rides with the sibling child
rather than with this one.

Recovery: the whole footprint is one directory that does not exist today, so
abandoning this child removes it without touching anything else.
