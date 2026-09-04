#!/usr/bin/env bash
# Verify harness for one-definition-of-the-board-not-two.
# Run from the CODE repo root: bash .pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh
# Counts are computed from disk each run — the board is live and moving, so
# nothing here is a hardcoded snapshot number.
set -u
# BOARD is the `.pearde` this harness sits under — found by walking, so no
# count of `..` has to match the PRD's nesting depth. ROOT is the tree under
# test: the runner's when it names one (a worker builds in a lane worktree at
# <board>/.lanes/<slug>, which holds no board of its own), that board's repo
# otherwise. The root no longer spells the board: in a lane there is none.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
cd "$ROOT" || exit 1

pass=0; fail=0
ok()   { pass=$((pass+1)); echo "  ok   $1"; }
bad()  { fail=$((fail+1)); echo "  FAIL $1"; }

echo "== A: memos — list count matches disk, check opens real files =="
disk_memos=$(python3 -c "
import os
d = os.path.join('$BOARD', 'memos')
print(len([f for f in os.listdir(d) if f.endswith('.md') and f != 'README.md']))
")
list_memos=$(python3 resources/memos.py list "$BOARD" | wc -l | tr -d ' ')
[ "$disk_memos" = "$list_memos" ] && ok "memos list ($list_memos) == memos on disk ($disk_memos)" \
  || bad "memos list ($list_memos) != memos on disk ($disk_memos)"

# check must not be silently-green over an unopened directory: it must not
# reference a bare "prds" basename resolution anywhere in its own source.
grep -q 'os.path.basename(p) == "prds"' resources/memos.py \
  && bad "memos.py find_board still resolves to <x>/prds" \
  || ok "memos.py find_board no longer resolves to <x>/prds"

echo "== B: workflows — list count matches disk, refs carry no prds/ prefix =="
disk_wf=$(python3 -c "
import os
d = os.path.join('$BOARD', 'workflows')
print(len([f for f in os.listdir(d) if f.endswith('.md') and f != 'README.md']))
")
list_wf=$(python3 resources/workflows.py list "$BOARD" | wc -l | tr -d ' ')
[ "$disk_wf" = "$list_wf" ] && ok "workflows list ($list_wf) == atomics+workflows on disk ($disk_wf)" \
  || bad "workflows list ($list_wf) != atomics+workflows on disk ($disk_wf)"

bad_prefix=$(python3 -c "
import sys; sys.path.insert(0, 'resources')
import workflows
refs = workflows.board_workflow_refs('$BOARD')
print(sum(1 for rel, v, home in refs if rel.startswith('prds/')))
")
[ "$bad_prefix" = "0" ] && ok "no workflow ref label carries a stray prds/ prefix" \
  || bad "$bad_prefix workflow ref label(s) still carry a stray prds/ prefix"

echo "== C: questions — prds() walks board/prds, not board =="
bad_q_prefix=$(python3 -c "
import sys; sys.path.insert(0, 'resources')
import questions
board = questions.find_board('$BOARD')
out = questions.prds(board)
print(sum(1 for rel, path in out if rel.startswith('prds/')))
")
[ "$bad_q_prefix" = "0" ] && ok "no questions.prds() label carries a stray prds/ prefix" \
  || bad "$bad_q_prefix questions.prds() label(s) still carry a stray prds/ prefix"

disk_prds=$(python3 -c "
import os
n = 0
for r, d, f in os.walk(os.path.join('$BOARD', 'prds')):
    if 'prd.md' in f:
        n += 1
print(n)
")
q_prds=$(python3 -c "
import sys; sys.path.insert(0, 'resources')
import questions
board = questions.find_board('$BOARD')
print(len(questions.prds(board)))
")
[ "$disk_prds" = "$q_prds" ] && ok "questions.prds() count ($q_prds) == prd.md files on disk ($disk_prds)" \
  || bad "questions.prds() count ($q_prds) != prd.md files on disk ($disk_prds)"

echo "== D: all four commands agree — no-arg walk, .pearde, repo root =="
for tool in memos questions workflows; do
  a=$(cd "$ROOT" && python3 "resources/$tool.py" list 2>&1)
  b=$(python3 "resources/$tool.py" list "$BOARD" 2>&1)
  c=$(python3 "resources/$tool.py" list "$ROOT" 2>&1)
  if [ "$a" = "$b" ] && [ "$b" = "$c" ]; then
    ok "$tool.py list agrees across no-arg / .pearde / repo-root"
  else
    bad "$tool.py list disagrees across invocation forms"
  fi
done

echo "== E: error path still names the command that was run =="
for tool in memos questions workflows; do
  msg=$(cd /tmp && python3 "$ROOT/resources/$tool.py" list 2>&1)
  code=$?
  case "$msg" in
    "$tool: no .pearde/ board found walking up from the cwd") ok "$tool.py: own error prefix, cwd walk" ;;
    *) bad "$tool.py: unexpected error text: $msg" ;;
  esac
  [ "$code" = "1" ] && ok "$tool.py: exit 1 with no board" || bad "$tool.py: exit $code with no board (want 1)"
done

echo "== F: doctor.sh rows report counts that match disk =="
doctor_out=$(bash resources/doctor.sh 2>&1)
echo "$doctor_out" | grep -qE "memos +ok +$disk_memos memos" \
  && ok "doctor memos row: $disk_memos memos, ok" \
  || bad "doctor memos row does not report $disk_memos memos ok — $(echo "$doctor_out" | grep 'memos ')"
echo "$doctor_out" | grep -qE "workflows +ok" \
  && ok "doctor workflows row: ok" \
  || bad "doctor workflows row not ok — $(echo "$doctor_out" | grep 'workflows ')"
echo "$doctor_out" | grep -qE "questions +ok" \
  && ok "doctor questions row: ok" \
  || bad "doctor questions row not ok — $(echo "$doctor_out" | grep 'questions ')"

echo "== G: knowledge.py board — no PRD note nested under a stray board/prds/ =="
python3 resources/knowledge.py board >/dev/null 2>&1
stray=$(python3 -c "
import os
print(1 if os.path.isdir('$BOARD/wiki/board/prds') else 0)
")
[ "$stray" = "0" ] && ok "knowledge.py board writes no board/prds/ subtree" \
  || bad "knowledge.py board still writes a stray board/prds/ subtree"

kb_count=$(python3 resources/knowledge.py board 2>&1 | grep -oE '^board: [0-9]+' | grep -oE '[0-9]+')
[ "$kb_count" = "$disk_prds" ] && ok "knowledge.py board wrote $kb_count PRD note(s), matching disk ($disk_prds)" \
  || bad "knowledge.py board wrote $kb_count PRD note(s), disk has $disk_prds"

echo
echo "$((pass+fail)) checks · $pass pass · $fail fail"
echo "verify.sh done, fail=$fail"
# the harness carries its own verdict — a run with a failed check must not
# exit 0, or the proof cannot fail
exit $(( fail != 0 ))
