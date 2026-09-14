---
complexity: medium
footprint:
- .cartridge/tests/context-quality/corpus.py
- .cartridge/tests/context-quality/corpus.json
- .cartridge/tests/context-quality/pins.json
- .cartridge/tests/context-quality/baseline.py
- .cartridge/tests/context-quality/test_baseline.py
- .cartridge/docs/context-quality.md
---
# Freeze and reproduce the complete native context baseline

Measured baseline `analysis/baseline.json` predates this spec. Corpus generator915a60e0 and manifeste12fc1e6 were frozen before the first selector observation: exactly100 and10000 candidate records (size−4 public typed documents, one private typed document, one declared file, one Memory entity, one public kernel entry). An undeclared file is a negative scope fixture, not a candidate. Six declared scenarios separately exercise documents, Memory, files, kernel, mixed evidence, and three6KiB documents under a16384-byte response cap. Critical facts, forbidden tokens and expected provenance are already listed; copy these exact generator/manifest bytes into the owner source without changing expectations after results. Keep old misses visible: document tail omitted at100, third budget fact omitted, document contributor unavailable at10000 due the existing4096-entry owner-reader cap. These do not make a synthetic Graph benchmark acceptable or justify changing this corpus.

Add a standalone read-only baseline runner and documentation owned by Landscape. The runner resolves exact40-hex pinned commits before use, refuses missing or mismatched objects, and creates an owned disposable second source checkout/composition from git archives. Pin Memo a458148fb21f85cabcd9e1ced85c96c581b8e0b2, Landscape422c521aed170a4d098505c73469a1a59dccf49d, FS3a79023311b1a9b30c383ec8c71cf31c20a69ee7, Runtimebd3b5e78d6e3ddd7dc7567b0c357d6fe60bd02df, Sessions191e2b6cb4291bdcce7a894f98bb2d475361d30f (the verified FS producer receipt dependency), and Runtime bd3b5's committed composed Cargo.lock SHA256bbd9430a981d958182a4f5873bd3fb90faaed66b36562e8191f14271c234b909. Bind every transitive local source input and lock byte. Source snapshots use the actual existing package files; generated minimal composition members/path plumbing may differ only to isolate these owners and must be saved and hashed. Build actual Memo and FS with offline locked dependencies and debug0/no incremental; verify source snapshots/lock unchanged after building. No symlink to mutable source, worktree stash, branch reset, provider activation, or edits to original owner trees. Reuse an explicitly designated target cache only within a coordinator-approved build window; copy resulting binaries immediately and record before/copy/after hashes. Saved binary bytes alone do not substitute for this rebuilt second-checkout proof.

Materialize the frozen fixture in an owned temporary directory. Use actual native Memo SDK `op:context prepare` and `op:context read`, actual document index/projection implementation, and actual FS SDK `fs.context`; explicit deterministic Memory and composition callbacks model existing granted boundary responses. Clearly label Memory/host fixtures: no claim of real Memory backend or Runtime-process composition performance. Enable each contributor according to the manifest. Host config owns the one file declaration; request data never chooses a source root. Deny all unexpected tool/model/write/event callbacks. Hash fixture source files before/after without following symlinks. Collect full raw Prepared responses, exact readbacks, callback traces and serialized UTF8 bytes. Verify each reference against predeclared owner/kind/exact ID/revision kind; source-byte file digest binds CRLF bytes, projection references are verified by real exact reads. Private/undeclared/config/preview/extension sentinels must be absent.

Record one warmup plus five completed timed prepare calls per scenario and corpus; exact reads and fixture creation/build are outside timing. Report all raw samples and per-ability recall, missing critical facts, row count, byte size, source statuses, complete/truncated/deadline flags, native callback counts and median latency. Source-internal document hydration is not directly observable: record null/unknown plus its pinned static bound, never infer a measured hydration count from returned rows. Preserve cap refusal and failures explicitly; baseline critical misses are findings, while forbidden output, wrong provenance, response over16384 bytes, false complete/unreported omission, unexpected side effects, digest mismatch and failed rebuild fail this baseline gate. No candidate selector is run here, and no20-percent performance comparison is claimed until the dependent comparison leaf.

Runner cleanup closes/disposes children and reaps them on success, malformed frame, deadline and exceptions; drains stderr with a bounded retained prefix; SDK line/frame size and process wait time are capped. Never recursively traverse fixture symlinks. Source/binary/fixture/manifest/toolchain hashes, exact argv/env, generated composition, exit codes, raw results and report all survive in the caller-selected output directory; cleanup deletes only owned disposable paths. A failed run retains enough evidence to reproduce it and does not overwrite a prior successful baseline. Toolchain versions are recorded and mismatches against reference run are explicit; claims of paired latency require the later gate to use the same host/toolchain/run window.

## Acceptance proof

- [ ] Exact pre-observation corpus/expectation bytes and all old source/toolchain/lock inputs are pinned; no candidate data changes them.
- [ ] A disposable second checkout builds and runs the full native context path at100/10000 with actual document and FS reads, repeated raw results, exact provenance,16KiB and scope checks.
- [ ] Baseline gaps and unavailable/internal-count information are honest, with all raw evidence retained and no original work/data mutation.
- [ ] Mutation tests reject changed corpus/pins, forbidden output, wrong references and understated truncation; malformed/timeout child fixtures are disposed/reaped and output publication does not replace good evidence on failure.

## Verify

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test landscape
just check landscape
cd /Users/feb/dev/cartridge/landscape.ctg
python3 -m unittest discover -s .cartridge/tests/context-quality -p 'test_baseline.py'
python3 .cartridge/tests/context-quality/baseline.py --repositories /Users/feb/dev/cartridge --target /Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract --output /tmp/cartridge-context-baseline-proof
```

The output path must be absent; select and record a fresh path for revalidation. Public Landscape gates preserve existing behavior; the explicit native runner is the behavioral baseline gate. The comparison child consumes the frozen manifest/pins and saved raw result contract, and remains incomplete until its separate reviewed comparison proof.
