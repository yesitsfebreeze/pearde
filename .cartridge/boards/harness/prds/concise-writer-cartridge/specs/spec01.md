---
complexity: medium
footprint:
  - src/main.rs
  - Cargo.toml
  - .cartridge/packages/writer.ctg
  - .cartridge/tests/integration/writer.rs
  - .cartridge/docs/writer.md
---

# spec01 — One optional writer policy in the existing harness

Ship an independently installable pure Lua cartridge under
`.cartridge/packages/writer.ctg`. A profile adds its entry and injects `writer`
into the existing harness. Harness system-memo assembly calls that optional
provider once, without a model request, before its existing size and framing
checks. Profiles without the injection keep their exact assembly. Removing the
entry and injection restores them.

Writer exposes its single owned guidance text and composes the effective system
memo response. Replace the configured local register slot; retain all other
memo bodies and order, the distillation debt, caller instructions and transcript.
Reject ambiguous or unrecognized rendering instead of silently losing content.
The guidance replaces competing surface registers with plain complete sentences,
answer first, no repetition, preserved facts and user-requested detail. Existing
source register and profiles remain unchanged. Document the two profile edits.

Memo rewriting is explicitly requested: return a preview bound to the read
revision, then save that exact proposal only through memo.write with its expected
revision. No automatic save, retry, transcript edit or second-model rewrite.
Use existing memo validation and revision-conflict behavior. Invalid data or
provider failure is explicit and leaves durable state intact.

## Acceptance

- [x] A real native harness plus Lua writer profile produces one effective writing policy; removal restores the original prompt, with the same journal and no router calls.
- [x] Other memos, structured fields, explicit user detail and instruction framing survive; ambiguous renderer input and missing configured providers fail explicitly.
- [x] Real memo preview has no disk effect; accepted save uses the expected revision; a stale proposal preserves a newer valid memo and source transcript/evidence.
- [ ] The separately recorded 60 baseline and 60 candidate real-model responses use the frozen corpus, rubric, settings and same model/tokenizer digest. Every required fact, protected literal, format and readability question is scored. Report length targets and irreducible cases; link a bounded repair for each failed criterion and do not claim a failed gate passed.

## Verify and Proof

```sh
bun /Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/harness/prds/concise-writer-cartridge/verify-isolated.ts "$PWD"
```

The verifier copies the chosen owner and its adjacent runtime/workspace sources,
records every source digest and runs public harness/memo tests and harness check.
It repeats against the integrated owner during collection. The original PRD lane
cannot directly join the sibling Cargo workspace. Preserve concurrent edits.
The model evaluation is a separate gate; deterministic integration doubles prove
wiring only. A failed model criterion leaves this PRD unfinished until repaired.
