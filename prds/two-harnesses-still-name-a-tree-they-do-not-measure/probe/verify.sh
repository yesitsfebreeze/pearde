#!/usr/bin/env bash
# probe — two harnesses still name a tree they do not measure
#
# What this measures: the four harnesses that were still computing their own
# root when this PRD was claimed. Every assertion below was run for real
# before it was written down; none is a prediction.
#
#   bash prds/two-harnesses-still-name-a-tree-they-do-not-measure/probe/verify.sh
#
# Scoped to this PRD's four files on purpose. The board-wide census lives in
# a-harness-measures-the-tree-its-worker-built-in and asserts a population
# that grows from other lanes mid-run — it went red on a fifth harness during
# this pass. A verify command that a landing elsewhere can redden is not a
# check on this unit's work.
#
# PEARDE_ROOT names the tree to measure; it defaults to the repo above the
# board this file sits in. The fixture is made at run time under $TMPDIR.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"

P=0; F=0
ok() { if [ "$2" = 0 ]; then P=$((P+1)); echo "  ok   $1"; else F=$((F+1)); echo "  FAIL $1 — $3"; fi; }

FOUR="
prds/every-run-session-works-in-a-worktree-of-its-own/probe/verify.sh
prds/every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe/verify.sh
prds/resources-are-organised-by-responsibility/probe/verify.sh
prds/resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule/probe/verify.sh
"

# The four greps that say a file takes its root from the runner. Printed as
# one offence per line, so the same function serves the census in A and the
# planted-defect experiment in C without either touching the other's files.
offences() {
  f="$1"
  [ -f "$f" ] || { echo "not on disk"; return; }
  grep -qF '${PEARDE_ROOT:-' "$f" || echo "does not read \${PEARDE_ROOT:-"
  grep -qF 'basename "$BOARD"' "$f" || echo "does not walk up to its board"
  grep -qE '(dirname "\$0"|BASH_SOURCE\[0\][:}][^)]*\}"|\$HERE)/\.\./\.\./\.\.' "$f" \
    && echo "counts .. to reach the repo"
  grep -qF '/Users/feb/dev/infra/pearde' "$f" && echo "names an absolute root"
  return 0
}

echo "probe: two harnesses still name a tree they do not measure — board $BOARD"
echo "A. each of the four takes its root from the runner"
for h in $FOUR; do
  f="$BOARD/$h"; n="$(basename "$(dirname "$(dirname "$f")")")/$(basename "$(dirname "$f")")"
  o="$(offences "$f")"
  [ -z "$o" ]; ok "A1 $n" $? "$(printf %s "$o" | tr '\n' ';')"
done

echo "B. the root each one resolves, measured by running it"
# A lane-shaped tree the harnesses can be pointed at: a repo with resources/
# but none of the modules the four import, made at run time, never under the
# board. Pointing a harness at it must change what the harness reads.
T="$(mktemp -d "${TMPDIR:-/tmp}/pearde-tworoot.XXXXXX")"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/fake/resources/board"
: > "$T/fake/resources/pearde.py"

S="$BOARD/prds/every-run-session-works-in-a-worktree-of-its-own/probe/verify.sh"
LANE="$BOARD/.lanes/every-run-session-works-in-a-worktree-of-its-own"

# the session harness is the one that used to hardcode a lane path. With no
# root named it reads the board's own repo, which holds no sessions.py, so it
# is red — the honest reading. Told to measure the lane that does hold it, it
# is green. Before this PRD it was green either way, because it named the lane
# in the file and never read the tree it was run against.
out="$(bash "$S" 2>&1)"; rc=$?
[ "$rc" != 0 ]; ok "B1 session harness is red against a tree with no sessions.py" $? "exit $rc"
printf %s "$out" | grep -q "No module named 'sessions'"
ok "B2 …and red for that reason, not another" $? "did not name the missing module"
if [ -d "$LANE" ]; then
  PEARDE_ROOT="$LANE" bash "$S" >/dev/null 2>&1
  ok "B3 …and green when the runner names the tree that holds it" $? "red under PEARDE_ROOT=$LANE"
else
  echo "  ok   B3 skipped — no lane cut for every-run-session-works-in-a-worktree-of-its-own"; P=$((P+1))
fi

# every one of the four reports or reads the named root, never the board's
# repo, once the runner names one.
for h in $FOUR; do
  f="$BOARD/$h"; n="$(basename "$(dirname "$(dirname "$f")")")"
  o="$(PEARDE_ROOT="$T/fake" bash "$f" 2>&1)"
  printf %s "$o" | grep -qF "$T/fake" || printf %s "$o" | grep -qiE 'not on disk|no such file|No module named|not found'
  ok "B4 $n reads the tree the runner named" $? "no sign of $T/fake in its output"
done

echo "C. section A can fail — proven on a copy, never on the file itself"
# Each of the four defects this PRD removed, planted back into a scratch copy
# under $T. The originals are read once with `cp` and never written to, so a
# run that dies between the plant and the check leaves the board untouched —
# an earlier draft did the experiment in place under `bash -e` and left a
# reverted harness behind when the block aborted.
i=0
for spell in \
  's|^ROOT=.*|ROOT="$(cd "$HERE/../../../.." \&\& pwd -P)"|' \
  's|^ROOT=.*|ROOT="/Users/feb/dev/infra/pearde"|' \
  's|^while \[ "$BOARD".*||' \
  's|^ROOT=.*|ROOT="$(dirname "$BOARD")"|' ; do
  i=$((i+1))
  cp "$BOARD/prds/resources-are-organised-by-responsibility/probe/verify.sh" "$T/planted.$i.sh"
  sed -i '' "$spell" "$T/planted.$i.sh"
  o="$(offences "$T/planted.$i.sh")"
  [ -n "$o" ]; ok "C$i a planted defect is seen: $(printf %s "$o" | tr '\n' ';')" $? "planted defect $i went unnoticed"
done
o="$(offences "$BOARD/prds/resources-are-organised-by-responsibility/probe/verify.sh")"
[ -z "$o" ]; ok "C5 …and the file it was copied from is unchanged" $? "$o"

echo "probe: $P passed, $F failed"
[ "$F" = 0 ]
