---
title: shipping-a-pr-and-landing-it-in-production-are-different-gat
date: 2026-09-04
type: conclusion
tags: [conclusion, deploy, gate, merge]
sources:
  - "[[260904-b1e7]]"
  - "[[260904-455c]]"
derived_from: []
---

# shipping-a-pr-and-landing-it-in-production-are-different-gates

Splitting "open the PR" from "merge, wait on CI/deploy, verify prod" lets each half carry the gate suited to its risk: the merge step gets a readiness report because it's the irreversible action, and the post-deploy step gets a canary whose depth scales with blast radius instead of running the same fixed checklist on a one-line doc fix and a full frontend rewrite. Fixed-depth verification either wastes time on low-risk changes or under-checks high-risk ones — scoped depth avoids both.

Consequence: pearde's collect/transition gate, which already routes on a verdict word, could scale what it checks by PRD change-scope the same way — a docs-only PRD should not clear the same gate as one touching the board's core commands.
