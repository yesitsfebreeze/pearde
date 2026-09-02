# Settings

Every board-wide knob. Per-PRD values — `priority`, `est`, `repo` — live in
each `prd.md`, not here.

The live copy is `.pearde/settings.md`. This file is its template. The skill
folder is shared across installs, so **never write values here** — they leak
into every board.

```yaml
---
language: English
workers: 0
pipeline: 0
weight-default: 50
gantt-day: 8h
happiness: 0
context-budget: 100k
---
```

A master board adds its identity and what it merges:

```yaml
---
name: master
members:
  - ../mitosys/prds
  - model: ../model/prds
---
```

| key           | default      | meaning                                                          |
|---------------|--------------|-------------------------------------------------------------------|
| `language`    | English      | the language every PRD, spec and report is written in. `pearde init` writes it by name and says so on its first line; `pearde settings language=<l>` changes it — `.pearde/memos/init-defaults-the-language.md` |
| `workers`     | 0            | implementer slots, loop step 5. `0` — the default — is **unlimited**: every dispatchable PRD is dispatched the moment its gates clear, and the plan's wall is the critical path. A number is a cap a person sets for a rate limit or a budget, never a guess about staffing; the view's header names the peak the fastest path asks for beside what the cap costs |
| `pipeline`    | 0            | analyst slots, loop step 4 — `specced` PRDs kept ahead. `0` — the default — is unlimited: every `open` PRD the drill gate does not hold is specced at once. A number is a cap, same as `workers` |
| `weight-default` | 50        | weight of an unscored PRD while no PRD on the board has `complexity` |
| `gantt-day`   | 8h           | weight one calendar day represents in the view's `dates` mode. The timeline is decoration; nothing schedules on it |
| `memos`       | `memos/`     | where decision records live, relative to `.pearde/`. Point it at another system's memo dir to mirror it read-only — the strict gate then applies only to the board's own `memos/`, per @references/memo.md |
| `workflows`   | `workflows/` | where the workflow library lives, relative to `.pearde/`. Unlike `memos:`, elsewhere is not a foreign system mirrored read-only — it is **the** library, shared by several boards and written by all of them, so it gets the whole check wherever it sits. @references/workflow.md |
| `grammar`     | `grammar.md` | where the board's vocabulary lives, relative to `.pearde/`. Like `workflows:` and unlike `memos:`, elsewhere is not another system mirrored read-only — it is **the** file, and several boards over one codebase share one vocabulary, so it gets the whole check wherever it sits. @references/grammar.md |
| `health-floor` | 40          | the health score under which a file is **unhealthy** — the one `pearde brief` names in the implementer's block, and `health list` prints by default. 1-100. @references/health.md |
| `health-weights` | `lines=25 branching=30 longest=20 fan_out=5 fan_in=10 links=10` | how much each health axis pulls. Space-separated `axis=weight`, any subset; a missing axis keeps its default, an unknown axis or an unreadable weight is one problem line from `health score` and `health check` and the default stands. The thresholds are constants in @resources/health.py, on purpose |
| `harnesses`   | `off`        | run the board's own `verify.sh` harnesses as part of `doctor` — `on` runs them on every `doctor` run, and `doctor --harnesses` runs them whatever this key says. Off by default because the row costs tens of seconds where every other row answers in one. Read by `doctor` alone; no other reader on the board looks at it. @references/parts/doctor.md |
| `happiness`  | 0            | whether a person has said this machine is tooled for this repo. `0` — the value `pearde init` writes — opens the ramp gate at loop step 0: it prints the gap between what the tree asks for and what is installed, proposes skills off scout's routes and hands the picks to the user, every pass until the answer is yes. Non-zero closes it, and only a person writes one — `pearde ramp happy 1`. @references/parts/ramp.md |
| `members`     | none         | the boards this one merges — `- <path>` or `- <name>: <path>`, relative to `.pearde/`. Present means **master board**: every member's PRDs join the scan as `@<member>/<rel>`, one plan spans them. @references/parts/master.md |
| `gate`        | none         | one command, run in the repo root by `collect` after the specs' verify blocks and before the commit. Red is exit 1 and no commit, like a red verify — measured against the output `claim:` recorded under `.pearde/.claims/<prd>/gate`: a line already there is known, a new line is red. With no record, red is any non-zero exit. @references/parts/commits.md |
| `context-budget` | 100k      | how far one window may grow **over its own floor**, in tokens — `off` removes it, `160k` moves it. A window opens holding the system prompt, the tools, `CLAUDE.md` and the skill before a pass exists — 50k on this repo's own `/pearde` session — so the budget is measured from the smallest window the session was billed for, never from zero. Context is billed on every turn, so what a window grew is paid for again on every turn left. `resources/guard.py` is the only reader: it notes the crossing at 70% and 85%, and at the ceiling refuses everything but the pass file, @references/parts/dispatch.md, @references/parts/loop.md, @references/parts/pass.md, dispatching a worker, asking the user and the board's own commands — the ceiling is a handover, not a stop. @references/parts/dispatch.md |
| `transitions-per-pass` | 8   | how many **returns** one `pearde-pass` worker collects before it hands back `MORE` and a fresh window carries on. A claim spends nothing against it — dispatching is one line in the pass's window — and a pass never stops dispatching while a PRD is ready: the count is spent on what comes back, and `MORE` goes out only when it is spent and nothing is in flight. Read by the pass worker itself, off this file — the board is on disk and `.pearde/.state/pass.md` is what crosses, so ending a pass costs one scan. Lower it on a board whose PRDs are large, raise it where they are one-line collects. @references/agents/pearde-pass.md |
| `claim-ttl`   | `30m`        | how long a held PRD's files may stand still before its claim is **silent** — the newest mtime over the PRD directory and its footprint union in `repo`, the same union `collect` commits. `30m`, `2h`, `1d`; a bare number is minutes. `plan.py`'s `silent_of` is the one reader; `scan`, the page and `sweep` print and act on its word. @references/parts/view.md |
| `footprint-above` | 40       | a footprint entry that is a directory holding more tracked files than this is **wide**: `pearde specced` prints `wide footprint — <path> holds N tracked files` and still accepts the set. A warning, never a refusal — a rename across a tree is legitimately wide, and it is also the PRD every other one on the board waits behind, which is what the line says. @references/parts/workers.md |
| `split-above` | 40           | a spec set whose `complexity` sums above this is REFINE, not SPECCED. The analyst brief carries the number as `<split_above>`, and `pearde specced` refuses the set — `over split-above: 58 > 40 — REFINE it` — so a verdict that ignored the brief cannot land. A limit, never a floor: a REFINE under it is still allowed. A master board reads each member's own |
| `specs-above` | 6            | a spec set with more files than this is REFINE, not SPECCED — the same two readers, `<specs_above>` in the brief and `over specs-above: 7 > 6 — REFINE it` from `specced`. A child over either limit is REFINEd in its turn; depth is unbounded |
| `name`        | inferred     | what the board calls itself — the view's title and `/board/<name>` URL. Inferred from the directory on a plain board, from the member names on a master — a placeholder: the first pass meeting an unnamed master asks the user and writes it |
| `machine-ceiling` | 12        | the highest concurrency `pearde machine` will name across every watched board. Not a limit that was found — the highest that was **measured** to cost nothing on this machine (12 at once, +4% mean latency, no knee), so it is a number to move rather than a law. `0` — like `workers` and `pipeline` — is **unlimited**: the load-derived count with the floor of 1 under it and nothing above it, printed `ceiling ∞`, never a bare `0`. `1`-`64` is that number. Absent, unparseable or out of that band leaves 12 standing, so an untouched board keeps the measured composite and only an explicit `0` lifts the cap. The floor is always 1 and load only ever lowers the count. Read by @resources/board/machine.py alone, off the board at the cwd — the command spans every board and writes to none, so the board a person is standing in is the one they addressed, and away from any board the default stands. @references/parts/machine.md |

