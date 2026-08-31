---
complexity: 12
footprint:
  - resources/graph/graph.sh
  - .gitignore
  - references/graph.md
  - references/skills/pearde-graph.md
  - resources/board/obsidian/app.json
  - resources/board/obsidian/graph.json
---

# spec01 — graph.sh writes and reads .pearde/graphify/, not graphify-out/

`resources/graph/graph.sh` exports `GRAPHIFY_OUT` absolute
(`<folder>/.pearde/graphify`) before every `graphify` call. graphify's own
`paths.py` reads `GRAPHIFY_OUT` at import time and accepts an absolute
override, and `out_path()` / `default_graph_json()` build on it — so
`extract`, `update`, every read command and the Obsidian exporter all resolve
to the same directory with no move and no symlink. `--graph` is still passed
explicitly to the read commands, matching the shape the PRD describes.

`extract` and `update` are passed the folder's resolved absolute path rather
than `.`, so the scan root is independent of the caller's cwd.

`graph.sh extract` and `graph.sh update` both end by running `graphify export
obsidian`, which writes `<GRAPHIFY_OUT>/obsidian`. Extraction alone does not
produce a vault (see the correction below), yet the `pearde-graph` skill
describes the vault as a product of a graph round — so the round runs the
export. It is a pure `graph.json` -> notes transform: no LLM call, no network.

`open`'s obsidian path is built from `$GRAPHIFY_OUT/obsidian` instead of the
hardcoded `graphify-out/obsidian`. `.gitignore`, `references/graph.md`,
`references/skills/pearde-graph.md`, `resources/board/obsidian/app.json` and
`resources/board/obsidian/graph.json` name the new path; `.gitignore`'s
`graphify-out/` line is dropped rather than renamed since `.pearde/` already
ignores the whole board.

### Two claims in the first draft of this spec were wrong

Both were checked against the installed source
(`~/.local/share/uv/tools/graphifyy/lib/python3.13/site-packages/graphify/`)
and are corrected here rather than left standing:

1. The PRD's premise that `extract`/`update` have **"no output flag and no
   environment variable for the output directory"** is false for this version.
   `paths.py` line 1 of the module body: `GRAPHIFY_OUT =
   os.environ.get("GRAPHIFY_OUT", "graphify-out")`, documented for "worktrees
   or shared-output setups" and explicitly accepting an absolute path. The
   move-vs-symlink fork the PRD posed is therefore moot — neither branch was
   needed.
2. The claim that **`update` writes `.graphify_root` as `str(watch_path)`
   with no `.resolve()`**, stamping a literal `.`, is false. `graphify
   update` (`cli.py:2385-2444`) never writes the marker at all; it only
   *reads* it (`cli.py:2409`) to recover a scan root when no path argument is
   given. The marker is written in exactly two places, `cli.py:4270` and
   `cli.py:4439`, both on the `extract` path and both as
   `str(Path(target).resolve())`. The literal-`.` reproduction could not be
   reproduced. Passing the resolved absolute path is still correct, for the
   scan-root reason above, so the behavior stands on a true premise.

A third fact the first draft assumed: **`graphify extract` writes the Obsidian
vault.** It does not — the extract block (`cli.py:3138-4513`) contains zero
occurrences of `obsidian`. The vault comes only from `graphify export
obsidian` (`cli.py:2996`), whose output dir is `Path(_GRAPHIFY_OUT) /
"obsidian"` (`cli.py:2793`). This is why `graph.sh` now runs the export.

## Acceptance

- [x] `bash .pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh`
      exits 0 (all three steps: update, query, extract) — final run against
      final code, vault cleared first (`rm -rf
      .pearde/graphify/obsidian` at 19:07) so step 3 proves `graph.sh` made
      it: `[1] update ... ok / [2] query ... ok / [3] extract ... ok /
      ALL PASS`, exit 0. (An earlier run failed step 3 — see the report; the
      export step in `graph.sh`, plus clearing the vault before export, are
      what closed it.) The block itself was then run exactly as `collect`
      runs it (`bash -e -o pipefail`, script on stdin) and exited 0:
      `OK: probe exit 0, no root leak, no stale mentions, vault has 1342
      notes`
- [x] the repository root holds no `graphify-out` directory after either
      command — `ls -d /Users/feb/dev/infra/pearde/graphify-out` printed
      `none` after `update --force` (18:33) and again after the full
      `extract --force` (18:48); `find -maxdepth 1 -iname "graphify-out*"`
      returns nothing
- [x] `graph.sh open <folder>` builds an `obsidian://` URL pointing at
      `<folder>/.pearde/graphify/obsidian`, not `graphify-out/obsidian`
      — run with `open` shimmed to echo:
      `OPEN-CALLED-WITH: obsidian://open?path=/Users/feb/dev/infra/pearde/.pearde/graphify/obsidian`
- [x] `grep -rn "graphify-out" .gitignore references/graph.md references/skills/pearde-graph.md resources/board/obsidian/app.json resources/board/obsidian/graph.json`
      returns nothing — grep exits 1 with no output. `graph.md`'s one
      remaining mention was reworded ("`graph.sh` redirects graphify's own
      default there with `GRAPHIFY_OUT`"): the box's parenthetical calls that
      prose fine, but the check it names greps `graph.md`, so the two
      disagreed; the sentence keeps its meaning without the literal token and
      `graph.sh`'s header still records the tool's default name. (This
      supersedes the box's original parenthetical, which called that prose
      fine while naming `graph.md` in the grep — the two disagreed.)

## Verify and Proof

`collect` runs this block with `bash -e -o pipefail`, cwd = the CODE repo,
script on stdin. So: every command whose failure is a legitimate outcome is
captured into a variable with `|| true` and the variable is tested, never
piped into `grep` (a non-zero producer fails the whole pipeline under
`pipefail` even when the grep matches). The probe's exit code is captured and
asserted explicitly — the previous version of this block ran the probe and
never tested its status, so a failing probe still exited 0. The block ends on
an explicit `echo`.

```sh
PROBE=.pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh
RC=0
OUT=$(bash "$PROBE" 2>&1) || RC=$?
printf '%s\n' "$OUT" | tail -15
[ "$RC" -eq 0 ] || { echo "PROBE FAILED (exit $RC)"; exit 1; }

LEAK=$(find /Users/feb/dev/infra/pearde -maxdepth 1 -iname "graphify-out*" || true)
[ -z "$LEAK" ] || { echo "ROOT LEAK: $LEAK"; exit 1; }

STALE=$(grep -rln "graphify-out" .gitignore references/graph.md references/skills/pearde-graph.md resources/board/obsidian/app.json resources/board/obsidian/graph.json || true)
[ -z "$STALE" ] || { echo "STALE MENTIONS: $STALE"; exit 1; }

VAULT=/Users/feb/dev/infra/pearde/.pearde/graphify/obsidian
[ -d "$VAULT" ] || { echo "NO VAULT at $VAULT"; exit 1; }
NOTES=$(find "$VAULT" -name '*.md' | wc -l | tr -d ' ')
[ "$NOTES" -gt 0 ] || { echo "VAULT EMPTY"; exit 1; }

echo "OK: probe exit 0, no root leak, no stale mentions, vault has $NOTES notes"
```
