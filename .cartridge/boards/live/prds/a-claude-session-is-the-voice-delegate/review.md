# @live/a-claude-session-is-the-voice-delegate review history

Plan: `@live/a-claude-session-is-the-voice-delegate`, `prd.ctg/.cartridge/boards/live/prds/a-claude-session-is-the-voice-delegate/prd.md`.
Scope: one observable outcome — a Claude session takes voice delegations carrying the transcript; executable leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: `live.ctg` @ `ea3c16ea888bef0c946842749d1e333e355440aa`, working tree clean before and after this review (MEASURED, both ends). PRD includes the coordinator's "Premise drift corrected" section and the box-4 rewording.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `27df568fc83d78198fd8290cf208618a6d63980ce72aa55c91daf89420108907` |
| Specs | `specs/spec01.md` SHA-256 `28fa9741d17a540451c5a5577f53f2ceac7228ecedeb45ff1a1ff9ec1fd4d3a7` |
| Material contracts/dependencies | `live.ctg/src/service.rs` @ ea3c16e SHA-256 `1ee75d7fde68068f9aba5b51aa6468e8207e4e43af177249ba0bb866ae233bc5`; sibling history `boards/live/prds/the-voice-runs-on-this-machine-with-no-network/.../a-setting-chooses-the-transport-and-the-gpt-one-keeps-working/review.md` (F20/F22) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The remaining gap is correctly identified and not widened: `watch` (`src/service.rs:691-730`) returns `{id, delegation, prompt, created}` with no line (payload `:709-714`), and `spoken()` (`:416-441`) filters on a hardcoded `"user"` at `:433` while assistant fragments are recorded at `:570-574` and never gathered. All read and confirmed. −2: PRD box 1 has a second clause ("marks the conversation as having an attached delegate while the stream is open") that the spec never restates; it is already true (`:693-696`) but the spec's Acceptance does not say so. |
| Ownership and reuse | 19 | One file, one owner. Step 4 collapses the three duplicated `format!("task {}: {}")` sites (`:349`, `:855`, `:864`) onto the new `line()` instead of adding a fourth. `cartridge.json` untouched, so the cartridge is not untrusted (repo memory: *Editing a manifest untrusts its cartridge*). |
| Dependencies and implementable slices | 18 | Seven steps with exact anchors. I implemented steps 1–7 from the spec text alone into a scratch tree; it compiled, `20 passed; 0 failed`, `cargo clippy --all-targets -- -D warnings` exit 0. Every anchor the spec names matched. −2: step 3's rationale is wrong (see F3). |
| Observable acceptance and baseline evidence | 8 | The analyst's five-tree table reproduced exactly on my own trees and my own reference implementation. But a **cheat cheaper to write than the honest implementation passes both blocks with the whole outcome missing** — see F1, blocking. The gate's claimed division of labour is real for the two cheats that were built; it does not survive their combination. |
| Failure, recovery and compatibility | 12 | Hazard 1 (the gating test must stop its voice session) is real and I reproduced it. Timings are inside the 120 s engine limit. Guard-shape scan confirmed clean. −5: PRD box 3 is ticked on evidence that only supports half of it (F2, blocking). −3: hazard 2 is not a deadlock (F3). |
| Reviewer total | 75 / 100 | FAIL |

### Reproduced cheat table (my trees, my reference implementation)

Each tree a `git archive ea3c16e` copy under the reviewer's scratch; blocks
extracted from the spec by fence and run as `sh -eu -c "$(cat blockN.sh)"`, cwd
= each tree root; `CARGO_TARGET_DIR=/private/tmp/claude-501/rv-target`, outside
every repository. Every exit code MEASURED.

| Tree | b1 | b2 | note |
| --- | ---: | ---: | --- |
| `clean` — ea3c16e untouched | **1** | **1** | b1 names both misses; b2 `missing test: …a_watching_delegate_…` |
| `honest` — my own steps 1–7 | 0 | 0 | `20 passed; 0 failed`, clippy `-D warnings` exit 0 |
| `cheatA` — surface wired everywhere but `watch` | 0 | **1** | dies inside `cargo test`: the gating test's own assertion, plus collateral `left: ["speaker", "microphone", "speaker", "microphone"]` |
| `cheatB` — cheatA + name kept, body swapped | **1** | 0 | 20 green, clippy clean; b1 names **4** lost properties |
| `cheatC` — honest + body swapped | **1** | 0 | isolates the slice check; same 4 properties |
| `cheatD` — honest + body of five dead strings | 0 | 0 | the ceiling the analyst declares — **confirmed** |
| **`cheatE`** — cheatA production **+** cheatD body | **0** | **0** | **both blocks green, `watch` never returns a line, nothing is asserted** |

The analyst's table is accurate in every cell it reports, and the claim that the
two built cheats die in different blocks is confirmed. The claim that closes the
sibling's F22 is also confirmed by construction: block 1 slices `fn <name>` →
next `\n\t#[` and checks its five properties inside that region only (`honest` 0
misses, `cheatB`/`cheatC` 4 of 5), and every failure message names the missing
property, never the token that would satisfy it.

### Findings

