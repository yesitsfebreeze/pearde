---

kind: work
level: 10
status: done
description: "`report` always ships every matching id, so the one aggregate read an agent has cannot be called from a context window — a `counts_only` flag fixes it"
read_when: "calling report from an agent"
---

# report-answers-counts-without-ids

## Do

`report_groups` (`src/rpc/src/server.rs:1497-1501`) writes `group`, `count` and
`ids` into every row unconditionally, and `limit` caps groups, not ids — so
`report {group: "scheme"}` over a 2,899-entity store returns three counts
buried in 2,899 ids. Measured 2026-09-05 from an agent session: 224,272
characters, over the tool-result cap, saved to a file and read back with a
script to recover eight numbers. `{group: "claim_kind"}` cost 221,266 the same
way. The aggregate read exists so an overview does not need `memory export`
(`operations`), and at this size it is the more expensive of the two for a
caller that wanted counts.

Add `#[serde(default)] counts_only: bool` to `ReportArgs`
(`src/rpc/src/server.rs:1236`), pass it into `report_groups`, and omit the
`"ids"` key when it is set — not an empty array, an absent key, so a caller
cannot mistake suppression for an empty group. Name it in the tool description
(`src/commands/src/commands_mcp.rs:27`) beside `limit` and `cursor`; the
handshake is the only place an agent learns the argument exists
(`reflex-measures-the-surface`).

## Check

`cargo test -p rpc report` — a new test in
`src/rpc/src/tests/server_report_test.rs` builds the same server as
`groups_by_kind_and_counts_every_active_row`, calls `report` twice over one
fixture, and asserts the `counts_only: true` answer carries identical `group`
and `count` values with no `ids` key on any row.

`counts_only` landed: the flag on `ReportArgs`, the `ids` key omitted in
`report_groups` (`src/rpc/src/server.rs`), named in the `report` tool
description, with `counts_only_drops_the_ids_and_keeps_the_counts` green in
`src/rpc/src/tests/server_report_test.rs`. The insights day histogram asks for
counts alone; the CLI fallback keeps its ids.
