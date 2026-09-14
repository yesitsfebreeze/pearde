# plugins-from-memory-toml — review

Canonical PRD: [@runtime/plugins-from-memory-toml](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [plugins-from-memory-toml](../../../root/reviews/round-1/plugins-from-memory-toml.md): reviewer 25/100; Rehome. General plugin configuration is excluded from current memory; reconcile needed configuration with cartridge composition instead of reviving memory plugins reload.
  Original SHA-256: `68b1000e48af6200c9830477a19081994e12b4571f67a7ee00a1608e3d6aadff`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14 (reconciliation, no score)

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `2730ac77ef51ca98bde8801da3571b2cc297c1b6278e5382c5a48b13a095208b` (frontmatter review fields only; body unchanged).

Reconciliation verdict: **SUPERSEDED**. The `[[plugin]]` rows in `memory.toml` and `memory plugins reload` do not exist in memory.ctg (`rg -i plugin memory.ctg/src/config` finds nothing). Composition is the host's:
- Profile entries `{id, path, disabled, config, inject}` in `.cartridge/init.lua`, laid over by `config.lua` (`cartridge.ctg/src/loader/entries.rs`).
- A duplicate entry id is refused (`entries.rs:71` "duplicate entry id").
- Reload is `Host::replace`/`reconcile` (`src/host/socket.rs:301`).
- Decision `a-cartridge-brings-its-own-surface` (2026-09-14, user) puts optional wiring in the profile and `config.lua`, never in a sibling's config.

The remaining generic checks (invalid candidate profile preserves the running composition) belong to host composition work such as `@runtime/cartridges-compose-recursively` / `the-profile-is-the-root-composer`, not to this item.
Recommendation: retire; keep the round-1 source as history. `state:` unchanged.
Validation: `rg` in memory.ctg and cartridge.ctg `src/loader`/`src/host`, decision memo read. No product gates were run.
Rounds used / remaining: 3 / 2.
