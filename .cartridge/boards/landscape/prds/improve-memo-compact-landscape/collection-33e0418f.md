---
commit: 33e0418fa82966772c38ec8191d02a158b2cb56d
spec-digests: {"spec01.md":"51270eafe95be02087793f897974fe8df28e2efc32ca444ae13f63e106fa60bb"}
child-contracts: {".cartridge/boards/landscape/prds/improve-memo-compact-landscape/bounded-inventory-snapshot/prd.md":"50cd49468c483d094971274dabcf77b5904b7d271a15735de6b5afda3641cee8"}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/landscape/prds/improve-memo-compact-landscape/specs/spec01.md: exit 0

Command SHA-256: 99892ce5f711595f1d2732cc25c1a4ccc47179fd1f407f443c3d86bf74e341c8

```text
bun test v1.3.14 (0d9b296a)

../memo.ctg/.cartridge/tests/integration/inventory.test.ts:
{"paths":10000,"summary_bytes":393,"max_page_bytes":11731,"snapshot_calls":3}
(pass) native compact snapshot pages 10000 paths exactly with one discovery and no hidden writes [9175.02ms]
(pass) cache replacement follows newest-started request and failed refresh preserves published snapshot [425.98ms]
(pass) restart, invalid inputs and partial sources are explicit while legacy landscape remains accepted [70.60ms]

 3 pass
 0 fail
 10183 expect() calls
Ran 3 tests across 1 file. [9.68s]

```
