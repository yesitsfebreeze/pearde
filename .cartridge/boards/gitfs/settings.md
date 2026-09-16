---
name: gitfs
language: English
memos: memos/note
workflows: ../../workflows
grammar: ../../grammar.md
repo: /Users/feb/dev/cartridge/fs.ctg
source-repository: /Users/feb/dev/cartridge/fs.ctg

require-repo: true
---

## Note on `repo` for composition-root rows

`repo: fs.ctg` is right for rows about the file cartridge's own code, since fs
absorbed gitfs. It is WRONG for any row whose claims are about the composition
root (`.gitmodules`, `.cartridge/init.lua`, the installed *.ctg set, the composed
host): `collect` maps each foot with `path.relative(code, f)`, so a superproject
path declared under this repo resolves outside it and
`git -C fs.ctg diff -- ../<path>` exits 128, which `assertFootprint` treats as a
failure — collection aborts before any verification runs. Such a row sets
`repo: /Users/feb/dev/cartridge` in its own frontmatter and collects with no
lane, because a superproject lane worktree has empty submodules. See
`prds/gitfs-is-back-in-the-composition/prd.md` (2026-09-16) for the worked case.

This central board keeps the original owner alias. `repo` names the source repository for implementation; planning state belongs to prd.ctg. Use the root board to include cross-owner dependencies.
