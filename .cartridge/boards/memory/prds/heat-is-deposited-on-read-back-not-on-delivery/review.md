# @memory/heat-is-deposited-on-read-back-not-on-delivery review history

Plan: `@memory/heat-is-deposited-on-read-back-not-on-delivery`,
`prd.ctg/.cartridge/boards/memory/prds/heat-is-deposited-on-read-back-not-on-delivery/prd.md`.
Scope: one observable outcome — access heat is deposited when a reference is read
back, not when a query delivers it. Executable leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none. No prior review record existed.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-19

Presented revision: `memory.ctg` at source HEAD
`3432b13376017be921d745719e0626d6f0b5463c`, working tree clean. Spec `spec01.md`
as published by analyst-1; `prd.md` as amended by the coordinator's `## Decision`
section of the same date.

| Input | Content digest |
| --- | --- |
| Plan | `prds/heat-is-deposited-on-read-back-not-on-delivery/prd.md` — SHA-256 `a5d23346b3237e30ce477a23653276bd6127f75fc91748b55628bc6a4038c1a3` |
| Specs | `specs/spec01.md` — SHA-256 `4e5d79db47309bb3513aca89bcd1bf6196e5d4fbe0b65685a3a4782065e6eb9d` |
| Material contracts/dependencies | `memory.ctg@3432b13` (base); `@memory/a-retention-probe-measures-the-half-life-of-a-stored-fact-per-claim-kind` (`done`, its `.cartridge/tests/integration/bench/RESULTS.md` present); `memory.ctg/README.md`, `memory.ctg/.cartridge/help.md`, `memory.ctg/cartridge.json` (surface); `prd.ctg/.cartridge/templates/spec.md` (Verify engine facts) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 15 | The mechanism is the right one and is minimal: `stamp_access` is split so a delivered row keeps only its order stamp and counter, `stamp_read` carries the full deposit on its own cooldown window, and both share one `deposit_heat` tail that refuses to stamp `heat_updated_at` for a zero amount. −5: the spec reverses the PRD Outcome's `tool.memory` carve-off without flagging it, and drops the help-text deliverable entirely (blocking finding 1). |
| Ownership and reuse | 18 | One cartridge, no sibling reach. `commit_access_ids` and `commit_read_ids` share one `stamp_ids` walk, so the monotonic-`now` rule and the never-bump-the-epoch rule keep one owner. Each of the eleven added paths verified independently in the clone: `hot_functions_from_file!("src/retrieval/piece/src/lib.rs")` at `src/retrieval/src/lib.rs:31` does generate the binding from that file alone; both unit tests are `#[path]`-mounted and reach crate-private items; `query_by_id`/`query_by_ids` are the only servers of a fetch by reference. −2: `.cartridge/help.md` is a surface file this change is required to move and it is absent from the footprint (blocking finding 2). |
| Dependencies and implementable slices | 18 | The `needs` link is `done` and its artifact exists. The slice is one coherent change; the reference implementation compiles workspace-wide (13 files, +267/−22). −2: the `sh` block pins the literal base sha `3432b13…`, so its "moved off base text" test passes on any edit to `README.md` or `RESULTS.md` by any other change, and the spec omits the analyst's own caveat about a rewritten history. |
| Observable acceptance and baseline evidence | 16 | All three mutants reproduced by the reviewer at exactly the claimed exits and assertion strings; every `pass:` name confirmed as an executed `... ok` line; both counts exact (`105 passed; 0 failed; 6 ignored`, `10 passed; 0 failed; 100 filtered out`). −4: `a_replayed_read_cannot_pump_one_references_heat` is vacuously satisfiable and stayed green under mutant 2; box 3's `RESULTS.md` gate accepts any edit (a literal `# PLACEHOLDER` line passes it); `query_by_ids` receives the change but has no test. |
| Failure, recovery and compatibility | 18 | The enqueue is advisory — a daemon with no queue deposits nothing; `deposit_delivery_fraction` defaults to `0.0` and is the documented dial back toward delivery; a zero amount does not restart the decay clock, which would have been a silent heat gain; the two cooldown windows are separated with a stated reason. −2: with the carve-out dropped, the agent's primary surface (`tool.memory`) can never warm the bank at all — a retention regression carried by no test and no rollback note beyond the config field. |
| Reviewer total | 85 / 100 | Below the 90 threshold, and two blocking findings are unresolved. |

