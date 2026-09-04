Verdict: DONE

# cmd-vault-calls-a-function-that-was-deleted — implementer

`da1aa69` (one-register-writer) moved `obsidian_running()`/`register_vault()`
out of `resources/board/init.py` into `resources/board/obsidian_register.py`
as `running()`/`write()` and repointed `cmd_init`/`cmd_upgrade`, but left
`cmd_vault()` and the `wait_for_quit()` helper it calls on the old names, so
`pearde vault` died with `NameError` at `init.py:1295`. The lane's working
tree already carried the swap from pass one; this pass reproduced the crash,
confirmed the move, proved no sibling caller was missed, and fixed the probe,
which was measuring the wrong tree.

## spec01 — boxes

All four ticked, each against a check that was run:

- [x] no call to `obsidian_running(` or `register_vault(` in `init.py` —
  `grep -n "obsidian_running(\|register_vault(" resources/board/init.py`
  in the lane returns nothing (rc 1).
- [x] `wait_for_quit()` calls `obsreg.running()` — `init.py:1228`, and the
  docstring at `:1224` names it too.
- [x] `cmd_vault()`'s two register-writing branches call
  `obsreg.write(d, retire=board)` — `init.py:1299` and `:1303`.
- [x] the CLI no longer raises `NameError` — see the run below.

## Verify and Proof — output

Pre-fix reproduction, main checkout, against a real fixture board:

```
File ".../resources/board/init.py", line 1295, in cmd_vault
    if obsidian_running():
NameError: name 'obsidian_running' is not defined
```

Post-fix, the lane's tree, scratch `HOME` so the real Obsidian register is
never touched (`env HOME=/tmp/fakehome-… XDG_CONFIG_HOME= python3
$LANE/resources/pearde.py vault /tmp/vault-fix-… --dir pearde`):

```
vault: seeded /tmp/vault-fix-ba2j/.obsidian — plugins: dataview, obsidian-local-rest-api, hidden-folders-access
vault: waiting for Obsidian to quit — the register is only writable while it is closed. Quit it now (⌘Q)…
```

That is past `:1295` and inside `wait_for_quit()`'s own `obsreg.running()`
loop — the "may still legitimately wait on Obsidian's own state" outcome the
box allows, with the scratch register still `{"vaults":{}}` afterwards. The
run was killed at the wait; the `pearde-vault.lock` it left behind was
removed after checking its pid was dead.

Probe:

```
$ python3 .pearde/prds/cmd-vault-calls-a-function-that-was-deleted/probe/reproduce_and_verify.py
vault: seeded /var/folders/…/tmp…/.obsidian
vault: /var/folders/…/tmp… registered as tmp… · obsidian://open?vault=deadbeef
ok: cmd_vault resolves obsreg.running()/obsreg.write(), no NameError
rc=0
```

Repo gate: `bash resources/doctor.sh` — `guard/board/vault/vision/workflows/
grammar/health/briefs/view/plan` all `ok`. The four `broken` rows
(`origin`, `memos`, `knowledge`, `questions`) are pre-existing and name other
PRDs' files; none is in this footprint.

## The probe was measuring the wrong tree

Pass one's probe resolved its repo as `HERE/../../../..`, which from
`.pearde/prds/<slug>/probe/` is the **main checkout** — not the lane where
the fix lives. Re-run at the start of this pass it failed on its own first
assertion (`AssertionError: deleted name still called`), because it was
reading the unfixed `init.py`. Fixed by the pattern already in
`a-collect-closes-the-claim-dir-it-measured-against/probe/verify.py`: prefer
`.pearde/.lanes/<slug>` when it holds a `resources/board`, fall back to the
walk-up so the probe still passes once the lane lands on main.

```python
LANE = os.path.join(HERE, "..", "..", "..", ".lanes",
                    "cmd-vault-calls-a-function-that-was-deleted")
REPO = os.path.realpath(LANE) if os.path.isdir(
    os.path.join(LANE, "resources", "board")) else os.path.realpath(
    os.path.join(HERE, "..", "..", "..", ".."))
```

The probe fails on a broken tree — it did, demonstrably, before the fix.

## No sibling caller was missed

