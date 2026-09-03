Verdict: SPECCED

## What was built

`resources/common.py` gains `prd_shape(dir_path)` — `(fm, title, body, specs,
children, problems)` for one PRD directory, plus the same comment-only-value
fix `resources/board/prdfile.py` `strip_comment` already carried, folded
into `common._clean` so every `common.split_frontmatter` caller gets it.
`resources/guard.py` `fm_state` drops its private `STATE_RE` and reads
through `common.split_frontmatter`. `resources/board/prdfile.py`
`_parse_prd_uncached` drops its private `KEY_RE`/`ITEM_RE` loop and reads
through the same call, keeping `KEY_RE`/`ITEM_RE`/`strip_comment` as aliases
for `plan.py`'s re-export and `specs.py` `fm_lines`'s direct use of
`plan.KEY_RE`.

After the change: `transitions.py`, `collect.py` and `plan.py` (which
already routed every PRD read through `prdfile.py`) and `guard.py` (which
had its own copy) all resolve to one frontmatter reader in `common.py` — a
`grep -E '^(KEY_RE|ITEM_RE|STATE_RE)\s*=\s*re\.compile'` over the four files
finds none. `plan.py scan` against this repo's own live `.pearde` board is
byte-identical before and after. `plan.dispatchable` was not touched.

Built and verified in a scratch clone (`git clone --shared`) of this repo's
own HEAD, not in `.pearde/.lanes/one-prd-reading-primitive` — see Findings.
Probe at `prds/one-prd-reading-primitive/probe/verify.sh`: 5/10 on the
unmodified checkout (the reader doesn't exist yet), 10/10 once the diffs in
the three specs are applied. `.pearde/prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh`
(the committed guard harness): 36 pass/5 fail on both an unmodified clone
and the built one — identical, the 5 pre-existing and unrelated to this PRD.

## Findings

- **The lane for this PRD is another PRD's lane.**
  `.pearde/.lanes/one-prd-reading-primitive`'s `HEAD` (`1be5d2b`) is the
  exact same commit as
  `lane/the-doctor-refuses-drift-one-primitive-one-definition-common-py-gains-a-git-runner-and-a-section-extractor`'s
  tip — a different PRD's lane, three commits ahead of this repo's own
  `HEAD` (`4a94475`) on work (a `run_git`/`section` addition to
  `common.py`) that has nothing to do with this contract and is not on
  `main`. Building on it would have entangled this PRD's diff with a
  sibling's uncommitted-to-main work. I built and verified in a fresh
  `git clone --shared` of the checkout's real `HEAD` instead; the diffs in
  `specs/spec01–03.md` apply cleanly there. This is a lane-creation defect,
  outside this PRD's footprint to fix.
- **The source page's title and body name a different fourth module.**
  The recovered page (`git show 6839a9b:docs/content/docs/improvements/board-prd-primitive.mdx`)
  titles itself "transitions, guard, collect and **lanes**" but the body and
  `## Done when` both say "the **plan**" (`plan.dispatchable`). I took the
  body as authoritative: `resources/board/lanes.py` does no frontmatter
  reading of a `prd.md` at all, so it was never a fourth reader to unify.
- **The `## Done when`'s own malformed-fixture example is wrong.** "A spec
  with no `subject:`" — specs never carry a `subject:` key
  (`references/templates/spec.md`, `resources/board/specs.py`
  `check_spec`); `subject:` is a memo/workflow key. I built the malformed
  fixture as a `prd.md` with no `state:` key and a spec with no closed
  fence instead, which is what `common.prd_shape`'s `problems` and
  `guard.fm_state`/`plan.parse_prd`'s agreement on "no state" actually
  demonstrate.
- **`transitions.py` `fake_prd` and `registry.py` `_scan_one`'s
  children/parent bookkeeping were left alone.** Both already call the one
  frontmatter reader for `(fm, title, body)`; the dict-shaped
  children/parent/board-name graph they build on top serves cross-repo
  `@member/rel` addressing across a whole scan, a different job from
  `prd_shape`'s single-directory child walk. Forcing one onto the other
  would be churn with no acceptance-visible gain, so `common.prd_shape`'s
  specs/children capability stands available (per the PRD's own "The
  change" paragraph) but unused by any of the four modules today beyond the
  frontmatter-parse consolidation the `## Done when` actually measures.
- No gap was auto-enqueued by `knowledge.py query` — the query's hits were
  all weak/unrelated (repo trivia, not this contract), and no new file
  appeared under `.pearde/wiki/pending/` after the run.

## Scores

complexity: 22
blast-radius: mid
workflow: probe-then-spec
