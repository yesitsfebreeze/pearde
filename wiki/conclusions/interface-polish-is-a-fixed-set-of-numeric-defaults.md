---
title: interface-polish-is-a-fixed-set-of-numeric-defaults
date: 2026-09-03
type: conclusion
tags: [conclusion, design-system, frontend, ui-polish]
sources:
  - "[[260903-eb69]]"
  - "[[260903-d9f4]]"
derived_from: []
---

# interface-polish-is-a-fixed-set-of-numeric-defaults

Interface polish is not a vibe check but a short list of fixed numeric defaults applied the same way everywhere a pattern recurs: outerRadius = innerRadius + padding for any nested rounded surface, exact scale/opacity/blur values (0.25 to 1, 0 to 1, 4px to 0px, spring bounce 0) for icon-state swaps, scale(0.96) never lower than 0.95 for press feedback, and a 40x40px minimum hit area for anything interactive — each one a number a reviewer can check against code rather than an opinion argued case by case.

Consequence: a polish review runs as a before/after diff table per principle, citing the file and property changed, so the fixed defaults stay enforceable instead of drifting per component.
