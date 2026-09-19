# @mcp/the-mcp-instances-fixture-composes-policy-without-reaching-across-the-boundary review history

Plan: `@mcp/the-mcp-instances-fixture-composes-policy-without-reaching-across-the-boundary`,
`prd.ctg/.cartridge/boards/mcp/prds/the-mcp-instances-fixture-composes-policy-without-reaching-across-the-boundary/prd.md`.
Scope: executable leaf — `just isolation` passes composition-wide again with
`mcp.ctg` naming no sibling checkout, and `instances.test.ts` proving exactly
what it proves today.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: superproject `c7e0894`, `mcp.ctg` `9db553e` (`mcp.ctg`
worktree clean, `git status --porcelain` empty before and after this review).
Superproject dirty at review time: `.cartridge/config.lua`, and the submodule
pointers `prd.ctg`, `proxy.ctg`, `router.ctg` — none in this footprint.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../prd.md` — `82eca707ff8cf6651c64c78025f3a658dcf37a680a14836733d151d940bfabf8` |
| Specs | `specs/spec01.md` — `ae0888be61bd167631897f355aa3728d426577a31b7219a369da946313e40dd0` |
| Material contracts/dependencies | `mcp.ctg/.cartridge/tests/integration/instances.test.ts` — `69d08e8a42a0f19a5155452272e2ba4488bdc703d35eb832c870dc93239d5f9f`; `.cartridge/memos/routine/check-cartridge-isolation.md` — `23f76eb5e6e4bdd409c6fb6e6eeb3650e5a9c9a5f7e3268d28c0cfc7c26c7a0a`; `.cartridge/memos/system/isolation.md` — `d0314b51dd9ba0dd4c9dabd049191555c5418b53fbecd82a96c336bfa3ae7543`; `mcp.ctg/src/service.rs`, `mcp.ctg/src/lib.rs`, `cartridge.ctg/src/host/mod.rs`, `policy.ctg/cartridge.json` at the same revisions |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | Removes the one illegal reference that fails `just isolation` composition-wide and blocks `@root/.../web-ctg-exists-as-a-cartridge` from collecting. Root cause (the file copy), not the symptom; one file, one step, no source or manifest change. Reproduced the failure verbatim through block 1: `mcp.ctg: .cartridge/tests/integration/instances.test.ts:63 includes policy.ctg`, exit 1. |
| Ownership and reuse | 20 | The three sanctioned ways out were checked against the code, not assumed. `mcp.ctg/cartridge.json` `needs` is `["sessions","policy","policy.*","tool.*"]` — the need **is** declared; `service.rs:574-605` emits one `policy` event per `tools/call` and proceeds only on `Some("allow")`, with `ask`/`deny` refusals and `_ =>` "invalid policy decision" — the integration **is** an event. Only the copy is illegal, so "ship an own copy" is the correct remaining door. The stub reuses the fixture's existing `cartridge(profile, id, manifest, init)` helper, the same one already used for `sessions` and `echo` — no new mechanism. |
| Dependencies and implementable slices | 19 | One step; diff verified byte-exact — lines 62-63 out, ten lines in, nothing else in the file touched. `mcp.ctg/Cargo.toml` has no sibling path dependency (only `path = "src/lib.rs"`), so a lone lane worktree builds. −1: block 2's cold host build inside the collector's 120 s was not provable here — my runs were warm (host 4.5 s, module 4.2 s against a shared registry). The spec discloses the risk and names the `claimed`-with-no-lane fallback. |
| Observable acceptance and baseline evidence | 17 | Three blocks, each red before and green after, **all three measured by me** (see Validation). Cheat table reproduced 7/7 exactly, independently built. −2 for F1 (block 1 has a silent-pass channel: it never asserts the sibling set it built). −1 for F4/F5 (PRD acceptance names `just audit`, no block covers it; the spec's first "Remaining risk" bullet is now factually stale). |
| Failure, recovery and compatibility | 18 | Block 3's guards are all single-statement: no `! grep`, no BSD `\|` alternation, no `test -n "$x" && test …` list; `count=$(grep -c …)` then `test "$count" -ge 11` is the correct form and bites (cheat-a2, census 5). No failure message prints the token it wants — the skip guard prints the offending line, not the cure. The `grep -nE 'skip…'` false positive on the word "skip" is disclosed and deliberate. −2 for F2: block 1 never removes its shadow root; five leaked in this session alone, and collect runs the block twice. |
| Reviewer total | **94 / 100** | PASS — ≥90 with no blocking finding. |

### Independently reproduced cheat table

Seven scratch trees built from `git -C mcp.ctg archive HEAD`, each symlinked in
as `mcp.ctg` under a fresh shadow composition root, gated through the real
`memo-run`; `guards` is block 3 verbatim with cwd at the tree. `census` is
`grep -c 'expect('`.

| tree | isolation | guards | census | agrees with analyst |
| --- | ---: | ---: | ---: | --- |
| `base` (live fixture) | 1 | 1 | 11 | yes |
| `ref` (step 1 applied) | **0** | **0** | 11 | yes |
| `cheat-a` (policy assertions deleted) | 0 | 1 | 5 | yes |
| `cheat-a2` (`ref` + same deletions) | 0 | 1 | 5 | yes |
| `cheat-b` (skip when the sibling is absent) | 0 | 1 | 11 | yes |
| `cheat-b2` (`ref` + unconditional `skipIf`) | 0 | 1 | 11 | yes |
| `cheat-c` (hardcoded `allow`, settings and config dropped) | 0 | 1 | 11 | yes |

`ref` is the only 0/0. No cheat clears both. The analyst's table is confirmed
in full, including which guard bites for `a2`, `b2` and `c`.

### Ruling: block 2 is no longer unmeasured

The analyst's disclosed gap is **closed by this review**, not carried forward.
Built the host and the module into `/tmp/rv-mcp/target` (outside every
repository) exactly as block 2 does, then ran block 2 verbatim:

- `ref` tree: **1 pass, 0 fail, 13 `expect()` calls, 2.88 s, exit 0.**
- live `mcp.ctg` (the `base` fixture, composing the real `policy.ctg`): **1 pass,
  0 fail, 13 `expect()` calls, 2.77 s, exit 0.**

Identical pass and identical `expect()` census on both sides. The analyst's
diagnosis was right: its red was the stale checked-in host binary (Sep 16 23:40,
predating `ec4de01`), which is why block 2 builds the host itself. The spec does
**not** ship with its main block unmeasured.

### No assertion is weakened

Verified against the hard constraint, by diff and by behaviour:

- The diff touches only lines 62-63. Every assertion, comment and helper below
  them is byte-identical to `base`.
- Both bridges initialize (`expect(initialized.result?.serverInfo?.name … )`),
  sessions differ (`expect(two).not.toBe(one)`), each stays its own
  (`toBe(one)` / `toBe(two)`), the cross-instance `notifications/cancelled`
  leaves a's call alone, killing a leaves b serving, `status` filters on
  `node.id === 'mcp' && node.state === 'active'` and `toHaveLength(1)`, and the
  run directory holds one pid directory with one `mcp.sock`. All still present,
  all still green, `expect()` census 13 (11 lines) on both trees.
- The `n.state === 'active'` term is intact and block 3 pins it by name.
- The stub is **stricter** than the sibling it replaces, not weaker: real
  `policy.ctg` declares `default: "allow"`, the stub declares `"ask"`. Drop the
  composition's `policy={default="allow"}` and the real copy would still allow
  every call (the assertions would pass vacuously); with the stub, `service.rs`
  takes the `Some("ask")` refusal arm and the session assertions fail. This
  change makes the composition's policy configuration load-bearing where the
  copied sibling did not.

### Findings

**F1 — non-blocking, fix on collect. Block 1 can pass with the defect present
if its shadow sibling set is incomplete.** The gate builds its sibling-name
alternation from the `*.ctg` directories it finds under `MEMO_OWNER_ROOT`
(`check-cartridge-isolation.md`, `const siblings=dirs.map(...)`). Measured: the
**unfixed** `base` tree, gated through a shadow root built the same way but
without `policy.ctg`, prints `Isolation passed for 16 cartridges.` and exits
**0**. Block 1 prints its own count and never asserts it. In the collector this
is not reachable — both passes walk up to the live composition root (only
`/Users/feb/dev/cartridge/.cartridge/tools/memo-run` exists; no `*.ctg` and not
`prd.ctg` carries one, so a lane cannot stop short), and there every sibling is
present. It becomes reachable in any checkout where a `*.ctg` submodule is not
initialised. One statement closes it, after the symlink loop:
`test "$(ls -d "$shadow"/*.ctg | wc -l)" -eq "$(ls -d "$composition"/*.ctg | wc -l)"`.

**F2 — non-blocking, fix on collect. Block 1 never removes its shadow root.**
`mktemp -d` with no cleanup; five `mcp-isolation-*` directories leaked into
`TMPDIR` during this review, and collect runs the block twice per PRD. Add
`trap 'rm -rf "$shadow"' EXIT` immediately after the `mktemp -d`, or `rm -rf
"$shadow"` is not enough on its own because the block exits on the gate's
status under `sh -eu`.

**F3 — non-blocking, correct the text. The first "Remaining risk" bullet is now
stale.** Block 2 measured green on both `ref` and the live tree (above).
Replace the bullet with the measured result; keep the second bullet (cold-build
timing), which still stands.

**F4 — non-blocking, informational. `just audit` is in the PRD's acceptance and
in no block.** `audit` reports every cartridge against the vision axes; it
cannot be moved by a change to one test file. Either drop it from the PRD
acceptance or note it as covered by the owner gates.

**F5 — non-blocking, citation nit.** The spec's "What the fixture actually needs
from `policy.ctg`" section cites "`lib.rs:29`" inside a paragraph headed
"Measured, at `policy.ctg/cartridge.json` and `policy.ctg/init.lua`".
`policy.ctg` is pure Lua and has no `src/lib.rs`; the line is
`mcp.ctg/src/lib.rs:29`, `base::needs().iter().any(|key| key == "policy.explain")`.
The **fact is correct** — mcp declares the `policy.*` glob and not the literal,
so `explain` is off and the stub rightly does not listen for it. Qualify the path.

Disposition: **keep**. Implement spec01 as written, with F1–F3 applied to the
Verify blocks and the risk note. Do not touch any assertion.

Validation (actual commands, cwd, exit status):

- `sh -eu block1.sh` (block 1 verbatim), cwd `/Users/feb/dev/cartridge/mcp.ctg` →
  exit **1**, `mcp.ctg: .cartridge/tests/integration/instances.test.ts:63 includes policy.ctg`.
  Shadow root at `$TMPDIR/mcp-isolation-hE5fb6`, composition resolved to
  `/Users/feb/dev/cartridge`, i.e. the walk-up works from a `*.ctg` root.
- Same gate over the scratch `base` tree → exit **1**, same message. Over `ref`
  → exit **0**, `Isolation passed for 17 cartridges.` The shadow-symlink form is
  confirmed in both directions.
- `sh gate-nopolicy.sh trees/base` (shadow without `policy.ctg`) → exit **0**,
  `Isolation passed for 16 cartridges.` — evidence for F1.
- `env CARGO_TARGET_DIR=/tmp/rv-mcp/target XDG_RUNTIME_DIR=/tmp/rvx TMPDIR=/tmp/rvt sh -eu block2.sh`
  (block 2 verbatim body, composition pinned because the scratch tree has no
  composed parent), cwd `trees/ref` → exit **0**, 1 pass / 13 `expect()`;
  cwd `/Users/feb/dev/cartridge/mcp.ctg` → exit **0**, 1 pass / 13 `expect()`.
  `XDG_RUNTIME_DIR=/tmp/rvx` is 8 characters, so `+ "/cartridge"` stays under
  the 48-character limit at `cartridge.ctg/src/host/socket.rs:49-53` and the run
  directories did **not** fall back to the shared `/tmp/cartridge-501`.
- `sh -eu block3.sh` (block 3 verbatim): `base` exit **1**, `ref` exit **0**,
  each cheat exit **1**.
- Cleanup: `/tmp/rvx`, `/tmp/rvt` and every `mcp-isolation-*` shadow removed.
  No daemon leaked — no process matching the scratch roots survived; the 27
  `cartridge` processes on this machine are the operator's pre-existing live
  host and were never touched. `git -C mcp.ctg status --porcelain` empty at the
  end; nothing in `mcp.ctg`, the PRD or the spec was edited.

Reviewer identity: independent reviewer subagent, round 1, session
`546d3989-73ec-4315-89f3-a5bc45a8211e`. Did not write the plan and did not implement it.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS** (94/100).
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed to implementation of spec01, applying F1, F2 and F3 to the
Verify blocks and the risk note before collect. No assertion may change.
