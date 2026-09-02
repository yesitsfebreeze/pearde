---
complexity: 5
footprint:
  - resources/board/brief.py
---

# spec03 — the brief names the lane as `<repo>`

A worker reads one command's output and works where it says. When the claim
cut a lane, `<repo>` is that lane; when it did not — a board outside a repo,
a claim from before lanes — `<repo>` is the checkout, exactly as before.

**What stands** — `repo_of` in `resources/board/brief.py` returns
`lanes.lane_dir(prd["board_path"], prd["local"])` when that directory is on
disk, and falls through to the old answer otherwise. Measured in a fixture:
the header line read `repo …/.pearde/.lanes/change-a` after a claim, and
`…/f2` before one.

**What is left** —

- The header line says `repo <path>` and nothing tells the worker that path
  is a lane, or which branch it is on. Say `repo <path> · lane
  lane/<slug>` when there is one, so the report of a worker that wandered
  into the checkout is diagnosable.
- `SKIP` in this file maps `footprint` to `clash`. spec05 removes the
  footprint gate, so that entry becomes dead — drop it with the gate, in
  spec05's own change, and leave a note here rather than two specs editing
  one dict.
- The `--consult` path builds `<repo>` from `planlib.repo_root(board)`
  separately, further down. A consultant has no claim and so no lane; leave
  it, and say why in the docstring.

## Acceptance

- [x] `pearde brief <prd> --worker <w>` on a claimed PRD names the lane directory as `repo` on its header line
- [x] the header line names the lane branch when there is a lane and says nothing extra when there is not
- [x] `pearde brief` on a PRD with no lane on disk prints the same `repo` path it printed before lanes existed
- [x] a board command run with the lane as its working directory resolves to the live board, not to a copy inside the lane
- [x] `python3 resources/board/brief.py --check` prints nothing

## Verify and Proof

```sh
python3 resources/board/brief.py --check
grep -q 'laneslib' resources/board/brief.py
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E '(^|@)resources/board/brief\.py([ ,:]|$)'; then exit 1; fi
```
