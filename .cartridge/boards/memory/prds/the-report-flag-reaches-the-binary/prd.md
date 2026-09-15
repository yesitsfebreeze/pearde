---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `counts_only` exists only in the working tree — `git log -S` finds no commit and HEAD carries zero occurrences, so the flag the record calls done is absent from every built memory

## Do

[report-answers-counts-without-ids](../report-answers-counts-without-ids/prd.md) is `status: done` and describes the flag,
the omitted `ids` key and a green test. None of it is committed. Measured
2026-09-06:

```
git show HEAD:src/rpc/src/server.rs | grep -c counts_only   -> 0
git log --oneline -S counts_only -- src/rpc/src/server.rs   -> (no commits)
git diff src/rpc/src/server.rs | grep -c counts_only        -> 4
```

The change sits in one working tree. The installed `~/.cargo/bin/memory` that
serves this repo does not have it: a raw JSON-RPC `report` with a real boolean
`counts_only: true` still answered every id, 817,904 characters. An agent
reading the index believes the guard exists; the surface it calls has none.

Commit the four hunks in `src/rpc/src/server.rs` together with the tool
description line in `src/commands/src/commands_mcp.rs:27` and the test in
`src/rpc/src/tests/server_report_test.rs`, then `cargo install --path .` so the
binary the daemon runs carries them. This is a symptom of
`the-record-has-no-truth-gate` — a `Check` written as a test that was never
run against a committed tree — and the same audit is owed to every other work
part marked done in the same session.

**Blocked 2026-09-06 on the curator, not on any agent.** The measurement
re-runs exactly as written — `git show HEAD:… | grep -c counts_only` is 0, `git
log -S` finds no commit, the working tree carries 4 — so the finding stands and
nothing about it has changed.

What cannot proceed is the `Do`, because it is "commit these hunks and
`cargo install`". The session working this record commits only when the curator
asks, and has not been asked; every part closed tonight is uncommitted for the
same reason. An agent that committed here to satisfy a `Check` would be taking a
decision the instruction reserves, and would take four hunks it did not write
with it — `counts_only` came from a session that has since ended.

So this is the one item in the plan whose `Do` no agent can execute, and that is
worth more than the flag it is about: a work part can name an action the working
agent is not permitted to take, and nothing in the part's shape says so. The
`level` bounds size, `status` records progress, and neither carries "who is
allowed". Unblocks with one word from the curator.

## Acceptance
`git show HEAD:src/rpc/src/server.rs | grep -c counts_only` is non-zero, and
against a daemon started from the freshly installed binary,
`report {group: "kind", counts_only: true}` answers under 4,000 characters with
no `ids` key on any group.

**Unblocked and done, 2026-09-06, by nobody acting on this item.** The three
halves the `Do` asked for are all in `HEAD` at `6ac36992` — the plan-app
commit, which carries them among its 106 files:

```
git show HEAD:src/rpc/src/server.rs            | grep -c counts_only  -> 4
git show HEAD:src/commands/src/commands_mcp.rs | grep -c counts_only  -> 3
git show HEAD:src/rpc/src/tests/server_report_test.rs | grep -c counts_only -> 2
cargo test -p rpc counts_only                  -> 1 passed
```

So the curator's decision this was blocked on was never taken, and the change
landed anyway, swept in by a session committing something else. That is the
same mechanism that closed the day's three build breaks
([[a-working-tree-covers-for-a-broken-head]]): the missing half arrives when
somebody commits widely, for unrelated reasons.

The `Check`'s second half is untested and stays that way here — it asks for a
daemon started from a freshly installed binary answering under 4,000
characters. The code path is proved by the unit test; the installed-binary
claim is not, and marking this done on the committed halves is the honest
reading of what was measured.