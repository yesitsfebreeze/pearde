---
complexity: 15
footprint:
  - references/parts/workers.md
  - references/parts/loop.md
  - references/parts/solo.md
  - .pearde/prds/the-board-runs-itself/brief-is-printed/probe
---

# spec01 — the lookup leaves the orchestrator's prose

`workers.md` no longer holds the verdict→command table, and `loop.md` step 6
no longer restates it. Three prose spots name the one call instead:
`collect <prd> --report <path>` (analyst "On return", implementer "On
return", the report-is-a-file paragraph), `loop.md` step 6, and `solo.md`
step 4. The judgment the PRD keeps prose — believe the report, and whether a
`## Workflow` edit was the atomic's fault or the code's — stands. The probe
code and the tool half are already in the tree from pass one. The
brief-is-printed harness pinned the removed prose — its swallowed-text check
looked for the `<x>` the old "On return" line carried — and is re-aimed to
the one-problem reality (already done this pass; the implementer re-runs it).

## Acceptance

- [x] `references/parts/loop.md` no longer holds the text `SPECCED → \`pearde specced\`` — the command mapping is gone from the loop step (grep -q finds 0)
- [x] `references/parts/workers.md` names `--report` in the analyst and implementer "On return" spots and keeps the two judgment sentences (believe; whose fault) (lines 297, 305, 326)
- [x] `bash .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh` prints `104/104 checks pass` — the re-aimed harness stays green
- [x] `bash resources/doctor.sh` prints `briefs ok` — the brief blocks survive the edit (`briefs      ok      5 blocks`)

## Verify and Proof

```sh
! grep -q "SPECCED → \`pearde specced\`" references/parts/loop.md && grep -q -- "--report" references/parts/workers.md && bash .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh 2>&1 | grep -q "104/104 checks pass" && echo "$(bash resources/doctor.sh 2>&1)" | grep -qE "briefs +ok" && echo PROSE-OK
```