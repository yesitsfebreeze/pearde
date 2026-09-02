---
complexity: 6
footprint:
  - resources/guard.py
---

# spec01 — `guard on` writes the SessionStart hook

`pearde guard on` writes a fourth entry into the repo's
`.claude/settings.json`: a `SessionStart` hook running
`python3 @resources/board/serve.py ensure >/dev/null 2>&1 || true`. `off`
removes it with the other three. `guard status` notes it when it is absent.

**This stands already** — built and measured in this PRD's probe pass. It is
in the tree uncommitted at `@resources/guard.py`. Nothing is left to write;
this spec exists so the implementer can re-prove it after the tree moves.

What was built:

| where | change |
|---|---|
| `HOOKS` | rows became `(event, matcher, command, pattern)`. `hook_cmd()` is gone — a row carries its own command, because the fourth one is not a `guard.py` invocation. `is_guard(hook, pat)` takes the pattern from the row |
| `SERVE` | new module constant, `resources/board/serve.py` beside `SELF` |
| the fourth row | `("SessionStart", None, f"python3 {SERVE} ensure >/dev/null 2>&1 \|\| true", r"serve\.py\s+ensure\b")` |
| `entry_for(matcher, command)` | new — a row with `matcher` `None` writes no `matcher` key at all |
| `guard_on` / `guard_off` | unpack four fields; the printed line drops the empty matcher (`SessionStart → …`, not `SessionStart None → …`) |
| `guard_status` | after the `ok` row, a note when `serve.py ensure` is not in the file |
| the module docstring | `guard.py on` names both halves of what it writes |

Three details are load-bearing and are not to be simplified away.

- **No `matcher`.** A `SessionStart` matcher is the start *reason* —
  `startup`, `resume`, `clear`, `compact`, `fork`. Omitting the key fires the
  hook on every one of them. Measured, not assumed.
- **`>/dev/null 2>&1`.** `serve.py ensure` prints `serve: registered …` on
  success. The contract is that a session start prints nothing extra.
- **`|| true`.** `ensure` exits 2 outside a board, and the hooks contract
  reserves exit 2 for refusing the session. Measured on Claude Code 2.1.258
  headless, exit 2 did *not* block — see `[[260902-b598]]` — but a wiring
  that depends on which reading is true breaks on an upgrade.

## Acceptance

- [x] `guard on` on a fresh repo prints five `+` lines: the env cap and four hooks, one of them `SessionStart → python3 <abs>/resources/board/serve.py ensure >/dev/null 2>&1 || true`
- [x] The written `SessionStart` entry has exactly one hook, `"type": "command"`, and **no** `matcher` key
- [x] A second `guard on` prints `already wired, nothing changed` and writes nothing
- [x] `guard off` prints four `-` lines and leaves `"hooks": {}` and `env.MAX_THINKING_TOKENS` behind
- [x] A settings file already holding a foreign `SessionStart` entry keeps it, first, with ours appended; `off` leaves the foreign one alone
- [x] `guard status` on a repo wired by `guard on` prints no note; with the `SessionStart` entry deleted by hand it prints `no SessionStart hook — the view is not brought up on a session start; pearde guard on writes it` and still exits 0
- [x] Sections A, B, C, D of this PRD's probe harness are green

## Verify and Proof

```sh
bash .pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh
bash .pearde/prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh
python3 resources/guard.py status /Users/feb/dev/infra/pearde
```
