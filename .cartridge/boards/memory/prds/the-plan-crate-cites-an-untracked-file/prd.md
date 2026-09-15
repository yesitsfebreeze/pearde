---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "0.5h"
---

# `src/rpc/src/plan.rs:2` cites a file in an untracked nested clone that exists only in the trunk, so `cited_paths::every_cited_path_is_there` fails in every fresh lane

The `//!` header of `src/rpc/src/plan.rs` cites a file in a nested repository
the parent does not track, so the path exists in the trunk working tree and in
no worktree `just lane` creates — `cited_paths::every_cited_path_is_there` passes
where a person runs it and fails everywhere an agent does. Found by
[memory-mcp-never-answers-initialize](../memory-mcp-never-answers-initialize/prd.md)'s lane, reproduced with that lane's own
files reverted.

## Do

Re-point the citation at something the repository actually carries: the memo
that holds the claim the header is reaching for, cited by leaf name, rather than
a file in an untracked subrepo. Check the rest of the header the same way
(`rg -n 'obsidian-memory/' src`) and re-point any sibling that names a path the
parent does not track.

## Acceptance
`cargo test --test cited_paths` is green from a fresh `just lane` worktree, and
`rg -n 'obsidian-memory/' src` returns nothing.

Done. The header of `src/rpc/src/plan.rs` now states the plan operation's own
contract — every `kind: work` memo in the record on one time axis, answered
once — and cites nothing outside the repository; both Check lines are green.
