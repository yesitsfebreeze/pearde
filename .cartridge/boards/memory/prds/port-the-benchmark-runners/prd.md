---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# the benchmark runners in tests/bench become Rust — ground and beam kept, LoCoMo and LongMemEval dropped — and the last Python leaves the tree

Done 2026-09-05: `tests/bench` is the `memory-bench` workspace crate — `ground`
and `beam` subcommands over `src/{common,ground,beam,score,pylit}.rs`, the e2e
`harness`, `ranking` and `fake_llm` modules included by path so the benchmark
drives the same project the suite does. `MemoryProject::with_bin` and three
`Config` fields (`embed`, `reason`, `max_deliver_results`) were added for it.
`just eval-ground --path direct` reported recall_any@10 0.735 / mrr 0.436 over
the 34 committed questions against qwen3-embedding:0.6b. BEAM's dataset
fetcher went with the rest of the Python and has no replacement:
`beam-has-no-fetcher`.

## Do

Port `tests/bench/run_ground.py` and `run_beam.py`, with `score.py` and the
parts of `common.py` they use, to one Rust binary target (`memory-bench` or a
`[[bin]]` under `tests/bench/`) that drives the built `memory` through
`tests/e2e/harness.rs`'s `MemoryProject` against a real Ollama named by flag.
Delete `run_locomo.py`, `run_longmemeval.py`, `datasets.py`, `harness.py`,
`ranking.py`, `fake_llm.py`, `requirements.txt` and `just bench-install`;
`just eval-ground` and `just eval-beam` call the binary. The scorer's
properties (`recall_any` vs `recall_all` on partial multi-evidence, `ndcg`,
`percentile`) come back as unit tests in the binary.

## Acceptance
`rg -l '\.py$' tests` prints nothing; `just eval-ground --path direct` prints
a report against a local Ollama; `cargo nextest run --workspace` runs the
scorer tests.
