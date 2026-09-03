#!/usr/bin/env python3
"""The one writer and the one reader of Obsidian's vault register.

    obsidian_register.py open
    obsidian_register.py has <vault>
    obsidian_register.py status <vault>
    obsidian_register.py write <vault> [--retire <path>] [--even-if-running]
    obsidian_register.py repair <path> [--even-if-running]
    obsidian_register.py self-check

Obsidian keeps every vault it can open in one JSON file. `obsidian://open`
resolves against that file and nothing else: a folder with no entry does not
open, it silently lands in whichever registered vault is its ancestor. So
every part of pearde that offers a `▸vault` link — the status line, the
doctor row, `pearde vault`, `pearde init`, `graph.sh open` — depends on what
this file says, and used to re-derive the same four rules from the source
each time it was touched. The four rules are here, once, and nothing outside
this module opens the file:

**1 — the write only survives while the app is closed.** Obsidian loads the
register once at launch and rewrites it *from memory* when it quits. An
entry added underneath a running app is not read by that app (the URI
answers "Unable to find a vault for the URL") and is then erased on quit.
The order that works is: quit, write, launch. `write()` therefore refuses
while the app runs, and a caller that means to write anyway — because it
prints its own warning that the entry will be erased, which `pearde init`
and `pearde upgrade` both do — says so with `even_if_running=True`. The
quit-and-wait loop is *not* here: waiting is a user-facing interaction with
a timeout and a printed line, which belongs to the `vault` verb, not to a
register writer.

**2 — the home directory is resolved from passwd, not only from `$HOME`.**
`doctor.sh` runs under hooks and CI shells that export no `HOME` at all.
`os.path.expanduser("~")` in such a shell returns the passwd home on POSIX,
but an *empty* `HOME` (set and blank) makes it return the empty string
instead, and a bare `~` is what bash leaves behind when it cannot resolve
one. `home()` treats unset and empty alike and falls back to
`pwd.getpwuid(os.getuid()).pw_dir`. `None` from it is the real fourth
answer a doctor row needs — `no-home` — not something to paper over with
the current directory.

**3 — the precedence inside the home is macOS, then `XDG_CONFIG_HOME`, then
`~/.config`.** In that order, and the macOS path wins only when the file is
actually there: a mac with Obsidian installed has
`~/Library/Application Support/obsidian/obsidian.json`, and a Linux box has
one under the XDG root. `candidates()` is the list; `path()` is the first
entry that exists. An empty candidate list means no home — see rule 2 — and
a non-empty list with no file on disk means Obsidian was never installed
here, which is not a fault.

**4 — a compat symlink's name is not the vault's name.** Obsidian names a
vault for the folder it is registered under, and the board carried a dot in
its name until 2026-09-02, so a vault registered at the old root is called
`.pearde` and shows nothing. Moving the vault means dropping the old entry
in the same write as the new one — Obsidian forgets a vault, it never
deletes one, so nothing on disk is touched. That is `write(..., retire=...)`
as one atomic read-modify-write. `repair()` is the same drop, standalone,
for a caller fixing a stale entry without registering a new one in the
same breath.

Every path comparison here is by `os.path.realpath`, because a register
entry, the caller's spelling and the vault's own root can each traverse a
different symlink to the same directory.

Python 3 stdlib only.
"""
import json
import os
import pwd
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE if os.path.isfile(os.path.join(HERE, "pearde_path.py"))
                else os.path.dirname(HERE))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import edit as editlib          # noqa: E402 — the one writer of bytes

# macOS names the process `Obsidian`, Linux `obsidian`.
PROCESS_NAMES = ("Obsidian", "obsidian")


# ── where the register is ─────────────────────────────────────────────────────

def home():
    """This shell's home directory, or `None` when there is none to find.
    Rule 2: `$HOME` when it is set and not empty, else the passwd entry for
    this uid. `None` is a real answer — a uid with no passwd row gets it —
    and the caller reports it rather than guessing a directory."""
    h = os.environ.get("HOME") or ""
    if not h or h == "~":
        try:
            h = pwd.getpwuid(os.getuid()).pw_dir or ""
        except (KeyError, OSError):
            h = ""
    return h or None


