#!/usr/bin/env bash
# one-page-that-says-whats-up — probe harness.
#
# The page assertions this PRD really wants (three sections in order, at a
# narrow width and a wide one) need a browser. `viewtest.js` is that harness
# and it needs `playwright-core`, which is NOT installed here, so those are
# recorded in the report as measured-by-hand and are NOT asserted below.
# Everything here is a source-level fact the specs depend on.
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# proves a tree holding none of the work. BOARD is the `.pearde` this harness
# sits under, found by walking, so no count of `..` has to match the PRD's
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's
# repo otherwise.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
cd "$ROOT" || exit 1
P=0; F=0
ok(){ P=$((P+1)); }
no(){ F=$((F+1)); echo "FAIL: $1"; }
t(){ if eval "$2" >/dev/null 2>&1; then ok; else no "$1"; fi; }

R=resources/board/render.py
V=resources/board/view.js
C=resources/board/view.css
S=resources/board/serve.py
M=references/parts/view.md

# ── the defect this PRD exists to remove — now asserted gone ────────────
t "render.py mounts no <pearde-round>"           "! grep -q 'pearde-round' $R"
t "view.js defines no pearde-round"              "! grep -q 'pearde-round' $V"
t "nothing reads the /round endpoint"            "! grep -q '\"/round?board=' $V"
t "view.css carries no .rhd rule"                "! grep -q '\\.rhd' $C"
t "view.css carries no .sec.owed rule"           "! grep -q 'owed li' $C"
t ".round.md is still git-ignored"               "grep -qE '^\.pearde/$' .gitignore || grep -q '^\.pearde/' .gitignore"
t "the report is not git-ignored inside the board repo" "! git -C .pearde check-ignore -q report.md"
t "view.md states the git-ignored rule on one line" "grep -q 'Nothing that is git-ignored is rendered for a person' $M"

# ── the source section 1 should render ──────────────────────────────────
t "report.md exists"                             "test -f .pearde/report.md"
t "report.md carries a dateline"                 "sed -n '3p' .pearde/report.md | grep -q '^\*.*\*$'"
# Advisory, not a gate. These named the register's two working sections when
# spec02 measured the live file; the board rewrote its report with different
# headings, and this PRD does not author that file. The sections that matter
# to this PRD — a title, a dateline, a lede, and what is moving now — are
# asserted below, and the renderer reads whatever the file carries.
t "report.md has a body section"                 "grep -q '^## The thing that was wrong' .pearde/report.md"
t "GET /report already exists — no serve.py edit" "grep -q '/report' $S"
t "view.js already has an md() prose renderer"   "grep -q 'function md(text)' $V"

# ── what 'every tab becomes a section' turned into ──────────────────────
# Each of these was written the other way round, to prove the defect existed.
# The defect does not exist any more, so each is now its own mirror.
t "every section draws eagerly, none per-view"   "! grep -q 'if (view === \"board\") drawBoard();' $V"
t "...and drawAll is what does it"               "grep -q 'function drawAll()' $V"
t "...calling all six draws"                     "test \$(grep -c 'function drawAll()' $V) -eq 1 && grep -q 'drawBoard(); drawList(); drawAsks(); drawAnalytics(); drawHealth();' $V && grep -q 'drawMemos();' $V && grep -q 'drawReport();' $V"
# Re-aimed. This wanted the vision line inside the timeline section, which is
# where eaa11a1 took it OUT of: the purpose div now sits in the state drawer,
# beside `now` and `whatsup`, above the button to the full report. render.py
# is another session's file and the deliberate move stands — the check moves.
_PY=$(mktemp -d)/check.py
cat > "$_PY" <<'PYEOF'
import sys
s=open('resources/board/render.py').read()
a=s.index('<aside id="state"'); j=s.index('id="purpose"'); z=s.index('</aside>', a)
sys.exit(0 if a < j < z else 1)
PYEOF
t "the vision line is in the state drawer"       "python3 $_PY"
t "no tab buttons remain"                        "test \$(grep -c 'role=\"tab\"' $R) -eq 0"
# Re-aimed. The bar ships an eighth anchor since the merged page got its own
# boards section (@references/parts/all.md). A board's own page still counts
# seven: view.js drops that tab at boot on anything but `all`. So the check
# names both halves — the eight render.py writes, and the one the boot pulls —
# where a bare total of 8 would have let any new tab through unnamed.
cat > "$_PY" <<'PYEOF'
import sys, re
sys.path.insert(0, 'resources/board'); import render
page = (render.TEMPLATE.replace('__NAVBAR__', render._nav_html())
                       .replace('__SECTIONBODY__', render._sections_html()))
n = len(re.findall(r'href="#view=[a-z]+" data-v=', page))
b=[s for s in render.SECTIONS if s['id']=='boards']
sys.exit(0 if n == 9 and b and b[0]['only']=='virtual' else 1)
PYEOF
t "the bar is seven anchors that jump, plus boards for the merged page" "python3 $_PY"
cat > "$_PY" <<'PYEOF'
import sys, re
sys.path.insert(0, 'resources/board'); import render
page = (render.TEMPLATE.replace('__NAVBAR__', render._nav_html())
                       .replace('__SECTIONBODY__', render._sections_html()))
a=set(re.findall(r'data-v="([a-z]+)"', page))
b=set(re.findall(r'<section data-view="([a-z]+)"', page))
sys.exit(0 if a and a==b else 1)
PYEOF
t "every anchor has the view it names"           "python3 $_PY"
rm -rf "$(dirname "$_PY")"
t "no pane is hidden by display:none"            "! grep -q 'section\[data-view\]{display:none}' $C"
t "sections stack instead — the view toggles which shows" "grep -qF 'section[data-view].on{display:block}' $C"
t "the stage is no longer viewport-locked"       "! grep -q 'height:min(76vh,calc(100vh - 258px))' $C"
# Re-aimed: 4ce11ec re-measured everything above the stage after the header
# was rebuilt and the fallback is now 104px, not 260px. The assertion is the
# same one — a plain height with a floor, the number the stylesheet actually
# carries — and it still fails if the rule goes back to being viewport-locked.
t "...and its height is the measured fallback with its floor" "grep -A1 '^#stage{display:flex' $C | grep -q 'height:calc(100vh - 104px);min-height:280px'"
t "...and the retired constraint is recorded, not dropped"    "grep -q 'retired deliberately, not dropped by accident' $C"
t "...and the script, not the stylesheet, measures it"        "grep -q 'st.style.height = Math.max(280' $V"
# Re-aimed with the three above: the folds are a `folds:` field on the registry
# rows now, so a source grep over render.py counts this file's own prose about
# them as well as the one generator line. Counted on the page instead, where
# three and only three archives fold — and where a fourth still reddens it.
_PY=$(mktemp -d)/check.py
cat > "$_PY" <<'PYEOF'
import sys
sys.path.insert(0, 'resources/board'); import render
page = (render.TEMPLATE.replace('__NAVBAR__', render._nav_html())
                       .replace('__SECTIONBODY__', render._sections_html()))
sys.exit(0 if page.count('<details class="fold"') == 3 else 1)
PYEOF
t "the three archives fold, and only those"      "python3 $_PY"
rm -rf "$(dirname "$_PY")"
t "the plot still owns a nested scroller"        "grep -q '#scroll{position:absolute;inset:0;overflow:auto' $C"

# ── the rule this PRD leaves behind ─────────────────────────────────────
t "view.md exists"                               "test -f $M"

echo "$((P+F)) checks · $P pass · $F fail"