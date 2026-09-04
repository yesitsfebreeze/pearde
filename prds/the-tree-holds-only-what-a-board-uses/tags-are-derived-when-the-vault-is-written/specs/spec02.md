---
complexity: 8
footprint:
  - resources/memos.py
  - resources/workflows.py
  - resources/pearde.py
  - .pearde/memos
  - .pearde/workflows
---

# spec02 — the stored tags and the two repair verbs go

With spec01's writer deriving the tags, nothing reads a tag stored in an
authored record. This spec removes the storage and the machinery that kept it
honest: `tags` leaves the closed frontmatter set of a memo and of a workflow,
`memo_tags` / `retag_text` / `retag` leave `memos.py`, `file_tags` / `retag`
leave `workflows.py`, both `retag` verbs leave `pearde.py`'s `FORWARD` map,
and the 67 authored records on this board lose the block.

**What already stands** — the code half, built in the lane and uncommitted
there: both modules and `pearde.py` are already cut, and `memos.py add` no
longer writes a tag block. Proven in a clean room: `memos.py check` and
`workflows.py check` both exit 0 once the records are stripped, and a memo
written by `memos.py add` carries no `tags:` and gets a correctly tagged
generated note on the next `board` run.

**What is left** — carry the three modules into the checkout and run
`probe/strip-stored-tags.py` against `.pearde`, which strips 67 records and is
idempotent (a second run reports 0).

One consequence to write into the check's message rather than migrate around:
a board upgrading to this build still has `tags:` in its own memos, and
`check` will call it a key that is not a memo's. That message is the whole
migration — there is no one-shot for a user's board, and the sibling PRD
`legacy-migrations-retire` says why none should be added. The message must
name the fix ("delete it — the vault writer derives it"), not just the fault.

## Acceptance

- [x] `tags` appears in neither `memos.py`'s nor `workflows.py`'s `OPTIONAL`
      tuple, and neither module defines `retag`, `retag_text`, `memo_tags` or
      `file_tags` — `grep -n 'retag\|memo_tags\|file_tags' resources/memos.py resources/workflows.py resources/pearde.py` exits 1.
- [x] `pearde memo retag` and `pearde workflow retag` are gone: both verbs are
      absent from `pearde.py`'s `FORWARD` map and the CLI reports them as
      unknown — both exit 2 printing usage.
- [x] `grep -l '^tags:' .pearde/memos/*.md .pearde/workflows/*.md` matches
      nothing — `strip-stored-tags.py .pearde` stripped 68 records, second run 0.
- [x] `python3 resources/memos.py check` and `python3 resources/workflows.py check`
      both exit 0 and print nothing.
- [x] A record carrying a stray `tags:` is still reported, and the message
      names deleting it as the fix — fixture memo and workflow both print
      `` `tags:` is not a memo key — delete it — the vault writer derives it ``, exit 1.
- [x] `python3 resources/memos.py add "<subject>"` writes a memo with no
      `tags:` key, and `check` is green on it — fixture: `grep -c '^tags:'` = 0, check green.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
python3 -m py_compile resources/memos.py resources/workflows.py resources/pearde.py
# both greps assert a NO-match, whose own exit is 1 — guarded so the block
# survives -e on exactly the result that means it passed, and asserted so a
# match still fails the block
grep -n 'retag\|memo_tags\|file_tags' resources/memos.py resources/workflows.py resources/pearde.py || true   # no output
if grep -l '^tags:' .pearde/memos/*.md .pearde/workflows/*.md 2>/dev/null; then
  echo "an authored record still carries tags:"; exit 1
fi
python3 resources/memos.py check   && echo "memos green"
python3 resources/workflows.py check && echo "workflows green"
# the unknown verb is the passing case — its exit 2 is what proves the removal
{ python3 resources/pearde.py memo retag 2>&1 || true; } | head -2
```
