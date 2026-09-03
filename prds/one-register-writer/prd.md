---
state: done
origin: requested
priority: 55
complexity: 16
blast-radius: mid
workflow: probe-then-spec
---

# One register writer

*Source: `docs/content/docs/improvements/obsidian-register-writer.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** obsidian · **Axis:** complexity (4 → 6) · **Pulls the score up by
~5 points**

## Why now

Writing one register entry safely composes four rules: the quit-wait-refuse
protocol (an entry written under a running app dies on exit), the
passwd-based home resolution (doctor runs in shells exporting no `HOME`),
the precedence inside the home (macOS `Library/Application Support`, then
`XDG_CONFIG_HOME`, then `~/.config`), and the compat-symlink history (a
link's name is not the board's name). Each lives in a different place — the
vault verb, the doctor row, the resolver — and each is a rule you reread the
source to re-derive. The reference page spells all four out because no
function does.

## The change

One module owns the register: `open`, `read`, `has`, `write` (refusing while
the app runs), `repair` — with the home resolution and the precedence inside
it. The vault verb and the doctor row both call it; neither parses
`obsidian.json` itself. The four rules get one docstring, and the module's
self-check runs the readback in a scratch home so the rules are testable
without the app.

## Done when

- `grep -rl "obsidian.json" resources/` names the one module (and no other
  file parses the register).
- The doctor `vault` row's readback goes through the module's `read` — the
  passwd resolution lives in one place, provable by `env -i` run.
- The self-check seeds a scratch register, writes an entry with the app
  "running" (refused) and not (written), and passes in a clean checkout.

## Fails when

- The module grows the fetch logic too: `pearde vault` also fetches plugin
  bundles, which is network, not register. Keep the fetch in the verb; the
  module only ever touches the register file.

## What stays out

No behavior change of any kind — this is a move, and a move that changes a
printout is a bug. The score page's complexity axis is what moves.

## Blocked

**2026-09-03 20:42 — the lane will not rebase**

`lane/one-register-writer` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/board/init.py`

Nothing is lost: the worker's commits are on `lane/one-register-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-register-writer`.

**2026-09-03 21:00 — the lane will not rebase**

`lane/one-register-writer` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/board/init.py`

Nothing is lost: the worker's commits are on `lane/one-register-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-register-writer`.

**2026-09-03 21:00 — the lane will not rebase**

`lane/one-register-writer` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/board/init.py`

Nothing is lost: the worker's commits are on `lane/one-register-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-register-writer`.

**2026-09-03 21:23 — the lane will not rebase**

`lane/one-register-writer` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/board/init.py`

Nothing is lost: the worker's commits are on `lane/one-register-writer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-register-writer`.
