---
state: done
origin: requested
priority: 55
complexity: 9
blast-radius:
needs:
  - a-density-checker-and-the-root-docs-are-rewritten
workflow: probe-then-spec
actual: 1.11h
commit: 64ed54a 85cde75
---

# skills-and-scout-docs-are-rewritten-dense — references/skills/` and `resources/scout/` docs rewritten dense (includes the one file over the sentence-length target)

references/skills/` and `resources/scout/` docs rewritten dense (includes the one file over the sentence-length target)

## Questions

### Q1: The line that decides when a tool starts

Each of the nineteen entry points opens with a one-line summary deciding when
that tool fires. The word checker counts that summary as writing and fails
five of them, so cleaning those five means editing the line that starts a
tool?

1. **Leave the summaries out of the count** — the checker reads only what a person reads, and every summary stays exactly as it is today. (recommended)
2. **Rewrite the summaries too** — every phrase that makes a tool fire is kept word for word, while the sentences around them change.
3. **Leave both alone** — five entry points stay flagged for good, and the checker never comes out clean.

<!-- for the board: references/skills/*.md frontmatter `description:`. resources/prose.py has no exemption mechanism at all — check() reads each file whole and strip_code removes only fences and inline code — so line 3 is read as prose: pearde-scout.md mean sentence length 39.0 over 24 (its 2-word body is clean at 2.0), and the last unbound hits in pearde-all `that could run`, pearde-drill `it is a contract`/`that can be specced`/`that would change`, pearde-machine `that could run`, pearde-persona-ask `it is a conversation`, pearde-workflow `it is followed`. Pass two closed the 11 body hits pass one left, so every body in references/skills/ and every file in resources/scout/ is now green in the lane and frontmatter is the only red left. Answer 1 = prose.py skips frontmatter; its footprint a-density-checker-and-the-root-docs-are-rewritten reached done at 3664de0, so answer 1 now needs its own PRD or a reopen. Answer 2 = this PRD's spec01 rewrites the description lines, proven in probe/frontmatter/pearde-scout-split.md at 39.0 -> 13.2 with every trigger phrase verbatim, and the same call then covers references/agents/, references/personas/ and references/templates/. -->

## Answers

**Q1** *(answered 2026-09-02 21:13)* — Rewrite the summaries too — every phrase that makes a tool fire is kept word for word, while the sentences around them change.

## Report

spec01: exit 0
merged tree 2e17d05cb0fe60c3c51e959cc17d05dfcb780651  (9889e78 + 64ed54a + uncommitted)
PASS  spec01.1 prose.py names no file in references/skills/
PASS  spec01.2 every name: and every trigger phrase byte-identical to 9889e78
PASS  spec01.3 no description: exceeds 1024 characters
PASS  spec01.4 doctor reports 19 well-formed skills
PASS  spec01.5 18+ files changed in scope and every line is M
PASS  spec02.1 prose.py names no file in resources/scout/
PASS  spec02.2 route.sh list returns 45 routes
PASS  spec02.3 the route id set is unchanged
PASS  spec02.4 findings.md keeps every table row
PASS  spec02.4 reading-list.md keeps every table row
PASS  spec02.4 README.md keeps every table row
PASS  spec02.4 routes.md keeps every table row
PASS  spec02.5 index.py check says exactly what it says on 9889e78
scope words 13115 -> 12928
PASS  spec02.6 the scope's word count is below 9889e78

boxes 14/14

spec02: exit 0
merged tree 2e17d05cb0fe60c3c51e959cc17d05dfcb780651  (9889e78 + 64ed54a + uncommitted)
PASS  spec01.1 prose.py names no file in references/skills/
PASS  spec01.2 every name: and every trigger phrase byte-identical to 9889e78
PASS  spec01.3 no description: exceeds 1024 characters
PASS  spec01.4 doctor reports 19 well-formed skills
PASS  spec01.5 18+ files changed in scope and every line is M
PASS  spec02.1 prose.py names no file in resources/scout/
PASS  spec02.2 route.sh list returns 45 routes
PASS  spec02.3 the route id set is unchanged
PASS  spec02.4 findings.md keeps every table row
PASS  spec02.4 reading-list.md keeps every table row
PASS  spec02.4 README.md keeps every table row
PASS  spec02.4 routes.md keeps every table row
PASS  spec02.5 index.py check says exactly what it says on 9889e78
scope words 13115 -> 12928
PASS  spec02.6 the scope's word count is below 9889e78

boxes 14/14
