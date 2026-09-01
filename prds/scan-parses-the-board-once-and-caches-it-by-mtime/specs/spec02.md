---
complexity: 10
footprint:
  - resources/questions.py
  - resources/board/plan.py
---

# spec02 — the drill count reads the same cache instead of re-parsing every prd.md

`cmd_scan` finishes by counting standing questions, and that count
(`drill_questions` → `questions.unanswered`) walks the board a second time and
calls `questions.parse` — its own reader — on every `prd.md`, re-reading and
re-parsing what `scan` just parsed. This unit points that reader at the cache
`scan` already filled: `questions.parse` consults the same store (plan.py's
`_PCACHE`, via one small accessor plan.py exposes) and pays a full parse only
on a miss. The drill count's answer does not change; the second walk stops
paying for the first walk's work again.

## Already standing

The cache in `plan.py` (spec01) is live and every `parse_prd` call made
anywhere already lands in it — the work here is only routing `questions.parse`
through it. Measured on this board: `questions.unanswered` costs ~12-14 ms of
a warm `cmd_scan`, most of it its own re-parse of ~81 `prd.md` files plus a
redundant second directory walk. `attempt.py` in the probe dir simulates this
wiring and measured warm `cmd_scan` at 29-39 ms with it in place.

## Acceptance

- [x] with a warm cache, `questions.unanswered` performs no `open` on any
      `prd.md` whose (path, mtime, size) the cache already holds, and returns
      the same question list it returned before the change — warm: 0 opens
      (was 81); list identical to the pre-change reader on all 81 PRDs
- [x] a PRD whose questions were just edited (new mtime/size) is re-parsed and
      the new question appears in `questions.py list` output on the next call
      — fixture: 1 open before, 2 open after the edit
- [x] `python3 resources/board/plan.py scan` prints the same drill count it
      printed before the change, on this board and on a fixture board holding
      one PRD with an open `### Q1:` round and one PRD with the matching
      `**Q1**` answer — fixture: asking 1 over 1 PRD before and after `answer`
      + rescan; real board: drill count unchanged (0 before, 0 after)

## Verify and Proof

```sh
python3 resources/questions.py list
python3 resources/board/plan.py scan | head -3
bash .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
```