# Derived work

Work the board found rather than the user asked for, and the two rules that
bound it.

- **`origin: requested`** — the user asked for it. The deliverable.
- **`origin: derived`** — the board found it while working.

Derived work is real and often good — and **self-generating**: a gate written
to prove a requested PRD can itself be defective, and its fix grows a gate of
its own. Two rules bound it, both at creation time:

1. **State the consequence for a requested PRD** — which one, and what breaks
   while the defect stands. A derived PRD naming no consequence is filed
   **`state: deferred`** — parked, per @references/parts/states.md. Never
   `open`, which means the board intends to do the work.
2. **A defect in an instrument is a memo, not a PRD.** A finding that changes
   no verdict about the deliverable — a check passing too quietly, a narrow
   census — is a memo per @references/parts/memos.md and costs no worker.

The test: **would fixing this change what ships, or only how loudly the board
would have noticed?** The first is a PRD. The second is a memo.

**The tripwire.** When open+`analyzing`+`specced`+`claimed` derived PRDs reach
the same count as requested ones, the board is working on itself. Stop filing
derived PRDs, report both counts, and put the choice to the user — continue,
defer the derived tree, or drop it. The trade between a finished deliverable
and a perfect record is the user's.

A derived PRD filed against a derived PRD is the loop feeding on itself. Fold
it into the first, or write the memo.
