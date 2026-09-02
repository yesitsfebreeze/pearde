#!/usr/bin/env bash
# Re-run every acceptance box of this PRD against the MERGED tree, never the
# lane alone. The lane's base and main's tip both move; a gate run on either
# side by itself is the defect this retry exists for.
#
#   LANE=<lane worktree> MAIN=<main ref> bash verify_merged.sh
#
# It writes nothing into either checkout: the merged tree is materialised
# from `git merge-tree --write-tree` into a temp dir, and the lane's
# uncommitted files are copied over it, because `collect` commits those onto
# the lane before it merges.
set -u

LANE=${LANE:-/Users/feb/dev/infra/pearde/pearde/.lanes/every-document-is-written-in-the-writer-s-prose-example-and-knowledge-fixtures-are-rewritten-dense}
# The lane's fork point, pinned as a literal SHA. `main` cannot be the default:
# `collect` commits the merge BEFORE it runs this block, so by then `main`
# contains the lane and every diff against it is empty — the box then reads
# 0 changed files and fails on work that is correct.
MAIN=${MAIN:-9a98fae}
cd "$LANE" || exit 2

pass=0; fail=0
box() { # box <name> <expected-exit> ; reads the last command's status
  local name=$1 want=$2 got=$3
  if [ "$got" = "$want" ]; then pass=$((pass+1)); echo "PASS  $name"
  else fail=$((fail+1)); echo "FAIL  $name (exit $got, wanted $want)"; fi
}

# REF=main runs the whole set against main alone — the negative control that
# says every box below can still go red.
REF=${REF:-HEAD}
TREE=$(git merge-tree --write-tree "$MAIN" "$REF" 2>/dev/null)
if [ -z "$TREE" ]; then echo "FAIL  the lane does not merge into $MAIN"; exit 1; fi
echo "merged tree $TREE  ($MAIN + $(git rev-parse --short "$REF") + uncommitted)"

M=$(mktemp -d); trap 'rm -rf "$M" "$D" "$K"' EXIT
git archive "$TREE" | tar -x -C "$M"
# the files `collect` will commit onto the lane, laid over the merged tree
if [ "$REF" = HEAD ]; then for f in $(git diff --name-only); do cp "$f" "$M/$f"; done; fi

cd "$M" || exit 2
FIX=$(find resources/board/example resources/board/knowledge -name '*.md' | sort)

# --- spec01 -----------------------------------------------------------------
out=$(python3 resources/prose.py check $FIX 2>&1); prose=$?
# the checker has to have run: a crashed prose.py names no file either
[ "$prose" = 0 ] || [ "$prose" = 1 ] ; box "spec01.0 prose.py ran over $(echo "$FIX" | wc -l | tr -d ' ') fixture files" 0 $?
echo "$out" | grep -q 'resources/board/example/' ; box "spec01.1 prose names no example/ file" 1 $?

D=$(mktemp -d)
python3 resources/board/plan.py example "$D" >/dev/null 2>&1
scan=$(python3 resources/board/plan.py scan "$D/pearde" 2>&1)
echo "$scan" | grep -q '8 PRDs' && echo "$scan" | grep -q 'boxes 3/5' && echo "$scan" | grep -q 'boxes 3/3'
box "spec01.2 scan prints 8 PRDs, boxes 3/5 and 3/3" 0 $?
echo "$scan" | grep -oE '^(collect|waiting on you|in flight|ready|gated)' | tr '\n' ' ' | grep -q 'collect waiting on you in flight ready gated '
box "spec01.2 band order unchanged" 0 $?

python3 resources/memos.py check "$D/pearde" >/dev/null 2>&1;     box "spec01.3 memos.py check silent" 0 $?
python3 resources/workflows.py check "$D/pearde" >/dev/null 2>&1; box "spec01.3 workflows.py check silent" 0 $?
python3 resources/questions.py check "$D" >/dev/null 2>&1;        box "spec01.3 questions.py check silent" 0 $?

cd "$LANE" || exit 2
ns=$(git diff --name-status "$MAIN" "$TREE" -- resources/board/example/)
# an empty diff would satisfy "no line is an add" — count the M lines too
[ "$(echo "$ns" | grep -cE '^M')" -ge 13 ] && [ -z "$(echo "$ns" | grep -vE '^M')" ]
box "spec01.4 13+ example/ files changed and every line is M" 0 $?

