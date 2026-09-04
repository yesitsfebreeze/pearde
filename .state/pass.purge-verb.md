# pass — lifecycle contract page + the purge verb

Written by the pass that landed the lifecycle-contract page and
`pearde purge`, on `main`, holding no session worktree of its own
(`pearde session list` shows one row, `s98669` — another live session, pid
98669; its tree and its dirty files are not this pass's, and neither are
the main checkout's other dirty files: `.gitignore`, `index.md` beyond the
two rows below, `references/*` beyond the edits below,
`resources/board/{all,dispatch,render}.py`, `view.js`, the untracked
`docs/` beyond the one file added — other sessions are live in them).

## What this pass did

1. **The page**: `docs/content/docs/improvements/lifecycle-contract.mdx` —
   the lifecycle contract (start / working / shutdown per participant:
   session tree, worker lane, daemon, probe fixture, reaped ref) with
   `pearde purge` as the reclaim; wired into `meta.json` and the
   improvements `index.mdx` inside the untracked `docs/`.
2. **The verb**: `resources/board/purge.py` — one command, read-only until
   `--apply`, candidates: stale lanes (PRD holds no claim), dead session
   trees (through `session.cmd_reap`'s own path, snapshot first),
   unregistered tmp boards (/tmp board with no serve.json, no
   live-or-unknown ledger row, past a day), `/tmp/pearde-*` probe fixtures
   past a day, reaped refs capped at `reap-cap` (default 8, a settings.md
   key). Refuse rule: a board the scan reads in-flight, every registered
   board, any ledger answering alive or unknown — never a candidate.
   Registered in `references/parts/handles.md`, `references/files.md`,
   `index.md` (`@@purge`); `doctor.sh` grew a read-only `purge` row that
   checks the refuse rule on every run; `references/parts/doctor.md` and
   `references/skills/pearde-doctor.md` (table row) updated.
3. **The PRD**: `.pearde/prds/the-lifecycle-contract-and-purge-reclaims-it/`
   — one PRD, `origin: requested`, boxes checked (the work landed in the
   same pass). Filed with `pearde add`, body rewritten after.
4. **`pearde purge` read-only was run**; `--apply` was withheld by
   judgement — see the first held fact.
5. Docs build: run (`cd docs && npm run build`) — clean, 53 pages, the
   lifecycle page prerendered at
   `docs/.next/server/app/docs/improvements/lifecycle-contract.html`.

## Held facts — do not re-derive

- **Why no `--apply` yet.** The read-only run listed 20 stale lanes +
  ~290 probe fixtures. The fixtures (~290 `/tmp/pearde-*` dirs, oldest 33
  days, from `the-view-row-names-a-variable-that-exists`'s
  `LNK="$(mktemp -d /tmp/pearde-viewrow-lnk.XXXXXX)"` and collect's
  mktemp prefixes) are safe and are the real run. But the same `--apply`
  pass removes lanes too, and 13 of the 20 lanes hold uncommitted worker
  dirt (`lanes.remove` destroys it — that is what dropping a lane means),
  and several had files written inside the last hour (graphify caches,
  scout snapshots — regenerable, but possibly a live probe's). The day
  gate covers fixtures only. The lazy safe order for the next pass:
  re-run `pearde purge` read-only, `git -C .pearde/.lanes/<slug> status`
  per lane, `pearde sweep --apply` the held-but-silent ones, then
  `--apply` what remains.
- `pearde session reap` was not run: the ledger holds one row, `s98669`,
  alive — nothing to reap; 0 reaped refs exist, the cap capped nothing.
- `pearde index check` exits 0. `pearde questions` names 3 pre-existing
  `## Answers`-with-no-`## Questions` rows — pre-existing, not touched.
  `pearde doctor`: vault/origin/memos/questions broken, all pre-existing
  with fixes printed; the new `purge` row reads `ok · N candidates ·
  every claim and registered board held`.
- The docs site (Next.js/fumadocs, `docs/package.json`, build `npm run
  build`) is another work stream's in-flight, untracked tree; this pass
  added one file and edited `meta.json` + `index.mdx` inside it and
  staged nothing there.
- `pearde help` lists `purge` (discovery via `COMMANDS =` in purge.py);
  `pearde purge --help` prints
  `takes: --board, --reap-cap, --json, --dry, --apply`.

## Findings owed a PRD or a memo

- **New**: a lane-age knob would make `purge --apply` safe without a
  human read — a lane is a candidate only when its `claim:` is gone AND
  its newest file is older than a day (the fixture gate, applied to
  lanes). 13 of the 20 lanes named on today's read hold dirt hours old.
  Small; one knob on the existing scan; not filed as its own PRD.
- Carried, unchanged, from the earlier passes: hunk-overlap false refusal
  in `collect.py`; `pearde add` writes `origin: requested` unconditionally
  and drops `--body`; `references/files.md` remains a merge-conflict
  hotspot; the 10 other stuck collect-band rows; `.state/pass.md` has no
  arbitration between pass workers beyond mtime/md5-check-before-write —
  met live this pass: another session rewrote this file mid-pass, so this
  pass wrote its own `pass.` variant instead of clobbering theirs.

## Follow-up (coordinator defect report) — fixed same pass

The coordinator named two /tmp probe-fixture SYMLINKS (dangling, 24d) that
failed removal with Errno 2 and read as candidates on every run, and asked
why the 342MB `/private/tmp/pearde-probe-*` dirs were not listed. Found
live and fixed in `resources/board/purge.py`:

- **Root cause of the Errno 2, and of the every-run candidate**: /tmp IS
  /private/tmp on macOS — the scan walked both roots and listed every
  entry under two spellings; the first spelling's rmtree removed the dir,
  the second's failed ENOENT, and the failed spelling then read as a
  candidate forever. Fixed: one walk, entries identified by
  `(st_dev, st_ino)`, so the two spellings collapse to one candidate.
- **Dangling symlinks** now enumerate: `os.path.exists` lies on links
  (`isdir` follows), so the read is `lstat` — a `pearde-*` symlink past a
  day is a candidate (`why: dangling symlink`) and removal is
  `os.remove` of the link, never its target. A scratch FILE past a day
  (the `pearde-idx.*` git-index files, `pearde-pass-*` stamps) removes
  with `os.remove` too — rmtree's ENOTDIR on them was the second half of
  the same never-a-candidate-gone shape.
- **ENOENT during removal** reads `removed · already gone` — a concurrent
  purge or the probe's own cleanup won the race; not a failure, the same
  spelling session reap keeps for a worktree already gone.
- The named repro links (`pearde-viewrow-lnk.mNhwUO`) were already gone by
  this pass's read — the shape they stood for is the double-spelling bug
  above, now closed.

Runs after the fix: `--dry` listed 6 (1 lane + 5 scratch files, 24-31d
old) → `--apply` removed all (second attempt after the ENOTDIR fix);
repeat `--dry` reads **`nothing to reclaim · 0 reaped ref(s)`**. Census
after: 157 `pearde-*` entries remain in /tmp — 0 dangling symlinks, all
dirs inside the 24h gate (oldest 23.5h; a harness sweep is running RIGHT
NOW — 28 dirs are under 6h old — so zero pearde-* trees is not reachable
today, and would break a live probe if forced).

**The 342MB `/tmp/pearde-probe-{cF5KTL,c78NOK,MEYRTu}` dirs**: the glob
did NOT miss them — the day gate did, correctly. Their newest file is
3.8-5.6h old (oldest content 21.3h — born at 11:47-12:18 today from
`…init-and-upgrade-write-the-dotted-board/probe/probe.sh`'s
`mktemp -d /tmp/pearde-probe-XXXXXX`), so under the refuse rule they stay
until ~18h from now: a probe mid-run has an EMPTY session ledger, so
ledger liveness proves nothing for a fixture — only the clock settles it.
They cross the gate tomorrow morning and the next `purge --apply` takes
them. Forcing them out today would delete possibly-live probe work — the
exact thing the rule exists to stop.

## Next pass should

1. Re-scan fresh before trusting anything above past this write's
   timestamp. Tomorrow ~10:00-12:00 the three `pearde-probe-*` dirs (342
   MB) cross the 24h gate — the next `pearde purge --apply` takes them and
   the 91 other viewrow dirs in the 18-24h bucket.
2. `pearde purge --apply` WAS run this pass (the fixture half was the
   ask's real run): 310 candidates removed — 302 probe fixtures (45 MB,
   oldest 33d) and 2 lane worktrees
   (`…one-primitive-one-definition-the-{core,lane-and-repo}…`, clean, 0
   dirt, branches kept; their unmerged own commits are the skeptic-held
   delegate-to-common work, branches intact). The other 18 originally
   stale lanes re-grew claims or held dirt and were kept by the fresh
   read. 155 `/tmp/pearde-*` dirs remain, all inside the 24h gate — the
   gate held them out correctly. Read-only run now lists nothing.
3. Docs build already ran clean this pass; re-run only if docs/ changes
   again.
4. Do not treat `pearde/.state/pass.md` as this pass's — read
   `pass.*.md` mtimes too; this file is the purge pass's record.