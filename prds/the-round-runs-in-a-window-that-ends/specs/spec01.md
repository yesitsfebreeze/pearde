---
complexity: 12
footprint:
  - resources/guard.py
  - references/agents/pearde-round.md
  - references/parts/dispatch.md
  - references/parts/loop.md
  - references/parts/guard.md
  - references/parts/workers.md
  - references/skills/pearde.md
  - references/settings.md
  - README.md
  - index.md
  - references/files.md
  - .pearde/.gitignore
---

# spec01 — the dispatcher holds nothing, and the ceiling hands over

One unit: the session that is asked stops working the board, and the budget
stops charging the round for the window it opened in. The two are one change
because either alone leaves the same complaint — a ceiling that stops the
work — standing.

What already stands, built in this PRD's round and verified by its probe:

- `references/agents/pearde-round.md` — the round worker type: it reads the
  round file, works @references/parts/loop.md, and hands back one of `MORE`,
  `ASK`, `DRAINED`, `BLOCKED`.
- `references/parts/dispatch.md` — what the asked session does instead: start
  a worker, read its line, put an `ASK` round to the user from
  `.pearde/.state/ask.md`, start the next one. It opens no PRD and runs no
  command but `status`.
- `references/skills/pearde.md` — the entry point now sends the session to
  that one file rather than to `@README.md` and the reference tree behind it.
- `resources/guard.py` — `budget()` measures `ctx - floor`, `floor` being the
  smallest window the session has been billed for; `Agent`/`Task` and
  `AskUserQuestion` join the calls that survive the ceiling, and the deny text
  names the handover. `stamp_key()` scopes the repeat-read and repeat-command
  stamps by `agent_id`, so a second round worker is never refused the first
  read of a file the first one read.
- the eight steps, `guard.md`, `workers.md`, `settings.md`, the README's core
  ring, `index.md` and `references/files.md` say the same thing the code does.

## Acceptance

- [x] A window is judged by what it grew, not by how large it is: a session
      whose floor is 60k passes at 150k and is refused at 170k, and a session
      whose first turn is 99k is not over a 100k budget — probe A1–A4,
      `ok A2 90k of growth over a 60k floor passes`,
      `ok A3 110k of growth is refused`
- [x] At the ceiling the round file, a dispatch and a question to the user are
      all still allowed, and the refusal text says to hand over rather than to
      stop — probe B1–B7, including
      `ok B5 the refusal names the handover, not a stop`
- [x] A worker's tool call is never refused on the dispatcher's window — probe
      B4 (`agent_id` present, 170k window, `allow`)
- [x] Repeat-read stamps belong to one window: the third read by one worker is
      refused, the next worker's first read is not — probe C1–C3
- [x] The dispatcher, the round worker and the four verdicts are on disk and
      named where a reader looks — probe D1–D9, D11, D12
- [x] `references/parts/loop.md` is still one page at 170 lines or fewer —
      probe D10
- [x] The board's own harnesses that pin these documents are green:
      `.pearde/prds/the-board-runs-itself/the-loop-is-commands/probe/verify.sh`
      60/60, and
      `.pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh`
      74 checks with only the pre-existing `knowledge` row failing (a fresh
      board has no `graph.json`; reproduced on `main` with this branch
      stashed, so it is not this PRD's)
- [x] `bash resources/doctor.sh` closes green — `index ok`, `briefs ok`,
      `skills ok 15 well-formed`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/the-round-runs-in-a-window-that-ends/probe/verify.sh
bash .pearde/prds/the-board-runs-itself/the-loop-is-commands/probe/verify.sh | tail -1
[ "$(wc -l < references/parts/loop.md)" -le 170 ] && echo "loop.md one page"
bash resources/doctor.sh | tail -1
echo "verify done rc=$?"
```
