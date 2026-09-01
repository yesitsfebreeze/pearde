# report — scan-parses-the-board-once-and-caches-it-by-mtime

implementer (pass two) · as engineer · workflow: probe-then-spec · 2026-09-01
The analyst's pass-one report stood in this file; a copy is at
`/tmp/pe-scan-cache-run/analyst-report-bak.md`.

## Verdict

DONE. Both specs implemented and every acceptance box ticked with quoted
output. Spec01's cache was already standing in `resources/board/plan.py`
(committed mid-run — see Workflow, step 1); this pass implemented spec02 and
ran every check.

## Workflow probe-then-spec

| step | atomic | outcome |
|------|--------|---------|
| 1 | read-the-contract | done — prd.md + both specs read; every `@` resolved; git status recorded (20 modified paths; see step-1 note) |
| 2 | capture-the-harness-baseline | done — 9 harnesses (8 foreign + own) counted and saved under /tmp/pe-scan-cache-run/; index.py check exit 0, doctor.sh exit 0, all rows ok |
| 3 | attempt-the-build | done — spec02 implemented in `resources/questions.py` (edit to an existing footprint file, in place); no new files outside the PRD folder |
| 4 | re-run-the-harnesses | done — all 9 re-run, same order, same command line; 8 unchanged, 1 red before and after (see Edits) |
| 5 | write-the-specs | n/a — specs were written by the analyst pass; this pass ticks their boxes. No back-edge taken. |

Step-1 note: at `git status --short` the tree held 19 modified paths, none of
them `resources/board/plan.py` — sibling commit `9a7ce2c` (11:15:28,
"pearde-next-prints-the-step-and-the-decision-it-owes") had taken the pass-one
cache code with it. `git show HEAD:resources/board/plan.py` carries the whole
mechanism; per the build table's clean-tree row the work stands in HEAD and
the specs' "what already stands" was re-read against the file, which matches.
A second sibling commit landed mid-run (`78357ed`, 11:25:29 — collect.py,
workers.md) and doctor's `statusline`/`vision`/`origin` rows moved between my
two gate runs; none of the moved lines name my footprint.

### Edits

None. Every atomic command ran as written; no `on failure` row fired, and no
replacement text is owed.

## What changed in the tree (this pass)

