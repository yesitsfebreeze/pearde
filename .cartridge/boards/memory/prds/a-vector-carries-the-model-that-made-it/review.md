# @memory/a-vector-carries-the-model-that-made-it review history

Plan: `@memory/a-vector-carries-the-model-that-made-it`, `prd.ctg/.cartridge/boards/memory/prds/a-vector-carries-the-model-that-made-it/prd.md`.
Scope: leaf. One observable outcome — a withdrawn premise made durable as a standing regression lock over the per-store `EmbedStamp` guard that already exists. No code, no tests; grep-only Verify blocks.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
When copying this template, resolve that link relative to the actual owner board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: superproject `fd68eaefc03f5a9c92ffa8b8563889ebf877c8de` (dirty: `.cartridge/config.lua`, unrelated); `memory.ctg` at `3432b13376017be921d745719e0626d6f0b5463c`, `git status --porcelain` empty before and after review.

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-vector-carries-the-model-that-made-it/prd.md` — SHA-256 `2f917bd7b567b2cc5fe7e688d821abb89b7f5eaf3b11c2c61cd3557da6f4c794` |
| Specs | `specs/spec01.md` — SHA-256 `65edc572678e37fb9959592f816c64a2069addeb469854d0ff03d58b1406d4ed` |
| Material contracts/dependencies | `memory.ctg@3432b13`: `src/store/core/src/lib.rs`, `src/graph/src/persist.rs`, `src/health/src/lib.rs`, `src/commands/src/commands_check.rs`, `src/retrieval/piece/src/retrieval_query.rs`, `src/bootstrap/src/lib.rs`; engine facts from `prd.ctg/.cartridge/templates/spec.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The spec does one thing and refuses to do more: it converts a withdrawal into a lock, adds no code, no test, no `cargo`. The refusal to run `cargo` is correctly justified against the 120 s block limit and against hot-restarting the live cartridge (`[[verify-blocks-must-not-build-live-targets]]`). −2: the spec's own prose overclaims (see finding 4). |
| Ownership and reuse | 16 | Owner `memory.ctg` is correct; the spec reuses the five files the blocks actually read and correctly drops a sixth (finding 5). −4: the load path of the guard is genuinely split across a crate boundary the footprint does not cross, so the lock stops at the crate edge (finding 1). |
| Dependencies and implementable slices | 19 | `complexity: 1`, one spec, no dependency on any other PRD, no build step, satisfied by `3432b13` as it stands — the lane verifies green on an empty diff, and pass 2 in `repo` runs the identical read-only blocks. −1: "Files and steps" carries no step at all; that is honest for a lock, but the section then earns nothing. |
| Observable acceptance and baseline evidence | 13 | Five acceptance boxes, four of them genuinely gated; I proved 14 of 16 realistic mutations turn a block red (table below). −7: acceptance box 3 asserts "the stamp is still checked at graph open", and no block gates that — deleting the only caller leaves all four blocks green (finding 1); box 5's `continue;` half is near-inert (finding 2). |
| Failure, recovery and compatibility | 17 | Blocks write nothing, use no `cd`, no absolute path, no `../<sibling>.ctg`; every path is relative to the repo root, so both collect passes behave identically. No statement-level `! grep` anywhere — the one negation is `if ! awk … \| grep -q …; then exit 1; fi`, a real gate, proved firing. No BSD-inert `grep 'a\|b'` alternation. −3: the lock is blind to semantic no-ops (finding 3) and its anchors are pinned to literal tab indentation (finding 6). |
| Reviewer total | **83** / 100 | Below the 90 threshold, and one blocking finding is open. |

### Findings and concrete revisions

