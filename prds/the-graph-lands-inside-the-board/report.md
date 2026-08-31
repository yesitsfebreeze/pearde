# report — the-graph-lands-inside-the-board

**Verdict: DONE.** 4 of 4 acceptance boxes closed and verified; the probe
exits 0 end to end against the final code, with the vault cleared first so
step 3 proves `graph.sh` produced the vault. The spec's Verify block was also
run exactly as `collect` runs it — `bash -e -o pipefail`, script on stdin —
and exited 0: `OK: probe exit 0, no root leak, no stale mentions, vault has
1342 notes`.

(An earlier state of this PRD was reported BLOCKED: probe step 3 failed
because `graphify extract` had never written an Obsidian vault. The
coordinator settled that fork — `graph.sh` gains the export step — and this
report was rewritten for the settled state. The blocked-state reasoning is
kept below under "The blocked fork" rather than erased.)

The board's graph output moved from `graphify-out/` at the repository root to
`.pearde/graphify/`. Every graphify entry point `graph.sh` drives now resolves
there through one exported `GRAPHIFY_OUT`, and a graph round now produces the
Obsidian vault it has always claimed to produce.

## The blocked fork, and how it was settled

I stopped rather than guess on one point: probe step 3 asserts an Obsidian
vault under `.pearde/graphify/` after `graph.sh extract`, and **`graphify
extract` has never written a vault** — at the old path or the new one. The
extract block (`cli.py:3138-4513`) contains zero occurrences of `obsidian`;
the vault comes only from the separate `graphify export obsidian` subcommand
(`cli.py:2996`), which nothing in `graph.sh` invoked. So `graph.sh open`
opened a vault `graph.sh` had no way to create.

The coordinator settled it: **`graph.sh` gains the export step; nothing is
dropped from the spec.** The reasoning on record — the `pearde-graph` skill's
own description promises "an Obsidian vault written to
`.pearde/graphify/obsidian/`" as the output of a graph round, so the vault is
a product of the round, not a separate command a person must know to run.
Step 3 was asserting the contract correctly; `graph.sh` was not meeting it.

## What changed

**`resources/graph/graph.sh`**

- One `export_vault()` function, called by both `extract` and `update`, so the
  two cannot drift apart. It runs `graphify export obsidian --graph
  "$GRAPH_JSON"` — a pure `graph.json` -> notes transform: no LLM call, no
  network. Chained with `&&` so a failed extraction never exports a vault from
  a graph it did not manage to rebuild.
- `update` exports too, so the vault cannot go stale against a `graph.json`
  that `update` just rebuilt.
- The `update` usage line in the header now says the vault is rebuilt.
- The comment on the `update` branch was rewritten off a false premise onto a
  true one (below). Behavior unchanged.

**`references/graph.md`** — one remaining `graphify-out` mention reworded to
"`graph.sh` redirects graphify's own default there with `GRAPHIFY_OUT`, set
absolute before every call". Box 4's parenthetical called that prose fine
while the check it names greps `graph.md`; the two disagreed, and the sentence
keeps its meaning without the literal token.

**`specs/spec01.md`** — the Verify block rewritten (below) and the two false
claims corrected in the narrative rather than left standing under a corrected
comment.

The other four footprint files were already correct from pass one; I left them
alone.

## The Verify block was broken, and that is how this could have shipped green

The original block ran the probe and **never tested its exit code**:

    bash .../probe/verify.sh
    find ... -maxdepth 1 -iname "graphify-out*"
    STALE=$(grep -rln ... || true)
    [ -z "$STALE" ] && echo "..." || { echo "..."; exit 1; }

`collect` reads the block's LAST command. That last line ends on an `echo`, so
**a failing probe still exits 0.** This run failed step 3 and the block would
have reported success. Rewritten to capture the probe's status and assert it,
and hardened for the environment `collect` actually provides (`bash -e -o
pipefail`, cwd = the CODE repo, script on stdin): every command whose failure
is a legitimate outcome is captured with `|| true` into a variable that is
then tested, never piped into `grep` — under `pipefail` a non-zero producer
fails the pipeline even when the grep matches. It still ends on an explicit
`echo`, and it now also asserts the vault exists and is non-empty.

## Wiring the export exposed a second defect, and it is fixed

