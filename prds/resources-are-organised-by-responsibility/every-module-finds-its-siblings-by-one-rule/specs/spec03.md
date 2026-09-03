---
complexity: 10
footprint:
  - resources/board/all.py
  - resources/grammar.py
  - resources/health.py
  - resources/memos.py
  - resources/questions.py
  - resources/board/boards.py
  - resources/board/mapfile.py
  - resources/board/needs.py
  - resources/board/prdfile.py
  - resources/board/registry.py
  - resources/board/repos.py
  - resources/board/schedule.py
  - resources/board/silence.py
  - resources/board/vision.py
  - resources/board/collect.py
  - resources/board/dispatch.py
  - resources/board/init.py
  - resources/board/run.py
  - resources/board/orphans.py
  - resources/board/ramp.py
  - resources/board/serve.py
  - resources/board/session.py
  - resources/board/shared.py
  - resources/board/specs.py
  - resources/board/transitions.py
  - resources/guard.py
  - resources/knowledge.py
  - resources/workflows.py
---

# spec03 — every other module opens with the rule, and launches by name

Twenty-five modules had a hand-rolled `sys.path` preamble of their own — one
line, or two, each spelling `HERE`, `BOARD`, `ROOT` or `dirname(dirname(...))`
in its own dialect. Twelve were there when the specs were written; thirteen
more — `grammar.py`, `health.py`, `memos.py`, `questions.py`, `boards.py`,
`mapfile.py`, `needs.py`, `prdfile.py`, `registry.py`, `repos.py`,
`schedule.py`, `silence.py`, `vision.py` — landed on the trunk while the lane
waited, and the contract is every module, so they are in the footprint too. Every one of them now opens with the same three lines
followed by the import, whatever directory it sits in:

    _D = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                    else os.path.dirname(_D))
    import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule

The conditional is what makes the rule depth-tolerant: a module directly
under `resources/` and a module one directory down both reach `resources/`
with the same text, so a file moving between them changes nothing.

The same modules stop building the path of a sibling they launch. `init.py`
asks `pearde_path.script()` for `serve.py`, `doctor.sh`, `knowledge.py`,
`memos.py` and `grammar.py`; `run.py` for `serve.py`; `guard.py` for
`plan.py` and `serve.py`, and takes `ROOT` and `PEARDE` from
`pearde_path.RES` and `pearde_path.skill_root()` instead of counting
directories; its `TOOLS` matcher reads `resources/\w+/\w+\.py`, so a module
that moves stays recognised as one of ours. `workflows.py`'s deferred `import
plan` needs no directory at all now and its three-line `board/` preamble is
gone. All of it stands in the lane, rebased onto the trunk.
`resources/board/plan.py` is deliberately **not** in this footprint — see the
report's handoff. What is left is landing it.

## Acceptance

- [x] each of the twenty-five files the block's `FILES` names contains
  `import pearde_path` and contains no bare `sys.path.insert` line of its own
  at module level besides the one the rule prescribes
- [x] no module under `resources/` other than `pearde_path.py` and
  `resources/board/plan.py` imports a sibling of this tree without carrying
  the rule
- [x] in a scratch copy with those modules moved into four new directories
  (`read/`, `write/`, `run/`, `draw/`) and no code edited, each of
  `specs.py`, `transitions.py`, `run.py`, `memos.py` and `guard.py`
  imports and executes from its new directory
- [x] no `.py` file under `resources/` addresses a sibling script as a path
  it builds itself — the pattern
  `os.path.join((HERE|DIR|BOARD|SELF|RES)…".py")` matches nowhere
- [x] no `.py` or `.sh` file under `resources/` launches a script through a
  spelled `board/` directory
- [x] `guard.py`'s `TOOLS` pattern matches `resources/read/plan.py` as well
  as `resources/board/plan.py`
- [x] `python3 resources/pearde.py help` still exits 0 and lists every
  command, so no module was broken by the edit

## Verify and Proof

```sh
python3 - <<'PYEND'
import os, re, shutil, subprocess, sys, tempfile
ROOT = os.path.abspath(".")
PY = sys.executable
sys.path.insert(0, "resources")
import pearde_path as p

FILES = ["resources/board/all.py", "resources/board/collect.py",
         "resources/board/dispatch.py", "resources/board/init.py",
         "resources/board/run.py", "resources/board/orphans.py",
         "resources/board/ramp.py", "resources/board/serve.py",
         "resources/board/specs.py", "resources/board/transitions.py",
         "resources/guard.py", "resources/workflows.py",
         "resources/grammar.py", "resources/health.py", "resources/memos.py",
         "resources/questions.py", "resources/board/boards.py",
         "resources/board/mapfile.py", "resources/board/needs.py",
         "resources/board/prdfile.py", "resources/board/registry.py",
         "resources/board/repos.py", "resources/board/schedule.py",
         "resources/board/silence.py", "resources/board/vision.py"]
