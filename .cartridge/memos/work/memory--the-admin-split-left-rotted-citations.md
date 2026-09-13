---
kind: work
description: thirteen memos cite src/commands/src/commands_admin.rs line numbers that the nine-subject split moved into siblings; `cargo test --test cited_paths` is red on every one of them and the parent's own Check names that test
read_when: "closing the-commands-admin-split, or reading a commands_admin.rs citation"
level: 10
status: done
estimate: 45m
---

# the-admin-split-left-rotted-citations

Ninth child of [[@prd/work/memory--the-commands-admin-split.md]], found by running the parent's
own `Check` after [[@prd/work/memory--split-admin-health.md]] landed. `commands_admin.rs` went
1515 → 645 → 20 lines across the eight subject children, and thirteen
citations to it were never repointed. Nine were already past the end of the
645-line file before the last child ran, so the gate has been red through
most of the chain; four more (`:21`, `:74`, `:561`, `:589`) stayed
numerically in range while pointing at whatever code happened to occupy
those lines, which is worse than a rotted citation because the test cannot
see it.

Two were fixed with the health child, because it moved their subject:
`health-prints-the-cold-counts-and-discards-the-daemons` now cites
`commands_health.rs:14-16` and `how-long-does-the-app-token-live` cites
`commands_app.rs:58`.

## Do

Repoint each citation at the sibling that now holds its subject, by
subject rather than by arithmetic — the old line number is not a reliable
guide, since four of them drifted onto unrelated code:

- `connect_hub_or_start` → `commands_hub.rs:332-363`
  ([[the-hub-waits-sixty-seconds-for-a-node]]:14,
  [[@prd/work/memory--memory-mcp-never-answers-initialize.md]]:18)
- `cmd_gc` → `commands_gc.rs:9-44`, its lock acquire at `:10-16`, its
  reaped-memories line at `:26` ([[@prd/note/memory--open-work.md]]:459,
  [[the-reap-drops-edges-it-never-counts]]:17,
  [[does-a-removal-need-a-tombstone]]:78)
- the `UnnamedAction::List` predicate → `commands_unnamed.rs:19-24`, the
  `Promote` arm → `:36-86` ([[a-promoted-root-does-not-persist]]:40,
  [[@prd/work/memory--unnamed-promote-routes-to-the-daemon.md]]:14 and :114)
- `cmd_hub_merge` → `commands_hub.rs:490-570`
  ([[a-refused-flush-undoes-another-writers-removals]]:29)
- `cmd_compress` → `commands_compress.rs:8-36`
  ([[binary-quantization-is-unreachable-and-in-memory-only]]:20)
- `spawn_detached` → `commands_hub.rs:295-328`
  ([[one-daemon-spawn-detaches-the-process-group-and-one-does-not]]:11)
- `cmd_rekey` → `commands_hub.rs:91-171`
  ([[rekey-leaves-the-ownership-indexes-on-the-old-ids]]:18)
- [[@prd/work/memory--the-root-memory-needs-one-authority.md]]:43 cites `commands_admin.rs:74,984,1008`
  as `root_memory()` sites; find where those three actually are now, since
  `:74` was already pointing at a health-line loop.

`memos/` is shared: commit each memo path by name, one commit each.

## Check

`cargo test --test cited_paths` is green, and
`grep -rn 'commands_admin.rs:' memos/` answers nothing.

**Done 2026-09-08.** All thirteen were repointed, none dropped: no subject the
split touched was deleted, so every one of them found a sibling. By subject —
`connect_hub_or_start` to `commands_hub.rs:332` and `:332-363`, `cmd_hub_merge`
to `:490`, `spawn_detached` to `:295-328`, `cmd_rekey` to `:91-171`; `cmd_gc` to
`commands_gc.rs:9`, its writer lock to `:10-16`, its reaped-memories line to `:26`;
the `UnnamedAction::List` predicate to `commands_unnamed.rs:23` and `:19-24`, the
`Promote` arm to `:36-86`; `cmd_compress` to `commands_compress.rs:8`.

The arithmetic was worthless, as the `Do` warned, and by more than the four it
names: measured against the tree each memo was written on, `:723-730` in
[[does-a-removal-need-a-tombstone]] was `cmd_consolidate`'s lock and not
`cmd_gc`'s, and the three `root_memory()` sites
[[@prd/work/memory--the-root-memory-needs-one-authority.md]] cites as `:74,984,1008` stood at 46, 976
and 1000 the day before the accessor landed. Those three are the claim-kind
registry, now `commands_health.rs:40` and `commands_claim_kind.rs:50,78` — the
subject moved and split across two siblings, so the one citation became two.

Two `k.id != g.root.id` quotes were left as written. `g.root` is gone
([[@prd/work/memory--the-root-memory-needs-one-authority.md]]) and the predicate reads
`g.root_memory_id()` today, but both quotes are dated statements about what a
commit and a decision established, so only their anchors moved.

The `Check`'s second clause cannot be satisfied as written — the line stating it
contains the string it greps for — and its real residue is the bare-name class
the gate cannot resolve: twenty anchors on a bare `commands_admin.rs` across
fifteen memos, every one of them false against a 20-line shim, and several of
them records *about* citation rot whose anchors have to stay.
[[@prd/work/memory--twenty-bare-name-anchors-point-into-a-dead-commands-admin.md]] carries them.
`cargo test --test cited_paths` is green, which is the clause the parent's own
`Check` names.
