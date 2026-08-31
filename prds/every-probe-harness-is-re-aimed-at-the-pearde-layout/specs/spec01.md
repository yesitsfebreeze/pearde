---
complexity: 13
footprint:
  - .pearde/prds/a-parked-prd-comes-back/probe/verify.sh
  - .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh
  - .pearde/prds/an-unknown-flag-refuses/probe/verify.sh
  - .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh
  - .pearde/prds/the-board-asks-for-itself/a-question-in-plain-words/probe/verify.sh
  - .pearde/prds/the-board-asks-for-itself/a-question-in-plain-words/probe/fixture.sh
  - .pearde/prds/the-board-asks-for-itself/a-question-in-plain-words/probe/viewprobe.js
  - .pearde/prds/the-board-runs-itself/hunks-land-where-they-came-from/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/the-loop-is-commands/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh
  - .pearde/prds/init-writes-a-board-on-the-pearde-layout/probe/check.sh
---

# spec01 — the five core harnesses, the two smoke probes, and the hardcoded one

The five harnesses the pointer in this PRD's contract names as the core of
the job, plus the two smoke-test probes (`a-parked-prd-comes-back`,
`the-gate-runs-the-harnesses`) that must run to a count line, plus three more
that turned out to share the identical two-breakage shape and were finished
in the same pass, plus the one file that hardcoded an absolute machine path.
Every file here is re-aimed at the `.pearde/` layout: the root-derivation
`..` count is corrected (a top-level probe needs four, a child probe five),
and every place that built or addressed a fixture board as `<dir>/prds`
now builds and addresses it as `<dir>/.pearde` — the `plan.py example <dir>`
convention, confirmed empirically: `example <dir>` writes the board at
`<dir>/.pearde`, never at `<dir>` itself.

The convention landed here, and repeated in every file: a board fixture is
`<D>/.pearde`; `PRDS="<board>/prds"` is a second variable wherever PRD
directories are addressed directly (state files, specs, `.claims/<prd>/`);
`.claims/`, `.state/`, `settings.md`, `vision.md`, `workflows/`, `memos/` sit
at the board root, siblings of `prds/`, never inside it; `.transitions.jsonl`
is `.state/transitions.jsonl`; `.round.md` is `.state/round.md`;
`.history.jsonl` is `.state/history.jsonl`. Two files
(`nothing-left-open/the-line-tells-the-truth/probe/verify.sh` and
`nothing-left-open/a-quoted-walk-is-data/probe/verify.sh`) already held this
shape and were the models; nothing here touches either.

**Already stands** — all fourteen files below are re-aimed and run, from any
directory, by absolute path from `/`:

