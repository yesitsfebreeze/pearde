---
complexity: medium
footprint: ["src/records.ts","src/service.ts",".cartridge/tests/source-declarations.test.ts",".cartridge/docs/source-declarations.md",".cartridge/tests/records.test.ts","src/source-records.ts",".cartridge/tests/source-records.test.ts",".cartridge/docs/source-records.md","package.json","bun.lock"]
---

# Normalize existing declared board edges before strict descendant checks

Actual baseline at PRD d9c79a00 and Landscape62185289: maintained members()/scan handles a three-level declaration tree and same-named records; missing child and backlinks abort scan. Keep that strict planning behavior. Extract/reuse the existing raw member-name/location interpretation from records.ts, preserving accepted mapping/list forms, duplicate/invalid member rejection and alias grammar. No new YAML parser/language or changed mutation semantics. The new helper calls the maintained document grammar on the exact bounded settings bytes; existing members() adds its existing canonicalBoard/existence/confinement checks as before.

Implement exported async readonly `sourceDeclarations(boardsRoot, relativeBoard)` and one **native-only** request on the existing `prd` capability, `{op:"source_declarations",board:"root"}`. No new capability key/manifest grant is necessary: main's existing `prd` routing branches to this method before tool dispatch; `tool.prd` still rejects it. This is the actual callback transport for later native consumers, not only a fixture API. Do not route through CLI execute/scan, mutation locks, Service.result spill, Memory recall/outbox or event publication. Bound ordinary wire concurrency as currently; return plain bounded JSON or static status without persistence.

Native board selector is a normal relative path below the configured `.cartridge/boards` (<=512 UTF8 bytes, <=32 normal components, no empty/current/parent/NUL/absolute/backslash forms). It cannot override root/config/cwd. Canonicalize and confine existing selected board under that configured root, then read only settings.md with a <=64KiB full-byte cap; reject nonregular or internal symlink settings files. Parse this exact text once using PRD's maintained grammar; SHA256 is over those exact bytes (including CRLF/BOM), and parsed members derive from that same text. No descendant file/read/exists requirement. At most64 declared edges; each alias follows existing member grammar <=64bytes, each location <=4096bytes before copying; normalized destination is absolute, <=4096bytes, lexically normalized and canonically confined as far as existing ancestors permit. Keep current per-board parent confinement plus configured boards scope. A missing child remains a normal declared edge for the census to classify; out-of-scope/malformed declaration fails this one result explicitly.

Available wire shape is `{"schema":"cartridge-source-declarations/v1","status":"available","root":<canonical selected directory>,"revision":<64 lowercase SHA>,"children":[{"name":<member alias>,"root":<normalized absolute target>,"kind":"board"}]}`. Sort children by alias; no record bodies or unrelated settings metadata. Entire serialized response <=262144bytes, checked without spill. Static failures are `unavailable`, `malformed`, `capacity`, or `timeout`; no raw OS/error text. The caller supplies the shared deadline; optional native deadline_ms1..2000 bounds awaiting reads/checks without claiming that a synchronous parser or filesystem operation was interrupted. No process spawn, provider activation, tool call or lifecycle action occurs in this operation.

## Acceptance

- [x] Existing member grammar and strict scanner behavior remain compatible.
- [x] Native and exported declarations preserve exact settings revisions and missing-child edges under configured root authority.
- [x] Actual composed-host and boundary tests prove bounded, native-only reads without operation-side writes or provider calls.

## Verify

Tests use actual settings declarations across three levels, missing child, backlink and repeated mount. Compare old members()/scan successful output and expected existing failures before/after. Native SDK and actual composed Host calls to `prd` prove operation reachability and omission from model tool operations; temporary fresh service state plus provider callback sentinels and before/after filesystem digests prove no operation-side Memory/events/spill/locks/writes. CRLF SHA matches exact bytes. Invalid root overrides, escaped symlinks, oversized settings/edges/paths, malformed members and cap failures are explicit and bounded. Source edits yield a new declaration revision; a deleted selected board is unavailable.

```sh
set -eu
export CARTRIDGE_TEST_BIN=/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/cartridge
test -x "$CARTRIDGE_TEST_BIN"
bun run test
bun run check
```

The maintained source-declarations.test.ts includes the actual composed-host proof, required by CARTRIDGE_TEST_BIN above. records.test.ts verifies immutable migration fidelity against its original committed snapshot while independently checking live canonical identities and graph, so legitimate lifecycle progress does not invalidate migration history. This spec preserves inherited rounds1–2 and requires independent round3 review before source changes. Landscape depends on this collected adapter; no records are copied, moved or deleted.