1. **BLOCKING — the open-time check is claimed but not locked.**
   `specs/spec01.md:46-48` states the stamp is checked "at open (`check_graph_stamp`, called from `src/bootstrap/src/lib.rs:83` — outside this footprint, so asserted only at its definition)", and acceptance box 3 (`specs/spec01.md:63-66`) asserts "The stamp is still checked at graph open". Verify block 2 only asserts that `pub fn check_graph_stamp` exists in `src/graph/src/persist.rs:96` and contains `check_stamp(`. `memory.ctg/src/bootstrap/src/lib.rs:83` (`graph::persist::check_graph_stamp(g);`) is the **sole** caller in the tree (`grep -rn check_graph_stamp src/` returns exactly two hits: the definition and this call). I deleted that line in a scratch copy: **all four blocks still exit 0**. The open-time half of the guard can be removed silently, and this spec's entire purpose is to make that impossible. I rule the analyst's own finding 1 **blocking**, not a documented limitation: a regression lock that concedes its central acceptance criterion is unenforced is not a lock.
   Remedy (do not apply from this review; the author applies it):
   - add `- "src/bootstrap/src/lib.rs"` to the `footprint:` list in `prd.ctg/.cartridge/boards/memory/prds/a-vector-carries-the-model-that-made-it/prd.md`;
   - add `- "src/bootstrap/src/lib.rs"` to the `footprint:` list in `prd.ctg/.cartridge/boards/memory/prds/a-vector-carries-the-model-that-made-it/specs/spec01.md`;
   - append to Verify block 2 (or add a fifth block):
     ```sh
     b=src/bootstrap/src/lib.rs
     awk '/^pub fn bind_embed_model\(/,/^}/' "$b" | grep -q 'graph::persist::check_graph_stamp(g);'
     ```
     I ran exactly that guard: exit 0 on the clean tree, exit 1 with `bootstrap/src/lib.rs:83` deleted;
   - drop the "so asserted only at its definition" parenthetical at `specs/spec01.md:47-48`, which then stops being true.

2. **Non-blocking — a decorative assertion in block 4.**
   `specs/spec01.md:174` asserts `printf '%s\n' "$c" | grep -q 'continue;'` inside `cold_candidates`. That function contains two `continue;` statements (`src/retrieval/piece/src/retrieval_query.rs:820` and `:825`), so the assertion is satisfied by the unrelated `valid_until` branch. I kept the superseded expression intact and replaced the branch body `continue;` with a `tracing::trace!` — all four blocks stayed green. The preceding assertion on the exclusion expression does fire (proved), so nothing is left unguarded in practice; the line only buys false confidence. Remedy: either delete it, or bind it to its branch, e.g. `printf '%s\n' "$c" | grep -A2 'entity.is_superseded()' | grep -q 'continue;'`.

3. **Non-blocking — a grep lock cannot see a semantic no-op.**
   Four mutations that keep every asserted string but destroy the behaviour left all four blocks green: an early `if true { return; }` in `check_stamp` (`src/graph/src/persist.rs:85`); the body of `check_graph_stamp` (`:96`) wrapped in `if false`; an early `return Ok(EmbedCheck::Match);` in `Store::check_embed_stamp` (`src/store/core/src/lib.rs:587`); and `pub fn embed_mismatch(&self)` (`src/store/core/src/lib.rs:645`) rewritten to `false`. This is the known ceiling of a text lock and the spec's no-`cargo` decision is still the right one at this complexity. Remedy: none required; record the ceiling in one line in the spec body so a later reader does not mistake the lock for a behavioural test.

4. **Non-blocking — the spec's evidence claim is wider than the evidence.**
   `specs/spec01.md:26-27`: "each block was proven to exit non-zero when the line it guards is deleted or weakened." Deletion holds (14/16 of my mutations). "Weakened" does not — see findings 1, 2 and 3. Remedy: narrow the sentence to "when the line it guards is deleted or renamed".

