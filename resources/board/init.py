#!/usr/bin/env python3
"""pearde init — a board exists after one command, and it asked nothing.

    init.py init [<dir>] [--language <l>] [--name <n>] [--example] [--dry]
    init.py settings <key>=<value> [--board <path>] [--dry]

`init` leaves `<dir>/.pearde/` (default: the working directory) on the
contract: a `settings.md` naming the five knobs by name, a `vision.md` from
@references/templates/vision.md with `terminals:` commented out, the three
machine-local names in `.gitignore` when `<dir>` is inside a git repo, the
daemon up and watching the board when the port can be bound — it says so and
goes on when it cannot — and one `doctor` report, every line printed. Then
four lines: `pearde guard on — optional, …` for the hook doctor's guard row
names, the URL, `pearde add "<title>"`, `pearde`. Its first line says
the language it defaulted and the command that changes it. `--example`
copies the example board instead of writing an empty one — the quickstart's.

Idempotent: on a board that already has `settings.md` nothing is written and
the same four lines close the output. `prds/`, `memos/`, `wiki/`,
`workflows/` and `.state/` are made empty on the first run regardless —
the five a board has even with nothing in them yet.

`settings` writes one key of `.pearde/settings.md` through edit.py — one
frontmatter line, every other line byte for byte — and is how any key is
set, `workers=N` and `pipeline=N` included.

Both declare their flags in `FLAGS` and parse through transitions.py `Args`:
an undeclared flag is refused with the list, exit 2, before anything is
read. `--dry` prints the first line the run would print, `dry ·` in front,
and the paths it would write — and starts no daemon, runs no doctor.

`COMMANDS` is what the dispatcher discovers. Each entry takes the argument
list after the command name and returns the exit code. Python 3 stdlib only.
"""
import os
import json
import re
import shutil
import subprocess
import time
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(HERE)                          # the skill's resources/
SKILL = os.path.dirname(RES)
sys.path.insert(0, HERE)
import edit as editlib          # noqa: E402 — the one writer of bytes
import plan as planlib          # noqa: E402 — every read
import transitions as trlib     # noqa: E402 — the flag parser

EXAMPLE = os.path.join(HERE, "example")   # the seed board
VISION_TEMPLATE = os.path.join(SKILL, "references", "templates", "vision.md")
SERVE = os.path.join(HERE, "serve.py")
DOCTOR = os.path.join(RES, "doctor.sh")

# The five knobs of @references/settings.md, in the order the file shows
# them, every one written by name so a reader sees the choice on disk.
DEFAULTS = (("language", "English"), ("workers", "3"), ("pipeline", "3"),
            ("weight-default", "50"), ("gantt-day", "8h"))

# Machine-local per board — regenerable. What this repo's own .gitignore
# holds for the same names. `.obsidian/` is the board's own vault config,
# written at `.pearde/.obsidian/` and never shared.
IGNORED = (".pearde/.state/", ".pearde/wiki/", ".obsidian/")

# A board is often its own git repo — the plan on its own branch, pushed. The
# names below are written into *that* repo's `.gitignore`, not the parent's.
# Two of them hold the same live credential — the REST key mirror, and the
# plugin `data.json` inside `.obsidian/` that it mirrors — and a board repo
# that tracks `wiki/` or the vault commits it, to a remote if it has one. The
# other two are machine-local rebuild output that only makes noise in a diff.
# Everything else under `wiki/` — the notes, the dashboard, the indexes — is
# the plan and belongs in the history.
# The machine-local corner joins them: the board's registration with the
# daemon, the daemon's log when this board started it, an adapter run's
# output and the guard's per-session counters all live under `.state/` now
# rather than in the install — the invariant
# `every-artifact-lands-inside-the-board` — and none of them is plan.
BOARD_IGNORED = ("wiki/.obsidian-api-key", "wiki/.graphify/",
                 "wiki/Dashboard.report.md", ".obsidian/",
                 ".state/serve.json", ".state/serve.log", ".state/run-*.log",
                 ".state/guard/", ".state/calibration.json")
BOARD_HEADER = "# machine-local — two hold one credential, the rest rebuild"

