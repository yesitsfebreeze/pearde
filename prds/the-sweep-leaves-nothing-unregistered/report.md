# report — the-sweep-leaves-nothing-unregistered

**DONE.** 1 spec, 4 of 4 acceptance boxes ticked, each re-run by hand against
the tree as it stands now. No code change was needed — both halves were
already built and uncommitted; this round verified them independently and
repaired the spec's `## Verify and Proof` block, which could not fail.

## What I changed

| file | change |
|------|--------|
| `.pearde/prds/the-sweep-leaves-nothing-unregistered/specs/spec01.md` | ticked the 4 boxes; rewrote the Verify block so its exit code tracks the boxes |

Nothing else. `references/files.md`, `index.md` and
`.pearde/memos/the-board-keeps-two-journals.md` already held the built work —
I read them, did not revert them, and did not need to edit them.

## The Verify block was broken on the trap the correction names

As written by the analyst the block ended on:

    test -f .pearde/memos/the-board-keeps-two-journals.md && echo "memo present"

`collect` reads the LAST command's exit code, so that block exited 0 whenever
the memo file merely existed — `index.py check` could fail, the registration
could be missing, and `collect.py` could still alias the transitions writer
under a `HISTORY_*` name, and the spec would pass. The two bare `grep`s above
it were the mirror trap: correct output, exit 1, and had either been last it
would have failed the spec on being right.

The block now chains every assertion with `&&` and closes on an explicit
`echo`, so it exits 0 exactly when the four boxes hold. Both directions were
tested, not assumed:

| test | result |
|------|--------|
| block as written in the spec | `spec01 verified: archive.md registered, memo decided, journals named right` · `EXIT=0` |
| one assertion falsified (registration pattern absent) | `EXIT=1`, echo never printed |
| a negated assertion made false | `EXIT=1`, echo never printed |

## Box-by-box evidence

**Box 1 — `python3 resources/index.py check` exits 0, silent.** Ran from
`/Users/feb/dev/infra/pearde`. No output, `exit=0`. `doctor`'s own row agrees:
`index ok · 118 files · 31 keywords · every anchor resolves`.

**Box 2 — `references/archive.md` registered in both places.**

`references/files.md:33`

    | @references/archive.md | how a finished PRD leaves `prds/` — the flat `prds/archive/` shape, and why `scan` already ignores it |

`index.md:48`, the `@@board` Keywords row, last entry:

    | `@@board` | what the scan walks and what it parses | … · @resources/board/init.py · @references/archive.md |

The row sits under the `references/` — read table beside `files.md` and
`language.md`, and the keyword is the one whose subject the file matches.

**Box 3 — the memo.** `.pearde/memos/the-board-keeps-two-journals.md` exists
with `kind: decision` and `status: decided`. `python3 resources/memos.py
check` is silent, `exit=0`; `doctor` reports `memos ok · 17 memos ·
frontmatter checks out`. The memo records the split: `.history.jsonl` is one
row a day (a board-count aggregate, written by `plan.write_history()`, deduped
same-day, capped at 400, read to draw the burn-down), `.transitions.jsonl` is
one row a transition. Different shape, writer, reader and purpose — so the
finding's design question resolves to a memo, not a code change, exactly as
the PRD's second branch requires.

**Box 4 — the naming defect is gone.** `resources/board/collect.py` defines
`TRANSITION_FILE` (line 80) and `def transition_row(...)` (line 708), called
at 913, 1051 and 1138. Neither `HISTORY_FILE` nor `def history_row` appears
anywhere in the file — asserted negatively in the Verify block, not just eyeballed.
`resources/board/specs.py:25` names `.transitions.jsonl`; `history.jsonl`
appears nowhere in it.

## Out of scope — reported, not fixed

`doctor` is red on two rows that this PRD does not own and whose files are not
in its footprint. Both look pre-existing and neither names this PRD:

| row | what it says |
|-----|--------------|
| `workflows` | `broken · 0 workflows · 0 atomics · 66 problems` — ~20 PRDs and specs across the board carry `workflow: probe-then-spec` / `implement-a-spec` / `correct-a-documented-claim`, and the library holds no such slug |
| `skills` | `broken · skills/ holds no .md file — there is nothing to install` |

`resources/workflows.py` is modified in the working tree by this round's other
work, so the `workflows` row may be mid-flight in another PRD. I left both
alone.

## Note for the orchestrator

The board's other work has `references/files.md` and `index.md` modified in
the working tree. I built on them and reverted nothing. I committed nothing,
and did not read or write `.pearde/.state/round.md`.
