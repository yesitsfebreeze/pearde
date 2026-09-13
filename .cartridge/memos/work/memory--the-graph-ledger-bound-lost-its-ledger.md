---

kind: work
level: 10
status: done
description: "`[graph] max_ledger_entries` is read by nothing — it was fixed for being dead in June, wired into the gossip routing ledger, and orphaned again when gossip was deleted"
read_when: "picking up work, or trusting a config key to do something"
---

# the-graph-ledger-bound-lost-its-ledger

## Do

`GraphConfig::max_ledger_entries` (`src/config/src/config.rs:627`, default
10,000 at `:654`) has four mentions in the whole tree and none of them is a
read: the declaration, the default, and two literals in test fixtures in the
commands crate's `lib.rs`. Those coordinates are the pre-change tree and no line replaces
them: the work below deleted all four sites, and the commands crate's `lib.rs`
has since lost half its length to the daemon split
([[the-commands-split-left-eight-anchors-past-the-end]]). `apply_graph_config`
(`src/bootstrap/src/lib.rs:16-22`) is where a `[graph]` key reaches the graph
and it applies `max_memories` and `disk_threshold` only.

It has been dead before. `d3769cd5` (2026-06-12) is titled "fix(gossip): wire
config max_ledger_entries into the routing ledger (was dead)", and `60157404`
deleted the gossip crate — the same commit that left `max_frame_len` behind
([[the-pre-auth-frame-cap-has-no-caller]]). The ledger went; the bound on it
did not.

Delete the field, its default and the two fixture literals. Nothing else reads
`GraphConfig` by construction, so the change is contained.

Nothing would have told an operator. `[graph]` is not one of the three
preset-managed sections, so it carries neither an allow-list nor
`deny_unknown_fields` — a key there is accepted whether it is real, dead or
misspelt, and only `[retrieval]`, `[heat]` and `[ingest]` refuse
([[config-rejects-unknown-keys]]). Deleting the field does not change that: a
`memory.toml` still setting it keeps booting, now with serde ignoring it rather
than parsing it into a field nobody reads. This repo's own
`.memory/memory.toml` sets `[watcher]` and `[reason]` only.

**Done 2026-09-06.** All four sites gone — the field, the default, and the two
fixture literals in `commands/lib.rs`. Both searches answer nothing.

**It is the second orphan from `60157404`.** That commit took `verify_auth` and
`AUTH_FRAME_MAX` with the token they guarded
([[the-pre-auth-frame-cap-has-no-caller]]) and deleted the gossip crate,
leaving the bound on its routing ledger behind. Two instances from one commit
make it a property of the commit rather than a coincidence: a deletion that
removes a subsystem leaves its *configuration* behind, because the config lives
in a different crate and nothing links a key to the thing it bounds.

The history sharpens it further. `d3769cd5` (2026-06-12) is titled
"fix(gossip): wire config max_ledger_entries into the routing ledger (was
dead)" — so this key was found dead once, wired, and orphaned again three
months later by a deletion that could not see it. **Being wired is not a stable
state for a config key** when the thing it configures can be removed
independently of it.

## Check

Neither `git grep max_ledger_entries` nor `rg max_ledger_entries` finds a hit
outside `target/` — both, because a tracked-only search passes silently on an
untracked subject (`two-method-laws-are-safe-only-in-one-order`). `just
check` and `just test` green. All hold: both searches answer 0, and the suite
read 1,243 passed.
