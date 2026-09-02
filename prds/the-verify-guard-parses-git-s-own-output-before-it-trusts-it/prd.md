---
state: done
origin: requested
priority: 0
complexity: 26
blast-radius: high
workflow: probe-then-spec
actual: 0.79h
commit: 483cdcf
---

# the verify guard parses git s own output before it trusts it

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Contract

`a-verify-block-must-not-destroy-the-checkout-it-runs-in` reached `done` at
`6ea9c20`, landing `guarded_run` and its helpers — `_dirty`, `_park`, `_heal`,
`_head_of`, `_restore_head`, `owned_by`, `_owned_files`, `_blobs`,
`_snapshot`, `_unerase` — into `resources/board/collect.py`, +288/−2. The
mechanism is sound. The parsing is not, and the guard as landed destroys
other sessions' work, so `8bbb4c1` reverted the code out of `collect.py`
while leaving that PRD `done`. Its full evidence is in that PRD's
`## Failure`.

This PRD re-lands the same guard with the parsing fixed. **The design is not
reopened** — the ordering inside `guarded_run` was checked and is correct
(`_park` pathspec-limited so it cannot disturb the snapshot's subjects;
snapshot after park; `_restore_head` before `_heal`; `_unerase` after `_heal`
and before the stash pop), and all 22 acceptance boxes and 24 harness checks
passed on the merged tree. Recover the code from `6ea9c20`, do not rewrite it.

## Acceptance

- `_dirty` reads `git status --porcelain -z` (which never quotes) or sets
  `-c core.quotePath=false`, and a path containing a space is classified,
  parked, healed and unerased identically to one without. A spaced-path case
  is in `probe_unit`.
- A foreign **untracked** file created inside the verify window survives the
  guard. `_heal` moves such a path aside rather than `git clean -f -d`-ing it,
  and a probe demonstrates the file present afterwards with its bytes intact.
- `_heal` checks the returncode of every git call it makes, and the
  `put back:` line names only paths actually restored. A failed restore says
  so.
