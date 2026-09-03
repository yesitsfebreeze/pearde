Verdict: DONE

## Summary

spec01 is built in the lane (`.pearde/.lanes/one-register-writer`, branch
`lane/one-register-writer`, cut from `1be5d2b`). All five acceptance boxes
run green as the block spells them, and the three baseline harnesses plus
the repo gate sit at their pre-edit numbers.

**The probe's build was not in the tree.** The brief said "the tree already
holds the probe's uncommitted code — continue it". It did not, anywhere:
`resources/board/obsidian_register.py` existed in no working tree, and
`git log --all -- resources/board/obsidian_register.py` was empty, so no
commit held it either. The lane directory's mtime is the claim's own
timestamp (18:19), so `lanes.create` re-cut it and the analyst pass's
uncommitted work went with the old tree. The orchestrator's checkout holds
hunks in two footprint files (`resources/doctor.sh`, `resources/board/serve.py`)
and I read both: they are the `purge`/lifecycle doctor row and `serve.py`'s
`ask_digest`, entirely other PRDs' work, so nothing was carried into the
lane. This pass therefore built spec01 from scratch against the spec text
rather than continuing a probe. The specs read as a faithful description of
what needed to exist, so nothing in them had to move.

## Per-box status

Every box was already `[x]` from the analyst pass; every one was re-run here
against the tree this pass built, and every one holds. `spec01.md` is
unedited — no box's words needed to change.

- **box 1 — one file names `obsidian.json`.** `grep -rl "obsidian.json"
  resources/` names `resources/board/obsidian_register.py` and nothing else.
  Block printed `ONE_MODULE`.
- **box 2 — the doctor `vault` row reads back through the module.** The row
  branches on `obsidian_register.py status` and nothing in `doctor.sh`
  resolves a home or parses the register any more. Proved under `env -i`:
  `env -i python3 resources/board/obsidian_register.py status
  /Users/feb/dev/infra/pearde` printed `registered c2b1c7c5878ce29c`, the
  same id the status line's old inline `sed` found. The `no-home` arm stayed
  unreachable on this machine, exactly as the spec's own finding predicted.
- **box 3 — the self-check.** `python3 resources/board/obsidian_register.py
  self-check` printed `19 checks · 19 pass · 0 fail`, exit 0. It seeds a
  scratch register under a scratch home, refuses a write with `running`
  mocked true and proves the file is byte-identical afterwards, writes once
  it is false, reads the write back by exact path, drops the retired entry
  in the same write, and drives `repair()` standalone — all inside one
  `tempfile.TemporaryDirectory()`, no real install read or written. The
  block asserts the exit code, not the tally, so a later pass can add the
  fifth assertion the spec's finding asks for without reddening this spec.
- **box 4 — one printed line changed.** `init.py cmd_vault`'s `Refused` now
  reads `"Obsidian is running — it rewrites its register from memory "`.
  Proved the other direction too: diffing every string literal of six or
  more characters in `init.py` and `serve.py` against `HEAD` shows exactly
  one changed line and no added one; every other removed literal is a path
  or process name that moved into the module with its function. Block
  printed `PRINTOUT_CHANGE_SCOPED`.
- **box 5 — the fetch stayed in the verb.** `ensure_bundles`, `copy_bundles`
  and the pinned plugin downloads are untouched in `init.py`; the module has
  no network call and imports no networking module.

Full block output, in order: `ONE_MODULE`, `19 checks · 19 pass · 0 fail`,
the three doctor rows (`ok … not installed`, `broken … not in Obsidian's
vault register`, `ok … registered as proj`), `DOCTOR_VAULT_ROW_OK`,
`PRINTOUT_CHANGE_SCOPED`, `VERIFY_DONE`, exit 0.

## Harnesses and the gate — every number back at baseline

Baselined before the first edit, re-run after, all with `PEARDE_ROOT=<lane>`
(all three honour it, so no board symlink was needed):

| harness | before | after |
|---------|--------|-------|
| `upgrade-leaves-the-memo-index-stale` | 40 checks · 17 pass · 22 fail · 1 skip | identical, row for row |
| `doctor-repairs-the-register-entry` | 8 ok · 6 fail | 8 ok · 6 fail |
| `seven-closed-probes-drifted-red/the-doctor-completes-without-a-home` | 12 checks · 9 pass · 3 fail · 0 skip | identical, row for row |

All three were already red before this pass; those reds are findings for
their own PRDs, not this one's. The first harness's comparison was made
against a pristine control (`git worktree add --detach` at `1be5d2b`) run in
the same conditions, because its section C is sensitive to what else is
running on the machine.

