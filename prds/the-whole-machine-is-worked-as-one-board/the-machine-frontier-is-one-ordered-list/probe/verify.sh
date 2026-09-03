#!/usr/bin/env bash
# the `plan` read over a watch set — read-only, so the whole harness is: it runs from a
# directory with no board above it, it prints an order, it prints the reading
# that produced the count, and the tree is no different afterwards.
set -u
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# proves a tree holding none of the work. BOARD is the `.pearde` this harness
# sits under, found by walking, so no count of `..` has to match the PRD's
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's repo
# otherwise.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
# the READ is `plan`, and `run` is the move. They are two commands: this
# harness used to spell `$RUN all` through run.py and dispatch the whole
# watch set on every line below, while calling itself read-only on line 2.
# @.pearde/memos/no-harness-under-the-board-dispatches-it.md.
RUN="${RUN_PY:-$ROOT/resources/board/plan.py}"
# the command is run from `/`, so a relative RUN_PY is resolved against
# the repo root here — a path that stops working when you cd is not a path
case "$RUN" in /*) ;; *) RUN="$ROOT/$RUN" ;; esac
[ -f "$RUN" ] || RUN="$(cd "$(dirname "$0")" && pwd)/plan.py"
fail=0
t() { if eval "$2" >/dev/null 2>&1; then echo "ok   $1"; else echo "FAIL $1"; fail=1; fi; }

# what the tree looked like BEFORE the read-only command ran. Snapshotting it
# afterwards could not tell this build's own new files from a write the
# command made, which is the only thing this row is asking about.
BEFORE="$(cd "$ROOT" && git status --porcelain)"
OUT="$(cd / && python3 "$RUN" plan all 2>&1)"

t "runs from / with no board above the cwd"      '[ -n "$OUT" ]'
t "prints a board count over the watch set"      'grep -qE "^[0-9]+ of [0-9]+ board\(s\) · [0-9]+ PRDs on the frontier · [0-9]+ wave\(s\)$" <<<"$OUT"'
t "prints the slot count and its reading"        'grep -qE "^[0-9]+ slots \(.*ceiling [0-9]+\) · " <<<"$OUT"'
t "the reading names the cpu term"               'grep -qE "· cpu [0-9.]+ of [0-9]+ loaded" <<<"$OUT"'
t "the reading names the memory term"            'grep -qE "· mem [0-9.]+ of [0-9]+ GiB used" <<<"$OUT"'
t "every row is addressed @<board>/<rel>"        'grep -qE "^ *[0-9]+\. @[a-z0-9-]+/" <<<"$OUT"'
t "prints at least one wave"                     'grep -qE "^wave 1: @" <<<"$OUT"'
t "a row marked ready is in a wave"              '! comm -23 <(grep -oE "@[^ ]+" <<<"$(grep " ready  " <<<"$OUT")" | sort -u) <(grep "^wave " <<<"$OUT" | grep -oE "@[^,]+" | sed "s/^wave [0-9]*: //" | tr -d " " | sort -u) | grep -q .'
t "no row marked ready carries a non-dispatchable state" '! grep -E " (question|blocked|analyzing|claimed|deferred) +ready " <<<"$OUT"'
t "the merged progress line is one line"         '[ "$(cd / && python3 "$RUN" plan progress 2>&1 | wc -l | tr -d " ")" = 1 ]'
t "--json parses and carries slots, rows, waves" 'cd / && python3 "$RUN" plan --json 2>/dev/null | python3 -c "import json,sys;d=json.load(sys.stdin);assert d[\"slots\"]>=1 and d[\"rows\"] and d[\"waves\"]"'
t "it moved nothing in this repo"                '[ "$BEFORE" = "$(cd "$ROOT" && git status --porcelain)" ]'

# ── the ceiling is a setting, and `0` is the word this board uses for
# unlimited. These three ran against a throwaway board rather than the repo's
# own, because the case is what `machine-ceiling` SAYS, not what this machine
# is doing: the count is read straight out of `slots()` with the meter held
# still, so a busy afternoon cannot make the answer flap.
CEIL="$(mktemp -d)"; mkdir -p "$CEIL/.pearde"
ceil() {  # ceil <value|-> -> "<ceiling> <slots on a quiet machine>"
  if [ "$1" = "-" ]; then rm -f "$CEIL/.pearde/settings.md"
  else printf -- '---\nmachine-ceiling: %s\n---\n\n# s\n' "$1" > "$CEIL/.pearde/settings.md"; fi
  MDIR="$(dirname "$RUN")" BOARD="$CEIL/.pearde" python3 - <<'PY'
import os, sys
sys.path.insert(0, os.environ["MDIR"])
import run as m
m.SLOT_CEILING = m.ceiling(os.environ["BOARD"])
m._machine = lambda: (10, 32768.0, 0.20, 2000.0)   # a quiet 10-core/32GiB
n, r = m.slots()
print(m.SLOT_CEILING, n, r.split(" · ")[0])
PY
}

t "machine-ceiling: 0 lifts the ceiling"         '[ "$(ceil 0 | cut -d" " -f1-2)" = "0 24" ]'
t "an unlimited ceiling prints ∞, never 0"       'ceil 0 | grep -q "ceiling ∞)"'
t "an unlimited ceiling keeps the floor of 1"    'MDIR="$(dirname "$RUN")" python3 -c "
import os,sys; sys.path.insert(0, os.environ[\"MDIR\"]); import run as m
m.SLOT_CEILING = 0
m._machine = lambda: (10, 32768.0, 40.0, 30000.0)
m._busy_now = lambda seconds=1: (0.99, 1.0)
n, r = m.slots(); assert n == 1, (n, r)"'
t "a set machine-ceiling is honoured"            '[ "$(ceil 4 | cut -d" " -f1-2)" = "4 4" ]'
t "an absent machine-ceiling still gives 12"     '[ "$(ceil - | cut -d" " -f1-2)" = "12 12" ]'
t "an unparseable machine-ceiling gives 12"      '[ "$(ceil banana | cut -d" " -f1-2)" = "12 12" ]'
rm -rf "$CEIL"

# ── groups. A group is a label a board writes on ITSELF, so the fixture is
# four throwaway board dirs and the functions that read them: `declared`,
# `all_groups`, `in_group`. The watch set is the daemon's and this repo does
# not get to add boards to it, so the filter is tested against synthetic
# entries — the same list `boards()` returns. `split_group` is tested against
# argv alone, because the whole question there is which bare word is a group.
GRP="$(mktemp -d)"
for b in a b c d; do mkdir -p "$GRP/$b"; done
printf -- '---\nname: a\ngroups: work infra\n---\n'                > "$GRP/a/settings.md"
printf -- '---\nname: b\ngroups:\n  - Private\n  - work\n---\n'    > "$GRP/b/settings.md"
printf -- '---\nname: c\ngroups: slots, all, private\n---\n'       > "$GRP/c/settings.md"
printf -- '---\nname: d\n---\n'                                    > "$GRP/d/settings.md"
g() { MDIR="$(dirname "$RUN")" GRP="$GRP" python3 - "$@" <<'GPY'
import os, sys
sys.path.insert(0, os.environ["MDIR"])
import run as m
G = os.environ["GRP"]
e = [(k, os.path.join(G, k)) for k in "abcd"]
q = sys.argv[1]
if q == "groups":
    print(" ".join(f"{k}={','.join(v)}" for k, v in sorted(m.all_groups(e).items())))
elif q == "in":
    print(",".join(k for k, _ in m.in_group(e, sys.argv[2])[0]))
elif q == "note":
    print(m.in_group(e, sys.argv[2])[1])
elif q == "bad":
    print(" ".join(b for b, _ in m.declared(os.path.join(G, sys.argv[2]))[1]))
elif q == "split":
    grp, rest = m.split_scope(sys.argv[2:], m.READ_VERBS)
    print(str(grp) + " |" + "".join(" " + x for x in rest))
GPY
}

t "a board declares its own groups"              '[ "$(g groups)" = "infra=a private=b,c work=a,b" ]'
t "a board carries several labels"               '[ "$(g in work)" = "a,b" ]'
t "labels are case-folded"                       '[ "$(g in private)" = "b,c" ]'
t "a board may declare none"                     '! g groups | grep -q "=.*d"'
t "a verb is refused as a label"                 'g bad c | grep -qw slots'
t "reserved all is refused as a label"           'g bad c | grep -qw all'
t "the filter note names what was left out"      'g note work | grep -qE "group .work.: 2 of 4 watched board\(s\) . a, b"'
t "a bare word is the group"                     '[ "$(g split work)" = "work |" ]'
t "a verb is never the group"                    '[ "$(g split slots)" = "None | slots" ]'
t "group and verb read in either order"          '[ "$(g split work slots)" = "$(g split slots work)" ]'
t "a flag value is never the group"              '[ "$(g split slots --workers 4)" = "None | slots --workers 4" ]'
t "an unknown group is refused, not empty"       'cd / && ! python3 "$RUN" plan no-such-group-here >/dev/null 2>&1'
t "the refusal names how to join one"            'cd / && python3 "$RUN" plan no-such-group-here 2>&1 | grep -q "settings.md"'
t "plan groups runs over the real watch set"    'cd / && python3 "$RUN" plan groups >/dev/null 2>&1'
t "--json carries the scope and the labels"      'cd / && python3 "$RUN" plan --json 2>/dev/null | python3 -c "import json,sys;d=json.load(sys.stdin);assert d[\"group\"] == \"all\" and isinstance(d[\"groups\"], dict)"'
rm -rf "$GRP"

[ $fail -eq 0 ] && echo "PASS" || echo "FAIL"
exit $fail