**F1 (BLOCKING) — a cheat cheaper than the honest implementation passes both blocks.**
`cheatE` is `cheatA`'s production (the `"line"` field simply absent from
`watch`'s JSON — the entire PRD box 1 / spec Acceptance 1) with `cheatD`'s body
(five dead strings, no assertion). MEASURED: b1 exit 0, b2 exit 0, `20 passed`,
clippy clean. It is strictly cheaper to write than the honest tree: no
end-to-end test, no `Vec<Task>` rewrite of `watch`, no lease-then-transcript
ordering, no fixture wiring — four mechanical edits and a five-line test body.
That is the F20 shape, not a contrived one: the cheapest path to green delivers
nothing. The two layers do not compose; each cheat merely has to avoid the
*other* block's check, and one tree can avoid both.
Recommendation, both parts, in block 1:
(a) check in the **service region** that `watch`'s payload carries the line —
the token `"line": self.line(` — with a message naming the property ("`watch`
hands its caller no line"). This kills `cheatA`/`cheatE` structurally and the
honest tree satisfies it by construction.
(b) require the region's `(live said: I can do that)` and `["line"]` tokens to
occur inside an `assert` macro call, not anywhere in the body — the cheapest
regex being a scan of `assert` … `;` spans within the sliced region. This makes
the dead-string body cost more than the real one. Neither closes the ceiling
completely; together they stop the cheat that is currently cheapest.

**F2 (BLOCKING) — PRD box 3 is ticked on evidence for only half of it.**
The box reads: "Delegations arriving with no watcher attached run on `agent.ctg`
exactly as before; **a watcher detaching mid-task hands pending tasks back to
`agent.ctg`**." The first clause is backed: `watched()` (`:682-688`) is consulted
at `:368-372` and `:872-877` and `hand_to_agent` is called otherwise. The second
clause is not implemented. `hand_to_agent` has exactly two call sites, `:376`
(dispatch) and `:876` (delegate), both reached only when a task is first
dispatched. A task already moved to `phase = "handed"` by `watch` (`:708`) has
no path back: nothing sweeps expired leases (`watchers` is read at `:683` and
`:804` only), so a delegate that dies after being handed a task strands it in
`handed` forever. Grep of every `phase =` assignment (`:351, :369, :377, :409,
:708, :747, :856, :865, :873, :892`) confirms no re-dispatch. Untick the box and
split the recovery clause into its own PRD, or reword it to what the code does
("a conversation whose lease has expired sends its **next** delegation to
`agent.ctg`") — which is true and testable. Box 2 (`reply`) **is** fully backed:
`:733-764` sets `completed`, stores `text`, and `speak()`/`commentary()`
(`:766-780`, `:982-993`) send `session.commentary.append`/`thinking` with
`delegation_id`; the unprompted path returns `{"sent"}` (`:743`, `:760-763`).

**F3 (non-blocking) — the "deadlock" hazard is not one.**
Spec step 3 says dropping the `tasks` guard before `line()` takes the store
guard "keeps the two locks from ever overlapping". The codebase already orders
these one way only — `delegated()` holds `tasks` and takes the store inside it
(`:628-643`), `reply()` does the same (`:743-749`), and `session_config()`
explicitly `drop(store)` before anything else (`:512-517`). There is no
store-then-tasks path anywhere, so calling `line()` inside `watch`'s existing
closure would deadlock nothing. The spec concedes this in its own last sentence,
so it is not misleading — but it is sold as a hazard the implementer must
respect, and an implementer who instead keeps the closure will be correct.
Reword it as what it actually is: a simplification that deletes the redundant
second lock pass (`:718-722`). Hazard 1 is real and I reproduced it: `cheatA`'s
run failed `voice_runs_a_session_on_the_wire_…` with exactly
`left: ["speaker", "microphone", "speaker", "microphone"]` when the gating test
aborted before its `voice(…, Some(false))`.

**F4 (non-blocking, resolved) — the box-4 rewording was the right call.**
MEASURED: `live.ctg/mcp` does not exist, the PRD's `mcp/**` footprint entry
matches nothing, and `.cartridge/memos/system/vision.md:135-136` records
`live-mcp` as a profile entry naming a directory that does not exist. `tool.live`
is the MCP surface and `tool_call`'s fallback (`:926-932`) already routes
`watch`/`reply` to `call()`. Rewording rather than raising a QUESTION did not
change intent: box 4's intent is "the tool surface offers these ops and an
offline test proves them end to end", and that intent survives the rename intact.
Note the wording still promises more than the spec delivers on the enum: step 5
lists thirteen ops, which is what `call()` matches (`:122-163`) — correct.

**F5 (non-blocking, resolved) — guard-shape scan is clean.** MEASURED on the
two extracted blocks: the only `!` is `if ! cargo test …`, a real condition
inside an `if`; no statement-level `! grep`; no `grep 'a\|b'` alternation; no
`test -n … && test … -ge …`; no `cd`; scratch files `$$`-suffixed under
`$TMPDIR` with `trap … EXIT`; `CARGO_TARGET_DIR` exported with a `${…:-…}`
default in every cargo block. The analyst's report of this scan is accurate.

Disposition: revise. The slice is right, one file, and its reference
implementation builds from the spec text alone. Two things must change before
implementation: the block-1 additions of F1, and the PRD box-3 correction of F2.

Validation: cwd = each scratch tree under
`/private/tmp/claude-501/…/scratchpad/reviewer-voice-delegate/trees/<tree>`;
`sh -eu -c "$(cat block1.sh)"` and `sh -eu -c "$(cat block2.sh)"`, blocks
extracted from the spec by fence; `CARGO_TARGET_DIR=/private/tmp/claude-501/rv-target`
(outside every repository). Exit codes as tabled. `git -C live.ctg
status --porcelain` empty and HEAD `ea3c16e` before and after; no `prd`
command run, nothing committed, no file in `live.ctg` written.
Reviewer identity: reviewer-1 (Claude Opus 5, independent of the analyst).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: FAIL (75/100).
Unresolved blocking findings: F1, F2.
Rounds used / remaining: 1 / 4.
Next action: bounded revision — add F1's two block-1 checks (re-measure `cheatE`
after), and correct PRD box 3 per F2. F3's rewording is optional and cheap.

## Round 2 — 2026-09-17

Presented revision: `live.ctg` @ `ea3c16ea888bef0c946842749d1e333e355440aa`, working tree clean before and after this review (MEASURED, both ends). Spec revision 2, published in place. PRD now carries "Premise drift corrected" and "Box 3 unticked".

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `966cf9e9f9bec99928e48753217a0033f70dae47c8f1a5cdf0d6f731f664f205` |
| Specs | `specs/spec01.md` SHA-256 `cf5831d5f96afd394c2ef72b4098ebcc184172e6c064a144a6207323e906e527` |
| Material contracts/dependencies | `live.ctg/src/service.rs` @ ea3c16e SHA-256 `1ee75d7fde68068f9aba5b51aa6468e8207e4e43af177249ba0bb866ae233bc5`; round 1 of this file; `.state/loop/…/analyst-2.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Unchanged and still correct: the remaining gap is `watch`'s payload (`:709-714`) and `spoken()`'s hardcoded `"user"` (`:433`), both re-read. −2, carried from round 1: PRD box 1's second clause ("marks the conversation as having an attached delegate while the stream is open") is still absent from the spec's Acceptance, though it is already true at `:693-696`. |
| Ownership and reuse | 19 | One file, one owner, `cartridge.json` untouched. Step 4 still collapses the three `format!("task {}: {}")` sites onto `line()`. Step 5 reuses `dispatch` rather than adding a second hand-off path. |
| Dependencies and implementable slices | 19 | I built steps 1–9 from the spec text alone into a scratch tree: every anchor matched, it compiled, `21 passed; 0 failed`, `cargo clippy --all-targets -- -D warnings` exit 0, block 2 cold ≈ 30 s. F3's rationale is now accurate. −1: step 5 never states the renewal obligation it silently creates (F6). |
| Observable acceptance and baseline evidence | 10 | The analyst's seven-tree table reproduced **exactly**, cell for cell, on my own trees and my own reference implementation, and `cheatE` is genuinely dead. But F1 is **not** closed: `cheatF` (below) passes both blocks with the line fabricated from the wrong role and the entire hand-back absent, at a fraction of the honest cost. Blocking. |
| Failure, recovery and compatibility | 16 | F2 is closed and its gate verified sound on its own merits (below). F3's deletion is safe (verified). −2: the >15 s slow-delegate yank and the double-answer it permits are neither handled nor disclosed (F6). −2: one sweeper task is spawned per hand-over and none exits until the lease lapses (F7). |
| Reviewer total | 82 / 100 | FAIL |

### Reproduced table (my trees, my reference implementation, my cheats)

Each tree a `git archive ea3c16e` copy under the reviewer's scratch; blocks
extracted from the spec by fence and run as `sh -eu -c "$(cat blockN.sh)"`, cwd
= each tree root; shared `CARGO_TARGET_DIR=/private/tmp/claude-501/rv2-target`,
outside every repository. Every exit code MEASURED.

| Tree | production | gating test body | b1 | b2 |
| --- | --- | --- | ---: | ---: |
| `clean` — ea3c16e untouched | — | — | **1** | **1** |
| `honest` — my own steps 1–9 | wired | real | 0 | 0 |
| `cheatA` | `watch` unwired, no hand-back | real | **1** | **1** |
| `cheatB` | `watch` unwired, no hand-back | builds the line itself | **1** | 0 |
| `cheatC` | wired | builds the line itself | **1** | 0 |
| `cheatD` | wired (byte-identical to `honest`) | inert | 0 | 0 |
| `cheatE` — round 1's winner | `watch` unwired, no hand-back | inert | **1** | 0 |
| **`cheatF` — mine** | **`line()` wired but gathers the wrong role; no hand-back at all** | inert | **0** | **0** |

Every one of the analyst's seven rows is confirmed. `cheatE` now exits 1 at
block 1 on exactly `the watch operation does not put the line it hands over into
the payload it returns`; `cheatA` and `cheatB` die on the same line. `cheatA`'s
block 2 dies inside `cargo test` with `18 passed; 3 failed`, including the
collateral `voice_runs_a_session_on_the_wire_…`. `honest` is 21 green, clippy
clean, both blocks 0.

### Verdicts on round 1's findings

**F1 (BLOCKING) — partly closed, and still open.** The scoping fix works for
what it was aimed at: slicing `watch`'s own region out of the service half and
requiring `"line": self.line(` inside it kills `cheatE` structurally, and
remedy (b) — the balanced-paren assert extractor — forces the two load-bearing
tokens into an assertion. Both verified. **But the central argument does not
hold.** The analyst's defence of `cheatD` is that its service half is
byte-identical to the reference (I verified this myself: the text before
`mod tests` in my `cheatD` and my `honest` compares equal), so `cheatD` is not a
cheaper route than doing the work. That is true *of `cheatD`*, and it is true
only because the analyst built `cheatD` by copying the honest production
verbatim. The gate does not require that. It requires **two tokens**: that
`watch`'s region contains `"line": self.line(`, and that the service half
contains `(live said: `. Any production half that satisfies those two tokens
passes, byte-identical or not.

`cheatF` is such a tree, and it is far cheaper than honest. Its whole production
diff against `ea3c16e` is one six-line helper and one field:

```rust
fn line(&self, task: &Task) -> String {
    match self.spoken(task) {            // the existing user-only spoken()
        Some(said) => format!("task {}: {} (live said: {said})", task.id, task.prompt),
        None => format!("task {}: {}", task.id, task.prompt),
    }
}
```

plus `"line": self.line(task),` added to `watch`'s existing `json!`. No step 1
(no role parameter, so "what the voice had already said" is the **user's own
words repeated**), no step 4, no step 5 (**the entire hand-back, i.e. all of PRD
box 3's second clause and the spec's second Acceptance, is absent**), no step 6,
and no real test anywhere. MEASURED: b1 exit **0**, b2 exit **0**.

That it is behaviourally wrong is measured too, not argued. Running my honest
test bodies against `cheatF`'s production gives
`a_watching_delegate_is_handed_the_line_…` failing with the line it actually
produced:

```
task live-fixture:d1: count the files (live said: count the files)
```

and `a_watcher_that_detaches_hands_its_task_back_to_the_agent`,
`the_live_tool_offers_watch_and_reply` and `voice_runs_a_session_…` failing
alongside it — `17 passed; 4 failed`. So `cheatF` is a tree whose production
half is superficially right, quietly wrong on the one behaviour the PRD's box 1
exists for, missing box 3's second clause entirely, strictly cheaper to write
than the honest implementation, and green on both blocks. That is round 1's own
test of whether a hole matters, and this hole fails it.

What is needed is not a third structural layer but one more token pinned where
the wrongness lives: block 1 should require, inside `line()`'s own region (same
`region()` helper already in the block), that the assistant role is what is
gathered — e.g. the token `self.spoken(task, "assistant")` — and, inside the
service half, that a hand-back exists at all: a `phase == "handed"` filter that
assigns `"queued"`, and a call to it from `watch`'s region. Three property
checks in the block already written, no new machinery. That closes `cheatF`
without touching `cheatD`'s stated ceiling, which then really is the ceiling.

**F2 (CLOSED) — the hand-back is implemented in this slice and its gate is
sound.** Verified on its own merits, not on the analyst's word:

- `unassigned` is set on **exactly one line** of `src/service.rs` — `:377`
  (MEASURED: `grep -n unassigned` returns one hit), inside
  `if let Err(error) = self.hand_to_agent(&mut task).await`. Every other
  `phase =` assignment (`:351, :369, :377, :409, :708, :747, :856, :865, :873,
  :892`) writes some other phase. The phase's origin is unique, so the gate's
  assertion really does prove the agent hand-off was attempted and not merely
  that the task was requeued. My reference tree reaches it and the assertion
  passes.
- The lease poll cannot miss a renewal or a detach. `watched()` (`:682-688`) is
  a pure `lease > now()` read; `watchers` entries are only ever inserted
  (`:693`) and never removed, so "detach" is nothing but expiry, and a 250 ms
  poll sees an expiry within 250 ms. A renewal is a later `watch` writing
  `now + timeout + 15 s` before the sweep's next read, so an actively polling
  delegate can never be swept.
- The `handed` → `queued` flip does prevent double-dispatch. It happens inside
  one `self.tasks.lock()` borrow and the ids returned are only those the flip
  itself changed; a second sweeper on the same conversation re-reads under the
  same lock, finds nothing in `handed`, and collects an empty vector.
  `dispatch` additionally early-returns unless the phase is `queued` (`:344`),
  so even a duplicated id cannot dispatch twice.

**F3 (CLOSED) — the withdrawal is right and the deletion is safe.** The spec no
longer warns of a deadlock; it presents collecting `Vec<Task>` as a
simplification that deletes the second-lock save loop (`:718-722`). I verified
the deletion in my reference tree: the loop only re-locked `tasks` per id to
reach the record it had just mutated, the replacement saves the clone in the
same pass, the lock order stays `tasks` → `store` as everywhere else
(`:628-643`, `:743-749`, `:512-517`), and the suite is green. One narrow
semantic delta worth knowing but not worth blocking: the old loop saved whatever
the map held at save time, the new pass saves the clone, so a `reply` completing
that task in the microseconds between the flip and the save would be overwritten
in the store by a stale `handed`. The in-memory map stays correct and `reply`
saves its own record, so the window is a store-only regression on a task the
watcher was handed and answered within one pass. Not blocking; not worth code.

**F4, F5 (unchanged, resolved).** Re-scanned both extracted blocks myself: the
only `!` is `if ! cargo test …`, a real condition inside an `if`; no
statement-level `! grep`; no `grep 'a\|b'` alternation; no
`test -n … && test … -ge …`; no `cd`; scratch files `$$`-suffixed under
`$TMPDIR` with `trap … EXIT`; `CARGO_TARGET_DIR` exported with a `${…:-…}`
default. Block 1's failure messages name properties ("does not put the line it
hands over into the payload it returns", "never asks the service to watch"),
never the token that would satisfy them — checked line by line.

### New findings

**F6 (non-blocking) — the hand-back creates a renewal obligation the spec never
states, and a double-answer it does not guard.** A delegate is swept the moment
its lease lapses, and a lease is only `timeout_ms + 15 s`. A delegate that is
simply busy — answering a long task without re-issuing `watch` — loses that
task after ~15 s: it is flipped to `queued` and dispatched to `agent.ctg`, which
starts the same work a second time. When the delegate finally calls `reply` with
the id it was handed, `reply` (`:733-764`) completes it unconditionally, so the
user can get two answers, or the agent's answer after the delegate's. Nothing in
the spec says "a delegate must re-watch at least every 15 s or lose its work",
and nothing in `reply` notices the task is no longer `handed`. Cheapest fixes:
state the contract in the spec's Acceptance, and have the sweeper skip tasks a
`reply` has already completed (it does) while `reply` refuses a task whose phase
has moved on (it does not). Worth one sentence and one condition.

**F7 (non-blocking) — one sweeper per hand-over, none exiting early.**
`hand_back_when_the_lease_goes` is spawned from `watch` on every call that hands
tasks over, and each spawned task polls every 250 ms until the lease lapses.
A delegate that takes fifty tasks over a session leaves fifty sweepers awake for
the lifetime of the attachment, all of them contending on the `watchers` lock
four times a second, and all of them waking at once at the end. Correct, but
untidy; guarding the spawn on a per-conversation flag is a two-line change.

**F8 (resolved) — the disclosed cheat repairs are real and nothing is still
weakened by a construction artifact.** I built my own inert bodies without
seeing the analyst's: raw strings so every token appears verbatim in the source
(`r#"fixture.heard("session.commentary.append")"#`), all three census names
present, no unused const left behind in the unwired trees. My exit codes match
the published table in every cell, which is what a post-repair table should do.
The published table is accurate.

### Ruling on the open questions put to this review

- **Keeping the hand-back in this slice is right.** One function, one call site,
  one test, the same file the spec already owns, and the other half of the same
  PRD box is already in that seam. Splitting it would make a child re-derive the
  lease and `dispatch` facts for no gain. Keep steps 5 and 8 here; F6 is one
  sentence of Acceptance, not a second PRD.
- **The `cheatD` argument does not hold** as a general defence of the gate, only
  as a true statement about `cheatD`. See F1.

Disposition: revise. The slice, the anchors and the reference implementation are
good; F2 and F3 are properly closed. One bounded change is left: the three
property checks in F1.

Validation: cwd = each scratch tree under
`/private/tmp/claude-501/…/scratchpad/reviewer-voice-delegate-r2/trees/<tree>`;
`sh -eu -c "$(cat block1.sh)"` and `sh -eu -c "$(cat block2.sh)"`, blocks
extracted from the spec by fence; `CARGO_TARGET_DIR=/private/tmp/claude-501/rv2-target`
(outside every repository). Exit codes as tabled. `git -C live.ctg
status --porcelain` empty and HEAD `ea3c16e` before and after; no `prd` command
run, nothing committed, no file in `live.ctg` written.
Reviewer identity: reviewer-2 (Claude Opus 5, independent of the analyst and of round 1).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: FAIL (82/100).
Unresolved blocking findings: F1 (a cheaper-than-honest tree, `cheatF`, passes both blocks).
Rounds used / remaining: 2 / 3.
Next action: bounded revision — add F1's three property checks to block 1 (pin
the assistant role inside `line()`'s region, pin a `handed` → `queued` sweep in
the service half, pin its call inside `watch`'s region), then re-measure
`cheatD`, `cheatE` and `cheatF`. F6 and F7 are cheap and optional.

## Round 3 — 2026-09-17

Presented revision: `live.ctg` @ `ea3c16ea888bef0c946842749d1e333e355440aa`, working
tree clean before and after this review (MEASURED, both ends). Spec revision 3,
published in place. PRD now carries a fifth Acceptance box (added by the
coordinator on round 2's F6).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `d8efa367e81896cdcc588ba3ef17973fc21fdbc614b573ebddeab05cd9cf0795` |
| Specs | `specs/spec01.md` SHA-256 `d9d0b66542817e441fd3cd258e707602e3bf68f1a8f8305b0702aa863d606805` |
| Material contracts/dependencies | `live.ctg/src/service.rs` @ ea3c16e SHA-256 `1ee75d7fde68068f9aba5b51aa6468e8207e4e43af177249ba0bb866ae233bc5`; rounds 1 and 2 of this file; `.state/loop/…/analyst-3.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Unchanged and still correct; the gap is `watch`'s payload (`:709-714`) and `spoken()`'s hardcoded `"user"` (`:433`), both re-read at ea3c16e. −2, carried from rounds 1 and 2: PRD box 1's second clause ("marks the conversation as having an attached delegate while the stream is open") is still absent from the spec's Acceptance, though already true at `:693-696`. |
| Ownership and reuse | 19 | One file, one owner, `cartridge.json` untouched. Step 4 still collapses the three `format!("task {}: {}")` sites onto `line()`; step 5 reuses `dispatch` rather than adding a second hand-off; step 7 adds one field rather than a registry. |
| Dependencies and implementable slices | 18 | An independent reference implementation of steps 1–12, built from the spec text alone, compiled, `23 passed; 0 failed`, `cargo clippy --all-targets -- -D warnings` exit 0, b1 0 and b2 0. Every anchor the spec names matched the real file, including "thirteen ops" (`call()` matches exactly thirteen) and the unique `15000` literal. −2: two genuine forks the spec leaves open (F11). |
| Observable acceptance and baseline evidence | 9 | The service-side pins are a real advance — six of the seven bite, and `cheatA`/`cheatB`/`cheatE`/`cheatF` are dead where round 2 left them alive (reproduced). But the round's load-bearing new idea, the once-rule, is **broken twice by one-line string surgery** (F9, blocking), one of its seven pins is **vacuous against the untouched baseline** (F10), and it **reds a correct tree that asserts more strongly than the spec's own prescription** (F12). |
| Failure, recovery and compatibility | 15 | F7 is closed by step 7. The double-answer the user would hear is genuinely closed by the refusal in `reply`. −3: the fifth box's first clause is not met by the design it proposes (F13). −1: the renewal obligation never reaches the delegate that must obey it (F13). −1: `renew()`'s "existing lease" is ambiguous in a way that changes where the *next* delegation goes (F11). |
| Reviewer total | 79 / 100 | FAIL |

### Reproduced table (my trees, my reference implementation, my cheats)

Each tree a `git archive ea3c16e` copy under this reviewer's scratch; both blocks
extracted from the spec by fence and run as `sh -eu ../../blockN.sh`, cwd = each
tree root (`sh -eu <file>` is the engine's `sh -eu -c <text>` with the same
options; this host's safety net refuses the `-c "$(cat …)"` form).
`CARGO_TARGET_DIR` outside every repository: `/private/tmp/claude-501/rv3-target-honest`
for `honest`, `/private/tmp/claude-501/rv3-target-cheat` for the rest. Every exit
code MEASURED.

| Tree | what it is | b1 | b2 |
| --- | --- | ---: | ---: |
| `clean` | `ea3c16e` untouched | **1** (11 reasons) | **1** (`missing test: …a_watching_delegate_…`) |
| `honest` | my own steps 1–12 | 0 | 0 — `23 passed; 0 failed`, clippy clean |
| `cheatF` | round 2's winner: `line()` on the user-only `spoken(task)`, no role parameter, no hand-back | **1** | 0 |
| `cheatI` | round 3's own sharp cheat: every service pin satisfied, `line()` **discards** the assistant words | **1** (once-rule, sole reason) | 0 |
| **`cheatJ` — mine** | **`cheatI`'s production; the same fabricated fixture, built so the phrase is never written twice** | **0** | **0** — `23 passed`, clippy clean |
| **`cheatK` — mine** | **`cheatI`'s production; the fabricated fixture moved to a `const` one item above the test** | **0** | **0** |
| `honest-stronger` | `honest` plus one **stronger, correct** assertion: `assert_eq!(line, "task live-fixture:d1: count the files (live said: I can do that)")` | **1** | (not run) |

The analyst's rows I rebuilt all reproduce. `cheatF` exits 1 naming five
properties; `cheatI` exits 1 on the once-rule and **nothing else**, which is
exactly the analyst's claim and exactly the problem: one check carries that
tree's entire rejection.

### Verdicts on every earlier finding

**F1 (round 1, round 2 — BLOCKING, still open, new mechanism).** The
production half of F1 is now genuinely closed: pinning each token inside the
item that owes it kills `cheatE` and `cheatF` structurally, and I reproduced
both. The test half is not closed; it has been replaced by a counting rule that
does not hold. See F9.

**F2 (CLOSED, unchanged).** Re-confirmed by reading: `unassigned` is written on
exactly one line (`:377`), inside the `hand_to_agent` failure path, so the
`BACK_TEST` assertion still proves the work reached the agent hand-off. My
reference tree reaches it and the assertion passes.

**F3 (CLOSED).** The spec no longer claims a deadlock hazard. But the step that
replaced the warning introduces a real one it does not mention — see F11.

**F4, F5 (resolved, re-scanned).** Guard shapes clean, MEASURED on the two
extracted blocks: the only `!` outside Python source is `if ! cargo test …`, a
real condition inside an `if`; no statement-level `! grep`; no `grep 'a\|b'`
alternation; no `test -n … && test … -ge …`; no `cd`; scratch files `$$`-suffixed
under `$TMPDIR` with `trap … EXIT`; `CARGO_TARGET_DIR` exported with a `${…:-…}`
default. Block 1's messages name properties, not the tokens that satisfy them —
with one small exception, F14.

**F6 (addressed in design, not met — see F13).** The obligation is now
disclosed and `renew`/refusal are specified. The disclosure is honest and the
double-*speaking* is closed. The box the coordinator wrote is still not met.

**F7 (CLOSED).** Step 7's `sweeping: Mutex<HashSet<String>>` gives one sweeper
per conversation that exits when the lease goes. My reference implementation
built it and the suite is green.

**F8 (unchanged, resolved).** My cheat trees were built without reading the
analyst's, and the rows I rebuilt match the published table cell for cell.

### New findings

**F9 (BLOCKING) — the once-rule is a count, and a count is dodged by string
surgery. Two trees, both cheaper than honest, both green on both blocks.**

The rule is `line_body.count("(live said: ") > 1`. It measures how many times a
literal appears in a region — not where a value came from. Two independent
one-line dodges, both MEASURED at b1 exit 0 **and** b2 exit 0, `23 passed`,
clippy clean:

- **`cheatJ`** — the fixture is built with the colon as an argument, so the
  literal it produces at runtime is identical and the literal in the *source*
  is not:
  ```rust
  let fabricated = format!(
      "task live-fixture:d1: count the files (live said{} {})",
      ":", "I can do that)"
  );
  assert!(fabricated.contains("(live said: I can do that)"));
  ```
- **`cheatK`** — the fixture is moved one item up the module, outside the slice
  `region()` returns:
  ```rust
  const WANT: &str = "task live-fixture:d1: count the files (live said: I can do that)";
  ```
  and the test asserts `String::from(WANT).contains("(live said: I can do that)")`.
  `region()` starts at `fn <name>`, so anything defined above the test is
  invisible to the count. This is the region escape the round was supposed to
  have closed on the service side, reappearing on the suite side.

Both trees carry `cheatI`'s production — `let _ = self.spoken(task, "assistant");`
and then the user's own words formatted into `(live said: …)` — so the behaviour
PRD box 1 exists for is quietly wrong, box 5's refusal is entirely absent
(`reply` still completes any task unconditionally), step 4's pane line is
untouched and step 8's `op` enum is never written. Whole diff against `ea3c16e`:
100 changed lines, five inert test bodies included, no fixture wiring, no
end-to-end test, no correctness anywhere. That is round 1's own test of whether a
hole matters, and this hole fails it for the third round running.

The deeper point, and the reason a fourth text check will not settle this: *the
words the voice said must reach the test from the service* is the right
property, and it is not a textual property at all. Every text encoding of it is
a proxy that string surgery moves around.

**Recommendation — stop counting and execute a mutant.** The spec says a
mutation gate "cannot be written the obvious way" because it would edit
`src/service.rs` inside the footprint. It does not have to: copy the tree to
`$TMPDIR`, mutate the copy, and build the copy with `--manifest-path`. Nothing
inside the footprint is written and no `cd` is needed. In block 2, after the
real suite passes:

```sh
mutant="${TMPDIR:-/tmp}/live-mutant-$$"
rm -rf "$mutant"; mkdir -p "$mutant"
tar -cf - --exclude target . | tar -xf - -C "$mutant"
python3 - "$mutant/src/service.rs" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old, new = 'self.spoken(task, "assistant")', 'self.spoken(task, "user")'
assert s.count(old) == 1, "the mutation has nothing to change"
open(p, "w").write(s.replace(old, new))
PY
if cargo test --manifest-path "$mutant/Cargo.toml" --quiet >/dev/null 2>&1; then
	echo "the suite passes against a service that hands over the wrong words, so it is not reading what the service produced"
	exit 1
fi
```

One mutation, no counting, no false reds, and it is the property itself rather
than a proxy for it: `honest` and `honest-stronger` pass it, and every tree in
the table with an inert or self-asserting body — `cheatD`, `cheatH`, `cheatI`,
`cheatJ`, `cheatK` — fails it, because none of them observes the service at all.
A second mutation (`"handed"` → `"queued"` in the sweeper filter, or deleting
the refusal in `reply`) extends the same mechanism to the other two boxes for
three more lines each. Cost: one extra rebuild of the lib and its tests; four
different trees sharing one `CARGO_TARGET_DIR` each rebuilt in seconds here, and
block 2 currently runs in well under a tenth of the engine's 120 s. The
`rm -rf "$mutant"` belongs in the existing `trap … EXIT`.

**F10 (non-blocking) — one of the seven pins is vacuous.** The pin
`("fn reply", …, '"completed"')` is satisfied by the untouched baseline:
`ea3c16e`'s `reply` already contains `task.phase = "completed".into();` (`:747`).
MEASURED two ways — `cheatF`, which never touches `reply`, is not accused of it,
and `cheatJ`, which contains no refusal at all, passes block 1 outright. So the
"answered once" half of the new box has no service-side gate whatsoever; it
rests entirely on `ONCE_TEST`, whose own requirements (`"op": "reply"` anywhere
in the body, `is_err()` inside any assert) are met by
`assert!(Err::<(), String>(…).is_err())`. Pin the refusal itself — e.g.
`task.phase == "completed"` or the refusal's own message — not the phase string
the baseline already writes.

**F11 (non-blocking) — two implementer forks the spec leaves open, one of them
the very hazard step 3 replaced.**
- *Step 3.* "saving each task in the same pass" deadlocks if the implementer
  hoists the store guard out of the loop (`let store = self.store();` before the
  map), because `line()` → `spoken()` takes the same non-reentrant `std::sync::Mutex`
  again. Saving with a per-statement temporary guard is fine. Round 2 rightly
  made the spec withdraw a hazard that did not exist; the step that replaced it
  should name the one that does, in one clause.
- *Step 6.* "puts an **existing** lease out to `store::now() + LEASE_GRACE`" reads
  either as `get_mut` (my reading) or as `insert`. Under `insert`, every `reply`
  on a conversation nobody watches creates a 15 s phantom lease, and the *next*
  delegation is diverted away from `agent.ctg` — PRD box 3's first clause,
  silently broken by a plausible reading. One word ("without creating one") closes it.

**F12 (non-blocking, but the overcorrection this round was warned about) — the
once-rule reds a correct tree that asserts more than the spec asked for.**
MEASURED: `honest-stronger` is my passing reference plus one added assertion,

```rust
assert_eq!(line, "task live-fixture:d1: count the files (live said: I can do that)");
```

which is strictly stronger than the `contains` the spec prescribes and is read
entirely from the service's own output. Block 1 exits 1 and tells its author the
test "writes the voice's words into its own fixture as well as its assertion, so
it never has to receive them from the service" — the opposite of what that line
does. The spec's own prescribed test sits at exactly the count limit, so the gate
has zero slack above the text the analyst wrote: strengthening it is punished,
and the two ways to weaken it that I found are not. The sibling PRD's round 3
marked exactly this shape down as overcorrection, and the judgement holds here:
a gate whose first false red lands on the strongest honest test in the file is a
gate the next implementer deletes. F9's mutant has no such failure mode.

**F13 (BLOCKING) — the fifth box is not met by the design offered for it.** The
box reads: "the hand-back fires on a watcher that has actually gone, not on one
that is **merely slow**". The design's answer is "answering is the delegate
saying it is still there", and it is a good answer for the half it covers: the
user no longer hears two answers, because `reply` refuses a task already
`completed`/`cancelled` before it speaks, and whoever answers first wins. But a
delegate that is genuinely working and says nothing for fifteen seconds — a
Claude session in the middle of one long tool call, which is the normal shape of
delegated work — is *merely slow*, and it loses its task: swept to `queued`,
dispatched to `agent.ctg`, the work done twice, and its own `reply` refused when
it finally arrives. The analyst states this residual openly, to its credit, and
then lists the box as gated anyway. It is not: the design meets the second clause
and not the first.

It is worse than a wording gap, because nothing tells the delegate the contract
it must obey. `brief()` (`:1118-1126`) tells an agent to call `reply` when the
work is done and says nothing about fifteen seconds; `watch`'s payload carries
`{id, delegation, prompt, created, line}` and no deadline; `describe()`'s prose
(`:1094-1113`) mentions neither. A contract that exists only in a spec paragraph
cannot be obeyed by the process that has to obey it. Two cheap ways out, either
acceptable: (a) reword the PRD box to the promise the design actually makes — "a
delegate that says anything, including a quiet word, keeps its task; silence for
fifteen seconds is treated as gone" — and put that sentence where the delegate
reads it, in `brief()` or in what `watch` hands over; or (b) give a task that has
been *handed* its own grace, independent of the poll, so being slow and being
gone stop being the same observation. Until one of them is in the spec, ticking
box 5 would repeat round 1's F2 — a box ticked on evidence for half of it.

**F14 (non-blocking) — one failure message hands out a name.**
`f"src/service.rs: \`{head}\` is not in the service"` prints the exact signature
head to type (`fn hand_back_when_the_lease_goes`). The token pins behind it still
have to be satisfied, so it is not a bypass by itself, and the other messages are
property-shaped throughout. Worth naming the *behaviour* the missing item owes
instead.

**F15 (non-blocking, unmeasured) — `region()` takes the first match, so a decoy
can move a pin.** `region(service, "fn line")` is `text.find("fn line")`: a
function named `fn line_for_the_pane` defined above the real one would take the
pin with it, and the same holds for any head that is a prefix of another item's
name. No tree I built needs this, and F9's mutant makes it moot; noted so it is
not rediscovered. Anchoring the search on `\n\tfn line(` would close it.

Disposition: revise. The service-side half of the gate is now sound and the
reference implementation builds from the spec text alone, green and clippy-clean.
The remaining work is one replacement (F9's mutant for the once-rule, which also
retires F10's vacuous pin and F12's false red) and one decision on the fifth box
(F13). Both are small; neither is a new PRD.

Validation: cwd = each scratch tree under
`/private/tmp/claude-501/…/scratchpad/reviewer-voice-delegate-r3/trees/<tree>`;
`sh -eu ../../block1.sh` and `sh -eu ../../block2.sh`, blocks extracted from the
spec by fence; `CARGO_TARGET_DIR=/private/tmp/claude-501/rv3-target-honest` and
`…/rv3-target-cheat`, both outside every repository. Exit codes as tabled.
`git -C live.ctg status --porcelain` empty and HEAD `ea3c16e` before and after;
no `prd` command run, nothing committed, no file in `live.ctg` written.
Reviewer identity: reviewer-3 (Claude Opus 5, independent of the analyst and of
rounds 1 and 2).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: FAIL (79/100).
Unresolved blocking findings: F9 (`cheatJ` and `cheatK` pass both blocks, cheaper
than honest, with box 1 wrong and box 5 absent); F13 (the fifth box's first
clause is not met by the design offered for it).
Rounds used / remaining: 3 / 2.
Next action: bounded revision — replace the once-rule with F9's `$TMPDIR` mutant
run in block 2, pin the refusal itself rather than `"completed"` (F10), and
resolve box 5 by rewording it to what the design promises **and** putting that
promise where the delegate reads it (F13). F11, F12, F14 and F15 fall out of the
same edit or cost one clause each.

## Round 4 — 2026-09-17

Presented revision: `live.ctg` @ `ea3c16ea888bef0c946842749d1e333e355440aa`, working
tree clean before and after this review (MEASURED, both ends). Spec revision 4,
published in place. PRD unchanged since round 3 (five Acceptance boxes, box 3
unticked).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `d8efa367e81896cdcc588ba3ef17973fc21fdbc614b573ebddeab05cd9cf0795` (unchanged from round 3) |
| Specs | `specs/spec01.md` SHA-256 `c8673271a652ce3186772eba282bb087d8396d445f544b448b8a90ae7373cc5e` |
| Material contracts/dependencies | `live.ctg/src/service.rs` @ ea3c16e SHA-256 `1ee75d7fde68068f9aba5b51aa6468e8207e4e43af177249ba0bb866ae233bc5`; rounds 1–3 of this file; `.state/loop/…/analyst-4.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Unchanged and still correct. −2, carried from rounds 1–3: PRD box 1's second clause ("marks the conversation as having an attached delegate while the stream is open") is still absent from the spec's own Acceptance, though already true at `:693-696`. |
| Ownership and reuse | 19 | One file, one owner, `cartridge.json` untouched, no new crate. Step 4 still collapses the three `format!("task {}: {}")` sites onto `line()`; step 5 reuses `dispatch`; step 7 adds one field. −1: block 3 introduces a `tar`-copy-and-mutate pattern new to this repo — justified, but it is machinery the next spec will copy, and it is not yet sound (F16). |
| Dependencies and implementable slices | 17 | An independent reference built from the spec text alone compiled, `23 passed; 0 failed`, `cargo clippy --all-targets -- -D warnings` exit 0, blocks **0/0/0**. Every anchor named in the spec matched the real file. −3 for two implementer forks, one of them measured: step 10's prescribed wait is a red as written (F17), and F11's step-3 store-guard deadlock is still unnamed (F11 re-opened). |
| Observable acceptance and baseline evidence | 12 | The mutant is a real advance and it closes what round 3 raised: `cheatJ` and `cheatK` both die at block 3, `honest+` is **0/0/0** so the false red is gone (F12 closed), and `cheatL` — every step done, every pin satisfied, 23 green, clippy clean — is caught by block 3 and by nothing else. But block 3 asks only that *the suite fail*, never that it fail *because it observed the behaviour*: `cheatM` (below) beats it in three lines. −8, blocking (F16). |
| Failure, recovery and compatibility | 12 | F7 and F10 stay closed (F10 measured non-vacuous). The refusal in `reply` is real and `renew()`'s extend-only fix is real. −8, blocking: the fifth box's promise is **measurably false** under the calling pattern the service's own comment prescribes — one further `watch` poll cuts the `answer_by` it just handed the delegate from 300 000 ms to 15 000 ms (F18). And `answer_by`/`describe()`, the half of box 5 that "reaches the delegate", is pinned by nothing in any block and asserted by no test. |
| Reviewer total | 78 / 100 | FAIL |

### Reproduced table (my own trees, my own reference)

Eight trees, each a `git archive ea3c16e` copy under the reviewer's scratch, one
shared `CARGO_TARGET_DIR` outside every repository, all three blocks extracted
from the spec by fence and run as `sh -eu -c "$(cat blockN.sh)"` with cwd = the
tree. Every number measured. Nothing in `live.ctg` was written.

| Tree | what it is | b1 | b2 | b3 |
| --- | --- | ---: | ---: | ---: |
| `clean` | `ea3c16e` untouched | **1** | **1** | **1** |
| `honest` | my own reference, steps 1–12, 23 green, clippy clean | 0 | 0 | 0 |
| `honest+` | `honest` with `assert_eq!` on the whole line in place of `starts_with` | 0 | 0 | 0 |
| `cheatL` | every step, every pin, only `line()` discards the voice's words | 0 | 0 | **1** |
| `cheatJ` | round 3's cheat: expectation built by `format!` string surgery | 0 | 0 | **1** |
| `cheatK` | round 3's cheat: expectation hoisted to a `const` outside the region | 0 | 0 | **1** |
| `cheatM` | **`cheatL` plus three lines** — beats all three blocks | 0 | 0 | 0 |
| `probe` | `honest` plus one read-only assertion on the lease | — | — | — |

Agreements with the analyst's table: `clean` 1/1/1, `honest` 0/0/0, `honest+`
0/0/0, `cheatL` 0/0/1 — **block 3 is the only thing that catches `cheatL`, and it
earns its place on that evidence**. Block 3 costs 4 s, as claimed.

One correction: the analyst tables `cheatJ` and `cheatK` at b1 **1**. With the
once-rule withdrawn there is nothing in block 1 left for them to fail, and I
measure both at **0/0/1**. They are still caught — by block 3 alone, exactly as
`cheatL` is — so the conclusion stands and the discrepancy is cosmetic.

### F16 (BLOCKING) — the mutant is beaten in three lines, by `cheatM`

Block 3 runs the whole suite against the mutant and reads *any* non-zero exit as
proof. It never asks **why** the mutant failed, never requires the mutant to
**build**, and never names **which** test must go red. So a tree passes it by
noticing the mutation rather than by observing the behaviour.

`cheatM` is `cheatL` — `line()` calls `self.spoken(task, "assistant")` so every
block-1 pin is satisfied, then throws the answer away and repeats the user's
words back — plus this:

```rust
#[test]
fn the_voice_is_the_role_the_record_spells_assistant() {
	assert!(include_str!("service.rs").contains("self.spoken(task, \"assistant\")"));
}
```

MEASURED: `cheatM` is **0/0/0**. 24 tests green, `clippy -D warnings` exit 0, and
the user hears their own words read back to them as the voice's. `include_str!`
reads the *mutated* copy at compile time, the guard test fails there, block 3 sees
a red suite and reports success. An env- or path-sniffing test
(`env!("CARGO_MANIFEST_DIR").contains("live-delegate-mutant")`) does the same job
more crudely. `cheatM` costs three lines and looks, in review, like diligence.

The same call cannot distinguish a mutant that failed to compile from one whose
suite failed: `cargo test` returns non-zero either way and the `if` is false, so
the block exits 0. No tree of mine needed that route, but it is the same hole.

Two clauses close it, and they are cheap:

- Require the mutant to **build** first — `cargo build --tests --manifest-path "$mutant/Cargo.toml"` outside the `if`, so a mutant that does not compile is a red, not a pass.
- Require the **named** test to be the one that dies:
  `cargo test --manifest-path "$mutant/Cargo.toml" -- --exact service::tests::a_watching_delegate_is_handed_the_line_and_its_reply_reaches_the_voice_session` must fail, and the rest of the suite must still pass on the mutant. `cheatM`'s guard test is not that test, so its red no longer counts, and a tree must make the *behavioural* test observe the flip.

That second clause also removes the block's current indifference to a timing
flake or a panic in setup anywhere else in the suite.

### F18 (BLOCKING) — the fifth box's promise is false after one more `watch`

"Holding work is itself the evidence of working" is sound as a principle and the
right answer to F13. The implementation of it in this spec is not, and the defect
is the one the analyst just found in `renew()`, one function over.

`watch` sets `answer_by = store::now() + HELD_GRACE` when it hands work over
(step 6). But `watch`'s *top-of-function* `insert` at `:693-696` is left
unconditional — step 6 changes only the constant's name there
(`LEASE_GRACE` replaces the inline `15000`), not the assignment. That insert is
not extend-only. So the second `watch` call overwrites the five-minute
commitment with `now + timeout + LEASE_GRACE`.

MEASURED on my `honest` reference (`probe` tree, read-only assertion, no
behaviour changed):

```
promised answer_by 300000ms out; lease after the hand-over 300000ms;
after one more poll 15000ms
```

The delegate is handed `answer_by` 300 s out, polls `watch` once more — which is
precisely what the service's own comment at `:697-698` tells it to do, "the wait
is short and the caller loops", and what the spec's own step-9 test does eight
times — and its commitment is now 15 s (35 s at the default `timeout_ms`). A
five-minute tool call after that loses the task. **That is F13, unclosed, for
any delegate that keeps polling**, and it makes the `answer_by` the spec just
promised to hand the delegate a number that is no longer true.

One clause fixes it: `watch`'s lease insert extends only, the same
`(*lease).max(…)` the spec already prescribes for `renew()` — or the hand-over
sets the lease *after* the top-of-function insert, which it already does, and the
top-of-function insert stops shortening. Say which, in the spec, because the
current text is what an implementer will follow literally.

Two smaller things in the same area, both non-blocking. A holder that keeps
talking can extend past five minutes 15 s at a time (`max` reaches past the lease
once `now + LEASE_GRACE` exceeds it) — coherent, and worth one sentence in the
spec because it is not obvious. And `answer_by` and `describe()`'s explanation —
the "the delegate is told" clause, which is the half of F13 that round 3 said
reached nobody — are gated by **nothing**: no block-1 pin names `answer_by`, no
test asserts it, and block 3 does not touch it.

### F17 (non-blocking, measured) — step 10's test is a red as written

Step 10 says: wait "for the task's phase to stop being `handed`, and assert it is
**`unassigned`**". The sweeper sets `queued` under the `tasks` lock, releases it,
and only then awaits `dispatch`. A poller sampling at `until()`'s 10 ms
therefore observes `queued` first. MEASURED — my reference failed exactly this
way, `left: "queued" / right: "unassigned"` — and it is not a flake but the
common case. The predicate has to exclude `queued` (or wait for `unassigned`).
One clause. The assertion itself is right and `unassigned` remains the strong
proof the spec says it is.

Step 9 has a second, smaller fork: it prescribes pushing transcript deltas
without saying they need `event_id` and `start_ms`, which `event()` requires
(`:561-580`) — a delta without them is silently dropped and the line comes back
`task …: Voice request`. Measured; one clause.

### Verdicts on every earlier finding

| # | Verdict |
| --- | --- |
| F1 | **Closed.** Its production half closed in round 3; its test half is superseded by block 3, which kills `cheatA`/`B`/`E`/`F`/`G`/`H`/`I`/`J`/`K`/`L`. |
| F2 | Closed (round 1). Unchanged. |
| F3 | Closed (round 2). Unchanged. |
| F4 | Closed. The `tool.live` rewording stands; step 8 and the cheap tool test back it. |
| F5 | **Re-confirmed.** No statement-level `! grep`, no `grep 'a\|b'` alternation, no `test -n … && test …` AND-OR guard, no `cd`, `$$`-suffixed scratch with `trap … EXIT`, `CARGO_TARGET_DIR` exported in both cargo blocks and never `target/debug`. Block 3's mutant lives under `$TMPDIR`, writes nothing in the footprint, and needs no `cd` (`--manifest-path`). Failure messages are property-shaped prose; none prints the token it wants. |
| F6 | Superseded by F13 → now F18. |
| F7 | Closed. Step 7 stands. |
| F8 | Closed. |
| F9 | **Closed.** The count is withdrawn; `cheatJ` and `cheatK` both die at block 3. This is the round's real achievement. |
| F10 | **Closed, measured.** The pin is now `task.phase == "completed"`, a comparison the baseline does not contain — `clean` is accused of it ("a task that already carries an answer can be answered a second time"). |
| F11 | **Half open.** Step 6's fork is closed: the prescribed `(*lease).max(…)` cannot be written under an `insert`, so no phantom lease. Step 3's fork is **not** closed — the spec still never says that hoisting `let store = self.store()` out of the loop self-deadlocks through `line()` → `spoken()` on the same non-reentrant `Mutex`. The analyst reports both forks written in; only one is. Non-blocking (the implementer hits a hang at once), but the claim is wrong. |
| F12 | **Closed, measured.** `honest+`, my reference with `assert_eq!` on the whole line in place of `starts_with`, is **0/0/0**. Strengthening a correct test is no longer punished. The ceiling round 3 called unacceptable is gone. |
| F13 | **Not closed — see F18.** The design change is the right idea and it is a genuine improvement; the lease it promises is given back by the next `watch` call. |
| F14 | **Closed.** No failure message names a function; all are property-shaped. Verified against `clean`'s twelve-line output. |
| F15 | **Closed.** `regions()` anchors on `\n\t(?:pub )?(?:async )?fn <name>` followed by `(` or `<` and tests **every** match. A `line_of` decoy cannot take `line`'s pin. |

### The remaining ceiling — ruling

The analyst narrows honestly, and the narrowing is the right one: one mutation is
one property. Had block 3 been sound, that residue would be **acceptable for a
pass** — the hand-back's `unassigned` assertion is genuinely strong (one line in
the file sets it, in the agent hand-off failure path), and the refusal test is
observable. A second mutant would be a later improvement, not a condition of
collecting.

It is not acceptable as things stand, but the reason is not the ceiling. It is
that mutant #1 does not yet prove the one property it claims. **What is owed is
not a second mutant; it is two clauses on the first** (build the mutant, name the
test that must die). Add them and the single mutation carries its stated weight.

### New findings

- **F16 (BLOCKING)** — block 3 accepts any red on the mutant as proof. `cheatM`, `cheatL` plus a three-line `include_str!` guard, is **0/0/0** with the behaviour wrong. Require the mutant to build, and require the named behavioural test to be the one that fails.
- **F17 (non-blocking, measured)** — step 10's wait predicate observes `queued` and reds a correct tree; step 9 omits `event_id`/`start_ms` from the deltas it prescribes.
- **F18 (BLOCKING)** — `watch`'s top-of-function lease insert is not extend-only, so one further poll cuts the just-promised `answer_by` from 300 000 ms to 15 000 ms (measured). Box 5's first clause is unmet for a polling delegate, and the `answer_by` handed over is untrue. `answer_by` and its `describe()` explanation are gated by nothing.
- **F19 (non-blocking)** — block 1's `asserted()` returns each assert's whole balanced argument list, so the **failure message** counts as asserted text. `assert!(line.starts_with("task "), "wanted (live said: I can do that) in {line}")` satisfies the pin while asserting nothing about it; that is how `cheatL`/`J`/`K`/`M` pass block 1. Block 3 is meant to be the backstop for exactly this, which is why F16 matters as much as it does.

Disposition: FAIL, revise within the last round.
Validation: eight trees under
`/private/tmp/claude-501/…/scratchpad/reviewer-voice-delegate-r4/trees/<tree>`,
each `git archive ea3c16e`; blocks extracted from the spec by fence and run as
`sh -eu -c "$(cat blockN.sh)"` with cwd = the tree;
`CARGO_TARGET_DIR=…/reviewer-voice-delegate-r4/cargo-target`, outside every
repository. Exit codes as tabled. `git -C live.ctg status --porcelain` empty and
HEAD `ea3c16e` before and after; no `prd` command run, nothing committed, no file
in `live.ctg`, the PRD or the spec written by this review.
Reviewer identity: reviewer-4 (Claude Opus 5, independent of the analyst and of
rounds 1–3).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: FAIL (78/100).
Unresolved blocking findings: F16 (block 3 accepts any red on the mutant;
`cheatM` is 0/0/0 with the behaviour wrong); F18 (one further `watch` poll cuts
the promised `answer_by` from five minutes to fifteen seconds, so box 5's first
clause is still unmet).
Rounds used / remaining: 4 / 1.
Next action: one bounded revision, three clauses and a sentence — make block 3
build the mutant and name the test that must die (F16); make `watch`'s lease
insert extend-only and gate `answer_by` with a pin or a test (F18); fix step 10's
wait predicate and step 9's delta fields (F17); name step 3's store-guard
deadlock (F11). If the fifth round does not land these, the PRD goes to
`question` — which, as the sibling PRD shows, is a better outcome than collecting
a spec whose strongest gate is beaten in three lines.

## Round 5 — 2026-09-17 — FINAL ROUND (allowance exhausted)

Presented revision: `live.ctg` @ `ea3c16ea888bef0c946842749d1e333e355440aa`,
working tree clean before and after this review (MEASURED, both ends). Spec
revision 5, published in place. PRD unchanged since round 3 (five Acceptance
boxes; box 3 unticked, box 5 added after round 2).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `d8efa367e81896cdcc588ba3ef17973fc21fdbc614b573ebddeab05cd9cf0795` (unchanged since round 3) |
| Specs | `specs/spec01.md` SHA-256 `975f94f07fed128b48cc0d388c521ca9a6d42361bdb87343e66a4f7752922b1a` |
| Material contracts/dependencies | `live.ctg/src/service.rs` @ ea3c16e SHA-256 `1ee75d7fde68068f9aba5b51aa6468e8207e4e43af177249ba0bb866ae233bc5`; rounds 1–4 of this file; `.state/loop/…/analyst-1.md`…`analyst-5.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Unchanged and still correct: one observable outcome, one owner, the box-4 rewording still right. −2 carried from rounds 1–4: PRD box 1's second clause ("marks the conversation as having an attached delegate while the stream is open") is still absent from the spec's own Acceptance, though true in code at `:693-696`. |
| Ownership and reuse | 19 | One file, `cartridge.json` untouched, no new crate, `line()` still collapses the three `format!("task {}: {}")` sites, step 5 still reuses `dispatch`, step 7 adds one field. −1: block 3's `tar`-copy-and-mutate machinery is now three rounds old and still does not hold (F16); the next spec will copy it. |
| Dependencies and implementable slices | 18 | The reference built from the spec text compiles, **24 passed; 0 failed**, `cargo clippy --all-targets -- -D warnings` exit 0, blocks **0/0/0**; every anchor named in the spec matches the real file. F17 (wait predicate), F19 (`asserted()` keeps `assert_eq!`'s first two arguments) and F11 (step 3's store-guard deadlock now named) are closed and re-measured. −2: the spec says "steps 1–13" in two places but prescribes twelve (F21); and `the_promised_answer_by_survives_another_watch`, the only test that executes box 5's first clause, is prescribed nowhere in a numbered step and required nowhere in block 2 (this is the mechanism of F20). |
| Observable acceptance and baseline evidence | 11 | The mutant is stronger than round 4's — the mutation moved to the gathering, the mutant must build, the named test must be the one that dies, and the suite may not read its own source by four spellings. `cheatM1` and `cheatM2` both die, reproduced. But the ban is four spellings and the analyst's stated prediction — that a fifth route "would still have to beat both block 3 clauses" — is **measurably false**. `cheatO` (below) reads its own source at **run time**, beats the ban and beats both clauses, and is **0/0/0** with `line()` reading the user's own words back to them as the voice's. Third consecutive round in which the strongest block is beaten by a tree cheaper than honest. −9, BLOCKING (F16, still open). |
| Failure, recovery and compatibility | 12 | F18's *defect* is genuinely fixed: `lease()` owns both writes, `entry().or_insert()` then `.max(until)`, `answer_by` is the value `lease()` returned, and I ran the poll sequence myself — on the reference the promise holds. But the *gate* does not hold it: `cheatN2`, round 4's exact unconditional insert with the promise test deleted, is **0/0/0**, and its own poll sequence collapses the promised deadline by 285 000 ms (measured: `1789650665646 < 1789650950646`). Block 1 pins `.max(` inside `lease` — satisfied by a `lease()` used only at the hand-over — and pins nothing that makes `watch`'s entry write go through it; block 2's required-test list omits the only test that would notice. −8, BLOCKING (F20, new). |
| Reviewer total | **78 / 100** | **FAIL — allowance exhausted** |

### Reproduced table (my own trees, my own extraction, every exit code measured)

Eleven trees under `…/scratchpad/reviewer-voice-delegate-r5/trees/<tree>`; the
nine tabled by the analyst were re-run from **my** fence extraction of spec
revision 5 (`b1`/`b3` byte-identical to the analyst's), each with a
`CARGO_TARGET_DIR` outside every repository, cwd = the tree, `sh -eu -c "$(cat
bN.sh)"`. Nothing in `live.ctg` was written.

| Tree | what it is | b1 | b2 | b3 | analyst |
| --- | --- | ---: | ---: | ---: | --- |
| `clean` | `ea3c16e` untouched | **1** | **1** | **1** | agrees |
| `honest` | steps 1–12, 24 green, clippy clean | 0 | 0 | 0 | agrees |
| `honest+` | stronger `assert_eq!` on the whole line | 0 | 0 | 0 | agrees |
| `cheatJ` | round 3's `format!` string surgery | **1** | 0 | **1** | agrees |
| `cheatK` | round 3's `const` outside the region | **1** | 0 | **1** | agrees |
| `cheatL` | every step, every pin, only `line()` discards the voice's words | 0 | 0 | **1** | agrees |
| `cheatM1` | round 4's cheat: `include_str!` guard on the call site | **1** | 0 | **1** | agrees |
| `cheatM2` | the adaptive form: guard on the mutation site | **1** | 0 | **1** | agrees |
| `cheatN` | round 4's unconditional insert, promise test kept | **1** | **1** | 0 | agrees |
| **`cheatO`** | **mine: `cheatL` + a run-time source read (fifth route)** | **0** | **0** | **0** | not built |
| **`cheatN2`** | **mine: `cheatN`'s defect with the promise test deleted** | **0** | **0** | **0** | not built |

The analyst's nine rows reproduce **exactly**, including `cheatJ`/`cheatK` at
b1 **1** (round 4's correction applied to revision 4; revision 5's block 1 fails
them again, and the analyst's revision-5 table is the accurate one). `honest+` is
**0/0/0**: the false red of round 3 stays fixed, and this review does not give it
back.

### F16 (BLOCKING, still open after three attempts) — `cheatO`, a fifth source-reading route that beats both clauses

The ban is a list of four spellings. Reading the source needs none of them:

```rust
let own = String::from_utf8_lossy(&std::fs::read(file!()).expect("own source")).to_string();
let flipped = format!("role.{}(", String::from_utf8_lossy(&[114, 101, 112, 108, 97, 99, 101]));
assert!(!own.contains(&flipped), "the record is asked for the speaker the caller named: (live said: I can do that)");
```

`std::fs::read` is not `read_to_string`; `file!()` is not `CARGO_MANIFEST_DIR`.
Three lines inside the named test, on top of `cheatL` — so `line()` still calls
`self.spoken(task, "assistant")`, throws the answer away and formats the user's
own words as `(live said: …)`.

MEASURED, **0/0/0**. It beats every clause the analyst added, and it beats them
for the reason the clauses were supposed to make impossible:

- the **ban**: none of the four spellings appears;
- the **build** clause: the read is at run time, so the mutant compiles;
- the **named-test** clause: `cargo test --manifest-path` runs the binary with
  cwd = the *mutant's* package root, so `file!()` resolves to the **mutated**
  copy, the guard fires, and the named test is exactly the one that dies.

The analyst stated this ceiling and predicted the tree would still die at block
3. It does not. This is round 4's `cheatM` with a different spelling, and it
shows the shape of the defect is not the spelling: **block 3 asks only that the
named test go red, never that it go red because it observed the behaviour**, and
a suite that can see the mutation by any means at all can satisfy it. A ban by
enumeration cannot close that; `cheatO` is the second enumeration break in two
rounds. (The one part of round 4's recommendation that *would* have narrowed it —
"and the rest of the suite must still pass on the mutant" — was not implemented;
it would not have caught `cheatO` either, whose guard lives in the named test.)

What would close it, for the record: stop proving the property by *copying and
mutating the source* and prove it through the seam instead — a direct,
executed assertion that `spoken(task, "assistant")` returns the assistant's
words and `spoken(task, "user")` the user's, pinned in block 1 inside a named
test *and* required to be read by an assertion, so the observation is of a
returned value rather than of the file. A guard cannot fake a value it did not
compute.

### F20 (BLOCKING, new) — F18's defect is fixed in the code and ungated in the blocks

Verified, not taken on report. In the reference: `fn lease(&self, conversation,
until) -> i64` takes the lock once, `entry(..).or_insert(until)` then
`*held = (*held).max(until)`, returns `*held`; `watch`'s entry write is
`self.lease(conversation, now + timeout + LEASE_GRACE)`; the hand-over is
`let answer_by = self.lease(conversation, now + HELD_GRACE)` and that value —
not a second guess — is the `answer_by` in the payload; `renew()` is
`get_mut` + `.max(now + LEASE_GRACE)`. The entry poll cannot shorten a deadline,
and I ran the poll sequence: `watch` → `delegate` → `watch` (promise made) →
`watch` again, the lease still `>=` the promise. Box 5's first clause is real in
the reference.

It is not real in what the blocks *require*. `cheatN2` is the reference with two
edits — `watch`'s entry write reverted to the unconditional
`watchers.lock().insert(...)` of round 4, and
`the_promised_answer_by_survives_another_watch` deleted — and it is **0/0/0**.
Restoring only that test to `cheatN2` and running it gives the collapse in real
numbers:

```
a further poll does not shorten what was promised: 1789650665646 < 1789650950646
```

285 seconds of the promised five minutes, gone on the poll the tool's own
description tells the delegate to make. That is round 4's blocking finding,
verbatim, passing all three blocks.

The mechanism is two gaps that meet: block 1's `.max(` pin is scoped to the
`lease` region, and a `lease()` that is called only at the hand-over satisfies it
while `watch`'s entry write bypasses it; and block 2's required-test list — 23
names — does not contain `the_promised_answer_by_survives_another_watch`, which
is named only inside step 6's prose. A pin inside `watch` for `self.lease(` and
that one name in block 2's list would have closed it; neither is there.

### Verdict on every earlier finding

| # | Round | Verdict at round 5 |
| --- | --- | --- |
| F1 | R1 | Superseded by F9/F16; the production half stays closed. |
| F2 | R1 | CLOSED. Box 3's second clause is owned by the spec and works in the reference (see the box ruling below). |
| F3 | R1 | CLOSED. |
| F4 | R1 | CLOSED; the `tool.live` rewording remains right. |
| F5 | R1 | CLOSED, re-scanned this round: no statement-level `! grep` (block 2's and block 3's `!` are both `if !`), no `grep 'a\|b'` alternation, no `test -n && -ge` AND-OR guard, no `cd`, `CARGO_TARGET_DIR` defaulted away from `target/debug`, scratch `$$`-suffixed under `$TMPDIR` with `trap … EXIT`, nothing written under the footprint. |
| F6 | R2 | CLOSED in the code (renewal + refusal), and folded into F13/F18; its gate is now F20. |
| F7 | R2 | CLOSED. `sweeping: Mutex<HashSet<String>>`, one sweeper per conversation, removed before dispatch. |
| F8 | R2 | CLOSED. |
| F9 | R3 | CLOSED. The once-rule is gone; `cheatJ`/`cheatK` die and `honest+` does not. |
| F10 | R3 | CLOSED. The `reply` pin is `task.phase == "completed"`, non-vacuous (`clean` fails block 1 on it). |
| F11 | R3 | CLOSED. Step 3 names the store-guard deadlock explicitly. |
| F12 | R3 | CLOSED and re-measured: `honest+` **0/0/0**. This is the one gain that has held from round 3 to round 5. |
| F13 | R3 | CLOSED in the code by `HELD_GRACE` + `answer_by` + the `describe()` text; its gate is F20. |
| F14 | R3 | CLOSED; block 1's messages name behaviour, not signatures. |
| F15 | R3 | CLOSED; `regions()` is exact and checks every item of the name. |
| F16 | R4 | **OPEN, BLOCKING.** Beaten again, by `cheatO`. |
| F17 | R4 | CLOSED. The wait settles on `unassigned`/`delegated`; step 9 requires `event_id`/`start_ms`. |
| F18 | R4 | Code CLOSED, gate OPEN → **F20**. |
| F19 | R4 | CLOSED. `asserted()` keeps `assert!`'s first argument and `assert_eq!`'s first two. |
| F20 | R5 | **OPEN, BLOCKING** (above). |
| F21 | R5 | Non-blocking: the spec says "steps 1–13" while prescribing twelve. |
| F22 | R5 | Non-blocking: round 4's "the rest of the suite must still pass on the mutant" was not implemented. |

### The stated ceiling, ruled on

Round 4 accepted "one mutation is one property; the hand-back, the refusal and
the contract rest on named tests plus pins" as tolerable residue. **I do not
accept it now, because the gate has changed shape underneath it.** That ruling
was sound only while the one mutated property was genuinely proved by execution,
so that at least one part of the seam could not be faked. `cheatO` shows it is
not: the mutant proves nothing a determined suite cannot supply for itself, and
`cheatL`'s gutted stand-ins (four-line bodies that satisfy every block-1 pin)
show what the "named tests plus pins" residue is worth on its own. With the one
executed property removed, **every** acceptance box in this spec rests on pins
over text — and this review has now broken pins-over-text three times (`cheatK`,
`cheatM1`/`cheatM2`, `cheatO`).

### Boxes 3 and 5

- **Box 3, second clause (a watcher detaching mid-task hands pending tasks
  back): the spec makes the behaviour real, and does not make the proof real.**
  The design is right and reuses what exists: the sweeper polls the lease, flips
  `handed` → `queued` under one lock, and re-dispatches; offline the agent
  cannot answer, so the task lands in `unassigned`, a phase produced on exactly
  one line of the file. In the reference it is measured green. But the only
  thing gating it is the named test's existence plus two tokens, and `cheatL`
  passes block 1 and block 2 with that test reduced to
  `let phase = "unassigned"; assert_eq!(phase, "unassigned", …)`. **Real in the
  design, not owned by the gate.**
- **Box 5 (a working delegate does not lose its task; no task is answered
  twice): the second half is owned, the first half is not.** The double-answer
  refusal is pinned inside `reply` by a token the untouched baseline does not
  satisfy, and executed by a named test. The first half — "the hand-back fires
  on a watcher that has actually gone, not on one that is merely slow" — is
  correct in the reference and, per F20, **survives its own deliberate
  regression at 0/0/0**. That is the same clause the coordinator added after
  round 2 and the same one round 4 blocked on. **Not owned by the gate.**

Findings and concrete revisions: F16 and F20 above, each with the tree, the exit
codes and the measured numbers. F21 and F22 are one-line edits and are recorded
for whoever picks this up, not as conditions.
Disposition: keep the PRD and the spec; the specification of the *behaviour* is
good work and rounds 1–5 have driven the design to something correct in a
built, tested reference. What has never converged is the *gate*: a
copy-and-mutate proof over a suite that can read the copy. Send the PRD to
`question` and put the one question to the user: whether to collect this slice
on named-tests-plus-pins without a mutation gate, or to re-plan the proof around
executed seam values (F16's recommendation) under a fresh allowance.
Validation: eleven trees under
`/private/tmp/claude-501/…/scratchpad/reviewer-voice-delegate-r5/trees/<tree>`;
blocks extracted by fence from spec revision 5 (`b1`, `b3` byte-identical to the
analyst's); run as `sh -eu -c "$(cat bN.sh)"`, cwd = the tree, one
`CARGO_TARGET_DIR` per tree outside every repository. Exit codes as tabled;
`cheatN2` probe run as `cargo test -- --exact
service::tests::the_promised_answer_by_survives_another_watch`.
`git -C live.ctg status --porcelain` empty and HEAD `ea3c16e` before and after;
no `prd` command run, nothing committed, no file in `live.ctg`, the PRD or the
spec written by this review.
Reviewer identity: reviewer-5 (Claude Opus 5, independent of the analyst and of
rounds 1–4).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: **FAIL (78/100) — round 5 of 5, allowance EXHAUSTED.** Per the review
method's step 7 and its `Fails when` table, automatic revision of this plan
stops here.
Unresolved blocking findings: **F16** — block 3 accepts a named test that dies of
anything, and `cheatO` reads the mutant's own source at run time through no
banned spelling, 0/0/0 with the voice's words replaced by the user's; **F20** —
the F18 fix is real in the code and ungated in the blocks, and `cheatN2` restores
the 285 s collapse at 0/0/0.
Rounds used / remaining: **5 / 0**.
Next action: **stop.** Move the PRD to `question` with the two unresolved
findings and the disposition above; do not collect this spec, and do not open a
sixth round by renaming, splitting or copying the scope.

## Round 6 — 2026-09-19 — post-exhaustion review under the coordinator's Decision

Presented revision: spec revision 6 ("spec06"), published in place, against
`live.ctg` @ `6922a8f12d5732c74a47f18c15c30e1fbc132467` (working tree clean
before and after, MEASURED). PRD unchanged in its Acceptance boxes; now carries
`## Decision (2026-09-17, coordinator)`. Analyst report `analyst-6.md`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `85cf505e62232cf099186e2e0fa6e5dffc35132883f4e6a809515354b1f553f8` |
| Specs | `specs/spec01.md` SHA-256 `7fef0a34c09e4fb3307914d5d8544eddf2072ff043dfb56e8e91e86b226db7f5` |
| Material contracts/dependencies | base `src/service.rs` @ 6922a8f SHA-256 `fd3dc4d92f0dc0a4ed069207d91d332d8600cc63b428ba09280b45ab2fe3ddd8`; analyst reference `src/service.rs` SHA-256 `d64de6237bfdcc99eb4b9e8f384e970cd3128f69264ca17905a3c19afe785e8b`; `review-plan.md` step 4 (ceiling rule); `templates/spec.md` engine facts |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | One outcome, one owner, one file; box 1's second clause is finally its own Acceptance line. −3: F23 below. A user's request made while a departed delegate's lease is still held is never answered by anyone. With `HELD_GRACE` that window lasts five minutes after any hand-over. |
| Ownership and reuse | 19 | `line()` still replaces the three `format!` sites. The hand-back reuses `dispatch`. `lease()`/`renew()` are the only two writers. `cartridge.json` is untouched. −1 carried: the copy-and-mutate machinery in block 3 will be copied by later specs. |
| Dependencies and implementable slices | 18 | Twelve numbered steps, and the text says twelve (F21 closed). Every anchor I spot-checked matches `6922a8f`. The reference builds and passes **27 passed; 0 failed** with clippy clean, re-run by me. −2: F24 below. The F20 paragraph says which block catches a reverted entry write, and it names the wrong block. |
| Observable acceptance and baseline evidence | 17 | Under `env -i`, base fails all three blocks and the reference passes all three, each well inside 120 s (table below). The ceiling is applied as `review-plan.md` step 4 requires and is **not** counted as blocking. −2: the hand-back test covers only the `handed` path, so the gate stays green on a tree that strands pending tasks (F23). −1: F25, an overclaim in the ceiling paragraph. |
| Failure, recovery and compatibility | 11 | The lease/refusal design holds by execution. The promise survives a further poll. A second `reply` is refused. The sweeper sends a lapsed `handed` task to the single `unassigned` line. −9, BLOCKING: F23. Box 3 promises that pending tasks are handed back. Tasks the service routed to a watcher but that it had not yet collected are never handed back (measured). |
| Reviewer total | **82 / 100** | **FAIL** |

### Validation (my own clones, my own fence extraction, every exit code measured)

Clones: `git clone --local live.ctg` into
`…/scratchpad/reviewer-delegate-6/{base,ref,n3,n4,probe}`, all at `6922a8f`.
`ref` is `6922a8f` with the analyst's reference `src/service.rs` copied in.
`diff -rq` against the analyst tree is empty outside `.git`/`target`. I
extracted the three `sh` fences from the published spec. Each block ran as
`cd <tree> && env -i PATH="$PATH" HOME="$HOME" perl -e 'alarm 120; exec @ARGV' sh -eu -c "$(cat bN.sh)"`.
That gives no injected env, a hard 120 s alarm, and the blocks' own default
`CARGO_TARGET_DIR`, which starts cold. There is no `cd` in any block, and
nothing is written under `src/`.

| Tree | what it is | b1 | b2 | b3 | wall (s) |
| --- | --- | ---: | ---: | ---: | --- |
| `base` | `6922a8f` untouched | **1** | **1** | **1** | 0 / 8 / 0 |
| `ref` | analyst reference, 27 green, clippy clean | 0 | 0 | 0 | 0 / 8 / 2 |
| `n3` | ref with `watch`'s entry write reverted to the raw `insert`, promise test kept | **0** | **1** | 0 | — |
| `n4` | `n3` with the promise test's body gutted and its name kept | 0 | 0 | 0 | — |

Base failure messages: b1 lists 15 findings. b2 prints `missing test: …line_and_its_reply…`.
b3 prints `the record is never asked for one speaker's words…`. `n3`'s b2 failure is
`26 passed; 1 failed`, and the failing test is `the_promised_answer_by_survives_another_watch`.

### F23 (BLOCKING, PLAN, new) — tasks a watcher had not yet collected are never handed back

Box 3's second clause says that a watcher detaching mid-task hands **pending**
tasks back to `agent.ctg`. The sweeper only takes `phase == "handed"`. When
`dispatch` sees a live lease it routes the task to the watcher and sets it to
`"delegated"` with no target (ref `:384-387`). Nothing ever sweeps that phase.
The sweeper itself only starts from a `watch` that actually hands something
over. Two probes were added to the `probe` copy and run with
`cargo test probe_`:

- `probe_a_watcher_gone_before_its_next_poll`: watch, delegate, lease lapsed,
  wait 3 s → `left: "delegated"`, `right: "unassigned"`. **FAILED.** No sweeper
  ever starts. The task waits forever for a watcher that has gone.
- `probe_the_second_task_after_a_handover`: watch, delegate A, watch (A handed,
  so a sweeper is running), delegate B, lease lapsed, wait 3 s →
  `left: ("unassigned", "delegated")`. **FAILED.** A goes back and B is lost.
  This is the realistic case. The delegate took one task and its session then
  closed, so for the rest of `HELD_GRACE` (five minutes) every new request is
  routed to nobody and stays unanswered for good.

This is a behaviour gap in the plan, not a gate that is missing. The analyst's
table has no entry for it, so the GATE-ONLY/PLAN split does not mislabel it:
it is simply unfound. No round from R1 to R5 raised it. **Recommendation (one
step, small):** in `dispatch`'s watched branch, set a phase of its own
(`"awaiting"`) and call `hand_back_when_the_lease_goes` there too. `watch`
should collect `"awaiting"` instead of `"delegated"`. The sweeper should take
`"handed" || "awaiting"`. Add a test for the B scenario above. The same change
closes F26.

### F24 (non-blocking, accuracy) — the F20 paragraph names the wrong block

The spec says that reverting `watch`'s entry write to a raw `insert` "now fails
block 1 on the new pin before block 2 is even reached". That was measured false
(`n3`: b1 **0**). `watch` also calls `self.lease(` at the hand-over, and that
call alone satisfies the pin. What actually catches `n3` is block 2, through the
newly required `the_promised_answer_by_survives_another_watch` (b2 **1**). The
PLAN fix for F20 is therefore real: the test is now required, and a named
executed test is exactly what the ceiling rule asks for. `n4` (body gutted) is
0/0/0, which is the known ceiling class (swapped body) and so GATE-ONLY. The
sentence needs correcting, and the pin should be described as documentation,
not as proof.

### F25 (non-blocking, accuracy) — ceiling paragraph parenthetical

"whose words reach the line — that much **is** genuinely proved by execution"
restates what round 5 withdrew. `cheatO` shows that block 3's red can be
self-supplied, so block 3 proves this only for a suite whose diff has been read.
The sentence should say that. The rest of the ceiling paragraph is accurate. It
names all five defeated routes, it names the diff reading as the backstop, and
it does not claim that the hand-back, refusal or `answer_by` are proved beyond
their named executed tests.

### F26 (non-blocking, from reading the diff) — `"delegated"` is overloaded

`hand_to_agent` (ref `:425`) and the pane path (`:367`) both set `"delegated"`,
and `watch` collects every `"delegated"` task. A watcher that attaches later,
or a slow delegate coming back after its hand-back, is therefore handed work
that an agent run or a pane already owns. The `reply` refusal keeps this to a
single completion, so box 5 still holds, but the work is done twice.
F23's separate phase fixes this.

### Analyst classification, checked

F16 GATE-ONLY: correct. Round 5's seam-value suggestion is another gate design,
and the ceiling rule caps that work. F22 GATE-ONLY: correct. Round 5 measured it
would not catch `cheatO`. F20 PLAN: correctly classified and substantively
fixed, but the explanation is wrong (F24). F21 PLAN: fixed. Box 1's clause:
fixed. No PLAN finding was labelled GATE-ONLY. F23 is new and unclassified.

### PRD boxes against this revision

Box 1: covered. The line is built in `line()` and the lease marks attachment.
Box 2: already ticked. Box 3: first clause holds. Second clause holds only for
`handed` tasks, not for pending ones (**F23**). Box 4 (`tool.live`, offline
end-to-end): covered, with the `enum` and the loopback test green. Box 5: the
refusal and the non-shortening promise are proved by execution in `ref`. The
proof is the named executed tests plus my reading of the diff (ceiling).

Findings and concrete revisions: F23 is blocking and needs one small
implementation step plus a test. F24 and F25 are one-sentence text corrections.
F26 is folded into F23's fix.
Disposition: keep the PRD and the spec. Revise only the F23 step. Open no new
gate work.
Reviewer identity: reviewer-delegate-6 (independent review sub-agent, Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round. The coordinator's Decision
(2026-09-17) is the authority this round was run under.
Result: **FAIL (82/100)**. One blocking finding.
Unresolved blocking findings: **F23**. A task routed to a watcher that leaves
before collecting it is never handed back to `agent.ctg` (probes measured
`"delegated"` where `"unassigned"` was required).
Rounds used / remaining under the ceiling rule: rounds 1–5 each carried at least
one PLAN finding (F2, F6/F7, F11/F13, F18, F20), so the rule reclassifies none
of them as gate-only and all five still count. This round reviewed a
substantive revision: spec 6 adds a new Acceptance line, a new step and a new
required test. It therefore counts as **round 6 of an allowance of 5**, with
**0 remaining**. The Decision recorded the ceiling but granted no new
allowance.
Next action: **stop automatic revision.** The coordinator or user decides
whether to authorize the one-step F23 fix (the separate phase plus the sweeper
covering it, plus a test) with F24/F25's sentence corrections. If they
authorize it, a narrow re-review can check that one change. Do not collect
spec 6 as it stands.