# The Obsidian requirement: dataview (the live views) and local-rest-api
# (the port a tool reads the vault through). The preset at
# resources/board/obsidian/ carries the settings; the plugin bundles are not
# vendored — `pearde install --apply` fetches them at pinned versions into
# the preset's plugins/, and this file copies whatever it finds there to
# <dir>/.obsidian when the board's parent is the vault it seeds. A bundle the
# install never fetched is reported, not silently skipped. The REST key is
# minted fresh — one per board, never shipped in the template.
OBSIDIAN_PRESET = os.path.join(HERE, "obsidian")
# `vault --wait` polls for the app to go: half a second apart, ten minutes of
# patience — long enough for a person to finish what they were doing and quit,
# short enough that a forgotten command does not sit there for a session.
WAIT_TICK, WAIT_TICKS = 0.5, 1200
OBSIDIAN_PLUGINS = ("dataview", "obsidian-local-rest-api")

# The knowledge layer's *content* seed — Dashboard.md, WORKFLOW.md, the
# indexes, the empty scaffolds — for `.pearde/wiki/`, the folder the preset
# above points its vault at. `write_knowledge` plants it; `init` and
# `upgrade` both call that. Not the same thing as resources/board/obsidian/:
# that is app configuration, this is vault content. Every path inside these
# files is vault-relative — the vault roots at `.pearde/`, so a KB query
# reads `wiki/conclusions`, never `conclusions`.
KNOWLEDGE_PRESET = os.path.join(HERE, "knowledge")
KNOWLEDGE_PY = os.path.join(HERE, "..", "knowledge.py")
MEMOS_PY = os.path.join(RES, "memos.py")

KEY_RE = re.compile(r"^[a-z][a-z0-9-]*$")


class Refused(Exception):
    """An argument the command cannot act on. Nothing was written."""


# The declaration — transitions.py `Args` is the parser.
FLAGS = {
    "init":     trlib.Flags(("language", "name"), ("example",) + trlib.DRY),
    "settings": trlib.Flags(("board",), trlib.DRY),
    "vault":    trlib.Flags((), ("wait", "open") + trlib.DRY),
    "upgrade":  trlib.Flags((), trlib.DRY),
}