- A foreign **staged** index entry is not wiped — `_heal`'s `git reset -q
  HEAD --` must not discard a peer's staging.
- `spec02`'s destructive-block claim is honest: either its wording narrows to
  "a block that **deletes**", or `git reset --hard HEAD` on the laneless path
  is caught and the pre-block bytes restored rather than the reverted content
  committed silently. Today it commits the revert, writes `done`, and prints
  nothing.
- `_owned_files` handles a footprint **symlink** — this repo's `.pearde` is
  one — or the limitation is written down and tested as a known gap.
- The two verify blocks drop the hardcoded `cd /Users/feb/dev/infra/pearde`.
  `collect` already runs a spec block in `repo`, so it is a no-op that pins
  the machine and is the one documented way to step outside the fence.
- `probe/verify.sh` is green on the **merged** tree, not the lane's base, and
  the run is made with `PEARDE_ROOT` at the merge rather than at a stale lane.

## Report

spec01: exit 0
collect.py parses
1
1849:            code, output = guarded_run(["bash", "-e", "-o", "pipefail"],
A. reproduced at 8bbb4c150bd6bab861a06668a6149aaf4790672d: a GREEN verify block destroys the checkout
  ok   A1 the old collect exits 0 — the block never failed
  ok   A1 ...and the PRD is done
  ok   A1 the neighbour's uncommitted work is GONE
B. the same block, guarded: the checkout it did not own is untouched
  ok   B1 collect exits 0
  ok   B1 the PRD reaches done
  ok   B1 the neighbour's uncommitted work survives
  ok   B1 no stash is left behind
C. the board is its own repo: the block still sees the change under test
  ok   C1 collect exits 0 — the footprint was NOT parked
  ok   C1 the PRD reaches done
  ok   C1 the neighbour's uncommitted work survives
C. this repo's own roots: the footprint groups under the code repo
  ok   C2 this board's repo and board root really are two paths
  ok   C2 ...and the footprint groups under the code repo, unrebased
E. laneless: a green block deletes the PRD's own uncommitted footprint
  ok   E1 collect exits 0
  ok   E1 the PRD reaches done
  ok   E1 collect names the path it put back, on its own line
  ok   E1 the uncommitted footprint is back on disk, not deleted
  ok   E1 ...and it is the helper that got COMMITTED, not the deletion
  ok   E1 the neighbour's uncommitted work survives
E. the same fixture on spec01's collect: the deletion is what lands
  ok   E2 spec01's collect exits 0 — the block never failed
  ok   E2 ...and the PRD is done
  ok   E2 the work under test is GONE from the checkout
  ok   E2 ...and the deletion is what got committed
F. laneless: a block that REVERTS the work under test to HEAD
  ok   F1 collect exits 0
  ok   F1 the PRD reaches done
  ok   F1 collect names the path it put back
  ok   F1 the work under test is on disk, not HEAD's bytes
  ok   F1 ...and the helper is what got COMMITTED, not the revert
F. the same fixture on pass one's collect (6ea9c204f94d746e4d186817dcf88399d47c4ee9): the revert lands
  ok   F2 pass one's collect exits 0 — the block never failed
  ok   F2 ...and the PRD is done
  ok   F2 the work under test is reverted on disk
  ok   F2 ...and the revert is what got COMMITTED, silently
F. a peer's new file, written inside the verify window
  ok   F3 collect exits 0
  ok   F3 the peer's file is not deleted — it is aside, with its bytes
  ok   F3 collect says where it put it
  ok   F3 the neighbour's uncommitted work survives
F. the same block on pass one's collect: the peer's file is destroyed
  ok   F4 pass one's collect exits 0
  ok   F4 the peer's new file is GONE
  ok   F4 ...while the output named it as put back
F. a foreign path git would have quoted
  ok   F5 collect exits 0
  ok   F5 the PRD reaches done
  ok   F5 the spaced foreign path survives, bytes intact
  ok   F5 no stash is left behind
F. the same fixture on pass one's collect: the quoting runs it unguarded
  ok   F6 pass one could not park it — it says so
  ok   F6 ...and the neighbour's uncommitted work went with the block
D. the unit probes
  ok   D probe_unit
  ok   D probe_roots

46 passed, 0 failed

spec02: exit 0
collect.py parses
no git clean left in the healing
no blanket index reset left
PASS: unguarded, the block really does empty the checkout
PASS: foreign dirt survives a block that empties the checkout
PASS: own footprint left exactly as the block leaves it
PASS: `git reset --hard` + `git clean -fdx` undone, foreign dirt intact
PASS: nothing foreign — no stash left behind
PASS: git reads inside the block see the real tree
PASS: without the snapshot the block loses the work under test
PASS: a deleted owned file comes back, bytes and mode, both branches
PASS: an owned file the block MODIFIES stays modified
PASS: an owned file the block CREATES stays created
PASS: a deletion the worker made before the block stays deleted
PASS: a directory footprint: a file deleted from inside comes back
PASS: every restored path is named on collect's own output line
PASS: a path with a space is classified, parked, healed and unerased
PASS: a rename is one row naming its destination, not two shifted ones
PASS: a peer's new file is moved aside, not deleted
PASS: `put back:` names only what was actually put back
PASS: a restore that fails says so
PASS: a peer's staged entry is not wiped
PASS: a block that reverts owned work to HEAD is undone
PASS: an ordinary modification by the block still stays
PASS: a footprint symlink comes back, target and all
PASS: a dangling footprint symlink is snapshotted and restored
PASS: the caller's cwd survives the park that emptied it
ALL PASS
A. reproduced at 8bbb4c150bd6bab861a06668a6149aaf4790672d: a GREEN verify block destroys the checkout
  ok   A1 the old collect exits 0 — the block never failed
  ok   A1 ...and the PRD is done
  ok   A1 the neighbour's uncommitted work is GONE
B. the same block, guarded: the checkout it did not own is untouched
  ok   B1 collect exits 0
  ok   B1 the PRD reaches done
  ok   B1 the neighbour's uncommitted work survives
  ok   B1 no stash is left behind
C. the board is its own repo: the block still sees the change under test
  ok   C1 collect exits 0 — the footprint was NOT parked
  ok   C1 the PRD reaches done
  ok   C1 the neighbour's uncommitted work survives
C. this repo's own roots: the footprint groups under the code repo
  ok   C2 this board's repo and board root really are two paths
  ok   C2 ...and the footprint groups under the code repo, unrebased
E. laneless: a green block deletes the PRD's own uncommitted footprint
  ok   E1 collect exits 0
  ok   E1 the PRD reaches done
  ok   E1 collect names the path it put back, on its own line
  ok   E1 the uncommitted footprint is back on disk, not deleted
  ok   E1 ...and it is the helper that got COMMITTED, not the deletion
  ok   E1 the neighbour's uncommitted work survives
E. the same fixture on spec01's collect: the deletion is what lands
  ok   E2 spec01's collect exits 0 — the block never failed
  ok   E2 ...and the PRD is done
  ok   E2 the work under test is GONE from the checkout
  ok   E2 ...and the deletion is what got committed
F. laneless: a block that REVERTS the work under test to HEAD
  ok   F1 collect exits 0
  ok   F1 the PRD reaches done
  ok   F1 collect names the path it put back
  ok   F1 the work under test is on disk, not HEAD's bytes
  ok   F1 ...and the helper is what got COMMITTED, not the revert
F. the same fixture on pass one's collect (6ea9c204f94d746e4d186817dcf88399d47c4ee9): the revert lands
  ok   F2 pass one's collect exits 0 — the block never failed
  ok   F2 ...and the PRD is done
  ok   F2 the work under test is reverted on disk
  ok   F2 ...and the revert is what got COMMITTED, silently
F. a peer's new file, written inside the verify window
  ok   F3 collect exits 0
  ok   F3 the peer's file is not deleted — it is aside, with its bytes
  ok   F3 collect says where it put it
  ok   F3 the neighbour's uncommitted work survives
F. the same block on pass one's collect: the peer's file is destroyed
  ok   F4 pass one's collect exits 0
  ok   F4 the peer's new file is GONE
  ok   F4 ...while the output named it as put back
F. a foreign path git would have quoted
  ok   F5 collect exits 0
  ok   F5 the PRD reaches done
  ok   F5 the spaced foreign path survives, bytes intact
  ok   F5 no stash is left behind
F. the same fixture on pass one's collect: the quoting runs it unguarded
  ok   F6 pass one could not park it — it says so
  ok   F6 ...and the neighbour's uncommitted work went with the block
D. the unit probes
  ok   D probe_unit
  ok   D probe_roots

46 passed, 0 failed
