---
state: done
origin: requested
priority: 80
complexity: 35
blast-radius:
workflow: probe-then-spec
actual: 0.49h
commit: 1858a35 7680a1b
---

# one copy per machine of what every lane regenerates

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
ok: the checkout is a tree share visits

spec02: exit 0
1  board                /Users/feb/dev/infra/pearde/pearde
1  find_repo(board)     /Users/feb/dev/infra/pearde/pearde
1  find_checkout(board) /Users/feb/dev/infra/pearde
1  trees()[0]           /Users/feb/dev/infra/pearde
1  code checkout        /Users/feb/dev/infra/pearde
1  VERDICT              ok
1  checkout in trees(): True
1  board in trees():    False  (it offers nothing)

2  fixture ignore  ['resources/board/node_modules/']
2  state before    refused
2  apply           refused — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
2  state after     refused
2  status prints   'refused'; summary buckets it under: refused

3  pearde/graphify    12.1 MB across lanes, unshared
ok: 25 refused of 269 rows

243 shared · 0 not yet · 25 refused (git would show the link) · 0 refused (git tracks them) · 0 linked to a retired store path · 0 someone else's link · 1 in the store only · 0 not here
= 269 of 269 row(s) surveyed

spec03: exit 0
refused   a-cross-board-need-that-names-no-board-in-the-scan-is-ignore/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   a-cross-board-need-that-names-no-board-in-the-scan-is-ignore/pearde/graphify/cache — no .gitignore row here ignores it — git would show the link — add `pearde/graphify/cache` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   a-harness-measures-the-tree-its-worker-built-in/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   a-refused-rebase-must-not-destroy-the-lane-it-was-left-in/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   a-verify-block-must-not-destroy-the-checkout-it-runs-in/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   collect-must-not-reset-the-checkout-it-did-not-write/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   collect-must-not-reset-the-checkout-it-did-not-write/pearde/graphify/cache — no .gitignore row here ignores it — git would show the link — add `pearde/graphify/cache` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-document-is-written-in-the-writer-s-prose/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-document-is-written-in-the-writer-s-prose/pearde/graphify/cache — no .gitignore row here ignores it — git would show the link — add `pearde/graphify/cache` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-document-is-written-in-the-writer-s-prose-a-density-checker-and-the-root-docs-are-rewritten/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-document-is-written-in-the-writer-s-prose-templates-personas-and-agents-are-rewritten-dense/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-document-is-written-in-the-writer-s-prose-the-loose-reference-files-are-rewritten-dense/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-document-is-written-in-the-writer-s-prose-the-parts-reference-is-rewritten-dense/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-document-is-written-in-the-writer-s-prose-the-parts-reference-is-rewritten-dense-the-cross-board-parts-are-rewritten-dense/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-document-is-written-in-the-writer-s-prose-the-standard-is-held-to-its-own-standard/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-run-session-works-in-a-worktree-of-its-own/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-run-session-works-in-a-worktree-of-its-own-a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   every-task-is-a-verb-under-one-skill-the-machine-is-the-run-verb/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   resources-are-organised-by-responsibility/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   resources-are-organised-by-responsibility-every-module-finds-its-siblings-by-one-rule/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   resources-are-organised-by-responsibility-the-largest-module-is-cut-by-responsibility/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   the-daemon-must-not-write-into-a-board-path-it-no-longer-own/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   the-master-ramp-measures-its-own-tree-not-its-members/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   the-master-ramp-measures-its-own-tree-not-its-members/pearde/graphify/cache — no .gitignore row here ignores it — git would show the link — add `pearde/graphify/cache` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused   the-verify-guard-parses-git-s-own-output-before-it-trusts-it/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
243 path(s) are shared.
ok: one cache in the store
refused: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: a-cross-board-need-that-names-no-board-in-the-scan-is-ignore/pearde/graphify/cache — no .gitignore row here ignores it — git would show the link — add `pearde/graphify/cache` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: a-harness-measures-the-tree-its-worker-built-in/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: a-refused-rebase-must-not-destroy-the-lane-it-was-left-in/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: a-verify-block-must-not-destroy-the-checkout-it-runs-in/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: collect-must-not-reset-the-checkout-it-did-not-write/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: collect-must-not-reset-the-checkout-it-did-not-write/pearde/graphify/cache — no .gitignore row here ignores it — git would show the link — add `pearde/graphify/cache` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-document-is-written-in-the-writer-s-prose/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-document-is-written-in-the-writer-s-prose/pearde/graphify/cache — no .gitignore row here ignores it — git would show the link — add `pearde/graphify/cache` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-document-is-written-in-the-writer-s-prose-a-density-checker-and-the-root-docs-are-rewritten/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-document-is-written-in-the-writer-s-prose-templates-personas-and-agents-are-rewritten-dense/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-document-is-written-in-the-writer-s-prose-the-loose-reference-files-are-rewritten-dense/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-document-is-written-in-the-writer-s-prose-the-parts-reference-is-rewritten-dense/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-document-is-written-in-the-writer-s-prose-the-parts-reference-is-rewritten-dense-the-cross-board-parts-are-rewritten-dense/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-document-is-written-in-the-writer-s-prose-the-standard-is-held-to-its-own-standard/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-run-session-works-in-a-worktree-of-its-own/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-run-session-works-in-a-worktree-of-its-own-a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: every-task-is-a-verb-under-one-skill-the-machine-is-the-run-verb/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: resources-are-organised-by-responsibility/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: resources-are-organised-by-responsibility-every-module-finds-its-siblings-by-one-rule/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: resources-are-organised-by-responsibility-the-largest-module-is-cut-by-responsibility/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: the-daemon-must-not-write-into-a-board-path-it-no-longer-own/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: the-master-ramp-measures-its-own-tree-not-its-members/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: the-master-ramp-measures-its-own-tree-not-its-members/pearde/graphify/cache — no .gitignore row here ignores it — git would show the link — add `pearde/graphify/cache` to .gitignore, with no trailing slash, and run `pearde share apply` again
refused: the-verify-guard-parses-git-s-own-output-before-it-trusts-it/resources/board/node_modules — `resources/board/node_modules/` ignores a directory and a symlink is not one — git would show the link — add `resources/board/node_modules` to .gitignore, with no trailing slash, and run `pearde share apply` again

spec04: exit 0
ok: no handle names a board path
references/language.md references @references/personas/writer.md — not on disk
ok: index.py check names no handle failure

spec05: exit 0
PASS  33 tree(s) point at one store: /Users/feb/dev/infra/pearde/.git/pearde-shared
PASS  0 path(s) hold a real copy, none in two trees at once
PASS  243 link(s), none of them visible to git status
PASS  6 shared row(s) reach 5 store path(s), none of them retired
0 claim(s) failed
ok: the script reports both failures and names tree and path
references/language.md references @references/personas/writer.md — not on disk
ok: index.py check names neither the script nor its row
