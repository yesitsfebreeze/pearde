---
complexity: small
footprint:
- src/file_kernel.rs
- src/lib.rs
- src/inventory.rs
---

# Collect the compact inventory library and native adapter together

This rollup retains all three original acceptance checks and inherited review rounds. It adds no implementation. The existing inventory module is listed only to bind the collected owner source, as the PRD spec publisher requires a nonempty footprint. The child Landscape library owns trusted composition capture, exact owner/path inventory, resource bounds, partial outcomes and frozen summary/page rendering. The memo child owns the additive native version 2 request and one-instance publication lifecycle. Unversioned native and model requests retain their existing contracts.

Measured combined proof: Landscape 62185289d148017c74986b618456a72bab620228 and memo 1ffca32db1d06364b3e35e6cbca4881a1f814f71. A real 10,000-path Git fixture now yields a 393-byte default version2 summary; the largest explicit page is 11,731 bytes. Every exact owner/path pair reconstructs once. One initial host snapshot call supplies all pages, with zero extra host work while paging. Two explicit refreshes account for the test's total three host calls. Before implementation the legacy fixture response was 260,311 bytes with no path cursor.

Unique capture tokens distinguish replacement from stable source content. Actual native fixtures prove stale-token refusal on identical refresh/restart, changed filters, and newest-started capture publication after success or failed refresh. Shared library fixtures additionally prove nested/shared roots, newline/escaped paths, process and aggregate resource caps, and source preservation. Partial contributor statuses keep unknown counts distinct from zero. No document bodies, provider activation, automatic retries or persistent inventory writes are introduced.

## Acceptance

- [x] Both child receipts bind passing reviewed checked contracts at the source revisions above.
- [x] Combined native proof retains the original 10,000-path/16-KiB reconstruction, stale replacement and partial readonly behavior, using the single shared library.

## Verify and proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
python3 - <<'PY_SOURCE'
import subprocess
for repo, expected in [('../landscape.ctg','62185289d148017c74986b618456a72bab620228'),('../memo.ctg','1ffca32db1d06364b3e35e6cbca4881a1f814f71')]:
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip() == expected
    assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True).strip()
PY_SOURCE
bun test ../memo.ctg/.cartridge/tests/integration/inventory.test.ts
```

The source-bound SDK builds the actual native binary against the exact shared library. Child proofs record 40 Landscape tests/check, 77 memo tests/check and native inventory3 tests/10,183 assertions plus context3 tests/80 assertions. Child receipts are collection prerequisites; this parent has no separate source commit. Limits remain scoped to post-decoding host data, bounded scan/serialization buffers, and observed cross-repository snapshots rather than atomic transactions. Timed-out work requests termination without asserting joined workers.
