---
kind: work
description: fifteen memos carry twenty line anchors on a bare `commands_admin.rs`, a file the split left at 20 lines; the gate cannot resolve a bare name so every one of them is silently false, and several are records *about* citation rot whose anchors must be left alone
read_when: "repairing a bare-name citation, or asking what the admin split left behind"
level: 10
status: done
estimate: 1h
---

# twenty-bare-name-anchors-point-into-a-dead-commands-admin

Residue of [[@prd/work/memory--the-admin-split-left-rotted-citations.md]], which repaired the
thirteen anchors `cited_paths` could see. The gate resolves a path, and a
citation spelled `commands_admin.rs:944` carries no directory, so it is in the
190-strong bare-name class [[@prd/work/memory--the-citation-gate-reads-code-and-not-the-record.md]]
left unchecked on purpose. That class was called a style question there. For
this one file it is not: `commands_admin.rs` is a 20-line re-export shim, so
every line anchor on it is false, and no test says so.

Measured 2026-09-08, `grep -rn 'commands_admin.rs:' memos/ --include='*.md'`
outside the generated indexes: twenty anchors across fifteen memos.

## Do

Repoint each by subject into the sibling that holds it now, the way
[[@prd/work/memory--the-admin-split-left-rotted-citations.md]] did — read the code, never the
arithmetic, and give the citation the full `src/commands/src/` path while it is
being rewritten so the gate can see it from then on.

Two classes do **not** get repointed, and telling them apart is most of the
work:

- A memo that quotes a broken anchor as its evidence keeps it. Four do:
  [[the-commands-split-left-eight-anchors-past-the-end]],
  [[@prd/work/memory--the-admin-split-left-rotted-citations.md]] (line 51, the anchors it repaired),
  this memo itself, and [[the-longest-unit-is-not-the-biggest-file]], whose
  `commands_admin.rs:484` is a dated measurement of the file's own size
  ranking, not a pointer into live code.
- A citation whose subject the split *deleted* rather than moved loses its
  anchor entirely rather than gaining a false one — the rule
  [[@prd/work/memory--the-citation-gate-reads-code-and-not-the-record.md]] established.

## Check

`grep -rn 'commands_admin.rs:[0-9]' memos/ --include='*.md'` names only the
memos that quote an anchor as evidence, each one listed by name in this memo's
`Do`, and `cargo test --test cited_paths` is still green.

Done 2026-09-08. Sixteen anchors across eleven memos repointed by subject into
`commands_health.rs`, `commands_gc.rs`, `commands_admin_compact.rs`,
`commands_hub.rs`, `commands_focus.rs` and `commands_unnamed.rs`, each rewritten
with its full `src/commands/src/` path so the gate reads it. The four evidence
memos above keep theirs; the fenced table in
[[the-embed-knobs-reach-two-of-eleven-clients]] stays bare-name like its
sibling rows, because a fence is the gate's exemption and no path there is
resolved.
