---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/prd.ctg"
work-kind: leaf
footprint:
- ".cartridge/tests/records.test.ts"
---

# The records test knows deferred and the current root board

## Outcome

`bun test ./.cartridge/tests/records.test.ts` (cwd `prd.ctg`) fails 2 of 2 at HEAD
(2026-09-16). The state list at line 16 omits `deferred`, which 176 PRDs use. The
migration test (line 38) still expects every one of the 182 migrated root ids to exist,
but PRDs were renamed, split and withdrawn after the migration. PROMPT.md names this test
as the gate for board edits, so it must describe the board as it is. Keep the history
check meaningful: withdrawn and renamed ids resolve through their `superseded-by` or
alias records, instead of the check being deleted.

## Acceptance

- [ ] `bun test ./.cartridge/tests/records.test.ts` (cwd `prd.ctg`) exits 0 against the live boards.
- [ ] `deferred` is an accepted state, and an unknown state still fails the test (a fixture case).
- [ ] Every migrated id either exists or resolves through a recorded alias or `superseded-by`, and an id that does neither fails the test.

## Proof and recovery

The test file changed last on 2026-09-13 (35e6786a). Found by the analyst of `@prd/the-engine-refuses-state-and-claim-changes-it-did-not-write`.
