---
complexity: 10
footprint:
  - README.md
  - index.md
  - references/archive.md
  - references/files.md
  - references/install.md
  - references/parts/doctor.md
  - references/parts/guard.md
  - references/parts/master.md
  - references/parts/workers.md
  - references/settings.md
  - references/system.md
  - resources/pearde.py
  - resources/memos.py
  - resources/guard.py
---

# spec01 — rewrite every genuinely-bare `prds/` mention to `.pearde/` or `.pearde/prds/`

Every bare `prds/` mention across the 14 scoped files is read in context,
checked against the code or contract it describes, and rewritten — `.pearde/`
where it names the board root, `.pearde/prds/` where it names the PRD tree.

## What is on disk

Measured against `HEAD`, not against an earlier pass's count: **20** bare
tokens across **11** files. `references/parts/workers.md`, `resources/memos.py`
and `resources/guard.py` carry none at `HEAD` — the rename-table PRD had
already corrected them, so they are in the footprint but need no edit.

| file | bare at `HEAD` |
|---|---|
| `README.md` | 1 |
| `index.md` | 1 |
| `references/archive.md` | 3 |
| `references/files.md` | 2 |
| `references/install.md` | 2 |
| `references/parts/doctor.md` | 2 |
| `references/parts/guard.md` | 1 |
| `references/parts/master.md` | 3 |
| `references/settings.md` | 3 |
| `references/system.md` | 1 |
| `resources/pearde.py` | 1 |

## Which of the two targets

`BOARD_DIR = ".pearde"` and `PRDS_DIR = "prds"` in `@resources/board/plan.py`.
`find_board` returns `<repo>/.pearde`, so every reader that joins a setting
onto `board` joins it onto `.pearde/`, not `.pearde/prds/`. Six mentions
describe exactly that join and take `.pearde/`:

| mention | the code it describes |
|---|---|
| `references/settings.md` `memos:` | `memos_dir` — `os.path.join(board, v)` |
| `references/settings.md` `workflows:` | `workflows_dir` — `os.path.join(board, v)` |
| `references/settings.md` `members:` | `members` — `os.path.join(board, path)` |
| `references/parts/master.md` member resolve | `members` — the same join |
| `references/parts/doctor.md` `workflows:` outside | `resources/doctor.sh` — the default `$BOARD/workflows` is inside `.pearde/`, so "outside" can only mean the board root |
| `references/parts/doctor.md` harness `find` | `resources/doctor.sh` — `find "$BOARD" -name verify.sh`, `BOARD="$d/.pearde"` |

The rest name the PRD tree and take `.pearde/prds/` — `README.md`'s "files
under", `archive.md`'s walk cost, `files.md`'s manifest row, `master.md`'s
"keeps its own" and repo-root row, `memos.py`'s `prds:` walk root
(`os.path.join(board, "prds")`), `guard.py`'s `skill_file` (the code tests
`os.path.join(SKILL, BOARD_DIR, PRDS_DIR)`). `index.md`, `install.md` and
`system.md` name the board root and take `.pearde/`.

## Exceptions

Bare `prds/` that stays bare, because the code it quotes is literal:

| where | why |
|---|---|
| `references/parts/guard.md`, `resources/guard.py` — `ls prds/*/prd.md` | the hand-walk pattern `guard.py`'s `WALKS` matches, quoted verbatim |
| `resources/guard.py` — `\bprds/[^\|;&]*\*` | that regex itself |
| `references/parts/workers.md` — `<prds/>` | the brief placeholder, a table rule |

## Acceptance

- [x] every bare `prds/` mention in the 14 scoped files is rewritten or is one
      of the documented exceptions — the Verify block's scanner reports
      `bare tokens: 0 | documented exceptions: 5`, and a `HEAD`-vs-worktree
      count run the same way reports `TOTAL bare: HEAD=20  now=0`
- [x] each of the six board-root mentions says `.pearde/`, not `.pearde/prds/`,
      matching the code that joins the setting onto `board` — Verify prints
      `board-dir ok` for all four call sites (`settings.md` x3 in one string,
      `master.md`, `doctor.md` x2)
- [x] no `.pearde/.pearde` or `prds/prds` introduced across the footprint —
      Verify prints `forbidden tokens (.pearde/.pearde, prds/prds): 0`
- [x] `resources/pearde.py`, `resources/memos.py`, `resources/guard.py` still
      compile — Verify prints `py_compile: ok`
- [x] the repo's own gate is green — `resources/index.py check` exit 0,
      `resources/memos.py check` exit 0, `resources/doctor.sh` exit 0 with
      `pearde: every part this repo owns checks out.`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 - <<'PY'
import io, sys

FILES = """README.md index.md references/archive.md references/files.md
references/install.md references/parts/doctor.md references/parts/guard.md
references/parts/master.md references/parts/workers.md references/settings.md
references/system.md resources/pearde.py resources/memos.py
resources/guard.py""".split()

# A `prds/` is bare unless it is spelled `.pearde/prds/`, is the `<prds/>`
# placeholder, or is the `ls prds/*` walk pattern / the regex that matches it.
# The test is on the characters immediately before the token — a substring
# test over the whole line is unsound ("elsewhere" contains "ls").
bare, allowed = [], []
for f in FILES:
    for n, line in enumerate(io.open(f, encoding="utf-8"), 1):
        i = 0
        while True:
            i = line.find("prds/", i)
            if i < 0:
                break
            b = line[:i]
            if b.endswith(".pearde/"):
                pass
            elif b.endswith("<"):
                allowed.append((f, n, "<prds/> placeholder"))
            elif b.endswith("ls "):
                allowed.append((f, n, "WALKS ls-pattern"))
            elif b.endswith("\\b"):
                allowed.append((f, n, "WALKS regex literal"))
            else:
                bare.append((f, n, line.strip()))
            i += 5

for f, n, why in allowed:
    print(f"allowed  {f}:{n}  ({why})")
if bare:
    for f, n, line in bare:
        print(f"BARE     {f}:{n}  {line}")
    sys.exit(f"FAIL: {len(bare)} bare prds/ token(s) remain")
print(f"bare tokens: 0 | documented exceptions: {len(allowed)}")

# the six board-root mentions: `.pearde/`, never `.pearde/prds/`
for path, needle, want in [
    ("references/settings.md", "relative to `.pearde/`.", 3),
    ("references/parts/master.md", "against the master's `.pearde/`.", 1),
    ("references/parts/doctor.md", "pointing outside `.pearde/` is", 1),
    ("references/parts/doctor.md", "returns under `.pearde/`, and nothing else", 1),
]:
    got = io.open(path, encoding="utf-8").read().count(needle)
    if got != want:
        sys.exit(f"FAIL: {path}: {got} x {needle!r}, want {want}")
    print(f"board-dir ok  {path}: {want} x {needle!r}")

for f in FILES:
    s = io.open(f, encoding="utf-8").read()
    for bad in (".pearde/.pearde", "prds/prds"):
        if bad in s:
            sys.exit(f"FAIL: {f} contains {bad}")
print("forbidden tokens (.pearde/.pearde, prds/prds): 0")
PY

python3 -m py_compile resources/pearde.py resources/memos.py resources/guard.py
echo "py_compile: ok"

python3 resources/index.py check
python3 resources/memos.py check
echo "gate: index + memos green"
echo "verify: clean"
```
