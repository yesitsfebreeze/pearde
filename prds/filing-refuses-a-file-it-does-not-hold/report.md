# filing-refuses-a-file-it-does-not-hold — implementer report

Verdict: DONE

One spec, `specs/spec01.md`, **10 of 10 acceptance boxes ticked**, every one
against a command run in this session and quoted below. Box 10 — the
board-wide `doctor` gate — was open for part of the run on the `knowledge`
row, which `resources/knowledge.py` decides and which never reads
`collect.py`; the orchestrator closed it and the box was re-run and ticked.
The account is under `## Box 10 — closed`.

This is **pass two**. The spec was re-aimed by the orchestrator after the
user answered Q1 (*look in the notes first, then where you are standing*),
and pass one's build implemented the inverse rule. This pass re-aimed
`also_path` and the harness to the answer and added the two scenarios the
new boxes name. HEAD is `5f3270a` and did not move during the run.

This file replaces pass one's report on the same path. Its five findings are
carried forward by name under `## Findings`, one of them corrected.

## The contract, met

`collect --also <path>` resolves a relative entry against the **board root
first and the caller's cwd second**, a name both hold resolves to the
**board's**, and a path neither holds refuses the **whole call**. From a
throwaway board, `--also nope.md` run from a cwd inside the repo that is not
the board root:

```
collect: --also nope.md: no such path — looked for /private/var/…/d2/nope.md
and /private/var/…/d2/away/nope.md; board root /private/var/…/d2;
nothing written, nothing committed
exit=1
```

Both places tried, the path as given, the board root, and nothing written.
`git rev-list --count HEAD` on that fixture is `1` — its `fixture` commit and
nothing else.

The change is three functions in `resources/board/collect.py`, all above
`# ── reads ──`:

- `also_places(board_root, a)` — the order, and the list a refusal prints.
  Board root first, caller's cwd second; an absolute entry is its own only
  place; the two are deduped when they coincide, so a call from the board
  root does not print the same path twice.
- `also_path(board_root, a)` — the first place that `os.path.exists`. This is
  what makes precedence go to the board's copy. Still the one place an
  `--also` entry becomes a path, so a refusal's path and a commit's path
  cannot drift.
- `check_also(board_root, opts)` — refuses when no place holds it, called
  from `cmd_collect` before the `for rel in rels` loop.

`--widen` and the footprint loop were not touched. The predicate stays
`os.path.exists`, not `os.path.isfile`.

## Per-box status

| box | evidence |
|---|---|
| `[x]` probe reads `N · N pass · 0 fail`, exit 0, N > 41 | ran, exit 0, final line **`52 checks · 52 pass · 0 fail`** |
| `[x]` pointed at HEAD's `collect.py` the same harness exits non-zero | exit 1, **`52 checks · 19 pass · 33 fail`**, zero `ModuleNotFoundError` — see `## An unrunnable can-fail proof, repaired` |
| `[x]` a `--also` neither root holds exits 1, commits nothing, names path + both places + board root | sections A (9 checks) and D2 (7 checks), all green; refusal quoted above |
| `[x]` two collectable PRDs, one bad `--also`, both left `claimed`, no commit | section B, 7 checks green, including the no-`--also` control that lands four commits |
| `[x]` a relative `--also` under the board rides the commit from a foreign cwd | section C, 5 checks green (`C from another cwd, the file is still on the commit`) |
| `[x]` a relative `--also` that exists only under the caller's cwd rides the commit | section D, 4 checks green — `--also rider.md` from `$D/away`, `git show --name-only` names `away/rider.md`, the PRD reaches `done` |
| `[x]` a name both roots hold resolves to the **board's** | section I, 5 checks green — commit carries `dup.md` with the board's bytes (`the board copy`), `git status --porcelain -- away/dup.md` still reads `?? away/dup.md` |
| `[x]` `collect-is-a-command` reads `133 checks · 133 pass · 0 fail` | ran, exit 0, `133 checks · 133 pass · 0 fail`; its section K (absolute `--also`) unchanged |
| `[x]` `collect-keeps-its-word` reads `101 checks · 101 pass · 0 fail` | ran, exit 0, `101 checks · 101 pass · 0 fail` |
| `[x]` `index.py check` exit 0 and `doctor.sh` exit 0 with no new row | `index.py check` **exit 0**; `bash resources/doctor.sh` **exit 0**. The only non-`ok` rows are `harnesses` and `jstests`, both `off` at the baseline too. Row set diffed against the baseline run: identical |

