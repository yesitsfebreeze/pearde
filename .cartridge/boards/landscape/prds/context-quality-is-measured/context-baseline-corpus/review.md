# A pinned corpus records the old selector baseline — review

Canonical PRD: [@landscape/context-quality-is-measured/context-baseline-corpus](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [context-quality-is-measured](../../../../root/reviews/round-1/context-quality-is-measured.md): reviewer 86/100; Resequence. Capture the corpus and old-path baselines before the replacement selector lands; define measurable regression tolerances and fixture sizes.
  Original SHA-256: `d4357ac7cf0b610600f4e48d5a080cfa891ac4845efd645d36f379b0a6a928e9`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 19 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.

Reconciliation verdict: **REBASE**. Aligned with the parent's round-3 REBASE (owner memo; baseline = the memo revision pinned when the corpus is frozen; the landscape snapshot is optional).
- The stale revision cited `landscape.ctg/src/lib.rs`, `surface.rs` and `just test landscape`. None exists: landscape was dissolved, and the selector is memo's `src/context.rs` over `memo.ctg/evidence` (memo `8d6a803`; cartridge.ctg `939e7d1` removed core fabric/evidence).
- Material evidence the stale text ignored: `analysis/` already holds a corpus frozen before observation (`corpus-manifest.json` SHA `e12fc1e6…`, generator `915a60e0…`, 100/10000 corpora `f8148994…`/`5ed27206…`, six scenarios, 16 KiB cap). It also holds a measured baseline at memo `a458148` (`baseline.json`, raw `19389aef…`) and a spec draft.
- That work is Python (`baseline-probe.py`, `corpus-generator.py`), contrary to decision `cartridge-repositories-keep-records-and-executable-memos`. It is owned by landscape, and it drives the old SDK socket rather than the base's events model.
- Revision: keep the frozen manifest bytes and expectations; port the generator and runner to Bun under memo `.cartridge/tests/context-quality/`; drive the base (`--dir <tmp> run memo`, per `PORTING.md`) with Lua fixture providers (the pattern memo `3dc1f61` already uses); pin the baseline at a memo revision; demote `a458148` results to historical evidence; state named failure cases and non-overwrite.

Stale presented revision: `aee3d5781808465edde2e0b3c13b6fd860e8b1b6fa2b714c753413995aaa664a`. Revised revision: `prd.md` SHA-256 `772afb76dfffd8784074dcfdf8550b377c8f8d9ba57cf553e1e0066a94317f26`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | A reproducible quality/cost baseline for memo's context selection is still wanted, and the frozen corpus is reused instead of redone. -2: the redefined baseline (a memo pin, not the dissolved old path) should be confirmed at claim, as the parent notes. |
| Ownership and reuse | 19 | memo owns the selector; the leaf reuses the manifest, `host.ts` and Lua fixture providers. -1: the board alias is still landscape. |
| Dependencies and implementable slices | 18 | No hard needs; the parent graph resolves. -2: executable only after the transport port is on main and a base binary is available (a porting precondition, not a defect). |
| Observable acceptance and baseline evidence | 18 | Byte-identical digests, a fixed run shape, named failures and recorded known misses. -2: `.cartridge/tests/context-quality/` and `baseline.test.ts` do not exist yet; the leaf creates them. |
| Failure, recovery and compatibility | 18 | Disposable checkout, original trees unchanged, a failed run never replaces a good baseline. -2: the Lua fixture providers for memory and files model boundary answers only; the leaf states timings are fixture evidence, but provider fidelity is not bounded. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Word count 294 body / 323 with frontmatter (`wc -w`).
Findings: the Python analysis files stay as historical evidence inside this PRD directory; do not copy them into memo.
Unresolved blocking findings: none.
Validation (read-only): `ls`/`rg` existence checks on memo.ctg `83bf1ad` (main = ws branch `transport`: `src/context.rs`, `evidence/`, `.cartridge/docs/context.md`, `.cartridge/tests/integration/{host.ts,context.test.ts}`), fs.ctg ws `03f360e` manifest, sessions.ctg `118b784`, ws/pty.ctg `c003065`, ws/router.ctg `ab184a1` (`src/context.rs`, `src/proxy.rs` `explain_routes`), ws/cartridge.ctg `ba198f4` `docs/transport.txt` and coordination `PORTING.md` (`--dir <dir> run <event>`); reads of the analysis files in context-baseline-corpus; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md`, footprint paths on main or ws, and every relative link; `wc -w`; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: port the generator and confirm the digests reproduce before writing the runner. Coordinator: rehome to the memo board with the parent.