The first pass of `export_vault()` was a bare `graphify export obsidian`.
That produced a vault **16 notes short**, silently:

    [graphify] WARNING: skipped 16 pre-existing file(s) graphify did not
    create, to avoid overwriting your notes: Drill.md, Guard.md, Persona.md,
    PRD.md, View_1.md (+11 more).

graphify refuses to overwrite notes it did not itself create, so exporting
over a previous vault skips every colliding note and **warns rather than
fails** — the round still exits 0. I quantified it instead of trusting the
count: a clean export of the same `graph.json` into an empty directory gives
1311 notes, the in-place vault had 1295, and `comm` on the two file lists
returns exactly the 16 the warning names (`Drill.md`, `PRD.md`,
`Settings.md`, `Workflow.md`, the six templates, ...).

`export_vault()` now clears `$GRAPHIFY_OUT/obsidian` before exporting, which
is graphify's own prescription ("Export into an empty directory ... to get
the full vault"). This is safe: the vault is pure output — `references/graph.md`
says "edit nothing in it, edit the corpus and re-extract instead" — and
graphify writes even the vault's `.obsidian/graph.json` config, byte-identical
in a clean export, so nothing of anyone's lives there. The function guards on
a non-empty `GRAPHIFY_OUT` so the `rm -rf` can never be handed a bare path.

After the fix, `graph.sh update` on a populated vault: 1311 notes, no skip
warning, no prune warning — matching the clean-export baseline exactly.

Worth noting this defect was **not** created by exporting from `update` as
well as `extract`. It fires on any second export into the same directory, so
it would have hit the second graph round either way; running the export twice
per round only surfaced it on the first.

## Three claims checked against the source, not taken on faith

Read from the installed tool
(`~/.local/share/uv/tools/graphifyy/lib/python3.13/site-packages/graphify/`):

1. **The PRD's central premise is false.** It states `extract`/`update` have
   "no output flag and no environment variable for the output directory".
   `paths.py`: `GRAPHIFY_OUT = os.environ.get("GRAPHIFY_OUT", "graphify-out")`,
   read at import, documented for "worktrees or shared-output setups",
   explicitly accepting an absolute path. `out_path()` and
   `default_graph_json()` build on it, so extract, update, every read command
   and the obsidian exporter resolve together. **The move-vs-symlink fork the
   PRD posed was moot** — neither branch was needed.
2. **`update` does not write `.graphify_root`.** The spec claimed it wrote
   `str(watch_path)` unresolved and that a literal `.` marker had been
   reproduced. `graphify update` (`cli.py:2385-2444`) never writes the marker;
   it only *reads* it (`cli.py:2409`) to recover a scan root when given no
   path. The marker is written in exactly two places, `cli.py:4270` and
   `cli.py:4439`, both on the extract path, both `str(Path(target).resolve())`.
   I could not reproduce the literal `.`. Passing the resolved absolute path
   is still right, for the scan-root reason, so the behavior stands on a true
   premise.
3. **`extract` does not write the vault** — the fork above.

Also confirmed: the board repo already ignores the new location
(`.pearde/.gitignore` carries `graphify/`), so nothing needed adding there.

Recorded to the KB as `[[260831-fd12]]` — these are facts about a library this
tree does not hold, and the query beforehand showed a genuine gap.

## Findings, not fixed

1. **`graph.sh update` silently drops its arguments.** The `update` branch
   ignores `${ARGS[@]}`, so `graph.sh update <folder> --force` never forwards
   `--force`. Probe step 1 invokes exactly that, so it has been testing a
   non-forced update while reading as forced. Pre-existing — the original line
   was `graphify update .`. `extract` forwards args correctly; `update` should
   too. Left as a finding per the coordinator.
2. **`graph.sh` could not create the vault it opens** — closed naturally by
   the export work above.

## Repo gate

`bash resources/doctor.sh`: three broken rows, none in my footprint and none
affected by this work.

- `skills` — globs `$SKILL_ROOT/skills/*.md` (`doctor.sh:69`), but commit
  aea6dae moved skills to `references/skills/` and `doctor.sh` was not updated
  with the rename. A live break from another PRD's work.
- `guard` — `guard.py` does not refuse a hand-walked board.
- `origin` — 3 derived PRDs carry no `from:`.

Every other row is `ok`.
