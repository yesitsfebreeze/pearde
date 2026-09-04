---
complexity: 10
footprint:
  - resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh
  - .pearde/memos/no-colour-group-in-the-vault-preset-is-a-path-query.md
  - .pearde/memos/the-graph-view-colours-by-tag-and-every-note-s-kind-tag-is-generated.md
  - references/memo.md
  - references/workflow.md
  - references/obsidian.md
  - references/templates/memo.doc.md
  - references/templates/workflow.doc.md
  - references/templates/atomic.doc.md
  - references/skills/pearde-memo.md
  - references/skills/pearde-workflow.md
---

# spec03 — the documented mechanism, the two memos and the invariant catch up

Nine documented lines across seven files still describe the mechanism spec02
deletes, and two memos record the decision it replaces. This spec brings them
to the new mechanism and hardens the invariant that guards it.

**What already stands** — nothing; the build proved the surface is exactly
this and no larger. The sweep for consumers found no Dataview query, no
`_index.md` and no dashboard reading a memo's or a workflow's tag, so the
change is prose plus one shell script.

**What is left** — the nine lines, the two memos, and the invariant.

The invariant is the part that bites. Its second check reads every `.md` under
the board and asks whether each colour group's tag is actually carried. Three
of the eight tags (`#conclusion`, `#pending`, `#graph`) already live only in
`wiki/`, which is gitignored — measured on a checkout with no `wiki/`, the
script reports four dead groups today and would report seven after spec01,
because `#memo`, `#workflow` and `#atomic` join them. The script has to
regenerate before it reads, or say plainly that an ungenerated vault is not a
break. Regenerating is the honest one: the invariant then proves the writers
emit the tags, which is what it claims to prove.

Both memos are `decided` and stay so — the decision they record (colour by
tag, never by folder; a tag is generated, never typed) is unchanged. What
changes is the writer named: `memo retag` / `workflow retag` become
`knowledge.py board`, and an authored record is now excluded from the graph
rather than tagged in place.

## Acceptance

- [x] `grep -rn retag references/ resources/` matches nothing — exit 1, whole tree.
- [x] `references/memo.md` and `references/workflow.md` no longer list `tags`
      as a frontmatter key of a memo or of a library file, and each says where
      the tag is written instead — the closed-set table drops the row, and a
      paragraph names `knowledge.py board` as the writer.
- [x] `references/obsidian.md`'s note/tag table names `knowledge.py board` as
      the writer for the `memos/<slug>` and `workflows/<slug>` rows (now spelled
      `wiki/memos/<slug>` / `wiki/workflows/<slug>`), and a paragraph says the authored
      folders are out of the graph and why.
- [x] `references/templates/memo.doc.md`, `workflow.doc.md` and
      `atomic.doc.md` no longer promise a `tags:` in the file the template
      writes — each says no `tags:` and names `knowledge.py board`.
- [x] `references/skills/pearde-memo.md` and `pearde-workflow.md` list no
      `retag` command — both command blocks drop the line.
- [x] The memo `the-graph-view-colours-by-tag-and-every-note-s-kind-tag-is-generated`
      names the vault writer, not the two `retag` verbs, and its `updated:` is
      set — `updated: 2026-09-03`.
- [x] The invariant memo `no-colour-group-in-the-vault-preset-is-a-path-query`
      states that the tags it checks are carried by generated notes and that
      the check regenerates before it reads; its `updated:` is set — `updated: 2026-09-03`.
- [x] The invariant script regenerates the vault before its second check, and
      exits 0 on a checkout whose `.pearde/wiki/` did not exist beforehand — fixture
      board with no wiki/memos, wiki/workflows, wiki/board: 8 colour groups, all carried,
      exit 0. Behavioural mutation (regeneration disabled + notes removed) breaks it
      with `tag:#memo, tag:#workflow, tag:#atomic` dead; restored by cmp.
- [x] `python3 resources/index.py check` names no file in this footprint, and
      `python3 resources/memos.py verify` is green — index check exits with 3 inherited
      lines, none in the footprint; `memos.py verify` green for every invariant this
      footprint holds. The one BROKEN row, `a-pass-holds-its-turn-until-its-workers-are-in`
      (exit 127, script absent from the tree), is inherited and outside this footprint.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
grep -rn 'retag' references/ resources/ || true   # no match wanted
if grep -rqn 'retag' references/ resources/; then
  echo "retag survives in the tree"; exit 1
fi
grep -n 'tags' references/memo.md references/workflow.md \
     references/templates/memo.doc.md references/templates/workflow.doc.md \
     references/templates/atomic.doc.md
rm -rf .pearde/wiki/memos .pearde/wiki/workflows
bash resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh
# the two board-wide gates are captured, never deciding the exit; this
# footprint's rows are the only ones that do
out=$(python3 resources/memos.py verify 2>&1) && rc=0 || rc=$?
if printf '%s\n' "$out" | grep -Eq 'no-colour-group-in-the-vault-preset-is-a-path-query.*BROKEN'; then
  echo "this footprint's invariant is BROKEN"; exit 1
fi
printf '%s\n' "$out"
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
if printf '%s\n' "$out" | grep -Eq 'memo\.md|workflow\.md|obsidian\.md|doc\.md|pearde-memo|pearde-workflow|path-query'; then
  echo "index check names a footprint file"; exit 1
fi
printf '%s\n' "$out"
```
