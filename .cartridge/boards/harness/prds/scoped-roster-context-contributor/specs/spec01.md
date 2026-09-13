---
complexity: medium
footprint:
- Cargo.toml
- src/main.rs
- src/inspection.rs
- src/roster.rs
- .cartridge/tests/unit/main/tests.rs
- .cartridge/tests/unit/inspection_tests.rs
- .cartridge/tests/unit/accounting.rs
- .cartridge/tests/unit/working_tests.rs
- .cartridge/tests/unit/roster_tests.rs
- .cartridge/tests/integration/roster.test.ts
- .cartridge/tests/integration/working.rs
- .cartridge/docs/roster.md
---

# One optional roster contribution in the composed prompt

The implementation was developed in isolated Harness lanes based on committed ca7eeabd, then integrated into the actual owner at 698a4dc9555a6b3ad8d46dcc5dd3a14463048e70. Before integration the exact existing main.rs/working.rs changes were independently reviewed, preserved as a separate commit and merged with the roster without conflict. The final tree matches the fully tested coherent candidate. The working-process test is bound in the footprint to preserve that existing behavior. Verify the committed actual owner through the separately digest-bound disposable composition: snapshot this owner and adjacent source files/manifests, verify every copied hash and run real public owner gates. Relative workspace members must resolve to the selected owner copy. Record external source/binary hashes and reject source changes during copying.

Add optional immutable config `roster{actor,credential_env,max_rows?,max_bytes?,deadline_ms?}`. Actor is a fixed host-provisioned session identity, credential_env must resolve a32..4096-byte secret at startup, row cap1..64(default20), final rendered block cap1024..8192(default4096), deadline1..2000ms(default500). Do not put credentials in prompt, inspection, storage or returned errors. Request JSON cannot override any of these fields. This is one host-configured actor context per harness instance, not automatic multi-user authentication. If the request's session differs from configured actor, return unavailable roster evidence without making a roster call. Ordinary native harness operations remain host-trusted. Default absent config performs no roster query and emits no roster block.

Reuse fixed injected sessions service and new scoped roster operation, using the immutable credential and host caps. Add the existing Landscape crate as a library dependency and compose through landscape::context::collect rather than introducing another context engine, store or memo service. Source adapter validates the roster response schema/status, authenticated actor, row/source revisions and bounded serialized size before producing allowlisted Evidence rows with observed_projection references. Each candidate contains only authorized roster metadata; labels/text remain untrusted data. Preserve unknown phase duration, unavailable contributors and omitted counts. Timeout/invalid/source errors yield explicit unavailable/timeout contribution; they do not silently produce an empty successful roster or block an otherwise fitting model context.

Capture roster once per resolved context/inspection/compaction request, retaining its revision/status in Request. Render one labeled untrusted swarm-data block after the instruction frame using existing escaping, with bounded rows and whole-row omission accounting. Do not splice source text into authoritative instructions or reparse placeholders. Closing-frame/template-like strings stay escaped evidence. A missing config leaves no block. The resulting system text participates in existing exact request-budget accounting and compaction paths; previous summary/transcript preservation and protected user/tool exchanges remain unchanged. Inspection names contributor status, source revision and selection reason without a model call or additional roster lookup.

No proxy parity or general harness-consumes-landscape completion is claimed here. That broader existing PRD may consume this adapter later, after its quality prerequisites. Parent roster remains incomplete until actual sessions and harness composition prove the optional block and all source receipts validate.

## Acceptance

- [x] Actual sessions+harness SDK bridge seeds20 scoped records plus outsiders, renders bounded roster once, refreshes a child phase without a post, and does not insert another actor's transcript or inbox.
- [x] Disabled config makes no roster call/block; copied request config/actor/token cannot override host credentials. Wrong actor/source schema, timeout and unavailable state are explicit in inspection and remain nonfatal to a fitting request.
- [x] Prompt-like names/text remain escaped untrusted data, source revisions and omission counts remain visible, and public harness unit/process/ring/working/compaction checks pass with default behavior unchanged.

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge/harness.ctg
python3 -c 'import hashlib; from pathlib import Path; assert hashlib.sha256(Path("/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/harness/prds/scoped-roster-context-contributor/verify-isolated.ts").read_bytes()).hexdigest() == "eb29f608b6f591ee7029d0e52664f119912c9186ec1519261ea22092d6f2978c"'
bun /Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/harness/prds/scoped-roster-context-contributor/verify-isolated.ts --committed "$PWD" --sessions-revision 191e2b6cb4291bdcce7a894f98bb2d475361d30f
```

The verifier archives Sessions at verified dependency 191e2b6cb4291bdcce7a894f98bb2d475361d30f, binding the integrated and collected change recorder alongside the roster proof. It records the exact owner/source snapshot and runs `just test harness`, `just check harness`, `just build harness` and `just build sessions` from its disposable composed runtime, followed by the owner's actual SDK roster.test.ts with both built binaries. All temporary stores and synthetic credentials are local fixtures. After integration, coordinator reruns this same verifier bound to the integrated clean owner and records any nonsemantic cwd/source binding change before collection. The verifier also accepts --committed /Users/feb/dev/cartridge/harness.ctg for the parent rollup: materialize the committed owner with git archive using the reviewed integrated owner, recording exact commit and file hashes. No copied-source proof alone constitutes integration.