RULE = re.compile(r'^sys\.path\.insert\(0, _D if os\.path\.isfile', re.M)
for f in FILES:
    s = open(f, encoding="utf-8").read()
    assert "import pearde_path" in s, f
    inserts = re.findall(r"^sys\.path\.insert\(.*$", s, re.M)
    assert len(inserts) == 1 and RULE.search(s), (f, inserts)

SIB = re.compile(r"^import (?!os|sys|re|json|time|glob|subprocess|shutil|hashlib"
                 r"|math|html|random|argparse|textwrap|tempfile|difflib|itertools"
                 r"|collections|datetime|urllib|importlib|webbrowser|socket|signal"
                 r"|threading|traceback|unicodedata|base64|struct|http|email"
                 r"|mimetypes|stat|errno|platform|getpass|uuid|csv|sqlite3|typing"
                 r"|functools|contextlib|copy|string|shlex|fnmatch|zipfile|gzip|io"
                 r"|pathlib|ast|inspect|logging|secrets|ssl|select|queue|pprint)"
                 r"[a-z_]+", re.M)
bad = []
for d in p.dirs():
    for n in sorted(os.listdir(d)):
        if not n.endswith(".py") or n in ("pearde_path.py", "plan.py"):
            continue
        s = open(os.path.join(d, n), encoding="utf-8").read()
        if SIB.search(s) and "import pearde_path" not in s:
            bad.append(n)
assert not bad, bad

spelled = subprocess.run(
    ["grep", "-rnE", r'os\.path\.join\((HERE|DIR|BOARD|SELF|RES)[^)]*\.(py|sh)"\)',
     "resources", "--include=*.py"], capture_output=True, text=True)
assert not spelled.stdout.strip(), spelled.stdout
boardstr = subprocess.run(
    ["grep", "-rnE", r'(python3|sys\.executable)[^#]*board/[a-z-]+\.(py|js)|"board", "[a-z]+\.py"',
     "resources", "--include=*.py", "--include=*.sh"], capture_output=True, text=True)
assert not boardstr.stdout.strip(), boardstr.stdout

g = open("resources/guard.py", encoding="utf-8").read()
tools = re.search(r"^TOOLS = re\.compile\(r\"(.*)\"\)$", g, re.M).group(1)
pat = re.compile(tools)
assert pat.search("resources/read/plan.py") and pat.search("resources/board/plan.py")

d = tempfile.mkdtemp()
try:
    shutil.copytree(os.path.join(ROOT, "resources"), os.path.join(d, "resources"))
    for dirpath, dirs, _ in os.walk(d):
        for n in list(dirs):
            if n == "__pycache__":
                shutil.rmtree(os.path.join(dirpath, n)); dirs.remove(n)
    R = os.path.join(d, "resources")
    for sub in ("read", "write", "run", "draw"):
        os.mkdir(os.path.join(R, sub))
    MOVES = {"read": ["board/specs.py", "board/orphans.py", "memos.py",
                      "workflows.py", "questions.py", "health.py"],
             "write": ["board/transitions.py", "board/collect.py", "board/init.py"],
             "run": ["board/run.py", "board/dispatch.py", "board/ramp.py",
                     "board/brief.py", "guard.py"],
             "draw": ["board/all.py"]}
    for sub, rels in MOVES.items():
        for rel in rels:
            os.rename(os.path.join(R, rel),
                      os.path.join(R, sub, os.path.basename(rel)))
    for m in ("specs.py", "transitions.py", "run.py", "memos.py", "guard.py"):
        r = subprocess.run(
            [PY, "-c",
             "import sys; sys.path.insert(0, 'resources')\n"
             "import pearde_path, importlib.util as u\n"
             "q = pearde_path.script(%r)\n"
             "s = u.spec_from_file_location('probe', q); mm = u.module_from_spec(s)\n"
             "s.loader.exec_module(mm); print('ok')" % m],
            cwd=d, capture_output=True, text=True)
        assert r.stdout.strip().endswith("ok"), (m, r.stdout, r.stderr)
finally:
    shutil.rmtree(d, ignore_errors=True)

h = subprocess.run([PY, "resources/pearde.py", "help"], capture_output=True, text=True)
assert h.returncode == 0 and h.stdout.count("\n") > 40, h.stderr
print("spec03 ok")
PYEND
```
