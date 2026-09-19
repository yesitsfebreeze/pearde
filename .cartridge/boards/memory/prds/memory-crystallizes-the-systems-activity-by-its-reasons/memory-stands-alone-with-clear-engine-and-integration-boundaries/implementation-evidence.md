# Verified existing standalone baseline

The existing implementation was committed at ff22be8dda3814e79b4d830c9904261b167af160 after scoped source selection and independent validation. The checked standalone implementation lane starts at collected writer commit d9161cd2f3a363915c7a7d642a4955e7a3836065 and contains no new source changes. The writer changed only README/help within this structural footprint.

Independent verifier /root/baseline_verify ran the published contract at that exact clean lane: 19 experience tests and six ASP tests passed, including all 11 named acceptance tests. Workspace check, formatting, 29-package/160-internal-path dependency validation and retired-ledger absence passed. See evidence/current-standalone for hashes, verdict and command logs. Prior baseline and both preserved plan review rounds remain historical evidence.

Root memory hard audit and 21-cartridge isolation passed after writer integration. Committed-only collection certifies the named source artifact. Live unrelated task, Scope, body-readback and concurrent graph-rollback changes are preserved and not certified by this proof. No loaded cartridge was replaced. This structural receipt does not collect the behavioral acceptance of other initial-feature or memory-reliability leaves.
