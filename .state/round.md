# Round — the board is DRAINED: 64/64 requested done, 100%, nothing open

Written by session `5ba5c4b5`, 2026-09-01. **The concurrency question was
settled by the user: this was the only round worker. `pearde-eb` stood down;
`pearde-19` is not to be waited on.**

`done 64/64 · 100% · derived 19/19 · open 0/86 · ready 0 · blocked 0`.
Parked: `probe-code-lives-in-the-prd-folder`, `snapshots-fold-to-one-row`,
`upgrade-leaves-the-memo-index-stale` (filed this round).

## What landed

| PRD | verdict | commits |
|---|---|---|
| `seven-closed-probes-drifted-red/the-doctor-completes-without-a-home` | done, 3rd pass | `ca29535` board / `5ebefc7` code, record `8b7468b` |
| `seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green` | done | `74f8048` board / `4735940` code, record `308149b` |
| `seven-closed-probes-drifted-red` (container) | done | record `752af7a` |
| spec02's orphaned footprint file | committed by hand | `893d01c` |

Seven memos on the board, `memo index` regenerated, `memo check` green.
`probe-then-spec` at `runs: 30` with its five atomics at 50/50/30/50/27;
four `## Fails when`/`## Done when` edits applied verbatim across two rounds;
`workflow check` green.

## The two refusals, so nobody relitigates them

**`the-doctor-completes-without-a-home` took three implementer passes.**
`doctor.sh:334` read `$HOME` bare under `set -u`, ending the script and
stopping the twelve rows below `vault` from printing. The diagnosis was right
on pass one; the *proof* took three.

- Pass one wrote the code, the probe, the boxes and the proof block. Pass two
  re-ran those four artefacts against each other and reported 8/8. **Box 3
  asserted the ABSENCE of a sentence its own author had chosen not to write** —
  it could not fail. Refused; boxes 3 and 5 unticked by the orchestrator.
- Pass two replaced `OBSHOME="${HOME:-}"` with `getpwuid` **through `python3`**.
  A skeptic falsified box 3 in ten minutes with a PATH edit: same fixture
  board, no `python3`, with-HOME read `broken` and scrubbed read `ok`. The uid
  resolved fine; the interpreter was absent — and `env -i`, launchd and
  containers are exactly the thin-PATH cases, with macOS `/usr/bin/python3` a
  stub that exits non-zero without the Command Line Tools. Refused again.
- **Pass three closed it at the layer that removes the dependency:**
  `OBSHOME=$(unset HOME; echo ~)`, a bash builtin reading the passwd database
  under `set -u` with no PATH and no interpreter. The `unset HOME` is
  load-bearing — `~` follows `HOME` when `HOME` is set-but-empty, one of the
  two cases that triggers the fallback. `python3` demoted to second fallback;
  the last-resort arm reports **`broken`**, never `ok`.

The skeptic could not falsify it again: four PATH shapes (stub exiting 1, thin
PATH, empty bin dir, no PATH at all) all MATCH `broken`/`broken`. `/bin/dash`
returns a literal `~` and `/bin/zsh` empty, both caught by the
`[ "$OBSHOME" = "~" ]` guard — **that guard is load-bearing, not decorative.**

**`init-seeds-a-board-doctor-calls-green` was pre-ticked by its analyst** —
`collect` warned `8 of 8` and `7 of 7` boxes already ticked before an
implementer ran them. The implementer was dispatched told to **attack, not
re-run**, citing the memo. It found a real defect the analyst missed:
`index_memos` swallowed a failing `memos.py index`, so `init` exited 0 while
the board landed `memos broken`. Fixed, new box, 5 probe checks, seen red under
M5/M6/M7. It also re-derived the pre-fix quickstart count from a `git clone` at
`5ebefc7` rather than inheriting it: `31 · 30 · 1 fail` → `37 · 37 · 0 fail`.

## The rules that came out of it — all on the board as memos

- `one-author-is-not-an-accepted-spec.md` — **a box is ticked only against a
  predicate that has been seen fail.** Seen red, quoted, not "could fail".
- `a-check-decided-by-scheduling.md` — a harness binding a fixed port is not
  evidence until it claims it or fails loudly, and **a stood-down check reports
  `skip`, never a pass.**
- `a-report-must-say-verdict.md` — `collect.py:254` demands the literal word
  `Verdict:` in the first 40 lines; `workers.md` and `templates/` hold it zero
  times. **Every dispatch must carry the requirement in its prompt** until the
  templates are fixed.
- `a-crashing-checker-reads-as-a-failing-check.md` — doctor renders a checker's
  traceback as the board's own failure. Run a red row's checker directly.
- `also-drops-a-path-it-cannot-find.md` — see below.
- `a-probe-that-prints-no-count.md` — the container's `run-all.sh` uses
  `printf "" "$out"` twice; every row reads `pass=0 fail=0`, every FAIL excerpt
  is empty, and only the exit code carries information.
- `a-container-cannot-reach-done.md`, and the rest, predate this round.

## Tooling traps a later round WILL hit

1. **`--also` resolves against the caller's cwd, not the board.** A board file
   needs its `.pearde/` prefix (`--also .pearde/memos/foo.md`), even though
   every other board command takes board-relative paths and `--widen` on the
   same command resolves against the board root. A path it cannot find is
   **silently dropped** and the commit message still names it: `ca29535` names
   ten files it does not contain. They were re-filed on `74f8048`.
2. **A spec's own `footprint:` has the same trap and is not checked either.**
   spec02 spelled its path `.pearde/prds/...`; `repo_of` sent it to the code
   repo where the board worktree is ignored, so it landed in neither commit and
   the PRD went `done` with its deliverable on the floor. Committed by hand at
   `893d01c` with the reason in the message.