`grep -rn 'obsidian_running(\|register_vault('` across `resources/`,
`references/` and the top-level `*.md` in both trees returns only
`resources/doctor.sh:444: vault_obsidian_running()`, a shell function whose
name merely contains the string — not a call to the deleted Python name.
`init.py` was the only file `da1aa69` left stale. `obsreg.write`'s return
shape (`("added"|"known"|"running"|None, id_or_None)`) matches what
`register_vault` returned, so nothing downstream in `cmd_vault` changed.

## Finding — a second, unrelated bug in the same command (out of scope)

`cmd_vault()` calls `unhide_board(d, args.opt.get("dir"))` before it ever
reaches this PRD's code. `unhide_board`'s default target is
`planlib.BOARD_DIR`, now `".pearde"`, but it refuses any target name starting
with a dot. So **every** `pearde vault <dir>` with no explicit `--dir`
refuses, still, on the fixed tree:

```
pearde vault: refused — a board directory is one plain name with no dot in front of it — `.pearde` is what the move is out of
```

Fallout from the board-naming flip (`c88a64a`, `d8b509c`) that never reached
`unhide_board`'s own default and guard. A refusal, not a `NameError`, and a
different function from this PRD's footprint — reported, not fixed. Carried
over from the analyst's report because it is still reproducible.

## Health

No file in the footprint is under the health floor; nothing to leave better.

## Workflow retarget-a-moved-symbol

| # | step | result |
|---|------|--------|
| 1 | `reproduce-the-failure` | pass — `NameError: name 'obsidian_running' is not defined` at `init.py:1295`, the exact error the PRD names, once the target was made a real board |
| 2 | `find-the-move` | pass — `da1aa69` "one-register-writer"; the symbols now live in `resources/board/obsidian_register.py` as `running()` (`:182`) and `write()` (`:199`) |
| 3 | `retarget-callers` | pass — five sites in `init.py` (`:1224` docstring, `:1228`, `:1295`, `:1299`, `:1303`); repo-wide grep confirms no sibling caller elsewhere |
| 4 | `verify-with-a-probe` | pass, after repairing the probe's root resolution — it was reading the main checkout, not the lane |

### Edits

**`reproduce-the-failure` · `## Do` step 1** — the command as written refuses
before it can reproduce anything: a bare directory is not a board, so the run
ends at `pearde vault: refused — no board at <dir>/.pearde`. Replace with:

> 1. Make the state the command needs, then run it. For `pearde vault` that
>    is a board: `mkdir -p <dir>/.pearde/prds && : > <dir>/.pearde/settings.md`,
>    then `python3 resources/pearde.py vault <dir> --dir pearde`.
> 2. Re-run the same command on the fixed tree with a scratch home
>    (`env HOME=<tmp> XDG_CONFIG_HOME= python3 …`) whenever the command
>    writes machine-level state — here it registers a vault in the user's
>    real Obsidian config, which a reproduction must not do.

**`reproduce-the-failure` · `## Fails when`** — empty. Add:

> - the command refuses on a precondition (no board, a bad flag) before it
>   reaches the code the report names — that is not the failure, build the
>   state and run again
> - the reproduction would write state outside the tree; stop and give it a
>   scratch `HOME`/fixture first

**`verify-with-a-probe` · `## Do` step 1** — this is the one that cost this
pass a full re-run. Add:

> 1a. Resolve the tree the probe reads **from the lane**, not from the
>     probe's own path: a probe under `.pearde/prds/<slug>/probe/` that walks
>     up four directories lands on the main checkout, which does not have the
>     fix. Prefer `.pearde/.lanes/<slug>` when it exists and fall back to the
>     walk-up, so the probe keeps passing after the lane lands.

**`verify-with-a-probe` · `## Fails when`** — empty, and it is what let a
green probe be written against the wrong tree. Add:

> - the probe passes on a tree that does not contain the fix, or fails on the
>   tree that does — it is resolving the wrong root
> - the probe's assertions would pass with the fix reverted

**`find-the-move` and `retarget-callers` · `## Fails when`** — both empty. For
`find-the-move`: *no commit removes the definition — the symbol was deleted
outright, which is a QUESTION, not this workflow.* For `retarget-callers`:
*the new symbol's signature or return shape differs from the old one, so the
call sites need more than a rename — stop and say so.*

## Scores

complexity: 5
blast-radius: low
workflow: retarget-a-moved-symbol