### What the reviewer executed

All probing in a throwaway `git clone --local` of `memory.ctg` at
`$TMPDIR/heat-review`, with a second clone at `$TMPDIR/heat-base` for the base
comparison. `CARGO_TARGET_DIR` always inside the clone. `memory.ctg` was read
only and is unchanged; no `prd` op was run, no box ticked, nothing committed.
The analyst's reference implementation was taken as a patch from its own probe
and applied to the reviewer's clone; it is evidence, not a patch to land.

**Mutants — all three reproduce exactly as the spec claims.**

| Mutant | Command | Exit | Observed |
| --- | --- | ---: | --- |
| `deposit_delivery_fraction` `0.0` → `1.0` | `cargo test -p retrieval-piece --lib` | 101 | `FAILED. 102 passed; 3 failed` — all three quoted assertions red: `delivery deposits nothing on the first row`, `the row that was shown but never read stays cold`, `delivery is the engine's own output and deposits no heat` |
| `stamp_read` tail → `deposit_heat(e, now, heat_cfg, 0.0)` | `cargo test -p retrieval-piece --lib` | 101 | `FAILED. 103 passed; 2 failed` — `the read reference earns the full access deposit` (`retrieval_score_test.rs:365`) and the bare delivery-cooldown guard (`:385`) |
| `task_commit_read(ids)` → `task_commit_access(ids)` in `server.rs:611` | `cargo test -p rpc --lib id_filter_tests` | 101 | `FAILED. 9 passed; 1 failed` — `the deposit rides the read-back task, not the delivery stamp / left: CommitAccess / right: CommitRead` |

**Does the gate select anything?** Yes. Every `pass:` name appeared as a literal
executed line. Block 1: all six, under
`retrieval_score::retrieval_score_tests::query_filter_tests::`, `105 passed; 0
failed; 6 ignored`. Block 2: both, under
`server::server_query_tests::id_filter_tests::`, `10 passed; 0 failed; 100
filtered out` — the filter `id_filter_tests` is a real module at
`server_query_test.rs:100` and both new names are inside it.

**The rpc filter is legitimate, and for a broader reason than the spec gives.**
The unfiltered `cargo test -p rpc --lib` on the patched tree passed 5/5 at `110
passed; 0 failed`, including
`server_admin_tests::readiness_tests::readiness_answers_while_a_write_holds_the_graph`.
The filter therefore hides no test the change breaks. The combined
`cargo test -p retrieval-piece -p rpc --lib` flaked once in four runs on the
patched tree — on
`server_mutate_tests::tests::tool_ingest_answers_the_sync_leg_with_a_document_and_balanced_counters`,
not the readiness test — and flaked once in six runs at **base**, on a third
test,
`server_query_tests::cold_tier_filter_tests::a_default_query_bounds_both_its_width_and_its_edges`.
The rpc crate has load-sensitive timing tests independently of this change. The
spec attributes the flake to one named test; the real condition is broader, which
strengthens rather than weakens the case for two narrow blocks.

**`CARTRIDGE_YOLO`.** `memory.ctg/cartridge.json` declares settings `dir, embed,
gnn, graph, heat, hygiene, ingest, ledger, owner, queue, reason, retrieval, tick,
watcher` — **no `yolo`** — and `rg CARTRIDGE_YOLO` over the repo returns no
match. The reviewer's session carries `CARTRIDGE_YOLO=1`. Both gate blocks and
all three mutants were run plain and again under `env -u CARTRIDGE_YOLO`; results
were byte-identical (`0`/`0` for the gate, `101`/`101`/`101` for the mutants, same
counts). No phantom failure and no false pass from this direction.

