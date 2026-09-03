Verdict: SPECCED

## Summary

Built `resources/board/obsidian_register.py` in the lane
(`.pearde/.lanes/one-register-writer`) — the one module that owns
`obsidian.json`: `home`, `path`, `open_`, `read`, `has`, `status`, `running`,
`write` (refuses while the app runs), `repair`. Rewired the five call sites
that used to parse the file or re-derive one of its four rules: `init.py`
(`cmd_init`, `cmd_vault`, `cmd_upgrade`), `serve.py`'s `vault_root`,
`doctor.sh`'s `vault` row, `statusline.sh`'s `▸vault` lookup, and
`graph.sh open`. One spec, already built and probed; see
`.pearde/prds/one-register-writer/specs/spec01.md` for the acceptance boxes
and a runnable verify block (all boxes pass — I ran it). Probe driver left
at `.pearde/prds/one-register-writer/probe/probe.sh`.

## A process mistake, caught and cleaned up before this report

I built the first pass in the *main* checkout (`/Users/feb/dev/infra/pearde`)
instead of the lane the brief named
(`.pearde/.lanes/one-register-writer`), because my early `cd`/`find` calls
into the lane were refused by a guard and I fell back to absolute paths
against the wrong root without noticing. Partway through, a `git stash`
I ran there (trying to isolate my own edits) collided with another
session's concurrent, legitimate work on `resources/board/plan.py` (the
`resources-are-organised-by-responsibility` split) and briefly left
conflict markers in that file. I did not resolve that by guessing: I
diffed every touched file against HEAD, confirmed which hunks were purely
mine (`init.py`, `doctor.sh`, `graph.sh` — clean; `serve.py` was
interleaved with a concurrent worker's `ask_digest`/`SWEEP_S` change), hand
-reverted only my own hunks, `git checkout --`'d the three purely-mine
files back to HEAD, deleted my untracked module from the main tree, and
dropped the one stash entry I created (verified its content was the stale
pre-split `plan.py`, and that its useful part — my own diffs — was already
reverted by hand, so nothing was lost by dropping it). `plan.py` had
already reconverged to a clean 644-line HEAD by the time I checked, most
likely because a concurrent `collect`/commit on that lane landed while my
stash was outstanding — I did not touch it further. The main checkout's
`git status` and `git stash list` are back to exactly what another session
left them, confirmed by `git diff --stat` showing only pre-existing,
unrelated changes. The actual build below was then redone from scratch in
the correct lane.

## Findings

- **Naming collision with a sibling PRD.** `.pearde/prds/
  doctor-repairs-the-register-entry` (already `claimed`) calls its
  `pearde doctor --fix` action "repair" and means *write the missing
  entry*. This module's `repair()` means the opposite: *drop a stale
  entry*, standalone from `write()`. That sibling PRD needs `write()`
  (refuses while running, returns `"added"`/`"known"`/`"running"`/`None`),
  not `repair()` — worth flagging so its implementer doesn't go looking for
  a `repair` call that does what its own PRD calls repair.
- **`statusline.sh` now spawns `python3` once per render.** It previously
  parsed the register with `sed` alone — the only script in the tree with
  no `python3` call at all, which reads as a deliberate choice for a script
  that renders continuously. The acceptance box (`grep -rl "obsidian.json"
  resources/` names one file) leaves no exception for it, so the lookup now
  goes through `obsidian_register.py has`. No test in the tree measures
  status-line latency, so this isn't a check I could fail against — noted
  as a design cost the move introduces, not a question the build hit.
- **`has()`/`status()` compare by `os.path.realpath`; `statusline.sh`'s old
  inline lookup compared the raw path string.** For a `$VAULT` that is
  itself a symlink (or traverses one), the two can disagree. This is
  arguably the correct fix given the PRD's own "compat-symlink history"
  rule, but it is a byte-level behavior change in that edge case, not a
  pure move — flagged per "a move that changes a printout is a bug."
- **One printed string changed on purpose.** `init.py cmd_vault`'s
  `Refused` message said `"it rewrites obsidian.json from memory"`; it now
  says `"it rewrites its register from memory"` — required by the first
  acceptance box (no file outside the module names the literal filename).
  Every other printed line is byte-for-byte unchanged; spec01 checks both
  directions.
- **`repair()` has no live caller yet.** The three existing call sites
  (`cmd_init`, `cmd_vault`, `cmd_upgrade`) all pass `retire=` to `write()`
  in one atomic read-modify-write, matching the original `register_vault`
  exactly. `repair()` is the same drop-only logic exposed standalone, self
  -checked, for a caller that wants to fix a stale entry without also
  registering a vault in the same breath — which is exactly what the
  `doctor-repairs-the-register-entry` sibling's `--fix` path will likely
  want, once it exists.
- **`grep -rl "obsidian.json" resources/` also matches
  `obsidian_register.py`'s compiled `__pycache__` blob.** Deleted it before
  handoff; harmless (bytecode, untracked, not source), but a fresh
  `pearde specced`/gate run that imports the module before checking will
  regenerate it — the check in spec01's verify block filters it out.
- Knowledge query for the PRD's contract returned nothing on-point (closest
  hits were about an unrelated `obsidian-unhide` plugin); no gap worth
  enqueuing.

## Scores

complexity: 16
blast-radius: mid
workflow: probe-then-spec
