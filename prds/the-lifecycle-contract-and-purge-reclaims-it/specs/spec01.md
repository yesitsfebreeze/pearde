---
complexity: 14
footprint:
  - resources/board/purge.py
---

# spec01 — `purge.py`: the reclaim over the five leftovers, read-only until `--apply`

The verb the contract's page argues for: one scan over stale lanes, dead
session trees, unregistered tmp boards, `/tmp/pearde-*` probe fixtures past
a day, and reaped refs past the cap — each read through the existing reader
(`plan.claim_of`, `session.liveness`, `session.read_ledger`), never a second
one. `run()` prints the scan with no flag; `--apply` removes every
candidate through the same remover the sweep and the reaper already run
(`lanes.remove`, `session.cmd_reap`, `git update-ref -d`) and a second run
lists nothing. `--json` prints the same scan as one document. The refuse
rule is load-bearing: a lane whose PRD holds a claim, a board whose ledger
answers alive or unknown, and a board the daemon registers (`serve.json`)
are never candidates whatever their age.

What already stands (built ahead of this pass, uncommitted, in the
checkout this lane was cut from — reproduced and probed fresh in this
lane): `resources/board/purge.py` whole — `stale_lanes`, `dead_sessions`,
`tmp_boards`, `probe_fixtures`, `reaped_refs`, `scan`, `run`, `cmd_purge`,
`cmd_json`, routed by `pearde.py`'s own discovery (`COMMANDS = {"purge":
cmd_purge}`, no edit to that file).

What this pass found and fixed, against the copy that was already
standing: two real defects, neither in the acceptance boxes as originally
measured because the run that measured them never exercised `--reap-cap`
or `--apply --json` together.

- `scan()` computed the reaped-ref candidates against `cap_of(board)` (the
  settings.md default) unconditionally; `run()`'s `--reap-cap` override
  only relabelled the printed cap, so `--apply --reap-cap 3` still dropped
  refs down to 8, not 3. `scan()` now takes `reap_cap=` and both `run()`
  and `cmd_json()` pass their override through it, so the rows a scan lists
  as over the cap are the rows an apply at the same flag actually drops.
- `cmd_json()` never called the removal path at all — `pearde purge --apply
  --json` printed `"applied": true` and removed nothing. The apply loop is
  now `_apply(board, rows)`, one function `run()` and `cmd_json()` both
  call, so `--json` alongside `--apply` does what a bare `--apply` does,
  and each JSON action row carries a `"did"` field naming what happened to
  it.

## Acceptance

- [x] A lane whose PRD holds a claim is never a candidate; one whose PRD
  holds none is, and `--apply` removes its worktree, keeps its branch, and
  the follow-up scan lists no lane
  - proof `probe/probe.py` case `[A]`: `ok held-prd's lane is not a candidate` · `ok dropped-prd's lane is the candidate` · `ok dropped lane's worktree is gone` · `ok held lane's worktree survives` · `ok the branch is kept, only the worktree drops` · `ok the follow-up scan lists no lane`
- [x] A dead session-ledger row is the only session candidate; the running
  session's own row is never one, whatever its liveness verdict says about
  a third row
  - proof `probe/probe.py` case `[A2]`: `ok exactly the dead row is reapable` · `ok the running session is never a candidate`
- [x] A probe fixture an hour old survives; one 25 hours old is removed —
  a plain directory, a dangling symlink (by its own `lstat`, never its
  gone target) and a stale scratch file all three
  - proof `probe/probe.py` case `[B]`: `ok an hour-fresh fixture survives` · `ok a 25h-old dir is a candidate` · `ok a dangling symlink is a candidate` · `ok a stale scratch file is a candidate`
- [x] Reaped refs past `reap-cap` (default 8) are candidates, oldest first,
  newest kept; `--reap-cap` overrides the default for one run and the
  override is what actually gets dropped
  - proof `probe/probe.py` case `[C]`: `ok default cap is 8` · `ok exactly 2 refs are over the cap` · `ok the oldest two are the candidates` · `ok a --reap-cap of 3 keeps only 3` — this box FAILED before the `scan(reap_cap=)` fix (`got: 8, want: 3`); see `## Findings` in the report
- [x] `--json` prints the same scan as one document, and `--apply --json`
  removes exactly what a bare `--apply` removes rather than only
  describing it
  - proof `probe/probe.py` cases `[D]`/`[D2]`: `ok json reap_cap defaults to 8` · `ok json is not applied on a bare run` · `ok json says applied` · `ok the lane is actually gone, not only reported` · `ok the action row names what happened` — the D2 box FAILED before the `_apply` refactor (the lane survived a `--apply --json` run); see `## Findings` in the report
- [x] With no candidates, `purge` prints `nothing to reclaim · <n> reaped
  ref(s) under the cap of <cap>` and exits 0
  - proof: the follow-up run in case `[A]` and `[C]` both hit the empty-scan branch; `run()`'s `if not rows:` line is exercised by the second `purge` call after `--apply` in `verify.sh`'s own smoke run

## Verify and Proof

```sh
LANE="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"
python3 -c "import ast; ast.parse(open('$LANE/resources/board/purge.py').read())"
python3 /Users/feb/dev/infra/pearde/.pearde/prds/the-lifecycle-contract-and-purge-reclaims-it/probe/probe.py "$LANE"
PEARDE_ROOT="$LANE" bash /Users/feb/dev/infra/pearde/.pearde/prds/the-lifecycle-contract-and-purge-reclaims-it/probe/verify.sh
python3 "$LANE/resources/pearde.py" purge --json /Users/feb/dev/infra/pearde/.pearde | python3 -c "import json,sys; json.load(sys.stdin)"
```
