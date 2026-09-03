# Settings

Every board-wide knob. Per-PRD values — `priority`, `est`, `repo` — live
in each `prd.md`.

Live copy: `.pearde/settings.md`; this file is its template. The skill
folder is shared across installs, so **never write values here** — a value
leaks into every board.

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

A master board adds its identity and members:

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
| `language`    | English      | the language every PRD, spec and report is written in. `pearde init` writes it by name on its first line; `pearde settings language=<l>` changes it — `.pearde/memos/init-defaults-the-language.md` |
| `workers`     | 0            | implementer slots, loop step 5. `0`, the default, is **unlimited** — every dispatchable PRD goes out as its gates clear, and the critical path is the plan's wall. A number caps for a rate limit or a budget, never a guess at staffing; the view's header names the peak the fastest path wants beside the cap's cost |
| `pipeline`    | 0            | analyst slots, loop step 4 — `specced` PRDs kept ahead. `0`, the default, is unlimited: every `open` PRD the drill gate does not hold is specced at once. A number is a cap, as with `workers` |
| `weight-default` | 50        | weight of an unscored PRD while no PRD on the board has `complexity` |
| `gantt-day`   | 8h           | weight one calendar day represents in the view's `dates` mode. The timeline is decoration; nothing schedules on it |
| `memos`       | `memos/`     | where decision records live, relative to `.pearde/`. Elsewhere mirrors another system's memos read-only — the strict gate then covers the board's own `memos/` alone. @references/memo.md |
| `workflows`   | `workflows/` | where the workflow library lives, relative to `.pearde/`. Unlike `memos:`, elsewhere is no read-only mirror — **the** library, shared and written by several boards, so the whole check applies wherever it sits. @references/workflow.md |
| `grammar`     | `grammar.md` | where the board's vocabulary lives, relative to `.pearde/`. Like `workflows:`, no read-only mirror — **the** file, one vocabulary shared by every board over one codebase, checked whole wherever it sits. @references/grammar.md |
| `health-floor` | 40          | the health score under which a file is **unhealthy** — the one `pearde brief` names in the implementer's block, and `health list` prints by default. 1-100. @references/health.md |
| `health-weights` | `lines=25 branching=30 longest=20 fan_out=5 fan_in=10 links=10` | how much each health axis pulls. Space-separated `axis=weight`, any subset; a missing axis keeps its default, an unknown axis or unreadable weight is one problem line from `health score` and `health check`, the default standing. Thresholds are constants in @resources/health.py, on purpose |
| `harnesses`   | `off`        | run the board's own `verify.sh` harnesses under `doctor` — `on` on every run, `doctor --harnesses` whatever the key says. Off by default: the row costs tens of seconds where every other answers in one. `doctor` is its only reader. @references/parts/doctor.md |
| `happiness`  | 0            | whether a person has said this machine is tooled for this repo. `0`, what `pearde init` writes, holds the ramp gate open at loop step 0: every pass prints the gap between what the tree asks for and what is installed, proposes skills off scout's routes and hands the picks to the user. Non-zero closes the gate, and only a person writes one — `pearde ramp happy 1`. @references/parts/ramp.md |
| `groups`      | none         | the labels this board carries — `groups: work infra`, or the list form. A label, never a partition: several per board, most boards none. `pearde plan <group>` is the machine frontier over the boards declaring one; `pearde run <group>` runs that group alone. Read by @resources/board/run.py, written by a person and `pearde settings groups=<labels>` alone. The reserved scopes (`here`, `all`) and the windows (`boards`, `slots`, `progress`, `groups`) are refused as labels and named by `plan groups`. No file lists which board is in which group — the board declares itself, the rule that makes the watch set the whole configuration. @references/parts/run.md |
| `members`     | none         | the boards this one merges — `- <path>` or `- <name>: <path>`, relative to `.pearde/`. Present means **master board**: every member's PRDs join the scan as `@<member>/<rel>`, one plan spans them. @references/parts/master.md |
| `gate`        | none         | one command, run in the repo root by `collect` between the specs' verify blocks and the commit. Red is exit 1 and no commit, like a red verify — measured against the output `claim:` under `.pearde/.claims/<prd>/gate`: a line already there is known, a new line red. Without a record, red is any non-zero exit. @references/parts/commits.md |
| `context-budget` | 100k      | how far one window may grow **over its own floor**, in tokens — `off` removes it, `160k` moves it. A window opens holding the system prompt, the tools, `CLAUDE.md` and the skill before a pass exists — 50k on this repo's own `/pearde` session — so the floor is the smallest window the session was billed for, never zero; every turn left pays again for what the window grew. `resources/guard.py`, the only reader, notes the crossings at 70% and 85%; at the ceiling it refuses everything but the pass file, @references/parts/dispatch.md, @references/parts/loop.md, @references/parts/pass.md, dispatching a worker, asking the user and the board's own commands — a handover, not a stop. @references/parts/dispatch.md |
| `transitions-per-pass` | 8   | how many **returns** one `pearde-pass` worker collects before handing back `MORE` for a fresh window to carry on. A claim spends nothing — dispatching is one line in the pass's window — and a pass never stops dispatching while a PRD is ready: the count is spent on returns alone, `MORE` going out once spent, with nothing in flight. Read by the pass worker itself, off this file — the board is on disk and `.pearde/.state/pass.md` is what crosses, so ending a pass costs one scan. Lower it where PRDs are large, raise it where they are one-line collects. @references/agents/pearde-pass.md |
| `claim-ttl`   | `30m`        | how long a held PRD's files may stand still before its claim is **silent** — newest mtime over the PRD directory and its footprint union in `repo`, the union `collect` commits. `30m`, `2h`, `1d`; a bare number is minutes. `silence.py`'s `silent_of` is the one reader; `scan`, the page and `sweep` print and act on its word. @references/parts/view.md |
| `footprint-above` | 40       | a footprint directory holding more tracked files than this is **wide**: `pearde specced` prints `wide footprint — <path> holds N tracked files` and still accepts the set. A warning, never a refusal — a rename across a tree is legitimately wide, and is the PRD every other one waits behind. @references/parts/workers.md |
| `split-above` | 40           | a spec set whose `complexity` sums above this is REFINE, not SPECCED. The brief carries it as `<split_above>`, and `pearde specced` refuses the set — `over split-above: 58 > 40 — REFINE it`. A limit, never a floor: a REFINE under it is allowed. A master board reads each member's own |
| `specs-above` | 6            | a spec set with more files than this is REFINE, not SPECCED — the same two readers, `<specs_above>` in the brief and `over specs-above: 7 > 6 — REFINE it` from `specced`. A child over either limit is REFINEd in its turn; depth is unbounded |
| `name`        | inferred     | what the board calls itself — the view's title and `/board/<name>` URL. Inferred from the directory on a plain board, from the member names on a master — a placeholder the first pass meeting an unnamed master replaces, asking the user |
| `machine-ceiling` | 12        | the highest concurrency `pearde plan` names across every watched board. **Measured**, not found — 12 at once cost +4% mean latency, no knee — so a number to move, not a law. `0`, like `workers` and `pipeline`, is **unlimited**: the load-derived count, floor 1, nothing above, printed `ceiling ∞`, never a bare `0`. `1`-`64` is that number. Absent, unparseable or out of that band leaves the measured 12 standing, so only an explicit `0` lifts the cap. Load only ever lowers the count. Read by @resources/board/run.py alone, off the board at the cwd — the command spans every board and writes to none, and away from any board the default stands. @references/parts/run.md |

