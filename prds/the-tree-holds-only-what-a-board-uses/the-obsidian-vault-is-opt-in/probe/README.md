# probe — pass two

The probe for this PRD is the working tree of the lane, uncommitted:

```
.pearde/.lanes/the-tree-holds-only-what-a-board-uses-the-obsidian-vault-is-opt-in
```

`git diff` there is the whole build — nine files, the four specs written from
it. Nothing is staged and nothing is committed.

Fixtures were made at run time under the session scratchpad with `mktemp -d`
and a `git init`, never under `.pearde/`. Three shapes were exercised:

1. `pearde init <fresh>` — asserts no `.obsidian/`, no `.obsidian-api-key`,
   and the one console line naming `pearde vault`.
2. `pearde doctor <fresh>` — asserts the vault row reads `off`.
3. `init.write_obsidian(<fresh>)` called directly, because `pearde vault`
   refuses on every `.pearde` board today (see the report). It returns
   `(['dataview'], [], None)` and seeds one plugin and no key.

A baseline copy of `f8968fe` was extracted with `git archive` into the
scratchpad and the same three shapes run against it, which is how the
`unhide_board` refusal and `init`'s vault registration were shown to be
pre-existing rather than this PRD's doing.
