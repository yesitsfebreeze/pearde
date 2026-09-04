---
complexity: 7
footprint:
  - resources/read
  - resources/write
  - resources/draw
  - resources/run
  - resources/record
  - resources/check
  - resources/install
  - resources/board
  - .gitignore
---

# spec02 — the sixty-three files move into the seven directories

Seven directories under `resources/`, each named for what the files in it are
responsible for, and `resources/board/` gone. Sixty-three files change path.
Two do not move: `resources/pearde.py`, which `pearde_path.skill_root()`
probes for, and `resources/pearde_path.py`, which every module's preamble
reaches for one directory up.

**What already stands.** With spec01 landed, the move needs no code edit at
all: the probe cut all sixty-three in a scratch tree and
`python3 resources/pearde.py help` came back byte-identical.

**What is left.** The cut itself, as `git mv`, in the shape
`probe/moves.sh` runs:

| directory | is responsible for | holds |
|---|---|---|
| `read/` | reading the plan and answering off it, writing nothing | `plan.py` `boards.py` `prdfile.py` `repos.py` `registry.py` `silence.py` `needs.py` `vision.py` `schedule.py` `mapfile.py` `orphans.py` `example/` |
| `write/` | changing the board | `transitions.py` `specs.py` `collect.py` `init.py` `edit.py` |
| `draw/` | drawing it for a person | `serve.py` `render.py` `all.py` `view.js` `view.css` `lit-core.min.js` `adapters/` `obsidian/` |
| `run/` | launching work, and holding the tree it runs in | `run.py` `dispatch.py` `ramp.py` `brief.py` `lanes.py` `session.py` `shared.py` `refuse.py` `guard.py` |
| `record/` | the records kept beside the board | `memos.py` `workflows.py` `grammar.py` `knowledge.py` `questions.py` `common.py` `knowledge/` |
| `check/` | checking the repo and what it says about itself | `index.py` `prose.py` `health.py` `doctor.sh` |
| `install/` | putting it where the agent looks | `install.sh` `update.sh` `statusline.sh` |

`scout/`, `graph/` and `invariants/` stay as they are — each is already one
directory named for what it is responsible for.

Two paths outside the move are wrong the moment it lands, and are part of it:
`install.sh`'s `PLUGIN_DIR`, which downloads the Obsidian plugins into
`$ROOT/resources/board/obsidian/plugins` and would quietly re-create a
`resources/board/`; and the three `.gitignore` patterns naming that same
plugin path.

## Acceptance

- [ ] `resources/board/` does not exist
- [ ] the seven directories exist, each holding what the table above names
- [ ] `resources/` holds no file directly but `pearde.py` and `pearde_path.py`
- [ ] every move is a `git mv` — `git log --follow` reaches each file's history
- [ ] `python3 resources/pearde.py help` is byte-identical to what it printed before this spec
- [ ] `python3 resources/pearde.py scan` reads this board and prints its PRD count
- [ ] `install.sh` writes its plugins under `resources/draw/obsidian/plugins`, and `.gitignore` names that path
- [ ] `pearde init` in an empty git repo, then `add`, then `scan`, all run against the moved tree

## Verify and Proof

```sh
test ! -d resources/board
for d in read write draw run record check install; do test -d "resources/$d"; done
test $(ls -p resources | grep -v / | grep -vc '^pearde\(_path\)\?\.py$' | tr -d ' ') -eq 0
test -f resources/read/plan.py && test -f resources/draw/serve.py
test -f resources/check/doctor.sh && test -f resources/install/install.sh
test -f resources/record/memos.py && test -f resources/write/collect.py
test -f resources/run/guard.py && test -f resources/draw/lit-core.min.js
! grep -rq 'resources/board/obsidian' resources/install/install.sh .gitignore
grep -q 'resources/draw/obsidian/plugins' .gitignore
python3 resources/pearde.py help > /tmp/spec02-help.txt
test $(wc -l < /tmp/spec02-help.txt | tr -d ' ') -eq 87
python3 resources/pearde.py scan | head -1 | grep -q '^board: '
B=$(mktemp -d); (cd "$B" && git init -q . \
  && python3 "$PWD/../resources/pearde.py" init >/dev/null 2>&1 || true)
python3 - "$B" <<'PY'
import subprocess, sys, os
B = sys.argv[1]
r = subprocess.run(['git', 'init', '-q', '.'], cwd=B)
R = os.path.abspath('resources/pearde.py')
for a in (['init'], ['add', 'a probe prd'], ['scan']):
    p = subprocess.run(['python3', R] + a, cwd=B, capture_output=True, text=True)
    assert p.returncode == 0, (a, p.stderr[-400:])
print('a board is made and read by the moved tree')
PY
rm -rf "$B"
echo spec02 green
```
