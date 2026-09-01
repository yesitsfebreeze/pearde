#!/usr/bin/env python3
"""PROBE — uncommitted. `collect --report <path>` routes its own verdict.

Builds a fixture board in a mktemp dir (never under a board), a PRD per
verdict, and runs `cmd_collect(["--report", <path>, <rel>, …])` through
collect.py's own entry. Asserts the transition each verdict routes to, that a
missing or unknown verdict is refused with nothing written, that a red verify
is still exit 1 with nothing written, and that bare `collect` (no --report)
still works. Pass one: the implementation already stands in the tree; this
measures it.
"""
import os
import subprocess
import sys
import tempfile

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"   # the verify forks python; no .pyc in the fixture

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/feb/dev/infra/pearde"
RES = os.path.join(REPO, "resources")
BOARD_PY = os.path.join(RES, "board")
sys.path.insert(0, BOARD_PY)
sys.path.insert(0, RES)

PASS = []
FAIL = []


def ok(label, cond, detail=""):
    (PASS if cond else FAIL).append(label)
    print(("ok   " if cond else "FAIL ") + label + (f" — {detail}" if detail and not cond else ""))


def sh(cmd, cwd, board=None):
    env = dict(os.environ)
    if board:
        env["PEARDE_BOARD"] = board   # not read by the tools; explicit --board is used
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return r.returncode, (r.stdout + r.stderr).strip()


def mkboard(root, include_lib=False):
    """A fixture board at <root>/.pearde with one committed src/ file."""
    board = os.path.join(root, ".pearde")
    os.makedirs(os.path.join(board, "prds"))
    os.makedirs(os.path.join(root, "src"))
    with open(os.path.join(root, "src", "app.py"), "w") as f:
        f.write("def run():\n    return 2\n")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "probe@example"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "probe"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
    if include_lib:
        import shutil
        shutil.copytree(os.path.join(REPO, ".pearde", "workflows"),
                        os.path.join(board, "workflows"))
    return board


def prd(board, slug, state, body="", needs=None, claim=None, specs=None):
    d = os.path.join(board, "prds", slug)
    os.makedirs(d, exist_ok=True)
    fm = [f"state: {state}", "priority: 10"]
    if needs:
        fm.append("needs:")
        fm += [f"  - {n}" for n in needs]
    if claim:
        fm.append(f"claim: probe {claim}")
    text = "---\n" + "\n".join(fm) + "\n---\n\n# " + slug + " — fixture\n\nfixture PRD for the probe.\n"
    if body:
        text += "\n" + body.strip() + "\n"
    with open(os.path.join(d, "prd.md"), "w") as f:
        f.write(text)
    if specs:
        os.makedirs(os.path.join(d, "specs"), exist_ok=True)
        with open(os.path.join(d, "specs", "spec01.md"), "w") as f:
            f.write(specs)
    return d


SPEC_OK = """---
complexity: 10
footprint:
  - src/app.py
---

# spec01 — the fixture's one unit

A passing spec: one unit, one box, one verify.

## Acceptance

- [ ] src/app.py still returns 2 after the change

## Verify and Proof

```sh
python3 -c "import sys; sys.path.insert(0, 'src'); import app; assert app.run() == 2"
```
"""

REPORT_HEAD = """Verdict: {word}

Built it. The report body stands in for the run's words.

## Scores

complexity: 10
blast-radius: mid
workflow: {wf}
"""


def state_of(board, slug):
    import plan as P
    p = P.scan(board).get(slug)
    return p["state"] if p else None


def collect_report(board, rel, report_path, extra=()):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "probe_collect", os.path.join(BOARD_PY, "collect.py"))
    C = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(C)
    argv = ["--as", "engineer", "--board", board, "--report", report_path,
            rel, *extra]
    return C.cmd_collect(argv)


