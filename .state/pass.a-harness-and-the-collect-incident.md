# Pass — one analyst collected, four forks out, and a data-loss incident on this checkout

## Established

- **`collect`'s rollback destroyed another session's uncommitted work at
  17:08.** Reflog `HEAD@{0}: reset: moving to 3587817` — `unland()` runs
  `git reset --hard` in the *orchestrator's* checkout, so sixteen verified-but-
  uncommitted files of `.../the-machine-is-the-run-verb` are gone and that PRD
  is `failed`, boxes 0/12. **No commit was lost; HEAD never moved.** Filed and
  claimed by another session as `collect-must-not-reset-the-checkout-it-did-not-write`,
  p95, `analyst-unland` since 17:14. Not mine — do not touch it.
- I snapshotted the checkout's whole uncommitted state before doing anything
  else: `.pearde/prds/a-harness-measures-the-tree-its-worker-built-in/probe/uncommitted-at-17-20.diff`
  (1670 lines) and `untracked-at-17-20.txt`. That is the only copy of the
  analyst's five-spec build outside the working tree.
- `a-harness-measures-the-tree-its-worker-built-in` is **specced** — 5 specs,
  complexity 32, sum 34 (under `split-above` 40), boxes 0/31, footprint = all
  59 board `verify.sh` plus `resources/doctor.sh`,
  `references/parts/workers.md` and two workflow files. No live footprint
  clash: the four PRDs owning those harnesses are `done`.
- Its analyst reproduced both contract claims and warns, in its own words, that
  **the checkout moved three times under the sweeps this session, board
  discovery is regressed there, and 15 harnesses it never touched are red.**
  Re-measure before believing any harness count taken now.
- `doctor origin` was **broken and is now ok** — 118 requested (33 live) · 28
  derived (1 live). Two derived PRDs had no `from:`; I added it to both. A
  derived PRD needs `from: <the PRD whose work surfaced it>` and `pearde add`
  cannot write it.
- **Three sessions are writing `.pearde/.state/pass.md` at once.** Mine was
  overwritten twice this pass (by `pearde-54`, then by a vault pass). The
  neighbour's file is preserved verbatim below rather than clobbered, and mine
  is also parked at `.state/pass.a-harness-and-the-collect-incident.md`.
- `sweep` 16:48 clean. `claim` takes the worker positionally; `add` wants
  `--body -` on stdin and has no `--origin`.

## Decided

- **Did not dispatch the implementer on the specced PRD, and did not claim
  `every-document-is-written-in-the-writer-s-prose`** — an override of "a pass
  never stops dispatching while a PRD is ready", made deliberately on four
  measured reasons: a live rollback that destroys uncommitted work in this
  checkout; a large uncommitted analyst build that a lane cut off HEAD would
  not carry (the documented trap); 15 unrelated red harnesses, so no verify
  block can be believed; and the analyst's own instruction to re-measure first.
  Rather than decide this alone I put it to the user as Q4 — the trade between
  speed and another session's work is theirs.
- Routed the worktree unit's findings without re-reading its report: findings 1
  (every harness computes `ROOT` from `$0`, so it can never read a lane) and 3
  (`nothing-left-open`'s `E14` globs `/tmp/pearde-index-*` machine-wide) are
  one contract, filed as the PRD above. Beat two PRDs and beat `deferred` —
  rule 1's consequence is nameable, and `a-check-decided-by-scheduling.md`
  already ruled E14's class folds into the next PRD opening that file.
- Finding 2 (`.lanes/` missing from the board's `.gitignore`) was not a PRD —
  `collect` skips board dotfiles, so no worker can land it. One-line
  orchestrator edit, made, and it survived the reset (separate repo).
- Absorbed the handover block appended to this file into
  `resources-are-organised-by-responsibility`, whose body `add` had left as the
  bare template placeholder. Left `priority: 0` — its own sequencing note says
  it runs when nothing else is in flight. Its fourth listed "fork" is a
  constraint, not a question: three, not four.

## Edits

- **None applied and none refused from this collect.** The analyst's report
  carries no `## Workflow` section — it named `probe-then-spec` in prose and in
  `## Scores` only — so per loop step 6 there is nothing to collect and
  `runs` stays 43. This is the **third** instance of
  `an-analyst-that-picks-its-own-route-leaves-its-run-uncounted`: I filed the
  PRD with no `workflow:` key, so the brief carried no workflow block and never
  demanded the section. That memo is now costing counted runs on every pass and
  should be reconsidered as a PRD.
- `write-the-specs` board-wide-gate row — refused and **closed, not owed**. Its
  author supplied a sentence about the row, never replacement text, and that
  window is gone. The orchestrator pastes or refuses and never rewrites, and a
  row is written from a run. Stop handing this one forward.

## Asked

- Q1 `resources-are-organised-by-responsibility` How the code is divided up · out
- Q2 `resources-are-organised-by-responsibility` How deep the tidy goes · out
- Q3 `resources-are-organised-by-responsibility` The downloaded dependency · out
- Q4 `collect-must-not-reset-the-checkout-it-did-not-write` Whether work
  continues while the tool that lost the work is fixed · out
- Knowledge query on the resources ask: 59 hits, none answering any fork. They
  are decisions, not facts.

## Owed

Record the four answers with `pearde answer`; on Q4's answer either dispatch
the implementer on `a-harness-measures-the-tree-its-worker-built-in` (5 specs
ready, 0/31 boxes) or hold it until `collect-must-not-reset-the-checkout-it-did-not-write`
lands; re-measure the harness set before believing any count; and leave the
other two sessions' PRDs alone.

---
---

# Below: another session's pass file, preserved verbatim, not mine

Three sessions share this path. This half was written by the session working
the Obsidian vault roots; I did not clobber it. Its content is untouched.

# pass — the vault roots at the project, the board loses its dot

Goal (from the user, verbatim): *"currently all the obsidian vaults are just
named `.pearde` But they should actually be named after the project… we want a
vault at the root of the project, indexing everything below it and also hidden
folders, especially the `.pearde` folder."*

## Established — read out of Obsidian's own bundle, not guessed
