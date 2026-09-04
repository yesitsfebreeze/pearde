# one primitive one definition — analyst pass two

Verdict: REFINE

Both questions from pass one are answered: Q1 picked "clean them up now" —
the check ships naming all thirty-seven and the same job folds every copy
into `resources/common.py`; Q2 picked "write the two missing ones" — a git
runner and a section extractor join `common.py`. Together that is the
contract now. The build (this pass) tried to do exactly that and hit a wall
wide enough to be several contracts, not one.

## What this pass built on top of pass one

Pass one's `resources/primitives.py` and the `primitives` row in
`resources/doctor.sh` still stand, uncommitted, unchanged — they are the
mechanism, not the fold. This pass read every one of the 37 flagged
definitions (`python3 resources/primitives.py list resources`) to attempt
the fold Q1 asks for, starting with the git runner and section extractor
Q2 asks for.

## What the read turned up: one name, several contracts

`git()` is defined seven times and none of the seven agree on what it does
on failure. `board/lanes.py` raises `LaneError`; `board/shared.py` raises
`Refused`; `board/collect.py`'s `git_out` raises `Stop` and also branches on
a private git index environment variable for `private_index`; `board/repos.py`
returns `None`; `board/orphans.py` returns `""`; `resources/health.py`'s
`_git` returns `None`. Writing "a git runner" into `common.py` is not typing
one function — it is choosing which of six behaviours becomes the shared one
and deciding whether the other five keep their own wrapper around it.

The same is true of the nine section extractors: `board/collect.py`'s
`section` returns `""` on a miss, `resources/workflows.py`'s returns a list
of lines or `None`, `board/specs.py` carries two different ones (`h2_line`
returns a line number, `section_text` a string), `resources/questions.py`'s
`sections` returns a list of `(heading, body)` pairs. One shared function
cannot be all of these return shapes at once without every caller changing,
and "without changing its own behaviour on failure" — the bar the board
resolver shims already clear — is not achievable for git or sections without
a signature wide enough to name each shape (`check=`, `default=`, `raise_as=`).

The board resolvers are closer to done — `resources/grammar.py`,
`resources/health.py` and `resources/memos.py` already delegate with a
matching `(d)`/`(d, prog)` signature — but not uniformly: `resources/guard.py`
and `resources/board/boards.py` both carry a `board_scanned(d)` with no
`prog` argument, one silent on two boards, the other raising through its own
`die()`. Folding those into `common.board_scanned(d, prog)` changes what a
caller sees on the two-boards case, which is a decision for whoever owns
each file, not a mechanical rename.

## Why this is REFINE and not SPECCED

Thirty-seven copies across seventeen files (`resources/guard.py`,
`health.py`, `knowledge.py`, `questions.py`, `workflows.py`,
`board/boards.py`, `collect.py`, `edit.py`, `lanes.py`, `orphans.py`,
`prdfile.py`, `ramp.py`, `refuse.py`, `repos.py`, `shared.py`, `specs.py`,
`transitions.py`), each needing its own judgment call about a preserved
failure contract, is not six specs at complexity forty — it is a spec near
enough to one per file. `common.py` gaining a git runner and a section
extractor is its own contract, hit before any fold can start, and everything
after it is independent per file. That is more than one contract under this
PRD's name.

## Findings outside this contract

- `resources/index.py check` still reports `resources/primitives.py is on
  disk with no row in references/files.md` — pass one's finding, unchanged
  this pass; not fixed here because no child below touches
  `resources/primitives.py` itself.
- Baseline unmoved: `index broken 4 · vault broken · origin broken · health
  broken · knowledge broken` were red before this PRD existed and stay red
  for reasons this PRD does not touch.

## Split

The common.py addition is the one thing every fold needs; the three fold
children own disjoint sets of files and run at once once it lands.

| child | contract | needs |
|---|---|---|
| `common-py-gains-a-git-runner-and-a-section-extractor` | `resources/common.py` holds one git runner and one section extractor, each shaped (via `check=`/`default=`/`raise_as=`-style parameters) to cover every existing caller's return-or-raise contract, so every module below has one version to point at. | — |
| `the-top-level-resources-modules-delegate-to-common` | `resources/guard.py`, `health.py`, `knowledge.py`, `questions.py` and `workflows.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`. | `common-py-gains-a-git-runner-and-a-section-extractor` |
| `the-core-board-modules-delegate-to-common` | `resources/board/boards.py`, `collect.py`, `edit.py`, `prdfile.py` and `specs.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`. | `common-py-gains-a-git-runner-and-a-section-extractor` |
| `the-lane-and-repo-modules-delegate-to-common` | `resources/board/lanes.py`, `orphans.py`, `ramp.py`, `refuse.py`, `repos.py`, `shared.py` and `transitions.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`. | `common-py-gains-a-git-runner-and-a-section-extractor` |

## Route followed

`probe-then-spec`. Read every flagged definition (step: attempt-the-build),
found the shape mismatch above, and split rather than spec.
