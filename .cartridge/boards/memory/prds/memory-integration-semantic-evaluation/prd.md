---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "2h"
actual: "3h — analyst probe plus the hand's runs; landed on main at `da15993c`"
---

# Measure production-model retrieval and grounded answers on realistic noisy project memory with reproducible provider identity.

Landed on main at `da15993c` (`tests/bench/`, `tests/e2e/eval_ground.rs`, `justfile`); every Check box closed in the lane, `just test` 1,502 passed.

## Do

Use the existing `memory-bench` ground and BEAM runners to build or select a realistic mixed corpus containing durable facts, stale and superseded claims, templates, similar names, and irrelevant prose. Pin dataset revision, retrieval configuration, provider URL class, embedding model, answer model, and source revision. Report retrieval and grounded-answer metrics separately, including unsupported answers and unavailable dependencies. Compare against the real-provider baseline recorded by [reconcile-the-ground-number](../reconcile-the-ground-number/prd.md); do not present the fake lexical embedder's 72-probe score as production semantic quality. Reuse [port-the-benchmark-runners](../port-the-benchmark-runners/prd.md) and do not add another framework.

## Spec

The probe is built and committed on branch `agent-a42ff0bba6eabd0e6`
(four commits on top of `60630ff9`); the lane worktree
`.claude/worktrees/memory-integration-semantic-evaluation` exists on branch
`memory-integration-semantic-evaluation` at `60630ff9` with a clean tree — the
analyst's harness refused git on the lane, so step 1 fast-forwards it. Only
defined work remains: fast-forward, re-run the documented invocations, land.

Files (all in the probe commits):

- `tests/bench/noise.json` — new. Four distractor sessions, 42 turns, CC0:
  `n1` similar names (Marta at Freightways, Biscotti the beagle, a second
  Jonas, Vos Logistics / Hanne, Gripped gym), `n2` superseded drafts and
  rejected alternatives (Delfshaven at 1400, Fender CD-60, the 6 GB
  intermediate peak, the late-April hike), `n3` templates with placeholders,
  `n4` unrelated prose sharing vocabulary (Maeslantkering, dal recipe, tokio
  changelog, a novel list naming The Overstory, Rotterdam–Oslo by rail,
  Postgres 17). Stale and superseded claims already live in `ground.json`'s
  `update` category (Biscuit three → four, Blaak → Katendrecht, 11 GB → 3.2 GB).
- `tests/e2e/eval_ground.rs` — one new test: no noise turn carries a
  `ground.json` anchor, duplicates a corpus turn, or reuses a session id.
- `tests/bench/src/ground.rs` — `--noise` ingests `noise.json` beside the
  corpus (labels included, so a distractor hit resolves to a key that is gold
  for nothing); `--answer` runs the grounded-answer leg on the direct path
  through the BEAM runner's `answer_question` (top-k turn texts are the only
  context, `ANSWER_SYSTEM` unchanged); `unretrieved_questions` lists the
  questions with no gold inside k; `dataset_revision` (sha256 of both data
  files, counts), `answer_model`, `answer_url_class`, `baseline` (0.735 /
  0.436 from [reconcile-the-ground-number](../reconcile-the-ground-number/prd.md)) and `direct.delta_vs_baseline`
  go into the report. A preflight `try_chat` "ping" that fails writes
  `grounded_answer: {status: blocked, reason}` into the report, prints
  `BLOCKED:` and exits 2 after the retrieval leg has run. `--answer` is
  refused under `--fake-llm` and on `--path distill`.
- `tests/bench/src/beam.rs` — `chat` split into `try_chat -> Result` (the
  backend's own `error` field counts as failure, so an unpulled model is a
  blocked run, not an empty answer) plus the panicking wrapper; the request
  carries `options: {temperature: 0, seed: 0}`; a missing
  `tests/eval/beam_<scale>.json` prints `BLOCKED:` and exits 2 instead of
  panicking. `ANSWER_SYSTEM`, `MAX_CONTEXT_CHARS`, `answer_question`,
  `coverage` are `pub(crate)` for `ground.rs`.
- `tests/bench/src/common.rs` — `base_report` adds `embed_url_class`
  (`local` / `ollama-cloud` for a `:cloud` tag on a loopback host / `remote`
  / `fake`), `retrieval` (`preset: medium` — `make_project` writes no preset
  so the binary runs `Preset::default()` — `k`, `max_deliver_results`), and
  `source_dirty` beside `commit`.
