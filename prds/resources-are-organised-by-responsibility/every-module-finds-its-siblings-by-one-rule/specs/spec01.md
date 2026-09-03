---
complexity: 8
footprint:
  - resources/pearde_path.py
  - references/files.md
  - index.md
---

# spec01 — one file holds the rule, and the map knows it

`resources/pearde_path.py` is the one place the rule is written. Importing it
puts `resources/` and every directory directly under it on `sys.path`, so a
bare `import plan` resolves from any of them. It exposes two functions
besides that side effect: `skill_root(start)`, the nearest ancestor holding
`resources/pearde.py` — the one file that cannot move, so it is the marker —
and `script(name)`, which finds a script by basename anywhere under
`resources/`, for the callers that launch a sibling as a subprocess where
`sys.path` does nothing.

The file stands in the tree, uncommitted, with its docstring, `RES`,
`dirs()`, `_install()`, `skill_root()` and `script()`. `dirs()` skips a name
beginning `.` or `_` and skips `node_modules`, so `__pycache__` never reaches
`sys.path`. It imports nothing of this tree, so it can never be part of an
import cycle. Its row in `references/files.md` and its two scope anchors in
`index.md` (`@@handles`, `@@install`) are written, and the `pearde.py` row's
claim that discovery walks `resources/board/*.py` is corrected in the same
edit. Nothing further is to be built here; what is left is landing it.

## Acceptance

- [x] `resources/pearde_path.py` is on disk and importing it adds
  `resources/` and every directory directly under it to `sys.path`, in that
  order, with `resources/` searched first
- [x] `dirs()` excludes any entry beginning `.` or `_` and excludes
  `node_modules`, so `__pycache__` is never on the path
- [x] no file reachable on that path shadows a stdlib module name
- [x] `skill_root(start)` returns the nearest ancestor of `start` holding
  `resources/pearde.py`, and returns `None` rather than exiting when there is
  none — the caller decides what an absent root costs
- [x] `script(name)` returns the path of a script held anywhere under
  `resources/` and `None` when no directory holds it
- [x] `pearde_path.py` imports no module of this tree, so it cannot close an
  import cycle
- [x] `references/files.md` carries a row for `@resources/pearde_path.py`,
  `index.md` names it in at least one `@@` scope, and
  `python3 resources/index.py check` reports no problem about it

## Verify and Proof

```sh
python3 - <<'PYEND'
import os, sys, subprocess
sys.path.insert(0, "resources")
import pearde_path as p

names = [os.path.basename(d) for d in p.dirs()]
assert names[0] == "resources", names
assert "board" in names, names
assert not [n for n in names if n.startswith((".", "_")) or n == "node_modules"], names
assert p.dirs()[0] == p.RES

std = set(sys.stdlib_module_names)
shadow = [n for d in p.dirs() for n in os.listdir(d)
          if n.endswith(".py") and n[:-3] in std]
assert not shadow, shadow

here = os.path.abspath(".")
assert p.skill_root(os.path.join(here, "resources", "board", "plan.py")) == here
assert p.skill_root("/") is None

assert p.script("serve.py") and os.path.isfile(p.script("serve.py"))
assert p.script("doctor.sh") and os.path.isfile(p.script("doctor.sh"))
assert p.script("no-such-thing.py") is None

src = open("resources/pearde_path.py", encoding="utf-8").read()
mods = {n for d in p.dirs() for n in os.listdir(d) if n.endswith(".py")}
for m in mods - {"pearde_path.py"}:
    assert ("import " + m[:-3] + "\n") not in src, m

files = open("references/files.md", encoding="utf-8").read()
assert "| @resources/pearde_path.py |" in files
assert "@resources/pearde_path.py" in open("index.md", encoding="utf-8").read()

out = subprocess.run([sys.executable, "resources/index.py", "check"],
                     capture_output=True, text=True)
named = [ln for ln in (out.stdout + out.stderr).splitlines() if "pearde_path" in ln]
assert not named, named
print("spec01 ok")
PYEND
```
