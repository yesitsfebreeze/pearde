---
commit: 422c521aed170a4d098505c73469a1a59dccf49d
spec-digests: {"spec01.md":"8af1d8251451756c2484014008197ab21262db5d5ea49a13c62feaecefd8a45c"}
child-contracts: {".cartridge/boards/landscape/prds/improve-memo-compact-landscape/bounded-inventory-snapshot/prd.md":"14bd317af867ac71141e1dec1fd0dfad2633af33d26009367e9dd857f39dc41d"}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/landscape/prds/improve-memo-compact-landscape/specs/spec01.md: exit 0

Command SHA-256: 247aacf56c40821b7582d8f322c9140520fa3121e200958413687f00a1a11fc9

```text
bun test v1.3.14 (0d9b296a)

../memo.ctg/.cartridge/tests/integration/inventory.test.ts:
{"paths":10000,"summary_bytes":393,"max_page_bytes":11731,"snapshot_calls":3}
(pass) native compact snapshot pages 10000 paths exactly with one discovery and no hidden writes [10337.29ms]
(pass) cache replacement follows newest-started request and failed refresh preserves published snapshot [530.66ms]
(pass) restart, invalid inputs and partial sources are explicit while legacy landscape remains accepted [143.38ms]

 3 pass
 0 fail
 10183 expect() calls
Ran 3 tests across 1 file. [11.03s]

```
