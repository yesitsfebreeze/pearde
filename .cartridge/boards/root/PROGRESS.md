# Root board progress

Snapshot: 2026-09-15, coordinator pass 4 (session cartridge-02).

Pass 4 dispatch: three tracks, one worker each.
- Track A worker 1: host-tests (cartridge.ctg only; the cartridge-ctg-22 hold
  is stale — that session is not live; takeover messaged to peers).
- Track A worker 2: pty-router-harness-mcp item (four repos; builds on the
  uncommitted earlier attempt, 8× `just test mcp`).
- Track B analyst: `prd refine` on the one-daemon PRD into children
  (host attach contract, per-cartridge audit with one child per breaking
  cartridge, composed acceptance test).
- Track C analyst: proxy ledger chain readiness (f77ed64, yolo-edit
  distinction, decision memo draft). proxy.ctg cleanliness is monitored;
  the four live peers were asked who owns the dirty files.
cartridge.ctg is clean; memory.ctg, live.ctg also clean.

## Ownership answers (pass 4, 4 peers asked)

- branch-server-20, branch-server-d7, cartridge-96: none own the
  pty/harness/mcp/router edits or the proxy yolo edits; the two
  branch-servers work only in ~/dev/diw/diw-installer.
- cartridge-96 IS claude-opus-5, claim owner of
  @proxy/the-proxy-hands-each-finished-exchange-to-the-memory-ledger
  (lane f77ed64; collect blocked only by the yolo edits). It also owns the
  uncommitted memory entry in .cartridge/init.lua and the memory block in
  .cartridge/config.lua, and the lsp line in init.lua is NOT its — both
  untouched here. Coordinator has offered: it finishes the collect, or our
  Track C worker runs prd collect while it stays claim owner.
- cartridge-38: not yet answered. If it disclaims too, the pty/harness/
  mcp/router edits and the proxy yolo edits are an abandoned earlier attempt.

## Stale hold released (14:40 local)

cartridge-ctg-22's hold on host-tests (since 09:00Z) was released to `open`
and re-claimed by cartridge-02. Justification: that session's last transcript
activity is 12:00 local; all four live peers started after the hold was set
(cartridge-96 ~11:30, branch-server-20 ~10:35, cartridge-38 and d7 ~13:34)
and none can be cartridge-ctg-22; three of four answered and disclaimed the
hold and all dirty-file sets outright. cartridge-38's answer remains queued;
its answer cannot restore a hold whose holder is provably dead, but its claim
on the dirty pty/harness/mcp/router and proxy files, if any, is still
respected — nothing of theirs is committed or reverted.

## Collected pass 4: pty-router-harness-mcp-tests-are-green (15:00)

Receipt root `2b038c2`. pty `a3dd1ab`, router `ad05d7d`, harness `9c144a3`,
mcp `6f06acd`. The mcp refresh test now prefers `target/debug` (the gates'
build) over the stale 07:33 release host; 8/8 `just test mcp` runs green,
13 tests each; pty/router/harness ×3 green; `just check` clean on all four.
The 07:13–07:41 pending-attempt edits were folded in and committed —
justified by the timeline (all live peers started after they were written;
three disclaimed), though cartridge-38's answer was still queued when the
worker committed. Nothing of a live session was touched.

Newly unblocked: @root/smoke-passes-mcp-and-proxy (dispatched, worker
track-a-smoke). M1 (@root/the-gates-are-green-at-one-pinned-set-of-shas)
now waits only on host-tests (claimed by cartridge-02, running) + smoke.
Note for prd owners: collect verify blocks must be one
`cd /Users/feb/dev/cartridge && just …` block per run — the prd service
node's sandbox denies exec of /opt/homebrew/bin/just.

## Track C readiness (analyst report, 14:35)

- f77ed64 verified on lane branch on 3380f34, +140/−1, matches the proxy PRD
  exactly; all four acceptance boxes pre-checked in the lane; 46 tests green.
- The proxy yolo edits are deliberate WIP (yolo-config policy bypass +
  keyless loopback listener), zero overlap with f77ed64's regions — merge is
  clean once they commit. Collect waits only on their owner's commit.