A key missing from the live copy reads at its default.

**No persona key.** Who is working is session state — `engineer` at the
start, switched by saying so, gone with the session;
@references/parts/personas.md says why a persisted one is worse than none.
A hand-added `persona:` is an unknown key: preserved, read by nothing.

## Read

Read `.pearde/settings.md` in loop step 1, once per session, and after writing
it.

## Write

The orchestrator is the only writer, same as PRD state.

| case                       | do                                                                    |
|----------------------------|------------------------------------------------------------------------|
| no `.pearde/settings.md`      | first run — `pearde init`, below                                       |
| `members:` and no `name:`  | in the same pass, ask the user what the group is called, write `name:`, then run — a group of projects is named for what it owns, not a join of directory names |
| a board joins or leaves    | append or remove its `members:` entry. Nothing in the member changes   |
| `workers=N` / `pipeline=N` | `pearde settings workers=N`, then run with it                          |
| any other setting stated   | `pearde settings <key>=<value>` — one key written, one line printed    |

First run: `pearde init` — @resources/board/init.py writes
`.pearde/settings.md` with every knob above by name and `language: English`
unless `--language <l>`, saying so on its first line. Nothing is asked: the
language is a printed default, never a guess, per
`.pearde/memos/init-defaults-the-language.md`.

Unknown keys in the live copy are the user's: preserve them, same as PRD
frontmatter.