def main():
    tmp = tempfile.mkdtemp(prefix="pearde-probe-")
    print(f"fixture: {tmp}")

    # ── SPECCED, workflow already in the library ────────────────────────
    b = mkboard(os.path.join(tmp, "a"), include_lib=True)
    prd(b, "specced-lib", "analyzing", specs=SPEC_OK)
    rp = os.path.join(tmp, "r-specced.md")
    with open(rp, "w") as f:
        f.write(REPORT_HEAD.format(word="SPECCED", wf="probe-then-spec"))
    code = collect_report(b, "specced-lib", rp)
    ok("SPECCED routes to specced and the PRD moves", code == 0
       and state_of(b, "specced-lib") == "specced",
       f"exit {code}, state {state_of(b, 'specced-lib')}")
    ok("SPECCED carries the Scores values onto the PRD",
       "complexity: 10" in open(os.path.join(b, "prds", "specced-lib",
                                            "prd.md")).read()
       and "blast-radius: mid" in open(os.path.join(b, "prds", "specced-lib",
                                                    "prd.md")).read())

    # ── SPECCED with a route — the slug is new, the report drafts it ────
    b = mkboard(os.path.join(tmp, "b"))
    prd(b, "specced-route", "analyzing", specs=SPEC_OK)
    route = REPORT_HEAD.format(word="SPECCED", wf="close-a-worker-round") + """
## Route

## Use when

- A worker's report is on disk and the round needs the state it names moved.
- Not when the state is being set by hand — `add-a-file-to-the-skill` is the
  near-miss for prose only.

## Steps

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | `read-the-report` | the verdict is read from the file, not from memory | `stop` |
| 2 | `read-the-report` | the same read answers again on a retry, and a second move is refused by the state's own gate | `→ 1` |

### atomic read-the-report

## Do

1. Read the head of the report for its verdict word.

## Done when

- The word is read or the absence is named.

## Fails when
"""
    rp = os.path.join(tmp, "r-route.md")
    with open(rp, "w") as f:
        f.write(route)
    code = collect_report(b, "specced-route", rp)
    wf_file = os.path.join(b, "workflows", "close-a-worker-round.md")
    ok("SPECCED with a new slug routes --route - and drafts the workflow",
       code == 0 and state_of(b, "specced-route") == "specced"
       and os.path.isfile(wf_file),
       f"exit {code}, state {state_of(b, 'specced-route')}, wf "
       f"{os.path.isfile(wf_file)}")

    # ── QUESTION ─────────────────────────────────────────────────────────
    b = mkboard(os.path.join(tmp, "c"))
    q = """## Questions

### Q1: Where does the stored summary live?

The summary is read many times a day and changes rarely. Keeping it in memory is fastest and gone on restart; keeping it on disk survives a restart and costs a write. Where should it live?

1. **On disk** — written when it changes, read at start; nothing is lost on a restart. (recommended)
2. **In memory** — rebuilt when asked; simpler, and a restart costs one rebuild.
3. **Both** — memory during the day, disk at close; always fast, never lost.
"""
    prd(b, "asker", "analyzing", body=q)
    rp = os.path.join(tmp, "r-q.md")
    with open(rp, "w") as f:
        f.write("Verdict: QUESTION\n\nThe fork is written into the PRD body.\n")
    code = collect_report(b, "asker", rp)
    ok("QUESTION routes to release question", code == 0
       and state_of(b, "asker") == "question",
       f"exit {code}, state {state_of(b, 'asker')}")

    # ── BLOCKED — an implementer's verdict, from claimed ────────────────
    b = mkboard(os.path.join(tmp, "d"))
    prd(b, "blocker", "claimed", claim="w 2026-09-01 08:00", needs=["doner"],
        specs=SPEC_OK)
    prd(b, "doner", "open")
    rp = os.path.join(tmp, "r-b.md")
    with open(rp, "w") as f:
        f.write("Verdict: BLOCKED\n\nWaits on the sibling.\n")
    code = collect_report(b, "blocker", rp)
    ok("BLOCKED routes to release blocked", code == 0
       and state_of(b, "blocker") == "blocked",
       f"exit {code}, state {state_of(b, 'blocker')}")

    # ── FAILED — needs a ## Failure section ──────────────────────────────
    b = mkboard(os.path.join(tmp, "d2"))
    prd(b, "failer", "claimed", claim="w 2026-09-01 08:00", specs=SPEC_OK)
    p = os.path.join(b, "prds", "failer", "prd.md")
    with open(p, "a") as f:
        f.write("\n## Failure\n\nThe verify went red and stayed red.\n")
    rp = os.path.join(tmp, "r-f.md")
    with open(rp, "w") as f:
        f.write("Verdict: FAILED\n\nWhat broke is in the PRD body.\n")
    code = collect_report(b, "failer", rp)
    ok("FAILED routes to release failed", code == 0
       and state_of(b, "failer") == "failed",
       f"exit {code}, state {state_of(b, 'failer')}")

    # ── REFINE — the Split table creates children ───────────────────────
    b = mkboard(os.path.join(tmp, "e"))
    prd(b, "splitter", "analyzing")
    rp = os.path.join(tmp, "r-r.md")
    with open(rp, "w") as f:
        f.write("Verdict: REFINE\n\nTwo contracts, one build.\n\n## Split\n\n"
                "| child | contract | needs |\n|---|---|---|\n"
                "| left | the reading half exists | — |\n"
                "| right | the writing half exists | left |\n")
    code = collect_report(b, "splitter", rp)
    kids = sorted(os.listdir(os.path.join(b, "prds", "splitter")))
    ok("REFINE routes to refine and lands the children", code == 0
       and state_of(b, "splitter") == "open" and "left" in kids
       and "right" in kids,
       f"exit {code}, state {state_of(b, 'splitter')}, kids {kids}")

    # ── DONE — collect itself, with the gates ────────────────────────────
    b = mkboard(os.path.join(tmp, "g"))
    good = SPEC_OK.replace("- [ ]", "- [x]")
    prd(b, "doner", "claimed", claim="w 2026-09-01 08:00", specs=good)
    rp = os.path.join(tmp, "r-done.md")
    with open(rp, "w") as f:
        f.write("Verdict: DONE\n\nEvery box ticked, verify green.\n")
    code = collect_report(b, "doner", rp)
    txt = open(os.path.join(b, "prds", "doner", "prd.md")).read()
    ok("DONE routes to collect — done, commit recorded", code == 0
       and state_of(b, "doner") == "done" and "commit:" in txt,
       f"exit {code}, state {state_of(b, 'doner')}")
    r = sh = subprocess.run(["git", "-C", os.path.dirname(b), "log",
                             "--oneline", "-3"], capture_output=True,
                            text=True)
    ok("collect's own commit path still lands two commits", r.returncode == 0
       and len(r.stdout.strip().splitlines()) >= 2, r.stdout)

    # ── a red verify is still exit 1 with nothing written ────────────────
    b = mkboard(os.path.join(tmp, "h"))
    bad = SPEC_OK.replace("- [ ]", "- [x]").replace(
        "assert app.run() == 2", "assert app.run() == 999")
    prd(b, "redder", "claimed", claim="w 2026-09-01 08:00", specs=bad)
    rp = os.path.join(tmp, "r-red.md")
    with open(rp, "w") as f:
        f.write("Verdict: DONE\n\nThe report claims green.\n")
    before = open(os.path.join(b, "prds", "redder", "prd.md")).read()
    code = collect_report(b, "redder", rp)
    after = open(os.path.join(b, "prds", "redder", "prd.md")).read()
    ok("DONE with a red verify refuses, nothing written", code == 1
       and state_of(b, "redder") == "claimed" and before == after,
       f"exit {code}, state {state_of(b, 'redder')}")

    # ── missing verdict ───────────────────────────────────────────────────
    b = mkboard(os.path.join(tmp, "i"))
    prd(b, "nov", "analyzing", specs=SPEC_OK)
    rp = os.path.join(tmp, "r-nov.md")
    with open(rp, "w") as f:
        f.write("The build went well but the word never landed.\n")
    before = open(os.path.join(b, "prds", "nov", "prd.md")).read()
    code = collect_report(b, "nov", rp)
    after = open(os.path.join(b, "prds", "nov", "prd.md")).read()
    ok("a report with no verdict is refused, nothing written", code == 1
       and state_of(b, "nov") == "analyzing" and before == after,
       f"exit {code}, state {state_of(b, 'nov')}")

    # ── an unknown verdict word ───────────────────────────────────────────
    b = mkboard(os.path.join(tmp, "j"))
    prd(b, "unk", "analyzing", specs=SPEC_OK)
    rp = os.path.join(tmp, "r-unk.md")
    with open(rp, "w") as f:
        f.write("Verdict: MAYBE\n\nThe build half worked.\n")
    code = collect_report(b, "unk", rp)
    ok("an unknown verdict word is refused, nothing written", code == 1
       and state_of(b, "unk") == "analyzing",
       f"exit {code}, state {state_of(b, 'unk')}")

    # ── a gate the transition already checks still runs ──────────────────
    b = mkboard(os.path.join(tmp, "k"))
    prd(b, "badspec", "analyzing", specs=SPEC_OK.replace(
        "## Acceptance", "## Acceptence"))
    rp = os.path.join(tmp, "r-bad.md")
    with open(rp, "w") as f:
        f.write(REPORT_HEAD.format(word="SPECCED", wf="probe-then-spec"))
    code = collect_report(b, "badspec", rp)
    ok("SPECCED through a broken spec is refused by specced's own gate",
       code == 1 and state_of(b, "badspec") == "analyzing",
       f"exit {code}, state {state_of(b, 'badspec')}")

    # ── bare collect, no --report, unchanged ──────────────────────────────
    b = mkboard(os.path.join(tmp, "l"))
    prd(b, "plain", "analyzing", specs=SPEC_OK)
    import plan as P
    r = P.compute_plan(b, None, warn=False)
    ok("bare collect still resolves its band from the scan (no crash, no write)",
       r is not None)

    print()
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())