# Preserve one outcome across its actual owners

The native baseline at FS `de140668`, GitFS `b4b95bb` and Sessions `c2693a7`
proves that FS sends only `touch {id,file}` and Sessions persists a string set.
GitFS emits no Sessions callback. Existing GitFS diff already reports distinct
base/overlay/disk revisions and conflict; external changes and unrelated files
remain unowned. See [native output](baseline-native.json) and the runnable
[probe](baseline-probe.ts). This is an attribution gap, not an inspection gap.

The historical source explicitly named Sessions and GitFS as participants, while
the migrated leaf names only FS. The engine requires source ownership by repo.
Propose these leaves, all inheriting rounds 1–2; no records or map entries have
been created or transitioned by this proposal:

| Proposed canonical owner | Observable outcome | Hard prerequisites |
| --- | --- | --- |
| `@sessions/file-change-records-retain-reported-revisions` | One strict, bounded Sessions-owned schema and durable per-session record/read API | existing client mapping contract |
| `@fs/improve-fs-change-provenance/direct-file-mutations-report-revisions` | FS reports exact known publications through that schema | Sessions record API; existing FS revision guards |
| `@gitfs/overlay-mutations-report-revisions` | Actual overlay/snapshot/materialize mutations report their storage targets | Sessions record API; existing readable diff |
| `@runtime/shipped-gitfs-profiles-grant-change-recording` | Existing default/live/MCP profiles grant Sessions to GitFS explicitly | GitFS producer; Sessions record API |
| existing `@fs/improve-fs-change-provenance` as rollup | Original three checks pass in a real composed profile | all four leaves above |

Draft records (`prd-draft.md`, never scanner-discoverable `prd.md`) and specs are
under [proposals](proposals). They are review inputs, not
live PRD states. The parent spec remains the integration qualification. Root must
create/refine canonical leaves and bind exact digests before implementation.
Sessions roster work retains its current lease; source baseline/review is refreshed
after that independent work lands. FS's new read-only context manifest fix remains
separate and its snapshot/no-touch behavior is a mandatory compatibility gate.

Records carry provider-reported invocation coordinates, never authentication or
ownership. Existing Sessions mapping metadata is not copied into actor identity.
The native Sessions service retains its documented host-trusted access boundary.
The shared Rust DTO lives in Sessions, avoiding three independently drifting
schemas; its source library introduces no service or authority.

No global journal, background observer, filesystem scan, implicit snapshot/import,
new authentication, cross-backend transaction or automatic retry is introduced.
The Sessions log is bounded and can become full; a published file plus failed or
uncertain recording is explicitly partial. An absent GitFS Sessions grant leaves
standalone mutation behavior available with `attribution: unavailable`; the
shipped profiles and integrated proof opt in through the exact grant. An injected
provider that later fails is reported as a recording failure, not as absence.

The four owner implementation specs and parent proof are one substantive round3
review candidate. Scope/ownership splitting does not reset review allowance.
