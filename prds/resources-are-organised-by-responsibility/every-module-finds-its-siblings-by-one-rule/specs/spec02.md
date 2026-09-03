---
complexity: 10
footprint:
  - resources/pearde.py
  - resources/board/brief.py
---

# spec02 — the two entry points probe for `resources/pearde.py` and discover everywhere

`resources/pearde.py` and `resources/board/brief.py` are the two files that
walk up looking for the repo root. Both walked for `resources/board/plan.py`
by name, so renaming that directory killed the whole command surface with no
file moved and no code changed. Both now ask
`pearde_path.skill_root(__file__)`, whose marker is `resources/pearde.py` —
the dispatcher, the one file that cannot move — and each keeps the exit it
already had when there is no root above it.

The dispatcher changes in three more ways. Its `FORWARD` table names a script
by bare basename (`plan.py`, `serve.py`) instead of `board/plan.py`, and
`run()`, `docstring()` and `cmd_view()` resolve that basename through
`pearde_path.script()`, printing `pearde: no <script> under <resources>` and
exiting 2 when nothing holds it. `discover()` no longer globs
`resources/board/*.py`: a new `modules()` walks every directory
`pearde_path.dirs()` names — the same list that is on `sys.path` — and a
basename claimed by two directories comes back as a problem naming both
rather than as a silent win for whichever sorted first. All of it stands in
the tree, uncommitted; `pearde help` is byte-identical to before the change,
and stays byte-identical when `resources/board/` is renamed or the modules
are split four ways. What is left is landing it.

## Acceptance

- [x] neither `resources/pearde.py` nor `resources/board/brief.py` contains
  the string `"resources", "board", "plan.py"`; the root probe is written out
  exactly once in the tree, in `resources/pearde_path.py`
- [x] `python3 resources/board/brief.py --check` exits 0, and outside any
  tree holding `resources/pearde.py` it still exits 2 with a message naming
  `resources/pearde.py`
- [x] `pearde help` prints the same bytes as before the change
- [x] in a scratch copy with `resources/board/` renamed to `resources/core/`
  and no code edited, `pearde help` prints those same bytes
- [x] every `FORWARD` row names a bare basename — no value in the table
  contains a `/`
- [x] `discover()` finds a `COMMANDS` module in a directory that is not
  `board/`: in a scratch copy with `specs.py` moved to `resources/read/`, the
  `specced` command is still routed
- [x] two files of the same basename in two directories under `resources/`
  produce a problem naming both directories, and neither is imported

## Verify and Proof

```sh
python3 - <<'PYEND'
import os, re, shutil, subprocess, sys, tempfile
ROOT = os.path.abspath(".")
PY = sys.executable

for f in ("resources/pearde.py", "resources/board/brief.py"):
    s = open(f, encoding="utf-8").read()
    assert '"resources", "board", "plan.py"' not in s, f
    assert "pearde_path" in s, f

probe = [p for p in ("resources/pearde_path.py", "resources/pearde.py",
                     "resources/board/brief.py")
         if '"resources", "pearde.py"' in open(p, encoding="utf-8").read()]
assert probe == ["resources/pearde_path.py"], probe

assert subprocess.run([PY, "resources/board/brief.py", "--check"]).returncode == 0

base = subprocess.run([PY, "resources/pearde.py", "help"],
                      capture_output=True, text=True)
assert base.returncode == 0 and base.stdout.count("\n") > 40

src = open("resources/pearde.py", encoding="utf-8").read()
table = src[src.index("FORWARD = {"):src.index("RESERVED")]
assert not re.findall(r'\("(?:[\w.-]+/)+[\w.-]+"', table), table

d = tempfile.mkdtemp()
try:
    shutil.copytree(os.path.join(ROOT, "resources"), os.path.join(d, "resources"))
    for dirpath, dirs, _ in os.walk(d):
        for n in list(dirs):
            if n == "__pycache__":
                shutil.rmtree(os.path.join(dirpath, n)); dirs.remove(n)
    os.rename(os.path.join(d, "resources", "board"),
              os.path.join(d, "resources", "core"))
    r = subprocess.run([PY, "resources/pearde.py", "help"], cwd=d,
                       capture_output=True, text=True)
    assert r.stdout == base.stdout, r.stdout[:400] + r.stderr[:400]

    os.mkdir(os.path.join(d, "resources", "read"))
    os.rename(os.path.join(d, "resources", "core", "specs.py"),
              os.path.join(d, "resources", "read", "specs.py"))
    r = subprocess.run([PY, "resources/pearde.py", "specced", "--help"], cwd=d,
                       capture_output=True, text=True)
    assert r.returncode == 0 and "specced" in r.stdout, r.stdout + r.stderr

    shutil.copyfile(os.path.join(d, "resources", "read", "specs.py"),
                    os.path.join(d, "resources", "core", "specs.py"))
    r = subprocess.run([PY, "resources/pearde.py", "help"], cwd=d,
                       capture_output=True, text=True)
    err = r.stderr
    assert "specs.py" in err and "core" in err and "read" in err, err
finally:
    shutil.rmtree(d, ignore_errors=True)
print("spec02 ok")
PYEND
```
