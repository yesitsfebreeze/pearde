---
kind: work
level: 10
status: done
description: the ground corpus is the only benchmark instrument that survived the purge and it answers 0.735 where the record publishes 0.824 — re-run it and settle which number is current
read_when: "quoting the ground corpus"
---

# reconcile-the-ground-number

Done 2026-09-05: 0.735 reproduced. Four consecutive `just eval-ground --path
direct` runs gave recall_any@10 0.7352941176470589 and identical
recall_all@10, recall_any@1/5 and NDCG@10; MRR agreed in three of four and
moved 3.6e-5 in the fourth, which is smaller than any rank flip inside k and
so is a gold item past rank 10 moving a place. The ground paragraph in
`measurement-verdicts` now states 0.735 with its date, its runner and its
embedder, and keeps the 0.824 sentence beside it naming the deleted Python
runner. The distill number, 0.324, came from that same deleted runner and is
still owed a re-run.

## Do

`measurement-verdicts` publishes the ground corpus at direct recall_any@10
**0.824** / MRR 0.407. [[@prd/work/memory--port-the-benchmark-runners.md]] recorded **0.735** / MRR
0.436 on 2026-09-05 from the Rust port, same 34 committed questions, same direct
path, same `qwen3-embedding:0.6b`. Recall fell 0.089 while MRR rose 0.029.
Neither part cites the other and the older instrument is deleted, so this is the
only published number the tree can still re-derive
(`every-published-number-is-unreproducible`).

Run `just eval-ground --path direct` against a local Ollama holding
`qwen3-embedding:0.6b` and compare all three. One cause is already ruled out:
the delivery cap is not truncating recall@10, because `ground.rs:202` sets
`max_deliver_results` only when `k > 25` and every preset's default is at least
12 (`src/config/src/config.rs:427-441`).

If the run reproduces 0.735, the ground line in `measurement-verdicts` is
rewritten to that number with its date and the runner that produced it, and the
0.824 sentence stays beside it naming the deleted Python runner — an edit adds,
it never deletes the sentence it corrects ([[SYSTEM]]). If it reproduces neither,
the port is not deterministic across runs, which is a defect in the last
instrument standing and gets its own work part.

## Check

`just eval-ground --path direct` prints a recall_any@10 for the 34 questions,
and the ground paragraph in `measurement-verdicts` names the runner and the date
of every number it states.
