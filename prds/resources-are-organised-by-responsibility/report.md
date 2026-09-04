# resources are organised by responsibility — analyst

Verdict: REFINE

Workflow followed: `probe-then-spec`. Its `## Use when` fits exactly — an open
PRD that needs specs before anyone can be sent at it. Steps 1–5 all ran.

The build went a long way. It did not hit a fork; it hit a size. Cutting
`resources/` into responsibility directories is three separate contracts, and
the fourth of the PRD's own concerns — the largest module — is bigger than the
move around it.

## What the build did

A copy of the tree was cut for real in a scratch directory made at run time.
Nothing was written into the lane's `resources/`, and nothing outside this
repo was touched except that scratch copy.

Three cuts were run, in order, each one until it worked or broke:

1. **Rename `resources/board/` to `resources/core/`, changing no code.** The
   whole command surface died on the first call: `pearde: no
   resources/board/plan.py above this file`. Six code files had to be patched
   before `pearde help` came back, and after that the rename was complete —
   a whole-directory rename is cheap.
2. **Cut the modules across four directories** — `read/`, `write/`, `run/`,
   `draw/`. Every module that imports a sibling by bare name broke:
   `ModuleNotFoundError: No module named 'plan'`. 43 such imports exist.
3. **One shared path file.** A new `resources/pearde_path.py` that puts every
   directory under `resources/` on `sys.path`, imported by each module in
   place of its hand-rolled preamble, brought the whole split back. `pearde
   help` listed every command, `pearde scan` read the real board, `pearde
   index check` ran, `pearde brief` reached its gate.

So the layout the PRD asks for is reachable. What the build measured is what
it costs.

## What the build measured

`bash prds/resources-are-organised-by-responsibility/probe/verify.sh` — **21
passed, 0 failed**. Every number below is one of its assertions.

| what | count |
|---|---|
| loose scripts at the top of `resources/` | 14 |
| Python modules in `resources/board/` | 15 |
| files spelling the root probe `resources/board/plan.py` | 2 |
| bare cross-imports that must resolve from a new directory | 43 |
| sibling scripts addressed by a path built from a directory | 4 |
| places `doctor.sh` spells `resources/board/` | 23 |
| manifest rows in `references/files.md` naming `resources/board/` | 30 |
| scope anchors in `index.md` naming `resources/board/` | 33 |
| committed `verify.sh` harnesses spelling `resources/board/` | 51 |
| other files under the board spelling it | 325 |

### The five mechanisms a move has to satisfy

1. **The root probe.** `pearde.py` and `brief.py` each walk up looking for
   `resources/board/plan.py` by name. Rename the directory and both fail. The
   probe wants to be `resources/pearde.py`, which is the one file that cannot
   move.
2. **Bare cross-imports.** Every module does `sys.path.insert(0, <its own
   dir>)` then `import plan`. That holds while they share a directory and
   fails the moment they do not. One shared path file fixes all 43 at once.
   `plan.py` is the exception: it imports only `render` and the loose scripts
   in `resources/`, both of which its existing two-line preamble already
   reaches — so `plan.py` needs no edit at all, which is what lets the largest
   module be cut in parallel with the rest.
3. **Sibling scripts addressed by path.** `init.py` launches `os.path.join(HERE,
   "serve.py")`; `machine.py`, `guard.py` and `pearde.py` do the same for
   `serve.py`. `sys.path` does nothing for a subprocess spelled by path. The
   probe caught this live: `can't open file '…/resources/write/serve.py'`.
4. **Assets read from a module's own directory.** `render.py` inlines
   `lit-core.min.js` as an import map by reading `dirname(__file__)/<name>`,
   and `serve.py` serves `view.js` and `view.css` the same way. Those four
   files have to land together, whatever the grouping is called.
5. **The map is the gate.** `index.py check` prints one problem per moved
   file. In the cut tree the `index` doctor row went from 3 problems to **192**.

### `plan.py` is its own contract

3032 lines, twelve banner sections: board resolution, the parse cache, master
boards, typed weights, silence and sweeps, the vision axis, lanes, the map
file, calibration, the schedule, the example board. It is also the module
every other one imports. Cutting it is the answer to Q2 and it is most of the
work in this PRD; moving it is a `git mv`.

## Findings

