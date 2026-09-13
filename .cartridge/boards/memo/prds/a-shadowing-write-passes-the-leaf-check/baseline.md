# Baseline — 2026-09-13

At memo revision 535915d3315ead89b92811cb70e63dd592d705b1,
`RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR=$PWD/target/tool-result-contract just test memo`
from the runtime passed all 48 tests. The output is retained in baseline-log.txt.
Existing namespace fixtures preserve both shipped identities, prefer an explicit
workspace reference, reject local duplicate leaves and refuse shipped-file writes.
Validation already limits leaf uniqueness to the workspace record, so the old
shadowing defect is not reproduced. The remaining proof must exercise the actual
shadowing write with both shipped records supplied, not only a write made before
that merged view is loaded. Add the stale-revision case to that same fixture.
