#!/usr/bin/env python3
"""pearde init — a board exists after one command, and it asked nothing.

    init.py init [<dir>] [--language <l>] [--name <n>] [--example] [--dry]
    init.py settings <key>=<value> [--board <path>] [--dry]

`init` leaves `<dir>/pearde/` (default: the working directory) on the
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

`settings` writes one key of `pearde/settings.md` through edit.py — one
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
import tempfile
import time
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(HERE)                          # the skill's resources/
SKILL = os.path.dirname(RES)
_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import edit as editlib          # noqa: E402 — the one writer of bytes
import plan as planlib          # noqa: E402 — every read
import transitions as trlib     # noqa: E402 — the flag parser
import obsidian_register as obsreg  # noqa: E402 — the one register writer

EXAMPLE = os.path.join(HERE, "example")   # the seed board
VISION_TEMPLATE = os.path.join(SKILL, "references", "templates", "vision.md")
# Every script this one launches is found under resources/, never spelled as
# a file beside this one — @resources/pearde_path.py `script`. sys.path does
# nothing for a subprocess addressed by path.
SERVE = pearde_path.script("serve.py")
DOCTOR = pearde_path.script("doctor.sh")

# The six knobs of @references/settings.md, in the order the file shows
# them, every one written by name so a reader sees the choice on disk.
# `workers: 0` and `pipeline: 0` are no cap: the board assumes unlimited
# parallel agents, and a number here is the cap the user chose.
# `happiness: 0` is written because the ramp gate reads it — a fresh board
# has never been asked whether the machine is tooled for its repo, and a key
# that is absent says the same thing less plainly.
DEFAULTS = (("language", "English"), ("workers", "0"), ("pipeline", "0"),
            ("weight-default", "50"), ("gantt-day", "8h"), ("happiness", "0"))

# Every settings key this board honours, whether or not `init` writes a
# default for it. DEFAULTS above is the printed subset — the six a new board
# opens with; the rest read at a default held by their one reader. This tuple
# is what says a key is real, and @resources/claims.py checks every key named
# in references/ against it: without it a renamed key leaves its old name
# standing in prose forever, since nothing else in the repo reads prose.
SETTING_KEYS = ("language", "workers", "pipeline", "weight-default",
                "gantt-day", "happiness", "memos", "workflows", "grammar",
                "health-floor", "health-weights", "harnesses", "groups",
                "members", "gate", "context-budget", "transitions-per-pass",
                "claim-ttl", "footprint-above", "split-above", "specs-above",
                "name", "machine-ceiling")

# The frontmatter contract, as a set of names — @references/parts/contract.md
# is its prose and this is what a checker can read. `prd.md` first, then the
# keys a `specNN.md` adds, then the two files a board keeps beside its PRDs.
FRONTMATTER_KEYS = ("state", "priority", "complexity", "blast-radius", "est",
                    "actual", "claim", "repo", "workflow", "needs",
                    "footprint", "origin", "from",
                    "vision", "terminals", "edges",
                    "subject", "date", "updated", "kind", "status", "verify")

# Machine-local per board — regenerable. What this repo's own .gitignore
# holds for the same names. `.obsidian/` is the vault's config, written at
# the project root (the vault IS the project) and never shared. `/.pearde`
# is the compatibility symlink `upgrade` leaves behind when it moves a board
# out of the hidden name — a link, not a directory, and nobody's history
# wants it.
def ignored_names(board):
    """Those names, spelled with the board's OWN directory name. Only the two
    paths under the board move when a project has to call its board something
    other than `pearde`: `.obsidian/` is the project's vault and `/.pearde`
    is the compat symlink, and neither depends on what the board ended up
    being called.

    Everything else here is output a tool rebuilds, and it is listed because
    `collect.scratch` is not the same guard: that one skips dotfiles directly
    under the board, so it answers for `.lanes/`, `.claims/` and `.state/` at
    commit time and for nothing a person types. `git status`, `git add -A`
    and a board whose plan is *tracked* — the normal case, since the PRDs are
    the plan — see the lot unless it is named here. `.lanes/` is the one that
    hurts: a lane is a git worktree, and a board mid-pass holds one per
    worker, tens of gigabytes offered to a commit that never wanted them."""
    n = os.path.basename(os.path.abspath(board)) if board else planlib.BOARD_DIR
    return (f"{n}/.state/", f"{n}/.lanes/", f"{n}/.claims/", f"{n}/wiki/",
            f"{n}/health/", f"{n}/graphify/", f"{n}/graphs/",
            f"{n}/prds/**/probe/", ".obsidian/", "/.pearde")

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
                 "Dashboard.report.md", ".obsidian/", "health/",
                 ".lanes/", ".claims/", "graphify/", "graphs/",
                 "prds/**/probe/",
                 ".state/serve.json", ".state/serve.log", ".state/run-*.log",
                 ".state/guard/", ".state/calibration.json")
BOARD_HEADER = "# machine-local — two hold one credential, the rest rebuild"

# The Obsidian requirement: dataview (the live views), local-rest-api (the
# port a tool reads the vault through) and hidden-folders-access (Obsidian
# refuses to read any path holding a dot-segment, so without it a board named
# `.pearde` is invisible in the vault it is supposed to be). The preset at
# resources/board/obsidian/ carries the settings; the plugin bundles are not
# vendored — `pearde vault` fetches them at the pinned versions below into
# the preset's plugins/, and this file copies whatever it finds there to
# <dir>/.obsidian when the board's parent is the vault it seeds. A bundle the
# fetch never got is reported, not silently skipped. The REST key is
# minted fresh — one per board, never shipped in the template.
#
# The fetch lives here and not in `install.sh` because the install is links
# and nothing else: it must run on a machine with no network, and a person
# who never opens Obsidian should never pay for bundles they will not
# read. `pearde vault` is the one command that says "I want this vault", so
# it is the one command allowed to reach the network.
OBSIDIAN_PRESET = os.path.join(HERE, "obsidian")
# `vault --wait` polls for the app to go: half a second apart, ten minutes of
# patience — long enough for a person to finish what they were doing and quit,
# short enough that a forgotten command does not sit there for a session.
WAIT_TICK, WAIT_TICKS = 0.5, 1200
# The names are plugin *ids* — the `id` field of each bundle's own
# manifest.json — not repo names: `hidden-folders-access` is
# dsebastien/obsidian-hidden-folders-access.
OBSIDIAN_PLUGINS = ("dataview", "obsidian-local-rest-api",
                    "hidden-folders-access")
# name -> (github repo, release tag). Pinned, because a vault that opens is
# worth more than the newest plugin. The three files are what an Obsidian
# release ships; styles.css is optional and a 404 on it is not a failure.
OBSIDIAN_BUNDLES = {
    "dataview": ("blacksmithgu/obsidian-dataview", "0.5.68"),
    "obsidian-local-rest-api": ("coddingtonbear/obsidian-local-rest-api", "5.1.0"),
    "hidden-folders-access": ("dsebastien/obsidian-hidden-folders-access", "2.0.0"),
}
BUNDLE_FILES = ("main.js", "manifest.json", "styles.css")
BUNDLE_TIMEOUT = 30

# The knowledge layer's *content* seed — Dashboard.md, WORKFLOW.md, the
# indexes, the empty scaffolds — for `pearde/wiki/`, the folder the preset
# above points its vault at. `write_knowledge` plants it; `init` and
# `upgrade` both call that. Not the same thing as resources/board/obsidian/:
# that is app configuration, this is vault content. Every path inside these
# files is vault-relative — the vault roots at the PROJECT, so a KB query
# reads `pearde/wiki/conclusions`, never `wiki/conclusions`.
KNOWLEDGE_PRESET = os.path.join(HERE, "knowledge")
KNOWLEDGE_PY = pearde_path.script("knowledge.py")
MEMOS_PY = pearde_path.script("memos.py")
GRAMMAR_PY = pearde_path.script("grammar.py")

KEY_RE = re.compile(r"^[a-z][a-z0-9-]*$")


class Refused(Exception):
    """An argument the command cannot act on. Nothing was written."""


# The declaration — transitions.py `Args` is the parser.
FLAGS = {
    "init":     trlib.Flags(("language", "name"), ("example",) + trlib.DRY),
    "settings": trlib.Flags(("board",), trlib.DRY),
    "vault":    trlib.Flags(("dir",), ("wait", "open") + trlib.DRY),
    # `--dir` is the board's DIRECTORY name, the one thing `upgrade` cannot
    # work out for itself: a project whose tree already uses the word
    # `pearde` has to call its board something else, and only a person knows
    # which name is free. Nothing else in the tool asks for it — the board is
    # found afterwards by the settings.md it carries.
    "upgrade":  trlib.Flags(("dir",), trlib.DRY),
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
    file is written only when it is not there, so a hand-made `pearde/` keeps
    what it has and gains what it lacks. Also makes the five directories a
    board has even when empty — `prds/`, `memos/`, `wiki/`, `workflows/`,
    `.state/` — so `scan` and the daemon find them from the first run,
    whether or not `--example` seeded any of them with content."""
    settings = os.path.join(board, "settings.md")
    if "example" in args.flags:
        if os.path.isdir(board) and os.listdir(board):
            raise Refused(f"{board} exists and holds no settings.md — "
                          "--example copies into an empty or missing board")
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