- `justfile` — `eval-ground` doc comment names `--noise` and `--answer`.

Grounded-answer scoring is deterministic token proxies, no judge — the
corpus has anchors, not rubrics, and a judge would put a second model's
non-determinism into a number the Check asks to reproduce:
`grounding` = fraction of the answer's content tokens found in the retrieved
context; `anchor_coverage` = fraction of the gold anchor phrase's tokens found
in the answer; `unsupported_answers` = answered (not the prompt's abstention
sentence) while no gold turn was among the top-k. The last is an upper
bound: the assistant echo turn often restates the user turn the label pins,
so a "hazelnut" answer read off `s4` turn 2 counts as unsupported when turn 1
missed the top-10. The report's `scoring` string says so.

What the probe measured (reports under `tests/eval/reports/` in the lane,
gitignored; `qwen3-embedding:0.6b` and `granite4:3b` on local Ollama,
`gpt-oss:20b` is also pulled and untried):

| run | recall_any@10 | recall_all@10 | MRR | grounded answer |
|---|---|---|---|---|
| clean, `--path direct` | 0.7353 | 0.6176 | 0.4357 | — (matches the 0.735 / 0.436 baseline) |
| `--noise --answer --llm-model granite4:3b`, run 1 | 0.6471 | 0.5588 | 0.4252 | answered 28, abstained 6, unsupported 8, grounding 0.841, anchor hit 0.676 |
| same, run 2 | 0.6471 | 0.5588 | 0.4252 | grounding 0.823, anchor_coverage Δ 0.004, unsupported 8 |
| clean, `--answer --llm-model no-such-model:latest` | 0.7353 | | | `grounded_answer.status: blocked`, `BLOCKED:` printed, exit 2 |
| `just eval-beam --mode retrieval` | | | | `BLOCKED: …/tests/eval/beam_100K.json missing`, exit 2 |

Noise costs 3 of 34 questions at k=10 (delta_vs_baseline −0.088); twelve
questions are listed under `unretrieved_questions`. Retrieval is exact across
runs; the answer means moved 0.018 with temperature 0, which sets the
tolerances below.

Steps, from `/Users/feb/dev/memory`:

1. Fast-forward the lane onto the probe:
   `git -C .claude/worktrees/memory-integration-semantic-evaluation merge --ff-only agent-a42ff0bba6eabd0e6`
   then `cd .claude/worktrees/memory-integration-semantic-evaluation`.
2. `cargo clippy --release -p memory-bench` and
   `cargo test --release --test e2e eval_ground` — clean and 5 passing.
3. The documented invocation, twice:
   `just eval-ground --path direct --noise --answer --llm-model granite4:3b`
   (about 2.5 minutes each; needs local Ollama with `qwen3-embedding:0.6b`
   and `granite4:3b` pulled). Keep both `report:` paths.
4. `just eval-ground --path direct` once — the clean number beside the
   noisy one.
5. `just eval-beam --mode retrieval` — exits 2 with `BLOCKED:` until someone
   converts the parquet split ([[beam-has-no-fetcher]]); that is the
   recorded state of BEAM, not a failure of this memo.
6. Run the Check block; tick boxes as they close; `just land
   memory-integration-semantic-evaluation`.

Not done and not owed here: a judge-scored answer leg, `--answer` on the
distill path, a BEAM fetcher.