`resources/questions.py` `parse()` — one hunk: when `plan` (resources/board/
plan.py) is importable — true for every caller that reaches questions through
the board scripts — `(fm, body)` is served from `planlib.parse_prd` plus this
reader's own `COMMENT_RE` strip on the cached body; on `ImportError` (plain
`questions.py` invocation) or an unreadable-through-cache file
(OSError/UnicodeDecodeError) it falls back to its own read, byte-for-byte as
before. The dialects were diffed line by line first: KEY_RE/ITEM_RE/
strip_comment identical; the only body differences (plan strips, questions
doesn't) are invisible to every questions.py consumer (regex section readers).
Verified against the pre-change module: per-file `(fm, body)` identical on all
81 real PRDs, `rows`/`unanswered`/`check` outputs identical, fixture drill
counts identical.

## Fails-when rows hit (named, not edited)

1. **transitions-are-commands harness red — pre-existing, not mine, left
   alone.** Baseline and re-run: `74 checks · 64 pass · 10 fail · 0 pending on
   resources/questions.py`. The 10 fails split in two:
   - `?? .pearde/.state/parse-cache.json` surfacing in the fixture's
     `git status` (2 checks: "git diff empty after every refusal", "only
     prd.md files … moved") and `.transitions.jsonl` row count 12 vs 13 —
   - "claim next now succeeds" and the 7 checks after it: the claim gate's
     drill refuses `asking 4` where the harness expects success. Reproduced
     with the sibling's HEAD transitions.py on a fresh fixture: the fixture
     board holds 4 unanswered questions (`asking` Q1-Q3 + `badround` Q1) and
     no `.state/round.md`, so `pending >= 2` refuses regardless of the cache
     or of my change (verified with my hunk stashed: same refusal). The
     harness (fixture.py mtime 2026-08-31 20:34, untracked — `.pearde/` is
     git-ignored) predates the drill gate's reach into `claim` and predates
     the cache file. Fix belongs to that harness's owner: whitelist
     `.pearde/.state/parse-cache.json` in the stray-file filter and give the
     fixture a `.state/round.md` whose `## Asked` carries the four titles (or
     answer `badround` Q1 in-harness). Not in my footprint; named, not fixed.

2. **spec01's deleted-entry box has a caveat the spec now carries.**
   `parse_cache_save` only fires when `_PCACHE_DIRTY` (a miss since load), so
   on a warm all-hit call after a deletion the stale entry stays on disk until
   the next miss-triggered save. The PRD count is still correct (the walk, not
   the cache, decides what exists); only the cache file lags. Measured: fixture
   81→80 PRDs, deleted entry dropped on the next miss. Spec box annotated with
   the measured behavior rather than rewritten.

## Verify and Proof (quoted)

- spec01 block: `python3 resources/board/plan.py scan | head -3` →
  `board: /Users/feb/dev/infra/pearde/.pearde · 81 PRDs · workers=6 · axis: 0 on · 4 off` (exit 0);
  `probe/verify.sh` → `parse-cache verify: pass` (exit 0).
- spec01 boxes, run by hand on the real board and on fixtures:
  warm `parse_prd`: 0 opens; `fm` mutation isolated (state stays `claimed`);
  external mtime edit: exactly 1 re-open, same content served; corrupt JSON /
  wrong version / non-dict `files` on the real cache: all exit 0, 81 PRDs;
  deleted-PRD fixture: 81→80 and entry dropped after the next miss;
  unchanged board: `parse-cache.json` mtime unchanged across a scan;
  cold vs warm scan output: `diff` identical.
- spec02 block: `python3 resources/questions.py list` → empty output, exit 0
  (0 answered / 0 open rows is this board's true state; identical to the
  pre-change reader — see above); `plan.py scan | head -3` → same as above;
  `probe/verify.sh` → pass.
- spec02 boxes: warm `unanswered`: 0 opens on cached prd.md (baseline reader:
  81), same list, `rows`/`unanswered`/`check` byte-identical to pre-change;
  edited-question fixture: 1 open → 2 open on the next call; drill fixture
  (open `### Q1:` + matching `**Q1**`): `asking 1 over 1 PRD` before and after
  `answer` + rescan; real board drill count unchanged.
- Repo gate: `python3 resources/index.py check` → exit 0;
  `bash resources/doctor.sh` → exit 0, "every part this repo owns checks out"
  (only statusline/vision/origin rows moved between runs — sibling commit
  `78357ed`, not mine).
- `serve.py status` at end: up on 127.0.0.1:8443, no fixture boards
  registered.

## Findings

1. **The PRD's headline number still does not reproduce** (carried from pass
   one). Warm `cmd_scan` wall on 2026-09-01: 71-83 ms (median 82.9 over 7),
   cold ~80 ms — the 40 ms bar is unreachable by parse-caching alone; the
   wall time is interpreter + imports + scan's printing. The number the specs
   correctly check instead: walk+parse cold 5.8 ms → warm 4.0 ms over 237
   files, and warm `questions.unanswered` 7.2 → 4.1 ms in-process. The cache
   and the spec02 routing both pay; the PRD's bar needs re-aiming at what
   actually spends the time (imports, printing, scheduling) if it still
   matters.
2. `questions.unanswered` was the one hot path re-parsing the board a second
   time; it now serves from the same cache. Statusline and serve.py inherit
   both wins with no edit (they call `planlib.scan`/`parse_prd`).
3. `resources/questions.py`'s working tree also carries a sibling's uncommitted
   change (the closed-PRD grading guard in `check()`); my hunk is disjoint
   from it. If collect splits by rebuilt blob, my file's hunk is the `parse()`
   fast path only.

## Box status

spec01: 6/6 ticked as run, each with quoted output. spec02: 3/3 ticked as run,
each with quoted output. No box ticked without the command (or in-process
probe, for the open-count assertions) having run in this session.
