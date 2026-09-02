---
complexity: 9
footprint:
  - references/parts/guard.md
---

# spec05 — guard.md, rewritten dense

1,879 words, the largest of the eleven, and the one carrying the most
measurements: 318,584 output tokens, 50,229 tokens of opening window, 32,000
and 7,073 and 8,000 thinking tokens, 7 ms on a 227-PRD master board, 0.05s
warm and 0.16s cold. Every number, every refusal string and the whole
`settings.json` block are facts, and the block is JSON a reader copies.

**Already standing.** Nothing; the analyst's build measured this file and
rewrote none of it. It fails `prose.py check` on 8 unbound waste words (`it`,
`that`, `there`). Mean sentence length is inside the limit.

**Left to finish.** The rewrite. 66% of the file is paragraph prose — the
lowest share of the four large parts, because the refusal table, the counter
table, the three-detail table and the JSON block are already structure. The
cut is in the argument around them. The fenced `json` block is copied by a
reader and changes not at all.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/guard.md` prints nothing and exits 0
- [x] the fact check prints nothing for `guard.md` against the lane's base commit and exits 0
- [x] `guard.md` holds fewer words at `prose.py stat` than at the base commit
- [x] the fenced `json` block is byte-identical to the one at the base commit
- [x] every measurement quoted at the base commit — 318,584, 50,229, 32,000, 7,073, 8,000, 7 ms, 227, 0.05s, 0.16s — is present afterwards
- [x] `git diff --name-status <base> -- references/parts/guard.md` prints exactly one row, beginning `M`
- [x] `python3 resources/index.py check` prints no line naming `guard.md`

## Verify and Proof

```sh
BASE=$(git merge-base HEAD main)   # fc75bcf at the lane cut
ROOT=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
PRD=$ROOT/.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-parts-reference-is-rewritten-dense/the-loop-parts-are-rewritten-dense
python3 resources/prose.py check references/parts/guard.md         # silent, exit 0
python3 "$PRD/probe/facts.py" "$BASE" references/parts/guard.md    # silent, exit 0
python3 resources/prose.py stat "$BASE" | grep 'parts/guard.md'
git diff --name-status "$BASE" -- references/parts/guard.md
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
case "$rc" in 0|1) ;; *) echo "index.py check crashed: $rc"; exit 1;; esac
if printf '%s\n' "$out" | grep 'parts/guard.md'; then exit 1; fi
for n in 318,584 50,229 32,000 7,073 8,000 '7 ms' 227 0.05s 0.16s; do
  grep -qF "$n" references/parts/guard.md || { echo "lost $n"; exit 1; }
done
json_was=$(git show "${BASE}:references/parts/guard.md" | awk '/^```json/{f=1} f{print} /^```$/{if(f&&++n)f=0}')
json_now=$(awk '/^```json/{f=1} f{print} /^```$/{if(f&&++n)f=0}' references/parts/guard.md)
[ -n "$json_was" ]                    # the block was there to compare
[ "$json_was" = "$json_now" ]         # and is byte-identical now
```