5. **Non-blocking — the dropped `base_types.rs` is CONFIRMED correct, with an asymmetry left behind.**
   The analyst's finding 2 holds. `grep -n 'EmbedStamp\|embed_mismatch\|embed_model' src/base/src/base_types.rs` returns nothing; `src/base/src/base_types.rs:328` (`pub struct Entity`) is cited by the PRD body only as the layout cost of the design that was *not* taken, and no Verify block reads the file. Dropping it from the spec footprint is right. Note for the record: `is_superseded` is defined at `src/base/src/base_types.rs:437` and the block-4 exclusion calls it, so rewriting that predicate to `false` would also escape the lock — the same ceiling as finding 3, on a predicate shared far too widely to lock here. The PRD footprint still lists the path while the spec's does not; a spec footprint narrower than its PRD's is legal and harmless here (no code is written), so no change is needed.

6. **Non-blocking — anchors pinned to hard-tab indentation.**
   `specs/spec01.md:88-90` uses `grep -q '^\tpub model: String,$'` (literal tabs, verified surviving the file round-trip). These are false-red risks, not false-green: a `rustfmt` change from `hard_tabs` to spaces would fail the block on unchanged behaviour. Acceptable as-is; remedy if desired is `grep -q '[[:space:]]pub model: String,$'`.

### Validation

