---
complexity: 4
footprint:
  - resources/board/collect.py
---

# spec01 — collect removes the claim dir at every terminal it writes

`collect.close_claims(board, rel)` (`shutil.rmtree(claims_dir(board, rel),
ignore_errors=True)`) is called at each of the four points `collect.py`
writes a PRD out of `claimed` into a terminal state, right after that
transition's own commit (if any) has landed:

- `collect_one`'s `done` path — after `transition_row(..., "done", ...)`,
  once the lane has merged and every commit (footprint, record, `commit:`)
  is on the branch.
- `collect_one`'s red-gate `failed` path (`--fail`) — after
  `transition_row(..., "failed", ...)`. This path writes `prd.md` directly
  and makes no commit of its own, so the removal follows the write, not a
  commit.
- `block_conflict`'s `blocked` path (a lane conflict) — after
  `transition_row(..., "blocked", ...)`, same reasoning: no commit here
  either, `prd.md` is written straight to disk.
- `close_container`'s `done` path (a parent whose children all landed) —
  after its own `transition_row(..., "done", ...)`, once the container's
  record commit has landed.

This is already built, on `lane/a-collect-closes-the-claim-dir-it-measured-against`
(uncommitted probe left at `prds/<this>/probe/verify.py`, gitignored).

What is **not** touched, per the contract's "must not change": `.claims/riders`
(`owe`/`owed`/`settle`), `snapshot`'s two-repo record, and `release`/`sweep`
(`transitions.py`) — neither calls `close_claims`, so a parked or swept
PRD's claim dir stands untouched, exactly as before; a re-claim after either
still finds no stale baseline.

## Acceptance

- [x] `collect_one` closing a claimed PRD to `done` removes
      `.claims/<rel>/` after the commits land.
- [x] `collect_one`'s `--fail` red-gate path to `failed` removes
      `.claims/<rel>/`.
- [x] `block_conflict`'s path to `blocked` removes `.claims/<rel>/`.
- [x] `close_container`'s `done` path removes `.claims/<rel>/`.
- [x] `--dry` removes nothing (every call site is already gated behind the
      real-write branch; no new `dry` check was needed).
- [x] `release` and `sweep` (`transitions.py`) still never touch
      `.claims/<rel>/` — no call was added there.

## Verify and Proof

```sh
# cwd is the code repo root — the cwd `collect` runs a verify block in
python3 .pearde/prds/a-collect-closes-the-claim-dir-it-measured-against/probe/verify.py
```
