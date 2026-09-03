---
state: done
origin: requested
priority: 21
complexity: 6
blast-radius:
actual: 1.85h
---

# runs meets the report count

*Source: `docs/content/docs/improvements/workflows-runs-check.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** workflows · **Axis:** reliability (8 → 9) · **Pulls the score up
by ~2 points**

## Why now

`runs:` on the frontmatter counts every run, and the report section per run
folds the lesson back in — the library's whole improvement mechanism. But
the counter is the one number in the machine trusted without a check: a
run that wrote its report and died before the frontmatter increment leaves
`runs:` one behind the reports. Nothing notices, and the counter is the
number a worker reads to judge "how settled is this how".

## The change

The doctor row's workflow check counts the report sections and reads
`runs:`; the two disagreeing is `broken`, named with both numbers. No
backfill, no auto-repair — the counter is the *claim*, the reports are the
*evidence*, and a break names both numbers so the fix is one edit.

## Done when

- A workflow with four report sections and `runs: 3` is `broken` on the
  doctor row, both numbers in the line.
- The same file with `runs: 4` reads `ok` — and a run that adds its report
  and bumps the counter in one atomic write (the write the templates
  already specify) never trips the check.
- A workflow with a report section the check cannot parse (no heading
  shape) names the file and the section, the way a dangling slug is named.

## Fails when

- A run's report is written but the counter bump lands in a later commit —
  an honest two-step write reads as broken between steps. Guard: the check
  counts *report sections*, not commits; an in-flight run's own state
  (`runs:` being written) is the writer's lock, not the check's.

## What stays out

No rewrite of the report grammar — this page adds one comparison to an
existing check, which is why it is cheap enough to be first.

## Questions

### Q1: How the check counts past uses

You are choosing how the check remembers past uses: a permanent running
tally that grows every time, or only what is currently visible right now.
Either way decides whether a well-used routine gets flagged as broken the
moment older records are cleared away, even though nothing is wrong?

1. **Compare the snapshot, but only one way** — judge by what is currently visible, and only warn when there are more records than expected, never fewer. (recommended)
2. **Keep a running tally** — a permanent count updates with every use, so a mismatch always means a real problem, never a natural gap.
3. **Compare the snapshot both ways** — judge by what is currently visible, and treat any difference in either direction as a problem to report.

<!-- for the board: resources/doctor.sh workflows row + resources/workflows.py check() — compares occurrences of `## Workflow <slug>` across .pearde/prds/*/report.md against `runs:` on the matching .pearde/workflows/<slug>.md; probed on probe-then-spec: 33 live report sections vs runs: 61, a steady-state gap from report.md being overwritten each pass, not a fault. spec01/spec02 in this PRD's specs/ once answered. -->

## Answers

**Q1** *(answered 2026-09-03 18:30)* — Compare the snapshot, but only one way — judge by what is currently visible, and only warn when there are more records than expected, never fewer.

## Report

spec01: exit 0
OK — 2 problem(s):
  broken-flow.md: 4 report sections in prds/*/report.md, runs: 3 — the counter is behind the evidence
  prds/p2/report.md:1: `## Workflow` — a report section heading names no slug

spec02: exit 0
152:  outnumber its own `runs:` — never the other way: a report is overwritten
155:- a `## Workflow` report-section heading naming no slug