Gate: `python3 resources/index.py check` prints the same three lines it
printed at baseline (`resources/common.py` has no `files.md` row — another
session's file; `hotreload-test.js` dangling twice), exit 1 both times.
`bash resources/doctor.sh /Users/feb/dev/infra/pearde` prints the same 21
rows with the same verdicts, except `knowledge` moved `broken` → `ok` — a
row outside this footprint that a sibling repaired mid-run.

Two regressions were caused and both were fixed before this report; each is
written up below because each is a shape the atomics do not name.

## Findings

### One file was written outside the spec's footprint: `references/files.md`

`resources/index.py check` refuses any file under `resources/` with no row
in `references/files.md`, so the new module reddened the gate with a line
naming this pass's own file the moment it landed. I added its row (and
corrected `init.py`'s row, which still said `vault` registers into
`obsidian.json` itself). The gate is back to its three baseline lines. This
is a write outside the `footprint:` the spec declares, done because the
repo's own gate leaves no alternative — **spec01's footprint should name
`references/files.md`**, and any PRD adding a file under `resources/` has
the same obligation.

### A closed PRD's harness asserts on `doctor.sh`'s variable *name*

`prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh:226`
reads:

```sh
ARM="$(grep -A2 -F 'elif [ -z "$OBSCFG" ]; then' "$DOCTOR" | grep -E '^[[:space:]]*row vault ' | head -1)"
```

It checks a real invariant — the no-home arm must report `broken` and claim
only that the home could not be resolved — but it checks it by grepping
`doctor.sh` for the literal shell condition, which pins the variable name
`OBSCFG`. That arm cannot be driven on any machine whose uid has a passwd
entry, which is why the harness asserts at the source; the pin is the price.

My first cut replaced the condition with `elif [ "$OBSTATE" = "no-home" ]`
and turned that check red (`got: <no arm>`) with the row's printed text
byte-identical. I did not edit the neighbour's harness. Instead the row now
keeps an `OBSCFG` in hand, supplied by the module rather than derived:

```sh
OBSREG=$(res obsidian_register.py)
OBSTATE=$(python3 "$OBSREG" status "$PABS" 2>/dev/null) || OBSTATE=""
[ -z "$OBSTATE" ] && OBSTATE="no-home"
OBSCFG=$(python3 "$OBSREG" open 2>/dev/null) || OBSCFG=""
```

and the `not-installed` arm was moved above the `-z "$OBSCFG"` arm, because
`open` prints nothing for a machine that never ran Obsidian either and those
are different verdicts. The neighbour is green again and the box still
holds: nothing in `doctor.sh` resolves a home or opens the register. The
coupling is worth routing — an assertion on another file's variable name
will break the next move too.

### An untracked footprint file is invisible to every fixture in the set

`upgrade-leaves-the-memo-index-stale`'s probe builds its copy with
`git ls-files -z | rsync -a0 --files-from=-`, so the new, untracked module
was not in the fixture while the `init.py` that imports it was. `git add`
in the lane fixed it and the harness returned to its control numbers
exactly. `re-run-the-harnesses` names this row and its `do` was right; its
`seen` column is too narrow — see `### Edits`.

### `has()`/`status()` compare by realpath; the old status-line lookup compared raw strings

Carried forward from the analyst pass and still true. For a `$VAULT` that is
itself a symlink, or traverses one, the module answers where the old inline
`sed` did not. This is the behaviour the PRD's own compat-symlink rule
argues for, but it is a widening, not a pure move. On this machine both
spellings resolve the same id (`c2b1c7c5878ce29c`), verified by rendering
the status line before and after.

### `statusline.sh` now spawns `python3` once per render

Carried forward. It was the only script in the tree with no `python3` call —
plausibly deliberate for a continuously rendered line. Box 1 leaves it no
exception. The call is guarded behind `[ -n "$VAULT" ]`, so it only runs on
a project that actually carries a vault directory. No test in the tree
measures status-line latency, so this is a design cost, not a failing check.

### `write()` refuses by default, and three callers opt out on purpose

The spec says `write()` refuses while Obsidian runs; the PRD says no printed
line may change. Those meet at a default: `write()` refuses and returns
`("running", None)`, and `cmd_init`, `cmd_upgrade` and `graph.sh open` pass
`even_if_running=True`, each with a comment saying why. All three already
wrote under a live app and printed their own warning that the entry would be
erased on quit; refusing there would have deleted a whole printed branch.
`cmd_vault`'s quit-and-wait loop is untouched — it still polls `running()`
itself, and the write after it also passes `even_if_running=True` because
the loop has already proved the app is gone and a second probe would only
add a race.

### Naming collision with a sibling PRD

Carried forward from the analyst pass and still worth flagging.
`prds/doctor-repairs-the-register-entry` calls its `--fix` action "repair"
and means *write the missing entry*. This module's `repair()` means the
opposite: drop a stale entry, standalone. That PRD wants `write()`.

### Knowledge

`python3 resources/knowledge.py remember` was not called: nothing here came
from outside this tree. Every rule written into the module's docstring was
read out of the files it replaced.

## Workflow probe-then-spec

