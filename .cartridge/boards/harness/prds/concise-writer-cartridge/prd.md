---
repo: /Users/feb/dev/cartridge/harness.ctg
state: open
origin: requested
priority: 95
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
capability-owner: harness
canonical-scope: concise-writer-cartridge
review-round: 2
review-status: stale-after-migration
---

# One writer cartridge produces short, precise text

Create one independently installable writer cartridge that tunes drafting through
the existing harness. Own it under harness development; keep its implementation
separate from existing cartridges. Apply the user's Caveman / “i-have-hdhd”
direction: answer first, plain words, short sections, no repetition or decorative
prose. Memos must remain understandable without the original conversation.

## Acceptance

- [ ] Enable or remove the writer through composition alone. Its owned guidance
  governs replies and authored memos without a runtime fork, duplicated harness,
  mandatory second model call, or competing verbosity instructions. Update the
  effective register for this profile; preserve existing profiles.
- [ ] Before tuning, freeze 20 fixtures: 12 verbose drafts, four already concise
  texts and four precision-sensitive cases, including conversation-to-memo and
  direct-reply tasks. List required decisions, constraints,
  uncertainty, provenance and next actions per fixture. Preserve every required
  fact, negation, number, unit, command, quoted error and executable memo field;
  introduce no unsupported claim.
- [ ] On the verbose set, target median output tokens at most 50% of the existing
  writer baseline. Already concise inputs must not grow. Score readability and
  fact retrieval against frozen questions: retain baseline correctness and readable
  sentences. Missing meaning fails regardless of length; report irreducible cases.
- [ ] Compare baseline and candidate using the same real model, settings and
  fixtures across three runs. Record prompts, model/tokenizer revisions, outputs,
  token counts and rubric scores. Mock endpoints verify wiring only. Structured
  output, parser validity and explicit user requests for detail still work.
- [ ] Draft directly in the requested style. Existing memo rewrites are opt-in
  previews saved through validated memo writes with expected revisions; stale
  writes preserve newer text. Source transcripts and linked detailed evidence
  remain intact. Each failed criterion gets a linked, bounded repair item.

## Proof and review

Start at [harness assembly](../../../main.rs) and the existing
[register](../../../../../../.cartridge/memos/system/register.md).
Use disposable memo records and configured evaluation endpoints. Add fixtures to
`just test harness` and `just test memo` from the composed root; model evaluation
is a separate recorded gate. These checks have not run.

This is the concrete writer slice of [the composition proof](../../../runtime/prds/second-harness-composition-proof/prd.md).
[Review](review.md): round 2/5, inheriting its first round.