All commands run with `cwd = /Users/feb/dev/cartridge/memory.ctg` (live-tree runs) or `cwd = <scratch>/mut` (mutation runs), blocks extracted verbatim from the four fenced ```sh regions of `specs/spec01.md` and executed as `sh -eu -c "<block>"` with empty stdin, exactly as `src/lifecycle.ts` collect/verify does. No `cargo` was run, so no `CARGO_TARGET_DIR` was needed and no live cartridge was restarted. All mutation work was done in `/private/tmp/claude-501/-Users-feb-dev-cartridge/546d3989-73ec-4315-89f3-a5bc45a8211e/scratchpad/reviewer-vector/mut`, a copy of six files; `memory.ctg` itself was never written. `git -C memory.ctg status --porcelain` is empty, before and after.

Live tree, `3432b13`, four blocks verbatim: **b1=0 b2=0 b3=0 b4=0**. Scratch copy baseline: **[0,0,0,0]**.

Mutation results (each anchor's match count asserted before and after the edit, per `[[verify-that-a-patch-anchor-matched]]`; every mutation reset to a fresh copy):

| Mutation | Block exits | Verdict |
| --- | --- | --- |
| `EmbedStamp` loses `pub dim: usize` | 1,0,0,0 | fires |
| mismatch path stops setting the durable flag | 1,0,0,0 | fires |
| unreadable stamp swallowed into "unstamped" (`map_err` → `or_else(Ok(None))`) | 1,0,0,0 | fires |
| warning no longer names `memory reembed` | 1,0,0,0 | fires |
| `EmbedRead::Unreadable` renamed away | 1,0,0,0 | fires |
| `flush_snapshot` stops checking (not in the analyst's table) | 0,1,0,0 | fires |
| `save_graph_into` stops checking | 0,1,0,0 | fires |
| `stamp_of` fakes the width (`dim: 0`) | 0,1,0,0 | fires |
| `snapshot_for_flush` carries `stamp: None` | 0,1,0,0 | fires |
| health hardcodes `embed_mismatch: false` | 0,0,1,0 | fires |
| `embed_mismatch` finding downgraded `error` → `warn` | 0,0,1,0 | fires |
| `embed_unreadable` finding gated off (`if false`) | 0,0,1,0 | fires |
| real ordering inversion: mismatch block moved above unreadable (not in the analyst's table) | 0,0,1,0 | fires |
| `cold_candidates` admits superseded rows | 0,0,0,1 | fires |
| a `vector_dim_mismatch` finding is reintroduced | 0,0,0,1 | fires |
| **`src/bootstrap/src/lib.rs:83` deleted — the only open-time caller** | 0,0,0,0 | **SURVIVES — finding 1** |
| superseded branch keeps its expression, drops its `continue;` | 0,0,0,0 | SURVIVES — finding 2 |
| `check_stamp` early-returns (call left as dead code) | 0,0,0,0 | SURVIVES — finding 3 |
| `check_graph_stamp` body wrapped in `if false` | 0,0,0,0 | SURVIVES — finding 3 |
| `Store::check_embed_stamp` early-returns `Ok(EmbedCheck::Match)` | 0,0,0,0 | SURVIVES — finding 3 |
| `embed_mismatch()` accessor returns `false` | 0,0,0,0 | SURVIVES — finding 3 |
| proposed remedy guard on `bind_embed_model` (clean / caller deleted) | 0 / 1 | remedy proved |

Analyst-report audit: every line number the analyst cites reproduced exactly — `store/core/src/lib.rs:312, 380, 587`, `graph/src/persist.rs:73, 85, 96`, `health/src/lib.rs:185-201`, `commands_check.rs:126-147`, `retrieval_query.rs:751`, `bootstrap/src/lib.rs:83`, `base_types.rs:328`. Twelve of the analyst's twenty claimed mutations were re-run independently and all twelve fired; their table is credible. Their removal of a `grep 'a\|b'` alternation guard is confirmed prudent — no `\|` appears in any published block. Their report's `Revision:` digest `2f917bd7…` is `prd.md`, not the spec; the published `spec01.md` digest is `65edc572…`.

Disposition: **revise** — one bounded edit (finding 1) plus three cheap prose/assertion cleanups (findings 2, 4, 6). The spec's shape, scope and grep-only decision are right and should be kept.
Reviewer identity: independent reviewer subagent `reviewer-vector` (Claude Opus 5, 1M context), round 1.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (83/100, below 90; one unresolved blocking finding).
Unresolved blocking findings: finding 1 — the sole open-time caller of `check_graph_stamp` (`memory.ctg/src/bootstrap/src/lib.rs:83`) is outside both footprints and is gated by no block; deleting it leaves all four Verify blocks green while acceptance box 3 claims otherwise.
Rounds used / remaining: 1 / 4.
Next action: add `src/bootstrap/src/lib.rs` to the PRD and spec footprints, add the proved `bind_embed_model` guard to block 2, drop the "asserted only at its definition" parenthetical, narrow the "deleted or weakened" claim, and either bind or delete the bare `continue;` assertion. Then present for round 2.

## Round 2 — 2026-09-17

Presented revision: superproject `fd68eaefc03f5a9c92ffa8b8563889ebf877c8de` (dirty: `.cartridge/config.lua`, `cartridge.ctg`, `mcp.ctg` — all unrelated); `memory.ctg` at `3432b13376017be921d745719e0626d6f0b5463c`, `git -C memory.ctg status --porcelain` **empty before and after this review**. The revised spec was published in place at `specs/spec01.md`; `prd.md` frontmatter also changed since round 1 (footprint gained `src/bootstrap/src/lib.rs`).

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-vector-carries-the-model-that-made-it/prd.md` — SHA-256 `d1555f2e5632361c04e833ecae527ded332f073a8c35befcb31851ddb10d65c0` (round 1 saw `2f917bd7…`) |
| Specs | `specs/spec01.md` — SHA-256 `f54c404fef7ed027f04b03bbae96e0be2dbe32d066051383dac04091c58f66f9` (round 1 saw `65edc572…`) |
| Material contracts/dependencies | `memory.ctg@3432b13`: `src/store/core/src/lib.rs`, `src/graph/src/persist.rs`, `src/bootstrap/src/lib.rs`, `src/health/src/lib.rs`, `src/commands/src/commands_check.rs`, `src/retrieval/piece/src/retrieval_query.rs`; engine facts from `prd.ctg/.cartridge/templates/spec.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Unchanged shape — a withdrawal turned into a standing lock, no code, no test, no `cargo`, correctly justified against the 120 s block limit and against hot-restarting the live cartridge. Round 1's −2 for overclaiming prose is recovered: `specs/spec01.md:20-24` now states exactly what a grep lock catches ("deletion, renaming, and a changed constant or severity") and exactly what it cannot ("a line that is still present and no longer reached"), and I confirmed both halves empirically. −1: `## Files and steps` still opens with a heading that has no step under it. |
| Ownership and reuse | 20 | Round 1's −4 is fully recovered. `src/bootstrap/src/lib.rs` is now in the PRD footprint (`prd.md:10`) **and** the spec footprint (`specs/spec01.md:6`), and the crate boundary the lock previously stopped at is crossed by real assertions. Owner `memory.ctg` correct; the six footprint files are exactly the six files the blocks read. |
| Dependencies and implementable slices | 19 | `complexity: 1`, one spec, no dependency on any other PRD, no build step; satisfied by `3432b13` as it stands, so the lane pass verifies green on an empty diff and pass 2 in `repo` runs the identical read-only blocks. Same −1 as round 1 for the empty steps section. |
| Observable acceptance and baseline evidence | 19 | All five acceptance boxes are now gated by a block that I proved fires. Box 3 — round 1's blocker — is gated four ways over (sole caller, three binder call sites, ordering). I ran 18 mutations this round; every intended-red one went red and every anchor was md5-verified applied. −1: the two new anchors are position-locked, so a behaviour-identical reorder goes red (NB-1, NB-2) — a false-red, never a false-green. |
| Failure, recovery and compatibility | 18 | Blocks write nothing (the only `>` characters in all four blocks are `->`/`=>` inside grep patterns — checked), use no `cd`, no absolute path, no `../<sibling>.ctg`, no `cargo`; every path is relative to the repo root, so both collect passes behave identically. **No statement-level `! grep` anywhere** — every negation is `if ! awk … \| grep -q …; then exit 1; fi`, a real gate, proved firing three times this round. **No `grep 'a\|b'` alternation** — zero `\|` in any block. −2: the tab-literal and positional anchors of finding 6 remain, and are now slightly wider (NB-1). |
| Reviewer total | **95** / 100 | At or above the 90 threshold, with no blocking finding open. |

