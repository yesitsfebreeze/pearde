#!/usr/bin/env python3
"""Build a throwaway board holding the three `needs:` shapes, in a directory
made at run time. Never under `.pearde/prds/` — a dir holding prd.md there is
a PRD. Prints the board path."""
import os, shutil, subprocess, sys, tempfile

SETTINGS = """---
name: probeboard
language: English
workers: 0
pipeline: 0
weight-default: 20
gantt-day: 8h
---

# probeboard
"""

PRDS = {
    # the control: nothing in its way
    "plain": ("---\nstate: open\norigin: requested\npriority: 60\n---\n\n"
              "# plain — no needs at all\n\nThe control row.\n"),
    # the contract's case: a qualified need naming a board not in this scan
    "crossboard": ("---\nstate: open\norigin: requested\npriority: 60\n"
                   "needs:\n  - '@other/thing'\n---\n\n"
                   "# crossboard — needs a board this scan does not hold\n\n"
                   "A member PRD worked on its own board.\n"),
    # the typo case: a bare name matching nothing anywhere
    "typo": ("---\nstate: open\norigin: requested\npriority: 60\n"
             "needs:\n  - nosuchprd\n---\n\n"
             "# typo — needs a name no board holds\n\nA misspelling.\n"),
    # a real, unmet local need
    "local": ("---\nstate: open\norigin: requested\npriority: 60\n"
              "needs:\n  - plain\n---\n\n"
              "# local — needs a sibling that is not done\n\nA real edge.\n"),
}


def build(root=None):
    root = root or tempfile.mkdtemp(prefix="xboard-probe-")
    board = os.path.join(root, ".pearde")
    prds = os.path.join(board, "prds")
    os.makedirs(prds, exist_ok=True)
    with open(os.path.join(board, "settings.md"), "w") as f:
        f.write(SETTINGS)
    for name, body in PRDS.items():
        d = os.path.join(prds, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "prd.md"), "w") as f:
            f.write(body)
    subprocess.run(["git", "init", "-q", root], check=True)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True)
    subprocess.run(["git", "-C", root, "-c", "user.email=p@p", "-c",
                    "user.name=probe", "commit", "-qm", "probe board"],
                   check=True)
    return board


MASTER_SETTINGS = """---
name: masterboard
language: English
workers: 0
pipeline: 0
weight-default: 20
gantt-day: 8h
members:
  - ../../member/.pearde
---

# masterboard
"""

MASTER_PRDS = {
    # the member board IS in the scan and holds this PRD — a real edge
    "resolves": ("---\nstate: open\norigin: requested\npriority: 60\n"
                 "needs:\n  - '@member/real'\n---\n\n"
                 "# resolves — a qualified need the master can see\n"),
    # the member board IS in the scan and holds no such PRD — a typo, held
    "membertypo": ("---\nstate: open\norigin: requested\npriority: 60\n"
                   "needs:\n  - '@member/nope'\n---\n\n"
                   "# membertypo — a qualified need into a board that is here\n"),
    # a board no member declares — ignored
    "absent": ("---\nstate: open\norigin: requested\npriority: 60\n"
               "needs:\n  - '@elsewhere/thing'\n---\n\n"
               "# absent — a qualified need into a board that is not here\n"),
    # the master's own name — its own board, so a missing PRD is a typo, held
    "ownname": ("---\nstate: open\norigin: requested\npriority: 60\n"
                "needs:\n  - '@masterboard/nope'\n---\n\n"
                "# ownname — a qualified need under the master's own name\n"),
}

MEMBER_PRDS = {
    "real": ("---\nstate: open\norigin: requested\npriority: 60\n---\n\n"
             "# real — the PRD the master's qualified need names\n"),
}


def _write(prds_dir, table):
    for name, body in table.items():
        d = os.path.join(prds_dir, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "prd.md"), "w") as f:
            f.write(body)


def build_master(root=None):
    """A master merging one member, in a directory made at run time. Returns
    the master's `.pearde/`."""
    root = root or tempfile.mkdtemp(prefix="xboard-master-")
    master = os.path.join(root, "master", ".pearde")
    member = os.path.join(root, "member", ".pearde")
    for b, settings, table in ((master, MASTER_SETTINGS, MASTER_PRDS),
                               (member, SETTINGS.replace("probeboard",
                                                         "member"),
                                MEMBER_PRDS)):
        os.makedirs(os.path.join(b, "prds"), exist_ok=True)
        with open(os.path.join(b, "settings.md"), "w") as f:
            f.write(settings)
        _write(os.path.join(b, "prds"), table)
    for r in (os.path.join(root, "master"), os.path.join(root, "member")):
        subprocess.run(["git", "init", "-q", r], check=True)
        subprocess.run(["git", "-C", r, "add", "-A"], check=True)
        subprocess.run(["git", "-C", r, "-c", "user.email=p@p", "-c",
                        "user.name=probe", "commit", "-qm", "probe"],
                       check=True)
    return master


if __name__ == "__main__":
    print(build())
    print(build_master())
