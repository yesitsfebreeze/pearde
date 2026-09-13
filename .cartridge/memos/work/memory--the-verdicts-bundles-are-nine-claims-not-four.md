---

kind: work
level: 9
status: done
estimate: 4h
description: "`review-and-store-verdicts` carries nine independent decisions under four headings, so splitting it on its section boundaries would still leave three bundles; the split needs nine memos and four inbound citations repointed to the right half"
read_when: "splitting a *-verdicts memo, or asking why one is still on memos-bundles.txt"
---

# the-verdicts-bundles-are-nine-claims-not-four

## Do

Split `review-and-store-verdicts` into one memo per claim. Counted
2026-09-08, its four `## ` headings hold nine decisions, which is why the
obvious four-way split does not clear the atomicity law:

| section | claims in it |
|---|---|
| The review lifecycle, Active by default | 1 — Active is the default and both halves shipped as one slice |
| The store guards | 3 — the advisory writer lock, the watchdog's bounded flush, hash compositions golden-pinned by shape |
| The watcher deny-list invariant | 1 — the union of `.memory/`, `data_dir` and `intake.dir` |
| Process items that closed as settled | 4 — the tracked hook, the anchor taxonomy, the void federation tier, standalone `memory mcp` never federating |

Three of the four are already covered or unique in a way that decides where
each half goes. The hook bullet is the one duplicate: [[gates-are-tests]] holds
`core.hooksPath` too and already links here, so that claim merges rather than
splits. The anchor taxonomy, the void federation tier and the standalone-`mcp`
contract appear nowhere else and each becomes its own memo.

Four memos cite this leaf and they do not all mean the same half, so a split
that leaves them pointing at the file leaves four readers at the wrong claim:

- [[operations]] cites the `[ingest] review_policy` half
- [[@prd/work/memory--finish-the-store-the-doctor-found.md]] and
  [[the-doctor-is-safe-only-because-it-never-asks-the-daemon]] cite the writer
  lock, which is one third of "The store guards"
- [[gates-are-tests]] cites the hook bullet

[[@prd/work/memory--compact-writes-a-twin-instead-of-replacing-its-source.md]] also names this leaf,
but as an example of a fold stripping a link; that text stays as written.

The same count is owed to the other three `*-verdicts` memos on
`memos-bundles.txt` — `ingest-verdicts` (7 headings), `measurement-verdicts`
(6) and `retrieval-verdicts` (8) — before any of them is split on its headings.

## Check

`rg -c '^## ' memos/decision/review-and-store-verdicts.md` returns nothing
because the file is gone, every claim above resolves as its own leaf, each of
the four citations names the half it meant, `review-and-store-verdicts` is
struck from `memos-bundles.txt`, and `just memos-check` is green.

Done 2026-09-08: eight decision memos in `decision/` —
[[review-defaults-to-active]], [[the-writer-lock-is-advisory-on-purpose]],
[[the-watchdog-flushes-before-it-exits]],
[[hash-compositions-are-pinned-by-shape]],
[[the-watcher-denies-what-memory-writes]],
[[the-checkers-widening-made-its-old-coverage-claim-false]],
[[the-federation-tier-is-void-not-closed]] and
[[standalone-memory-mcp-never-federates]]; the hook claim merged into
[[gates-are-tests]] as the rule it supersedes; the source file and its
`memos-bundles.txt` line are gone.
