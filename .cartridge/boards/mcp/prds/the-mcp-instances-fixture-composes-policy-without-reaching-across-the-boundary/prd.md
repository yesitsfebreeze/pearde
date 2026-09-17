---
state: "done"
origin: observed
priority: 80
repo: "/Users/feb/dev/cartridge/mcp.ctg"
capability-owner: mcp
footprint:
- ".cartridge/tests/integration/instances.test.ts"
commit: "5a7c54c58a26ac771e449d278d3b086fcbaa18a6"
---

# The mcp instances fixture composes policy without reaching across the boundary

## Outcome

`just isolation` passes for the whole composition again. `mcp.ctg` stops naming
`../policy.ctg` in any file, and its instances fixture still proves what it
proves today: two attached bridges, separate sessions, separate in-flight calls,
and exactly one active `mcp` node with exactly one `mcp.sock`.

## Evidence — this is a regression, and this board landed it

`just isolation` fails composition-wide, exit 1:

```
1 cross-cartridge reference(s). Fix each inside the cartridge that carries it:
declare the need, make it an event, or ship an own copy.
isolation composition FAIL
```

The one reference is `mcp.ctg/.cartridge/tests/integration/instances.test.ts:63`:

```js
for (const file of ['cartridge.json', 'init.lua'])
  fs.copyFileSync(path.join(runtime, '../policy.ctg', file), path.join(profile, 'policy', file));
```

`.cartridge/memos/system/isolation.md` forbids exactly this: a cartridge
"includes no sibling's crate, script, fixture or file", and the gate's second
check is "any file in the cartridge naming `../<sibling>.ctg`".

Traced with `git -C mcp.ctg log -S"'../policy.ctg'"`: the line entered at
`ec4de01` "Key every client's session and in-flight calls by attached instance",
which is the commit
`@root/one-daemon/.../mcp-keys-sessions-and-inflight-calls-by-attached-instance`
collected on 2026-09-17 at superproject `805efec`. `9db553e` then edited the
same file without touching that line.

It was not caught because nothing in that PRD's path runs the isolation gate:
its five Verify blocks do not, and its owner gates are `just check mcp`,
`just test mcp` and `just check cartridge`, none of which call it. Worse, the
spec **named the dependency in its own risk list** — "the composed block needs
`policy.ctg` beside `mcp.ctg`, because the fixture composes the real policy
cartridge from `../policy.ctg`" — and four review rounds read that sentence
without connecting it to the isolation rule that forbids it. The fact was
written down; the rule it broke was not the one anyone was looking for.

Found on 2026-09-17 by the implementer of `@root/.../web-ctg-exists-as-a-cartridge`,
which runs `just isolation` in its own Verify block and reported the failure as
pre-existing and outside its footprint. That is the correct handling and it is
why this is a separate PRD rather than a widened one.

## Acceptance

- [x] No file in `mcp.ctg` names `../policy.ctg` or any other `../<sibling>.ctg` path.
- [x] `just isolation` exits 0 for the whole composition, and `just audit` still passes for every cartridge.
- [x] `instances.test.ts` still proves what it proves today, with no assertion weakened: both bridges initialize, their sessions differ and stay their own across calls, a cross-instance cancel leaves the other's call alone, killing one leaves the other serving, and `status` lists exactly one `mcp` node in state `active` while the run directory holds exactly one pid directory with exactly one `mcp.sock`.
- [x] `just test mcp` exits 0, and the fixture's `expect()` census does not fall.

## Notes for whoever plans this

The isolation memo names three ways out: declare the need, make it an event, or
ship an own copy. The fixture needs a policy cartridge in its temp profile only
so the composed daemon has one to load. A minimal own copy written by the
fixture is likely the smallest fix, but do not assume it — read what the fixture
actually needs from `policy.ctg`'s `cartridge.json` and `init.lua` before
choosing, and check whether a policy-shaped stub changes what the test proves.

Do not weaken any assertion to make the gate pass. One of this fixture's
assertions was already unticked once on this board for resting on a check that
could not fail; it was rewritten and re-proved with three mutants. Keep it that
way.

## Evidence for the ticked boxes (2026-09-17, coordinator cartridge-24)

Fixed in the lane at `5a7c54c58a26ac771e449d278d3b086fcbaa18a6` (base
`9db553e`): one hunk, `@@ -59,8 +59,15 @@`, 9 insertions and 2 deletions, with
everything below byte-identical — the verifier re-checked that by extracting
`git archive 5a7c54c` and diffing against the lane file.

All three Verify blocks exit 0 in the lane, block 1 printing
`Isolation passed for 17 cartridges.` and block 2 at 1 pass with 13 `expect()`
calls. Against `repo` before the merge they read 1 / 0 / 1, which is the
unfixed `9db553e` printing the defect at line 63. The verifier did not leave
that as reasoning: it extracted the post-fast-forward tree into a scratch
composition root and ran all three there — 0 / 0 / 0. `just test mcp` exits 0
(22 passed, 0 failed, 1 ignored), `just audit mcp` exits 0, and I ran the full
`just audit` myself: 17 of 17 cartridges pass.

**No assertion is weakened.** The static `expect()` census is 11 before and
after and the runtime count is 13 both sides; `node.state === 'active'` is
intact with `toHaveLength(1)`; every named property is still asserted by name.

**The stub is strictly stronger than the sibling copy it replaces, measured in
both directions.** With `policy={default="allow"}` dropped from the composition,
the fixed tree FAILS (exit 1, 0 pass / 1 fail, "approval required for echo
read…") while the old tree composing the real `policy.ctg` — which declares
`"default": "allow"` itself — still PASSES, vacuously. So the fix does not merely
satisfy the isolation gate; it makes the composition's policy configuration
load-bearing where it previously was not.

Two things the review's non-blocking findings bought, both confirmed by the
verifier: F1's sibling-set assertion is what makes block 1 print 17 rather than
passing falsely at 16 — with `policy.ctg` dropped from the shadow and the
assertion removed, the UNFIXED tree passes at `Isolation passed for 16
cartridges.` F2's trap leaves nothing behind: zero shadow roots after five runs.

A trap worth carrying: a shadow root whose `.cartridge` is a SYMLINK measures
the live tree, because `memo-run` realpaths back to the live root — so such a
gate reports the defect against the FIXED lane. Block 1 uses a real
`.cartridge/memos/routine` directory with the memo copied in.

Hygiene: `/tmp/cartridge-501` held 229 entries before and after, so nothing fell
back to the shared runtime root; no daemon survived; the live project daemon
was untouched.
