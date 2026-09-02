---
complexity: 8
footprint:
  - references/parts/states.md
  - references/parts/pass.md
  - references/parts/dispatch.md
---

# spec02 — states, pass and dispatch, rewritten dense

The three mid-sized parts, 1,763 words at the base commit. `states.md` carries
the gate every command reads, `pass.md` the file a compacted session recovers
from, `dispatch.md` what crosses between passes — a paraphrased state name,
refusal string or key changes behaviour, so every one survives verbatim.

**Already standing.** Nothing; the analyst's build measured these three and
rewrote none of them. `states.md` fails on 2 unbound waste words, `pass.md` on
9, `dispatch.md` on 4; mean sentence length is already inside the limit on all
three (8.4, and 7.8 for `dispatch`).

**Left to finish.** The rewrite. The four hits in `dispatch.md` and two in
`states.md` are located in the analyst's report; each is a vague-subject `it
is` / `that is` / `there is`, rewritten to name its noun or dropped. Then the
judgement pass: rationale paragraphs become tables where the content is a fact
set, and every rule is stated once.

## Acceptance

- [x] `python3 resources/prose.py check` prints nothing for `states.md`, `pass.md` and `dispatch.md` and exits 0
- [x] the fact check prints nothing for the three files against the lane's base commit and exits 0
- [x] each of the three holds fewer words at `prose.py stat` than at the base commit
- [x] `git diff --name-status <base>` shows all three as `M` — none renamed, none deleted
- [x] every state name and every refusal string quoted in `states.md` at the base commit is present character-identical afterwards
- [x] `python3 resources/index.py check` prints no line naming any of the three

## Verify and Proof

```sh
BASE=$(git merge-base HEAD main)   # fc75bcf at the lane cut
ROOT=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
PRD=$ROOT/.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-parts-reference-is-rewritten-dense/the-loop-parts-are-rewritten-dense
F="references/parts/states.md references/parts/pass.md references/parts/dispatch.md"
python3 resources/prose.py check $F              # silent, exit 0
python3 "$PRD/probe/facts.py" "$BASE" $F         # silent, exit 0
python3 resources/prose.py stat "$BASE" | grep -E 'parts/(states|pass|dispatch)\.md'
git diff --name-status "$BASE" -- references/parts
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
case "$rc" in 0|1) ;; *) echo "index.py check crashed: $rc"; exit 1;; esac
if printf '%s\n' "$out" | grep -E 'parts/(states|pass|dispatch)\.md'; then exit 1; fi
python3 - "$BASE" <<'PY'
import re, subprocess, sys
base = sys.argv[1]
lost = 0
for name in ("states", "pass", "dispatch"):
    p = "references/parts/%s.md" % name
    was = subprocess.run(["git", "show", "%s:%s" % (base, p)],
                         capture_output=True, text=True).stdout
    now = open(p, encoding="utf-8").read()
    for span in sorted(set(re.findall(r"`([^`\n]+)`", was))):
        if "`%s`" % span not in now:
            print("%s: span not character-identical — %s" % (p, span))
            lost += 1
sys.exit(1 if lost else 0)
PY
```
