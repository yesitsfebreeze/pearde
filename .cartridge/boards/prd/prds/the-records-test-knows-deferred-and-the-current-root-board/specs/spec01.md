---
complexity: small
footprint:
  - .cartridge/tests/records.test.ts
---

# spec01 — The state check fails an unknown state on a fixture record

Base: `prd.ctg` working tree, where `bun test ./.cartridge/tests/records.test.ts`
already exits 0 (2 pass, observed 2026-09-17) and the dirty edit already admits
`deferred` and retires the twelve `@ui/` ids by count and prefix.

What is missing is the second clause of the PRD's box 2: an unknown state
still fails the test. Today the state validation is a loop over the live
boards only, so a bogus state can never reach it without editing a real PRD.
Probed in place: adding `'bogus-state'` to the accepted list keeps the suite
green (2 pass), which is exactly the unfailable shape the PRD rejects.

## Acceptance

- [x] A fixture case in `records.test.ts` builds a synthetic record in a
      `mkdtemp` directory — a `boards/fixture/settings.md` with an absolute
      `repo` pointing at the real repository, and one `prds/bogus/prd.md`
      whose frontmatter carries `state: "bogus-state"` — and asserts the same
      accepted-states check that runs over the live boards fails it, so an
      unknown state cannot pass.
- [x] The same fixture asserts a `deferred` state on the synthetic record
      passes the check, so the fixture fails for the accepted list shrinking
      as well as for a new bogus state.

## Verify and Proof

Block 1 — the suite, including the new fixture case, and the two tests it must
still be running. No cargo; bun only, so no CARGO_TARGET_DIR is needed.

```sh
test -f .cartridge/tests/records.test.ts
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
bun test ./.cartridge/tests/records.test.ts > "$log" 2>&1 || { cat "$log"; exit 1; }
cat "$log"
if grep -Fq 'Ran 3 tests across 1 file' "$log" && grep -Fq '3 pass' "$log" && grep -Fq '0 fail' "$log"; then
  :
else
  echo "the suite did not run all three tests green"
  exit 1
fi
for named in \
  'central records retain explicit owners and a resolvable acyclic dependency graph' \
  'migration preserves original PRD fields, native states and historical review inputs' \
  'the accepted-states check fails an unknown state and passes deferred, on a fixture board'
do
  if grep -Fq "$named" .cartridge/tests/records.test.ts; then
    :
  else
    echo "the suite no longer declares $named"
    exit 1
  fi
done
if ! grep -q 'fixture' .cartridge/tests/records.test.ts; then
  echo "no fixture case in the test"
  exit 1
fi
```

Block 2 — the fixture is a denied world, not a decoration.

```sh
if grep -q 'bogus-state' .cartridge/tests/records.test.ts && \
   grep -q 'mkdtemp' .cartridge/tests/records.test.ts; then
  :
else
  echo "the unknown-state fixture case is missing"
  exit 1
fi
```

## Correction to block 1 (2026-09-17, coordinator cartridge-fa)

Block 1 originally grepped the log for underscored identifiers
(`central_records_retain_...`). `bun test` prints the test titles as written,
with spaces, so the block failed collection at
`the suite no longer runs central_records_retain_...` while the suite itself
was green at 3 pass / 0 fail. Two engine facts made the original shape
unworkable: `bun test` prints test titles with spaces rather than underscores,
and it prints a per-test line only for a failing test, so a passing test's name
never appears in the log at all. The block now reads the log for the run's own
census — `Ran 3 tests across 1 file`, `3 pass`, `0 fail` — and pins the three
titles in the test source instead, which is where a rename or a deletion would
actually show. The Acceptance above is unchanged.

## Denied worlds, built and run while preparing this spec

- M1: adding `'bogus-state'` to the accepted list — suite still green, exit 0.
  This is why the fixture case is required, and why its assertion must be
  against a synthetic record rather than the live boards.
- M1b: removing `'deferred'` from the accepted list — the first test fails
  with `Expected to contain: "deferred"`, observed exit 1. The `deferred`
  clause of box 2 is pinned by the live loop today.
- M2: removing the `retired` guard so every migrated id must exist again —
  the migration test fails at `records.test.ts:46` (`current.has(id)`
  expected true, received false), observed. Box 3's guard is pinned.

## Remaining work

Add the fixture case to `records.test.ts` on top of the dirty edit already in
the tree, changing no other file.

Done 2026-09-17 (coordinator cartridge-fa): the accepted-state list is hoisted
to a module-level `STATES` so the live loop and the fixture check the same
list, and the fixture case builds a synthetic board under `mkdtemp` and asserts
the check rejects `bogus-state` and accepts `deferred`. Observed: `bun test
./.cartridge/tests/records.test.ts` 3 pass / 0 fail, and denied world M1
re-run against the new shape (adding `'bogus-state'` to `STATES`) now fails the
fixture test, 2 pass / 1 fail, where before it was green.

The dirty edit already in the tree is collected with this PRD rather than left
for an owner to claim: it is the `deferred` state and the retired-`@ui/` guard
that boxes 1 and 3 of the PRD name, so it is this PRD's own work, and the file
is this PRD's whole footprint.
