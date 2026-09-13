---
needs:
- '@runtime/startup-eof-retains-exit-status'
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: native-tool-observation-adapter
footprint: ["Cargo.toml","src/lib.rs","src/cartridge.rs","src/service.rs","src/turn.rs","src/observation.rs",".cartridge/tests/unit/observation.rs",".cartridge/tests/integration/tool-observations.test.ts",".cartridge/tests/integration/observation-fixture.ts",".cartridge/docs/tool-observations.md","src/loader.rs",".cartridge/tests/unit/src/tests/mod.rs",".cartridge/tests/unit/src/tests/composition.rs"]
commit: "bd3b5e78d6e3ddd7dc7567b0c357d6fe60bd02df"
---

# Native tool observation adapter

Record metadata at the existing native cartridge call boundary, where the runtime knows the issuing cartridge and resolved provider generation. Reuse the opt-in bounded turn diagnostic sink; no observer RPC or second journal. This is the runtime prerequisite of [Reflex](../../../sessions/prds/reflex-reports-attributed-tool-outcomes/prd.md), inheriting its two used review rounds.

## Acceptance

- [x] Real composed native calls distinguish host-configured agent, UI and polling sources, intrinsic describe discovery, and unknown sources without trusting request identity fields.
- [x] Attempts, dispatch, valid success/error, transport uncertainty and cancellation/drop are distinct; duration and response byte size are observed without arguments or bodies.
- [x] Descriptor revisions come from successful actual describe replies, cached within exact provider generation; a changed descriptor in the same generation is visible and missing evidence remains unknown.
- [x] Disabled, full/failed sinks and bounded cache eviction preserve tool behavior; no auto-replay or rollback claim.

## Baseline and proof

[Real native baseline](baseline.json): SDK child calls tool.fixture successfully through the runtime; the existing enabled diagnostic sink contains no tool events. Use disposable processes and stores only. Public runtime tests/check plus actual native integration fixture prove the adapter; the sessions report and original mixed-use acceptance remain separate.

## Review

[Inherited review and round 3](review.md). Maximum five rounds, two already used by the original source.
