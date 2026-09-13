---
complexity: small
footprint: ["src/inspection.rs","src/accounting.rs",".cartridge/tests/unit/accounting.rs",".cartridge/tests/integration/working.rs","Cargo.toml","src/main.rs","src/roster.rs",".cartridge/tests/unit/main/tests.rs",".cartridge/tests/unit/inspection_tests.rs",".cartridge/tests/unit/working_tests.rs",".cartridge/tests/unit/roster_tests.rs",".cartridge/tests/integration/roster.test.ts",".cartridge/docs/roster.md"]
---

# spec01 — Label local token estimates and keep usage attribution separate

Estimate the exact current harness projection with the versioned heuristic
ceil(serialized UTF-8 bytes / 4). This is explicitly high-uncertainty, has no
installed model tokenizer, and is never used as a context-window or enforcement
bound. Identify any session model hint, with unknown model/tokenizer represented
as null. Hash the serialized projection to identify what was estimated. Include
configured byte headroom and its separately labelled heuristic token equivalent.

List numeric provider usage from model_turn_finished records separately, keyed
by run, turn sequence and journal record, with requested/reported model metadata
when present. Do not claim those records measure the currently assembled request.
Do not invoke models or tokenization services. Add a visible inspector item and
structured tokens field; preserve existing byte safeguards and exchange grouping.

## Acceptance

- [x] Multilingual text, schemas and complete tool exchanges produce labelled nonzero estimates while existing byte limits and output reservation still hold.
- [x] Unknown model/tokenizer remain explicit with high uncertainty; inspection performs no model call.
- [x] Historical provider usage keeps run/turn attribution, never replaces the current estimate, and contains no transport credentials.

## Verify and Proof

```sh
cargo test --manifest-path Cargo.toml -p harness
```

Deterministic unit and real-process inspection fixtures only. Preserve and rerun
the collected compaction comparison proof because inspection is shared source.
