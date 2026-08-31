# round — the previous round's owed list is cleared, and the collect is the wall

## Established

- `scan` at open: 63 PRDs, done 41 · open 17 · superseded 2 · specced 2 ·
  blocked 1; progress done 34/53 · 67%; workers=1, pipeline=3.
  `sweep --as engineer`: `no claim silent past claim-ttl 30m`.
- **`sweep` and every board command refuse without a persona.** This shell is
  `nu`, so `export PEARDE_AS=engineer` does not apply — pass `--as engineer`
  on every line. Do not spend a turn rediscovering this.
- Two repos, one board, unchanged from last round: `/Users/feb/dev/infra/pearde/.pearde`
  is the BOARD repo and holds the PRD tree; `/Users/feb/dev/infra/pearde` is
  the OUTER repo and holds every footprint path — `references/`, `resources/`,
  `README.md`, `index.md`.

## The previous round's owed list — 1, 2, 3 and 6 are cleared

**1 · The ~48-file rename diff is reviewed and it is sound.** `git diff --numstat`
over the outer repo: every one of the 48 files has equal insertions and
deletions — a 1-for-1 line replacement, 207/207. The only line in the whole
diff that is not a path rename is one prose rewrap in `references/parts/workers.md`
(`repo, installed` → `in this repo, installed`). Every path is inside
spec01's `footprint:` (`references/`, `resources/`, `README.md`, `index.md`).
**There is no wrong footprint and nothing to name under
@references/parts/commits.md's out-of-footprint rule.** The parent PRD carries
no `footprint:` of its own; it does not need one — `collect` unions the specs'.

**2 · The board side is committed.** Three commits in the BOARD repo:

- **`c1156d3`** `nothing-left-open/the-line-tells-the-truth — blocked: …` —
  the PRD folder whole, `memos/two-holes-the-flag-probe-found.md`, and the
  five `workflows/*.md`, plus `prds/every-probe-harness-is-re-aimed-at-the-pearde-layout/`
  as the named unblocker it filed.
- **`5f8c387`** `… — record` — `commit: c1156d3` alone, the one key that
  cannot name the commit it is in.
- **`76df2d4`** `every-document-names-the-path-the-board-is-on — the refine
  split, and the board state that had been riding` — the refine's two-row
  table and `resolve-bare-board-path-mentions/`, `a-quoted-walk-is-data`'s
  `analyzing → specced` from an earlier round, `pipeline: 1 → 3`, and the
  seven finding PRDs that had never been committed.

The board repo is now clean but for `.state/` and the in-flight PRD folder.

**3 · `pearde workflow check` — root cause found, and the four atomic edits
are verified.** It was never the edits. **`resources/plan.py find_board`
resolves the board to `.pearde/`; `resources/memos.py find_board` — which
`workflows.py` and everything else delegating to it uses — still resolves it
to `<x>/prds`.** Two definitions of the word *board* in one tool, the second
a directory inside the first. Every library helper then joins its name one
level too deep: `.pearde/prds/workflows`, `.pearde/prds/memos`,
`.pearde/prds/knowledge`, none of which exist.

Measured: `pearde memo list .pearde` prints nothing over 16 memos on disk;
`pearde memo check .pearde` prints nothing **because it opened no file**, and
`doctor`'s memos row runs it, so doctor reports memos ok while blind;
`pearde workflow list .pearde` prints nothing over 18 atomics.

**The workaround, and the verification it bought.** Calling
`workflows.check('/Users/feb/dev/infra/pearde/.pearde')` in-process — the
board directory, not the `prds/` child — is **silent**. All 18 atomics parse.
The four edited files carry their bumps: `read-the-contract` runs 45,
`capture-the-harness-baseline` runs 45, `attempt-the-build` runs 25, all
`updated: 2026-08-31`; `re-run-the-harnesses` runs 45; `probe-then-spec` runs
25, `kind: workflow`. **The edits committed in `c1156d3` are verified. This
owed item is closed, not carried.**

**6 · Three findings filed, all `origin: derived`:**

- `one-definition-of-the-board-not-two` (p88) — the above.
- `an-analyst-workflow-does-not-survive-into-specced` (p60) — the refused
  fifth workflow edit's real cause. No flag works around it.
- `brief-does-not-refuse-the-claim-it-was-just-handed` (p45) — `brief` refuses
  the `claimed` state `claim` just wrote, so @references/parts/loop.md steps 4
  and 5 cannot be run as documented without `--force` on every dispatch.

