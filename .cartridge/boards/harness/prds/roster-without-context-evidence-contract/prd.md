---
state: "blocked"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/harness.ctg"
needs: ["@harness/scoped-roster-context-contributor","@root/the-isolation-gate-reads-the-composition-profile/an-optional-need-with-no-provider-still-loads","@harness/the-working-memory-proof-accounts-for-the-jev-context-suffix"]
footprint: ["src/evidence.rs","src/lib.rs","src/roster.rs",".cartridge/tests/unit/roster_tests.rs",".cartridge/tests/integration/roster.test.ts","README.md",".cartridge/help.md",".cartridge/docs/roster.md","src/roster/capture.rs","src/roster/render.rs"]
---

# roster without context evidence contract

## Outcome

replace the general context evidence collector with bounded roster-specific capture and rendering, preserving the authenticated roster feature and removing the old wire schema/types.

## Acceptance

- [ ] actual sessions+harness composition renders the authorized roster under row/byte/deadline caps; disabled configuration makes no call and no block. Actor mismatch, unavailable/partial sources, malformed responses and deadline expiry produce explicit metadata without credentials or other scopes. Inspection retains source/composition revision meaning, omission/truncation and unavailable state. Prompt-like and closing-frame data remain escaped untrusted observations. Compaction/transcript gates still pass. No cartridge-context/v1 schema or generic Contribution/Prepared protocol is retained under a new name.

## Proof and recovery

Footprint starts: `src/evidence.rs`, `src/lib.rs`, `src/roster.rs`, new roster-specific responsibility modules if needed, `.cartridge/tests/unit/roster_tests.rs`, `.cartridge/tests/integration/roster.test.ts`, `README.md`, `.cartridge/help.md`, `.cartridge/docs/roster.md`; add `src/limits.rs`/`cartridge.json` only if actual retired-protocol names require changes. Preserve current caps rather than inventing settings changes. The old delivered roster PRD is baseline evidence, not a duplicate work item or a new round allowance.

## Dependencies and review

This slice inherits two used rounds from the context-deletion decomposition: round 1 failed at 66/100 and round 2 passed at 94/100. Three remain. Decomposition approval does not approve an executable spec. Preserve every requirement in the linked split plan and independently review the executable specification before implementation.

## Current prerequisite evidence

The implementation candidate 75a56fad43f6830115eb3870add922515279e124 is preserved in its clean lane. The unchanged base c8305341 also fails the mandatory working composition because the host treats absent optional jev? as required. The linked optional-needs prerequisite owns that defect. After it is delivered, rerun working, ring and slim with an explicitly identified current host binary, then obtain independent verification. Targeted tests pass but do not replace these gates. Full evidence is in ../../.state/loop/roster-without-context-evidence-contract/implementer-codex-1.md. No acceptance criterion or review allowance changes.

## Remaining proof prerequisite after host delivery

The optional-provider fix is collected at host 54749f4. A later committed host b4345b6 also clears the pinned Sessions ASP-schema startup failure: the exact rebuilt artifact activates stock Sessions and passes all five roster integration tests with 272 assertions. Reports implementer-codex-2.md and implementer-codex-3.md preserve both the earlier failure and the new proof. No broad ASP prerequisite is needed for that resolved failure.

The unchanged candidate 75a56fad now waits only on the linked working-memory proof correction. The same working.rs assertion fails on untouched c8305341, outside the roster footprint. Preserve the candidate and foreign assessment edits. After that prerequisite is delivered, rerun the full executable spec with the identified compatible host and obtain independent verification. No acceptance or review allowance changes.
