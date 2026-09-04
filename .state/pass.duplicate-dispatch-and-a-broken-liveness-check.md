# pass — this run was a duplicate, and the liveness check every pass uses is broken

Written 2026-09-03 09:20 by the pass worker of session `s47729`
(transcript `3706ce59-…`, agent `abef19454548f9608`), scope
`the-board-is-a-real-directory-at-pearde-never-a-symlink`.

**Deliberately NOT written to `pass.md`.** A live pass worker owns that file
and rewrites it whole at every transition; two writers on one file is how a
pass loses its memory. Fold what is below into `pass.md` when the live pass
has finished, then delete this file.

## Three pass workers were running on one board

| session | transcript | pass agent | what it holds |
|---|---|---|---|
| `s29969` | `5cb9dbba-…` | `a6460a700a8cb555f` | **the real one** — 8 implementers + the analyst for this scope |
| `s47707` | `ef98acb7-…` | `a17a3b36097a15c93` | duplicate, launched 09:16:15 |
| `s47729` | `3706ce59-…` | `abef19454548f9608` | duplicate — me, launched 09:16:15 |

`s47707` and `s47729` were started **within the same second** by two
`claude --print … /pearde run the-board-is-a-real-directory-at-pearde-never-a-symlink`
processes. `.state/run-<scope>.log` has both attempts, tagged `@pearde` and
`@pearde-2` — one log, two dispatchers.

**Nothing was left for either duplicate to move.** `pearde next` at 09:19 said
step 6 with four collects; three are `s29969`'s own live implementers
(`impl-the-cross-board-parts`, `impl-plan-cut`, `impl-two-harnesses`) and the
fourth is the container `every-run-session-works-in-a-worktree-of-its-own`,
which that pass will close on its own next turn. No `ready` section, no
dispatch. All ten of `s29969`'s workers were writing to their transcripts
within 3 seconds of 09:19:01 — **alive, not stale.**

**The scope's analyst was already out**: `analyst-pearde-dir`, claimed
09:16:19, is `s29969`'s subagent `a38e9573d5163920c`
(`pearde-analyst`, "Analyst: .pearde real directory", opus). Re-dispatching it
under the same claim id would have run two analysts on one contract.

**The rule this earns:** before a pass dispatches or collects anything, read
the *sessions ledger and the peer transcript metas*, not just `pearde scan`.
`scan` shows a claim; it cannot show that the claim's worker belongs to another
live orchestrator. `pearde session reap --apply` reporting `N left on the
ledger` with N>1 and real pids is the tell.

## The anchored liveness pattern is self-matching — every worker reads dead

`pass.md` tells every pass to check a worker is alive with

    grep -cE '"(text|content)":"API Error|"is_error":true.*API Error|Claude AI usage limit reached'

**Two of the three alternatives are anchored. The third is a bare literal.**
And `pass.md` prints the pattern itself, on its own line 127. So:

- every worker reads `pass.md`;
- the Read result puts `Claude AI usage limit reached` in its transcript;
- the grep scores ≥1;
- **the healthy worker is declared dead and re-dispatched.**

Measured on the twin pass worker `a17a3b36097a15c93` at 09:19, per alternative:

| alternative | hits |
|---|---|
| `"(text\|content)":"API Error` | **0** |
| `"is_error":true.*API Error` | **0** |
| `Claude AI usage limit reached` | **2** |

Both hits are the pattern's own text — one from reading `pass.md`, one from the
worker's own Bash command echoing it back. **Zero real errors.** The previous
pass fixed two alternatives and left the third, and the file that carries the
fix is the file that defeats it.

**The fix is to anchor the third the way the first two are anchored:**

    grep -cE '"(text|content)":"(API Error|Claude AI usage limit reached)'

Better still, stop publishing the pattern in the file every worker reads — put
it in a script (`resources/…`) and have `pass.md` name the script. A liveness
check quoted in a document that all its subjects read cannot stay honest.
**This is a derived PRD and it is not yet placed.**

## Free disk is falling ~1 GiB/minute and nothing on the board is the cause

| time | free on `/System/Volumes/Data` |
|---|---|
| 08:51 (previous pass) | 19 GiB |
| 09:17 | 11 GiB |
| 09:20 | **8.7 GiB** |

`pearde/.lanes` is **148 MiB** across 29 lanes and `pearde/.sessions` is
**12 MiB** — pruning lanes would recover nothing that matters. **The consumer
is outside the board.** Ten opus workers are running harnesses against it.

`pass.md`'s own standing warning: *a full disk makes harnesses lie, with no
error line.* At this rate the surface goes to zero inside ten minutes and the
live pass's ten workers begin reporting green boxes that are not green — and
their collects would commit them. **This is the reason to stop, and it needs a
person: find the consumer.** Neither `.lanes` nor `.sessions` is it.