**Engine facts.** Blocks are `sh -eu -c` safe: no `${VAR:?}`, and
`${CARGO_TARGET_DIR:-$PWD/target/heat-read-back-verify}` is the unset-safe form —
confirmed by running every block with the variable unset. Paths are relative to
the repo root, no absolute `cd`, the target dir is pinned to a slug subdirectory
so pass 2 cannot overwrite the live `target/debug` dylib, and no block writes
inside the footprint. No inert guard: the doc gate uses
`if grep -qin ...; then exit 1; fi` and `if git show ... | diff -q ...; then exit
1; fi`, never `! grep` and never an `&&` chain. The doc gate's failure message
names the property, not the token that would satisfy it.

**Timings are optimistic but inside the limit.** On the reviewer's machine with a
cold target directory, block 1 took **45 s**, not the spec's 18.3 s; block 2 took
**14 s**, not 7.9 s. Both are separately limited at 120 s, so 37% of budget is the
worst observed. The figures should be corrected, but they do not threaten the
gate.

**Footprint and Acceptance.** The spec's thirteen paths are the PRD's thirteen,
written absolute (`/Users/feb/dev/cartridge/memory.ctg/...`) where the PRD is
repo-relative. The linked sibling `a-retention-probe-...` used the same absolute
form and collected, so this is precedent rather than defect, but the majority
convention on this board is relative. The spec's six acceptance boxes are a
superset of the PRD's four and each PRD box maps onto one: PRD 1 → spec 1, PRD 2
→ spec 2 (with spec 3 and 4 as refinements), PRD 3 → spec 6, PRD 4 → spec 5. Both
boxes the coordinator corrected are honoured in their corrected wording.

### Findings and concrete revisions

**BLOCKING 1 — the spec reverses the PRD Outcome's `tool.memory` carve-out and
never says so.** The PRD's Outcome reads: "The `tool.memory` `query` path keeps
depositing until the agent surface has a read-back of its own, and says so in its
help text." The spec's Mechanism item 6 states the opposite outcome for that
surface: the text-query path "keeps enqueuing `task_commit_access` unchanged —
the `tool.memory` `query` surface still stamps order and count, **and now
deposits no heat**." The task kind is unchanged but its meaning is not:
`task_commit_access` → `do_commit_access` → `commit_access_ids` → `stamp_access`
now deposits `deposit_access * deposit_delivery_fraction`, which is `0.0` by
default. The consequence is that the model's own surface can never warm the bank
at all, which is the exact condition the PRD's sentence exists to prevent. This
is not one of the two corrections the coordinator settled, it is not flagged as a
deviation, it was not raised as a QUESTION, and no acceptance box covers it in
either direction. A revision must either implement the carve-out — the delivery
amount has to become a property of the call site rather than of the one shared
config field, since the spec's own rule that "one kind must not carry two deposit
rules" forbids overloading `CommitAccess` — or record that the carve-out is
deliberately dropped, with the reason, and carry that back to the PRD Outcome so
the two documents agree. Either way it needs an acceptance box asserting what
`tool.memory` `query` does to heat.

**BLOCKING 2 — `.cartridge/help.md` is absent from the footprint, and it carries
the sentence the spec rewrites.** `memory.ctg/.cartridge/help.md` lines 7–9
mirror `README.md` lines 14–16, including the identical `context.memory` sentence
("Query previews are discarded; the compact exact-ID readback is the evidence.")
that the spec's Mechanism item 7 amends in `README.md` alone. The file is
hand-maintained, not generated — `README.md:28` links to it as the cartridge's
help page. The standing record rule is that a cartridge ships both a `README.md`
and a `.cartridge/help.md` and that a change to its behaviour or surface updates
both in the same change; this change alters the behaviour of the `memory`
service's `get` (it now deposits) and of `tool.memory` `query` (it now does not).
`.cartridge/help.md` is also the literal "help text" the PRD's Outcome names, so
finding 1 cannot be closed without it. The doc `sh` block inspects only
`heat.rs`, `README.md` and `RESULTS.md`, so the divergence would collect green. A
revision must add `.cartridge/help.md` to the footprint, state the edit in the
Mechanism, and extend the doc gate to it.

