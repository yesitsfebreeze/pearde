---
complexity: 4
footprint:
  - .pearde/prds/one-page-that-says-whats-up/probe/verify.sh
---

# spec01 — the page harness follows the two deliberate view changes

Two checks in `one-page-that-says-whats-up` guard a page layout that its owning
session then changed on purpose. `eaa11a1` lifted the `purpose` div out of the
timeline section and into the state drawer, beside `now` and `whatsup`;
`4ce11ec` re-measured everything above the stage and the no-script fallback
height became `calc(100vh - 104px)`. Neither `render.py` nor `view.css` may be
touched to satisfy a check — both changes stand and belong to another session.
Only the harness moves.

**Already standing (this analyst's uncommitted pass one):**

- "the vision line is inside it too" is now "the vision line is in the state
  drawer" and asserts `<aside id="state"` < `id="purpose"` < the first
  `</aside>` after it, rather than the old timeline-section ordering.
- The fallback-height needle reads `104px` instead of `260px`. Its sibling
  checks — that the stage is no longer viewport-locked, that the retired
  constraint is recorded in a comment, and that the script writes the same
  number — were already green and are untouched.
- Both carry a comment saying what moved underneath them and which commit
  moved it, so the next reader does not re-derive it.

**Left to finish:** confirm the two above against the tree as the implementer
finds it, and re-run the harness whole. Nothing else.

## Acceptance

- [x] `resources/board/render.py` and `resources/board/view.css` are byte-identical to what the implementer found — `git diff --name-only` names neither
- [x] The harness reports every check passing with 0 fail and exits 0, and both re-aimed rows stand in it exactly once (31/31 at this run; the denominator is a shared board file three live sessions move, so it is printed, never gated)
- [x] The drawer check fails when the `purpose` div is moved back out of `<aside id="state">` — shown against a scratch copy of the file's text, never against the real file
- [x] The height check fails when the needle is set back to `260px` — shown the same way

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
H=.pearde/prds/one-page-that-says-whats-up/probe/verify.sh
rc=0; bash "$H" > "$W/out" 2>&1 || rc=$?
tail -2 "$W/out"; echo "exit=$rc"
# green means every check passed and none failed. The denominator is NOT pinned:
# this harness is a shared board file and a neighbour adding a passing check
# must not redden this PRD's block.
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
tally="$(python3 "$W/tally.py" "$W/out")"
# the two re-aimed checks still stand in this PRD's own footprint file
drawer="$( { grep -c 'the vision line is in the state drawer' "$H" || true; } )"
height="$( { grep -c "height:calc(100vh - 104px);min-height:280px" "$H" || true; } )"
# neither view file is this PRD's to change
moved="$(git diff --name-only -- resources/board/render.py resources/board/view.css | wc -l | tr -d ' ')"
# non-vacuity, entirely on scratch text — neither real file is written
mut="$(python3 - <<'PY'
s = open('resources/board/render.py').read()
c = open('resources/board/view.css').read()
def drawer(t):
    try:
        a = t.index('<aside id="state"'); j = t.index('id="purpose"')
        z = t.index('</aside>', a)
        return a < j < z
    except ValueError:
        return False
def height(t):
    i = t.find('#stage{display:flex')
    return i >= 0 and 'height:calc(100vh - 104px);min-height:280px' in t[i:i+400]
m = s.replace('    <div id="purpose"></div>\n', '', 1)
n = c.replace('height:calc(100vh - 104px)', 'height:calc(100vh - 260px)')
print('drawer live=%s mutated=%s | height live=%s mutated=%s'
      % (drawer(s), drawer(m), height(c), height(n)))
PY
)"
echo "$mut"
echo "tally=$tally drawer-rows=$drawer height-rows=$height view-files-moved=$moved"
[ "$rc" = 0 ] && [ "${tally##* }" = green ] && [ "$moved" = 0 ] \
  && [ "$drawer" = 1 ] && [ "$height" = 1 ] \
  && [ "$mut" = 'drawer live=True mutated=False | height live=True mutated=False' ]
```
