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
actual: "20m"
---

# `.gitignore` excludes `/memos/`, so a plain `rg` from the repository root silently skips the whole record — and the caller search [[code-laws]] demands is exactly that search.

## Do

Approved 2026-09-08 as "Approve, put it in code-laws instead" [[approve-noting-the-ignored-record-in-system-commands]]. The warning goes into [[code-laws]], beside the caller rule it protects; [[system-commands]] is left unchanged.

Observed defect, measured 2026-09-08 at 11:21 in `/Users/feb/dev/memory`, code revision `36d6def6`. `.gitignore:8` is `/memos/`, the record being a nested clone the parent ignores ([[memo-layout]]). `rg -l "herd-workflow" .` from the repository root returns nothing; `rg -l --no-ignore "herd-workflow" .` returns `./memos/routine/herd.md`, where [[@prd/routine/run-board.md]] line 33 says to run `scripts/herd-workflow.js`. This assessment ran that first search while checking whether any script had lost its caller, and was one step from filing `scripts/herd-workflow.js` as dead code under [[code-laws]]' rule that code without a caller is deleted — a rule whose check is precisely a root-level search. The trap is silent: the search succeeds, it just cannot see the half of the repository that names things.

Proposed scope: add one short paragraph to `memos/system/code-laws.md`, beside the frontier-mode rule whose caller check it protects. State that `/memos/` is ignored by the parent repository, that a plain `rg` from the root therefore searches the code and not the record, and that a search meant to find every mention — a caller, a link, a command name — passes `--no-ignore` or names `memos/` explicitly. Change nothing else: not `.gitignore`, not [[system-commands]], not [[memo-layout]], and not the [[@prd/routine/plan-cartridge-work.md]] inventory recipe, which already passes `--no-ignore` for its own roots.

Benefit: the caveat sits with the rule it qualifies, so a reader meets it at the moment [[code-laws]] tells them an uncalled symbol is deleted. Tradeoff: one more paragraph in a memo [[SYSTEM]] has every session read; it earns the space by preventing a deletion. Preserve what works: `just memo <leaf>` and `just memos-check` both reach the record correctly and are unaffected, and the [[@prd/routine/plan-cartridge-work.md]] inventory command stays exactly as it is.

Done 2026-09-08: the warning is the second law of [[code-laws]], between frontier mode and the comment rule, in record commit `2e9fd676`. Nothing else changed; `code-laws`' own `description` still names only frontier mode and comments.

## Acceptance
Already run, 2026-09-08: `rg -l "herd-workflow" .` returned nothing, `rg -l --no-ignore "herd-workflow" .` returned `./memos/routine/herd.md`, and `grep -n '^/\?memos' .gitignore` printed `8:/memos/`.

Unrun: after the change, `memos/system/code-laws.md` contains the warning, and a reader following it runs a search that finds the record.

Run `just memos-check` once after the change and require success.
