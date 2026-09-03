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
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's repo
# otherwise.
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
# one-section-registry made render.py generate the header bar and the section
# wrappers from its own SECTIONS list, so the three checks below that used to
# grep the hand-typed markup out of render.py's source now read the page that
# source writes. Same rules, same failure modes — a stray hand-written anchor
# or section anywhere in TEMPLATE still reddens them — read one level later.
PAGE="import sys; sys.path.insert(0, 'resources/board'); import render
page = (render.TEMPLATE.replace('__NAVBAR__', render._nav_html())
                       .replace('__SECTIONBODY__', render._sections_html()))"

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
t "report.md has an '## In work' section"        "grep -q '^## In work' .pearde/report.md"
t "report.md has a '## Planned' section"         "grep -q '^## Planned' .pearde/report.md"
t "GET /report already exists — no serve.py edit" "grep -q '/report' $S"
t "view.js already has an md() prose renderer"   "grep -q 'function md(text)' $V"

# ── what 'every tab becomes a section' turned into ──────────────────────
# Each of these was written the other way round, to prove the defect existed.
# The defect does not exist any more, so each is now its own mirror.
t "every section draws eagerly, none per-view"   "! grep -q 'if (view === \"board\") drawBoard();' $V"
t "...and drawAll is what does it"               "grep -q 'function drawAll()' $V"
t "...calling all six draws"                     "test \$(grep -c 'if (!replaced.has(' $V) -eq 6"
t "the plan toolbar is inside its own section"   "python3 -c \"\$PAGE
i=page.index('<section data-view=\\\"timeline\\\"'); j=page.index('id=\\\"tcontrols\\\"')
k=page.index('</section>', i)
sys.exit(0 if i<j<k else 1)\""
# Re-aimed. This wanted the vision line inside the timeline section, which is
# where eaa11a1 took it OUT of: the purpose div now sits in the state drawer,
# beside `now` and `whatsup`, above the button to the full report. render.py
# is another session's file and the deliberate move stands — the check moves.
t "the vision line is in the state drawer"       "python3 - <<'PY'
import sys
s=open('resources/board/render.py').read()
a=s.index('<aside id=\"state\"'); j=s.index('id=\"purpose\"'); z=s.index('</aside>', a)
sys.exit(0 if a < j < z else 1)
PY"
t "no tab buttons remain"                        "test \$(grep -c 'role=\"tab\"' $R) -eq 0"
# Re-aimed. The bar ships an eighth anchor since the merged page got its own
# boards section (@references/parts/all.md). A board's own page still counts
# seven: view.js drops that tab at boot on anything but `all`. So the check
# names both halves — the eight render.py writes, and the one the boot pulls —
# where a bare total of 8 would have let any new tab through unnamed.
t "the bar is seven anchors that jump, plus boards for the merged page" "test \$(python3 -c \"\$PAGE
import re; print(len(re.findall(r'href=\\\"#view=[a-z]+\\\" data-v=', page)))\") -eq 8 && python3 -c \"import sys; sys.path.insert(0, 'resources/board'); import render
b=[s for s in render.SECTIONS if s['id']=='boards']
sys.exit(0 if b and b[0]['only']=='virtual' else 1)\" && grep -q 's.only === \"virtual\"' $V"
t "every anchor has the view it names"           "python3 -c \"\$PAGE
import re
a=set(re.findall(r'data-v=\\\"([a-z]+)\\\"', page))
b=set(re.findall(r'<section data-view=\\\"([a-z]+)\\\"', page))
sys.exit(0 if a and a==b else 1)\""
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
t "the three archives fold, and only those"      "test \$(python3 -c \"\$PAGE
print(page.count('<details class=\\\"fold\\\"'))\") -eq 3"
t "the plot still owns a nested scroller"        "grep -q '#scroll{position:absolute;inset:0;overflow:auto' $C"

# ── the rule this PRD leaves behind ─────────────────────────────────────
t "view.md exists"                               "test -f $M"

echo "$((P+F)) checks · $P pass · $F fail"
[ "$F" -eq 0 ] || exit 1
