---
complexity: 10
footprint:
  - references/templates/atomic.doc.md
  - references/templates/memo.doc.md
  - references/templates/prd.doc.md
  - references/templates/report.doc.md
  - references/templates/spec.doc.md
  - references/templates/vision.doc.md
  - references/templates/workflow.doc.md
---

# spec03 — the seven `.doc.md` companions are rewritten dense

The seven files documenting each template — how to fill it and why each line is
there — carry the same facts in fewer words. No code reads them: their only
reader is a person or a worker, so the whole file is prose surface. They are
the densest opportunity in this PRD, 60% of their words in paragraphs and
bullets.

Already standing, uncommitted in the lane: `report.doc.md` rewritten, 275 → 249
words (9.5%), `prose.py check` green. That file is 93% prose and took the
largest cut of any file the probe touched — the honest ceiling for the group.

One wrong claim to correct while rewriting, found by running the writer:
`atomic.doc.md` and `workflow.doc.md` both say `pearde workflow add` "takes the
body from the template's shape". It does not. `workflows.py add` checks only
that `references/templates/<kind>.md` **exists**, writes the frontmatter itself,
and takes the body on stdin. Say what the writer does.

## Acceptance

- [x] `python3 resources/prose.py check references/templates/*.doc.md` exits 0.
- [x] The group's words, `prose.py`'s own count, fall from 2456 to **2301 or fewer** — `prose.py stat <base>` summed over the group's lines. 6.3% off, the measured floor, and the check fails on the count itself.
- [x] Every table row of the base revision survives as a row: each file's count of lines beginning `|` is unchanged or higher.
- [x] Every frontmatter key named in a table — `prd.doc.md`'s fifteen, `spec.doc.md`'s four, `memo.doc.md`'s ten, `atomic.doc.md`'s and `workflow.doc.md`'s five each, `vision.doc.md`'s three — is still named, spelled identically.
- [x] Every state name, settings key, default value and command in the base text survives character-identical: `open` `analyzing` `refine` `question` `specced` `claimed` `blocked` `done` `failed` `deferred`, `split-above`, `specs-above`, the defaults 40 and 6, and every `pearde <verb>` and `resources/*.py` path.
- [x] `atomic.doc.md` and `workflow.doc.md` say the body comes from stdin and the template is existence-checked; neither says the body comes from the template.
- [x] Every heading of the base revision survives with the same text, and no file gains or loses a section.
- [x] `python3 resources/index.py check` names no `@` in `references/templates/`.

## Verify and Proof

```sh
BASE=${BASE:-$(git merge-base HEAD main)}
set -e
python3 resources/prose.py check references/templates/atomic.doc.md references/templates/memo.doc.md \
  references/templates/prd.doc.md references/templates/report.doc.md references/templates/spec.doc.md references/templates/vision.doc.md \
  references/templates/workflow.doc.md

# every table row survives as a row, and no heading moved
for f in references/templates/*.doc.md; do
  a=$(git show "$BASE:$f" | grep -c '^|' || true)
  b=$(grep -c '^|' "$f" || true)
  [ "$b" -ge "$a" ] || { echo "$f: $a table rows -> $b"; exit 1; }
  git show "$BASE:$f" | grep '^#' > /tmp/h.old
  grep '^#' "$f" > /tmp/h.new
  diff /tmp/h.old /tmp/h.new || { echo "$f: headings changed"; exit 1; }
done

# every state name, settings key and default survives, character-identical
for w in open analyzing refine question specced claimed blocked done failed \
         deferred split-above specs-above; do
  grep -qr -- "$w" references/templates/prd.doc.md || { echo "prd.doc.md lost $w"; exit 1; }
done

# the corrected claim: workflows.py takes the body on stdin
if grep -l 'body from the template' references/templates/*.doc.md; then
  echo "the wrong claim about workflows.py add is still on disk"; exit 1
fi

if python3 resources/index.py check | grep -q '^references/templates/'; then
  echo "a dangling @ under references/templates/"; exit 1
fi
# the ceiling, on prose.py's own count
python3 resources/prose.py stat "$BASE" | grep '\.doc\.md:' \
  | awk -F'[ >]+' '{b+=$2; a+=$4} END {
      printf "group: %d -> %d (%.1f%% off)\n", b, a, 100*(b-a)/b;
      if (a > 2301) { printf "over the %d ceiling\n", 2301; exit 1 } }'
```
