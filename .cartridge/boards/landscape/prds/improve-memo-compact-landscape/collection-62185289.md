---
commit: 62185289d148017c74986b618456a72bab620228
spec-digests: {"spec01.md":"6aeb4e525964949fe3d3170f3ca4694f30c806c3db5fcc1a26a589add3fb9870"}
child-contracts: {".cartridge/boards/landscape/prds/improve-memo-compact-landscape/bounded-inventory-snapshot/prd.md":"752e93a13fb88367bbbf48c1552efe63ceae0c652267493c586b88acd78fc5a4"}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/landscape/prds/improve-memo-compact-landscape/specs/spec01.md: exit 0

Command SHA-256: c6ad9d1d59d9ad124ac0a66c2ff65c56d4b5b6fc9695bc4c0e21faea776563ca

```text
bun test v1.3.14 (0d9b296a)

../memo.ctg/.cartridge/tests/integration/inventory.test.ts:
{"paths":10000,"summary_bytes":393,"max_page_bytes":11731,"snapshot_calls":3}
(pass) native compact snapshot pages 10000 paths exactly with one discovery and no hidden writes [7392.22ms]
(pass) cache replacement follows newest-started request and failed refresh preserves published snapshot [471.20ms]
(pass) restart, invalid inputs and partial sources are explicit while legacy landscape remains accepted [177.61ms]

 3 pass
 0 fail
 10183 expect() calls
Ran 3 tests across 1 file. [8.06s]

```
