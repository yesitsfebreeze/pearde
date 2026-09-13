# Concise writer — review

Canonical plan: [concise-writer-cartridge](prd.md).
Reviewer: side-conversation assistant, self-review. No product evaluation has run.

## Inherited round 1

This slice refines the [second-harness experiment](../../../runtime/prds/second-harness-composition-proof/review.md).
It inherits one used round, not the parent's score. No standalone writer score
existed in round 1. Scope: composition-level customization of authored output.

## Round 2 — 2026-09-13

User feedback: use one cartridge to produce precise, short, digestible replies
and memos, inspired by Caveman / “i-have-hdhd”. These are style references here;
no external plugin implementation or clinical benefit is assumed.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 20 | One installable writing policy; concrete reply and memo outcomes. |
| Ownership and reuse | 19 | Harness owns development; reuse existing register and memo validation. Packaging is determined during the composition probe. |
| Dependencies and slices | 19 | A bounded fixture corpus precedes tuning; current profiles remain usable. Failed extension seams become owner-local repairs. |
| Acceptance and baseline | 18 | Fixed corpus, paired model settings, three runs, 50% median target and mandatory meaning preservation. Fixture questions and readability rubric must be frozen before evaluation. |
| Failure and compatibility | 18 | Protect exact technical content, uncertainty, typed fields, source evidence and stale revisions; preserve requested detail. Negative fixtures remain to be authored. |

**94/100 — PASS** for the plan; no blocking plan findings.
Inputs are bound in [review-inputs.json](review-inputs.json). Local links, five
acceptance criteria, word limit and input digests checked. No model-quality or
implementation pass is claimed.

Rounds used: 2/5; remaining: 3. Next: build the disposable writer prototype and
run its paired evaluation. Brevity never compensates for lost meaning.

## Round 3 — frozen corpus and implementation boundary

Reviewer: Codex self-review; no independent agent was spawned because session
instructions restrict delegation. Inputs include the frozen corpus, rubric,
baseline guidance, recorded baseline outputs, current memo system response and
harness assembly. See review-round-3-inputs.json for content digests.

Value/scope 19; ownership/reuse 19; dependencies/slices 18; acceptance/baseline
19; failure/recovery/compatibility 19. **94/100 — PASS for the plan**, not model
quality. The bounded optional hook does not fork the runtime or duplicate the
harness. Existing memo writes retain validation and stale guards. The baseline
has missing facts, so correctness is scored against frozen facts as well as the
baseline. Length failure stays visible and blocks completion. Concurrent harness
changes require isolated implementation and explicit integration preservation.
Three rounds used; two remain. No blocking plan finding.

## Round 4 — preserve failed model results; evaluate local model compatibility

Reviewer: Codex self-review. Both Granite candidates failed frozen meaning,
concise-input and format gates; their length target failed too. These results
remain failures. The bounded repair tests the unchanged first candidate guidance
on the already installed gpt-oss:20b using a new paired baseline, the identical
20-case corpus and unchanged meaning/readability/length criteria. No case is
removed. Evaluation settings and exact model digest were frozen before this pair.

Native generated-token totals include reasoning for this model. Measure visible
text by native raw-input tokenization instead, with model special-token insertion
disabled and requests retained; report generation totals separately. This is
metering in the evaluation, not another production drafting pass. A passing pair
would qualify only its tested model; Granite remains unqualified with linked
failures. Value 19, ownership 19, dependencies 19, evidence 19, recovery 19:
**95/100 — PASS for the revised evaluation plan**, no quality pass claimed.
Four rounds used, one remains. Inputs: evaluation/gptoss-pair.json, frozen corpus
and rubric, unchanged candidate-guidance.txt, run.ts, and the two failed complete
Granite response sets, bound in review-round-4-inputs.json.

Implementation proof clarification: the already-reviewed disposable-copy fallback
is now executable in verify-isolated.ts. It retains owner manifests, records
source digests, and runs the three specified public gates; no acceptance outcome
changed. The first three deterministic checks passed. Candidate prompt tuning
continues within the reviewed frozen-corpus evaluation; all variants are retained.
