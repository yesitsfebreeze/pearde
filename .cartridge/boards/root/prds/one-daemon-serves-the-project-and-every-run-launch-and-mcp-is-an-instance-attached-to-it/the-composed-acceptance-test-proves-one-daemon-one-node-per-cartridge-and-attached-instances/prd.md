---
state: "claimed"
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/sessions-runs-once-in-the-daemon-with-one-buffer-id-space"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/mcp-keys-sessions-and-inflight-calls-by-attached-instance"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/router-refreshes-oauth-tokens-under-the-one-daemon-not-per-process"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/live-attaches-to-the-daemon-instead-of-spawning-its-own"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/prd-journals-and-outbox-replay-once-in-the-daemon"
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/agent-runs-key-per-attached-instance-not-per-process"
footprint:
- ".cartridge/tests/"
claim: "coordinator-5d0e-4 2026-09-19T12:01:29.761Z"
---

# The composed acceptance test proves one daemon, one node per cartridge and attached instances

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
its "composed test" analysis item. This is the parent's Acceptance, made
runnable as one composed test in cartridge.ctg.

## Outcome

One test composes the full profile, starts instances against it and proves
the parent's four acceptance boxes:

1. With a daemon running, `cartridge run memory '{"op":"status"}'` answers
   without starting any node process (count `cartridge node` children before
   and after).
2. Two `cartridge launch` instances and one `cartridge mcp` leave exactly one
   `cartridge daemon` and one node per composed cartridge.
3. A memory `ingest` from one instance is returned by `query` from another,
   with no writer-lock error; two instances' sessions and pty shells stay
   separate.
4. With no daemon running, two instances started concurrently end up sharing
   one daemon.

## What changes

- A composed test (likely under `.cartridge/tests/`, following the host-tests
  conventions: `CARTRIDGE_HOME` per test, no daemon kills by process name —
  use the documented stop command from the host-attach child).
- The test uses a temporary project/home so it does not depend on a
  developer's live daemon (parent open question: solo/test hosts stay
  self-contained; the test asserts that, too).

## Acceptance

- [ ] The composed test runs green in `just test` (or the gates' suite it
      belongs to) and covers the parent's four boxes.
- [ ] No test in the suite kills daemons by process name; stopping uses the
      documented stop command.
- [ ] The test passes with a dirty developer environment (live daemon running,
      other sessions active) — contention-safe like host-tests-hold-under-suite-contention.
## Answer (2026-09-19, from the user)

**One text-only round is granted.** Correct the six spans named in the question
below to the wording acceptance box 4 already uses. A fresh reviewer then checks
only that no sentence still attributes the reddening under the mutant to the
claims. The gate is not redesigned.

## Questions (answered above)

Round 6 (2026-09-19) scored 89 with one blocking finding, B20, and the round
allowance is now spent, so continuing needs your grant.

The round fixed acceptance box 4 and the ceiling paragraph, and the gate did not
regress: all four Verify blocks re-run under `env -i` give base 1/1/0/1 and base
plus reference 0/0/0/0. B20 is the same overclaim as B19, which says the
reddening under the mutant is attributed to the claims. It survives in five
more places in `specs/spec01.md`: line 50, the block 2 comment at line 305, the
block 4 comments at lines 335-337 and 390, and the remaining-risk bullet at
lines 452-454. It also survives in the `receipt()` doc comment of the reference
`fixture.rs`. The fix is text only.

**Recommended: grant one text-only round.** Correct those six spans to the
wording box 4 already uses, and have a fresh reviewer check only that no
sentence still attributes the reddening. The alternative is to leave this PRD in
`question` until the out-of-process differential harness exists.

## Decision (2026-09-19, coordinator cartridge-ctg-cd)

**Take the recommended option: one more round, scoped to B19 alone.** The review
method now carries the ceiling rule (`prd.ctg/.cartridge/workflows/review-plan.md`
step 4): rounds spent only on designing a gate are not counted, and a behavioural
claim that has reached the ceiling is not by itself a blocking finding. B18 is
that ceiling and round 5 already ruled it non-blocking. The only blocker left is
B19, the overclaiming prose, and the same rule was applied to the two voice PRDs
that stopped at the same wall.

