"""the daemon must not write into a board path it no longer owns — the probe.

Every check is a write that must not happen. Fixtures are made at run time
under FIXROOT (the repo root, not /tmp: `serve.EPHEMERAL` turns `save_entry`
into a no-op under /tmp, which would hide the very write being measured) and
removed on the way out.
"""
import os, shutil, sys, tempfile

# The tree under test is the runner's when it names one — a worker builds in
# a lane and this file only ever sits in the orchestrator's checkout.
BOARD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.environ.get("PEARDE_ROOT") or os.path.dirname(BOARD)
sys.path.insert(0, os.path.join(ROOT, "resources", "board"))
import plan as planlib                                   # noqa: E402
os.environ.setdefault("PEARDE_SERVE_PORT", "8999")
import serve as servelib                                 # noqa: E402

FIXROOT = os.path.join(ROOT, ".probe-daemon-path")


def fresh_project():
    os.makedirs(FIXROOT, exist_ok=True)
    return tempfile.mkdtemp(prefix="proj-", dir=FIXROOT)


FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" · " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


def call(fn, *a):
    """Run it and report how it declined — `die()` raises SystemExit, which is
    not an Exception and so escapes every `except Exception` on the board."""
    try:
        return fn(*a), None
    except BaseException as e:                            # noqa: BLE001
        return None, e


# 1 — state_dir must not conjure a board that is not on disk at all
proj = fresh_project()
gone = os.path.join(proj, ".pearde")                      # the migrated-away name
_, err = call(planlib.state_dir, gone)
check("state_dir does not conjure a board directory", not os.path.isdir(gone),
      f"declined with {type(err).__name__ if err else 'nothing'}")

# 2 — state_dir must not write into a husk: a directory at the old name that
#     carries no board. This is the state the defect leaves behind, so a fix
#     that only tests isdir() cannot heal a repo it has already touched.
proj = fresh_project()
husk = os.path.join(proj, ".pearde")
os.makedirs(husk)
_, err = call(planlib.state_dir, husk)
check("state_dir refuses a directory that carries no board",
      not os.path.isdir(os.path.join(husk, planlib.STATE_DIR)),
      f"declined with {type(err).__name__ if err else 'nothing'}")

# 3 — how it declines: an OSError the daemon's writers already catch, never a
#     SystemExit, which kills the watch thread instead of skipping one board
proj = fresh_project()
_, err = call(planlib.state_dir, os.path.join(proj, ".pearde"))
check("state_dir declines with an OSError, not a SystemExit",
      isinstance(err, OSError), f"raised {type(err).__name__}")

# 4 — save_entry on a stale in-memory path must not re-create the old name
proj = fresh_project()
os.makedirs(os.path.join(proj, "pearde", "prds"))         # the board, migrated
stale = os.path.join(proj, ".pearde")                     # where it used to be
_, err = call(servelib.save_entry, servelib.Board(stale))
check("save_entry does not re-create a board at a path it no longer owns",
      not os.path.isdir(stale),
      f"declined with {type(err).__name__ if err else 'nothing'}")
check("save_entry declines without raising", err is None,
      f"raised {type(err).__name__}" if err else "")

# 5 — drop_entry removes without creating
proj = fresh_project()
absent = os.path.join(proj, ".pearde")
_, err = call(servelib.drop_entry, servelib.Board(absent))
check("drop_entry does not create the board directory",
      not os.path.isdir(absent),
      f"declined with {type(err).__name__ if err else 'nothing'}")

# 6 — the watch set drops a board whose path no longer carries a board, husk
#     included, so the daemon stops polling what it cannot resolve
proj = fresh_project()
husk = os.path.join(proj, ".pearde")
os.makedirs(os.path.join(husk, ".state"))                 # what the defect left
live = os.path.join(proj, "pearde")
os.makedirs(os.path.join(live, "prds"))
with servelib.BOARDS_LOCK:
    servelib.BOARDS.clear()
    b = servelib.Board(husk)
    servelib.BOARDS[b.name] = b
left, err = call(servelib.vanished)
check("the watch set drops a path that carries no board",
      not any(x.path == husk for x in servelib.boards()),
      f"{left} left, declined with {type(err).__name__ if err else 'nothing'}")

# 7 — nothing above may cost a live board its .state
proj = fresh_project()
real = os.path.join(proj, "pearde")
os.makedirs(os.path.join(real, "prds"))
sd, err = call(planlib.state_dir, real)
check("state_dir still makes .state inside a real board",
      bool(sd) and os.path.isdir(sd), str(err or sd))
b = servelib.Board(real)
_, err = call(servelib.save_entry, b)
check("save_entry still records a real board",
      os.path.isfile(os.path.join(real, ".state", "serve.json")),
      str(err or ""))
_, err = call(servelib.drop_entry, b)
check("drop_entry still removes a real board's marker",
      not os.path.exists(os.path.join(real, ".state", "serve.json")),
      str(err or ""))

shutil.rmtree(FIXROOT, ignore_errors=True)
print(f"\n{len(FAILS)} failing · {'FAILED' if FAILS else 'OK'}")
sys.exit(1 if FAILS else 0)