### Verdict on each round-1 finding

1. **Finding 1 (BLOCKING) — CLOSED, and closed wider than the remedy offered.** The remedy I proposed in round 1 locked only the call inside `bind_embed_model`. The analyst refused it verbatim and was right to: `bind_embed_model` has exactly three callers, all in the same file, and a guard on the callee alone survives any one of them being dropped. I re-derived the caller set independently — `grep -rn 'bind_embed_model\|check_graph_stamp' memory.ctg/src` returns exactly seven lines: the three call sites (`:57`, `:71`, `:99`), the definition (`:81`), the sole `check_graph_stamp` call (`:83`), one tracing string, and the definition in `persist.rs:96`. Block 2 now asserts all five load-bearing ones plus the ordering. **Five worlds built in a scratch copy, each md5-verified applied, block 2 exit code in each:**

   | world | file:line mutated | block exits (1,2,3,4) |
   | --- | --- | ---: |
   | sole caller of `check_graph_stamp` deleted | `src/bootstrap/src/lib.rs:83` | 0, **1**, 0, 0 |
   | `load_graph` drops the binder | `src/bootstrap/src/lib.rs:57` | 0, **1**, 0, 0 (`load_graph does not bind the embedding model`) |
   | `try_load_graph` drops the binder | `src/bootstrap/src/lib.rs:71` | 0, **1**, 0, 0 (`try_load_graph does not bind the embedding model`) |
   | `reload_graph` drops the binder (hot-reload path) | `src/bootstrap/src/lib.rs:99` | 0, **1**, 0, 0 (`reload_graph does not bind the embedding model`) |
   | order inverted: check moved above `set_embed_model` | `src/bootstrap/src/lib.rs:82-83` | 0, **1**, 0, 0 |

   The ordering assertion is not decorative: I confirmed `stamp_of` (`src/graph/src/persist.rs:73`) returns `None` while the model is empty, so the inverted form is the silent no-op the spec says it is, and the `[ "$set_at" -lt "$chk_at" ]` test catches it. Acceptance box 3 (`specs/spec01.md:68-75`) now claims only what block 2 proves.

