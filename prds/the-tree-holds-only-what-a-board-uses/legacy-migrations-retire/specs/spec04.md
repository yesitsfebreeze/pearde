---
complexity: 15
footprint:
  - resources/common.py
  - resources/guard.py
  - resources/grammar.py
  - resources/health.py
  - resources/knowledge.py
  - resources/questions.py
  - resources/board/boards.py
  - resources/board/registry.py
  - resources/board/run.py
  - .pearde/prds/a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re/probe/verify.sh
---

# spec04 — one spelling resolves a board, and a board is found by what it carries

Three modules carry their own `LEGACY_BOARD_DIR` / `BOARD_DIRS` pair —
`resources/board/boards.py`, `resources/common.py` and `resources/guard.py` —
and guard's is **inverted**: its `BOARD_DIR` is `"pearde"` and its
`LEGACY_BOARD_DIR` is `".pearde"`, the reverse of the other two. The pair is
the 2026-09-02 compatibility branch. Pass one proved it can go: every one of
the nine boards on this machine resolves to the identical path with the legacy
name removed from `BOARD_DIRS`, because each of the seven undotted ones carries
a `.pearde` symlink beside its real directory and `board_link` already reads
through it.

What cannot simply follow the name is the second job the same constant does.
`BOARD_DIRS` is also the "never scan a board" set in `health.SKIP_DIRS`,
`health.picked_files`, `grammar.unused` and `registry`'s nested-board test, and
a board's directory name is configurable anyway — `/Users/feb/dev/infra`'s
board is called `board`. Those sites stop comparing names and ask
`common.is_board_dir` / `board_named` / `named_boards` instead, which is
correct for every board name including the two this spec drops.

**Nothing of this is built.** Pass one ran the resolution probe only
(`probe/resolves-without-the-legacy-name.py`).

## Acceptance

- [x] `LEGACY_BOARD_DIR` and `BOARD_DIRS` are defined in no module under `resources/`, and named in none. — `grep -rn 'LEGACY_BOARD_DIR\|BOARD_DIRS' resources/` → no match.
- [x] `resources/guard.py`'s `BOARD_DIR` is `".pearde"` — the same value the other two modules hold, not its inverse. — `grep -n '^BOARD_DIR = '` over guard/common/boards prints `.pearde` three times.
- [x] `plan.board_named`, `plan.find_board`, `common.find_board`, `guard.board_named`, `run.py`'s walk-up, `knowledge.py` and `questions.py` each resolve a board through `BOARD_DIR` alone. — every loop over `BOARD_DIRS` is gone from those files; `run.py`'s walk-up takes `planlib.BOARD_DIR` alone.
- [x] Every one of the nine boards on this machine resolves to the same path before and after, the seven undotted ones through their `.pearde` symlink. — `probe/resolves-without-the-legacy-name.py`: ten boards, `0 board(s) resolve differently without the legacy name`, rc=0.
- [x] `health` and `grammar` still skip a board directory under any name, including `pearde` and `board`, by asking whether it carries a board rather than what it is called. — fixture: `health.tracked_files` over a tree holding `board/` (settings.md + prds/) and `pearde/` (prds/) returns nothing; `grammar._walk` over a project holding a `pearde/` board lists only `docs/readme.md`.
- [x] `registry`'s nested-board test answers yes for a directory carrying `settings.md` or `prds/` under any name. — `registry.is_board_dir(<fixture>/pearde)` → True; the test is now `is_board_dir(path) or isdir(path/.git)`.
- [x] `pearde doctor`, `pearde scan` and `pearde plan` print the same board and the same PRD count as before the change. — doctor names the same board and rows (no Traceback / no-board lines; `plan ok`, `knowledge ok`); `scan`: board `/Users/feb/dev/infra/pearde/.pearde · 229 PRDs`, same as baseline.

## Verify and Proof

```sh
cd "$REPO"
if grep -rn --exclude-dir=__pycache__ 'LEGACY_BOARD_DIR\|BOARD_DIRS' --include='*.py' --include='*.sh' resources/; then exit 1; fi
grep -n '^BOARD_DIR = ' resources/guard.py resources/common.py resources/board/boards.py
python3 .pearde/prds/the-tree-holds-only-what-a-board-uses/legacy-migrations-retire/probe/resolves-without-the-legacy-name.py
python3 resources/pearde.py scan | tail -3
python3 resources/health.py score .pearde >/dev/null
python3 resources/grammar.py check
bash resources/doctor.sh > doctor.after 2>&1 || true
if grep -qE 'Traceback|no board at|not a board|no \.pearde/ board' doctor.after; then exit 1; fi
grep -qE '^  plan +ok' doctor.after && grep -qE '^  knowledge +ok' doctor.after
rm -f doctor.after
```
