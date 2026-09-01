# Round — the round is moved out of the session that was asked

## Established
- a `/pearde` session opens at a 50,229-token floor and ended at 200,725 with 66k of content in it — measured off `~/.claude/projects/-Users-feb-dev-infra-pearde/252b219d*.jsonl`, first and max assistant `usage` · 09:05
- the transcript a hook is handed holds no sidechain turns, so a worker's window cannot be measured from the dispatcher's — same file, zero `isSidechain` entries · 09:10
- read and command stamps were keyed by path alone, so a second round worker in one session would be refused a file the first had read — fixed by `stamp_key`, probe C1–C3 · 09:30
- probe green: 26 checks · 26 pass · 0 fail; `the-loop-is-commands` 60/60; `doctor` closes green · 09:38
- `readme-in-three-rings` keeps one pre-existing failure: a freshly-init'd board has no `graph.json`, so `knowledge.py doctor` exits 1 and doctor's `knowledge` row reads `broken`. Reproduced with this branch stashed — not this PRD's · 09:34

## Decided
- the round runs in a `pearde-round` worker and the asked session only dispatches — it beat raising `context-budget`, which pays the same window again on every turn
- the budget is measured from the window's own floor — it beat leaving it absolute, which spent half the budget before the round read anything
- a worker keeps no ceiling of its own — it beat guessing one from the dispatcher's transcript, which is not its window

## Owed
- tell the user what changed, and that `.pearde/memos/` in this tree is another session's live work
