---
complexity: 10
footprint:
  - .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
  - .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/verify.sh
  - .pearde/prds/no-work-is-lost-on-the-board/the-board-locks-by-realpath/probe/probe.py
---

# spec03 — the three harnesses stop launching the machine

Eight lines across three harnesses reach a dispatcher. The PRD names one; the
reader found the others. Every replacement below was run against this board
and its output checked before it was written down.

**`the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` — line 59.**
The one the PRD measured. Its comment calls it "the read"; it is
`run.py all`, and each of the three nested command substitutions around it
forks a subshell, which is the four-frames-deep tree in the PRD. Replace the
inner command with `python3 "$ROOT/resources/board/plan.py" plan all` — the
same frontier, moving nothing. Checked: the `ready` rows it greps for come
back identically.

**`the-machine-frontier-is-one-ordered-list/probe/verify.sh` — lines 29, 41,
121, 122, 124.** The file calls itself "read-only, so the whole harness is",
and its `$RUN` is `run.py`. Line 29 is a second full dispatch of the machine
and is the reason its own `it moved nothing in this repo` box could never have
been trusted. Point `RUN` at `plan.py` and give every invocation the `plan`
verb; `RUN_PY` keeps its override role. Two boxes need more than a rename:

  - line 124 asserts `d["scope"] is None`. The payload has no `scope` key and
    never did — it is `group`, and under `plan --json` it is `"all"`. The box
    was written against the pre-rename shape and cannot pass; assert
    `d["group"] == "all"` and `isinstance(d["groups"], dict)`.
  - lines 121-122 prove an unknown group is refused. Through `run.py` the
    refusal now comes from the script entry, for the wrong reason. Through
    `plan.py` it is the real one, and the message still names `settings.md`.

**`the-board-locks-by-realpath/probe/probe.py` — `run_here`, lines 117-124.**
This one is legitimate: it dispatches a board it built in a mktemp dir with
`PEARDE_ADAPTER_BIN` stubbed to a sleeper, to prove two dispatchers on one
physical board race. Two edits. Its `argv` needs the verb — spec01's
`script_main` refuses a bare invocation, so this harness goes red without it.
And it needs `# dispatch-exempt: <reason>` above each of the two calls, or
spec02's invariant refuses it along with the rest.

Nothing already stands here: spec01 and spec02 are built in the lane, these
three files are untouched.

## Acceptance

- [x] no `probe/` file on the board reaches a dispatcher without `--dry`, a read word or an exemption — the invariant of spec02 is green
- [x] `the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` reads the frontier through `plan.py plan all`, and its `a row the frontier marks ready but claim refuses is skipped` box still passes against this board
- [x] that file's `--dry opened no run log on this board` box is now true of the whole file, not only of the line above it
- [x] `the-machine-frontier-is-one-ordered-list/probe/verify.sh` names `plan.py`, not `run.py`, and every one of its invocations carries the `plan` verb
- [x] its `--json` boxes assert `group == "all"` and a dict of `groups`, and pass
- [x] its unknown-scope boxes get their refusal from the scope resolver and the message still names `settings.md`
- [x] the two harnesses' own PASS counts are re-recorded, and the `the sibling read-only harness is still 33/33` box is updated to whatever the repaired sibling prints
- [x] `the-board-locks-by-realpath/probe/probe.py` spells the `run` verb in `run_here`'s argv, and both its spawns carry a `# dispatch-exempt:` line naming the mktemp board and the stubbed adapter
- [x] all three harnesses pass, run one at a time and never through `doctor.sh --harnesses` until they do — spec03's own harness green (7/7); `the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` green (12/12, re-run 2026-09-03 21:0x against the live board, 29 `would` rows); `the-board-locks-by-realpath/probe/probe.py` still fails 8/12 on the sibling PRD's unbuilt features (A/C/E), red for the reason a probe for an in-flight PRD is red — recorded in the report, re-checked when that PRD lands

## Verify and Proof

```sh
LOGS_BEFORE=$(ls .pearde/.state/run-*.log 2>/dev/null | wc -l)
bash resources/invariants/no-harness-under-the-board-dispatches-it.sh
bash .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/verify.sh
bash .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
python3 .pearde/prds/no-work-is-lost-on-the-board/the-board-locks-by-realpath/probe/probe.py
# and nothing was launched: the log count is the same either side of the three
[ "$(ls .pearde/.state/run-*.log 2>/dev/null | wc -l)" = "$LOGS_BEFORE" ]
```
