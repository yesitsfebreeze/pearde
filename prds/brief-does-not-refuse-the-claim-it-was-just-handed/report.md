# report — brief does not refuse the claim it was just handed

**DONE.** spec01: 5/5 boxes, every one re-run personally against what is on
disk now, none taken on the analyst's word. Probe 7/7. `## Verify and Proof`
exits 0.

## The question the orchestrator asked

> whether `pearde brief <prd> --worker <name>` now succeeds without `--force`
> on a PRD that worker just claimed.

**It holds.** Proven two ways, not one.

Live, on this board, on this PRD, with its real `claim: impl-11 2026-08-31 18:42`:

```
$ python3 resources/pearde.py brief brief-does-not-refuse-the-claim-it-was-just-handed --worker impl-11
# brief brief-does-not-refuse-the-claim-it-was-just-handed · implementer · as engineer · wf none · repo /Users/feb/dev/infra/pearde
exit 0
```

Exit 0, the implementer brief, **no `· forced` on the header, nothing on
stderr**. Through the `pearde` CLI wrapper, not just the module — the path the
loop actually runs.

And end to end, the documented steps 4·5 in order on a throwaway board, with
`claim` doing the writing rather than a hand-written fixture:

```
$ python3 resources/board/transitions.py claim e2e w9 --board $B
▸ e2e: open → analyzing …
  state: analyzing   claim: w9 2026-08-31 18:43
$ python3 resources/board/brief.py e2e --worker w9 --board $B      # no --force
# brief e2e · analyst · as engineer · wf none · repo …
exit 0
  state: analyzing   claim: w9 2026-08-31 18:43   ← untouched; brief still writes nothing
```

So the routine dispatch no longer needs the escape hatch. Stop forcing.

## What still refuses, checked one by one

The worry with this fix is that it buys the loop its convenience by disarming
the gates. It does not. Each of these was run, not reasoned about:

| case | result |
|---|---|
| no `--worker` at all | exit 1, `held — … is `claimed`, `claim: impl-11 …`` |
| `--worker an-15` (a different worker) | exit 1, `held —`, naming the real holder |
| self-claim + a `needs:` not done | exit 1, `gated — needs: needsdep is `open`, not done` |
| self-claim + footprint clash with a `claimed` PRD | exit 1, `clash — footprint: fpother is claimed and holds `shared/thing.py`` |
| self-claim + state `blocked` | exit 1, `state — … not open or specced` |
| `open` PRD already holding a matching claim | exit 1, `held —` — the odd corner stays shut |
| `--force` | unchanged: `pearde brief: forced past …` on stderr, `· forced` on the header, exit 0 |
| `--worker` with no value / `--workr` | refused by the flag parser, writes nothing |

The exemption lifts exactly one gate word, `unclaimed`, and only when the
worker named is the worker in `claim:`. `leaf`, `container`, `needs`,
`footprint`, `workflow` and the `state` pre-check all still fire.

I read the mechanism rather than trusting the spec's account of it:
`plan.dispatchable` gates on `if held and held["who"] != holder`
(`plan.py:1448`), and I enumerated every caller. All six others —
`plan.py:1633/1730/2076/2078`, `collect.py:1071`, `transitions.py:175` — pass
three positional arguments, so `holder` is `None` and `held["who"] != None` is
always true: byte-for-byte the old, stricter test for everything that is not
`brief` naming a worker. `transitions.py:293`, the `claim` branch, likewise
passes no holder. Nothing else on the board got quietly more permissive.

## The board moved under box 2, and I corrected it

The analyst wrote box 2 and the `## Verify and Proof` block against
`--worker an-15` with `state: analyzing`, asserting a `clash` against
`collect-defaults-to-the-boards-enclosing-repo`. Both facts have since expired:
this PRD is now `claim: impl-11`, `state: claimed`, and that other PRD has
collected, so the clash is gone. Run as written, the block would have proved
nothing — `an-15` is now merely *a different worker*, and its `held` is the
refusal case, not the acceptance case.

The box said in its own words it was "written to be re-run then". So I made it
re-runnable instead of stale: box 2 and the Verify block now read the holder out
of the PRD's own `claim:` line and assert on that, plus assert that a
non-holder is still refused. The spec's intent is unchanged; only its
dependence on a moving target is gone. The outcome is the *clean* half the box
predicted — exit 0, no `· forced` — not the `clash` half.

## State of the tree, for collect

Three of the four footprint files are **already committed** — `brief.py`,
`plan.py` and `loop.md` were swept into earlier commits by other PRDs'
collects. One hunk is uncommitted and is what remains to collect:
`resources/board/transitions.py`, `gate_claim` gaining `holder=None` and
threading it into `dispatchable` (7 insertions, 3 deletions). I committed
nothing.

`brief.py:210`'s `collectlib.repo_of(prd, board, board_root)` is present and
untouched, as instructed.

## Defects outside this scope — reported, not fixed

Two documents describe `brief`'s interface and are now stale. Both are outside
spec01's footprint, so I left them alone:

- `README.md:73` — the step 4 row still reads `pearde brief <prd>`, without
  `--worker`. It mirrors the `loop.md` table that this PRD updated, so the two
  now disagree.
- `references/parts/handles.md:55` — the flag list reads
  `brief <prd> [--role <role>] [--as <id>] [--force]`; `--worker` is missing.

Also seen, unrelated to this PRD and pre-existing: `doctor` reports three
`broken` rows — `skills` (no `.md` in `skills/`), `guard` (`resources/guard.py`
does not refuse a hand-walked board; the file is another PRD's uncommitted
work-in-progress right now) and `origin` (3 derived PRDs with no `from:`). The
rows this PRD touches are green: `briefs ok`, `index ok`, `board ok`.
