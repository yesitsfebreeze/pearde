---
complexity: 18
footprint:
  - resources/board/serve.py
---

# spec01 — `ensure` writes `.state/view.json`, `reap` trusts a file-backed pid

The board's own directory learns the daemon: `serve.py ensure` writes
`<board>/.state/view.json` — pid, port, `started_at` and the board's name —
straight from `/status`, the daemon's own word about itself, never the pid
this process may or may not have spawned. `serve.py reap` (and its
`--dry-run`) reads it back: a pid some live board's `view.json` names is
kept outright, skipping the age-based grace window and the port/`/status`
guesswork below it. A pid no file names — the pre-rule case, or a daemon
whose file went stale because the pid it names died — falls through to
today's sweep unchanged.

**Already standing** — the whole change is in the lane, uncommitted:

- `write_view`/`read_view`/`view_path` in `resources/board/serve.py`, and
  `common.atomic_write` — the tmp-then-`os.replace` every other state write
  in this tree already takes — is what makes the write itself.
- `cmd_ensure` calls `write_view` with the pid and port `running()` (i.e.
  `/status`) reports, after the `/register` call returns, board name
  included.
- `/status`'s payload carries a new `started_at` — when this process became
  the daemon, computed once at import and unrelated to `BOOT` (the source
  stamp used for hot-reload) — so the file and the live daemon never
  disagree about it.
- `file_named(pid)` asks the pid's own `/status` for the boards it watches
  and reads each live one's `view.json`; `stranded(pid)` calls it before the
  age check and returns "kept" immediately on a hit, with `why` naming the
  board and file.
- Probe at
  `.pearde/prds/the-daemon-s-liveness-moves-onto-the-board/probe/probe.sh`
  exercises both arms end to end, on an isolated port and a `mktemp -d`
  board — never the real machine daemon.

- One guard in `write_view`, added by the implementer pass: an existing file
  already saying these exact bytes is left alone, so the loser of the race the
  PRD's `## Fails when` describes reads the winner's file rather than
  overwriting it. There is no `flock` anywhere under `resources/`; the lock
  that clause names is `common.atomic_write`'s `os.replace`, and this guard is
  what the clause buys on top of it.

**Left to finish** — nothing. Every box below was run in the lane and is
ticked against its own output; the pre-edit baseline the checks compare
against is a `git clone` of the lane at `HEAD`, and both sweeps' numbers are
in `report.md` under `## Harness baseline`.

## Acceptance

- [x] `python3 -c "import ast; ast.parse(open('resources/board/serve.py').read())"` exits 0.
- [x] `bash .pearde/prds/the-daemon-s-liveness-moves-onto-the-board/probe/probe.sh` prints a `view.json` naming the live daemon's own pid and port (matched against `serve.py status`'s own line), then a `reap --dry-run --pid <that pid>` line reading `keeping … file-backed, no grace needed` — with `PEARDE_REAP_GRACE_S` set low enough that the grace window has already closed, so the "kept" verdict is provably the file, not the grace.
- [x] The same probe's second scenario — the board directory deleted before `reap` runs, so no `view.json` survives it — still gets `would stop … watching no board`: the pre-rule sweep is unchanged for a pid no file names.
- [x] `python3 resources/board/serve.py reap --dry-run` against the real machine daemon(s) prints no new error and changes no existing "keeping …" line's reason for a board that predates this change and carries no `view.json` yet. Run twice over the same six live daemons — once from a `git archive HEAD` copy, once from the build — both `serve: 0 of 6 stranded`, both exit 0, every pid kept in both. The four daemons carrying no `view.json` keep their reason verbatim, the real machine daemon among them: `serve: keeping pid 3707 · port 8443 — watching 2 live board(s): pearde, forkprobe` and `serve: keeping pid 22786 · port 50615 — started 47s ago — inside the 60s grace a session start needs to register its board`. The two whose reason moved are the two that do carry one — `keeping pid 2871 … named by a's .state/view.json — file-backed, no grace needed` — which is the change, not a regression.
- [x] `doctor.sh --harnesses`'s own `reap` line — the plain, flag-less sweep it has always run — ends with the same shipped grace and the harness sweep's pass/fail counts unchanged from its own pre-edit baseline. The `reap` line: `git diff --stat -- resources/doctor.sh` is empty and `REAP_GRACE_S = float(os.environ.get("PEARDE_REAP_GRACE_S", "60"))` reads identically at `HEAD` and in the build, and neither sweep's row carries a `leaked service reaped` clause — so the flag-less sweep stopped nothing in either tree. The counts, run once per tree: `harnesses broken 3 of 98 green · 86 unpinned · 653s · 62 failed` before, `4 of 99 green · 87 unpinned · 872s · 60 failed` after. Compared by name rather than by total, as the totals moved for reasons outside this footprint: 64 failing harnesses before, 62 after, one name new (a PRD a neighbour landed mid-run) and three gone, every one of the three shown by a sequential re-run to be sweep contention or a clone artefact rather than this change — proof in `report.md` under `## Harness baseline`. No failing harness names this PRD in either run.
- [x] `python3 resources/index.py check` reports nothing new about `resources/board/serve.py`. Three lines, all pre-existing and none naming it: `resources/common.py is on disk with no row in references/files.md` · `references/files.md lists @resources/board/hotreload-test.js — not on disk` · `@@view names @resources/board/hotreload-test.js — not on disk`.

## Verify and Proof

Run from the repo root that holds the build — the lane while this is
uncommitted, the checkout after it merges. `PEARDE_ROOT` is what points the
probe at that tree rather than at whatever checkout the board sits in.

```sh
python3 -c "import ast; ast.parse(open('resources/board/serve.py').read())"
PEARDE_ROOT="$PWD" bash .pearde/prds/the-daemon-s-liveness-moves-onto-the-board/probe/probe.sh
python3 resources/board/serve.py reap --dry-run
grep -q 'REAP_GRACE_S = float(os.environ.get("PEARDE_REAP_GRACE_S", "60"))' resources/board/serve.py
if [ -n "$(git diff --stat -- resources/doctor.sh)" ]; then exit 1; fi
idx=$(python3 resources/index.py check 2>&1 || true)
printf '%s\n' "$idx"
if printf '%s\n' "$idx" | grep -q 'board/serve\.py'; then exit 1; fi
```

`doctor.sh --harnesses` is deliberately **not** in this block. It is a
board-wide gate: it runs every PRD's harness on the board, takes tens of
minutes, and its exit is decided by every other unit's reds — a unit whose
pass is conditional on the whole board can never pass. The two lines above
it are what this footprint actually owes that sweep: `doctor.sh` untouched
(so its flag-less `reap` line is the one it has always run) and the shipped
`REAP_GRACE_S` default still `60` (so that `reap` still carries the grace).
The sweep's own pass/fail counts are recorded in `report.md` under
`## Harness baseline`, before and after, and belong there rather than in a
block `collect` must run.
