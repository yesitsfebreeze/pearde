# The example board

One row in every band of the pressure order, and the board the quickstart
opens. `python3 resources/board/plan.py example <dir>` copies it. Never run in
place — a ticked box here changes what every other check sees.

| PRD | state | shows |
|---|---|---|
| `landed` | `done` | the landed band — a `commit:` a reader can follow and an `actual:` the calibration reads |
| `building` | `claimed` | in flight — five boxes, three closed, a claim held since a written timestamp |
| `finished` | `claimed` | to collect — every box closed and `prd.md` clean, the band that leads every list |
| `asking` | `question` | waiting on you — one pass, three answers, one recommended, rendered as picks |
| `next` | `open` | gated — it needs `building`, and the scan says so |
| `big` | `open` | the tree — a parent that weighs zero, with `big/first` landed and `big/second` open |

| beside them | holds |
|---|---|
| `settings.md` | the board name `example`, in English |
| `memos/` | the one decision this board records |
| `workflows/` | one route of two atomics, followed by `building` |

Every date is written, never stamped. `building`'s claim reads `2026-08-28
13:49`, so the rendered holding time grows with the clock and the view's gate
normalises it before comparing snapshots.