def unhide_board(d, name=None):
    """`<dir>/.pearde/` → `<dir>/<name>/`, and a `.pearde` symlink left where
    the directory was. `name` defaults to `pearde`, which is what every board
    that can have it is called.

    The board carried a dot until 2026-09-02 and that dot decided what a
    person could see. Obsidian skips every path holding a dot-segment before
    a setting is read, so from a vault at the project root the whole board
    was invisible; rooting the vault at the board instead hid the project
    from the board, and a symlink out of the hidden name does not work either
    — the app refuses a symlink that resolves back inside the vault
    (@references/obsidian.md reads both out of the bundle). A board with no
    dot in its name is the whole fix: one vault at the project root, named
    for the project, showing everything.

    The symlink is the other half. Every path spelled `.pearde/…` — in a
    worktree, another tool, a person's muscle memory, a doc written before
    today — keeps resolving through it, and it is relative, so a moved or
    copied project keeps working. It is gitignored, never a directory, and
    nothing pearde writes goes through it.

    `name` is the other half of that. `pearde` is an ordinary word, and a
    project whose own folder tree already uses it — this repo's checkout sits
    at `infra/pearde`, right beside the `infra` board — has that name taken
    and cannot move its board into it. So the target is an argument, the
    board is found afterwards by the `settings.md` it carries rather than by
    what it is called (@resources/board/plan.py `named_boards`), and the one
    name that must never be the target is the hidden one this moves out of.

    Returns "moved", "linked" (the move was done, the link was not there),
    or None when there was nothing to do."""
    name = name or planlib.BOARD_DIR
    if (name.startswith(".") or os.sep in name
            or (os.altsep and os.altsep in name)):
        raise Refused(f"a board directory is one plain name with no dot in "
                      f"front of it — `{name}` is what the move is out of")
    old = os.path.join(d, planlib.LEGACY_BOARD_DIR)
    new = os.path.join(d, name)
    moved = False
    if os.path.isdir(old) and not os.path.islink(old):
        if os.path.exists(new):
            if os.path.realpath(new) != os.path.realpath(old):
                raise Refused(f"{new} is already there and is not {old} — "
                              "move or remove it, then run this again")
        else:
            os.rename(old, new)
            moved = True
    if not os.path.isdir(new):
        return None
    if not os.path.exists(old) and not os.path.islink(old):
        os.symlink(name, old)          # relative: a copied project still works
        return "moved" if moved else "linked"
    return "moved" if moved else None


