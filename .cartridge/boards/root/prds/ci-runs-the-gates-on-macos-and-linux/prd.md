---
state: open
origin: requested
priority: 72
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 4
date: "2026-09-15"
footprint:
- ".github/workflows"
needs:
- the-repository-answers-by-text
---

# CI runs the gates on macOS and Linux

## Outcome

The composed gates run on every push on the two supported hosts.

## Acceptance

- [ ] Both jobs check out the pinned composed revision and run `just check && just test && just isolation`; Windows is named as excluded with no `continue-on-error`.

## Folds

Deferred with `superseded-by` pointing here:

- @runtime/ci-proves-the-supported-terminal-matrix
- root memo `prd/the-windows-runner-gates-again`

## Result

Not started.
