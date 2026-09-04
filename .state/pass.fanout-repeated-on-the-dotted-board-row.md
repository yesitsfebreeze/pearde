# pass · the fan-out repeated, 2026-09-03 12:02-12:04

Kept under its own name because `.state/pass.md` has no arbitration and any
racing sibling clobbers it. Companion to
`.state/pass.duplicate-run-fanout-on-one-row.md`, which recorded the same
failure three minutes earlier on a different row.

## What happened

`.state/run-the-board-is-a-real-directory-at-pearde-never-a-symlink_init-and-upgrade-write-the-dotted-board.log`
holds **three** `pearde run … attempt 1` lines for one PRD inside 38 seconds:
12:02:26, 12:02:54, 12:03:04. Nothing refused any of them. Three pass workers
took three sessions — `s33739`, `s56476`, `s62159` — on one board.

At 12:03 `ps` showed **seven** live `claude --print … /pearde run` dispatchers
across five distinct rows. The realpath lock is still uncommitted in
`impl-lock-realpath`'s lane; until it lands this repeats on every row a person
types twice.

## How the race actually resolved — the useful finding

The claim *is* a working arbiter when the losing worker uses a **name of its
own**. `s33739` (first by ~30s) took the scoped row and six more. `s56476`
claimed all seven with `-6476`-suffixed names and got seven clean refusals:

```
pearde claim: refused — claim: …/init-and-upgrade-write-the-dotted-board is `claimed`
pearde claim: refused — claim: …/a-claim-names-the-process-that-holds-it is `analyzing`
```

No stand-down judgment was needed and no second implementer entered a lane.
This is the counter-case to the 11:57 incident, where the note observed that
*a worker whose own claim name matches briefs itself without refusal* — the
danger there was that every sibling reaches for the same obvious name
(`impl-lock-realpath`). **Suffix every worker name with the session id.** It
converts a silent self-brief into a loud refusal, and costs nothing.

That belongs in the mechanism, not in a pass file: `pearde claim` could derive
or reject an unsuffixed name itself.

## What s56476 did instead

Rather than idle, it took the five `specced` rows `s33739` had not reached and
dispatched five implementers at 12:04, all verified alive at 12:04:36:

| PRD | worker |
|---|---|
| `a-pass-holds-its-turn-until-its-workers-are-in` | `impl-pass-holds-6476` |
| `no-work-is-lost-on-the-board/collect-runs-the-invariants-and-red-refuses` | `impl-collect-inv-6476` |
| `the-tree-holds-only-what-a-board-uses/install-fetches-nothing` | `impl-install-nofetch-6476` |
| `the-tree-holds-only-what-a-board-uses/ramp-is-a-doctor-row-not-a-gate` | `impl-ramp-row-6476` |
| `the-tree-holds-only-what-a-board-uses/scout-s-research-leaves-the-tree` | `impl-scout-out-6476` |

After those five claims the board reported **ready 0** — every dispatchable
row on the board is held by a worker.

## 12:11 — the first collect of the new red-refuses era unmerged itself

`impl-ramp-row-6476` returned DONE at 12:11, 16/16 boxes, probe 19/19 green.
`pearde collect` merged the lane, ran `spec01`, and got:

```
collect: …/ramp-is-a-doctor-row-not-a-gate: spec01 exit 127 — nothing written
spec01: exit 127
bash: .pearde/prds/…/ramp-is-a-doctor-row-not-a-gate/probe/verify.sh: No such file or directory
  unmerging 1 commit(s) — dropping references/files.md, references/parts/doctor.md,
  references/parts/handles.md, references/parts/loop.md +5 more, back to 7a162c2
```

The probe exists on the board. The Verify block named it **relative to its
cwd**, and collect runs it inside the lane worktree, whose `.pearde/` is empty
because the board is gitignored. This is the finding pass.md has carried all
day — *nothing stops a fifth* — and this is the fifth. What changed is that it
is no longer silent: with red refusing the collect, it now **unmerges good
work**.

Repaired by hand in `spec01.md` and `spec02.md` with the established form:

```sh
B="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)/.pearde"
```

and filed as a PRD at last —
`a-verify-block-resolves-the-board-absolutely-not-from-its-cw`, p92,
`origin: derived`, `open`. The ask is the **refusal**: `pearde specced` accepts
the broken shape, which is why five have been written. Four more live PRDs
carried it at 12:14 — `a-harness-measures-the-tree-its-worker-built-in`
(30/31), `no-work-is-lost-on-the-board/collect-runs-the-invariants-and-red-refuses`
(whose own collect would defeat itself), `…/a-lane-rebases-before-collect` and
`…/a-conflicted-lane-is-reported-not-stranded`. Only the second was repaired
here — the others are other sessions' claims and one writer owns a PRD.

## Liveness: line growth, not mtime

The mtime of a subagent's `.output` under `tasks/` **lags badly** — four
transcripts read 712-718s stale while three of the four had visibly grown
between two reads. `stat -f %m` produced a false STALLED twice. Count lines
between polls instead; and `tail -1 | jq .type` distinguishes a worker parked
in a long `tool_use` from a finished one.

## Sessions at 12:15

`s7022` died and was reaped (1 tree, `refs/pearde/reaped/s7022`). Alive:
`s9856` (interactive, owns the two `collect` rows), `s33739`, `s56476`,
`s88291`.

## 12:29 — the second collect unmerged too, and the reason is worse

With the path repaired the probe went green — all four `PASS` rows printed.
The collect **still unmerged**, on `spec02`'s remaining three verify lines.
All three are defective, and two of them in the same direction:

```sh
python3 resources/index.py check                      # exits 1 on 4 standing problems
grep -c happiness references/settings.md              # exits 1 when the count is 0
grep -c '0 ramp' references/parts/loop.md             # exits 1 when the count is 0
```

The block's own boxes say `grep -n 'happiness' references/settings.md` must
**match nothing** and `loop.md` must hold **no** `0 ramp` row. A bare `grep -c`
exits 1 on zero matches. **The block is green only while the work is undone,
and red the moment it succeeds.** The third line asserts a clean index, while
its box says *"no problem that was not already there — the four standing ones
are named in the report as out of scope"*.

So a correct implementer, 16/16, probe green, was unmerged twice by its own
spec. Rewritten to say what the boxes say: the four standing index lines are
listed in a heredoc and only a *new* problem reddens; the two greps become
`! grep -q`. This is a strengthening — the block now fails when the boxes are
false — not a weakening to force a pass.

Not filed as a third PRD: `an-acceptance-box-that-cannot-fail-is-refused` and
`a-verify-block-that-pipes-a-probe-exits-zero-on-a-broken-tre` already own this
ground, and the derived tripwire says fold rather than file. But neither
catches the *inverted* case, and `pearde specced` should: **a verify line whose
success condition is a zero count must be `! grep -q`, never `grep -c`.** That
one sentence belongs in whichever of the two PRDs is still live.

## The four standing index problems, for whoever fixes them

Two are the wake of landed commits, two are older:

- `resources/common.py` on disk, no row in `references/files.md` — from
  `7e4d610`.
- `references/files.md` lists `@resources/board/hotreload-test.js`, deleted by
  `b1d3f5d`. `@@view` names it too.
- `references/parts/commits.md` cites `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`
  — the standing `index check` failure pass.md has carried all day.

Every spec whose verify block runs a bare `index.py check` will unmerge until
these four are closed.