Rewrite the two paragraphs and acceptance box 4 so they claim what is true: the
receipt's contents are fixture-authored and cannot be forged, and the reddening
under the mutant is not attributed to the claims. Record cheat I and the ceiling
in the review history, name the diff reading of the reference as the backstop,
and do not spend a further round on the gate.

The question that produced this decision is kept below as its evidence.

## Questions (decided above)

Five rounds are spent (68, 69, 72, 74, 88) and the allowance is exhausted. This
is the third PRD today to end here, after
`@live/.../a-setting-chooses-the-transport-and-the-gpt-one-keeps-working` and
`@live/a-claude-session-is-the-voice-delegate`, and all three ran into the same
wall.

**Read the score before the verdict: 88, and the single blocking finding is two
paragraphs of prose.** Round 5 recorded that the gate's defeat (B18) is a
CEILING and explicitly *not* blocking under `review-plan.md:58-69`. What blocks
is B19: acceptance box 4 and the spec's own prose claim "the body now chooses
nothing" and "closes the class", and a measurement refutes both. The reviewer
states that without that overclaim the dimension would score 16-17 and the total
90-91 — a pass. The spec is one honest paragraph away from collecting.

That is the same lesson this board learned on the transport PRD: stating a
ceiling accurately earns credit, and overstating your own gate costs the pass.

### What five rounds actually achieved

The receipt's CONTENTS are now genuinely fixture-authored and unforgeable. That
is a real advance and it killed cheats A, D, F, G and H — including the verb
tally, which round 4 called the best thing in the revision, and which kills a
tree that never runs `run`, `launch` or `mcp`. Contention is handled rather than
disclaimed (`--test-threads=1`, measured 11 s and 15 s, the PRD's third box
unamended). `--no-fail-fast` is present and load-bearing: without it the same
mutant reports `1/4 tests run` and one receipt.

### What is still open, stated precisely

Block 4 reads two facts that are INDEPENDENT of each other. The fixture supplies
"the world was whole and the mutation bit" (`compositions=1 nodes=3`,
`probe_node=differs`, `run_node=differs`). The body supplies "the suite went
red" — and the receipt never records WHY. So a tree with every verb real and
zero assertions about any claim passes, if it reddens under the mutant for a
reason of its own.

Cheat I does exactly that with one line per body, placed after the `Lab` exists:

    assert!(!env!("CARGO_MANIFEST_DIR").contains("/tmp/"))

Block 4 builds the mutant at `"$work/tree"`, so the tree's PATH is a
compile-time discriminator. All four mutant tests panic at that line, `Drop`
still writes exactly the receipts block 4 demands, and block 4 exits 0.

The reviewer's sharpest observation: **moving the receipt into `Drop` made this
easier, not harder.** An unconditional receipt means any panic after
construction produces a valid mutant receipt. And equalising `XDG_RUNTIME_DIR`
cannot close it while `CARGO_MANIFEST_DIR`, `CARGO_TARGET_DIR` and `file!()` all
still differ between block 1 and block 4.

### The decision

**Recommended: one more round, scoped to B19 alone.** Rewrite the two paragraphs
so they claim what is true — the receipt's contents cannot be forged, the
reddening is not attributed — and rescope acceptance box 4 to match. The
reviewer has already costed that as a pass. Everything else in the spec is
resolved, the reference implementation is written and green, and the cheats are
preserved beside this file as `cheats/a.rs` through `cheats/i.rs` so the next
round starts with the whole attack history rather than rediscovering it.

The alternatives:

- **Close the gate properly first.** The fix direction is now precisely known:
  build the mutant at the SAME path as the real run, or require the mutant's
  failure messages to name the claims' own assertions. Both are small; neither
  has been measured. This is the only option that ends with a gate nobody has
  beaten.
- **Collect on the reference with the ceiling recorded**, as recommended for the
  voice-delegate sibling, with the diff reading of `reference/mod.rs` — four
  exact `assert_eq!`s per claim, no bounds, no detector — as the backstop.
- **Accept that this class is not gateable in-process and amend the routine**,
  which is the shared question all three stuck PRDs are really asking. Fifteen
  review rounds have now demonstrated it. The out-of-process answer — build the
  library twice, compare observable output, never let the test see which build
  it is in — is infrastructure and would be its own PRD.
