---
complexity: low
footprint:
  - src/main.rs
  - src/observations.rs
  - .cartridge/tests/unit/main/observation_tests.rs
  - .cartridge/tests/integration/observations.test.ts
  - .cartridge/docs/observations.md
---

# Roll up actual attributed execution evidence

The sessions projector and runtime native-call adapter jointly fulfill the original mixed-activity outcome. Preserve original source aliases and both used review rounds. Require verified dependency receipts plus an actual composed runtime producing the source read by a real sessions process. Unit-only or manually inserted collector rows cannot satisfy parent mixed-use acceptance. Native host actor configuration is provenance, not authenticated end-user identity. Unknown historical dimensions, unseen descriptor changes, lost diagnostic rows and effects after cancellation remain explicit.

## Acceptance

- [x] Both dependency receipts validate at current source footprints.
- [x] Real composed runtime plus sessions SDK fixture passes mixed attribution, uncertainty, bounded/redacted reports and no tool interference.

## Verify and Proof

```sh
cd ../prd.ctg
bun -e 'for (const ref of ["@runtime/native-tool-observation-adapter", "@sessions/reflex-reports-attributed-tool-outcomes/attributed-outcome-report"]) { const p=Bun.spawnSync(["./prd","verified-status",ref,"--json"]); const r=JSON.parse(p.stdout.toString()); if(p.exitCode || !r.data?.verified) throw Error(ref+": "+r.data?.reason); console.log(ref+" verified at "+r.data.commit); }'
```

```sh
cd ../cartridge.ctg
CARTRIDGE_TEST_BIN="$PWD/target/sessions-mapping/debug/cartridge" SESSIONS_BINARY="$PWD/target/sessions-mapping/debug/sessions" bun test ../sessions.ctg/.cartridge/tests/integration/observations.test.ts
```

No additional source changes. Runtime footprint is validated through its receipt rather than pretending runtime paths belong to sessions. Preserve earlier evidence and diagnostic data; no repair/replay.