The whole `## Verify and Proof` block, extracted with `awk` and run the way
`collect` runs it — `bash -c "set -o pipefail; $BLK"` — exits **0**.

## Box 10 — closed

`bash resources/doctor.sh` was `exit 0` at the baseline, before the first
edit, with every row `ok` except `view`, `harnesses` and `jstests`, all `off`.
It now reads:

```
  knowledge   broken  the research layer does not check out
                      graph.json is behind the files: 260902-14d9,
                      260902-4b7c, cargo-vendor-is-order-independent-…
```

Not this unit's, and provably so:

- `resources/doctor.sh:599` decides the row with
  `python3 "$DIR/knowledge.py" --root "$BOARD/wiki" doctor`. It reads
  `.pearde/wiki/` and its graph. It never reads `resources/board/collect.py`.
- The three notes it names are `.pearde/wiki/sources/260902-14d9.md`,
  `.pearde/wiki/sources/260902-4b7c.md` and
  `.pearde/wiki/conclusions/cargo-vendor-is-order-independent-of-the-source-replacement-.md`.
  All three are newer than `2026-09-02 09:50`; my baseline was taken at
  ~10:03 with the row `ok`. `.pearde/wiki/.graphify/graph.json` is stamped
  `2026-09-02 00:21` — behind them.
- Nothing in my footprint writes under `.pearde/wiki/`.

**Closed by the orchestrator, not by this footprint.** It ran
`python3 resources/knowledge.py relink`, and box 10's two commands were then
re-run here as the box spells them:

```
python3 resources/index.py check   → exit 0
bash resources/doctor.sh           → exit 0
```

`knowledge` reads `ok · graph in sync`. The only non-`ok` rows are
`harnesses` (`off`) and `jstests` (`off`), both `off` at the baseline. The row
*names* were diffed against the baseline doctor run and are identical, so no
row appeared and none was lost — which is what the box asks. Box ticked.

