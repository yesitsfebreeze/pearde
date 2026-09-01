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

- [ ] `resources/board/render.py` and `resources/board/view.css` are byte-identical to what the implementer found — `git diff --name-only` names neither
- [ ] The harness reports 31 checks, 31 pass, 0 fail, and exits 0
- [ ] The drawer check fails when the `purpose` div is moved back out of `<aside id="state">` — shown against a scratch copy of the file's text, never against the real file
- [ ] The height check fails when the needle is set back to `260px` — shown the same way

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/one-page-that-says-whats-up/probe/verify.sh; echo "exit=$?"
git diff --name-only -- resources/board/render.py resources/board/view.css
# non-vacuity, entirely on scratch text — neither real file is written
python3 - <<'PY'
s=open('resources/board/render.py').read()
def pred(t):
    try:
        a=t.index('<aside id="state"'); j=t.index('id="purpose"'); z=t.index('</aside>',a)
        return a<j<z
    except ValueError: return False
m=s.replace('    <div id="purpose"></div>\n','',1)
print("live:", pred(s), "| purpose out of the drawer:", pred(m))
PY
sed 's/height:calc(100vh - 104px)/height:calc(100vh - 260px)/' resources/board/view.css \
  | grep -A1 '^#stage{display:flex' | grep -q 'height:calc(100vh - 104px);min-height:280px' \
  && echo "VACUOUS" || echo "height check fails on a changed rule"
```
