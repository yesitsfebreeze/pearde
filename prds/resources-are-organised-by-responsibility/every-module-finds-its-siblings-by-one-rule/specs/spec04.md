---
complexity: 6
footprint:
  - resources/doctor.sh
  - resources/invariants/a-master-need-is-the-union-of-its-members.sh
  - resources/invariants/every-artifact-lands-inside-the-board.sh
  - resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh
---

# spec04 — the shell half of the same rule

`sys.path` does nothing for a shell script. `doctor.sh` spelled
`$DIR/board/` in fifteen launches and two existence gates, and the two
invariant harnesses spelled `resources/board/ramp.py` and `$R/board/serve.py`
outright. `doctor.sh` now carries `res()` — resources/ first, then every
directory directly under it, printing the first hit — and every launch of
`plan.py`, `brief.py`, `serve.py`, `viewtest.js` and `hotreload-test.js` goes
through it, including the ones inside `fix "…"` strings, which now print a
real absolute path. The `briefs` gate tests `[ -z "$(res brief.py)" ]` rather
than a path, and the `plugins` gate resolves `adapters` into `$ADAPTERS`
once and reuses it. The two invariant harnesses find `ramp.py` and `serve.py`
by `ls "$RES"/x.py "$RES"/*/x.py | head -1`, the same rule in the smallest
shell that will hold it.

All of it stands in the tree, uncommitted. `bash resources/doctor.sh` prints
the same 13 ok / 2 off / 5 broken rows as before the change, in the same
order; the five broken and two off rows are inherited, not caused here. What
is left is landing it, and running the PRD's probe, which is the proof for
the contract as a whole.

## Acceptance

- [x] `resources/doctor.sh` defines `res()` and contains the string
  `$DIR/board/` nowhere
- [x] sourced on its own against a tree whose modules have been moved into
  new directories, `res` finds `plan.py`, `serve.py` and `brief.py` and each
  path it prints is a real file
- [x] `res` returns non-zero and prints nothing for a name no directory under
  `resources/` holds
- [x] neither invariant harness spells a `board/` directory in a launch;
  both still parse under `bash -n`
- [x] `bash resources/doctor.sh` exits with the same code and prints the same
  sequence of row verdicts as the committed tree — no row is added, dropped
  or reddened by this change
- [x] the PRD's probe passes whole against this tree and fails against a tree
  without the rule, so the boxes above can fail

## Verify and Proof

```sh
# The board is .pearde/ at the repo root, or two directories up when this runs
# in a lane at <repo>/pearde/.lanes/<name>. The probe measures the tree it is
# named, and PEARDE_ROOT is the only thing that names it — left unset it
# defaults to the directory above the board, which is the orchestrator's
# checkout whatever tree this block was started in.
PRD=prds/resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule
B=.pearde; [ -d "$B/$PRD" ] || B=../..
PEARDE_ROOT="$PWD" bash "$B/$PRD/probe/verify.sh"
python3 - <<'PYEND'
import os, shutil, subprocess, sys, tempfile
ROOT = os.path.abspath(".")

doc = open("resources/doctor.sh", encoding="utf-8").read()
assert "\nres() {" in doc
assert "$DIR/board/" not in doc

for f in ("resources/invariants/a-master-need-is-the-union-of-its-members.sh",
          "resources/invariants/every-artifact-lands-inside-the-board.sh"):
    s = open(f, encoding="utf-8").read()
    launches = [ln for ln in s.splitlines()
                if "board/" in ln and ("python3" in ln or "bash " in ln)
                and not ln.lstrip().startswith("#")]
    assert not launches, (f, launches)
    assert subprocess.run(["bash", "-n", f]).returncode == 0, f

d = tempfile.mkdtemp()
try:
    shutil.copytree(os.path.join(ROOT, "resources"), os.path.join(d, "resources"))
    R = os.path.join(d, "resources")
    os.mkdir(os.path.join(R, "run"))
    os.rename(os.path.join(R, "board", "brief.py"),
              os.path.join(R, "run", "brief.py"))
    body = doc[doc.index("res() {"):]
    body = body[:body.index("\n}\n") + 3]
    open(os.path.join(d, "res.sh"), "w", encoding="utf-8").write(body)
    for n in ("plan.py", "serve.py", "brief.py"):
        r = subprocess.run(
            ["bash", "-c", '. "$1/res.sh"; res "$2"', "_", d, n],
            env=dict(os.environ, DIR=R), capture_output=True, text=True)
        assert r.returncode == 0 and os.path.isfile(r.stdout.strip()), (n, r.stdout, r.stderr)
    r = subprocess.run(
        ["bash", "-c", '. "$1/res.sh"; res "$2"', "_", d, "no-such-thing.py"],
        env=dict(os.environ, DIR=R), capture_output=True, text=True)
    assert r.returncode != 0 and not r.stdout.strip(), (r.returncode, r.stdout)
finally:
    shutil.rmtree(d, ignore_errors=True)
print("spec04 ok")
PYEND
```
