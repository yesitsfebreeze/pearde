---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1h"
---

# `just --list` shows only the last line of a recipe's comment block, so twelve recipes describe themselves with a sentence fragment and three describe themselves not at all.

## Do

Approved 2026-09-08 as "Approve, use [doc()] attributes" [[approve-just-list-description-repair]]. The mechanism is just’s `[doc(...)]` attribute, not the comment reordering this memo first proposed; the explanatory comment blocks stay unedited where they are.

Observed defect, measured 2026-09-08 at 11:16 in `/Users/feb/dev/memory`, just 1.58.0, code revision `36d6def6`. [[@prd/routine/plan-cartridge-work.md]] step 1 names `just --list` as an inventory command and [[system-commands]] is the record's command list, so this is a discovery surface an agent is told to read. `just` takes only the comment line immediately above a recipe as its description, and twelve recipes carry a multi-line comment block whose last line is a subordinate clause: `check` reads `# under the narrow form.` (the block runs `justfile:12-15`), and the same happens for `all`, `e2e`, `scale`, `hot`, `dev`, `piece`, `piece-build`, `clean`, `stop`, `eval-ground` and `eval-beam`. Three more — `panes`, `pi-test`, `terminal-check` — carry no comment and list with no description at all. The prose in those blocks is good; it is simply written for a reader of the file, and the last line of it is what the listing shows.

Proposed scope: `justfile` only. Give each of the twelve an explicit `[doc('…')]` attribute stating what the recipe does, and give `panes`, `pi-test` and `terminal-check` their first one. The explanatory comment blocks stay exactly where they are, unedited — no text is deleted and no recipe body, dependency or default changes. Do not reword the surviving prose, and do not touch [[system-commands]], which documents the commands by hand and is correct as it stands.

Benefit: the inventory command an agent is instructed to run stops describing `check` as "under the narrow form". Tradeoff: the justfile gains a syntax it does not currently use, and a recipe's description then lives in two places for a reader — the attribute and the prose above it. Preserve what works: every recipe already listing correctly — `build`, `install`, `land`, `lane`, `lane-rm`, `memo`, `memos-check`, `grammar`, `one-dispatch` and the rest — keeps its exact description, and no recipe body, dependency or default is edited.

## Acceptance
Already run, 2026-09-08: `just --list` printed `check # under the narrow form.`, `clean # default layout and misses every configured one.` and ten more fragments, with `panes`, `pi-test` and `terminal-check` bare; `grep -n -B6 '^check:' justfile` showed the four-line block at `justfile:12-15`.

Unrun: after the change, `just --list` gives every recipe a description that reads as a complete statement of what that recipe does, and the fifteen names above are each checked by eye against the recipe body.

Run `just memos-check` once after the change and require success, and `just --list` once to read the result.

Done 2026-09-08 in lane `just-list-recipe-docs`: sixteen `[doc("…")]` attributes in `justfile`, insertions only, no comment block, recipe body, dependency or default touched. `just --list` now gives every recipe a complete statement; `just memos-check` green. The set differs from the count above because the count was taken against a dirty trunk: `pi` was a fragment the survey missed — thirteen fragments plus the three bare names.
