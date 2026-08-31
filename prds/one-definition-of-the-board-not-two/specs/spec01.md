---
complexity: 16
footprint:
  - resources/memos.py
  - resources/questions.py
  - resources/workflows.py
  - resources/knowledge.py
---

# spec01 — every board-root reader agrees with `plan.py find_board`

`memos.py find_board` and `questions.py find_board` stop resolving `<x>/prds`
and resolve `<x>/.pearde` instead, matching `plan.py`'s `BOARD_DIR = ".pearde"`
byte for byte (own `BOARD_DIR` constant duplicated per file, same reason
`guard.py` duplicates it rather than importing across `resources/` and
`resources/board/`). `workflows.py find_board` already delegates to
`memos.find_board`, so it inherits the fix with no body of its own to change.

Fixing board *resolution* alone is not the whole job: every helper that joins
a name onto the old board root (`<x>/prds`, back when `prds/` *was* the
board) now needs to join it onto `<x>/.pearde/prds` instead, or it flips from
silently reading nothing to loudly mislabeling what it reads — a real defect
in its own right, not a cosmetic one. `board_prds()` in `memos.py` had exactly
this: `os.walk(board)` + `relpath(r, board)` treated `.pearde` as the PRD
tree, so every `prds:` reference in a memo mismatched by one path segment and
`memos.py check` went from opening no files to reporting 21 false failures —
including a real, existing PRD (`the-sweep-leaves-nothing-unregistered`).
That helper is already patched in the tree (fixed ahead of this spec, in the
same round); this spec is everything after it.

Two more instances of the identical class, found by running the actual
commands rather than reading the diff: `workflows.py _refs_one()` walked
`board` and computed `relpath(path, board)`, so `workflows.py check` and
`list` still *found* every `workflow:` reference (the PRD tree is a subtree
of `.pearde` either way) but labeled each one `prds/<real-rel>` — one segment
off from `plan.py`'s own convention (`_scan_one`'s `local = relpath(root,
prds_dir(board))`). `questions.py prds()` had the same shape: it walked
`board` and mislabeled every PRD the same way. Both now walk
`os.path.join(board, "prds")` and take `relpath` from there, matching
`plan.py` and the patched `board_prds()`.

