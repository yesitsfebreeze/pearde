---
complexity: 21
footprint:
  - .pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh
  - .pearde/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/one-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/the-page-shows-the-round/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/too-big-splits-itself/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/tokens-per-transition/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/vision-is-first-class/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/the-next-line-runs/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/an-example-board/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-skill/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-attach/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-reader/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-seed/probe/verify.sh
  - .pearde/prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh
  - .pearde/prds/check-crosses-member-boundaries/probe/verify.sh
  - .pearde/prds/check-crosses-member-boundaries/probe/fixture.sh
  - .pearde/prds/complexity-is-guarded-like-priority/probe/verify.sh
  - .pearde/prds/one-page-that-says-whats-up/probe/verify.sh
---

# spec02 — the remaining twenty-two harnesses, the same two breakages

Every file listed in `footprint:` has had its root-derivation `..` count
corrected already (child probes to five, the one non-`/probe/` file —
`workflow-reader/verify.sh` — to four) and none of them die or hardcode a
machine path; `bash <file> </dev/null` run by absolute path from `/` reaches
its own count line on every one, measured on arrival for this spec:

`guard-on-is-one-command` 64/78 · `one-predicate-for-dispatchable` 23/53 ·
`one-command` 43/54 · `brief-is-printed` 41/104 · `the-page-shows-the-round`
14/29 · `too-big-splits-itself` 16/60 · `tokens-per-transition` 3/43 ·
`vision-is-first-class` 18/52 · `the-next-line-runs` 70/96 · `an-example-board`
30/37 · `readme-in-three-rings/quickstart.sh` 24/31 ·
`readme-in-three-rings/verify.sh` 65/72 · `workflow-skill` (fails at its
first check) · `workflow-improve` 63/71 · `workflow-attach` 29/46 ·
`workflow-reader` 5/39 · `workflow-seed` 33/48 · `the-skill-tree-is-guarded`
22/41 · `check-crosses-member-boundaries` 6/18 · `complexity-is-guarded-like-priority`
19/61 · `one-page-that-says-whats-up` 22/30.

What is left on every one is the second breakage: each still builds or
addresses at least one fixture board as `<dir>/prds` — a bare `example
"<dir>"` call whose result is then read at `<dir>/prds/...` instead of
`<dir>/.pearde/prds/...`, a hand-built fixture that `mkdir -p`s `<dir>/prds`
directly, or a `--board <dir>/prds` that should be `--board <dir>/.pearde`.
`spec01`'s eleven finished harnesses are the worked examples of the fix,
covering every shape this footprint holds:

- `plan.py example <dir>` lands the board at `<dir>/.pearde`, never at
  `<dir>` — confirmed empirically, not assumed. A fixture that calls
  `example "$D"` and then reads `"$D/prds/..."` reads `"$D/.pearde/prds/..."`
  after the fix.
- A hand-built fixture (`mkdir -p "$D/prds/<name>"`, `cat > "$D/prds/settings.md"`)
  moves its board root to `"$D/.pearde"`: PRD directories to
  `"$D/.pearde/prds/<name>"`, and `settings.md`, `vision.md`, `workflows/`,
  `memos/` to `"$D/.pearde/"` directly — they are board-root siblings of
  `prds/`, not its children.
- `.transitions.jsonl` is `.state/transitions.jsonl`; `.round.md` is
  `.state/round.md`; `.history.jsonl` is `.state/history.jsonl`; `.claims/`
  stays directly under the board root. A fixture that needs `.state/` before
  the first write may `mkdir -p "<board>/.state"` as a marked workaround —
  `example` does not write it, and that gap is `state-dir-belongs-to-the-board`'s,
  not this PRD's to close.
- Where a script both drives `--board <dir>/prds` as a CLI argument and reads
  PRD files directly, splitting `B` (board root, for `--board`) from a second
  `PRDS="$B/prds"` (for PRD-directory paths) keeps every reference honest
  without renaming the whole file — the pattern `specced-is-a-command` and
  `the-loop-is-commands` in spec01 both use.

No assertion is added, removed or weakened by this spec: the fix is the
board-path substitution alone, and every harness's own denominator — the
total the file itself prints — stays exactly where it is. A harness that,
once re-aimed, still fails on something that is not a board path (fixture
content, or a real bug in `resources/`) is a finding for this spec's report,
the same way spec01's eleven were — not a box to force closed.

## Acceptance

- [x] Every file in `footprint:` resolves its root to `/Users/feb/dev/infra/pearde` when run by absolute path from `/`, and none hardcodes a machine path
- [x] `grep -rn -- '--board [^ ]*prds' .pearde/prds --include='*.sh'` finds nothing under any path in this spec's `footprint:` (the one standing exception board-wide, `collect-keeps-its-word`'s `run_old`, is outside this footprint and deliberately unchanged — it drives a pinned pre-move `collect.py`)
- [x] No fixture in this footprint builds or addresses a board at `<dir>/prds`; each is `<dir>/.pearde`, with `prds/`, `.claims/`, `.state/`, `settings.md`, `vision.md`, `workflows/` and `memos/` at the positions spec01 established
- [x] Every file in `footprint:` runs to its own count line with no crash, no Python traceback, and no `no .pearde/ board at` / `no example board` refusal
- [x] `git -C .pearde diff --stat -- prds` over this footprint holds only path and root-derivation hunks — the number of `check`/`t`/`ok`/`eq`/`has` call sites in each file, run before and after, is unchanged
- [x] No file under `resources/` is modified by this spec

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
for f in \
  .pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh \
  .pearde/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/one-command/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/the-page-shows-the-round/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/too-big-splits-itself/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/tokens-per-transition/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/vision-is-first-class/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/the-next-line-runs/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/an-example-board/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh \
  .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh \
  .pearde/prds/workflows-on-the-board/workflow-skill/probe/verify.sh \
  .pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh \
  .pearde/prds/workflows-on-the-board/workflow-attach/probe/verify.sh \
  .pearde/prds/workflows-on-the-board/workflow-reader/verify.sh \
  .pearde/prds/workflows-on-the-board/workflow-seed/probe/verify.sh \
  .pearde/prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh \
  .pearde/prds/check-crosses-member-boundaries/probe/verify.sh \
  .pearde/prds/complexity-is-guarded-like-priority/probe/verify.sh \
  .pearde/prds/one-page-that-says-whats-up/probe/verify.sh \
; do
  echo "== $f =="
  bash "/Users/feb/dev/infra/pearde/$f" </dev/null 2>&1 | tail -1
done
find .pearde/prds -name '*.sh' -print0 | xargs -0 grep -ln -- '--board [^ ]*prds' 2>/dev/null
echo "spec02: twenty-two files measured above, the census is the record"
```