def vault_weight(path):
    """How much of a person is in an `.obsidian/` — files, plugin bundles, and
    whether Obsidian ever wrote a layout into it.

    Used only to say which of two vaults looks configured when both exist. A
    seeded vault is the preset's five JSON files and the two bundles and
    nothing else; a vault someone has opened has a `workspace.json`, because
    Obsidian writes one the moment it loads a vault and never otherwise. That
    file is the strongest single signal and is reported on its own rather
    than folded into the count. Returns (files, bundles, has_workspace)."""
    files = bundles = 0
    for dirpath, _dirs, names in os.walk(path):
        files += len(names)
        if os.path.basename(dirpath) in OBSIDIAN_PLUGINS and "main.js" in names:
            bundles += 1
    return files, bundles, os.path.isfile(os.path.join(path, "workspace.json"))


def stranded_vault(legacy, dest):
    """The line to say when the lift could not happen because the project
    root already had an `.obsidian/`.

    `write_obsidian` moves a vault left at the old board root up to the
    project, and refuses to when the destination exists — an installed vault
    wins, which is the right call, because overwriting one silently would
    lose a person's plugins and layout. The bug this repairs is that it also
    said nothing: the board's vault stayed below, invisible, and whoever had
    been using it found their plugins, their REST key and their layout gone
    with no clue where. Both paths are named, both are weighed, and the one
    that looks configured is called out, so a person is told rather than left
    to discover it. Nothing is moved either way. Returns None when there is
    no second vault to report."""
    if not os.path.isdir(legacy) or not os.path.isdir(dest):
        return None
    lf, lb, lw = vault_weight(legacy)
    df, db, dw = vault_weight(dest)
    def say(n, f, b, w):
        return (f"{n} ({f} file{'s' if f != 1 else ''}, {b} plugin bundle"
                f"{'s' if b != 1 else ''}, "
                f"{'a layout Obsidian wrote' if w else 'no workspace.json'})")
    # A layout decides it; failing that, the bundles; failing that, the count.
    richer = legacy if (lw, lb, lf) > (dw, db, df) else dest
    return (f"two vaults, and nothing was moved: {say(dest, df, db, dw)} is "
            f"where Obsidian opens this project, and {say(legacy, lf, lb, lw)} "
            f"was left below by the board. "
            + (f"The one that looks configured is the one below — copy what "
               f"you want out of it, or move it up by hand once Obsidian is "
               f"quit. " if richer == legacy else
               f"The one in use looks the richer of the two, so the leftover "
               f"below is most likely a seeded stub. ")
            + "Neither is deleted; the installed vault wins by default.")


# ── the plugin bundles: the one place this repo reaches the network ───────────
# `install.sh` used to do this, and an installer whose whole thesis is links —
# five symlinks per skill, no copies — had a `curl` in it that a person with no
# network watched fail. The bundles are not part of an install: they are part of
# a vault, and a vault is opt-in. So the fetch moved here, behind the one verb
# that asks for one.

def bundle_at(name):
    """Where a bundle lives in the preset."""
    return os.path.join(OBSIDIAN_PRESET, "plugins", name)


def bundle_state(name):
    """`ok`, `stale` or `missing` for the bundle in the preset, against the
    version pinned above. A manifest whose version cannot be read is stale —
    a half-written bundle is not one we should copy into someone's vault."""
    want = OBSIDIAN_BUNDLES.get(name, (None, None))[1]
    at = bundle_at(name)
    main, manifest = os.path.join(at, "main.js"), os.path.join(at, "manifest.json")
    if not (os.path.getsize(main) if os.path.isfile(main) else 0):
        return "missing"
    try:
        with open(manifest, encoding="utf-8") as f:
            have = json.load(f).get("version")
    except (OSError, ValueError):
        return "stale"
    return "ok" if have == want else "stale"


def fetch_bundle(name):
    """Download one pinned bundle into the preset. Returns None on success or
    the line to print on failure.

    Every file lands as `<f>.part` and is renamed, so an interrupted fetch
    leaves no half-file that `bundle_state` would read as ok. `styles.css` is
    optional — dataview ships one, plenty of plugins do not — so only a
    missing `main.js` or `manifest.json` fails the bundle."""
    import urllib.error
    import urllib.request
    repo, ver = OBSIDIAN_BUNDLES[name]
    at = bundle_at(name)
    os.makedirs(at, exist_ok=True)
    got = []
    try:
        for f in BUNDLE_FILES:
            url = f"https://github.com/{repo}/releases/download/{ver}/{f}"
            try:
                with urllib.request.urlopen(url, timeout=BUNDLE_TIMEOUT) as r:
                    data = r.read()
            except urllib.error.HTTPError as e:
                if e.code == 404 and f == "styles.css":
                    continue                   # optional, and plenty ship none
                raise
            part = os.path.join(at, f + ".part")
            with open(part, "wb") as out:
                out.write(data)
            os.replace(part, os.path.join(at, f))
            got.append(f)
    except Exception as e:                      # network, DNS, TLS, HTTP, disk
        for f in BUNDLE_FILES:
            part = os.path.join(at, f + ".part")
            if os.path.isfile(part):
                os.remove(part)
        return f"{name} {ver}: {e}"
    return None if "main.js" in got else f"{name} {ver}: the release carried no main.js"


def ensure_bundles(names=OBSIDIAN_PLUGINS):
    """Fetch every pinned bundle the preset does not already hold at its
    version. Returns (fetched, failed) — `fetched` the names brought in or
    refreshed, `failed` one line per bundle that could not be got.

    Never raises: a vault without dataview renders no view, which is worth
    saying out loud, but it is not worth refusing to register the vault
    over."""
    fetched, failed = [], []
    for name in names:
        if name not in OBSIDIAN_BUNDLES:
            continue
        state = bundle_state(name)
        if state == "ok":
            continue
        bad = fetch_bundle(name)
        (failed.append(bad) if bad else fetched.append(name))
    return fetched, failed


