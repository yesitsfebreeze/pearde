---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
actual: "1h"
---

# a bare `part list` returns every `.md` under the watched roots with its front matter — 560 parts and roughly 303,000 characters today, about 76,000 tokens — with no limit, no cursor and no page, on the surface an agent calls to see the record

## Do

`part`'s default op is `list` (`src/rpc/src/part.rs:9,15`), and `list` walks
every directory under `cfg.watcher.effective_roots`, skipping dot directories,
reading each `.md` in full and answering path, stamps and parsed front matter
(`:71-92`). There is no `limit`, no `cursor` and no truncation anywhere in the
function, and the tool's own description promises the whole thing: "list
answers every `.md` with its front matter" (`commands_mcp.rs:61`).

Measured against this record on 2026-09-06: **560 parts, about 303,000
characters of front matter and paths — roughly 76,000 tokens.** That is larger
than the answer `query` used to give before it was capped, and it is the
default op, so `part {}` is the whole of it.

The precedent is the fix. [query-caps-its-default-answer](../query-caps-its-default-answer/prd.md) measured a bare
query at 202,901 characters and now answers five entities and at most twelve
edges each, 13,439 characters; [map-leaves-the-agent-surface](../map-leaves-the-agent-surface/prd.md) is the same
argument taken to its end for a 10.8 MB answer. Both are the same reasoning
[the-agent-surface-is-usable](../the-agent-surface-is-usable/prd.md) collected: an operation whose answer no context
can hold is not on the surface, it is a tool slot that cannot be spent.

Give `list` the shape `report` already has — `limit` with a default, and a
`cursor` for the rest ([report-answers-counts-without-ids](../report-answers-counts-without-ids/prd.md) is that pattern,
including a `counts_only` for the caller who wants the shape rather than the
contents). A bare call should answer a page and say how many there are.

What makes this worth doing rather than tolerating: an agent that reads
`SYSTEM.md` already holds the index, ~148 KB of it, and `part list` is the same
information again in a different shape
([[the-index-tripled-in-one-commit-restoring-rows]] measures the first half).

## Acceptance
A bare `part` answers a bounded page with a total count and a cursor, the
cursor walks the rest, and the answer for this record is under ten thousand
characters; `cargo test -p rpc part` and `just all` green.

**The rest of the surface, swept the same day.** Every tool's declared schema read for a `limit`, `k`, `cursor` or `counts_only`: `query`, `search`, `log`, `events`, `report`, `audit` and `ask` carry one. Of the tools that do not, all but three answer something fixed or are writes — `health`, `gc`, `pulse`, `setup`, `intake_drain`, `ingest`, `link`, `forget`, `forget_by_source`, `move`, `promote`, `degrade`. The three whose answer grows with the store are `map` (10.8 MB, [map-leaves-the-agent-surface](../map-leaves-the-agent-surface/prd.md)), `part` (this), and the two list actions on `graviton` and `claim_kind`, which are bounded in practice by what they enumerate — the root's direct children ([[the-graviton-list-is-the-roots-children-only]]) and the claim-kind registry.

So the unbounded-answer class has exactly two members with a part each, and a reader does not need to sweep it again.

**Done 2026-09-08.** The operation is `memo`, not `part` — it was renamed
before this ran, so the coordinates above read `src/rpc/src/memo.rs` and the
Check's `cargo test -p rpc part` filters nothing; `cargo test -p rpc memo` is
the same eleven tests and they pass. `list` now takes `limit` (20 by default)
and `cursor` (the last path delivered, rows sorting by path) and answers
`memos`, `total`, `cursor` and `more`. Measured against this record: a bare
`memo` answers **5,968 characters** for 20 of 944 rows, against the 412,544 it
used to hand back, and the cursor walks all 944 over 48 pages. `limit: 0` is
still the whole of it, which is what the one internal reader asks for — the
MCP tool declaration scans the record for a `kind:` and is not an agent's turn.

Two gates are red in a lane for reasons this part did not touch and did not
introduce — the diff is three files, none of them a `Cargo.toml` or a cited
path. `tests/cited_paths.rs` fails on `src/rpc/src/plan.rs` citing a gitignored
nested clone ([[lanes-not-a-shared-tree]]), present in the trunk and absent
from every worktree, so the citation gate is green on the trunk and red in
every lane.
`tests/declared_dependencies.rs` fails on the `extension` entry in
`[workspace.dependencies]`, which no member inherits. `just memos-check` fails
on `memos/research/an-indexing-analyzer-answers-empty-not-late.md` holding five
free-form sections — a committed memo of somebody else's, not this part's to
split.

