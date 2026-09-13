---
complexity: low
footprint:
- src/main.rs
- src/mailbox.rs
- src/channels.rs
- src/roster.rs
- .cartridge/tests/unit/main/channel_cursor_tests.rs
- .cartridge/tests/unit/main/roster_tests.rs
- .cartridge/tests/integration/channel-cursors.test.ts
- .cartridge/tests/integration/roster.test.ts
- .cartridge/docs/channel-cursors.md
- .cartridge/docs/roster.md
---

# Verify one scoped roster from durable delivery state to composed context

Preserve the original three acceptance checks and both inherited review rounds. The sessions cursor child owns authenticated delivery progress; scoped roster is a read-only projection of existing sessions/channel snapshots; the harness adapter uses the existing Landscape collector. No parallel roster storage, transcript scanning or automatic acknowledgement from roster/prompt reads is introduced. The original reading-progress criterion is exercised by explicit channel read/ack, which changes only the requester and cannot skip later posts.

Require all source receipts, plus actual sessions and harness SDK composition with20 scoped sessions and outsiders. Missing activity-start evidence stays unknown; mixed contributor revisions remain separate. Native host trust, single-writer scope persistence and ephemeral wake notifications remain explicit. The future broader harness integration and named-channel wake/global-journal work remain their own PRDs.

## Acceptance

- [ ] Cursor, roster, harness and Landscape contract receipts validate at current owner source footprints.
- [ ] Actual composed SDK fixture proves scoped bounded prompt data, phase refresh without post, explicit cursor acknowledgement and disabled/unavailable behavior.
- [ ] Scope history, input/binary revisions and no-mutation/failure limitations are recorded; parent completion is not inferred from synthetic renderer tests alone.

## Verify and Proof

```sh
cd ../prd.ctg
bun -e 'for (const ref of ["@sessions/an-agent-is-one-lookup-from-the-roster/durable-channel-read-cursors","@sessions/an-agent-is-one-lookup-from-the-roster/scoped-roster-projection","@harness/scoped-roster-context-contributor","@landscape/landscape-composes-system-context/context-contributor-contract"]) { const p=Bun.spawnSync(["./prd","verified-status",ref,"--json"]); const r=JSON.parse(p.stdout.toString()); if(p.exitCode || !r.data?.verified) throw Error(ref+": "+r.data?.reason); console.log(JSON.stringify(r.data)); }'
```

```sh
bun /Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/harness/prds/scoped-roster-context-contributor/verify-isolated.ts --committed /Users/feb/dev/cartridge/harness.ctg
```

The committed mode materializes the current committed harness owner into the disposable composition without original working changes, records its source commit/file hashes, and runs the same public gates and actual SDK fixture as the child. Receipt validity must hold before invoking it. It neither changes nor certifies unrelated original harness edits. Runtime/Landscape external contract changes require manual rollup revalidation in addition to engine receipt checks. The sessions footprint is the exact two-child union; external harness/Landscape paths are validated through their owner receipts and input digests.
