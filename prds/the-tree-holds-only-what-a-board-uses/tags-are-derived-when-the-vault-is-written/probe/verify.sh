#!/usr/bin/env bash
# The probe's own gate — run from the repo root, board at .pearde/:
#
#     bash .pearde/prds/the-tree-holds-only-what-a-board-uses/tags-are-derived-when-the-vault-is-written/probe/verify.sh
#
# Four checks, in the order the mechanism runs:
#   1. no authored memo or workflow carries `tags:`
#   2. both record checkers are green with them gone
#   3. the vault writer derives one note per record, tagged
#   4. the colour-group invariant is green against the regenerated vault
set -u
root="${PEARDE_ROOT:-$(pwd)}"
cd "$root" || exit 1
board=".pearde"
fail=0

stored=$(grep -l '^tags:' "$board"/memos/*.md "$board"/workflows/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "1. authored records carrying \`tags:\`: $stored (want 0)"
[ "$stored" = "0" ] || fail=1

python3 resources/memos.py check && python3 resources/workflows.py check \
  && echo "2. memos check + workflows check: green" \
  || { echo "2. record checkers: BROKEN"; fail=1; }

python3 resources/knowledge.py board >/dev/null || { echo "3. board writer: BROKEN"; fail=1; }
m=$(ls "$board"/wiki/memos/*.md 2>/dev/null | wc -l | tr -d ' ')
w=$(ls "$board"/wiki/workflows/*.md 2>/dev/null | wc -l | tr -d ' ')
a=$(ls "$board"/memos/*.md 2>/dev/null | grep -vc README)
b=$(ls "$board"/workflows/*.md 2>/dev/null | grep -vc README)
echo "3. generated notes: $m memo, $w workflow (authored: $a, $b)"
[ "$m" = "$a" ] && [ "$w" = "$b" ] || fail=1
grep -q '^tags: \[memo, kind/' "$board"/wiki/memos/*.md || { echo "   no derived memo tag found"; fail=1; }

bash resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh || fail=1

echo "probe: $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