| harness | denominator | left, and why it is not this PRD's |
|---|---|---|
| `a-parked-prd-comes-back` | 44/44 | — |
| `the-gate-runs-the-harnesses` | 56/57 | `skills/` holds no `.md` at this repo's root — unrelated to the move, pre-existing; and 2 of 36 real harnesses lack the exit-code idiom `census` checks for (also pre-existing) |
| `an-unknown-flag-refuses` | 194/196 | `add()`'s `rel = os.path.relpath(d, board)` in `resources/board/transitions.py` computes relative to the board root, not `prds/`, so a new PRD's line reads `prds/<slug>` instead of `<slug>` — a real regression from the move, but in `resources/`, out of this footprint; and `resources/board/brief.py`'s flag list gained `--worker`, undocumented here |
| `the-tool-keeps-its-word/collect-keeps-its-word` | 101/101 | — |
| `the-board-runs-itself/collect-is-a-command` | 133/133 | — |
| `the-board-runs-itself/specced-is-a-command` | 88/90 | `specs.py` now refuses `--workflow none` outright (`draft the route as ## Route on stdin`) — a behavior change, not a path bug; and `specs.py` imports `datetime`, outside the harness's stdlib allow-list |
| `the-board-runs-itself/transitions-are-commands` | 59/74, and **the box this PRD names — "the line opens with the transition" — passes** | the `asking` fixture's own Q3 quotes a backtick, which `questions.py` now refuses (7 boxes, pre-existing fixture content, not a path bug); the same `add()` regression above (3 boxes); `resources/board/plan.py`'s `members()` appends `/prds` to a member's path, and `_scan_one()` also calls `prds_dir()` on it — doubled, so a master board finds no member PRDs at all (4 boxes) — a real `resources/` regression from the move, out of this footprint |
| `the-board-asks-for-itself/a-question-in-plain-words` | 11/11 | — |
| `the-board-runs-itself/hunks-land-where-they-came-from` | 47/47 | — |
| `the-board-runs-itself/the-loop-is-commands` | 59/60 | `references/parts/loop.md` is 155 lines, over its own 120-line ceiling — unrelated to the move |
| `the-board-runs-itself/init-asks-nothing` | 76/89 | `pearde init` (the CLI, not `init.py` alone) now also writes `memos/`, `workflows/`, `.obsidian/`, registers with the daemon and turns the guard on, and `.gitignore` gained two more lines and folded four file-entries into one directory entry — a real feature grown since this harness was written, not a path bug |
| `init-writes-a-board-on-the-pearde-layout/probe/check.sh` | PASS | — the absolute `BOARD_PY=/Users/feb/dev/infra/pearde/resources/board` is now `ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"` |

Every "left" item above is a finding, not a gap in this spec: none of it is a
root-derivation or `--board <x>/prds` bug, each is named with its file and
cause, and every one is outside `resources/`'s ban or is fixture content this
PRD does not own widening.

## Acceptance

- [x] `bash .pearde/prds/a-parked-prd-comes-back/probe/verify.sh` prints `44 checks · 44 pass · 0 fail`
- [x] `bash .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh` prints `57 checks · 56 pass · 1 fail`
- [x] `bash .pearde/prds/an-unknown-flag-refuses/probe/verify.sh` prints `verify: 196 checks · 194 pass · 2 fail`
- [x] `bash .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh` prints `101 checks · 101 pass · 0 fail`
- [x] `bash .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh` prints `133 checks · 133 pass · 0 fail`
- [x] `bash .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh` prints `verify: 88/90 checks pass`
- [x] `bash .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh` prints `ok   the line opens with the transition` and a final count of `74 checks · 59 pass · 15 fail`
- [x] `bash .pearde/prds/the-board-asks-for-itself/a-question-in-plain-words/probe/verify.sh` has no `FAIL` line
- [x] `bash .pearde/prds/the-board-runs-itself/hunks-land-where-they-came-from/probe/verify.sh` prints `47 checks · 47 pass · 0 fail`
- [x] `bash .pearde/prds/the-board-runs-itself/the-loop-is-commands/probe/verify.sh` prints `60 checks · 59 pass · 1 fail`
- [x] `bash .pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh` prints `89 checks · 76 pass · 13 fail`
- [x] `bash .pearde/prds/init-writes-a-board-on-the-pearde-layout/probe/check.sh` prints `PASS` and exits 0, run both from the repo root and from `/`
- [x] every file above, invoked by its absolute path from `/`, resolves its root to `/Users/feb/dev/infra/pearde` — none hardcodes a machine path

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/a-parked-prd-comes-back/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/an-unknown-flag-refuses/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-board-asks-for-itself/a-question-in-plain-words/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-board-runs-itself/hunks-land-where-they-came-from/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-board-runs-itself/the-loop-is-commands/probe/verify.sh </dev/null 2>&1 | tail -1
bash .pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh </dev/null 2>&1 | tail -1
bash /Users/feb/dev/infra/pearde/.pearde/prds/init-writes-a-board-on-the-pearde-layout/probe/check.sh
echo "spec01: fourteen files re-aimed, denominators checked above"
```
