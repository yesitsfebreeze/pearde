---
complexity: 5
footprint:
  - .pearde/prds/the-kb-survives-a-lane/probe/verify.sh
---

# spec01 — the KB-survives-a-lane contract, asserted with a check that can fail

What the PRD's "Why now" describes — a lane's `remember`/`conclude` writing
into a tree that never reaches the board — is not the current state of the
tool. Two earlier fixes already closed it: `knowledge.py`'s `default_root`
resolves the wiki by climbing from the cwd to the board above it
(`common.board_above`), the same rule every other board reader uses, rather
than resolving beside its own script copy; and `lanes.py` `create` excludes
the board directory from a lane's own checkout with a `--no-cone`
sparse-checkout, so a lane never materialises a phantom copy of `.pearde` to
climb into by mistake. A worker's own worktree sits at `<board>/.lanes/<slug>`
— physically inside the live board, not a copy of it — so a lane's `remember`
or `conclude` lands in the same `wiki/sources/` or `wiki/conclusions/` the
board's own session writes, immediately, with no collect and no reroute
required to make it visible. `wiki/` is also not on `resources/board/shared.py`'s
candidate list, so there is nothing for `share apply`/`share undo` to seed or
restore — it was never duplicated per lane in the first place.

What already stands: everything above, proven by `probe/verify.sh`, which
this spec's only job is to land as a permanent regression check — the same
kind of silent regression already happened once (see the report's finding on
`260902-2085`), and this PRD's contract is exactly the set of properties that
must not regress again.

What is left: commit `probe/verify.sh` at the footprint path above, unchanged
from what pass one built. No source file changes — the underlying mechanism
already does what the PRD asks.

## Acceptance

- [x] a `remember` run from a lane-shaped cwd (`<board>/.lanes/<slug>`, no
      `--root`) lands under that board's `wiki/sources/`, verified without a
      collect step because the lane and the board share one physical `wiki/`
- [x] the same `remember` run with cwd at the board itself writes the
      identical layout — no lane, no rerouting, byte-for-byte the same code
      path
- [x] `resources/board/shared.py` names no `wiki` candidate, so `share apply`
      finds nothing of the KB's to seed and `share undo` nothing of it to
      restore
- [x] two `conclude` calls racing the same title do not both report success
      and do not silently merge — exactly one writes, the other refuses

## Verify and Proof

```sh
bash .pearde/prds/the-kb-survives-a-lane/probe/verify.sh
```
