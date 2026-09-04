---
complexity: 11
footprint:
  - resources/doctor.sh
  - resources/install.sh
  - resources/update.sh
  - resources/index.py
  - resources/prose.py
  - resources/memos.py
  - resources/grammar.py
  - resources/workflows.py
  - resources/board/plan.py
  - resources/board/refuse.py
---

# spec01 — every root and every launch is found, not counted

No script under `resources/` may work out the repo root, a sibling module or a
sibling script by counting directory levels. Eleven files still do, and each
one is correct only while it sits exactly where it sits today. This spec makes
them all ask, and moves nothing — the tree is byte-identical in shape when it
is done, and `pearde help`, `pearde scan` and `doctor.sh` print what they
printed before.

**What already stands.** `resources/pearde_path.py` holds the rule:
`skill_root()` finds the repo by probing for `resources/pearde.py`, `script()`
finds a sibling script by basename anywhere under `resources/`, and importing
it puts every directory under `resources/` on `sys.path`.
`resources/doctor.sh` already carries `res()`. Thirty-one modules already open
with the one preamble.

**What is left.** Four classes, each one found by running the move in a
scratch tree and reading what died:

1. **A hand-rolled preamble.** `resources/board/plan.py` inserts its own
   directory and its parent and then imports `memos`, `questions`, `render`,
   `workflows`. `resources/index.py` inserts its own directory and imports
   `common`. `resources/prose.py` has no preamble and needs one for the root.
   All three take the four-line rule the other thirty-one carry.
2. **A root that is two `dirname` calls.** `memos.py`, `grammar.py`,
   `workflows.py`, `prose.py` and `index.py` each spell
   `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` for the repo
   root. That is the repo only while the file sits directly in `resources/`.
   Each becomes `pearde_path.skill_root()`.
3. **A shell script whose root is its own parent.** `doctor.sh`, `install.sh`
   and `update.sh` set `SKILL_ROOT`/`ROOT` to `$DIR/..`, and `doctor.sh`'s
   `res()` searches `$DIR` and `$DIR/*/`. Each gets the shell half of the same
   rule — anchor on the directory holding `pearde.py`, then derive the root
   and search from there. Twenty-six `$DIR/<script>` launches in `doctor.sh`
   go through `res()`, and its one
   backtick-quoted `sys.path.insert(0,'$DIR/board')` anchors on `resources/`.
4. **A sibling loaded inside a bare `except Exception`.**
   `resources/board/refuse.py` `_guard_board_of()` builds
   `dirname(dirname(__file__))/guard.py` and swallows every failure, so a
   wrong path costs the caller its guard in silence. It asks
   `pearde_path.script("guard.py")` instead.

`resources/board/lanes.py`, `edit.py`, `render.py` and `resources/common.py`
are left alone on purpose: none reaches a sibling or the root.

## Acceptance

- [ ] `resources/pearde_path.py` is unchanged — this spec uses the rule, it does not extend it
- [ ] no file under `resources/` matches `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`
- [ ] `resources/board/plan.py`, `resources/index.py` and `resources/prose.py` each carry `import pearde_path`
- [ ] `doctor.sh`, `install.sh` and `update.sh` each derive their root from the directory holding `pearde.py`, not from `$DIR/..`
- [ ] `doctor.sh` launches no sibling script as a path it builds itself — every one goes through `res()`
- [ ] `resources/board/refuse.py` resolves `guard.py` through `pearde_path.script`
- [ ] `python3 resources/pearde.py help` is byte-identical to what it printed before this spec
- [ ] `python3 resources/index.py check` prints the same four inherited problems it printed before this spec
- [ ] `bash resources/doctor.sh` prints the same row verdicts it printed before this spec

## Verify and Proof

```sh
test $(grep -rlE 'os\.path\.dirname\(os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\)' \
       resources --include='*.py' | wc -l | tr -d ' ') -eq 0
for f in resources/board/plan.py resources/index.py resources/prose.py \
         resources/board/refuse.py; do grep -q 'import pearde_path' "$f"; done
grep -q 'pearde_path.script("guard.py")' resources/board/refuse.py
for f in resources/doctor.sh resources/install.sh resources/update.sh; do
  ! grep -q 'cd "$DIR/.." && pwd' "$f"; done
test $(grep -c '\$DIR/[a-z_]*\.\(py\|sh\)' resources/doctor.sh | tr -d ' ') -eq 0
! grep -q 'DIR/board' resources/doctor.sh
python3 resources/pearde.py help > /tmp/spec01-help.txt
test $(wc -l < /tmp/spec01-help.txt | tr -d ' ') -eq 87
python3 resources/index.py check > /tmp/spec01-index.txt || true
cat /tmp/spec01-index.txt
test $(wc -l < /tmp/spec01-index.txt | tr -d ' ') -eq 4
bash resources/doctor.sh > /tmp/spec01-doctor.txt 2>&1 || true
grep -E '^  skills +ok ' /tmp/spec01-doctor.txt
grep -E '^  statusline +ok ' /tmp/spec01-doctor.txt
grep -E '^  briefs +ok ' /tmp/spec01-doctor.txt
echo spec01 green
```
