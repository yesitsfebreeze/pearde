---
complexity: 9
footprint:
  - resources/board/collect.py
  - references/parts/commits.md
---

# spec03 — a claim taken before the fix says so, and the harness is on the board

spec01 changes what `snapshot` writes, not what is already written. Every
`.claims/<prd>/` dir on this machine — twenty of them — was recorded by the
one-repo `snapshot` and holds no code side. For those, `side(repo)` is `None`,
the splitter cannot run, and the collect refuses. The refusal is the safe
direction, and it is right that it refuses rather than sweeps; but the message
reads "these edits are unattributable" when the truth is "this claim cannot
tell", and the person cannot act on it. That is the half of the PRD's decision
that is about *saying why*, not about splitting.

The other half of this unit is that pass one's probe is a loose script the
board never runs. `doctor --harnesses` sweeps `verify.sh` under the board, so
the probe has to be one to count.

**What already stands**: the refusal appends the stale-claim clause — which
root the baseline never covered, and `pearde collect --snapshot <prd>` on a
clean tree as the way out — with probe scenario 6 holding it, driven from a
claim dir aged back to the one-repo shape.

**What is left**: rename `probe/run.sh` to `probe/verify.sh` so the board's
harness sweep runs it (keep the scenario-selection argument; the sweep passes
none); and give `references/parts/commits.md` a line saying the baseline
records both repos and that a claim older than that cannot split.

## Acceptance

- [x] A claim dir with no `repo` side, on a board whose code repo is not its board repo, refuses with a message naming the uncovered root and the re-snapshot command
- [x] The same claim dir commits nothing and leaves the sibling's line in the tree
- [x] A claim dir that does hold a `repo` side never shows that clause
- [x] `.pearde/prds/collect-stages-a-shared-file-whole/probe/verify.sh` exists and exits 0 with none failing — the tally is parsed, so a check added to it never reddens this unit
- [x] Running it with no argument runs every scenario, and with `1 2` runs only those two
- [x] `references/parts/commits.md` says the claim record covers the board's repo and the code repo

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
V=.pearde/prds/collect-stages-a-shared-file-whole/probe/verify.sh
{ bash "$V" > /tmp/s03.out 2>&1 || true; }
tail -3 /tmp/s03.out
{ bash "$V" 1 2 > /tmp/s03b.out 2>&1 || true; }
{ N=$(grep -c '^PASS\|^FAIL' /tmp/s03b.out) || true; }
echo "selected run made $N checks"
# this unit's own tally is parsed, never pinned: a check folded into the
# probe must be able to be added without reddening the spec that names it
{ T=$(grep -oE '[0-9]+ passed, [0-9]+ failed' /tmp/s03.out | tail -1) || true; }
printf 'probe tally: %s\n' "$T"
printf '%s\n' "$T" | awk '{ if (NF != 4 || $1 + 0 < 1 || $3 != 0) exit 1 }'
grep -q 'recorded before the baseline covered' resources/board/collect.py
[ "$(grep -c 'the code repo' references/parts/commits.md)" -ge 1 ]
```