| # | step | result |
|---|------|--------|
| 1 | `read-the-contract` | done — PRD, `specs/spec01.md`, the analyst's `report.md` and `probe/probe.sh` read; `git status --short` recorded in the lane (empty) and in the checkout (17 paths, none this PRD's); five of six footprint paths present, `obsidian_register.py` absent. Table row for "the `repo:` root is a worktree under `<board>/.lanes/`… and the brief says the probe's uncommitted code is already there" applied: checkout hunks read and left where they were |
| 2 | `capture-the-harness-baseline` | done — 98 board harnesses enumerated, 3 selected as reading the register or a footprint path, all 3 honour `PEARDE_ROOT`; each baselined with output saved. Gate baselined in the lane, exit codes included. Recorded before the first edit |
| 3 | `attempt-the-build` | done, entered twice. First pass built the module and rewired all five call sites. Re-entered from step 4 twice: once for the neighbour harness's `OBSCFG` anchor, once for `git add` |
| 4 | `re-run-the-harnesses` | done, run three times. First run: two harnesses moved. Second: one still moving. Third: all three at baseline, gate at baseline |
| 5 | `write-the-specs` | second-pass form — no spec authored. `## Fails when` applied to the standing block: the previous pass's `report.md` was read and its findings carried forward (its own row), no line exits non-zero on its passing result, no line is a board-wide gate, no box asserts a literal probe total, no `.pearde/prds/…` read that a lane would empty. Nothing needed changing |

Both back-edges to step 3 were taken from step 4, the edge its `on failure`
names, and the limit of two was not exceeded.

### Edits

**`re-run-the-harnesses.md`, the `git ls-files` row — the `seen` column is
too narrow.** Its `do` was exactly right and saved the run; its `seen` names
a symptom that never appeared. `init.py` raised `ImportError` inside a
fixture whose harness captures output and greps it, so nothing printed
`ModuleNotFoundError` anywhere I could see. What I actually saw was a
missing *output line* (`missing: init: regenerated memos/README`) and a
doctor report that came back 8 rows instead of 21 — the copied command
dying before it printed. Replacement `seen`:

> a harness fixture's copy of a command you did not change prints less than
> it did at baseline — a missing line, a short report, a row count that
> dropped — or crashes with `ModuleNotFoundError` naming a module this pass
> added, while the same command is green in the tree you built in

**`read-the-contract.md`, `## Fails when` — no row for a probe's build that
is gone from every tree and every commit.** The existing row assumes the
work is somewhere: the lane is empty *because* the checkout holds it
uncommitted. `attempt-the-build`'s companion row assumes the other case: it
is clean *because* something committed it. Neither covers a lane re-cut
between the analyst's pass and the implementer's, which drops uncommitted
lane work on the floor and leaves the brief still saying the code is there.
I burned a step confirming the absence three ways. New row:

> | the brief says the probe's uncommitted code is in the lane, the lane's
> `git status --short` is empty, `git log --all -- <the new file>` is empty,
> and no hunk in the checkout is this PRD's | the lane was re-cut after the
> analyst's pass — the lane directory's own mtime is the claim's timestamp —
> and `lanes.create` cuts from HEAD, so uncommitted lane work is gone rather
> than mislaid | stop looking. Build the specs from their own text: they are
> the probe's knowledge, written down for exactly this, and step 5 of this
> route exists so that they can be. Say in the report that the build is a
> rebuild and not a continuation, and check each box against the file rather
> than against the spec's "already stands" prose |

**`attempt-the-build.md`, `## Fails when` — no row for a neighbour harness
that pins your footprint file's source text.** The nearest row covers a
neighbour harness decided by *its own* defect and says do not edit that file
and report it. Here the harness is sound, my contracted move broke its
anchor, and the answer was neither to edit it nor to leave it red. New row:

> | a committed harness outside your footprint goes red on a `grep -F` of a
> **source line** in a file of yours — a variable name, a shell condition —
> while the behaviour it guards is byte-identical | the neighbour asserts an
> invariant it cannot drive on this machine, so it asserts it at the source
> and pins your spelling as a side effect. This is not its defect and not a
> real regression | keep the anchor text. Where the pinned name can be
> re-sourced rather than re-derived — the value now comes from the module,
> the name stays — do that and say so; reorder sibling arms if the new
> source makes the old one ambiguous. Never edit the neighbour's harness,
> and report the coupling: the next move breaks it again |

## Files

Under `/Users/feb/dev/infra/pearde/.pearde/.lanes/one-register-writer`:

- `resources/board/obsidian_register.py` — new, staged, 380 lines
- `resources/board/init.py` — three functions removed, five call sites rewired
- `resources/board/serve.py` — `vault_root` reads `obsreg.read()`
- `resources/doctor.sh` — the `vault` row branches on `status`
- `resources/statusline.sh` — `▸vault` looks up through `has`
- `resources/graph/graph.sh` — `open` writes through `obsreg.write`
- `references/files.md` — outside the footprint; see the finding

Everything is staged or modified and uncommitted in the lane, for `collect`
to land. No file in the orchestrator's checkout was touched.

## Scores

complexity: 16
blast-radius: mid
workflow: probe-then-spec