for f in prds/building/specs/spec01.md prds/finished/specs/spec01.md; do
  diff <(git show "$MAIN:resources/board/example/$f" | grep -E '^\s*- \[') \
       <(git show "$TREE:resources/board/example/$f" | grep -E '^\s*- \[') >/dev/null
  box "spec01.5 box text unchanged in $f" 0 $?
done

a=$(git show "$TREE:resources/board/example/prds/asking/prd.md")
[ "$(echo "$a" | grep -cE '^[0-9]+\. \*\*')" = 3 ] && [ "$(echo "$a" | grep -c '(recommended)')" = 1 ]
box "spec01.6 asking/prd.md keeps three answers, one recommended" 0 $?

# --- spec02 -----------------------------------------------------------------
echo "$out" | grep -q 'resources/board/knowledge/' ; box "spec02.1 prose names no knowledge/ file" 1 $?

diff <(git show "$MAIN:resources/board/knowledge/WORKFLOW.md" | sed -n '2,/^---$/p') \
     <(git show "$TREE:resources/board/knowledge/WORKFLOW.md" | sed -n '2,/^---$/p') >/dev/null
box "spec02.2 WORKFLOW.md frontmatter byte-identical" 0 $?

grep -rq Vicky "$M/resources/board/knowledge/" ; box "spec02.3 the legacy name is gone" 1 $?

w=$(git show "$TREE:resources/board/knowledge/WORKFLOW.md")
[ "$(echo "$w" | grep -cE '^### (default|deep-dive|triage|crystalize)')" = 4 ]
box "spec02.4 all four workflow ids present" 0 $?
diff <(git show "$MAIN:resources/board/knowledge/WORKFLOW.md" | grep -E '^\|') \
     <(echo "$w" | grep -E '^\|') >/dev/null
box "spec02.4 the Routing table rows are unchanged" 0 $?

for f in Dashboard.md conclusions/_index.md sources/_index.md; do
  diff <(git show "$MAIN:resources/board/knowledge/$f" | awk '/^```dataview/,/^```$/') \
       <(awk '/^```dataview/,/^```$/' "$M/resources/board/knowledge/$f") >/dev/null
  box "spec02.5 dataview fences byte-identical in $f" 0 $?
done

cd "$M" || exit 2
K=$(mktemp -d)
python3 resources/pearde.py init "$K" >/dev/null 2>&1
n=0; for f in Dashboard.md WORKFLOW.md conclusions/_index.md sources/_index.md sources/.absorbed/_index.md; do
  [ -f "$K/pearde/wiki/$f" ] && n=$((n+1)); done
[ "$n" = 5 ] ; box "spec02.6 pearde init plants all five knowledge files" 0 $?
python3 resources/knowledge.py --root "$K/pearde/wiki" doctor >/dev/null 2>&1
box "spec02.6 knowledge.py doctor is clean on the planted vault" 0 $?

# --- spec03 -----------------------------------------------------------------
python3 resources/prose.py check resources/board/example/memos/README.md >/dev/null 2>&1
box "spec03.1 the generated index reads dense" 0 $?
python3 resources/memos.py check "$D/pearde" >/dev/null 2>&1
box "spec03.2 the example fixture equals what render_index() emits" 0 $?
python3 resources/memos.py check "$K/pearde" >/dev/null 2>&1
box "spec03.3 a board this generator made checks clean" 0 $?
git -C "$LANE" show "$TREE:resources/board/example/memos/README.md" | grep -q '^# Memos' \
  && git -C "$LANE" show "$TREE:resources/board/example/memos/README.md" | grep -q '^## Decisions' \
  && git -C "$LANE" show "$TREE:resources/board/example/memos/README.md" | grep -q 'dates-are-written-not-stamped' \
  && git -C "$LANE" show "$TREE:resources/board/example/memos/README.md" | grep -q 'decided · 2026-08-28'
box "spec03.4 every content line of the index survives" 0 $?
echo "$out" | grep -qE 'resources/board/(example|knowledge)/' ; box "spec03.5 prose names no fixture file at all" 1 $?

echo
echo "boxes $pass/$((pass+fail))"
[ "$fail" = 0 ]