3. **`close_container()` (`collect.py:1227`) never reads `opts["also"]`** — a
   container collect accepts `--also` and silently ignores it, so an orphan
   cannot ride the parent.
4. **After any collect: `git show --stat` the commits AND `git status` the
   board.** A clean `--also` list is not a clean tree.
5. **A worker killed by infrastructure is RESUMED, not replaced.** The init
   analyst died on `API Error: Your computer went to sleep mid-response`; a
   `SendMessage` to its agent id brought it back with 78 tool calls of context,
   told to re-establish the tree and check the interrupted write landed whole.
   Count API errors before and after a resume — do not just grep for the string,
   the historical one stays in the transcript.
6. **`brief` on a claimed PRD** takes `--worker <the claim's id>`.
7. **SPECCED commits nothing** — riders cannot travel on it.
8. **sonnet 402s, bare inherit 429s, opus works.** Pin `model: "opus"`.
   Worker clocks run ~15 min fast; trust commits and `stat`.

## Owed, none of it blocking

- **`upgrade-leaves-the-memo-index-stale`** — filed `deferred` this round.
  `cmd_upgrade` shares `plant_graph` with `cmd_init` but not `index_memos`, so
  an upgraded board keeps a stale index and fails the check a fresh one passes.
  One line closes the behaviour; the proof is the work. **Not `open` by
  default** — @references/parts/derived.md. The user's call.
- **`spec01` box 8 of the init PRD needs an existence anchor** — the skeptic
  found all four of its checks pass over a directory `init` never touched
  (`doctor` prints 16 rows over a real empty board and 7 over a boardless one,
  so one line closes it). It is green for the right reason today and IS
  falsifiable, so it was not a withhold — but it is the vacuous shape this
  board has now refused twice. Take it in the next pass that opens that file.
- **`memos.py index` could in principle print a path it did not write** and
  `init` would claim success. Not reachable (`write_index` writes a `.tmp`,
  `os.replace`s, then returns the path), but a one-line `os.path.exists` before
  claiming would harden it.
- **`ignore_patterns("README.md")` is directory-blind** — it ate
  `memos/README.md` and will eat any future `README.md` at any depth.
- **`resources/index.py` does not ignore an untracked `node_modules/`** — see
  below. A real question for whoever owns that drop.
- **`doctor.sh:743` analyst hunk adopted** — carried from four rounds back,
  still unwritten and still unexplained. Establish what it was before writing.
- **`doctor --harnesses` has no job cap** (`doctor.sh:722`) — 47 harnesses at
  once. `the-gate-runs-the-harnesses` is green standalone at `57/57` and red
  only inside the sweep, which is this and not a real failure.

## A neighbour's red, not the board's

A sibling session installed playwright at ~13:56. `resources/board/node_modules/`
is untracked, so `index.py check` prints **115 lines and exits 1**, `doctor .`
ends "something is installed and not working" on `index broken · 115 problems`,
and the gate reads `57 · 55 pass · 2 fail`, both failures downstream of that one
row. Verified line by line: lines NOT naming
`node_modules/`/`package.json`/`package-lock.json` = **0**; lines naming
`init.py`, `memos.py` or `knowledge.py` = **0**. It clears when that session
finishes or the path is ignored deliberately.

## Carry-over findings, unactioned

The view-row harness (`prds/the-view-row-names-a-variable-that-exists/probe/verify.sh`)
binds hard-coded ports 8477-8479 with no bind check and never initialises
`SRVPID3`, so its `cleanup()` dies under `set -u` on an early exit and leaks two
listeners machine-wide — both in `a-check-decided-by-scheduling.md`, both
one-line fixes, to be folded into the next PRD that legitimately opens that
file. It also leaks three `Terminated: 15` lines past its `6/6/0` summary.
A harness four directories deep hard-codes its `..` chain — the doctor probe
walks up to the directory holding `resources/doctor.sh` instead, worth
generalising. graph-probe spec02 check A is a spelling-grep, not semantic, and
graph-probe's `prd.md` is still the unfilled template. Narrow the fixtures
`clean()` filter now that parse-cache is ignored. Sweep restarts the live view
daemon. `doctor.sh --harnesses .` renders the board name `?` from relative
paths. `reportParts()` in view.js parses 3 of 4 parts. One-page harness lives in
a git-ignored probe dir. `START="${1:-$PWD}"` at doctor.sh:46 reads `$PWD` bare
and survives only because bash sets it at startup. The `18`-row doctor tripwire
now lives in two committed harnesses, so adding a doctor row reddens both.
A thin-PATH fixture loop that symlinks `command -v` output leaves a
self-referential `printf -> printf` — harmless for builtins, silently lossy if
`echo` or `test` is ever added to such a list.

**Settled and stale**: `.state/round.HANDOFF-collect1-will-fail.md` — its
alarming name is stale and the file itself says so. Ignore it.

## Sessions live on this tree

- **the view / ⌘K search-palette session** — live and broad:
  `resources/board/render.py`, `view.css`, `viewtest.js`, `edit.py`, `serve.py`,
  `questions.py`, `references/drill.md`, `references/parts/doctor.md`,
  `references/parts/view.md`, `references/templates/prd.md`, and the playwright
  install. Notes at `.state/round.ck-search-palette.md` and
  `.state/round.board-modal.md`. **None of those are ours.**
- **memo/`.state`-move session** — finished; `6c1023f`, `e15dd0c` and the
  `MACHINE_DIR` → `LEGACY_MACHINE_DIR` refactor are committed.
- **`pearde-eb`** — stood down. Durable fact: **run collects serially**; census
  reds during overlapping full-board sweeps are contention, not code.
- **`pearde-19`** — its "land the collect" conclusion is superseded twice over.
