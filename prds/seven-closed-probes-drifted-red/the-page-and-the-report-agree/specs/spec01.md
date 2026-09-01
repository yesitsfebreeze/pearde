---
complexity: 4
footprint:
  - .pearde/report.md
  - .pearde/prds/one-page-that-says-whats-up/probe/verify.sh
---

# spec01 — the live report takes the four-part shape, and one-page's stage-height checks pin the rule the tree carries

`.pearde/report.md` is rewritten whole into the shape three committed things
name — the four parts in `references/report.md`, the skeleton in
`references/templates/report.md`, and `reportParts()` in
`resources/board/view.js`, which reads title, lede, In work and Planned off
the file. Beside that, the two stage-height checks in one-page's probe harness
stop asserting the retired rule (`height:min(74vh,720px)`, no `calc(`) and pin
what the tree now carries instead: the measured-era fallback
`height:calc(100vh - 260px);min-height:280px` and the CSS comment that records
the constraint was retired deliberately, not dropped.

## What the probe already established

The build is done; this spec records it. Rewrote `.pearde/report.md` in the
four-part shape from a fresh board scan; replaced the two failing checks in
one-page's `verify.sh` with three that pin the current rule (the fallback plus
its floor, the retired-constraint comment, and the JS that measures — the
third replaces the count, not the pair, since the harness had exactly two
stage-height lines failing). Harness output after the change:

```
31 checks · 31 pass · 0 fail
```

`python3 resources/index.py check` exits 0, prints nothing. Nothing under
`resources/` changed; the report file parses to a person and is parsed by
nothing, so no other harness reads it.

## Acceptance

- [x] `sed -n '3p' .pearde/report.md` is a dateline `*YYYY-MM-DD*`, and `grep -c '^## \(Planned\|In work\|Undecided or failing\)' .pearde/report.md` reports 3 — the four parts after the title
- [x] `bash .pearde/prds/one-page-that-says-whats-up/probe/verify.sh` prints `31 checks · 31 pass · 0 fail` — the two stage-height checks now pin `height:calc(100vh - 260px);min-height:280px` and the `retired deliberately, not dropped by accident` comment
- [x] `grep -q 'st.style.height = Math.max(280' resources/board/view.js` — the measured height is still written by script, not only by the stylesheet
- [x] `python3 resources/index.py check` exits 0 and prints nothing

## Verify and Proof

```sh
bash .pearde/prds/one-page-that-says-whats-up/probe/verify.sh
grep -c '^## \(Planned\|In work\|Undecided or failing\)' .pearde/report.md
python3 resources/index.py check
```