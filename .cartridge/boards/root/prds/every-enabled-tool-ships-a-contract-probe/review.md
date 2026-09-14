# Every enabled tool ships a contract probe — review

Canonical PRD: [every-enabled-tool-ships-a-contract-probe](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [every-enabled-tool-ships-a-contract-probe](../../reviews/round-1/every-enabled-tool-ships-a-contract-probe.md): reviewer 82/100; Merge. Turn prose into bounded probe metadata/schema and fixture-safety acceptance under capabilities-live-with-their-owners; keep discovery separate from execution.
  Original SHA-256: `2fc3ee87f5582575d752a880584dff58b004d64232577f869ca8be11e83b5b64`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 18 | Resolved hard dependencies and child links; external prerequisites require recorded owner handoff. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **93/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `6f3c241ba286e4ddf2c34ac395f2b0149253bbf9b352c0b9becd6ce6f0d8cc2f`. Composition: root `24aa2be` (dirty), memo.ctg `9a1cf99`, memory.ctg `c25af4d`, cartridge.ctg `c9ef10b`, prd.ctg `077e57a2` (dirty).
Change: the transport host already runs declared contracts: manifest `selftest`/`integration` keys (cartridge.ctg/src/loader/document.rs:27), `Host::verify`/`verify_one`/`run_contracts` (cartridge.ctg/src/host/run.rs:72-190), CLI `Verify` (src/cli/args.rs:126), `just verify`, unit test `verify_sends_every_declared_contract`. The old text re-invented a probe declaration and started at settings.md/justfile only. Rebased to a coverage census inside `cartridge verify`; dropped the stale debug-mode prerequisite (blocked memo citing `builtin/memory/.zirkle` paths). Pre-revision SHA-256 `977133b9779fe342d0451508ea65eb8e3d4beb255a4f414db7b0a2e588fdfbb8`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 18 | Real gap: only harness.ctg and tools.ctg declare `selftest`; uncovered cartridges pass silently. -2: coverage lines alone do not add contracts. |
| Ownership and reuse | 17 | Reuses the existing contract mechanism and test helpers. -3: host-owned work homed in the root board; rehome to runtime recommended. |
| Dependencies and slices | 19 | No hard needs; shared `host.rs` footprint with tool-probes named. -1: follow-up per-cartridge contracts not yet itemised. |
| Acceptance and baseline | 19 | Three observable checks with exact fixture location and gates `just test cartridge`, `just check cartridge`. -1: output wording not pinned beyond `no contract`. |
| Failure and compatibility | 18 | Compatibility kept (informational lines, exit codes unchanged, manifests without contracts load). -2: no statement on `verify_one` coverage output. |

Agent score: **91/100 — PASS**.
Findings: Old plan duplicated an existing mechanism (would not have passed). Rebased revision is small and verifiable.
Unresolved blocking findings: none.
Disposition: keep; rehome to `@runtime` recommended.
Validation (cwd /Users/feb/dev/cartridge): existence checks of the named starting files, fixtures and justfile recipes (`.cartridge/justfile`: check, test, smoke, verify; root `justfile`: isolation); `rg` for the named symbols and tests; `git log` in the owner submodules; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md` and every relative link; `shasum -a 256`. No product gates (`just check`, `just test`, `just smoke`, `just verify`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: select when ready; add the fixture beside `verify_sends_every_declared_contract` first.