- **A broken module takes down every command.** `pearde.py` `discover()` wraps
  `exec_module` in `except Exception`, but `brief.py`'s root probe ends in
  `sys.exit(2)` — `SystemExit` is a `BaseException`, so that catch does not
  hold it. In the probe, one module that could not find its root killed `scan`,
  `plan` and `help` alike, and the comment above the catch says "a broken child
  must not take the rest down". The catch should be `except BaseException` or
  the probe should raise. Not in this PRD's contract; reported, not fixed.
- **A doctor row that cannot fail.** The `plugins` row is gated on `if [ -d
  "$DIR/board/adapters" ]`. In the cut tree the row did not go red — it
  **vanished** from the output entirely, silently. A row that disappears
  rather than reddening cannot fail.
- **The knowledge record has nothing on this question.** `knowledge.py query`
  returned 0 hits and enqueued the gap at `pearde/wiki/pending/260902-fd4a.md`,
  priority med. Not a question of mine.
- **Three `index.py check` problems stood before the first edit**, in the lane
  and in the checkout: `references/skills/pearde-machine.md` has no row in
  `references/files.md`; `references/language.md` cites
  `@references/personas/writer.md`, not on disk; `resources/board/edit.py`
  cites `@questions.py`, not on disk. Inherited, not mine.
- **The shared checkout is dirty in seven files**, `resources/board/plan.py`
  among them, with another session's edits to `state_dir()` and eight hunks in
  all. The lane was cut off HEAD and carries none of them. Whichever child
  moves `plan.py` will collide with that work unless it runs when nothing else
  is in flight — which this PRD's own `## Sequencing` already says.
- **The checkout's seven dirty files were committed under the run.** They were
  modified when the build started and `git status --short` is silent now; a
  sibling session landed them. The collision above is still real for whichever
  child moves `plan.py` — it is a collision with the next uncommitted pass, not
  with that one.
- **One fixture registered itself with Obsidian.** `pearde init` on a
  `mktemp -d` board printed `registered … with Obsidian`, and said in the same
  line that a running Obsidian erases the entry when it quits. Nothing landed
  in the view service's registry — `serve.py status` lists no scratch board.
- **The board grew under the run**: 121 PRDs at the baseline, 122 by the last
  `scan`. Another session's, not mine.
- **Node costs nothing to drop.** `node_modules/`, `package.json` and
  `package-lock.json` are already in `.gitignore` — untracked. The only
  downloaded package is `playwright-core`, imported by exactly two files,
  `viewtest.js` and `hotreload-test.js`. `lit-core.min.js` is vendored and
  read from disk. So Q3's answer costs one doctor row and one paragraph of
  prose, not a rewrite — it is a spec inside a child, not a child.

## Why this is a split and not one set of specs

Written as one set, the units are: the path rule; the move; the map and prose;
the harness sweep; the node row; and the cut of `plan.py`. Six units summing
about 52 — over `split-above: 40`, and the sixth alone prices at about 20.
Dropping the largest module into its own contract leaves five units at about
32, which is a real PRD.

The first two children have disjoint footprints and run at once: the path rule
touches every module under `resources/board/` **except** `plan.py`, and the
largest module's cut touches `plan.py` and the modules that come out of it and
nothing else. The third consumes both — it can only move files once they find
each other and once there is no 3000-line module to move.

## Split

| child | contract | needs |
|---|---|---|
| every-module-finds-its-siblings-by-one-rule | One file puts every directory under `resources/` on the import path, one probe finds the repo root by `resources/pearde.py`, discovery walks every directory under `resources/`, and every tool that launches a sibling script finds it rather than spelling `board/` — so a file can move with no second edit anywhere; nothing has moved yet | — |
| the-largest-module-is-cut-by-responsibility | `resources/board/plan.py` is several modules beside each other, each named for one thing it is responsible for and none over 700 lines, with every command, caller and harness unchanged from the outside | — |
| every-file-sits-under-what-it-is-responsible-for | Every file under `resources/` sits in a directory named for what the files in it are responsible for, the manifest and the map and the prose and the board's 51 harnesses all name the new paths, nothing is downloaded to run or draw the board, and `index.py check` and `doctor.sh` are green | every-module-finds-its-siblings-by-one-rule, the-largest-module-is-cut-by-responsibility |