def copy_bundles(dest):
    """Put every preset bundle the vault at `dest` does not already have into
    it. Returns the names copied.

    `write_obsidian` seeds a vault that is not there yet and never touches one
    that is — a hand-tuned vault wins, which is right. But a person whose
    vault was seeded before the bundles arrived has an `.obsidian/` and no
    dataview, and telling them to run `pearde vault` has to actually fix that.
    A plugin directory that is already there is left alone: their copy, their
    settings, their version."""
    copied = []
    for plugin in OBSIDIAN_PLUGINS:
        src = bundle_at(plugin)
        dst = os.path.join(dest, "plugins", plugin)
        if os.path.isdir(dst) or not os.path.isfile(os.path.join(src, "main.js")):
            continue
        shutil.copytree(src, dst, dirs_exist_ok=True)
        copied.append(plugin)
    return copied


def write_obsidian(d):
    """Step 4b: the vault, and it roots at the PROJECT — `<dir>/.obsidian/`.

    It rooted at the board until 2026-09-02, because Obsidian skips every
    path holding a dot-segment and `.pearde/` was invisible from a vault one
    level up. `unhide_board` takes the dot out of the board's name instead,
    which lets the vault sit where a person expects it: at the project, named
    for the project's own folder, indexing every file under it — the code,
    the docs, and the board among them, linkable to each other. Every
    vault-relative path the board writes — the Dataview sources, the
    generated wikilinks — is written against the project root, so the board's
    own notes are `pearde/wiki/…`.

    Copies the vendored preset and plugins in — dataview,
    obsidian-local-rest-api, hidden-folders-access, the graph and app
    configuration — and mints a
    fresh REST key into the plugin's data.json, mirrored at
    `pearde/wiki/.obsidian-api-key` where the loop's tools read it. Everything
    already there is kept (a hand-tuned vault wins), including a whole
    `.obsidian/` a person already had at the project root. A vault the board
    left at the old root is moved up rather than copied, so the plugins,
    workspace and key a person has been using survive the move. A plugin
    whose bundle is not in the preset — `pearde vault` has not run, or could
    not reach the network — is returned in the second list and named on the
    console, because a vault missing dataview renders no view at all.

    When BOTH vaults exist the lift does not happen — an installed
    vault wins — and that used to be silent, which is how a person
    lost a configured vault to a stub without being told. It is now
    reported: `stranded` carries the line naming both paths and which
    looks configured, and every caller prints it.
    Returns (installed, missing, key, stranded)."""
    board = planlib.board_at(d)
    dest = os.path.join(d, ".obsidian")
    legacy = os.path.join(board, ".obsidian")
    stranded = None
    if os.path.isdir(legacy) and not os.path.exists(dest):
        os.rename(legacy, dest)                # the vault a person has, moved up
    else:
        stranded = stranded_vault(legacy, dest)   # both there: say so
    plugins, missing = [], []
    if not os.path.isdir(OBSIDIAN_PRESET):
        return [], list(OBSIDIAN_PLUGINS), None, stranded
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
    # The preset's `userIgnoreFilters` are written for a board called
    # `pearde`, and this one may not be — a vault-relative filter naming a
    # folder the project does not have hides nothing and reads as a lie about
    # the layout. Correcting it here means a vault seeded fresh is right from
    # the first open, not right after the first `upgrade`.
    repair_ignore_filters(dest, os.path.basename(board))
    repair_graph_view(dest)
    # the key: fresh per board, in the v5 schema the plugin reads, both
    # where the plugin reads it and where a tool looks it up
    key = os.urandom(24).hex()
    cfg = {"port": 27124, "insecurePort": 27123, "enableInsecureServer": False,
           "apiKey": key}
    # The key is written beside the plugin's own bundle, and the bundle is not
    # vendored — a machine that never ran `pearde vault` has no plugin dir
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
    key_path = os.path.join(board, "wiki", ".obsidian-api-key")
    have = ""
    if os.path.exists(key_path):
        have = open(key_path, encoding="utf-8").read().strip()
    if have != key:
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        editlib.write_atomic(key_path, key + "\n")
    return plugins, missing, key, stranded


def write_knowledge(d):
    """The knowledge layer's content, seeded into `<dir>/.pearde/wiki/` —
    except `Dashboard.md`, which lands at the board's own root.

    `knowledge.py`'s Store makes the directories on first use but writes no
    Dashboard and no WORKFLOW — a board that never had them opens in Obsidian
    with no views at all, which is what a fresh vault looked like before this
    step existed. Copies every file of the preset that is not already there;
    a file a person edited is never replaced. Returns the vault-relative
    names it planted."""
    board = planlib.board_at(d)
    wiki = os.path.join(board, "wiki")
    planted = []
    # The dashboard is the vault's front page and the vault roots at the
    # board, so it lands at the board's root. A board seeded before that was
    # true carries the person's own edited copy one folder down: move it,
    # never plant a second one beside it. Its Dataview sources are already
    # vault-relative, so the move is a rename and nothing else.
    old_dash = os.path.join(wiki, "Dashboard.md")
    new_dash = os.path.join(board, "Dashboard.md")
    if os.path.isfile(old_dash) and not os.path.exists(new_dash):
        os.makedirs(board, exist_ok=True)
        os.replace(old_dash, new_dash)
        planted.append("../Dashboard.md (moved up from wiki/)")
    if not os.path.isdir(KNOWLEDGE_PRESET):
        return planted
    for src_dir, _dirs, files in os.walk(KNOWLEDGE_PRESET):
        rel = os.path.relpath(src_dir, KNOWLEDGE_PRESET)
        dst_dir = wiki if rel == "." else os.path.join(wiki, rel)
        os.makedirs(dst_dir, exist_ok=True)
        for name in sorted(files):
            if name == ".DS_Store":
                continue
            dst = (new_dash if rel == "." and name == "Dashboard.md"
                   else os.path.join(dst_dir, name))
            if os.path.exists(dst):
                continue
            shutil.copyfile(os.path.join(src_dir, name), dst)
            planted.append(os.path.relpath(dst, wiki))
    # the two the Store makes but the preset carries no file for
    for name in ("sources", "conclusions", "pending", "graphs"):
        os.makedirs(os.path.join(wiki, name), exist_ok=True)
    return planted


