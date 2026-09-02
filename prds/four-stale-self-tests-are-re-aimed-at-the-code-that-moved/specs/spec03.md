---
complexity: 6
footprint:
  - .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh
---

# spec03 — the vanished registry: four checks in two harnesses, not two

Both harnesses read `resources/board/state/serve.json`. That path has not
existed since the `every-artifact-lands-inside-the-board` invariant moved the
daemon's registration into the board that owns it — `resources/board/serve.py`
`entry_path()` returns `<board>/.state/serve.json`, and no machine-wide list
survives.

Each harness carries **two** checks on that path, and this is the trap the PRD
names: the loud one ("the copy's registry never learned the fixture", wanting
`[]`) fails, and the silent sibling ("the real registry is untouched") compares
an empty string to an empty string and **passes measuring nothing**. Re-aiming
only the loud one leaves the harness green and blind. All four move.

**Already standing (this analyst's uncommitted pass one), the same shape in
each file:**

- `REG` points at `$ROOT/.pearde/.state/serve.json` — this board's own
  registration, the file the invariant actually created.
- `REG_BEFORE` and the comparison both end `|| echo absent`. That is the part
  that removes the vacuity: the real board is not registered on a machine where
  the view daemon is not watching it, so a bare `[ -f ] && cksum` would still be
  empty-versus-empty. With the sentinel, a run that *creates* the real board's
  registration flips `absent` to a checksum and the check fails — which is the
  failure the check exists to catch.
- The sibling is re-aimed to the invariant it now expresses rather than to a
  deleted file's contents: `find "$TOP/srv" -name serve.json | wc -l` is `0` —
  the copied install is code only, and nothing the fixture run did wrote state
  beside it. `find` does not follow the symlinks `$TOP/srv` holds into the real
  tree, so this reads only the copy.
- Both are retitled ("the real board's registration is untouched", "the copied
  install holds no registration at all") and carry a comment naming the
  invariant that moved the file.

**Left to finish:** re-run both harnesses whole. `collect-is-a-command` is slow
and binds a port; run it on its own, never through a sweep.

**Downstream, already confirmed and not to be edited:**
`the-collect-and-brief-harnesses-are-carried-across-the-layou` sums sibling
totals and picked up `133 · 133 pass · 0 fail` with no edit of its own. Re-run
it as proof, change nothing in it.

## Acceptance

- [x] `collect-is-a-command` reports every check passing with 0 fail, exits 0, and its two R rows both read ok (133/133 at this run; the denominator is a shared board file, so it is printed, never gated)
- [x] `init-asks-nothing` reports every check passing with 0 fail, exits 0, and its two J rows both read ok (89/89 at this run — a neighbour added `A settings.md · happiness` to this shared file after the run that read 88, which is exactly why the denominator is printed, never gated)
- [x] Neither harness names `resources/board/state/serve.json` any more — `grep -c` over both files is 0
- [x] The re-aimed sibling is shown non-vacuous: in a scratch directory, the `absent` sentinel changes value when the file is created, and the `find` count goes 0 → 1 when a `serve.json` is planted. Neither probe touches the real board
- [x] `the-collect-and-brief-harnesses-are-carried-across-the-layou` exits 0 with no edit — `git -C .pearde diff --name-only` does not name it

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
C=.pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
I=.pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh
D=.pearde/prds/the-collect-and-brief-harnesses-are-carried-across-the-layou/probe/verify.sh
cat > "$W/tally.py" <<'PY'
import re, sys
last = None
for line in open(sys.argv[1], errors="replace"):
    m = re.search(r"(\d+) checks \S+ (\d+) pass \S+ (\d+) fail\s*$", line)
    if m:
        last = m.groups()
if not last:
    print("no-tally red")
else:
    print("%s/%s fail=%s %s" % (last[0], last[1], last[2],
          "green" if last[0] == last[1] and last[2] == "0" else "red"))
PY
crc=0; bash "$C" > "$W/c" 2>&1 || crc=$?
irc=0; bash "$I" > "$W/i" 2>&1 || irc=$?
drc=0; bash "$D" > "$W/d" 2>&1 || drc=$?
tail -2 "$W/c"; echo "collect-is-a-command exit=$crc"
tail -2 "$W/i"; echo "init-asks-nothing exit=$irc"
tail -2 "$W/d"; echo "downstream exit=$drc"
# green means every check passed and none failed. The denominators are NOT
# pinned: all three are shared board files, and a neighbour adding a passing
# check must not redden this PRD's block. It did — init-asks-nothing went 88 to
# 89 mid-run when another session added `A settings.md · happiness` to it.
ct="$(python3 "$W/tally.py" "$W/c")"
it="$(python3 "$W/tally.py" "$W/i")"
dt="$(python3 "$W/tally.py" "$W/d")"
# the four re-aimed rows, by their own titles, in the run output and in the files
rr="$( { grep -cE "ok   R (the real board's registration is untouched|the copied install holds no registration at all)" "$W/c" || true; } )"
jj="$( { grep -cE "ok   J (the real board's registration is untouched|the copied install holds no registration at all)" "$W/i" || true; } )"
cf="$( { grep -cE "(the real board's registration is untouched|the copied install holds no registration at all)" "$C" || true; } )"
if_="$( { grep -cE "(the real board's registration is untouched|the copied install holds no registration at all)" "$I" || true; } )"
# the vanished path is named nowhere in either harness
dc="$( { grep -c 'resources/board/state/serve.json' "$C" || true; } )"
di="$( { grep -c 'resources/board/state/serve.json' "$I" || true; } )"
# the downstream harness is arithmetic over its siblings and carries no edit
edited="$(git -C .pearde diff --name-only | { grep -c 'the-collect-and-brief-harnesses-are-carried-across-the-layou' || true; } )"
# non-vacuity, in a scratch dir only — the real board is never touched
mkdir -p "$W/srv/board"
e0="$(find "$W/srv" -name serve.json | wc -l | tr -d ' ')"
echo '{}' > "$W/srv/board/serve.json"
e1="$(find "$W/srv" -name serve.json | wc -l | tr -d ' ')"
R="$W/x.json"; B="$( [ -f "$R" ] && cksum < "$R" || echo absent )"
echo x > "$R"; A="$( [ -f "$R" ] && cksum < "$R" || echo absent )"
echo "collect=$ct init=$it downstream=$dt"
echo "R-rows=$rr J-rows=$jj in-C=$cf in-I=$if_ dead-path=$dc,$di downstream-edited=$edited"
echo "find 0->1: $e0 -> $e1 | sentinel: $B -> $A"
[ "$crc" = 0 ] && [ "$irc" = 0 ] && [ "$drc" = 0 ] \
  && [ "${ct##* }" = green ] && [ "${it##* }" = green ] && [ "${dt##* }" = green ] \
  && [ "$rr" = 2 ] && [ "$jj" = 2 ] && [ "$cf" = 2 ] && [ "$if_" = 2 ] \
  && [ "$dc" = 0 ] && [ "$di" = 0 ] && [ "$edited" = 0 ] \
  && [ "$e0" = 0 ] && [ "$e1" = 1 ] && [ "$B" = absent ] && [ "$A" != "$B" ]
```
