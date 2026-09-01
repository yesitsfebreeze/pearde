---
complexity: 5
footprint:
  - .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/fixture.py
  - .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh
---

# spec02 — the transitions fixture pays the drill gate it was written before

`gate_claim` refuses every dispatch while two or more unanswered questions have
not yet been put to the user — `asking N — drill first`. The escape is part of
the design: `plan.drill_questions` marks a question `out` when the round file's
`## Asked` already lists it, by title, normalized. The transitions fixture
builds a board carrying four unanswered questions and writes no round file, so
from the moment the gate landed every `claim` in that harness was refused for a
reason the harness was not testing — eight failures in one file.

The fixture now writes `<board>/.state/round.md` with an `## Asked` section
holding the four titles, which is what an orchestrator that had actually put
them would leave behind. The board under test is unchanged in every other
respect; the gate is exercised, not disabled.

## What the probe already established

`plan.drill_questions` on the fixture board returns four questions, none of
them still unput. `set building done --force` then `claim next impl-1` exits 0,
and the drill gate never appears in its output. Truncating the round file on an
otherwise identical board puts all four back on the frontier and the same
`claim` is refused, exit 1, `asking 4 — drill first` — so the fixture edit is
load-bearing and the check can fail in both directions.

The harness's own `clean()` and its `STRAY` filter were re-aimed at
`.pearde/.state/` in the same pass, for spec01's reason: `transitions.jsonl`
was already named there by hand and the parse cache had joined it. The
harness's separate `.history.jsonl byte-identical` check and its explicit
`transitions.jsonl` greps still hold, so nothing that moved into `.state/` went
unwatched.

## Acceptance

- [x] `bash .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh` exits 0 and prints `74 checks · 74 pass · 0 fail · 0 pending on resources/questions.py`; before the fixture edit it reported 10 failures
- [x] the `## Asked` section the fixture writes lists exactly the four question titles the fixture's own PRDs carry: the titles under `^## Asked` in `.pearde/prds/the-board-runs-itself/transitions-are-commands/probe/fixture.py` diff empty against that same file's `^### Q<n>: ` titles, four of each
- [x] section B of this PRD's harness passes: with `## Asked` in place `claim next impl-1` exits 0 and never names the drill gate; with the round file truncated the same command exits 1 with `asking 4 — drill first`
- [x] `resources/board/transitions.py` and `resources/board/plan.py` are untouched by this spec — the gate was not weakened to make the fixture green

## Verify and Proof

```sh
bash .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh | tail -1
F=.pearde/prds/the-board-runs-itself/transitions-are-commands/probe/fixture.py
diff <(awk '/^## Asked$/{f=1;next} f&&/^- /{print substr($0,3)} f&&/^"""/{exit}' "$F" | sort) \
     <(grep -E '^### Q[0-9]+: ' "$F" | sed 's/^### Q[0-9]*: //' | sort) && echo "the four titles match"
bash .pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
```