def json_text(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


# ── init ──────────────────────────────────────────────────────────────────────

def settings_text(language, name):
    lines = ["---"]
    if name:
        lines.append(f"name: {name}")
    for k, v in DEFAULTS:
        lines.append(f"{k}: {language if k == 'language' else v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def write_board(board, args):
    """Steps 1–3: the board directory, `settings.md` and `vision.md`. Each
    file is written only when it is not there, so a hand-made `.pearde/` keeps
    what it has and gains what it lacks. Also makes the five directories a
    board has even when empty — `prds/`, `memos/`, `wiki/`, `workflows/`,
    `.state/` — so `scan` and the daemon find them from the first run,
    whether or not `--example` seeded any of them with content."""
    settings = os.path.join(board, "settings.md")
    if "example" in args.flags:
        if os.path.isdir(board) and os.listdir(board):
            raise Refused(f"{board} exists and holds no settings.md — "
                          "--example copies into an empty or missing .pearde/")
        shutil.copytree(EXAMPLE, board, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("README.md"))
        for key in ("language", "name"):
            if args.opt.get(key, "").strip():
                editlib.set_key(settings, key, args.opt[key].strip())
    else:
        os.makedirs(board, exist_ok=True)
        editlib.write_atomic(settings, settings_text(
            args.opt.get("language", "").strip() or "English",
            args.opt.get("name", "").strip()))
    vision = os.path.join(board, "vision.md")
    if not os.path.exists(vision):
        shutil.copyfile(VISION_TEMPLATE, vision)
    for name in (planlib.PRDS_DIR, "memos", "wiki", "workflows",
                 planlib.STATE_DIR):
        os.makedirs(os.path.join(board, name), exist_ok=True)


def in_git(d):
    try:
        p = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
    except OSError:
        return False
    return p.returncode == 0


def obsidian_config():
    """Obsidian's vault register — the file that decides what
    `obsidian://open` can resolve. macOS first, then the Linux/XDG path.
    Returns the path when the app has one, else None: a machine that never
    ran Obsidian gets no file written."""
    candidates = [
        os.path.expanduser("~/Library/Application Support/obsidian/obsidian.json"),
        os.path.join(os.environ.get("XDG_CONFIG_HOME",
                                    os.path.expanduser("~/.config")),
                     "obsidian", "obsidian.json"),
    ]
    return next((c for c in candidates if os.path.isfile(c)), None)


def obsidian_running():
    """Is the app holding its vault list in memory right now. macOS names the
    process `Obsidian`, Linux `obsidian`; neither found (or no pgrep) reads as
    not running, which is the safe answer — the caller only ever uses it to
    decide whether to warn."""
    for name in ("Obsidian", "obsidian"):
        try:
            if subprocess.run(["pgrep", "-x", name],
                              capture_output=True).returncode == 0:
                return True
        except OSError:
            return False
    return False


def register_vault(vault):
    """Step 4c: the register. `obsidian://open` resolves against the vaults
    Obsidian already knows — an unregistered folder does not open, it silently
    lands in whichever registered vault is its ancestor (the repo root, on a
    board whose repo is itself a vault). So the board is written into
    `obsidian.json` here: a fresh 16-hex id, its absolute path, a timestamp.
    An entry with the same path is kept as it is.

    **A write only survives while the app is closed.** Obsidian loads this
    file once at launch and rewrites it *from memory* when it quits — an entry
    added underneath a running app is not read by that app (the URI answers
    "Unable to find a vault for the URL") and is then erased on quit. The
    order that works is: quit, write, launch. `cmd_vault` is that order, and
    `--wait` does the writing the moment the process goes.

    Returns ("added", id), ("known", id), or (None, None) when Obsidian has
    no config on this machine."""
    cfg = obsidian_config()
    if not cfg:
        return None, None
    try:
        data = json.load(open(cfg, encoding="utf-8"))
    except (OSError, ValueError):
        return None, None
    vaults = data.setdefault("vaults", {})
    for vid, entry in vaults.items():
        if os.path.realpath(str(entry.get("path", ""))) == os.path.realpath(vault):
            return "known", vid
    vid = os.urandom(8).hex()
    vaults[vid] = {"path": vault, "ts": int(time.time() * 1000)}
    editlib.write_atomic(cfg, json.dumps(data))
    return "added", vid


def write_obsidian(d):
    """Step 4b: the vault, and it roots at the board. `<dir>/.pearde/.obsidian/`
    — not `<dir>/.obsidian/`: Obsidian hides a dot-directory *inside* a vault,
    so a vault at the repo root cannot show `.pearde/` at all, while a vault
    whose own root is `.pearde/` shows every one of its children. Every
    vault-relative path the board writes — the Dataview sources, the generated
    wikilinks — is written against this root.

    Copies the vendored preset and plugins in — dataview,
    obsidian-local-rest-api, the graph and app configuration — and mints a
    fresh REST key into the plugin's data.json, mirrored at
    `.pearde/wiki/.obsidian-api-key` where the loop's tools read it. Everything
    already there is kept (a hand-tuned vault wins). A plugin whose bundle is
    not in the preset — the install has not run, or could not reach the
    network — is returned in the second list and named on the console, because
    a vault missing dataview renders no view at all.
    Returns (installed, missing, key)."""
    vault = os.path.join(d, ".pearde")
    dest = os.path.join(vault, ".obsidian")
    plugins, missing = [], []
    if not os.path.isdir(OBSIDIAN_PRESET):
        return [], list(OBSIDIAN_PLUGINS), None
    os.makedirs(dest, exist_ok=True)
    for entry in sorted(os.listdir(OBSIDIAN_PRESET)):
        src = os.path.join(OBSIDIAN_PRESET, entry)
        dst = os.path.join(dest, entry)
        if entry == "plugins":
            for plugin in OBSIDIAN_PLUGINS:
                src_p = os.path.join(src, plugin)
                dst_p = os.path.join(dst, plugin)
                if os.path.isdir(os.path.join(dest, "plugins", plugin)):
                    continue                      # already installed wins
                if not os.path.isfile(os.path.join(src_p, "main.js")):
                    missing.append(plugin)        # install never fetched it
                    continue
                shutil.copytree(src_p, dst_p, dirs_exist_ok=True)
                plugins.append(plugin)
        elif not os.path.exists(dst):
            shutil.copyfile(src, dst)
    # the key: fresh per board, in the v5 schema the plugin reads, both
    # where the plugin reads it and where a tool looks it up
    key = os.urandom(24).hex()
    cfg = {"port": 27124, "insecurePort": 27123, "enableInsecureServer": False,
           "apiKey": key}
    # The key is written beside the plugin's own bundle, and the bundle is not
    # vendored — a machine that never ran `install --apply` has no plugin dir
    # at all (the loop above reported it into `missing`). Writing the key
    # cannot create the directory it belongs to and crash init: makedirs, and
    # the key lands whenever the bundle later arrives.
    cfg_path = os.path.join(dest, "plugins",
                            "obsidian-local-rest-api", "data.json")
    if os.path.exists(cfg_path):
        try:                              # the plugin's own key wins
            key = json.load(open(cfg_path, encoding="utf-8"))["apiKey"]
        except (OSError, ValueError, KeyError):
            pass
    else:
        os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
        editlib.write_atomic(cfg_path, json_text(cfg))
    # The mirror follows the plugin, never the other way round: a key that
    # disagrees with data.json is a 401 on every call, and the file a tool
    # reads is the one that has to be wrong-proof. Rewritten whenever it
    # differs — including a mirror left behind by an older vault root.
    key_path = os.path.join(d, ".pearde", "wiki", ".obsidian-api-key")
    have = ""
    if os.path.exists(key_path):
        have = open(key_path, encoding="utf-8").read().strip()
    if have != key:
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        editlib.write_atomic(key_path, key + "\n")
    return plugins, missing, key


def write_knowledge(d):
    """The knowledge layer's content, seeded into `<dir>/.pearde/wiki/`.

    `knowledge.py`'s Store makes the directories on first use but writes no
    Dashboard and no WORKFLOW — a board that never had them opens in Obsidian
    with no views at all, which is what a fresh vault looked like before this
    step existed. Copies every file of the preset that is not already there;
    a file a person edited is never replaced. Returns the vault-relative
    names it planted."""
    wiki = os.path.join(d, ".pearde", "wiki")
    planted = []
    if not os.path.isdir(KNOWLEDGE_PRESET):
        return planted
    for src_dir, _dirs, files in os.walk(KNOWLEDGE_PRESET):
        rel = os.path.relpath(src_dir, KNOWLEDGE_PRESET)
        dst_dir = wiki if rel == "." else os.path.join(wiki, rel)
        os.makedirs(dst_dir, exist_ok=True)
        for name in sorted(files):
            if name == ".DS_Store":
                continue
            dst = os.path.join(dst_dir, name)
            if os.path.exists(dst):
                continue
            shutil.copyfile(os.path.join(src_dir, name), dst)
            planted.append(os.path.relpath(dst, wiki))
    # the two the Store makes but the preset carries no file for
    for name in ("sources", "conclusions", "pending", "graphs"):
        os.makedirs(os.path.join(wiki, name), exist_ok=True)
    return planted


def index_memos(board):
    """Regenerate `memos/README.md`, the index by kind, after a copy.

    `--example` copies the example board through
    `shutil.ignore_patterns("README.md")`, and that pattern is matched in
    every directory the walk enters, not only the top one. It is there to
    drop the example board's own README — the page describing the example to
    a reader — and it drops `memos/README.md` with it. The board that lands
    therefore holds a memo and no index, which is exactly what `memo check`
    calls stale and what doctor's `memos` row reports as broken on a board
    one command old.

    Teaching the copy to keep that one file is the wrong repair: the index is
    generated, `memo add` rewrites it, and a copied one would be right only
    until the first memo. Generating it after the copy is the same answer
    `upgrade` gives for the knowledge graph — plant, then regenerate.

    Runs only when the board holds a memo, so an empty board still lands with
    an empty `memos/` and no generated page in it. Returns the relative path
    written, or None.

    When `memos.py index` cannot write the page — an unwritable board, a
    memo it chokes on — the failure is *said*, not swallowed. A board that
    holds memos and no index is one doctor calls broken on the next line, so
    a bare `return None` there is `init` exiting 0 having quietly not done
    the thing it was asked for. Nothing on the happy path changes.
    """
    d = os.path.join(board, "memos")
    if not os.path.isdir(d):
        return None
    if not any(f.endswith(".md") and f != "README.md"
               for f in os.listdir(d)):
        return None
    out = subprocess.run([sys.executable, os.path.abspath(MEMOS_PY),
                          "index", board], capture_output=True, text=True)
    written = out.stdout.strip().splitlines()
    if out.returncode != 0 or not written:
        why = (out.stderr.strip().splitlines() or written
               or ["no output"])[-1]
        print(f"init: could not regenerate memos/README.md, the memo index "
              f"by kind — {why} · the board holds memos and no index, which "
              "doctor reads as stale; run `memo index` once that is fixed")
        return None
    return os.path.relpath(written[-1], board)


def plant_graph(board):
    """`knowledge.py board`, then `relink` — the two verbs `upgrade` runs.

    `write_knowledge` plants the layer's *files*; neither verb runs there, so
    a board that has only been through `init` has notes and no
    `.graphify/graph.json`, and `knowledge.py doctor` reports `graph.json
    missing — run relink`, which doctor's `knowledge` row reports as broken.
    `upgrade` has always ended on these two verbs; `init` did not, so the one
    command a newcomer runs left the layer half-planted.

    `board` writes the generated PRD and memo notes, `relink` builds the
    graph over what is on disk — so the order is fixed, and both run after
    `index_memos`, since `board` reads the memos it indexes. Returns one
    `(verb, first line)` pair per verb, for the caller to print or drop.
    """
    lines = []
    for verb in ("board", "relink"):
        out = subprocess.run(
            [sys.executable, os.path.abspath(KNOWLEDGE_PY),
             "--root", os.path.join(board, "wiki"), verb],
            capture_output=True, text=True)
        line = (out.stdout.strip().splitlines() or
                out.stderr.strip().splitlines() or ["no output"])[0]
        lines.append((verb, line))
    return lines


def repair_plugin_ids(dest):
    """Obsidian enables a community plugin by its manifest id, and a list
    holding a name that is not one enables nothing and reports nothing. An
    early preset spelled the REST plugin `local-rest-api`; its id is
    `obsidian-local-rest-api`, so every vault seeded from it came up with the
    port closed. Rewrites only the ids this repo ships — a plugin someone
    else added is left exactly where it is. Returns what it changed."""
    path = os.path.join(dest, "community-plugins.json")
    if not os.path.isfile(path):
        return []
    try:
        have = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if not isinstance(have, list):
        return []
    fixed, changed = [], []
    for entry in have:
        if entry in OBSIDIAN_PLUGINS or not isinstance(entry, str):
            fixed.append(entry)
            continue
        match = next((p for p in OBSIDIAN_PLUGINS if p.endswith("-" + entry)
                      or entry.endswith("-" + p)), None)
        if match and match not in have:
            fixed.append(match)
            changed.append(f"{entry} -> {match}")
        elif match:
            changed.append(f"dropped duplicate {entry}")
        else:
            fixed.append(entry)
    for plugin in OBSIDIAN_PLUGINS:
        if plugin not in fixed and os.path.isdir(
                os.path.join(dest, "plugins", plugin)):
            fixed.append(plugin)
            changed.append(f"enabled {plugin}")
    if changed:
        editlib.write_atomic(path, json_text(fixed))
    return changed


def write_gitignore(d):
    """Step 4: the machine-local names, appended to `<dir>/.gitignore` — the
    board's parent, where `.pearde/…` is the right spelling — when they are not
    already there. Returns the names it added."""
    path = os.path.join(d, ".gitignore")
    text = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""
    have = {l.strip() for l in text.splitlines()}
    add = [n for n in IGNORED if n not in have]
    if not add:
        return []
    if text and not text.endswith("\n"):
        text += "\n"
    if text:
        text += "\n"
    text += "# machine-local per board — regenerable\n"
    text += "".join(n + "\n" for n in add)
    editlib.write_atomic(path, text)
    return add


def write_board_gitignore(board):
    """The board's own repo, when it is one. Returns the names it added.

    Separate from `write_gitignore`, which writes the *parent* repo's file
    with `.pearde/…`-prefixed names. A board on its own branch never sees
    that file — git does not descend into a nested work tree — so the key
    it holds gets committed and, if the branch has a remote, published."""
    if not os.path.isdir(os.path.join(board, ".git")) and not in_git(board):
        return []
    path = os.path.join(board, ".gitignore")
    text = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""
    have = {l.strip() for l in text.splitlines()}
    add = [n for n in BOARD_IGNORED if n not in have]
    if not add:
        return []
    if text and not text.endswith("\n"):
        text += "\n"
    # the header is written once and then found — a later run adding one more
    # name must not stack a second copy of it under the first
    if BOARD_HEADER not in text:
        if text:
            text += "\n"
        text += BOARD_HEADER + "\n"
    text += "".join(n + "\n" for n in add)
    editlib.write_atomic(path, text)
    return add


def ensure(board):
    """Step 5: `serve.py ensure <board>`. Returns the URL — the daemon's own
    when it came up, the one it would have been when it did not."""
    p = subprocess.run([sys.executable, SERVE, "ensure", board],
                       capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    m = re.search(r"https?://\S+/board/\S+", p.stdout)
    if p.returncode == 0 and m:
        return m.group(0)
    why = (p.stderr.strip().splitlines() or ["no daemon"])[-1]
    print(f"view: not watching — {why} · the board reads and plans "
          "without it; `pearde view` when the port is free")
    return planlib.serve_url(board)


def doctor(d):
    """Step 6: one report, every line printed. Its exit code is its own —
    a broken row is a line the reader now has, not a reason to stop."""
    sys.stdout.flush()
    subprocess.call(["bash", DOCTOR, d])


def cmd_init(argv):
    """a board that asked nothing — [<dir>] [--language <l>] [--name <n>]
    [--example]: settings, vision, .gitignore, the daemon, doctor, next."""
    args = trlib.Args(argv, FLAGS["init"], "init")
    if len(args.pos) > 1:
        raise Refused("init [<dir>] [--language <l>] [--name <n>] [--example]")
    d = os.path.abspath(args.pos[0] if args.pos else os.getcwd())
    board = os.path.join(d, ".pearde")
    existing = os.path.isfile(os.path.join(board, "settings.md"))
    if args.dry:
        if existing:
            language = str(planlib.board_settings(board).get(
                "language", "")).strip() or "English"
            print(f"dry · board {planlib.board_name(board)} · language "
                  f"{language} — pearde settings language=<l> changes it")
            print(f"  would write: nothing — {board}/settings.md exists")
            return 0
        language = args.opt.get("language", "").strip() or "English"
        name = args.opt.get("name", "").strip() or os.path.basename(d)
        paths = [os.path.join(board, "settings.md"),
                 os.path.join(board, "vision.md")]
        if in_git(d):
            paths.append(os.path.join(d, ".gitignore"))
        paths.append(os.path.join(board, ".obsidian", "plugins", "dataview"))
        print(f"dry · board {name} · language {language} — pearde settings "
              "language=<l> changes it")
        print("  would write: " + " · ".join(paths)
              + (" from the example board" if "example" in args.flags
                 else ""))
        return 0
    if not existing:
        write_board(board, args)
    language = str(planlib.board_settings(board).get("language", "")).strip() \
        or "English"
    print(f"board {planlib.board_name(board)} · language {language} — "
          "pearde settings language=<l> changes it")
    if not existing:
        print(f"init: wrote {board}/settings.md and vision.md"
              + (" from the example board" if "example" in args.flags else ""))
        if in_git(d):
            added = write_gitignore(d)
            if added:
                print(f"init: .gitignore += {' '.join(added)}")
        indexed = index_memos(board)
        if indexed:
            print(f"init: regenerated {indexed}, the memo index by kind — "
                  "the copy carries the memos, `memo index` writes the page "
                  "over them")
        planted = write_knowledge(d)
        if planted:
            print(f"init: knowledge layer at .pearde/wiki/ — "
                  f"{', '.join(planted)} · Dashboard.md is the vault's "
                  "front page, WORKFLOW.md its configuration")
        for verb, line in plant_graph(board):
            print(f"init: knowledge {verb} — {line}")
        plugins, missing, _ = write_obsidian(d)
        if plugins:
            print(f"init: obsidian vault at .pearde/ (its own root, so every "
                  f"board folder shows) — plugins: "
                  f"{', '.join(plugins)} · dataview serves the live views "
                  "from the first open, local-rest-api (local-rest-api with MCP) answers on "
                  "127.0.0.1:27124 (key: .pearde/wiki/.obsidian-api-key) "
                  "after Obsidian loads the vault once")
        state, _vid = register_vault(board)
        if state == "added" and obsidian_running():
            print("init: registered .pearde/ with Obsidian — but Obsidian is "
                  "running, and it rewrites its vault list from memory when "
                  "it quits, which erases this. Run: pearde vault --wait "
                  "--open, then quit Obsidian — the entry is written the "
                  "moment it exits and the vault opens")
        elif state == "added":
            print("init: registered .pearde/ with Obsidian — the status "
                  "line's ▸vault opens it")
        if missing:
            print(f"init: no bundle for {', '.join(missing)} — the vault "
                  "opens without them and renders no view. Fetch them with: "
                  "pearde install --apply <skills-dir>")
    url = ensure(board)
    if not existing:
        doctor(d)
    print("pearde guard on — optional, refuses the waste the loop's rules name")
    print(url)
    print('pearde add "<title>"')
    print("pearde")
    return 0


# ── settings ──────────────────────────────────────────────────────────────────

def cmd_settings(argv):
    """<key>=<value> [--board <path>] — write one key of .pearde/settings.md,
    every other line kept byte for byte."""
    args = trlib.Args(argv, FLAGS["settings"], "settings")
    if len(args.pos) != 1 or "=" not in args.pos[0]:
        raise Refused("settings <key>=<value>")
    key, _, value = args.pos[0].partition("=")
    key, value = key.strip(), value.strip()
    if not KEY_RE.match(key):
        raise Refused(f"`{key}` is not a key — lowercase, digits and `-`")
    if not value:
        raise Refused(f"{key}= names no value — to drop a key, edit the file")
    board = planlib.find_board(args.opt.get("board"))
    path = os.path.join(board, "settings.md")
    if not os.path.isfile(path):
        raise Refused(f"no settings.md at {board} — `pearde init` writes it")
    old = planlib.board_settings(board).get(key)
    was = f"{old} → " if old not in (None, "", []) else ""
    if args.dry:
        trlib.say_dry(board, f"settings: {key} {was}{value}", [path])
        return 0
    editlib.set_key(path, key, value)
    print(f"settings: {key} {was}{value}")
    return 0


# ── vault ─────────────────────────────────────────────────────────────────────

def cmd_vault(argv):
    """[<dir>] [--wait] [--open] — put the board in Obsidian's vault register,
    which is what makes `obsidian://open` resolve to it.

    The register (`obsidian.json`) is read once, at launch, and written back
    from memory on quit. So an entry added under a running app is invisible to
    it and gone afterwards — the app answers "Unable to find a vault for the
    URL" and then erases the line. This command holds that order: it writes
    only while Obsidian is closed. `--wait` waits for the running app to exit
    and writes the instant it does; `--open` launches the vault after writing.
    The vault directory itself is seeded when it is not there yet."""
    args = trlib.Args(argv, FLAGS["vault"], "vault")
    d = os.path.abspath(args.pos[0] if args.pos else os.getcwd())
    board = os.path.join(d, ".pearde")
    if not os.path.isdir(board):
        raise Refused(f"no board at {board} — pearde init {d} writes one")
    if args.dry:
        print(f"dry · would register {board} with Obsidian"
              + (" · seeds .obsidian/ first" if not os.path.isdir(
                  os.path.join(board, ".obsidian")) else ""))
        return 0
    if not os.path.isdir(os.path.join(board, ".obsidian")):
        plugins, missing, _ = write_obsidian(d)
        print(f"vault: seeded {board}/.obsidian"
              + (f" — plugins: {', '.join(plugins)}" if plugins else "")
              + (f" · no bundle for {', '.join(missing)}" if missing else ""))
    if obsidian_running():
        if "wait" not in args.flags:
            raise Refused(
                "Obsidian is running — it rewrites obsidian.json from memory "
                "when it quits, so anything written now is erased and never "
                "read. Quit it and run this again, or run it with --wait and "
                "quit: the entry lands the moment the process goes")
        print("vault: waiting for Obsidian to quit — the register is only "
              "writable while it is closed. Quit it now (⌘Q)…", flush=True)
        for _ in range(WAIT_TICKS):
            if not obsidian_running():
                break
            time.sleep(WAIT_TICK)
        else:
            raise Refused(f"Obsidian still running after "
                          f"{int(WAIT_TICKS * WAIT_TICK)}s — nothing written")
        time.sleep(1)                 # let the app finish its own last write
    state, vid = register_vault(board)
    if state is None:
        print("vault: Obsidian has no config on this machine — nothing to "
              "register. The vault directory is there for when it does")
        return 0
    uri = f"obsidian://open?vault={vid}"
    print(f"vault: {board} {'registered' if state == 'added' else 'already registered'}"
          f" · {uri}")
    if "open" in args.flags:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        try:
            subprocess.run([opener, uri], check=False)
            print(f"vault: opened it — ▸vault on the status line is the same URI")
        except OSError:
            print(f"vault: open it with: {opener} '{uri}'")
    return 0


# ── upgrade ───────────────────────────────────────────────────────────────────

def cmd_upgrade(argv):
    """[<dir>] — bring an existing board up to the layout this repo is on.

    `init` writes a board and then, on every later run, deliberately writes
    nothing: a board that already has `settings.md` skips the vault, the
    gitignore and the knowledge seed entirely. That is right for `init` and
    wrong for a board made before a part of the layout existed — the boards
    on this machine had no `wiki/` content, no Dashboard, no generated PRD
    notes, and in one case a vault whose REST plugin id could never load.

    Every step is idempotent and additive. Nothing already on disk is
    replaced: a file a person edited, a plugin they installed, a settings key
    they changed all survive. The one thing rewritten is a community-plugins
    id that names no plugin, because that value is not an edit, it is a
    typo that silently disables the port.
    """
    args = trlib.Args(argv, FLAGS["upgrade"], "upgrade")
    if len(args.pos) > 1:
        raise Refused("upgrade [<dir>]")
    d = os.path.abspath(args.pos[0] if args.pos else os.getcwd())
    board = os.path.join(d, ".pearde")
    if not os.path.isfile(os.path.join(board, "settings.md")):
        raise Refused(f"no board at {board} — pearde init {d} writes one")
    name = planlib.board_name(board)
    if args.dry:
        print(f"dry · upgrade {name} — would seed wiki/ content, the vault, "
              "the gitignore names, the register, and regenerate wiki/board/")
        return 0
    print(f"upgrade {name} · {board}")
    for folder in (planlib.PRDS_DIR, "memos", "wiki", "workflows",
                   planlib.STATE_DIR):
        os.makedirs(os.path.join(board, folder), exist_ok=True)
    planted = write_knowledge(d)
    print(f"  wiki      {'planted ' + ', '.join(planted) if planted else 'already seeded'}")
    plugins, missing, _ = write_obsidian(d)
    repaired = repair_plugin_ids(os.path.join(board, ".obsidian"))
    vault_line = ", ".join(plugins) if plugins else "already there"
    if repaired:
        vault_line += " · repaired " + "; ".join(repaired)
    if missing:
        vault_line += (f" · no bundle for {', '.join(missing)} — "
                       "pearde install --apply <skills-dir> fetches them")
    print(f"  vault     {vault_line}")
    if in_git(d):
        added = write_gitignore(d)
        print(f"  gitignore {'+= ' + ' '.join(added) if added else 'already names them'}")
    board_added = write_board_gitignore(board)
    if board_added:
        print(f"  board-git += {' '.join(board_added)} — the board is its own "
              "repo and was tracking its REST key")
    state, _vid = register_vault(board)
    if state is None:
        print("  register  Obsidian has no config on this machine")
    elif state == "added" and obsidian_running():
        print("  register  added — but Obsidian is running and rewrites its "
              "vault list from memory on quit, which erases this. "
              "pearde vault --wait --open, then quit it")
    else:
        print(f"  register  {'added' if state == 'added' else 'already registered'}")
    for verb, line in plant_graph(board):
        print(f"  {verb:<9} {line}")
    if repaired and obsidian_running():
        print("  note      Obsidian reads community-plugins.json at launch — "
              "restart it, or enable the plugin in its settings, for the "
              "repaired id to take")
    return 0


# ── the surface ───────────────────────────────────────────────────────────────

def _command(name, fn):
    def call(argv):
        try:
            return fn(argv)
        except trlib.FlagRefused as e:
            print(f"pearde {name}: {e}", file=sys.stderr)
            return 2
        except Refused as e:
            print(f"pearde {name}: refused — {e}", file=sys.stderr)
            return 1
    call.__doc__ = fn.__doc__
    call.__name__ = name
    call.flags = FLAGS[name]        # what `pearde <name> --help` prints
    return call


COMMANDS = {"init": _command("init", cmd_init),
            "settings": _command("settings", cmd_settings),
            "upgrade": _command("upgrade", cmd_upgrade),
            "vault": _command("vault", cmd_vault)}


def main(argv):
    if len(argv) < 2 or argv[1] not in COMMANDS:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    return COMMANDS[argv[1]](argv[2:])


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main(sys.argv))