## Acceptance
- [x] `just eval-ground --path direct --noise --answer --llm-model granite4:3b` writes a report whose `dataset_revision.ground_sha256` and `noise_sha256` are 64 hex chars, `embed_model`, `embed_url_class`, `answer_model`, `answer_url_class`, `retrieval.preset`, `retrieval.max_deliver_results`, `commit` and `source_dirty` are set, and `direct.turn_granularity` carries `recall_any@1`, `recall_any@5`, `recall_any@10`, `recall_all@10`, `mrr`, `ndcg@10`
- [x] the same report lists `direct.unretrieved_questions` and a `direct.grounded_answer` block with `answered`, `abstained`, `unsupported_answers`, `grounding_mean`, `anchor_coverage_mean`, separate from `turn_granularity`
- [x] a second identical run agrees: recall_any@10 and recall_all@10 exactly, MRR within 0.001, `grounding_mean` and `anchor_coverage_mean` within 0.05, `unsupported_answers` within 2
- [x] `just eval-ground --path direct` (clean corpus) reports `recall_any@10` within 0.03 of `baseline["recall_any@10"]` (0.735) and the report carries `direct.delta_vs_baseline`
- [x] `just eval-ground --path direct --answer --llm-model no-such-model:latest` exits 2, prints `BLOCKED:`, and its report has `grounded_answer.status == "blocked"` with a `reason`
- [x] `just eval-beam --mode retrieval` exits 2 and prints `BLOCKED:` while `tests/eval/beam_100K.json` is absent
- [x] `--fake-llm` reports still carry `MEANINGLESS`, and `--fake-llm --answer` is refused
- [x] `cargo test --release --test e2e eval_ground` passes, including `noise_turns_carry_no_anchor_and_duplicate_no_corpus_turn`

```sh
set -e
cd .claude/worktrees/memory-integration-semantic-evaluation
cargo clippy --release -p memory-bench
cargo test --release --test e2e eval_ground 2>&1 | grep -q "noise_turns_carry_no_anchor_and_duplicate_no_corpus_turn ... ok"
rep() { grep '^report:' | sed 's/^report: //'; }
A=$(just eval-ground --path direct --noise --answer --llm-model granite4:3b | rep)
B=$(just eval-ground --path direct --noise --answer --llm-model granite4:3b | rep)
C=$(just eval-ground --path direct | rep)
for k in '.dataset_revision.ground_sha256' '.dataset_revision.noise_sha256'; do jq -e "$k | test(\"^[0-9a-f]{64}$\")" "$A" >/dev/null; done
for k in embed_model embed_url_class answer_model answer_url_class retrieval.preset retrieval.max_deliver_results commit source_dirty \
	'direct.turn_granularity["recall_any@1"]' 'direct.turn_granularity["recall_any@5"]' 'direct.turn_granularity["recall_any@10"]' \
	'direct.turn_granularity["recall_all@10"]' direct.turn_granularity.mrr 'direct.turn_granularity["ndcg@10"]' \
	direct.unretrieved_questions direct.grounded_answer.answered direct.grounded_answer.abstained \
	direct.grounded_answer.unsupported_answers direct.grounded_answer.grounding_mean direct.grounded_answer.anchor_coverage_mean \
	direct.delta_vs_baseline; do jq -e ".$k != null" "$A" >/dev/null || { echo "missing $k"; exit 1; }; done
d() { jq -n --argjson x "$(jq "$1" "$2")" --argjson y "$(jq "$1" "$3")" '($x - $y) | if . < 0 then -. else . end'; }
within() { v=$(d "$1" "$A" "$B"); echo "$1 delta=$v tol=$2"; [ "$(jq -n "$v <= $2")" = true ]; }
within '.direct.turn_granularity["recall_any@10"]' 0
within '.direct.turn_granularity["recall_all@10"]' 0
within '.direct.turn_granularity.mrr' 0.001
within '.direct.grounded_answer.grounding_mean' 0.05
within '.direct.grounded_answer.anchor_coverage_mean' 0.05
within '.direct.grounded_answer.unsupported_answers' 2
jq -e '(.direct.turn_granularity["recall_any@10"] - .baseline["recall_any@10"]) | (if . < 0 then -. else . end) <= 0.03' "$C" >/dev/null
set +e
out=$(just eval-ground --path direct --answer --llm-model no-such-model:latest); rc=$?
set -e
[ "$rc" = 2 ] && echo "$out" | grep -q '^BLOCKED:'
jq -e '.grounded_answer.status == "blocked" and (.grounded_answer.reason | length > 0)' "$(echo "$out" | rep)" >/dev/null
set +e
out=$(just eval-beam --mode retrieval); rc=$?
set -e
[ "$rc" = 2 ] && echo "$out" | grep -q '^BLOCKED:'
F=$(just eval-ground --path direct --fake-llm | rep); jq -e '.MEANINGLESS' "$F" >/dev/null
! just eval-ground --path direct --fake-llm --answer >/dev/null 2>&1
echo CHECK OK
```
