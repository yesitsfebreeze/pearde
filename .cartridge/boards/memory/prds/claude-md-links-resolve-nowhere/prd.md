---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "30m"
---

# All ten links in `memos/SYSTEM.md` are paths relative to `memos/`, so from `CLAUDE.md` — the symlink whose contents every session is handed — none of them resolve.

## Do

Approved 2026-09-08 as "Approve as written" [[approve-claude-md-link-repair]].

Observed defect, measured 2026-09-08 in `/Users/feb/dev/memory`, code revision `36d6def6`. `CLAUDE.md` is a symlink to `memos/SYSTEM.md`, so there is no drift between them, and the harness inlines its contents into every session with no path context. Its body links `[memo-layout](system/memo-layout.md)` and nine more the same way; tested from the repository root, all ten — `system/memo-layout.md`, `code-laws`, `git-policy`, `memo-writing`, `memo-atomicity`, `memo-index`, `_index_`, `system-commands`, `work`, `terminal` — do not exist, because the paths are relative to `memos/`. A cold session reads the one file it is told to read first and cannot follow a single link out of it.

Proposed scope: in `memos/SYSTEM.md` only, replace those ten markdown path links with wikilinks — `[[memo-layout]]`, `[[code-laws]]`, and so on — leaving the prose and the reading order exactly as they are. This is the record's own protocol: [[memo-writing]] states a memo links by leaf name, leaf names are unique across `memos/`, and `just memo <leaf>` prints the file a leaf resolves to from anywhere. Do not touch `CLAUDE.md`, the symlink, other memos' links, or the gate.

Benefit: the entry point's links work for the reader they exist for, and SYSTEM.md stops being the one memo that disobeys the linking rule it introduces. Tradeoff: none found — the memos gate already checks wikilink destinations. Preserve what works: `CLAUDE.md` stays a symlink so the two never drift, `just memo <leaf>` stays the resolver, and the file keeps its `kind: documentation` frontmatter and heading order.

## Acceptance
Already run, 2026-09-08: `ls -la CLAUDE.md` printed `CLAUDE.md -> memos/SYSTEM.md`, `diff CLAUDE.md memos/SYSTEM.md` was empty, and a `test -e` over the ten link targets from the repository root printed `MISS` for all ten.

Unrun: after the change, `just memo <leaf>` resolves each of the ten leaves to a file that exists, and a search of `memos/SYSTEM.md` for a markdown link whose target begins `system/` returns nothing.

Run `just memos-check` once after the change and require success — its link check is the regression guard.

Done 2026-09-08 in `memos/SYSTEM.md` (memos `2900ac9d`): nine of the ten targets have a unique leaf and are wikilinks now; the tenth, the generated system index, does not — `_index_` names twenty-four files and the gate excludes generated files from link targets, so `[[_index_]]` would be both ambiguous and a link to nothing. It is cited as the backticked path `memos/system/_index_.md`, which the reader handed `CLAUDE.md` can open. All ten leaves resolve to a file that exists, `grep '](system/' memos/SYSTEM.md` returns nothing, and `just memos-check` passes.