Three doctor rows moved during the run and none is anyone's finding:
`knowledge` `ok` → `broken` → `ok` (above), `view` `off` → `ok` (the
coordinator started the service mid-run), and `statusline` `*16` → `*17` (the
tree's dirty-file count, which every live session moves). `harnesses` counts
53 rather than 52: a sibling landed a new probe mid-run. It names neither
`resources/board/collect.py` nor a board census, so it is outside the
baseline set and has no baseline to regress against.

## Harnesses — baseline taken before the first edit

Every number below was recorded before this run wrote a byte;
`git status --short` at that point listed no file this session added.

| harness | baseline | after |
|---|---|---|
| this PRD's probe | `41 · 41 pass · 0 fail` (the inverse rule) | **`52 · 52 pass · 0 fail`** |
| `collect-is-a-command` | `133 · 133 pass · 0 fail` | `133 · 133 pass · 0 fail` |
| `collect-keeps-its-word` | `101 · 101 pass · 0 fail` | `101 · 101 pass · 0 fail` |
| `the-gate-runs-the-harnesses` | `57 · 57 pass · 0 fail` | `57 · 57 pass · 0 fail` |
| `graph-probe-makes-harness-sweep-unaffordable` | `4 · 4 pass · 0 fail` | `4 · 4 pass · 0 fail` |
| `nothing-left-open/the-line-tells-the-truth` | `85 · 85 pass · 0 fail` | `85 · 85 pass · 0 fail` |
| `the-brief-names-the-verdict-line-collect-requires` | `15 ok · 0 FAIL` | `15 ok · 0 FAIL` |
| `hunks-land-where-they-came-from` | `47 · 47 pass · 0 fail` | `47 · 47 pass · 0 fail` |
| `the-fixtures-meet-the-tool` | `35 · 34 pass · 1 fail` **before the first edit** | `35 · 33 pass · 2 fail` |

The set was chosen by `grep -l 'board/collect\.py\|find.*verify\.sh'` over all
52 harnesses `find .pearde/prds -name verify.sh` prints, so it covers both the
harnesses that name my footprint and the ones that enumerate the board.

**The one count that dropped is `the-fixtures-meet-the-tool`, and it is not
mine.** The single new red line is:

```
  FAIL F no file under resources/ carries any of this
       got [1] want [0]
```

Its predicate is
`git diff --name-only -- resources/board/plan.py resources/board/init.py |
grep -c .`. Running it now prints `resources/board/init.py`. That file's
mtime is `2026-09-02 10:09`, after my ~10:03 baseline, and it is not in this
spec's footprint — `git diff --stat -- resources/board/collect.py` is my whole
change, `1 file changed, 64 insertions(+), 7 deletions(-)`. No back-edge was
taken: there is nothing in the footprint that closes it.

The route's `re-run-the-harnesses` row for exactly this — *a count dropped,
and every failing line names a file outside your footprint that `git status`
shows a live sibling modified after your baseline* — is what was followed.

`python3 resources/index.py check` exit 0 at baseline and after.

## An unrunnable can-fail proof, repaired

The spec's `## Verify and Proof` block spelled the can-fail proof as a lone
`git show HEAD:resources/board/collect.py > /tmp/pearde-head/board/collect.py`.
`collect.py:74-78` inserts its own directory on `sys.path` and imports
`plan`, `edit`, `transitions` and `specs` from beside itself, so a lone copy
dies on `ModuleNotFoundError`. Run as spelled it gave `52 · 22 pass · 30
fail` with **9 lines of `ModuleNotFoundError`** — non-zero for the wrong
reason, and no evidence at all that the checks read the behaviour.

The block now copies `resources/board/` and `resources/*.py` whole into
scratch and swaps `collect.py` alone for `HEAD`'s. That reads
`52 · 19 pass · 33 fail`, exit 1, with **zero** import errors: the checks do
fail on the old code, and they fail because of the rule.

The block's last line was also changed from a bare `bash resources/doctor.sh`
to capture-then-grep. `collect` runs the block under `pipefail`, so a bare
board-wide gate makes this unit's pass conditional on every other PRD on the
board — the failure `write-the-specs` names. Doctor's rows stay printed; its
exit no longer decides the block's.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass — PRD, `specs/spec01.md`, the new memo, pass one's report and `git status --short` all read before the first command. **The PRD carries no `## Answers` heading** though the spec and the brief both cite it; the answer's text is in the spec and in the memo, so the fork was closed and no question is asked back. Stale path in the atomic, below |
| 2 | `capture-the-harness-baseline` | pass — pass one's build was uncommitted, so no baseline was inherited. Nine harnesses plus `index.py check` and `doctor.sh` recorded, exit codes and lines, into a scratch subdirectory named for this run |
| 3 | `attempt-the-build` | pass — the change is an **edit to an existing footprint file** (`collect.py`), so per the atomic it stands in place and is not staged under `probe/`; only the harness lives under `probe/`. Every fixture is its own `mktemp -d` with its own `git init`; `ls .pearde/prds` and doctor's `board` row both still read 95 PRDs, so nothing was left on the real board |
| 4 | `re-run-the-harnesses` | pass — one count dropped, shown above to be a neighbour's `init.py` edit. No harness outside my own probe was edited |
| 5 | `write-the-specs` | not re-run — the specs exist and this is the implementer's pass. Nine boxes ticked as each closed, the tenth once the orchestrator cleared the `knowledge` row; the block checked under `pipefail`, exit 0 |

No back-edge was taken.

### Edits

Replacement text for the failures the atomics caused. The workflow files were
not edited.

1. **`attempt-the-build`, its `Fails when` table, has no row for a
   script-swap can-fail proof.** Add a row: *seen* — "a can-fail proof that
   swaps one script for `git show HEAD:<f>` goes red on
   `ModuleNotFoundError`"; *means* — "the script imports its siblings from
   beside itself (`sys.path.insert(0, dirname(__file__))`), and a lone copy
   has no siblings, so the harness measures the import and not the
   behaviour"; *do* — "copy the whole directory the script imports from, plus
   the package dir above it, and overwrite the one file from `HEAD`; then
   assert `grep -c ModuleNotFoundError` is `0` in the red run before quoting
   its count."

2. **`capture-the-harness-baseline`, its "Resuming a killed run" clause**
   (carried from pass one; the route now holds the corrected text —
   `git -C <board> rev-parse --show-toplevel` and `ls-tree`). Verified again
   this run: `git -C .pearde rev-parse --show-toplevel` prints
   `/Users/feb/dev/infra/pearde/.pearde`, so the board is its own repo and its
   harnesses are tracked there. No further edit needed; the row is correct as
   it now stands.

3. **`read-the-contract` steps 1-2, and `attempt-the-build` steps 2 and 4,
   name `prds/<prd>/…`.** This board is at `.pearde/prds/`. Every such path
   needs the `.pearde/` prefix. Already owned by
   `every-probe-harness-is-re-aimed-at-the-pearde-layout` — carried forward,
   not re-filed.

## Findings — outside this contract, not fixed

1. **Corrected, twice over — there *is* a concurrent writer this run.** Pass
   one reported one; its own correction denied it. Measured here: between the
   step-1 `git status --short` (7 modified, 4 untracked) and the step-4 one
   (12 modified, 5 untracked), a sibling session added `SKILL.md`,
   `index.md`, `references/settings.md`, `references/parts/handles.md`,
   `resources/pearde.py`, `resources/board/init.py` and
   `references/skills/pearde-grammar.md` — the `grammar` work. HEAD did not
   move (`5f3270a` throughout), so nothing was committed under me. **None of
   those files is mine and none may ride this PRD's `--also`.** My whole diff
   is `resources/board/collect.py`.

2. **`resources/board/collect.py` carries another PRD's uncommitted hunks.**
   Four hunks in the same file rename `round file owed` → `pass file owed` and
   `.round.md` → `.pass.md` (in `scratch`'s docstring, `dry_line`,
   `collect_one` twice, and `close_container`). They were in the tree before
   my first edit and are not mine. **A commit of this footprint takes them
   too** unless the collector splits by hunk. Named here so the collector
   knows before it stages.

3. **`close_container()` silently drops a valid `--also`** (unchanged from
   pass one). It holds no `opts["also"]` reference. The pre-flight refuses a
   *bad* `--also` on a container close — probe section G proves it — but a
   *good* one is still never added and never named. A second way filing fails
   to hold what it names, and a different contract from this one. The new memo
   records it too, in its "second half".

4. **`--widen` has no existence guard either** (unchanged from pass one). It
   builds absolute paths and checks none. Harmless where `--also` was not: it
   drops a path rather than inventing one, so nothing false lands in the
   record. The PRD forbids touching `--widen`, so it is left alone.

5. **`the-fixtures-meet-the-tool`'s row `F no file under resources/` reads the
   whole working tree's `git diff`** (unchanged from pass one, and it fired
   again). Any uncommitted work under `resources/board/plan.py` or
   `resources/board/init.py` reddens it, whoever wrote it. Its second red row,
   `E …and every row it still fails is the quickstart's or the index's`, was
   already failing **before the first edit** of this run. Not chased, not
   fixed — noted so the next reader does not chase it either.

6. **`prd.md` has no `## Answers` heading.** The spec and the memo both cite
   `## Answers` Q1 for the resolution order, and the answer itself is
   recorded in both, so nothing was ambiguous for this build. But the PRD's
   own file does not carry it, and `## Questions` is gone too, so the board's
   record of what was asked and what came back lives only in the memo. For the
   orchestrator, not for an implementer.

## Scores

complexity: 8
blast-radius: mid
workflow: probe-then-spec
