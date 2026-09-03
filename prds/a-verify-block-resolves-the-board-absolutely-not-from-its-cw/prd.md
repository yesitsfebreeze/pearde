---
state: done
origin: requested
priority: 92
complexity: 8
blast-radius: low
workflow: probe-then-spec
---

# a verify block resolves the board absolutely not from its cwd

<The request, for an analyst who knows the codebase but not this conversation:
what exists at the end and why, what must not change, pointers to files and
prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Blocked

**2026-09-03 16:47 — the lane will not rebase**

`lane/a-verify-block-resolves-the-board-absolutely-not-from-its-cw` does not land on `session/s98669`; 1 file(s) disagree:

- `resources/board/ramp.py`

Nothing is lost: the worker's commits are on `lane/a-verify-block-resolves-the-board-absolutely-not-from-its-cw` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock a-verify-block-resolves-the-board-absolutely-not-from-its-cw`.

## Report

spec01: exit 0
ok   hardcoded repo root — refused -> [(15, "verify block 1 `cd`s to `/Users/feb/dev/infra/pearde` — collect already runs this block there; naming it again pins the check to one checkout and is the documented way past guarded_run's cwd fence")]
ok   hardcoded repo root, trailing slash — refused -> [(15, "verify block 1 `cd`s to `/Users/feb/dev/infra/pearde/` — collect already runs this block there; naming it again pins the check to one checkout and is the documented way past guarded_run's cwd fence")]
ok   hardcoded repo subpath — refused -> [(15, "verify block 1 `cd`s to `/Users/feb/dev/infra/pearde/resources` — collect already runs this block there; naming it again pins the check to one checkout and is the documented way past guarded_run's cwd fence")]
ok   pushd the repo root — refused -> [(15, "verify block 1 `cd`s to `/Users/feb/dev/infra/pearde` — collect already runs this block there; naming it again pins the check to one checkout and is the documented way past guarded_run's cwd fence")]
ok   no cd at all — untouched -> clean
ok   relative cd under the footprint — untouched -> clean
ok   absolute cd to a scratch dir — untouched -> clean
ok   a path merely mentioning the repo, no cd — untouched -> clean
ok   repo=None — check skipped, not raised -> clean
9 passed, 0 failed
