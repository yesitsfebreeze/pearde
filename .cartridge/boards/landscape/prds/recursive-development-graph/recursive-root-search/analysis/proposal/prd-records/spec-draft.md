---
complexity: medium
footprint:
- src/records.ts
- src/source-records.ts
- src/service.ts
- .cartridge/tests/source-records.test.ts
- .cartridge/docs/source-records.md
---
# A bounded public projection reuses the PRD owner

Baseline10637d19 proves the trusted scan includes private metadata/body and replacement-decodes invalid UTF8. Add exported async `sourceRecords(boardsRoot, board, request, deadlineMs, track?)` and native-only `prd` operation `source_records`; ordinary planning scan/edit and tool.prd stay unchanged. Reuse parseDocument through an internal/exported text parser and the existing confined bounded file reader; do not invoke CLI/scan descendants, Memory, events, spill, journal or locks.

Requests accept only board, action index/read, expected_source_revision, deadline_ms, and for read path/expected_revision. Board is the existing normal selector under configured boards. Both expected revisions are lowercase64hex; source revision is mandatory and compares exact settings bytes against the census. No path/root/cwd/config authority overrides. The helper selects exactly one existing canonical board under configured scope, and records only beneath its own prds tree. Read paths are normal board-relative `prds/.../prd.md`, <=4096UTF8, <=32 components; hidden components, absolute paths, traversal, backslashes, symlinks and special files are refused.

A shared bounded reader uses nonblocking/no-follow open, checks file type and matching inode before/after read, reads cap+1, fatal-decodes UTF8 and hashes the exact same bytes (including BOM/CRLF) it parses. Directory identity and settings revision are checked around the operation; observable mutation returns changed, never a transactional filesystem claim. Each PRD is <=1MiB, metadata header<=16KiB; reject malformed frontmatter. Public means visibility absent/public and private absent/false. private:true, visibility:private or any malformed/unknown visibility/private value are excluded before copying path/title/text or constructing search metadata. Read of excluded records returns the same unavailable shape as missing. Public title<=512UTF8; no arbitrary frontmatter copied. Existing trusted scanner privacy behavior remains compatible.

Index enumerates only local `prd.md` files with async bounded directory iteration, sorted after collection within cap. At most4096 encountered entries, depth32,128 returned public records,8MiB bytes read and1MiB serialized response; limits are fixed initially. Every encountered filesystem entry and every file byte counts, including excluded records, without reporting private counts/names. Public items contain path,title,bytes,revision,visibility:public. Complete public index revision is SHA256 over canonical public items plus canonical root/source_revision; excluded-private-only changes do not enter that digest. Capacity returns bounded partial items with complete:false/truncated:true and static reason; never silently claim exhaustive index. No cursor or retained cache. Unavailable/malformed public entries make index incomplete with bounded static diagnostics (no raw OS messages); private records are silently excluded.

Read requires exact record revision and returns the complete valid UTF8 source text with its byte count/hash, public visibility and selected path, or changed/unavailable/capacity/malformed/timeout. Whole read response cap is8MiB to accommodate JSON escaping of a1MiB source; never label a truncated read exact. Shared schema `cartridge-source-records/v1`, status available/partial/unavailable/changed/malformed/capacity/timeout, canonical root and source_revision on successful rows. Index fields: action,index_revision,items,complete,truncated. Read fields: action,path,title,bytes,revision,visibility,text,complete:true. Failure shapes are static and do not echo unvalidated input. Document the exact bounded wire contract for Landscape/Memo reuse.

One1–2000ms absolute deadline (default500) covers all filesystem work. Native source_records shares the existing eight actual-I/O slots with source_declarations; a timed-out response must not free a slot while underlying IO is outstanding. Close all handles once issued work settles, stop further work on deadline, and never retry or acknowledge remote cancellation. Refuse requests when closed/capacity full. No synchronous unbounded directory listing or whole-array alias expansion.

## Acceptance proof

- [ ] Actual three-level PRD fixture indexes each local board independently and returns exact selected record bytes with BOM/CRLF hashes; tool.prd rejects operation.
- [ ] Private/invalid visibility records expose no marker/path/title/count; trusted scan still sees them. Invalid UTF8, duplicate/malformed headers, stale revisions, rename/replacement and missing files are explicit.
- [ ] Entry/depth/file/aggregate/wire caps, symlink/FIFO swap, delayedIO slots, deadline and closure regressions preserve bounded output and source bytes.

## Verify

```sh
set -eu
cd /Users/feb/dev/cartridge/prd.ctg
CARTRIDGE_TEST_BIN=/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/cartridge bun test ./.cartridge/tests/source-records.test.ts ./.cartridge/tests/source-declarations.test.ts
bun test ./.cartridge/tests
bun run check
```

Actual native fixture traps Memory/events and compares source tree bytes before/after. Freeze old declaration helper/service hashes; any necessary census test pin update is a separately reviewed proof refinement and revalidation, not an acceptance change. Root owns source implementation/collection after independent review. Existing source and handles are left recoverable on failure; no user data changes.