A key missing from the live copy reads at its default.

**The persona is not here, and there is no key for it.** Who is working is
session state — it starts as `engineer`, is switched by saying so, and ends
with the session. @references/parts/personas.md says why a persisted one is
worse than none. A `persona:` key someone adds by hand is an unknown key like
any other: preserved, and read by nothing.

## Read

Read `.pearde/settings.md` in loop step 1, once per session, and after writing
it.

## Write

The orchestrator is the only writer, same as PRD state.

| case                       | do                                                                    |
|----------------------------|------------------------------------------------------------------------|
| no `.pearde/settings.md`      | first run — `pearde init`, see below                                   |
| `members:` and no `name:`  | ask the user what the group is called, write `name:`, then run the pass |
| a board joins or leaves    | append or remove its `members:` entry. Nothing in the member changes   |
| `workers=N` / `pipeline=N` | `pearde settings workers=N`, then run with it                          |
| any other setting stated   | `pearde settings <key>=<value>` — one key written, one line printed    |

First run: `pearde init` — @resources/board/init.py writes `.pearde/settings.md`
with every knob above by name, `language: English` unless `--language <l>`,
and says so on its first line. It asks nothing: the language is a default
that is printed, not a guess, per `.pearde/memos/init-defaults-the-language.md`.

Ask `name` the first time `members:` is read with no `name:`, in the same
pass — a group of projects is named for what it owns, not a join of directory
names.

Unknown keys in the live copy are the user's: preserve them, same as PRD
frontmatter.
