---
state: "open"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/live.ctg"
needs: ["voice-runs-headless-on-the-microphone"]
footprint: ["src/**", "mcp/**", ".cartridge/**", "cartridge.json", "init.lua"]
---

# A Claude session is the voice delegate

## Outcome

GPT Live and a Claude Code session work as one coworker in one conversation.
GPT Live hears and speaks; when it delegates, the task goes to an attached
Claude session instead of `agent.ctg`, carrying the transcript that led to it.
The Claude session answers a task, or speaks up on its own (a PRD finished, a
question), and GPT Live says it. With no Claude session attached, delegation
falls back to `agent.ctg` as today.

## Acceptance

- [ ] `live {op:"watch", conversation}` streams one line per delegated task (`task <id>: <user words> (live said: …)`) and marks the conversation as having an attached delegate while the stream is open.
- [x] `live {op:"reply", conversation, text, task?, quiet?}` sends `session.commentary.append` (or `thinking` when quiet) tied to the task, or unprompted when `task` is absent; the task is recorded done with that text.
- [ ] Delegations arriving with no watcher attached run on `agent.ctg` exactly as before; a watcher detaching mid-task hands pending tasks back to `agent.ctg`.
- [ ] A delegate that is still working does not lose its task: the hand-back fires on a watcher that has actually gone, not on one that is merely slow, and a task handed back cannot then be completed twice. (Added 2026-09-17 on review round 2, finding F6: the lease sweeper introduces a renewal obligation of about fifteen seconds, and without this the user can receive two answers — one from `agent.ctg` after the hand-back and one from the delegate whose `reply` still completes the task.)
- [ ] `tool.live` exposes `watch`/`reply`; an offline test runs a mock voice session, a watcher, and a reply end to end. (Reworded 2026-09-17: the box named `live-mcp`, which does not exist — `live.ctg/mcp/` is absent and the PRD's `live.ctg/mcp/**` footprint entry matches nothing. `.cartridge/memos/system/vision.md:135-138` calls `live-mcp` a dangling profile entry, and `@root/the-shared-record-describes-only-this-repository` records that the root profile no longer declares it either. `tool.live` is what actually exposes these ops today: `src/service.rs:926-932` routes any op to `call()`.)

## Premise drift corrected, and what is already done (2026-09-17, coordinator cartridge-24)

Most of this PRD has already landed. Boxes 2 and 3 are ticked and the analyst
confirmed the code backs them by reading it at `ea3c16e`: `watched()`
(`src/service.rs:682-688`) is consulted at `:368-372` and `:872-877`, so the
attachment already diverts delegations from `agent.ctg`, and a detaching watcher
already hands pending tasks back.

What is left is one gap and it is small. `watch` exists and works — it leases,
hands `delegated` tasks and marks them `handed` (`src/service.rs:691-730`) — but
its payload is `{id, delegation, prompt, created}` with **no line**
(`:709-714`). `spoken()` gathers the user's words only, on a hardcoded `"user"`
literal (`:433`), while the assistant's words are recorded (`:570-574`) and never
gathered per task. That is the whole of box 1.

Box 4's `live-mcp` was premise drift and is reworded above on evidence rather
than planned around. The footprint's `live.ctg/mcp/**` entry matches nothing and
should be read as dead.

### Box 3 unticked (2026-09-17, after review round 1)

Box 3 has two clauses and only the first is true, so the box is unticked until
both are.

**First clause holds.** Delegations arriving with no watcher attached still run
on `agent.ctg` exactly as before — `watched()` (`src/service.rs:682-688`) is
consulted at `:368-372` and `:872-877`, and the reviewer confirmed it against
the code.

**Second clause is not implemented.** "A watcher detaching mid-task hands
pending tasks back to `agent.ctg`" has nothing behind it: `hand_to_agent` has
exactly two call sites, `:376` and `:876`, both on first dispatch, and nothing
sweeps an expired lease. A lease is only ever read as a liveness test
(`:687`, `:809`). So a task moved to phase `handed` when a watcher took it
(`:708`) stays there forever once that watcher goes away — it is not returned to
`agent.ctg`, and no timer notices.

Box 2 was checked in the same round and is correctly ticked: `:733-764` and
`commentary()` `:982-993` back it fully.

## Answer (2026-09-19, from the user)

**One more round is granted.** Fix F23: a task delegated to a watcher but not
yet collected gets its own phase, the lease sweeper hands such tasks back to
`agent.ctg` when the watcher is gone, and one named test proves it. Fold in the
non-blocking findings F24 to F26.

## Questions (answered above)

Round 6 (2026-09-19) scored 82 with one blocking finding, F23, and the review
allowance is spent, so continuing needs your grant.

F23 is a plan gap, not a gate problem. When a watcher leaves, only the tasks it
had already collected are handed back to `agent.ctg`. A task that was delegated
to the watcher but not yet collected stays in phase `delegated` forever, and
once a watcher has collected one task that window is five minutes. Two probe
tests confirmed it. The fix is known: give such tasks their own phase, have the
lease sweeper hand them back too, and add one test.

The rest of the plan held. Base fails and the reference passes all three Verify
blocks, each well under 120 s. The three non-blocking findings are cheap: F24
names the wrong block in the spec, F25 is one overclaiming sentence in the
ceiling paragraph, and F26 notes that `watch` can take tasks already running on
`agent.ctg` or a pane.

**Recommended: grant one more round** that fixes F23 as above and folds in F24
to F26. The alternative is to leave this PRD in `question`.

## Decision (2026-09-17, coordinator)

**The ceiling is now recorded in the review method, and this PRD proceeds under
it.** `prd.ctg/.cartridge/workflows/review-plan.md` step 4 now states that a
behavioural claim rests on a named executed test and a reading of the diff; that
a Verify block can require a named test to exist, to be executed and to turn red
on a mutated tree, but cannot establish that the test died of the behaviour
rather than of something the test itself supplied; that at most one round is
spent designing such a gate; and that rounds spent only on the gate are not
substantive revisions and are not counted against the five-round allowance. A
behavioural claim that has reached this ceiling is no longer a blocking finding.

This is the first of the three alternatives the analyst offered, and it was
chosen because ten review rounds across two PRDs in this cartridge reached the
same obstacle by five different routes. The out-of-process differential harness
remains a real and correct idea, but it is its own PRD and nothing on this board
depends on it today.

What this PRD must now do: finish box 1, which is the one genuine gap — `watch`
hands a payload of `{id, delegation, prompt, created}` with no line, and
`spoken()` gathers only the user's words on a hardcoded `"user"` literal while
the assistant's words are recorded and never gathered per task. The remaining
boxes land on the reference implementation the reviewers converged on. The
review history records the defeated gate attempts and names the diff reading as
the backstop.

The question that produced this decision is kept below as its evidence.

## Questions (decided above)

Five review rounds are spent (75, 82, 79, 78, 78) and the allowance is
exhausted, so this needs your decision rather than another round. This is the
**second** PRD in this cartridge to exhaust five rounds on the same obstacle,
after `@live/.../a-setting-chooses-the-transport-and-the-gpt-one-keeps-working`.

**The work is understood and it is correct.** Reviewers built a reference
implementation independently in rounds 2, 3, 4 and 5; the last one runs 24 green
tests, clippy clean. Round 5 confirmed by execution that box 3's second clause is
real in the design (a detaching watcher's task reaches `unassigned` through the
one agent-hand-off line) and that box 5's promise holds when the poll sequence is
actually run. What could not be settled is narrower and stranger: **no Verify
block anyone could write proves that the test which passes is the test that
matters.**

### What was tried, in order, and how each was beaten

1. Greps for the production shape — passed a tree that declared the field and
   never read it.
2. A named executed test — passed a tree that kept the name and swapped the body.
3. A required phrase, counted once in the test's own region — beaten by
   `format!("… (live said{} {})", ":", …)`, which keeps the runtime string while
   writing the literal once, and by moving the fixture to a `const` just outside
   the slice.
4. A mutant: copy the tree out, flip `"assistant"` to `"user"`, require the suite
   to go red. Beaten by `assert!(include_str!("service.rs").contains(…))` — a
   guard that reads the mutated copy at compile time and dies there, so the red
   arrives for a reason unrelated to the behaviour.
5. The mutant plus three more clauses: build the mutant first and require the
   build to succeed; require the *named* test to fail; ban the suite from reading
   its own source; and move the mutation off the call sites into the gathering.
   Beaten by `std::fs::read(file!())` with a `format!`-assembled needle — no
   banned spelling, a runtime read so the mutant still builds, and
   `--manifest-path` runs with cwd at the mutant's package root so `file!()`
   resolves to the mutated copy and the named test is exactly the one that dies.

The pattern is one sentence: **a Verify block can require a test to die, but not
to die of the behaviour.** A test can always supply its own red. Round 5
withdrew round 4's acceptance of the residual ceiling on exactly that ground —
the one property that had been genuinely proved by execution is faked by
`cheatO` too.

### The decision

**Recommended: collect it on the reference implementation, with the ceiling
recorded in the PRD.** The design is right, four independent reviewers built it
and agreed on what it does, and the two clauses this PRD exists to add — a
detaching watcher hands work back, and a working delegate neither loses its task
nor answers it twice — are implemented and observed. What is missing is a gate
that survives an adversary who is trying to defeat it, and the adversary here is
a reviewer instructed to defeat it, not an implementer doing the work. The diff
reviewer is the honest backstop, and the spec says so.

The alternatives:

- **Accept that this class of claim is not gateable and say so in the routine.**
  Two PRDs have now spent ten review rounds discovering the same thing. If that
  is the true answer, `review-plan.md` should say that a behavioural claim rests
  on a named executed test plus a reading of the diff, and stop spending rounds
  proving otherwise. This is the cheapest change and it would pay for itself
  immediately.
- **Build the gate out of process.** Everything beaten so far shares one flaw:
  the judge and the judged run in one process, so the judged can see the judge.
  A differential harness that builds the library twice and compares observable
  output — never letting the test see which build it is in — would close it. That
  is a real piece of infrastructure, its own PRD, and nothing on this board
  depends on it today.
- **Split the PRD** so the ungated clauses land separately. Slower, and it does
  not answer the question; the same obstacle reappears in each child.

### What is NOT in doubt, so a decision here is cheap

The reference is written and green. If you say collect, the implementation step
is short. If you say gate it out of process, this PRD waits on a new one. If you
say record the ceiling in the routine, I will open that PRD and this one
collects behind it.