2. **Finding 2 (non-blocking, decorative `continue;`) — CLOSED.** I rebuilt round 1's exact gutted branch and three neighbours in a scratch copy. The new anchor pair at `specs/spec01.md:230-234` fires on all four:

   | mutation to `cold_candidates` (`src/retrieval/piece/src/retrieval_query.rs:751`) | block exits |
   | --- | ---: |
   | expression kept, branch body `continue;` (`:820`) → `tracing::trace!` — **round 1's exact leak** | 0, 0, 0, **1** |
   | disjunct (`:817`) demoted to a standalone `let _unused = …;` | 0, 0, 0, **1** |
   | disjunct deleted outright | 0, 0, 0, **1** |
   | `continue;` → `admitted += 1;` | 0, 0, 0, **1** |

   Round 1's leak is dead. The bare `grep -q 'continue;'` is gone from the published spec.

3. **Finding 3 (non-blocking, semantic no-ops) — CLOSED as disclosure, and the disclosure is accurate.** The new `## Risk` section (`specs/spec01.md:94-105`) names the ceiling and the four no-ops. I did not take the table on report: I rebuilt all four and confirmed each survives, with md5 before/after proving each edit landed — early `return` in `check_stamp` (`src/graph/src/persist.rs:85`) → `0,0,0,0`; `check_graph_stamp` (`:96`) body in `if false` → `0,0,0,0`; `check_embed_stamp` (`src/store/core/src/lib.rs:587`) short-circuited to `Ok(EmbedCheck::Match)` → `0,0,0,0`; `embed_mismatch()` (`src/store/core/src/lib.rs:645`) hardcoded `false` → `0,0,0,0`. The Risk text understates nothing and overstates nothing. Its stated reason for accepting the ceiling — closing it needs an executing test, a test is code, and this PRD is withdrawn precisely to add none — is the right call at `complexity: 1`. **The spec is now honest about what it does and does not catch.**

4. **Finding 4 (overbroad "deleted or weakened") — CLOSED.** The sentence is gone. `specs/spec01.md:20-24` replaces it with a claim I verified true in both directions.

5. **Finding 5 (dropped `base_types.rs`) — no change required, still correct.** The spec footprint (six paths) remains a strict subset of the PRD footprint (seven, including `src/base/src/base_types.rs`). No block reads `base_types.rs`; the PRD cites `:328` only as the layout cost of the design not taken. Legal and harmless — no code is written.

6. **Finding 6 (tab-literal anchors) — OPEN, non-blocking, marginally wider.** See NB-1/NB-2.

### New findings, round 2

