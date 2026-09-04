---
atomic: reproduce-the-failure
subject: turns the report into a command that fails on this tree, so the fix has a check
date: 2026-09-04
runs: 0
tags:
  - atomic
---

## Do

1. Run the command the report names against a real instance of the state it needs (here: a real board, `python3 resources/pearde.py vault <dir> --dir pearde`).

## Done when

- the run raises the exact error the report describes

## Fails when