`knowledge.py cmd_board` (`resources/knowledge.py:582`) doesn't call
`find_board` — it derives the board root itself from `store.root.parent`
(`.pearde/wiki`'s parent) and had the reverse mistake: it called that
directory `prds` in a comment and used it directly as the PRD tree. Measured:
`python3 resources/knowledge.py board` wrote all 68 PRD notes to
`<KB>/board/prds/<name>.md` instead of `<KB>/board/<name>.md`, and its
`(prds / "memos")` glob happened to still find the real memos only because
the mislabeled variable actually held `.pearde`, not `.pearde/prds` — one
correct access and one wrong slug, from the same bad variable. Split into
`board_root` (`.pearde`) and `prds` (`.pearde/prds`); `board_root / "memos"`
replaces the old `prds / "memos"`.

## What the probe already left in the tree

Built in place — every file above already carries the fix; there is no
separate fixture copy. `.pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh`
is the harness: 20 checks, sections A–G, run from the code repo root. Every
count it asserts is read from disk at run time (memo files, workflow atomics,
`prd.md` files), not a hardcoded snapshot — the board keeps moving under
concurrent sessions.

## Decision the build made

`_refs_one` and `questions.prds()` return early (empty) when `<board>/prds`
does not exist, rather than raising — a board mid-`init`, before its first
PRD, is not an error for a reader that only reports what is there.

## Finding — out of this footprint, not fixed here

`resources/board/transitions.py` `add()` — the body `cmd_add` calls — computes
`rel = os.path.relpath(d, board)` at transitions.py:574 and again at
transitions.py:584, where `d = os.path.join(planlib.prds_dir(board), slug)`.
That is `relpath` from `.pearde`, not from `.pearde/prds`, so a PRD created
through `/new` is recorded in the transitions journal and printed as
`prds/<slug>`, while `plan.py _scan_one` reads the same PRD back as `<slug>`
on the very next scan (plan.py:230, `local = os.path.relpath(root,
scan_root)`). The `slug is taken` error at transitions.py:569 carries the same
mislabel.

Confirmed by the implementer by simulation, not by creating a real PRD:
`os.path.relpath(os.path.join(plan.prds_dir(board), 'a-new-prd'), board)` is
`prds/a-new-prd` while `os.path.relpath(..., plan.prds_dir(board))` is
`a-new-prd`. The neighbouring `relpath` calls at transitions.py:389 and
transitions.py:416 are *not* instances — both anchor on `planlib.repo_root`,
which is the intended anchor for a repo-relative path.

It sits outside `memos.main`/`workflows.main`/`questions.main` — the callers
this PRD names — and outside this spec's footprint, so it is reported rather
than folded in.

## Acceptance

Every box below was re-run by the implementer against the tree as it stands,
not carried over from the build. Counts moved between the two runs — the board
is live (68 → 71 PRDs, 16 → 17 memos) — so each box quotes the run that ticked
it.

- [x] `bash .pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh` from the code repo root prints `20 checks · 20 pass · 0 fail` / `verify.sh done, fail=0`. Re-run: that exact pair of lines. The harness now carries its own verdict (`exit $(( fail != 0 ))`); proved it can fail by running a copy with one forced `bad` — `21 checks · 5 pass · 16 fail`, exit 1.
- [x] `python3 resources/memos.py list .pearde` lists every memo on disk and exits 0; `check` opens them and reports on frontmatter. Re-run: `list` printed 17 rows against 17 `.md` files in `.pearde/memos/`; `check` exited 0. Proved `check` is not silently-green over an unopened directory — on a scratch fixture board it printed `bad-memo.md: missing \`memo:\``, `bad-memo.md: \`prds: no-such-prd\` is not a PRD on this board` and exited 1, while the fixture's real `real-prd` was *not* flagged. That last pair is the direct proof `board_prds()` anchors on `<board>/prds`: the 21 false failures reported earlier this round would have flagged the existing PRD too.
- [x] `python3 resources/workflows.py list .pearde` lists every atomic and workflow on disk; `python3 resources/questions.py list .pearde` reports the PRDs carrying a `## Questions` round. Re-run: workflows `list` printed 18 rows against 18 `.md` files in `.pearde/workflows/`; questions `list` printed nothing against `grep -rl '^## Questions' .pearde/prds --include=prd.md` = 0. Proved neither reader is blind: on the fixture, `questions.py list` printed `asks-a-question  1 asked  0 answered  question` and `workflows.py check` printed ``asks-a-question/prd.md: `workflow: no-such-workflow` names no workflow in the library`` (exit 1) — both labels with no `prds/` prefix.
- [x] All four commands agree with no argument, with `.pearde`, and with the repo root. Re-run: `list` output md5-identical across four forms — no-arg from the repo root, `.pearde`, the absolute repo root, and no-arg from a deep cwd (`resources/board/`) — for all three tools. `memos.find_board` and `questions.find_board` return `/Users/feb/dev/infra/pearde/.pearde` for all three argument forms, byte-identical to `plan.find_board`. Error path re-run both ways: cwd walk gives `<tool>: no .pearde/ board found walking up from the cwd`, an explicit argument gives `<tool>: no .pearde/ board at <path>`, exit 1, each with its own prefix.
- [x] `resources/doctor.sh`'s `memos`, `workflows`, `questions` rows report counts matching disk. Re-run: `memos ok 17 memos · frontmatter checks out` (disk 17), `workflows ok 5 workflows · 13 atomics · the library checks out` (5+13 = 18, disk 18), `questions ok no PRD carries a round — nothing is waiting on you` (disk 0). The rows doctor still calls broken are `skills`, `guard` and `origin` — none in this footprint, all owned elsewhere.
- [x] No board is resolved to `<x>/prds` in `resources/memos.py`, `resources/questions.py` or `resources/workflows.py`, and a `settings.md` override still redirects. Re-run: `grep -n '"prds"' ...` returns six lines — the `OPTIONAL` key tuple and a `fm.get("prds")` read in `memos.py`, a stop-word list in `questions.py`, and three deliberate `os.path.join(board, "prds")` descents (`memos.py:125`, `questions.py:167`, `workflows.py:206`). Swept the whole path arithmetic of all four files, not just their resolvers: every `os.walk`/`relpath`/`join` is anchored on the right level. Override proved live, not just unedited — a fixture `settings.md` with `memos: ../elsewhere-memos` made `list` return the external memo and `memos_dir`/`workflows_dir` return the external paths with `external=True`; removing it returned the reader to the board's own directory.
- [x] `python3 resources/knowledge.py board` writes every PRD note to `<KB>/board/<name>.md`, never `<KB>/board/prds/<name>.md`. Re-run from a deleted `wiki/board/`: `board: 71 PRD note(s), 17 memos scanned`, `os.path.isdir('.pearde/wiki/board/prds')` is `False`, 71 notes written (37 at the top level, the rest nested one directory per parent PRD — `board/the-tool-keeps-its-word/collect-keeps-its-word.md`), matching 71 `prd.md` files on disk. Spot-checked this PRD's own note: `- [[.pearde/prds/one-definition-of-the-board-not-two/specs/spec01]]`, and that file exists.

## Verify and Proof

```sh
bash .pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh
for f in resources/memos.py resources/questions.py resources/workflows.py resources/knowledge.py; do
  python3 -c "import ast; ast.parse(open('$f').read())" && echo "$f parses"
done
grep -n '"prds"' resources/memos.py resources/questions.py resources/workflows.py
echo "verify block complete"
```
