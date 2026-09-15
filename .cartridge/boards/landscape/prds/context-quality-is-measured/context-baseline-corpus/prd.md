---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: context-quality-is-measured
footprint:
- /Users/feb/dev/cartridge/memo.ctg/.cartridge/tests/context-quality/
- /Users/feb/dev/cartridge/memo.ctg/.cartridge/docs/context.md
---

# A pinned corpus records the memo context baseline

memo's `context` operation (`src/context.rs`, `evidence` crate) is the selector under test. A corpus was frozen on 2026-09-13, before any candidate observation, in [analysis](analysis/): `corpus-manifest.json` (100 and 10000 rows; corpus SHA-256 `f8148994…`, `5ed27206…`; six scenarios; 16 KiB cap). One baseline run at memo `a458148` is in `analysis/baseline.json`. That run used Python and the dissolved landscape layout, so it is historical evidence and not a gate input. This leaf moves the frozen corpus into memo and records a reproducible baseline at a pinned memo revision.

## Acceptance

- [ ] A Bun generator in `.cartridge/tests/context-quality/` regenerates both corpora with the manifest's digests. Critical facts, forbidden tokens and provenance expectations are copied byte-identically from the manifest.
- [ ] A runner builds a pinned memo revision in a disposable second checkout. It drives the base (`cartridge --dir <tmp> run memo '{"op":"context",…}'`) with Lua fixture providers for memory and files, and runs one warmup plus five timed prepares and exact readbacks per scenario and size. It writes raw results with corpus, source, toolchain and binary digests, and the original trees stay unchanged.
- [ ] The runner fails by name on forbidden output, wrong provenance, a response over 16384 bytes, unreported truncation, a digest mismatch or a failed build. Known misses (`DOC_TAIL_CRITICAL` at 100; documents unavailable at 10000) are recorded as findings, and a failed run never replaces an earlier good baseline.

## Proof and recovery

Reuse `.cartridge/tests/integration/host.ts`. Gates, cwd `/Users/feb/dev/cartridge`: `just test memo` and `bun test memo.ctg/.cartridge/tests/context-quality/baseline.test.ts` (created by this leaf). Neither has run. They need memo's events-model port (`83bf1ad`) and a base binary. Timings are fixture evidence, not model quality.

## Dependencies and review

No hard prerequisite. Rounds 1–2 are inherited from `context-quality-is-measured`; round 3 rebased ([review](review.md)).
