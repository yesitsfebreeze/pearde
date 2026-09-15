---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1d"
---

# `memory compact` left seven condensed memos beside the originals it folded rather than replacing them, and each output doubles its title, writes a `description` starting with `#`, writes a `read_when` that answers no question, downgrades wikilinks to backticks and stamps `sources:` batch-wide

The seven twins were already gone when this ran: `168de297` (2026-09-08)
deleted them, and all six originals it names are on disk, so no repair was
owed and none was made.

The writer is fixed in `src/commands/src/commands_compact.rs`, two commits on
`main`. The fold's block now carries a `Read when:` and a `From:` line the
model must supply and `parse_claims` validates — a `From:` naming a memo
outside the batch, a missing or oversized `read_when`, an invented or
unterminated `[[wikilink]]` are all refused — so `sources:` is per claim
rather than batch-wide, `read_when` names a question rather than provenance,
and wikilinks are whitelisted from the source texts instead of banned, so the
fold no longer severs the graph it folds. `description` is the body's first
whole sentence, and the dry run prints the title and description it would
write through the same `description` function `land` uses.

Measured end to end on a two-memo fresh intake: intake emptied, one `# title`
per output, `sources:` one name each, `read_when` a question, and
`[[lanes-not-a-shared-tree]]` through verbatim.

## Do

Fix the fold's writer so a condensed memo replaces what it folded and is worth
reading. Five defects, all measured 2026-09-08 across the seven twins deleted
that day:

- **The source survives.** [[memo-layout]] says compaction condenses intake
  "with the folded intake memos deleted", but each output sat beside a live
  original at 0.65–0.99 body similarity. Every twin had zero inbound wikilinks
  and every original had one to seven, so the record never moved.
- **The title is written twice** — once as the file's own `# <name>-condensed`
  heading and again as the original's `# <name>` inside the body.
- **`description` is a prefix of the body**, `#` heading included, truncated
  mid-sentence at about a hundred characters. It is the one line a cold agent
  reads before deciding to open the memo ([[memo-writing]]), and it carried no
  claim.
- **`read_when` is `"condensed from the intake by memory compact"`** — provenance
  where the field's whole job is to name the question that sends a reader here.
- **The source's wikilinks come out as backticks.** A fold over the record's own link
  graph severed it: `review-and-store-verdicts` where the source wrote
  `[[review-and-store-verdicts]]`, so nothing reaches the neighbour any more.
- **`sources:` is stamped batch-wide.** One twin listed 25 sources for a body
  drawn from a single memo, so the field cannot be read as evidence of what the
  fold used.

The `--dry-run` discipline the [[hygiene]] routine already prescribes catches
the title and description defects before a run lands; the source-deletion and
link-preservation halves are the writer's own.

## Acceptance
`rg -l '^read_when:.*condensed from the intake' memos/` returns nothing, and a
`memory compact --kind <kind> --limit 5 --dry-run` on a fresh intake prints
titles that carry a number, path or symbol rather than a heading prefix.

The first half was written as a bare `rg -l 'condensed from the intake'`, and
that form can never return nothing: three memos quote the string as evidence
rather than carry it — this memo, [[the-rows-grew-back-into-the-protocol]] and
[[the-first-compact-run-destroyed-25-parts]]. The defect was the frontmatter
field, so the Check now names the field. `find memos -name '*-condensed*'`
returns 0 as well.
