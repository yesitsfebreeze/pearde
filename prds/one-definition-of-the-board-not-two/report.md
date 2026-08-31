# Report — one-definition-of-the-board-not-two

Verdict **DONE**. 1 spec, 7 of 7 acceptance boxes ticked, each re-run by the
implementer. Harness: 20 checks · 20 pass · 0 fail.

## Knowledge

`python3 resources/knowledge.py query` against this contract returned 5 hits,
all scout-sweep notes, none relevant — no prior conclusion on record.
`.pearde/wiki/pending/` stayed empty, so no gap was enqueued. Nothing was
learned outside this repo during the implementation round, so nothing was
written back with `knowledge.py remember`.

## What is in the tree

| file | change | state |
|---|---|---|
| `resources/memos.py` | `find_board` resolves `<x>/.pearde`; `board_prds()` walks `<board>/prds` | uncommitted |
| `resources/questions.py` | `find_board` resolves `<x>/.pearde`; `prds()` walks `<board>/prds` | uncommitted |
| `resources/workflows.py` | `_refs_one` walks `<board>/prds`; `find_board` delegates, no body of its own | already committed in `eef2dba` |
| `resources/knowledge.py` | `cmd_board` splits `board_root` (`.pearde`) from `prds` (`.pearde/prds`) | uncommitted |
| `.pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh` | ends `exit $(( fail != 0 ))` — the harness carries its own verdict | new |

`workflows.py` shows no working-tree diff: its `_refs_one` fix landed under a
different PRD's collect (`eef2dba a-route-is-written-at-spec-time`). Verified
present and correct — `git log -S'prds_root = os.path.join(board, "prds")'`
names that commit and no other.

`memos_dir()` and `workflows_dir()` were not edited, as the contract requires.

## The lesson the round actually taught

Fixing `find_board` alone flips a helper from blind to **wrong**, which is
worse. Every helper joining a name onto the old board root had the same
off-by-one-level defect, and none of them raised:

| helper | before | symptom |
|---|---|---|
| `memos.board_prds` | `os.walk(board)` | 21 false `check` failures, one on a PRD that exists — blocked a finished PRD from landing |
| `workflows._refs_one` | `relpath(path, board)` | every `workflow:` ref labelled `prds/<rel>` |
| `questions.prds()` | `os.walk(board)` | every PRD labelled `prds/<name>` |
| `knowledge.cmd_board` | one variable named `prds` holding `.pearde` | 68 notes written to `board/prds/<name>.md`; the `memos` glob was accidentally right |

Swept the full path arithmetic of all four footprint files, not just their
resolvers — every remaining `os.walk`, `relpath` and `join` is anchored on the
right level.

## Proof, re-run rather than inherited

The pre-ticked boxes were not taken on trust. Three of them turned out to rest
on "exit 0 today", which proves nothing about a reader that opens no file, so
each was re-proved against a scratch fixture board built for the purpose:

| reader | proof it is not blind |
|---|---|
| `memos.py check` | flagged ``prds: no-such-prd`` and left the fixture's real `real-prd` alone — the direct proof `board_prds()` anchors correctly, since the old bug flagged existing PRDs too |
| `questions.py list` | printed `asks-a-question  1 asked  0 answered  question`, label with no `prds/` prefix |
| `workflows.py check` | printed ``asks-a-question/prd.md: `workflow: no-such-workflow` names no workflow in the library``, exit 1 |
| `settings.md` override | `memos: ../elsewhere-memos` redirected `list` to the external memo and `memos_dir`/`workflows_dir` to the external paths, `external=True`; removing it returned both to the board |

Live numbers, re-measured: 17 memos = 17 files on disk; 18 workflows+atomics
(doctor: 5 workflows · 13 atomics) = 18 files on disk; 0 open question rounds
= 0 `grep -rl '^## Questions'` hits; 71 PRD notes = 71 `prd.md` on disk, with
no `wiki/board/prds/` subtree. `list` output is md5-identical across four
invocation forms (no-arg, `.pearde`, absolute repo root, no-arg from a deep
cwd) for all three tools, and `memos.find_board`/`questions.find_board` return
the same absolute path as `plan.find_board` for every argument form. Error
paths keep their own prefixes both ways: `<tool>: no .pearde/ board found
walking up from the cwd` and `<tool>: no .pearde/ board at <path>`, exit 1.

The harness was made able to fail — it ended on an `echo`, so it exited 0
whatever it found. It now ends `exit $(( fail != 0 ))`; a copy with one forced
`bad` printed `21 checks · 5 pass · 16 fail` and exited 1.

## Findings — not fixed, out of this footprint

1. **`resources/board/transitions.py` `add()`** (the body `cmd_add` calls)
   computes `rel = os.path.relpath(d, board)` at transitions.py:574 and again
   at transitions.py:584, where `d = os.path.join(planlib.prds_dir(board),
   slug)`. That anchors on `.pearde`, not `.pearde/prds`, so a PRD created
   through `/new` is journalled and printed as `prds/<slug>` while
   `plan.py _scan_one` (plan.py:230) reads the same PRD back as `<slug>` on the
   next scan. transitions.py:569's `slug is taken` error carries the same
   mislabel. Confirmed by simulation, not by creating a real PRD.
   `relpath` at transitions.py:389 and :416 are **not** instances — both anchor
   on `planlib.repo_root`, which is correct there. Same defect class as
   everything this PRD fixed; it belongs to whichever PRD owns
   `transitions.py`.

2. **The spec's `footprint:` names `prds/one-definition-of-the-board-not-two/probe/verify.sh`**
   — no such path exists from the code repo root; the file is at
   `.pearde/prds/...`. Left as written, since frontmatter is not the
   implementer's to edit. Corrected in the spec body, where it was repeated.

3. **`doctor.sh` still calls `skills`, `guard` and `origin` broken.** None is
   in this footprint and none was touched. `plan`, `harnesses` and `jstests`
   are `off`, not broken.

## Scores

complexity: 16
blast-radius: mid
workflow: none fit