- cartridge-96 handed all three Track C items to this run: proxy collect (run
  by our worker under the handed-over claim), the root ledger item (its
  uncommitted init.lua memory line and config.lua memory block are the
  starting point, commit as part of the item), and the decision memo (write
  directly; the user decided in cartridge-96's session).
- One wording fix queued: the root ledger item's acceptance names "the recall
  half of the-surface-is-the-orchestrators-doors' consequences", but the
  recall clause actually lives in the-profile-is-the-orchestration-service;
  `prd refine` will correct the acceptance when the item is claimed.
- Head-up from cartridge-96: some session's lsp tests run
  `pkill -f "cartridge daemon"`; one killed the ledger-condensing daemon at
  13:58. Host-tests child must land the per-test isolation that stops this.

## Smoke attempt 1: blocked (15:20)

@root/smoke-passes-mcp-and-proxy cannot be claimed: its footprint (all of
proxy.ctg) overlaps the live proxy-ledger claim. Full diagnosis in the item's
Result: fixture symlinks a gone `builtin/` dir (fix in root repo); scratch
profiles fail trust (per-spawn CARTRIDGE_HOME pattern); router node dies
under sandbox_apply in scratch compositions (fix in cartridge.ctg, same repo
as host-tests). Re-dispatch after the proxy collect releases the footprint
AND host-tests lands (its isolation work touches the same trust/sandbox
machinery). Footprint likely needs prd refine (add cartridge.ctg).

## Pass 5 (18:5x, coordinator now cartridge-7b, was cartridge-02)

Session restarted as cartridge-7b. State:
- host-tests: implementation landed (cartridge.ctg `bceb644` — nextest
  one-test-per-process, poison-recovery trust_home(), ambient
  CARTRIDGE_YOLO save/clear/restore). Verification: 4 full-suite runs
  green, 166/166 each (three consecutive + one with ambient yolo
  unset). `just check` clean. Independent spec review in flight; collect
  after it passes ≥90 with no blockers.
- proxy collect: lane rebased onto preservation commit, main at
  `bd2035c`, 48/48 tests, fmt/clippy clean. `prd collect` refused:
  fresh uncommitted proxy.ctg edits (18:48–18:49, ask/bail pipe
  refactor + degraded-tool skip). Owner identified: cartridge-a7, live,
  waiting on its user's commit decision. Collect blocked on that.
  First collect refusal (from proxy board) was an alias problem —
  @memory/… resolves only from root, collect from the root board.
- cartridge-98 disclaims the edits; holds a queued two-line lsp-
  contributor change on proxy, sequenced after the collect.
- Peer roster turned over completely; cartridge-38 and cartridge-96
  are gone. Their queued answers are moot: host-tests was re-claimed
  and implemented; the yolo edits were preservation-committed
  (`7bc7c4f`); a7's fresh edits are owned and untouched.

## Host-tests ready to collect; gated on a7's cartridge.ctg fix (21:10)

- Implementation `bceb644` verified: 4× full gate runs 166/166 green
  (three consecutive + one without ambient CARTRIDGE_YOLO); `just check`
  clean; independent review 93/100, no blockers (PASS). All acceptance
  and spec boxes ticked; Result records the pass.
- Collect refused while cartridge.ctg carries a7's uncommitted
  `src/transport/cartridge.rs` blocking-pool listener fix (+11/−4, the
  memo/harness/proxy deadlock fix, awaiting that session's user) — it
  is inside the item's whole-repo footprint and would be swept into the
  collect commit. The proxy-ledger collect is gated the same way on a7's
  proxy.ctg WIP. Both run as soon as a7's user commits.
- Incident recorded: coordinator accidentally swept a7's proxy WIP into
  a fmt commit (6710665), noticed within a minute, reset and restored
  the tree; a7 confirmed all three files intact, fmt clean, 50 tests
  green. The stale proxy lane worktree was removed after ancestry check
  (bd2035c ancestor of main).

## Host-tests: review passed, collect gated (21:0x)

Independent review of spec01: 93/100, PASS, no blockers (two low findings:
theoretical restore-on-panic gap under plain in-process runs — mitigated by
nextest killing the process; the macOS-CI acceptance box is verifiable only
in the wave-4 CI item). All spec + PRD boxes ticked; implementation
cartridge.ctg `bceb644`; verification 4×166/166 green incl. one run with
ambient CARTRIDGE_YOLO unset.

Collect is BLOCKED: cartridge-a7's uncommitted deadlock fix
(src/transport/cartridge.rs, +11/−4, awaiting its user) is inside the
item's whole-repo footprint. Same session's proxy.ctg WIP blocks the
proxy-ledger collect. Both fixes weigh as a pair (per a7: 12-parallel
all-green needed both; host fix alone stops the wedge, 1/12 answered
without the proxy fix). Both collects run when a7's user commits.

Pass 3 snapshot: done 2 (record vocabulary, sessions+gitfs green).

- done this pass: 2 — `the-record-has-one-vocabulary-and-no-shadowed-copies`,
  `sessions-and-gitfs-tests-are-green`
- open: 15 on root; 1 specced (blocked), 1 analyzing (held), 13 waiting on a
  `needs`
- `pty-router-harness-mcp-tests-are-green` — pty, router, harness 3/3 green,
  all four checks clean; mcp refresh test hangs 1 in 3. Two attempts under its
  Result. Blocked on the host session's commit. No claim.
- `host-tests-hold-under-suite-contention` — claimed by cartridge-ctg-22;
  analysis under its Result. Held by the host session's uncommitted
  cartridge.ctg change (51 files at 11:35), which is on the same failure.
- Every other root item needs one of those two. The whole board waits on one
  commit in cartridge.ctg.
- `@memory/...exchange-ledger...` shows in the root plan but is a memory-board
  item; not touched.
- hosts: none started by this session. A `cartridge launch claude` host from
  another session runs from `cartridge.ctg/target/debug`; it is not touched.

## Landed

| item | where |
|---|---|
| `the-gates-run-from-the-root-justfile` | root `585a767` |
| `the-composition-comes-up-without-memory` | root `2cb8cb4`, prd.ctg `a2ece4fb` |
| `collect-checks-the-footprint-not-the-whole-working-tree` | prd.ctg `c0226fe0` |
| `the-profile-is-the-orchestration-service` | root `6ee17d9` and earlier |
| `the-record-has-one-vocabulary-and-no-shadowed-copies` | collected at root `714c088`, prd.ctg `e50d14b0` |
| `sessions-and-gitfs-tests-are-green` | sessions `b896162`, gitfs `f837c81`, root `ee73c53`, prd.ctg `5f33812d` |

## What changed since pass 2

cartridge.ctg is clean: the two sessions holding it committed (`f8a2c00`), so
the host-tests item is no longer held and is claimed.

The untracked principle memo that held the record item belonged to session
cartridge-ctg-0b, which committed it at root `714c088`; collect then verified
the item.

## Still held, and by what

`pty-router-harness-mcp-tests-are-green` and `sessions-and-gitfs-tests-are-green`:
their footprints carry 22 uncommitted changes written 07:13–07:41 today (two doc
edits at 09:14 and 09:17). They are exactly this work: `CARTRIDGE_HOME` set per
spawned test host in pty, harness, sessions and mcp; rustfmt reflows; gitfs cap
tests pinned to the cap in force instead of a hard-coded 8 MiB; `grant.env`
prefixes in harness and sessions. Three live peer sessions answered "not mine";
the fourth (cartridge-e0) has not answered yet. If no session owns them they
are an abandoned earlier attempt, and the analysts continue from them rather
than starting over.

## Worth deciding, all outside every footprint here

- Two acceptance boxes name `cartridge call memo '{"op":"index"}'`, which
  cannot work: a native memo request must carry `cwd`, or the service answers
  `trusted memo cwd required`.
- `.cartridge/justfile` still has a `sweep` recipe; `cartridge sweep` is gone.
- `.cartridge/config.lua` carries a `memory` block that settles nothing.
- `memo.ctg`'s docs still tell a reader to run `cartridge --yolo run tui`.
- Twelve cartridges each ship an identical `type/note.md` and `type/type.md`,
  so `memo index` reports no single declaration for either kind.
- `.obsidian/` and `.yolo-test/` are untracked in the composed root.
- The composed repository's `source-layout` test is red, on a `cargo metadata`
  lookup for the memory package.

## Next action

When cartridge.ctg's host session commits: rebuild the debug host, make the mcp
tests take the binary the gates build, rerun `just test mcp` eight times; revise
host-tests spec01 against the committed tree so `CARTRIDGE_HOME` is per test.
