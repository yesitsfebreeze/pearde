---
title: e2e-and-unit-tests-both-trade-fixed-waits-for-explicit-state
date: 2026-09-04
type: conclusion
tags: [conclusion, cypress, frontend, testing, vitest]
sources:
  - "[[260904-51f7]]"
  - "[[260904-f1ee]]"
derived_from: []
---

# e2e-and-unit-tests-both-trade-fixed-waits-for-explicit-state

Cypress and Vitest solve flakiness from opposite ends of the same rule: Cypress replaces a fixed cy.wait() with a per-element timeout so the test waits exactly as long as the real page does, and Vitest replaces implicit module/mock persistence with an explicit reset — vi.resetModules(), vi.clearAllMocks() in both hooks — so no test inherits state from the one before it. Both also push structure out of the test body into one named layer: Cypress into a Page Object class holding every selector, Vitest into a factory function holding every fixture — the test itself stays a call plus an assertion, never a raw selector string or a hand-built object literal.

Consequence: a flaky test in either suite has the same first diagnostic step — find the implicit wait or the leaked state, not the assertion that failed.
