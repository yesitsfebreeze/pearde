---
state: open
origin: derived
priority: 70
repo: "/Users/feb/dev/cartridge"
footprint:
  - ".cartridge/tests/integration/source-layout.test.ts"
---

# The source-layout test asserts a builtin path the repository no longer has

## Outcome

`just test layout` passes on a clean checkout, so a real layout regression is
visible again. The snapshot asserts the layout this repository actually has,
and every path it names exists.

## Acceptance

- [ ] `env -u CARTRIDGE_YOLO just test layout` exits 0 on a clean checkout.
- [ ] No assertion in `source-layout.test.ts` names a path absent from the
      repository. One check enumerates the paths the test asserts on and
      resolves each against the tree, so the next rename fails loudly instead
      of silently.
- [ ] The test still fails when the layout genuinely breaks. Prove it by
      execution against a tree where a submodule is moved or unlinked, not by
      reading the assertions.

## Evidence

Reported 2026-09-19 by cartridge-5c and confirmed here by reading the test and
the tree.

Line 57 is `expect(fs.realpathSync(path.join(checkout, 'builtin/memory'))).toBe(memory)`,
and it throws ENOENT. There is no `builtin/` directory in this repository, and
`git ls-files | grep -c '^builtin/'` returns 0. The neighbouring assertions use
`memory.ctg` and `cartridge.ctg` under the same `checkout` (lines 36 and 56),
which is where the memory submodule actually lives, so line 57 is the only
survivor of an older layout in which it was `builtin/memory`.

The failure predates `db88de4` ("Make every relative link in the record
resolve and test it"), which added two link tests to the same file. Both of
those pass and its diff touches no `builtin` line, so the collect that landed
it was correct and this is not a regression from it.

## Why this is worth a row rather than a one-line fix

A gate that is red for a stale reason stops being read. `just test layout`
cannot report a real layout regression while it fails on a path that was
renamed, and nobody can tell the difference without opening the file — which is
the same failure this board has now met three times in one day, in three
different instruments: a gate whose verdict depended on the shell that invoked
it, a gate that silently ran an extra check, and now a gate that fails for a
reason unrelated to what it measures.

So the fix is not only to correct line 57. The second acceptance box asks for
the paths to be enumerated and resolved, so that the next time the layout moves,
the test says which path is gone rather than throwing ENOENT from inside an
assertion.

## Coordination

The footprint is one file and does not overlap any lane currently held. Note
that `.cartridge/tests/integration/source-layout.test.ts` is also named in the
footprint of cartridge-5c's link-check child, which has already collected at
`db88de4`; confirm that row is done before claiming, rather than assuming.