def index_memos(board, verb="init"):
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

    `verb` names the command in that failure line. Both `init` and `upgrade`
    run this step — a board brought forward by `upgrade` was made before this
    function existed, so its index is exactly as stale as a copied one's, and
    bringing a board forward has to leave it as healthy as making one fresh.
    A message hard-coded to say `init:` would name the wrong command on the
    half of the callers that are not `init`.
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
        print(f"{verb}: could not regenerate memos/README.md, the memo index "
              f"by kind — {why} · the board holds memos and no index, which "
              "doctor reads as stale; run `memo index` once that is fixed")
        return None
    return os.path.relpath(written[-1], board)


def grammar_file(board):
    """Where the board's vocabulary sits — `pearde/grammar.md` unless
    `grammar:` in `settings.md` points elsewhere. The same resolution
    @resources/grammar.py `grammar_path` does, and that file is its only
    writer."""
    v = str(planlib.board_settings(board).get("grammar", "")).strip()
    return os.path.normpath(os.path.join(board, v or "grammar.md"))


def plant_grammar(board, verb="init"):
    """Write the board's grammar from @references/templates/grammar.md.

    The template already holds pearde's own vocabulary — the words every board
    shares — and ends on an empty `This repo` group, which is the half the
    board fills. So a newcomer's first `show` answers rather than reporting an
    empty file.

    `grammar.py init` is the one writer of that file and never overwrites, so
    this is idempotent: a board that already has a vocabulary keeps every row.
    Runs after `settings.md` exists, since the template's `<board>` is filled
    from `name:` there. Returns the relative path written, or None when the
    file was already on disk.

    A failure is said, not swallowed — a board with no grammar file is
    doctor's `grammar` row reading `off` for the life of the board, and a
    `verb` that exits 0 having quietly not written it is how that happens.
    """
    if os.path.isfile(grammar_file(board)):
        return None
    out = subprocess.run([sys.executable, os.path.abspath(GRAMMAR_PY),
                          "init", board], capture_output=True, text=True)
    written = out.stdout.strip().splitlines()
    if out.returncode != 0 or not written:
        why = (out.stderr.strip().splitlines() or written
               or ["no output"])[-1]
        print(f"{verb}: could not write the board's grammar from "
              f"references/templates/grammar.md — {why} · doctor's `grammar` "
              "row reads `off` until it exists; run `pearde grammar init` "
              "once that is fixed")
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

    `board` writes the generated PRD and memo notes, `index` writes one note
    per row of the repo's manifest so a `@@<keyword>` is answerable from the
    dashboard (and writes nothing where the repo carries no map), `relink`
    builds the graph over what is on disk — so the order is fixed, and all
    three run after `index_memos`, since `board` reads the memos it indexes.
    Returns one `(verb, first line)` pair per verb, for the caller to print
    or drop.
    """
    lines = []
    for verb in ("board", "index", "relink"):
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


def repair_ignore_filters(dest, name=None):
    """Obsidian's `userIgnoreFilters` are vault-relative, and the vault moved
    up one level: a filter written when the vault rooted at the board reads
    `wiki/pending/`, which under a project vault names nothing (and would name
    the wrong thing in a project that happens to have a `wiki/`). Rewrites
    only the filters this repo ships, prefixing them with the board's folder.
    A filter someone else added is left exactly where it is. Returns what it
    changed.

    `name` is the board's directory name, and the preset is written for a
    board called `pearde` — so a project that had to call its board something
    else has BOTH shapes to correct: the bare suffix a board-rooted vault
    left, and the default name a run before the rename wrote. Both map to the
    one spelling this board actually has."""
    path = os.path.join(dest, "app.json")
    if not os.path.isfile(path):
        return []
    try:
        have = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return []
    filters = have.get("userIgnoreFilters")
    if not isinstance(filters, list):
        return []
    try:
        shipped = json.load(open(os.path.join(OBSIDIAN_PRESET, "app.json"),
                                 encoding="utf-8")).get("userIgnoreFilters", [])
    except (OSError, ValueError):
        return []
    name = name or planlib.BOARD_DIR
    pre = planlib.BOARD_DIR + "/"
    preset = [name + "/" + f[len(pre):]
              if isinstance(f, str) and f.startswith(pre) else f
              for f in shipped]
    old = {}
    for f in shipped:
        if not isinstance(f, str) or not f.startswith(pre):
            continue
        want = name + "/" + f[len(pre):]
        old[f[len(pre):]] = want          # a board-rooted vault's spelling
        if f != want:
            old[f] = want                 # written before this board was renamed
    fixed, changed = [], []
    for entry in filters:
        if isinstance(entry, str) and entry in old:
            fixed.append(old[entry])
            changed.append(f"{entry} -> {old[entry]}")
        else:
            fixed.append(entry)
    for entry in preset:
        if entry not in fixed:
            fixed.append(entry)
            changed.append(f"added {entry}")
    if changed:
        have["userIgnoreFilters"] = fixed
        editlib.write_atomic(path, json_text(have))
    return changed


def repair_graph_view(dest):
    """The graph view's own config, brought to the preset. `graph.json` is
    seeded once and then owned by Obsidian, which rewrites it as a person
    pans and zooms — so the copy in `write_obsidian` never overwrites it, and
    a vault seeded under an older layout kept colour groups naming folders
    that no longer exist (`prds/knowledge/board`, `prds/memos`). A group whose
    query matches nothing is not an error the app reports: the graph simply
    draws grey, and the layout looks like the one thing it is not.

    Only the three keys this repo has an opinion about are taken from the
    preset — the colour groups, the search filter and `showTags`. Everything
    else in the file is where the person left their view: scale, node size,
    the forces. The groups are `tag:` queries now, and a tag survives a folder
    move, which is what makes this the last time this repair is needed.
    Returns what it changed."""
    path = os.path.join(dest, "graph.json")
    if not os.path.isfile(path):
        return []
    try:
        have = json.load(open(path, encoding="utf-8"))
        want = json.load(open(os.path.join(OBSIDIAN_PRESET, "graph.json"),
                              encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if not isinstance(have, dict) or not isinstance(want, dict):
        return []
    changed = []
    for key in ("colorGroups", "search", "showTags"):
        if key in want and have.get(key) != want[key]:
            have[key] = want[key]
            changed.append(f"graph {key}")
    if changed:
        editlib.write_atomic(path, json_text(have))
    return changed


def write_gitignore(d, board=None):
    """Step 4: the machine-local names, appended to `<dir>/.gitignore` — the
    board's parent, where `<board>/…` is the right spelling — when they are
    not already there. `board` names the directory the board is actually in,
    because that name is not always `pearde`. Returns the names it added."""
    path = os.path.join(d, ".gitignore")
    text = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""
    have = {l.strip() for l in text.splitlines()}
    add = [n for n in ignored_names(board or planlib.board_at(d))
           if n not in have]
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
    with `pearde/…`-prefixed names. A board on its own branch never sees
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


# ── the host's own settings ───────────────────────────────────────────────────

# Suggestions, never writes. Each one is a fixed per-turn cost in the window
# every pass runs in — context is billed on every turn, so what a window
# carries is paid for again on each turn left in the session, and a setting
# is the only place that kind of cost can be cut once instead of per pass.
# `key: value` is what the host settings file would say; the line is what a
# person needs to decide it. Measured on this machine, 2026-09-02.
HOST_SETTINGS = os.path.expanduser("~/.claude/settings.json")
HOST_SUGGESTIONS = (
    ("enableWorkflows", False,
     "workflows dispatch their own agents — a second orchestrator beside the "
     "board, competing for the same slots"),
    ("enableArtifact", False,
     "artifacts publish a hosted page; a board's readers are already in the "
     "terminal and in `report.md`"),
    ("promptSuggestionEnabled", False,
     "suggestions are extra model calls per prompt, and a pass is not typing"),
    ("skillOverrides", None,
     "the skill listing is re-sent on every turn — 64 skills measured at "
     "~5,900 tokens. pearde's own siblings are reached by shell (`pearde memo "
     "add`), never the Skill tool, so `name-only` on them costs the "
     "orchestrator nothing and cut that listing to ~1,950"),
)


def host_gap():
    """Which HOST_SUGGESTIONS the machine has not settled. Unreadable or
    absent settings answers the whole list — a file nobody has written is
    the case the suggestion is for. Reads; writes nothing."""
    try:
        with open(HOST_SETTINGS, encoding="utf-8") as f:
            have = json.load(f)
        if not isinstance(have, dict):
            have = {}
    except (OSError, ValueError):
        have = {}
    return [(k, v, why) for k, v, why in HOST_SUGGESTIONS
            if k not in have or (v is not None and have.get(k) != v)]


def suggest_host(out=print):
    """Print the gap as suggestions. Returns how many it printed, so a caller
    can stay silent on a machine that has already settled them."""
    gap = host_gap()
    if not gap:
        return 0
    out(f"init: the machine, not this board — {len(gap)} setting"
        f"{'' if len(gap) == 1 else 's'} in {HOST_SETTINGS} the loop pays "
        "for on every turn:")
    for key, value, why in gap:
        shown = f"{key}: {json.dumps(value)}" if value is not None else key
        out(f"  {shown} — {why}")
    out("  none of these is written for you; a pass runs the same without "
        "them, and more expensively")
    return len(gap)


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
    board = planlib.board_at(d)
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
                 os.path.join(board, "vision.md"),
                 os.path.join(board, "grammar.md")]
        if in_git(d):
            paths.append(os.path.join(d, ".gitignore"))
        paths.append(os.path.join(d, ".obsidian", "plugins", "dataview"))
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
            added = write_gitignore(d, board)
            if added:
                print(f"init: .gitignore += {' '.join(added)}")
        indexed = index_memos(board)
        if indexed:
            print(f"init: regenerated {indexed}, the memo index by kind — "
                  "the copy carries the memos, `memo index` writes the page "
                  "over them")
        seeded = plant_grammar(board)
        if seeded:
            print(f"init: wrote {board}/{seeded}, the board's vocabulary — "
                  "pearde's own words are already in it; `pearde grammar add "
                  "<term> <meaning>` files this repo's")
        planted = write_knowledge(d)
        if planted:
            print(f"init: knowledge layer at {planlib.BOARD_DIR}/wiki/ — "
                  f"{', '.join(planted)} · Dashboard.md is the vault's "
                  "front page, WORKFLOW.md its configuration")
        for verb, line in plant_graph(board):
            print(f"init: knowledge {verb} — {line}")
        plugins, missing, _, stranded = write_obsidian(d)
        if plugins:
            print(f"init: obsidian vault at {d} — the project itself, named "
                  f"{os.path.basename(d)}, indexing every file under it, the "
                  f"board included — plugins: "
                  f"{', '.join(plugins)} · dataview serves the live views "
                  "from the first open, local-rest-api (local-rest-api with MCP) answers on "
                  "127.0.0.1:27124 (key: pearde/wiki/.obsidian-api-key) "
                  "after Obsidian loads the vault once")
        if stranded:
            print(f"init: obsidian {stranded}")
        # even_if_running: the entry is written under a live app on purpose
        # — the next line tells the user it will be erased on quit and what
        # to run instead. Refusing here would drop that whole branch.
        state, _vid = obsreg.write(d, retire=board, even_if_running=True)
        if state == "added" and obsreg.running():
            print(f"init: registered {os.path.basename(d)} with Obsidian — "
                  "but Obsidian is "
                  "running, and it rewrites its vault list from memory when "
                  "it quits, which erases this. Run: pearde vault --wait "
                  "--open, then quit Obsidian — the entry is written the "
                  "moment it exits and the vault opens")
        elif state == "added":
            print(f"init: registered {os.path.basename(d)} with Obsidian — "
                  "the status line's ▸vault opens it")
        if missing:
            print(f"init: no bundle for {', '.join(missing)} — the vault "
                  "opens without them and renders no view. Fetch them with: "
                  "pearde vault")
    url = ensure(board)
    if not existing:
        suggest_host()
        doctor(d)
    print("pearde guard on — optional, refuses the waste the loop's rules name")
    print(url)
    print('pearde add "<title>"')
    print("pearde")
    return 0


# ── settings ──────────────────────────────────────────────────────────────────

def cmd_settings(argv):
    """<key>=<value> [--board <path>] — write one key of pearde/settings.md,
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

