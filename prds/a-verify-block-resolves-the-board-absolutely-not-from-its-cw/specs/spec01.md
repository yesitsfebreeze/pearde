---
complexity: 8
footprint:
  - resources/board/specs.py
---

# spec01 — `specced` refuses a verify block that hardcodes the board's own path

`collect` already runs a spec's `## Verify and Proof` block with `cwd` set
to the PRD's code repo — `repo_of` in `resources/board/collect.py`, a
walk-up that also substitutes a session's or a lane's own worktree when one
applies. That answer is already absolute and already right. Seventy-two
verify blocks on this board today open with a literal `cd
/Users/feb/dev/infra/pearde` anyway — a no-op when it happens to match, a
silent redirect to the wrong checkout when it does not (a session or a lane
worktree), and, per
`the-verify-guard-parses-git-s-own-output-before-it-trusts-it`'s own
acceptance list, "the one documented way to step outside the fence" —
`guarded_run` fences `cwd`, not what a script does after changing it.

This spec closes the gap at its source: `check_spec`
(`resources/board/specs.py`), the function `specced` already runs over
every `specs/*.md` before it will close a PRD, refuses a verify block that
`cd`s or `pushd`s to the literal absolute path `read_specs` already resolved
for that PRD (`plan.prd_repo`), or to a path under it. A block that `cd`s
anywhere else — a scratch directory, a relative path inside the footprint,
or nowhere at all — is untouched.

This is a source-side gate, not a retrofit: the seventy-two existing blocks
belong to other, mostly `done` PRDs and are out of this one's footprint —
recorded in this PRD's report as a finding, not rewritten here.

## Acceptance

- [x] `check_spec` takes the PRD's code repo (`plan.prd_repo`, computed once
      in `read_specs` and threaded through) and refuses a `## Verify and
      Proof` block whose fenced script `cd`s or `pushd`s to that repo's own
      absolute path, or to any path under it — file and line, the same
      shape `cannot fail` already refuses in. Confirmed in the lane: `git
      diff -- resources/board/specs.py` shows `check_spec(path, fm, text,
      lib, own_feet, repo=None)` and `read_specs` calling it with `repo`
      (`plan.prd_repo`, computed once). `probe_hardcoded_cd.py` cases 1-4
      (root, trailing slash, subpath, `pushd`) all refused with file/line:
      `ok   hardcoded repo root — refused -> [(15, "verify block 1 \`cd\`s
      to \`/Users/feb/dev/infra/pearde\` — ...")]` (and the three siblings,
      all `ok`).
- [x] A verify block that `cd`s to anywhere else — a relative path, an
      absolute scratch directory unrelated to the repo, or nothing at all —
      is not refused by this check. `probe_hardcoded_cd.py` cases 5-8 (no
      `cd`, relative `cd` under the footprint, scratch dir, a bare mention
      with no `cd`) all print `ok ... -> clean`.
- [x] `check_spec` called with no repo to check against (`repo=None`, the
      shape a caller with no PRD to resolve one from would pass) skips this
      check rather than raising. `probe_hardcoded_cd.py`'s dedicated case:
      `ok   repo=None — check skipped, not raised -> clean`. Full run: `9
      passed, 0 failed`.
- [x] The two existing harnesses that already exercise `check_spec` directly
      — `an-acceptance-box-that-cannot-fail-is-refused` and
      `an-analyst-workflow-does-not-survive-into-specced` — still pass
      unchanged, run with `PEARDE_ROOT` at this PRD's own lane.
      `PEARDE_ROOT="<lane>" bash .pearde/prds/an-acceptance-box-that-cannot-fail-is-refused/probe/verify.sh`
      → `verify: 2 passed, 0 failed`. `PEARDE_ROOT="<lane>" bash
      .pearde/prds/an-analyst-workflow-does-not-survive-into-specced/probe/verify.sh`
      → `verify: 21/21 checks pass`.

## Verify and Proof

```sh
# exercises check_spec in resources/board/specs.py
python3 .pearde/prds/a-verify-block-resolves-the-board-absolutely-not-from-its-cw/probe/probe_hardcoded_cd.py
```
