---
complexity: 18
footprint:
  - resources/board/init.py
  - resources/board/transitions.py
  - resources/board/specs.py
  - resources/board/collect.py
  - references/parts/contract.md
  - references/parts/workers.md
---

# spec01 — `lane:` declares a read PRD, and `claim` honours it

A frontmatter key `lane: write` / `lane: read` (absent reads as `write`)
joins the contract. `pearde claim` (`transitions.cut_lane`) reads it: `read`
cuts no worktree and prints `claim: <rel> is \`lane: read\` — no worktree
cut`; anything else — absent or `write` — cuts the lane exactly as before.
`brief.repo_of` already falls back to the checkout when no lane dir is on
disk, so a `lane: read` brief names `<repo>` as the pre-lane path with no
further change there; `collect.land_lane` already returns `(None, None,
[])` on `not laneslib.exists(...)`, so `collect` merges nothing for a PRD
whose claim never cut a lane. The claim gate, `snapshot_claim` and `sweep`
run unconditionally in `transition`, before and independent of `cut_lane`,
so a read PRD still snapshots and still reclaims.

The analyst writes the key at spec time through `pearde specced --lane
write|read`, the same path `--blast` already takes: `specs.specced`
validates the value against `LANES = ("write", "read")`, refusing
anything else by name, and writes it to `prd.md` frontmatter on both the
dry and the real path. `collect.scores_of` reads an optional `lane:` line
out of a report's `## Scores` block and `collect.route_report`'s SPECCED
branch forwards it as `--lane <value>` — the same mechanism `blast-radius`
and `workflow` already use to reach `specced` from a worker's report
without the worker ever touching frontmatter by hand.

## What already stands

`transitions.cut_lane` cuts a lane unconditionally; `brief.repo_of` and
`collect.land_lane`'s no-lane fallbacks are already correct for a PRD that
never gets one — nothing there needs to change, only `cut_lane` gains the
check that skips the cut.

## Acceptance

- [x] `lane` is in `resources/board/init.py`'s `FRONTMATTER_KEYS`
- [x] `references/parts/contract.md` documents `lane` in the `prd.md` table
      and its default (`write`) in the defaults table
- [x] `transitions.cut_lane` cuts no worktree for a PRD whose frontmatter
      carries `lane: read`, and prints a line saying so instead
- [x] `transitions.cut_lane` still cuts a lane exactly as before when
      `lane` is absent, or set to anything other than `read`
- [x] `specs.py`'s `specced` command takes `--lane write|read`, refuses any
      other value by name, and writes the key to `prd.md` on both `--dry`
      and the real run
- [x] `collect.scores_of` returns an optional `lane` alongside `blast` and
      `workflow`, and `collect.route_report`'s SPECCED branch passes it to
      `specced` as `--lane <value>` when the report's `## Scores` block
      carries one
- [x] `python3 resources/claims.py check` (via `bad_keys`) reports no new
      problem from the `lane` row added to `contract.md`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 - <<'PY'
import os, sys, tempfile, subprocess
sys.path.insert(0, "resources")
sys.path.insert(0, "resources/board")
import transitions as trlib
import specs as specslib
import collect as collectlib

def repo(prd_body):
    D = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q"], cwd=D, check=True)
    subprocess.run(["git", "config", "user.email", "a@a.com"], cwd=D)
    subprocess.run(["git", "config", "user.name", "a"], cwd=D)
    open(os.path.join(D, "x.txt"), "w").write("x")
    subprocess.run(["git", "add", "."], cwd=D)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=D)
    os.makedirs(os.path.join(D, ".pearde", "prds", "p"))
    open(os.path.join(D, ".pearde", "prds", "p", "prd.md"), "w").write(prd_body)
    subprocess.run(["git", "add", "."], cwd=D)
    subprocess.run(["git", "commit", "-q", "-m", "prd"], cwd=D)
    return D, os.path.join(D, ".pearde")

# 1 — lane: read cuts no worktree
D, board = repo("---\nstate: open\nlane: read\n---\n\n# p\n\nx\n")
trlib.transition(board, "p", "analyzing", "engineer", worker="w1")
assert not os.path.isdir(os.path.join(board, ".lanes", "p")), "lane: read cut a worktree"

# 2 — absent lane: still cuts one, unchanged default
D, board = repo("---\nstate: open\n---\n\n# p\n\nx\n")
trlib.transition(board, "p", "analyzing", "engineer", worker="w1")
assert os.path.isdir(os.path.join(board, ".lanes", "p")), "default `write` stopped cutting a lane"

# 3 — specced --lane rejects a bad value by name
import io, contextlib
D, board = repo("---\nstate: analyzing\n---\n\n# p\n\nx\n")
err = io.StringIO()
with contextlib.redirect_stderr(err):
    code = specslib.COMMANDS["specced"](["p", "--board", board, "--lane", "bogus"])
assert code == 1 and "lane" in err.getvalue() and "bogus" in err.getvalue(), err.getvalue()

# 4 — collect.scores_of reads lane out of a ## Scores block
blast, lane, workflow = collectlib.scores_of(
    "Verdict: SPECCED\n\n## Scores\n\ncomplexity: 1\nblast-radius: low\nlane: read\n")
assert lane == "read"

print("spec01: ok")
PY
n=$(python3 resources/claims.py check . 2>&1 | grep -c "contract.md.*lane" || true)
test "$n" -eq 0
```
