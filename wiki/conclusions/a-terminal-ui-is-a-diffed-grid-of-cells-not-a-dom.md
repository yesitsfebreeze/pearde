---
title: a-terminal-ui-is-a-diffed-grid-of-cells-not-a-dom
date: 2026-09-03
type: conclusion
tags: [color, conclusion, rendering, terminal, tui]
sources:
  - "[[260903-f670]]"
  - "[[260903-9c7a]]"
derived_from: []
---

# a-terminal-ui-is-a-diffed-grid-of-cells-not-a-dom

A terminal UI has no DOM, no CSS, no pixels — every design decision resolves to a character, a foreground/background color, and SGR style flags on a fixed (row, col) grid, so layout is integer math against reserved chrome rows and color is a semantic role rather than a value: the renderer diffs a current and a next buffer each frame and flushes only the delta in one write, while the role-to-index mapping (error, success, warning, info) is resolved differently per surface — native terminals inherit the user's own ANSI 16 palette, xterm.js needs an explicit theme object since it ships no inherited palette at all.

Consequence: a TUI spec keeps layout math, box-drawing, and the diff/flush loop identical across native terminal and xterm.js targets, and isolates the one thing that legitimately differs — color resolution — behind a role table instead of a shared hex palette.
