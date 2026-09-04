Verdict: SPECCED

## Build

Read the PRD (its body is the docs page
`docs/content/docs/improvements/lifecycle-contract.mdx`). Ran
`python3 resources/knowledge.py query` against the contract; 104 hits, none
close — no gap enqueued (`.pearde/wiki/pending/` unchanged after the
query). Ran `python3 resources/workflows.py list` and followed
`probe-then-spec` (open PRD, contract to specs from a build).

The verb and its docs page were already built ahead of this pass —
uncommitted, in the checkout this lane was cut from
(`resources/board/purge.py`, `docs/content/docs/improvements/
lifecycle-contract.mdx`, plus draft hunks to `index.md`, `references/
files.md`, `references/parts/handles.md` and `resources/doctor.sh`,
timestamped 17:45-18:04, before this claim). This is a resume, not a
fresh build: reproduced the whole thing in the lane
(`.pearde/.lanes/the-lifecycle-contract-and-purge-reclaims-it`, the `repo:`
this brief names), wrote a probe under this PRD's own `probe/` (nothing
existed there before), and ran it.

The probe (`probe/probe.py`, run via `probe/verify.sh`) found two real
defects in the already-standing build, both fixed in the lane's copy of
`purge.py`:

1. **`--reap-cap` did not reach the candidate list.** `scan()` computed
   which reaped refs are "over the cap" against `cap_of(board)`
   unconditionally; `run()`'s `reap_cap` override only relabelled the
   printed number. `pearde purge --apply --reap-cap 3` still dropped refs
   down to 8. `scan()` now takes `reap_cap=` and both `run()` and
   `cmd_json()` pass their override through it. Probe: `got: 8, want: 3`
   before the fix, `ok` after.
2. **`--apply --json` never applied.** `cmd_purge` routes `--json` to
   `cmd_json`, which only ever called `scan()` — the removal loop lived
   only in `run()`. `pearde purge --apply --json` printed `"applied":
   true` and removed nothing. The apply loop is now `_apply(board, rows)`,
   called by both `run()` and `cmd_json()`; each JSON action row now
   carries a `"did"` field naming what happened to it. Probe: the lane
   under test survived a `--apply --json` run before the fix, was gone
   after.

Wiring (`spec02`'s footprint) reproduced clean: `references/parts/
handles.md` and `references/files.md` each gained one row, `index.md`'s
`@@handles` gained `purge.py` and a new `@@purge` row was added,
`resources/doctor.sh` gained one read-only row between `plan` and
`harnesses`. `python3 resources/index.py check` on the lane prints the
same 3 lines before and after this pass's edits (`resources/common.py` no
manifest row, `references/files.md` names `hotreload-test.js` not on disk,
`@@view` names the same missing file) — all three pre-existing, none
this PRD's. `bash resources/doctor.sh /Users/feb/dev/infra/pearde/.pearde`
(read-only, no `--apply`, run from the lane) prints `purge ok 7 candidates
· every claim and registered board held`; no other row flipped state.
`pearde help` and `pearde purge --json` work with zero edits to
`pearde.py` — plain `COMMANDS` discovery.

## Finding — `docs/` carries no git history on this machine

Same finding another analyst pass on this board already recorded
(`enforce-pointer-not-verdict`'s report): `git ls-files docs/` returns
nothing on this branch — the whole fumadocs site, including
`docs/content/docs/improvements/lifecycle-contract.mdx` itself, exists
only as uncommitted content in the checkout this board's lanes are cut
from. `spec03`'s footprint is the one .mdx file alone; its acceptance
leaves the `meta.json`/`index.mdx` linkage open rather than editing two
files a separate, larger effort (`pearde-ships-as-a-product`'s docs axis)
is also mid-write on — editing them here would race that write, not join
it. The `@@purge` row added to `index.md` in this pass names only files
this repo tracks (`purge.py`, `session.py`, `lanes.py`, `handles.md`); the
draft that was already standing named `@docs/content/docs/improvements/`
too, which `index.py check` flags `not on disk` in any tree docs/ has not
landed in — dropped from the row rather than carried, since nothing in
the contract requires the map row to name it and a check that fails in
every lane until an unrelated PRD lands is not a check this pass should
add.

## Scores

complexity: 15
blast-radius: low
workflow: probe-then-spec
