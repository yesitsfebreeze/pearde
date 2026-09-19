# Committed collection and explicit re-verification

`prd collect <ref> --committed` checks the integrated commit in a clean temporary
checkout. It preserves unrelated uncommitted files. The returned
`verification_target` is `committed`; `workspace_verified` and `workspace_drift`
say whether the live source checkout matches that proof. This does not establish
which cartridge binary is loaded. Test the loaded artifact separately.

`prd collect <done-ref> --reverify` reruns an unchanged collected contract against
current HEAD. It refuses missing or altered evidence, changed specifications,
unverified dependencies and active ownership. Each successful refresh archives
the exact prior receipt under its SHA-256 digest, preserving original integration
provenance. Failed proof leaves the old receipt stale and untouched.

Normal collection and legacy receipts retain their strict workspace behavior.
Later committed changes inside a footprint invalidate committed proof until an
explicit refresh passes. No later PRD automatically vouches for earlier work.
Dirty files overlapping a lane fast-forward still cause Git to refuse integration;
reconcile only the intended lane changes while preserving the user's edits, then
retry. Neither option stashes, force-resets or stages the source checkout's tails.
