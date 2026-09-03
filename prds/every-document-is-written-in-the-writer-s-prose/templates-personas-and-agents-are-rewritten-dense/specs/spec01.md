---
complexity: 5
footprint:
  - references/agents
---

# spec01 — the three worker agent files are rewritten dense

`references/agents/pearde-analyst.md`, `pearde-implementer.md` and
`pearde-pass.md` carry the same facts in fewer words. Frontmatter is untouched:
`name`, `description` and `model` are read by the harness that dispatches the
worker, so a changed `description` changes dispatch.

Already standing, uncommitted in the lane: all three bodies rewritten, 1,015 →
951 words (6.3%), by `prose.py stat`, `prose.py check` green on the group. Left to finish: a
second pass over `pearde-pass.md`, whose 689 words hold the most prose in the
group and took the smallest cut (5.0%).

## Acceptance

- [x] `python3 resources/prose.py check references/agents/pearde-analyst.md references/agents/pearde-implementer.md references/agents/pearde-pass.md` exits 0.
- [x] The group's words, `prose.py`'s own count, fall from 1015 to **915 or fewer** — `prose.py stat <base>` summed over the group's lines. 9.9% off, and the check fails on the count itself.
- [x] The `name:`, `description:` and `model:` lines are byte-identical to the base revision — `git diff <base> -- references/agents | grep '^[-+]\(name\|description\|model\):'` prints nothing.
- [x] `pearde-analyst.md` and `pearde-implementer.md` still differ in exactly one word of body — the role noun — `diff <(sed s/analyst/W/g pearde-analyst.md) <(sed s/implementer/W/g pearde-implementer.md)` differs only in the frontmatter lines.
- [x] Every fact of the base text survives: the brief command with `--worker`, the report path, the one-line return holding verdict, path and numbers, the 15-line ceiling, and for `pearde-pass.md` the three numbered steps, the six stop conditions, the four verdicts as four table rows, and the dead-worker rule (`API Error`, one re-dispatch, then `BLOCKED`).
- [x] `python3 resources/index.py check` names no `@` in `references/agents/`.

## Verify and Proof

```sh
BASE=${BASE:-$(git merge-base HEAD main)}
set -e
AG="references/agents"
python3 resources/prose.py check $AG/pearde-analyst.md \
  $AG/pearde-implementer.md $AG/pearde-pass.md

# the dispatch keys are untouched
if git diff "$BASE" -- $AG | grep -qE '^[-+](name|description|model):'; then
  echo "a dispatch key changed"; exit 1
fi

# the four verdict rows survive as four rows
n=$(grep -c '^| `' $AG/pearde-pass.md)
[ "$n" = 4 ]

# the two worker files still differ in the role noun alone
diff <(sed 's/analyst/WORKER/g' $AG/pearde-analyst.md | grep -v '^name:\|^description:\|^model:') \
     <(sed 's/implementer/WORKER/g' $AG/pearde-implementer.md | grep -v '^name:\|^description:\|^model:')

if python3 resources/index.py check | grep -q '^references/agents/'; then
  echo "a dangling @ under references/agents/"; exit 1
fi
# the ceiling, on prose.py's own count
python3 resources/prose.py stat "$BASE" | grep '^references/agents/' \
  | awk -F'[ >]+' '{b+=$2; a+=$4} END {
      printf "group: %d -> %d (%.1f%% off)\n", b, a, 100*(b-a)/b;
      if (a > 915) { printf "over the %d ceiling\n", 915; exit 1 } }'
```