# the register file is one file for the whole machine, not one per board — so the
# writer slot the wait guards is machine-wide too. A lock under the board
# would let two boards each think they were the only one waiting.
VAULT_LOCK = os.path.join(tempfile.gettempdir(), "pearde-vault.lock")


def _lock_holder_alive(pid):
    """Same liveness check the rest of the tree uses for a pid it did not
    start: signal 0, ProcessLookupError means gone, any other answer means
    it is still there (or not ours to ask), which is read as held."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True
    return True


def acquire_vault_lock():
    """Claim the one writer slot the wait-then-write holds. Two `pearde
    vault` runs waiting on the same Obsidian quit would both wake and both
    write the register — the second one now refuses instead, the way
    `claim` refuses a PRD someone already holds. A lock left by a process
    that is no longer running is dropped and retried once; a live one
    refuses."""
    for _ in range(2):
        try:
            fd = os.open(VAULT_LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            pid = None
            try:
                pid = int(open(VAULT_LOCK, encoding="utf-8").read().strip())
            except (OSError, ValueError):
                pass
            if pid is not None and _lock_holder_alive(pid):
                raise Refused(
                    "vault: the writer is already held — another `pearde "
                    f"vault` (pid {pid}) is waiting for Obsidian to quit")
            try:
                os.remove(VAULT_LOCK)   # a dead holder's lock — clear it
            except OSError:
                pass
            continue
        with os.fdopen(fd, "w") as f:
            f.write(str(os.getpid()))
        return
    raise Refused("vault: the writer is already held — another `pearde "
                  "vault` is waiting for Obsidian to quit")


def release_vault_lock():
    """Drop the lock, but only the copy this process wrote — a lock another
    run has since taken (ours was cleared as dead and re-claimed) is never
    this process's to remove."""
    try:
        held = open(VAULT_LOCK, encoding="utf-8").read().strip()
    except OSError:
        return
    if held == str(os.getpid()):
        try:
            os.remove(VAULT_LOCK)
        except OSError:
            pass


