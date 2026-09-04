# The fan-out is a probe, not a person

Written 2026-09-03 12:05 by the pass worker for
`the-board-is-a-real-directory-at-pearde-never-a-symlink/init-and-upgrade-write-the-dotted-board`
(pid 87419, under dispatcher 62159). Kept under its own name: any sibling
rewriting `pass.md` clobbers it.

## The correction

`pass.md` records the 11:56 fan-out as **`pearde run` invoked four times on one
row** by a person, and says *"A person kills them; the board cannot."* That
diagnosis is wrong, and acting on it will not stop the recurrence.

**Two acceptance probes dispatch the whole machine for real, every time they
run.** There is no read-only `run` verb: `READ_VERBS` in
`resources/board/run.py:393` is `("boards", "slots", "progress", "groups")`.
`all` is not in it, so `main()` falls through to
`dispatchlib.main(rest, entries=entries)` — a live launch of every ready row on
every watched board — unless `--dry` is in `rest`.

Both probes call it without `--dry`:

- `.pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh:59`
  — `python3 "$ROOT/resources/board/run.py" all 2>&1`, inside the box
  *"a row the frontier marks ready but claim refuses is skipped"*. Line 43 in
  the same file gets `--dry` right; line 59 does not.
- `.pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/verify.sh:29`
  — `OUT="$(cd / && python3 "$RUN" all 2>&1)"`.

The second is the harness the first calls its **"read-only" sibling** (parallel
probe line 64-69, asserting it is *still 33/33*). It is not read-only. One run
of the parallel probe therefore dispatches the machine twice.

## Why it compounds

It is a feedback loop, not a one-off. A probe dispatches every ready row → each
row's pass worker runs probes → those probes dispatch again. The process table
at 12:03 showed `verify.sh` chains six deep by ppid:

```
55326 → 55327 → 55330 → 55331 → 55332 → python run.py all (55333)
                                          → claude --print /pearde run <row> (62159)
                                            → this pass worker (87419)
```

Six live `run.py all` processes, six `pearde run` dispatchers, 32 `claude`
processes. Three dispatchers on this one row (33739 at 12:02:26, 56476 at
12:02:54, 62159 at 12:03:04) — the same shape as 11:56, from the same cause.

This is also why the 11:56 count was four and nothing refused: nobody typed it.

## What a person does

1. Kill the runaway — the `run.py all` processes and the `verify.sh` trees
   above them, then the orphaned `claude --print … /pearde run` dispatchers.
   Killing dispatchers alone does not stop it; the probes respawn them.
2. Put `--dry` on both call sites, or give `run.py` a read verb for the frontier
   listing and use that. The parallel probe's line 59 wants the rows the read
   marks ` ready ` — check `--dry` still prints them before assuming the flag
   is a free swap; line 43's output shape is `would`/`skip`, not ` ready `.
3. Only then re-run either harness.

Until 1 and 2 are done, **every harness run and every collect that touches these
two probes re-dispatches the machine.** The realpath lock
(`no-work-is-lost-on-the-board/the-board-locks-by-realpath`) narrows the blast
radius to one worker per board but does not close this: the probes are the
thing calling the launcher.

## This pass dispatched nothing, on purpose

`…/init-and-upgrade-write-the-dotted-board` was already `claimed` by
`impl-dotted-init` at 12:03 — the first dispatcher on the row (s33739) has it.
A second implementer into one lane is what `s7022` refused at 11:57 and what
this window refuses now. Dispatching anything at all would have fed the loop.