**Non-blocking 3 — one new test is vacuously satisfiable.**
`a_replayed_read_cannot_pump_one_references_heat` captures `let once = heat_of(&g,
"a")` and then asserts the second read leaves it equal. It never asserts that
`once` is non-zero, so a build in which `commit_read_ids` deposits nothing
satisfies it with `0.0 == 0.0`. Observed: under mutant 2 this test stayed green
while its two siblings went red. The property is covered elsewhere, so the suite
is not defeated, but one added line (`assert!(once > 0.0, ...)`) makes the test
mean what its name says.

**Non-blocking 4 — Acceptance box 3 has only a file-changed proxy.** The gate
requires `.cartridge/tests/integration/bench/RESULTS.md` to differ from its base
text and nothing more. In the reference implementation that check is satisfied by
a single inserted line, `# PLACEHOLDER retention rerun section`, which the
reviewer ran and watched exit 0. The spec discloses the ceiling honestly — the
probe needs a real embedder and cannot fit a 120 s block — so this is not a
concealed gap, and under the review method a recorded gate ceiling is not by
itself blocking. It is still weaker than it needs to be: requiring the file to
carry two dated tables, by property rather than by naming the text, would cost
one `grep` and would fail a placeholder. Combined with the hardcoded base sha
(finding 6), the box today asserts only that somebody touched the file.

**Non-blocking 5 — `query_by_ids` is changed but untested.** The batch path
receives the same `commit_read` call as `query_by_id`, and spec box 3 speaks of
"only the reference that resolved", which is the batch path's distinguishing
behaviour (a partial hit must enqueue the found ids and not the missing ones).
`a_read_by_id_enqueues_the_read_back_deposit` exercises the singular path only.

**Non-blocking 6 — the `sh` block pins a literal base sha.** `base=3432b13…`
makes the README/RESULTS check pass on any edit by any other change that lands
first, and the analyst's own caveat about a rewritten history is not carried into
the spec. Comparing against the lane's merge-base, or asserting a property of the
new content, is more durable.

**Non-blocking 7 — stated timings are 2.5× optimistic.** 18.3 s / 7.9 s claimed;
45 s / 14 s observed cold on the reviewer's machine. Still inside 120 s per block.

**Non-blocking 8 — the spec never states its box mapping.** Six spec boxes
against the PRD's four; the mapping is derivable and correct, but a collector has
to derive it.

Disposition: revise. The mechanism, the footprint widening and the gate are sound
and the mutants are real; the failure is that the spec does not implement the last
sentence of the PRD's Outcome and does not carry the cartridge's help page.

Validation: `git clone --local` of `memory.ctg@3432b13` to `$TMPDIR/heat-review`
and `$TMPDIR/heat-base`; the analyst's reference diff applied to the first only.
Gate: block 1 exit 0 (45 s cold), block 2 exit 0 (14 s), doc block exit 0.
Mutants: exit 101 / 101 / 101 as tabled. Unfiltered `cargo test -p rpc --lib` exit
0 five times (`110 passed`). Combined two-crate command: 1 failure in 4 on the
patched tree, 1 failure in 6 at base, different tests each time. Every command
repeated under `env -u CARTRIDGE_YOLO` with identical results.
`/Users/feb/dev/cartridge/memory.ctg` was not written to and its tree is clean.

Reviewer identity: independent fresh reviewer subagent, Claude Opus 5 (1M
context), session 18d6ba8cb545f358-2, 2026-09-19. Not the spec's author.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL — 85/100, below the 90 threshold, with two unresolved blocking
findings.
Unresolved blocking findings: (1) the spec reverses the PRD Outcome's
`tool.memory` `query` carve-out and drops its help-text clause, unflagged and
uncovered by any acceptance box; (2) `.cartridge/help.md` is missing from the
footprint though it carries the surface sentence the spec rewrites in `README.md`
and is the help text the PRD names.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision of `spec01.md` resolving findings 1 and 2, with
findings 3 and 5 folded in as two small test additions; then round 2.
