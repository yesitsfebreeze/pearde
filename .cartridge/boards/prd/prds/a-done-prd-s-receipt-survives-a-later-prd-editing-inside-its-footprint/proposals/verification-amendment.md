# Proposed bounded verification amendment (not published)

The final approved contract remains unchanged until independently reviewed.
Clean HEAD lacks the unrelated untracked runtime declared-settings child needed
by an existing global live-board graph test. No unrelated board record will be
committed or copied into the candidate to disguise that limitation.

## Exact changes proposed

Prepend this setup block to Verify and Proof, preserving every named regression:

```sh
bun install --frozen-lockfile
```

Keep the collection-proof named test block and the full engine suite unchanged.
Replace only the clean-candidate records invocation with the two self-contained
fixture/migration tests. Keep the TypeScript check in the same block:

```sh
bun test ./.cartridge/tests/records.test.ts --timeout 30000 -t 'the accepted-states check|migration preserves'
bun run check
```

Before collection, independently run the full unchanged records.test.ts against
the canonical live board, with records.ts, planner.ts and records.test.ts hashes
proven identical to the candidate. Record dataset manifest digest and observation
time. This audit establishes only the named live dataset's validity; it does not
claim the committed board snapshot is complete. Preserve the failing clean-HEAD
graph result and exact missing reference in verification evidence.

Execute live audit from /Users/feb/dev/cartridge/prd.ctg:

```sh
bun test ./.cartridge/tests/records.test.ts --timeout 30000
```

The live-board test remains required; failure blocks collection. Record the live
audit independently rather than falsely attaching it to committed-snapshot proof.
Source/helper behavior, invariants, exact source footprint and all eight named
regression gates remain unchanged. No new repair scope or PRD is introduced.

## Code identity and initial dataset manifest

| File | Live SHA-256 | Candidate SHA-256 |
| --- | --- | --- |
| `src/records.ts` | `e17e8615d3f9b99012a78cc3d500b03820312fd2c4ea1f27923225331a598926` | `e17e8615d3f9b99012a78cc3d500b03820312fd2c4ea1f27923225331a598926` |
| `src/planner.ts` | `fd60f4c7603e212279d47bf1bc37a30e7f2b28d2865b9cc3cbb175317807fcfe` | `fd60f4c7603e212279d47bf1bc37a30e7f2b28d2865b9cc3cbb175317807fcfe` |
| `.cartridge/tests/records.test.ts` | `4369020d825cf92456e94f5c5e5f369a98dacf4da4a917e43dbbf91e91589a7e` | `4369020d825cf92456e94f5c5e5f369a98dacf4da4a917e43dbbf91e91589a7e` |

Initial live dataset digest: `0c0a9f6dc6281a0f71610f35b65855bed14fc4edbbf62643aac6996bddc75c28`. Full paths and hashes, with UTC observation timestamp, are in `verification-amendment.dataset.json`. Refresh the manifest when the final audit runs.
