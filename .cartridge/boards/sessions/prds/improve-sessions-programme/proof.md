# Integrated sessions programme evidence

All three [dependency receipts](proof-dependencies.json) are engine-verified at
`b772c6ee4f1ad476995c8c8c07cd02ed2be264fa`, including refreshed mapping and recovery
receipts. Their independent reviews passed within inherited limits: mapping 96,
retention 95 and recovery 96, each at round 3. Programme review: independent
coordinator `/root`, round 3, **97/100**.

[Exact commands and evidence bindings](proof-inputs.json) reference the unchanged
integrated source's completed gates: **41 native sessions tests**, public sessions
check/build, **41 harness tests**, and **7 actual SDK integration tests with 83
assertions**. The executable rollup spec reruns combined tests and verifies each
dependency receipt at collection. Its source footprint is the exact 14-path union
of all three leaf specifications; no implementation or user-data changes were made.

Verified mitigations include immutable host identity instead of copied metadata,
reconnect isolation, preserved transcript bytes, stale revisions and atomic-write
failure handling, protected retention and real harness activity-race refusal,
exact backups with explicit bounded resume, and narrow revision-checked legacy
repair. Receipt refreshes retain prior collection history.

Limits remain explicit: native services trust their host, external references need
registration, transcript writes retain a single active owner across processes,
uncooperative direct filesystem changes are not a distributed transaction, and
recovery never replays model/tool work automatically. Unconfigured client mappings
remain instance-scoped. Retention backups remain until explicit operator handling.
All deletion and failure fixtures use disposable directories.
