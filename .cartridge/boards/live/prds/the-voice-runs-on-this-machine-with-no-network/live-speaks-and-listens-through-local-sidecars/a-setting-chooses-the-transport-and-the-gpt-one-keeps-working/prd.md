---
state: "done"
origin: requested
priority: 95
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/lib.rs", "src/service.rs", "src/socket.rs", "src/transport.rs", "cartridge.json", "README.md", ".cartridge/help.md"]
commit: "6922a8f12d5732c74a47f18c15c30e1fbc132467"
---

# A setting chooses the transport, and the GPT one keeps working

## Outcome

`live` gains a `provider` setting. Today `start_voice` fetches a credential and
dials `socket::connect` at one call site; after this it asks a seam which
transport to build, and the GPT transport is one implementation of that seam,
behaving exactly as it does now.

Nothing else changes. `Service::event` keeps its arms, the record keeps its
shape, and with `provider: "gpt"` — the default — a conversation is
indistinguishable from today's. The second implementation is the next child's
work; this one only makes room for it, and proves that making room broke
nothing.

The seam is deliberately small: `send`, `audio`, `close`, `id`, and a
constructor taking the session configuration and an event callback. Those are
the only four things the service asks of a session today.

## Acceptance

- [x] `cartridge.json` declares `provider` with default `"gpt"` and a documented doc string.
- [x] `src/transport.rs` holds the seam as an enum, and `src/socket.rs` is one variant of it with its behaviour and its endpoint constant unchanged.
- [x] `src/service.rs` builds the transport through the seam: `socket::credential` is reached only on the GPT branch, and `socket::connect` is not named in `src/service.rs` at all.
- [x] Selecting an unknown provider fails the `voice` call with a message naming the setting and the values it accepts, rather than falling back silently.
- [x] The existing `mod tests` in `src/socket.rs`, `src/audio.rs` and `src/service.rs` — three, five and ten tests, eighteen in all — pass unchanged, and a new test asserts the seam returns the GPT variant for `"gpt"` and an error for anything unknown. (The counts written here at planning time were three, three and five; measured on 2026-09-17 against `ea3c16e`, `cargo test` prints `running 18 tests` and exits 0, from `src/audio.rs:331,338,344,363,388` and `src/service.rs:1303,1378,1416,1443,1452,1464,1497,1505,1517,1531`.)
- [x] `README.md` and `.cartridge/help.md` describe the setting and both values.

## Decision (2026-09-17, coordinator)

**Apply the round-5 remedy, and do not charge it against the allowance.**
`prd.ctg/.cartridge/workflows/review-plan.md` step 4 now states that rounds spent
only on designing a gate are not substantive revisions of the plan and are not
counted as rounds. The remedy this PRD is waiting on is exactly that kind of
round: slice the token test to the gating test's own region, from `fn <name>` to
the next `\n\t#[`, instead of grepping the whole file. It is four lines inside a
block that already exists, a reviewer has run it against five trees, it kills the
round-3, round-4 and round-5 cheats, and both honest trees stay green. Round 4
had pre-authorised the slice.

The plan itself was never in doubt: a `provider` setting defaulting to `"gpt"`, a
seam in `src/transport.rs` with the existing socket transport as one variant, and
`src/service.rs` reaching `socket::credential` only on the GPT branch. Four of
the five recorded scores are 89 or 90, and every failure was a gate failure
rather than a plan failure.

If the sliced gate is itself defeated, that is the ceiling: record it and the
defeated attempts in the review history, name the diff reading as the backstop,
and score the plan on its remaining dimensions. Do not spend further rounds on
the gate.

The question that produced this decision is kept below as its evidence.

## Questions (decided above)

Five review rounds are spent (79, 90, 89, 89, 90) and the allowance is
exhausted, so this needs your decision rather than another round.

**The plan itself is not in doubt.** Every round agreed on what the change
should be: a `provider` setting defaulting to `"gpt"`, a seam in
`src/transport.rs` with the existing socket transport as one variant, and
`src/service.rs` reaching `socket::credential` only on the GPT branch. Both
honest implementations built during review compile, pass 21 tests and pass all
four Verify blocks, so the work is well understood and reachable. What five
rounds could not settle is one thing: **a Verify block that a plausible
non-implementation cannot pass.**

The defect had five costumes, each smaller than the last, and each found by a
reviewer that built the cheat rather than arguing about it:

1. Round 1 — a grep for the setting passed a tree that never read it.
2. Round 2 — tighter greps passed a tree where the field was declared,
   `Provider::parse("gpt")` took a literal, and the identifier lived only in a
   comment.
3. Round 3 — a comment-stripping, brace-matching parser was beaten twice, once
   by discarding the parse result and once by a decoy function above the real
   one. The same parser also false-redded a correct tree over `"gpt".to_string()`
   and a rustfmt line wrap.
4. Round 4 — the executed test was beaten by keeping its name and swapping its
   body to test the wrong function. That body is *less* work than the honest
   one, so it is the likely accident rather than a contrived attack.
5. Round 5 — the four-substring condition guarding that test body is tested
   file-wide, and two of the four tokens (`.voice(` with six occurrences, and
   `expect_err`) are already in the untouched baseline. So it is really a
   two-token condition, neither token has to sit in the named test, and a test
   that never calls `voice` passes it while the unknown provider still dials.

**Round 5 left a verified remedy on the table.** Slice the token test to the
gating test's own region (`fn <name>` to the next `\n\t#[`) instead of grepping
the whole file — four lines inside a block that already exists. The reviewer ran
it: it kills the round-3, round-4 and round-5 cheats, and both honest trees stay
green. Round 4 had pre-authorised exactly this slice.

So the question is not what to write. It is what the rounds rule should do here.

### The decision

**Recommended: authorise one more round to apply that remedy.** The rule exists
to stop a plan churning, and this plan is not churning — each round closed its
predecessor's finding and found a strictly smaller one, and the remaining fix is
four lines that a reviewer has already run against five trees. Spending the plan
now would throw away five rounds of converged work over a gap that is understood
and measured.

The alternatives, honestly stated:

- **Collect it as it stands, with the ceiling documented.** The spec is candid
  about its limits — round 5 credited it for predicting its own bypasses in
  advance — and a diff reviewer is named as the backstop. The cost is real: a
  test written to pass rather than to prove would collect green, and this board
  has already had to untick one box that rested on exactly that.
- **Split the PRD.** Land the seam and the manifest setting, which nothing
  disputes, and make the unknown-provider refusal its own child with its own
  review budget. Slower, and it leaves Acceptance box 4 unowned in the interim.
- **Drop the gate and rely on review.** Cheapest, and the least defensible on a
  board whose whole discipline is that only observed evidence ticks a box.

### One finding worth keeping regardless of the answer

Block 2's failure message prints the exact tokens it found missing. A gate that
names what would satisfy it hands out its own bypass. Whatever is decided here,
that message should say a condition failed without enumerating the cure.
