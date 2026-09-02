#!/usr/bin/env bash
# The flip for the re-aimed readme-in-three-rings harness, on a tree built
# from `git archive HEAD` so no neighbouring session's uncommitted file can
# move the answer. Three trees:
#
#   good     HEAD as it stands                                 -> green
#   skill    one extra file under references/skills/           -> STILL GREEN
#            (the old harness pinned `16` and `80` and went red on this)
#   home     doctor's `memos` row taught to read $HOME         -> RED
#   board    init writes an example board with a broken memo    -> RED
#            (a row other than vault that depends on the home — the one
#             thing section 6 exists to catch)
#
# Pass `noise` as $1 to add a fourth: the view service stopped between the
# two doctor runs. The old harness went red on it; the control pair names it
# as machine noise and stays green.
set -u
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
P=".pearde/prds/the-board-runs-itself/readme-in-three-rings/probe"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT

TREES="good skill home board"
for d in $TREES; do
  mkdir -p "$T/$d"
  ( cd "$ROOT" && git archive HEAD | tar -x -C "$T/$d" )
  mkdir -p "$T/$d/$P"
  cp "$ROOT/$P/verify.sh" "$ROOT/$P/quickstart.sh" "$T/$d/$P/"
  ( cd "$T/$d" && git init -q . && git add -A >/dev/null 2>&1 \
      && git -c user.email=p@p -c user.name=p commit -qm base )
done

# skill — a seventeenth skill file, committed so the copy carries it
cp "$T/skill/references/skills/pearde-view.md" \
   "$T/skill/references/skills/pearde-probe.md"
( cd "$T/skill" && git add -A && git -c user.email=p@p -c user.name=p commit -qm skill -q )

# home — doctor's memos row made to depend on $HOME, which is what a
# home-dependent row that is not `vault` actually looks like
python3 - "$T/home/resources/doctor.sh" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
i = s.index('row memos ok')
s = s[:i] + '[ -d "$HOME/.obsidian" ] || { row memos broken "probe"; }\n    ' + s[i:]
open(p, "w").write(s)
PY
( cd "$T/home" && git add -A && git -c user.email=p@p -c user.name=p commit -qm home -q )

# board — the example board `init` copies carries a memo doctor rejects, so
# the fault IS the board init wrote. A bare checkout has no memos row at all,
# so the control cannot excuse it.
printf -- '---\nkind: not-a-kind\n---\n\n# broken\n' \
  > "$T/board/resources/board/example/memos/probe-broken.md"
( cd "$T/board" && git add -A && git -c user.email=p@p -c user.name=p commit -qm board -q )

# Differential, never absolute: three other sessions write this tree while
# this runs, and HEAD itself is mid-flight (doctor.sh at HEAD names a
# references/grammar.md that is not committed yet). So `good` is the
# baseline, whatever it prints, and each variant is judged only by what it
# ADDS to it. That is the flip: the added-skill tree must add nothing, the
# home-dependent tree must add exactly the one check this section exists to
# make.
RC=0
run() { bash "$T/$1/$P/quickstart.sh" 2>&1 | grep -E '^FAIL' | sed 's/ — .*//' | sort; }
run good > "$T/good.f"
echo "--- good (baseline): $(grep -c . < "$T/good.f") fail"
sed 's/^/    /' "$T/good.f"
for d in skill home board; do
  run "$d" > "$T/$d.f"
  ADDED="$(comm -13 "$T/good.f" "$T/$d.f")"
  echo "--- $d: adds $(printf '%s' "$ADDED" | grep -c . || true) over the baseline"
  printf '%s\n' "$ADDED" | grep . | sed 's/^/    + /' || true
done
WANT_SKILL=""
WANT_HOME="FAIL: 6 no row but vault reads the home"
WANT_BOARD="FAIL: 2 the board init wrote breaks no doctor row"
GOT_SKILL="$(comm -13 "$T/good.f" "$T/skill.f")"
GOT_HOME="$(comm -13 "$T/good.f" "$T/home.f")"
GOT_BOARD="$(comm -13 "$T/good.f" "$T/board.f")"
[ "$GOT_SKILL" = "$WANT_SKILL" ] || { echo "UNEXPECTED: an added skill file reddened the harness"; RC=1; }
case "$GOT_HOME" in
  *"$WANT_HOME"*) ;;
  *) echo "UNEXPECTED: a home-dependent row did not redden the harness"; RC=1 ;;
esac
case "$GOT_BOARD" in
  *"$WANT_BOARD"*) ;;
  *) echo "UNEXPECTED: a board init wrote badly did not redden the harness"; RC=1 ;;
esac
[ "$RC" = 0 ] && echo "FLIP: green on the input it must pass, red on the input it must catch"
exit $RC
