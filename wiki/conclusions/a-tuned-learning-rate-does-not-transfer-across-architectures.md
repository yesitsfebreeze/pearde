---
title: a-tuned-learning-rate-does-not-transfer-across-architectures
date: 2026-09-02
type: conclusion
tags: [a0, conclusion, experiment, learning-rate]
sources:
  - "[[260902-d570]]"
  - "[[260902-a6c8]]"
derived_from: []
---

# A tuned learning rate does not transfer across architectures — zirkle's A0-pre rates are wrong for this tree's MLP arm at every width

zirkle A0-pre measured four per-arm rates on a two-block transformer over wiki.txt at 150 steps. This tree's A0 arm is a two-layer MLP over synthetic transformation families. Re-measured here at arm load, the optima are 3e-3 / 1e-2 / 2e-2 / 2e-2 against zirkle's 2e-3 / 3e-3 / 5e-3 / 1.2e-2 — no width agrees, and at n=16 the borrowed rate costs 1.32 held-out against 0.166 at the measured one. A rate tuned on one architecture is not a rate for another; the confound the parent PRD calls closed is closed in zirkle, not here.