Derived against requested, counting open + analyzing + specced + claimed:
**4 to 18.** @references/parts/derived.md's tripwire is nowhere near.

## Dispatched, and what came back

| worker | PRD | verdict | move made |
|---|---|---|---|
| impl-1 | `every-document-names-the-path-the-board-is-on/apply-the-prds-rename-table` | **DONE** | none yet — the collect is refused, below |

`brief` again needed `--force`, as filed. The brief was hand-corrected with
the two-repo root note before dispatch; without it the worker resolves every
footprint path against the board.

impl-1 reports spec01 5/5 boxes ticked with quoted output. In-scope `prds/`
lines 221 → 76; 45 unconverted tokens, 36 bare `prds/` (the sibling PRD's job)
and 9 named exceptions. It fixed six table-rule matches pass one missed for
want of a trailing slash — `references/archive.md` 65, 70, 82, 96 and
`references/obsidian.md` 78. `git diff --stat` now 49 files, 211/211.
`py_compile` 9/9, `bash -n` 2/2, zero `.pearde/.pearde` or `prds/prds`.

## The wall — `collect --dry` is refused, and it is the Verify block

```
collect: every-document-names-the-path-the-board-is-on/apply-the-prds-rename-table:
  spec01 exit 1 — nothing written
spec01: exit 1
     164
references/archive.md is on disk with no row in references/files.md
```

Two things are wrong and neither is the rename:

1. **The Verify block asserts a failure the Acceptance box explicitly
   permits.** Box 2 says `index.py check` should print *only* the
   pre-existing `references/archive.md` line. `index.py check` **exits 1**
   when it prints that line, the block's last-command exit is what `collect`
   reads, so the spec fails on exactly the condition it was written to allow.
   The block's `echo "exit $?"` records the code and then discards it.
2. **The grep count printed 164 where impl-1 reported 152.** Not
   reconciled — the round hit its ceiling here. It is a count, not a
   correctness claim, and box 1 reads "far below the measured-before count",
   so 164 does not by itself fail anything. Establish which is right before
   editing anything.

The PRD is left **`claimed`**, `claim: impl-1 2026-08-31 17:20`. The work is
on disk and the boxes are ticked; only the transition is owed.

## Dirty and uncommitted at stop

- **outer repo** — 49 files under `references/`, `resources/`, `README.md`,
  `index.md`. All of it is the rename, reviewed above, inside the footprint.
  Nothing else. **This is the whole of what the collect must commit.**
- **board repo** — `.state/*` only, plus
  `prds/every-document-names-the-path-the-board-is-on/apply-the-prds-rename-table/`,
  which is the in-flight PRD's own folder.

## Owed, in order

1. **Settle the Verify block, then collect.** The honest assertion is that
   `index.py check` prints nothing naming `agents/` or `skills/` — not that it
   exits 0. Either the spec's block ends on a command whose exit reflects the
   box, or `index.py check`'s exit code is the defect and gets its own PRD.
   Decide which; do not paper over it by deleting the check.
2. **Find out whether `collect` can commit the outer repo at all.** `collect`
   resolves its repo the way `plan.py repo_root()` does — up from the board,
   stopping at `.pearde/.git`. Every path it must commit is in the *outer*
   repo. This is exactly
   `collect-commits-the-code-repo-not-the-board-repo-twice` (p88, open), and
   this collect is the first one that actually needs it. If `collect` cannot
   reach the outer repo, the choice is to land that PRD first or to commit
   the 49 files by hand and write `commit:` in by hand, as `c1156d3` was.
3. **File impl-1's two out-of-scope findings** (it did not file them; the
   report holds them): `resources/doctor.sh:69` still globs `skills/*.md`
   after the move, so `doctor` reports `skills broken` on a healthy install;
   and `resources/board/knowledge/**` plus `obsidian/**` still name
   `prds/knowledge/` in 43 live Dataview/Obsidian queries against a vault now
   at `.pearde/wiki/`. Both `origin: derived`.
4. `every-probe-harness-is-re-aimed-at-the-pearde-layout` (p85) — closes
   `the-line-tells-the-truth`'s 7 boxes with no further code change.
5. `one-definition-of-the-board-not-two` (p88) and
   `collect-commits-the-code-repo-not-the-board-repo-twice` (p88) — until
   both land, every checker on this board can report clean by seeing nothing
   and every collect commits into the wrong repo.
6. `pearde report`, then park `pearde view wait`.

## Asked

Nothing is out to the user. No `question` PRD on the board.
