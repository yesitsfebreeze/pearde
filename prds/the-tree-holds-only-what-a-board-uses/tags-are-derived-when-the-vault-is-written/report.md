# tags-are-derived-when-the-vault-is-written — analyst pass two

Verdict: SPECCED

Workflow followed: `probe-then-spec`. Persona: engineer.

Pass one left the lane holding the code half of the cut — `retag` gone from
`memos.py`, `workflows.py` and `pearde.py` — and stopped on Q1. Q1 is answered
("derive at write"), so this pass built the other half and ran it end to end.

## What the build did

A clean room: the lane's checkout plus a copy of this board, so nothing was
written to the live board or to another PRD's files. In it:

1. `knowledge.py` gained `Store.memos` / `Store.workflows`, `memo_tags()` and
   `workflow_tags()` beside the existing `prd_tags()`, and `write_kind_notes()`
   — one generated note per authored memo and per authored library file,
   carrying the tags its kind and status imply and relaying every wikilink the
   authored body draws.
2. `cmd_board` calls it, scanning the library through `workflows.py scan`, and
   re-aims a PRD note's `## Decisions` links at the generated memo notes.
3. `graph.json`'s `search` stops drawing the authored `memos/` and
   `workflows/` folders — the same move that already hides `prd.md`.
4. `tags:` stripped from all 67 authored records.

It went through. Measured in the clean room:

```
board: 189 PRD note(s), 67 memo/workflow note(s), 42 memos scanned
memos.py check   → exit 0, silent
workflows.py check → exit 0, silent
invariant        → 8 colour groups, all tag queries, all carried (exit 0)
```

Round trip proved too: `memos.py add` writes a memo with no `tags:`, `board`
gives it `tags: [memo, kind/decision, status/decided]`, deleting the memo and
re-running `board` removes the generated note.

The probe is left uncommitted — `resources/knowledge.py` and
`resources/board/obsidian/graph.json` in the lane, on top of pass one's three
modules; `probe/strip-stored-tags.py` (idempotent: 67 then 0) and
`probe/verify.sh` in this PRD.

## Specs

| spec | goal | complexity |
|---|---|---|
| `specs/spec01.md` | the vault writer derives a tagged note for every memo and every workflow | 14 |
| `specs/spec02.md` | the stored tags and the two repair verbs go | 8 |
| `specs/spec03.md` | the documented mechanism, the two memos and the invariant catch up | 10 |

Sum 32, three units — under the board's 40 and 6.

Footprint union:

```
resources/knowledge.py            resources/board/obsidian/graph.json
resources/memos.py                resources/workflows.py
resources/pearde.py               resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh
.pearde/memos                     .pearde/workflows
references/memo.md                references/workflow.md
references/obsidian.md            references/templates/memo.doc.md
references/templates/workflow.doc.md
references/templates/atomic.doc.md
references/skills/pearde-memo.md  references/skills/pearde-workflow.md
```

## Finding — the invariant is already green only where the vault was generated

Run in a checkout whose `.pearde/wiki/` does not exist, the invariant reports
**four** dead colour groups today: `#prd`, `#conclusion`, `#pending`, `#graph`
all live only in generated notes, and `wiki/` is gitignored. It passes on this
machine because a vault has been generated here. After spec01 it would report
seven, since `#memo`, `#workflow` and `#atomic` join them. This is a
pre-existing weakness the change widens, not one it creates — spec03 fixes it
by regenerating before the second check, which is also the stronger claim: the
invariant then proves the writers emit the tags rather than that some file
somewhere holds the string.

## Finding — `-path:"memos"` would have hidden the generated notes too

Obsidian's `path:` matches a **substring** of the path. A filter spelled
`-path:"memos"` hides both `<board>/memos/` and `<board>/wiki/memos/`, and the
generated notes would have gone dark with no error — the exact silent failure
the invariant memo was written about. The filter is spelled `pearde/memos` /
`pearde/workflows`, which separates the two and is still a substring of
`.pearde/memos`, so it holds under either board name. Written back to the
record as `[[260903-b678]]` from the Obsidian help page.

## Finding — three footprint collisions with live siblings

Not mine to resolve; the orchestrator sequences them.

| my spec | file | sibling holding it | that sibling's state |
|---|---|---|---|
| spec02 | `resources/pearde.py` | `a-board-s-grammar-holds-only-its-own-words` spec02 | specced |
| spec03 | `references/obsidian.md` | `install-fetches-nothing` spec02 | claimed |
| spec03 | `references/obsidian.md` | `the-documented-board-matches-the-code` spec04 | specced |

## Finding — every existing board breaks its own memo check on upgrade

A board that upgrades to this build still carries `tags:` in its own memos and
workflows, and `check` will call it a key that is not a memo's — a red
`memos` row in `doctor` until the owner deletes the block. There is no
one-shot for a user's board and the sibling `legacy-migrations-retire` says
none should be added, so the check's own message is the migration. spec02
makes it name the fix.

## Findings outside this contract

- `resources/index.py check` reports four problems that predate this PRD and
  belong to none of its specs: `resources/common.py` has no row in
  `references/files.md`; `references/files.md` and `@@view` both name
  `@resources/board/hotreload-test.js`, deleted in `b1d3f5d`; and
  `references/parts/commits.md` cites `@pearde/memos/a-board-s-own-file-…`,
  a path that does not exist under that spelling.
- No Dataview query, `_index.md` or dashboard anywhere in the tree reads a
  memo's or a workflow's tag. The sweep found only prose. That is why spec03
  is nine documented lines and not a query rewrite.
- The record answered the contract's question with 91 hits and none on point,
  so no gap was enqueued; one source was written back instead.

## The two numbers

**complexity 22** — the mechanism is built and proven, and what is left is
mechanical: two files carried in, 67 records stripped by a script that already
runs, nine documented lines and one shell script hardened. Breadth, not depth.

**blast-radius mid** — it rewrites every authored record on every board and
changes a graph preset that ships to users, and it deletes two public verbs;
but no loop verb, no state transition and no PRD reader moves, and one
invariant is the whole gate.

## Scores

complexity: 22
blast-radius: mid
workflow: probe-then-spec