- **NB-1 (non-blocking) — block 4's anchor is position-locked, not just indentation-locked.** `specs/spec01.md:232-234` uses `grep -A3 '<disjunct>' | tail -1` to require `continue;` exactly three lines on. I reordered the three disjuncts of the `if` at `src/retrieval/piece/src/retrieval_query.rs:816-818` — a behaviour-identical edit — and block 4 exited **1**. This is a false-red, never a false-green, so it cannot let a regression through; it can only fail a collect on an innocent reformat. Remedy if wanted: replace the `-A3 | tail -1` pair with an `awk '/<disjunct>/,/^\t\t}/'` range asserted to contain `^\t\t\tcontinue;$`, which is order-tolerant. Acceptable as published.
- **NB-2 (non-blocking) — block 2's binder loop greps a literal argument list.** `specs/spec01.md:206` requires `bind_embed_model(&mut g, cfg);`. Renaming the local binding `g` or the parameter `cfg` is behaviour-identical and turns block 2 red. Same class as NB-1 and round-1 finding 6. Remedy if wanted: `grep -q 'bind_embed_model('`, which still catches the dropped call and survives a rename.
- **NB-3 (non-blocking) — the Acceptance boxes still read as behavioural.** Box 2 (`specs/spec01.md:63-67`) says "A changed model **still raises** the durable `embed_mismatch` flag"; the block proves only that the line raising it is present in the function that must hold it. `## Risk` covers this for a reader who reaches it. Remedy if wanted: one clause under `## Acceptance` — "each box below is asserted textually; see **Risk** for the ceiling."
- **The analyst's disclosed `open_graph` error is CONFIRMED absent from the published spec.** `grep -rn open_graph memory.ctg/src` returns nothing, and `grep -c open_graph` over all four extracted blocks returns `0 0 0 0`. I went further and checked **every** function/type name any block names against the file that block names: all 16 anchors (`EmbedStamp`, `EmbedRead`, `set_embed_stamp`, `check_embed_stamp`, `stamp_of`, `check_stamp`, `check_graph_stamp`, `save_graph_into`, `flush_guarded`, `flush_snapshot`, `snapshot_for_flush`, `bind_embed_model`, `load_graph`, `try_load_graph`, `reload_graph`, `cold_candidates`) exist **exactly once** in the file named. Structurally, a phantom identifier could not survive here anyway: an `awk` range that never opens yields empty output, every downstream `grep -q` then fails, and the block goes red on the clean tree — which is precisely how the analyst caught its own error. All four blocks exit 0 on the clean tree, so no range is dead. Every prose line citation was also re-derived: `store/core/src/lib.rs:312` = `pub struct EmbedStamp {`, `:587` = `pub fn check_embed_stamp`, `persist.rs:73` = `fn stamp_of(`, `bootstrap/src/lib.rs:81` = `pub fn bind_embed_model(`, `health/src/lib.rs:185` = `embed_model: match &stamp {`, `commands_check.rs:126-147` = the two findings, `retrieval_query.rs:751` = `fn cold_candidates(`. All accurate.

### Validation

Blocks extracted from the four fenced ```sh regions of the published `specs/spec01.md` **by script, not retyped** (python `re.findall`), and executed as `sh -eu -c "<block>"` with empty stdin and no `cd`, exactly as `src/lifecycle.ts` collect/verify does.

- **Clean live tree, `cwd = /Users/feb/dev/cartridge/memory.ctg` @ `3432b13`: b1=0 b2=0 b3=0 b4=0.**
- Clean scratch copy baseline: **0, 0, 0, 0**; re-confirmed 0,0,0,0 after every restore (five times).
- 18 mutations this round, every one md5-verified before/after and asserted non-identical before the blocks were trusted (per `[[verify-that-a-patch-anchor-matched]]`): 5 bootstrap worlds, 5 `cold_candidates` worlds, 4 semantic no-ops, 4 block-1/block-3 regression spot-checks (`EmbedStamp` loses `dim` → 1,0,0,0; warning stops naming `memory reembed` → 1,0,0,0; `embed_mismatch` finding downgraded `error`→`warn` → 0,0,1,0; health hardcodes `embed_mismatch: false` → 0,0,1,0 — blocks 1 and 3 retain round 1's proved power).
- No `cargo` was run, so no `CARGO_TARGET_DIR` was needed and no live cartridge was restarted (`[[verify-blocks-must-not-build-live-targets]]`, `[[gates-need-a-quiet-host]]`).
- No `prd` transition command was run. Nothing was committed. The spec, the PRD and every source file were left unedited by me.
- All mutation work in `/private/tmp/claude-501/-Users-feb-dev-cartridge/546d3989-73ec-4315-89f3-a5bc45a8211e/scratchpad/reviewer-vector-r2/mut`, a private six-file copy with an `orig/` baseline (`[[subagents-share-one-scratchpad]]`). **`git -C /Users/feb/dev/cartridge/memory.ctg status --porcelain` is empty, before and after; HEAD still `3432b13`.**

Disposition: **keep** — publish as specced. NB-1 through NB-3 are optional polish and none of them can admit a regression; they can be folded into a later touch of this spec or dropped.
Reviewer identity: independent reviewer subagent `reviewer-vector-r2` (Claude Opus 5, 1M context), round 2. Did not write the plan and did not review round 1.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS** (95/100, at or above 90; no unresolved blocking finding).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed — the spec is a sound standing regression lock over existing code. Collect it; the blocks read six files, write nothing, and are green at `3432b13` in both passes.
