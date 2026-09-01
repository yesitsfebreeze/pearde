---
complexity: 9
workflow: probe-then-spec
footprint:
  - resources/board/init.py
---

# spec01 — `upgrade` regenerates the memo kind-index, and a harness proves an upgraded board is as healthy as a fresh one

`cmd_upgrade` shared `plant_graph` with `cmd_init` and not `index_memos`, so a
board brought forward kept whatever index it had — none at all on any board
made before that step existed — while a board made fresh landed with a current
`memos/README.md`. `memo check` calls the first stale and doctor's `memos` row
reports it broken. This unit closes that: `upgrade` runs the same regeneration
`init` runs, and the harness drives an old-shaped board through it and compares
the doctor report row for row against a freshly `init --example`ed one.

**All of it already stands in the tree, uncommitted.** The implementer's job is
to read it, run the harness, tick each box against what it printed, and account
for the one row that still differs and the one check that stands down.

## What already stands

- `resources/board/init.py:349` — `index_memos(board, verb="init")`. The
  failure line was hard-coded to say `init:`; it now says `{verb}:`, because
  `upgrade` is the second caller and naming the wrong command in a failure is
  worse than no line. `cmd_init`'s call site at `:582` is unchanged — the
  parameter defaults.
- `resources/board/init.py` in `cmd_upgrade`, between the `wiki` row and
  `write_obsidian` — reads `memos/README.md`'s bytes, calls
  `index_memos(board, "upgrade")`, reads them again, and prints one aligned row
  in `upgrade`'s own format: `regenerated …` when the page moved, `already
  current …` when it did not, `no memo on this board — nothing to index` when
  the board holds none. It sits before the `plant_graph` loop because
  `knowledge.py board` reads the memos this step indexes — the ordering
  `plant_graph`'s own docstring fixes.
- `.pearde/prds/upgrade-leaves-the-memo-index-stale/probe/verify.sh` — 40
  checks, sections A-H. It builds the old shape rather than describing it: the
  example board copied through `shutil.ignore_patterns("README.md")`, which is
  literally what `init --example` did before the index step existed. Section A
  sees that fixture red before anything repairs it; section F strips the call
  back out of a *copy* of `init.py` and watches the red return; section G
  mutates the copy's `memos.py` to fail and asserts the line names `upgrade`
  and not `init`. Every command runs under a HOME holding no Obsidian config,
  so no fixture reaches this machine's real vault list — section H asserts it.

## What is left to finish

Nothing to build. Run it, tick the boxes, and read the two notes below.

- The `vision` row still differs between the two boards — `write_board` copies
  the vision template on `init` and `upgrade` seeds no `vision.md`, so an
  upgraded board reads `vision off` where a fresh one reads `vision ok`. Doctor
  calls that `off`, not `broken`, so both boards are green; the harness excludes
  that row by name, and closing it is a separate contract named in the report.
  Do not widen this unit to cover it.
- Section H's last line reports `skip`, not `ok`, whenever another session's
  probe wrote the machine's Obsidian vault list mid-run. That is
  `memos/a-check-decided-by-scheduling.md` applied: the race-free half of the
  obligation — no path of *this* run reaching that file — is the check above
  it, and it is a real `ok`. A skip is never a pass; quote the counts as they
  print, `39 pass · 0 fail · 1 skip` or `40 pass · 0 fail · 0 skip`.

## Acceptance

- [x] `upgrade` on a board that holds a memo and no index writes
      `memos/README.md`, and `memos.py check` on that board then exits `0`
      saying nothing — where before the upgrade it exits `1` saying
      "the kind index is stale".
- [x] The page `upgrade` writes is byte-identical to the example board's own
      `resources/board/example/memos/README.md`, and to the page a fresh
      `init --example` board carries.
- [x] `doctor` on the upgraded board exits `0`, closes on "every part this repo
      owns checks out.", and its `memos` and `knowledge` rows both read `ok`.
- [x] No doctor row reads `broken` on either board, and every row's verdict
      except `vision` matches between the upgraded board and a fresh one — the
      row reader having read all 18 rows, not zero.
- [x] A second `upgrade` prints `already current` and leaves the page's bytes
      unchanged; an `upgrade` of a board with no memo prints
      `no memo on this board — nothing to index`, writes no page, and doctor
      calls that board green.
- [x] Taking the `index_memos(board, "upgrade")` call back out of a copy of
      `init.py` makes `memos.py check` exit `1` again and doctor's `memos` row
      read `broken` — the boxes above are checks that can fail — and the copy
      is restored, proved with `cmp`.
- [x] A `memos.py index` that fails is said rather than swallowed, and the line
      begins `upgrade: could not regenerate memos/README.md`, never `init:`.
- [x] No fixture path from the run appears in this machine's Obsidian vault
      list, and none reached the live daemon's board list. The registry
      *file* cannot carry this obligation and the box no longer claims it
      does: `save_entry` returns early on an ephemeral path
      (`serve.py:385,402` — `EPHEMERAL` covers `/var/folders/`, where every
      fixture here lives) and `entry_path` is board-local, so no run of this
      probe can move `.pearde/.state/serve.json`. Its mtime is `Sep 1
      13:22:54` through five probe runs *and* through a stray registration
      made during implementation — the exact failure this box exists to
      catch, which a byte-identity check read `ok` straight through. The
      probe now asks the daemon instead, and that predicate has been seen
      red: `0` clean, `1` after an `init` without `PEARDE_PORT=1` reached
      `127.0.0.1:8443`, `0` after `serve.py forget`. It stands down to `skip`
      when the daemon is down, because down is not the same answer as clean.
- [x] The four harnesses this footprint touches stay at their baseline counts:
      `init-seeds-a-board-doctor-calls-green` 41/41, `guard-on-is-one-command`
      78/78, `readme-in-three-rings` 74/74, `the-next-line-runs` 96/96 — and
      `python3 resources/index.py check` prints nothing and exits `0`.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
# the footprint file itself: the call site is present, and the module parses
grep -n 'index_memos(board, "upgrade")' resources/board/init.py
python3 -c "import py_compile;py_compile.compile('resources/board/init.py',doraise=True)" \
  && echo "resources/board/init.py compiles"
bash .pearde/prds/upgrade-leaves-the-memo-index-stale/probe/verify.sh </dev/null
bash .pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe/verify.sh </dev/null | tail -1
bash .pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh </dev/null | tail -1
bash .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh </dev/null | tail -1
bash .pearde/prds/the-board-runs-itself/the-next-line-runs/probe/verify.sh </dev/null | tail -1
python3 resources/index.py check && echo "index ok"
```