def wait_for_quit():
    """Block until Obsidian's process is gone, or raise Refused naming the
    process after the same timeout `--wait` has always carried. One code
    path: the flagless run and `--wait` both call this the moment Obsidian is
    found running, so the flag no longer decides whether the command waits
    — only `--wait` asked for it in words, the flagless run finds out from
    `obsidian_running()` instead."""
    print("vault: waiting for Obsidian to quit — the register is only "
          "writable while it is closed. Quit it now (⌘Q)…", flush=True)
    for _ in range(WAIT_TICKS):
        if not obsidian_running():
            break
        time.sleep(WAIT_TICK)
    else:
        raise Refused(f"Obsidian still running after "
                      f"{int(WAIT_TICKS * WAIT_TICK)}s — nothing written")
    time.sleep(1)                     # let the app finish its own last write


def cmd_vault(argv):
    """[<dir>] [--wait] [--open] — put the board in Obsidian's vault register,
    which is what makes `obsidian://open` resolve to it.

    The register (@resources/board/obsidian_register.py owns it) is read
    once, at launch, and written back
    from memory on quit. So an entry added under a running app is invisible to
    it and gone afterwards — the app answers "Unable to find a vault for the
    URL" and then erases the line. This command holds that order: it writes
    only while Obsidian is closed. Obsidian running is no longer a refusal —
    with no flag named it prints the quit instruction and waits for the same
    process exit `--wait` has always waited for, one code path either way.
    `--wait` keeps its meaning for a headless script (no TTY needed, still
    waits, still writes, still exits zero); `--open` launches the vault after
    writing. A second `pearde vault` started while the first is waiting
    refuses — the register is one writer at a time. The vault directory
    itself is seeded when it is not there yet."""
    args = trlib.Args(argv, FLAGS["vault"], "vault")
    d = os.path.abspath(args.pos[0] if args.pos else os.getcwd())
    board = planlib.board_at(d)
    if not os.path.isdir(board):
        raise Refused(f"no board at {board} — pearde init {d} writes one")
    if args.dry:
        want = [n for n in OBSIDIAN_PLUGINS if bundle_state(n) != "ok"]
        print(f"dry · would register {d} with Obsidian"
              + (f" · would fetch {', '.join(want)}" if want else "")
              + (" · seeds .obsidian/ first" if not os.path.isdir(
                  os.path.join(d, ".obsidian")) else "")
              + (f" · would move {board} out of the hidden name first"
                 if os.path.basename(board) == planlib.LEGACY_BOARD_DIR
                 else ""))
        return 0
    if unhide_board(d, args.opt.get("dir")):
        board = planlib.board_at(d)
        print(f"vault: the board is {board} now, with a {planlib.LEGACY_BOARD_DIR} "
              "symlink where it was — Obsidian shows no path holding a "
              "dot-segment, so a board with a dot in its name cannot be in "
              "the project's vault at all")
    # The bundles, before anything is copied anywhere. This is the one command
    # in the repo that reaches the network, and it does it only for what the
    # preset does not already hold at the pinned version.
    fetched, failed = ensure_bundles()
    if fetched:
        print(f"vault: fetched {', '.join(fetched)}")
    for line in failed:
        print(f"vault: could not fetch {line}")
    if not os.path.isdir(os.path.join(d, ".obsidian")):
        plugins, missing, _, stranded = write_obsidian(d)
        print(f"vault: seeded {d}/.obsidian"
              + (f" — plugins: {', '.join(plugins)}" if plugins else "")
              + (f" · no bundle for {', '.join(missing)}" if missing else ""))
        if stranded:
            print(f"vault: {stranded}")
    else:
        copied = copy_bundles(os.path.join(d, ".obsidian"))
        if copied:
            print(f"vault: put {', '.join(copied)} into {d}/.obsidian — "
                  "Obsidian loads a plugin on the next open of the vault")
    if obsidian_running():
        acquire_vault_lock()
        try:
            wait_for_quit()
            state, vid = register_vault(d, retire=board)
        finally:
            release_vault_lock()
    else:
        state, vid = register_vault(d, retire=board)
    if state is None:
        print("vault: Obsidian has no config on this machine — nothing to "
              "register. The vault directory is there for when it does")
        return 0
    uri = f"obsidian://open?vault={vid}"
    print(f"vault: {d} {'registered' if state == 'added' else 'already registered'}"
          f" as {os.path.basename(d)} · {uri}")
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
        raise Refused("upgrade [<dir>] [--dir <board-directory-name>]")
    d = os.path.abspath(args.pos[0] if args.pos else os.getcwd())
    into = args.opt.get("dir") or planlib.BOARD_DIR
    board = planlib.board_at(d)
    if not os.path.isfile(os.path.join(board, "settings.md")):
        raise Refused(f"no board at {board} — pearde init {d} writes one")
    name = planlib.board_name(board)
    if args.dry:
        print(f"dry · upgrade {name} — would seed wiki/ content, the vault, "
              "the gitignore names, the register, and regenerate wiki/board/"
              + (f" · would move {board} to {os.path.join(d, into)}"
                 if os.path.basename(board) == planlib.LEGACY_BOARD_DIR
                 else ""))
        return 0
    print(f"upgrade {name} · {board}")
    # The board out of the hidden name, before anything else reads a path:
    # every step below writes into the board, and the vault seeded at the end
    # can only show a board with no dot in its name.
    moved = unhide_board(d, into)
    if moved:
        board = planlib.board_at(d)
        print(f"  board     {'moved to ' + board if moved == 'moved' else board}"
              f" · {planlib.LEGACY_BOARD_DIR} is a symlink to it now, so every "
              "path spelled the old way still resolves")
    for folder in (planlib.PRDS_DIR, "memos", "wiki", "workflows",
                   planlib.STATE_DIR):
        os.makedirs(os.path.join(board, folder), exist_ok=True)
    planted = write_knowledge(d)
    print(f"  wiki      {'planted ' + ', '.join(planted) if planted else 'already seeded'}")
    # The memo kind-index, the same regeneration `init` does after its copy.
    # A board made before `index_memos` existed carries whatever index it had
    # — none at all, on every `--example` board older than that step — and
    # `memo check` calls that stale, which doctor's `memos` row reports as
    # broken. `upgrade`'s whole job is to bring a board current, so it does
    # here what `init` does there. Read the page before and after rather than
    # asking `index_memos`: the row then says which of the two happened, the
    # way `wiki` and `register` already do.
    memos_page = os.path.join(board, "memos", "README.md")
    before = (open(memos_page, "rb").read()
              if os.path.isfile(memos_page) else None)
    indexed = index_memos(board, "upgrade")
    if indexed:
        after = open(memos_page, "rb").read()
        print(f"  memos     {'already current' if after == before else 'regenerated'} "
              f"{indexed}, the index by kind")
    else:
        print("  memos     no memo on this board — nothing to index")
    # A board made before the grammar existed has no vocabulary file, which
    # doctor's `grammar` row reads `off` for the life of the board. `init`
    # plants it; bringing a board forward has to leave it as healthy as
    # making one fresh, and `plant_grammar` never overwrites a file that is
    # already there, so an existing vocabulary keeps every row.
    seeded = plant_grammar(board, "upgrade")
    if seeded:
        print(f"  grammar   wrote {seeded} — the board vocabulary is in it, "
              "this repo's words are yours to add")
    else:
        print("  grammar   already on this board")
    plugins, missing, _, stranded = write_obsidian(d)
    repaired = repair_plugin_ids(os.path.join(d, ".obsidian"))
    repaired += repair_ignore_filters(os.path.join(d, ".obsidian"),
                                      os.path.basename(board))
    repaired += repair_graph_view(os.path.join(d, ".obsidian"))
    vault_line = ", ".join(plugins) if plugins else "already there"
    vault_line = f"{d} as {os.path.basename(d)} · " + vault_line
    if repaired:
        vault_line += " · repaired " + "; ".join(repaired)
    if stranded:
        vault_line += " · " + stranded
    if missing:
        vault_line += (f" · no bundle for {', '.join(missing)} — "
                       "pearde vault fetches them")
    print(f"  vault     {vault_line}")
    if in_git(d):
        added = write_gitignore(d, board)
        print(f"  gitignore {'+= ' + ' '.join(added) if added else 'already names them'}")
    board_added = write_board_gitignore(board)
    if board_added:
        print(f"  board-git += {' '.join(board_added)} — the board is its own "
              "repo and was tracking its REST key")
    # even_if_running as in cmd_init: the branch below is the warning.
    state, _vid = obsreg.write(d, retire=board, even_if_running=True)
    if state is None:
        print("  register  Obsidian has no config on this machine")
    elif state == "added" and obsreg.running():
        print("  register  added — but Obsidian is running and rewrites its "
              "vault list from memory on quit, which erases this. "
              "pearde vault --wait --open, then quit it")
    else:
        print(f"  register  {'added' if state == 'added' else 'already registered'}")
    for verb, line in plant_graph(board):
        print(f"  {verb:<9} {line}")
    if repaired and obsreg.running():
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