def candidates(home_dir=None):
    """Every place the register could be, in precedence order — rule 3. Empty
    when there is no home and no `XDG_CONFIG_HOME`, which is the `no-home`
    answer. `home_dir` overrides the lookup, which is how the self-check runs
    against a scratch home without touching the real one."""
    h = home_dir if home_dir is not None else home()
    out = []
    if h:
        out.append(os.path.join(h, "Library", "Application Support",
                                "obsidian", "obsidian.json"))
    xdg = os.environ.get("XDG_CONFIG_HOME") or ""
    if xdg:
        out.append(os.path.join(xdg, "obsidian", "obsidian.json"))
    elif h:
        out.append(os.path.join(h, ".config", "obsidian", "obsidian.json"))
    return out


def path(home_dir=None):
    """The register file, or `None` when Obsidian has never written one here.
    The first candidate that exists — a machine that never ran the app has
    no file, and that is not a fault."""
    return next((c for c in candidates(home_dir) if os.path.isfile(c)), None)


# ── reading it ────────────────────────────────────────────────────────────────

def open_(home_dir=None):
    """`(register path, parsed document)`, or `(None, None)`. The one place
    the file is opened and parsed; a truncated or half-written register reads
    as absent rather than raising, because every caller's next move is the
    same either way."""
    cfg = path(home_dir)
    if not cfg:
        return None, None
    try:
        with open(cfg, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None, None
    if not isinstance(data, dict):
        return None, None
    return cfg, data


def read(home_dir=None):
    """The `vaults` mapping — `{id: {"path": …, "ts": …}}` — `{}` when there
    is no register or it holds none. What every reader wants."""
    _, data = open_(home_dir)
    vaults = (data or {}).get("vaults") or {}
    return vaults if isinstance(vaults, dict) else {}


def has(vault, home_dir=None):
    """The id `vault` is registered under, else `None`. By realpath, so a
    caller's spelling and the register's own need not match byte for byte."""
    want = os.path.realpath(vault)
    return next((vid for vid, entry in read(home_dir).items()
                 if isinstance(entry, dict)
                 and os.path.realpath(str(entry.get("path", ""))) == want),
                None)


def status(vault, home_dir=None):
    """The four-state answer a doctor row wants, as one word or two:

    - `no-home` — rule 2: no `$HOME`, no passwd entry, no XDG root. The row
      could not perform its check, which is not the same as failing it.
    - `not-installed` — a home, but no register file: Obsidian was never run
      here, so there is nothing to register with.
    - `registered <id>` — an entry names this exact path.
    - `not-registered` — Obsidian is here and this path is not in it.
    """
    cands = candidates(home_dir)
    if not cands:
        return "no-home"
    if not any(os.path.isfile(c) for c in cands):
        return "not-installed"
    vid = has(vault, home_dir)
    return f"registered {vid}" if vid else "not-registered"


def running():
    """Is the app holding its vault list in memory right now — rule 1.
    Neither process name found, or no `pgrep` on this machine, reads as not
    running: the safe answer, since the caller only ever uses it to decide
    whether to warn or to hold off."""
    for name in PROCESS_NAMES:
        try:
            if subprocess.run(["pgrep", "-x", name],
                              capture_output=True).returncode == 0:
                return True
        except OSError:
            return False
    return False


# ── writing it ────────────────────────────────────────────────────────────────

def write(vault, retire=None, even_if_running=False, home_dir=None,
          is_running=None):
    """Register `vault`, dropping `retire`'s entry in the same atomic write.

    A fresh 16-hex id, the absolute path, a millisecond timestamp — the shape
    Obsidian writes itself. An entry with the same path is kept as it is, so
    calling this twice is calling it once. `retire` is rule 4: the vault's
    old root, dropped in the same read-modify-write, never dropped when it
    resolves to the vault being added.

    Refuses while Obsidian runs — rule 1 — returning `("running", None)`
    without touching the file. A caller that has already told the user the
    entry will be erased on quit passes `even_if_running=True` and gets the
    write. `is_running` overrides the probe, for a test that must not depend
    on what is open on the machine running it.

    Returns `("added", id)`, `("known", id)`, `("running", None)`, or
    `(None, None)` when Obsidian has no register on this machine.
    """
    if not even_if_running:
        live = running() if is_running is None else is_running
        if live:
            return "running", None
    cfg, data = open_(home_dir)
    if not cfg:
        return None, None
    vaults = data.setdefault("vaults", {})
    dropped = _drop(vaults, retire, keep=vault)
    known = has(vault, home_dir)
    if known:
        if dropped:
            editlib.write_atomic(cfg, json.dumps(data))
        return "known", known
    vid = os.urandom(8).hex()
    vaults[vid] = {"path": vault, "ts": int(time.time() * 1000)}
    editlib.write_atomic(cfg, json.dumps(data))
    return "added", vid


def repair(retire, even_if_running=False, home_dir=None, is_running=None):
    """Drop `retire`'s entry and register nothing — the retire-only half of
    `write()`, for a caller fixing a stale entry on its own. Same refusal
    while the app runs, same reason. Returns the list of ids dropped: empty
    when there was nothing to drop, and the file is then left untouched."""
    if not even_if_running:
        live = running() if is_running is None else is_running
        if live:
            return None
    cfg, data = open_(home_dir)
    if not cfg:
        return None
    vaults = data.setdefault("vaults", {})
    dropped = _drop(vaults, retire)
    if dropped:
        editlib.write_atomic(cfg, json.dumps(data))
    return dropped


def _drop(vaults, retire, keep=None):
    """Remove every entry whose path resolves to `retire` and return their
    ids. `keep` is never dropped, however it is spelled — `write()` passes
    the vault it is about to add, so retiring a path onto itself is a no-op
    rather than a register that loses the entry it just made."""
    if not retire:
        return []
    want = os.path.realpath(retire)
    if keep is not None and os.path.realpath(keep) == want:
        return []
    gone = [vid for vid, entry in vaults.items()
            if isinstance(entry, dict)
            and os.path.realpath(str(entry.get("path", ""))) == want]
    for vid in gone:
        del vaults[vid]
    return gone


# ── the command line, so a shell reads the register the same way ──────────────

def _self_check():
    """Drive every rule against a scratch home under one temp directory. No
    real Obsidian install is read and none is written: `home_dir=` takes the
    passwd fallback out of the picture entirely, and `is_running=` mocks
    rule 1 rather than depending on what is open on this machine."""
    import tempfile
    ok = []

    def check(label, cond):
        ok.append((label, bool(cond)))

    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "home")
        cfg = os.path.join(h, "Library", "Application Support", "obsidian",
                           "obsidian.json")
        os.makedirs(os.path.dirname(cfg))
        vault = os.path.join(tmp, "proj")
        old = os.path.join(tmp, "proj", ".pearde")
        os.makedirs(old)

        # rule 3 — the macOS path leads the candidate list, and an empty home
        # is the `no-home` answer rather than a guess.
        check("path precedence names the macOS register first",
              candidates(h)[0] == cfg)
        check("no home and no XDG is no candidate at all",
              candidates("") == [] or os.environ.get("XDG_CONFIG_HOME"))

        # no register file yet: not-installed, and nothing to read.
        check("no register file reads as not-installed",
              status(vault, home_dir=h) == "not-installed")
        check("no register file reads as no vaults", read(home_dir=h) == {})

        # seed one, holding only the superseded entry — rule 4's setup.
        with open(cfg, "w", encoding="utf-8") as fh:
            json.dump({"vaults": {"0badc0de": {"path": old, "ts": 1}}}, fh)
        check("a seeded register reads as not-registered",
              status(vault, home_dir=h) == "not-registered")

        # rule 1 — the app is running, so the write is refused and the file
        # is byte-for-byte what it was.
        before = open(cfg, encoding="utf-8").read()
        state, vid = write(vault, retire=old, home_dir=h, is_running=True)
        check("write refuses while Obsidian runs", (state, vid) == ("running", None))
        check("a refused write leaves the register untouched",
              open(cfg, encoding="utf-8").read() == before)
        check("a refused write registered nothing",
              has(vault, home_dir=h) is None)
        check("repair refuses while Obsidian runs too",
              repair(old, home_dir=h, is_running=True) is None)

        # the app is closed: the write lands, and rule 4's retire lands with
        # it in the same read-modify-write.
        state, vid = write(vault, retire=old, home_dir=h, is_running=False)
        check("write adds the vault once Obsidian is closed", state == "added")
        check("the write reads back by exact path",
              vid and has(vault, home_dir=h) == vid)
        check("the retired entry is gone in the same write",
              "0badc0de" not in read(home_dir=h))
        check("the register now holds exactly one vault",
              len(read(home_dir=h)) == 1)
        check("a registered vault reads as registered",
              status(vault, home_dir=h) == f"registered {vid}")

        # writing the same vault again is writing it once.
        state2, vid2 = write(vault, home_dir=h, is_running=False)
        check("a second write keeps the entry it found",
              (state2, vid2) == ("known", vid))

        # rule 4 — retiring the vault onto itself never drops it.
        state3, vid3 = write(vault, retire=vault, home_dir=h, is_running=False)
        check("retiring a vault onto itself keeps it",
              (state3, vid3) == ("known", vid) and has(vault, home_dir=h) == vid)

        # repair alone: drop a stale entry, register nothing.
        stale = os.path.join(tmp, "gone")
        os.makedirs(stale)
        data = json.load(open(cfg, encoding="utf-8"))
        data["vaults"]["deadbeef"] = {"path": stale, "ts": 2}
        with open(cfg, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        check("repair drops the entry it names",
              repair(stale, home_dir=h, is_running=False) == ["deadbeef"])
        check("repair registered nothing of its own",
              list(read(home_dir=h)) == [vid])
        check("repair with nothing to drop is a no-op",
              repair(stale, home_dir=h, is_running=False) == [])

    for label, good in ok:
        print(f"  {'ok  ' if good else 'FAIL'}  {label}")
    bad = [label for label, good in ok if not good]
    print(f"{len(ok)} checks · {len(ok) - len(bad)} pass · {len(bad)} fail")
    return 1 if bad else 0


def main(argv):
    if not argv:
        print(__doc__.split("\n\n")[0], file=sys.stderr)
        return 2
    verb, rest = argv[0], argv[1:]
    even = "--even-if-running" in rest
    rest = [a for a in rest if a != "--even-if-running"]
    retire = None
    if "--retire" in rest:
        i = rest.index("--retire")
        if i + 1 >= len(rest):
            print("--retire takes a path", file=sys.stderr)
            return 2
        retire = rest[i + 1]
        rest = rest[:i] + rest[i + 2:]

    if verb == "self-check":
        return _self_check()
    if verb == "open":
        cfg = path()
        if not cfg:
            return 1
        print(cfg)
        return 0
    if not rest:
        print(f"{verb} takes a path", file=sys.stderr)
        return 2
    target = rest[0]
    if verb == "has":
        vid = has(target)
        if not vid:
            return 1
        print(vid)
        return 0
    if verb == "status":
        print(status(target))
        return 0
    if verb == "write":
        state, vid = write(target, retire=retire, even_if_running=even)
        print(f"{state or 'none'}{' ' + vid if vid else ''}")
        return 0 if state in ("added", "known") else 1
    if verb == "repair":
        gone = repair(target, even_if_running=even)
        if gone is None:
            print("running")
            return 1
        print(" ".join(gone))
        return 0
    print(f"no verb `{verb}` — open, has, status, write, repair, self-check",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
