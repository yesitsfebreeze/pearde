---
commit: 3b9f72854c39ddd90128a48bfce2667e387c3fba
spec-digests: {"spec01.md":"467639816673d1e5a4cf6d1e7e9b8a13a017567733d0d4ebca26461926f1405b"}
child-contracts: {".cartridge/boards/landscape/prds/improve-memo-compact-landscape/bounded-inventory-snapshot/prd.md":"57205e867076691c24a395e9f507dcc3d0395323fff963f8aaee70a28d5d11ce"}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/landscape/prds/improve-memo-compact-landscape/specs/spec01.md: exit 0

Command SHA-256: ad02a823b21f46e0331c287a9029e80e5e88b38c643932132c76f0c1533c5c4b

```text
bun test v1.3.14 (0d9b296a)

../memo.ctg/.cartridge/tests/integration/inventory.test.ts:
{"paths":10000,"summary_bytes":393,"max_page_bytes":11731,"snapshot_calls":3}
(pass) native compact snapshot pages 10000 paths exactly with one discovery and no hidden writes [4320.15ms]
(pass) cache replacement follows newest-started request and failed refresh preserves published snapshot [432.60ms]
(pass) restart, invalid inputs and partial sources are explicit while legacy landscape remains accepted [118.75ms]

 3 pass
 0 fail
 10183 expect() calls
Ran 3 tests across 1 file. [4.88s]

```
