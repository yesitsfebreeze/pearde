---
complexity: small
footprint: []
---

# Collect the combined document contract

This rollup preserves the existing three-child scope and inherited review rounds.
It owns no new runtime implementation. Identity supplies one canonical owner/path
and exact primary revision; projections add bounded public linked prose with a
separate derived digest; validation freezes a conservative Just descriptor without
launch authority. No full Just grammar, runner, sidecar/event lifecycle, model tool
migration or execution permission is claimed here.

The combined native fixture at3251566 reads one source through metadata index,
commands, docs, human and validate. Every view agrees on primary identity/revision.
Editing only a prose dependency changes the readable projection digest while the
primary/validation revisions remain fixed. Editing primary description, prose and
recipe updates the respective views without a synchronization action. No new paths
are created. See integration-proof.json and retained integration-probe.txt.

The collection gate binds all three passing child contracts. Each child must have
its reviewed checked acceptance and current source receipt before parent collection.
All three child receipts now bind memo 3251566e6c92439e4a32c5ce8b734e55726801ee
and their current checked specifications; they remain collection prerequisites.

## Acceptance

- [x] All three child receipts bind their checked acceptance and passing review at the integrated source revision.
- [x] Actual native integration proves shared identity/revision, linked-only digest separation and primary edits updating index/prose/commands without launches or hidden writes.

## Verify and proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
cargo build --manifest-path ../memo.ctg/Cargo.toml -p memo_cartridge
python3 - <<'PY_VERIFY'
from pathlib import Path
import hashlib, runpy
probe = Path('../prd.ctg/.cartridge/boards/memo/prds/one-document-serves-every-reader/integration-probe.txt')
assert hashlib.sha256(probe.read_bytes()).hexdigest() == "ac02bef73a906b9f4c89fdb54afd48ae47d9ef5699b81fedafa4f064455eeea6", 'integration probe changed'
runpy.run_path(str(probe), run_name='__main__')
PY_VERIFY
```

Child public gates cover77 memo tests and the public check; validation SDK63 and
context compatibility80 assertions pass at3251566. Historical identity/projection
proofs remain append-only and are supplemented by refreshed collection receipts.
