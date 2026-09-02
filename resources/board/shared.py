#!/usr/bin/env python3
"""shared — one copy per machine of what every lane regenerates.

    share [<board>] [--repo <path>] [--json]      what is shared, what is not
    share apply [<board>] [--dry]                 link them; seed from the first copy
    share undo [<board>] [--dry]                  put real directories back

A lane is a git worktree, and a worktree costs the bytes git tracks. On this
repo that is 2.1 MB across 174 files. The tree on disk was 273 MB across
15,992 files, and 27 lanes held 143 MB of it — because a lane regenerates its
own graphify cache, fetches its own Obsidian plugin bundles, installs its own
`node_modules`. **The checkout is not what eats the disk; the lane's own
output is**, and no filesystem trick reaches it: copy-on-write shares a block
until one side writes it, and each lane writes its own cache by construction,
so the divergence lands exactly where the disk goes. Measured 2026-09-02, an
APFS `clonefile` of this tree cost 176 MB against 809 MB for a plain copy —
real, and nowhere near free, because 11,766 of those files are under 4 KB and
a clone still allocates every inode and directory entry.

So the fix is not a filesystem. It is one copy of each regenerable directory,
in a place every worktree already shares, symlinked into each of them.

Where the store lives: `<git-common-dir>/pearde-shared/`. `git rev-parse
--git-common-dir` answers the SAME path from the checkout and from every
worktree of it, which is the whole reason it is the store — a lane needs no
configuration to find it. Nothing under `.git/` is ever walked by `git
status`, staged by `git add -A`, or removed by `git gc`; `git worktree remove`
deletes the lane's symlink and cannot reach through it.

**Only an ignored path is ever shared.** Every candidate is put to `git
check-ignore` in the tree that holds it, and a path git would track is refused
and reported, never linked — a symlink where git expects a file is a
modification on every `status` and a deletion on the next checkout. That check
is the one invariant here; the table below is only a list.

Seeding. The first tree to be linked moves its real directory into the store,
so nothing is refetched. A later tree with its own copy is merged in — files
the store does not have are copied over before its directory is dropped, so a
plugin bundle only one lane fetched survives. A tree with no copy yet gets an
empty store directory and a link, and whatever generates it next writes
straight into the shared copy.

Concurrency. The shared caches are content-addressed (`graphify/cache` keys on
a hash of the file and the extractor version) or install-once
(`node_modules`, the plugin bundles), so two lanes writing at once write
distinct paths or the same bytes. Nothing here is a lock, and nothing here
holds state a lane owns: `pearde/.state/`, the board and the specs stay
per-lane, as they must.

Python 3 stdlib only.
"""
import glob as globlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan as planlib          # noqa: E402
import transitions as trlib     # noqa: E402

STORE = "pearde-shared"
FLAGS = planlib.Flags(("board", "repo"), ("dry", "json"))


class Share:
    """One thing worth sharing. `pattern` is relative to a checkout root;
    `kind` is `dir` when the whole directory is one shared object, `glob`
    when every file the pattern matches is shared on its own; `key` is the
    path it takes IN THE STORE, which is the pattern unless two patterns
    name one object — the two board spellings do."""

    def __init__(self, pattern, kind, why, key=None):
        self.pattern, self.kind, self.why = pattern, kind, why
        self.key = key or pattern

    def __repr__(self):
        return f"<Share {self.pattern} {self.kind}>"


# One store key for the graphify cache, whichever way the board is spelled.
# `.pearde` is a symlink onto `pearde` in an upgraded CHECKOUT and both rows
# then resolve to one directory — but in a lane both are real directories, both
# rows fire, and before this key the store grew two caches that shared no
# entry. Measured 2026-09-02: 24 MB under `pearde/graphify/cache` beside 2.6 MB
# under `.pearde/graphify/cache`, across 29 of 30 trees. One copy per machine,
# twice, which is the duplication this module exists to remove.
CACHE_KEY = "pearde/graphify/cache"
RETIRED = ((".pearde/graphify/cache", CACHE_KEY),)

# The table. A row is regenerable — losing it costs a refetch, never work —
# and gitignored, which `git check-ignore` proves per tree before anything is
# linked. Both board spellings are listed: `pearde/` since 2026-09-02, and
# `.pearde/` the compatibility symlink and every board not yet upgraded.
SHARED = (
    Share("resources/board/node_modules", "dir",
          "playwright-core, fetched on demand for the js tests"),
    Share("pearde/graphify/cache", "dir",
          "graphify's AST cache — keyed on content hash and extractor version",
          key=CACHE_KEY),
    Share(".pearde/graphify/cache", "dir",
          "graphify's AST cache, on a board not yet upgraded",
          key=CACHE_KEY),
    Share("resources/board/obsidian/plugins/*/main.js", "glob",
          "third-party plugin bundles, pinned by `install --apply`"),
    Share("resources/board/obsidian/plugins/*/styles.css", "glob",
          "third-party plugin bundles, pinned by `install --apply`"),
    Share("resources/board/obsidian/plugins/*/manifest.json", "glob",
          "third-party plugin bundles, pinned by `install --apply`"),
)


class Refused(Exception):
    """Something a person has to decide. The message is what is printed."""


# ── where things are ──────────────────────────────────────────────────────────

def git(root, *args, check=False):
    try:
        r = subprocess.run(["git", "-C", root, *args],
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Refused(f"git {' '.join(args)}: {e}")
    if check and r.returncode != 0:
        raise Refused((r.stderr or r.stdout).strip()
                      or f"git {' '.join(args)} exit {r.returncode}")
    return r


def store_of(tree):
    """The shared store for whatever repo `tree` belongs to. Every worktree
    of one repo answers the same absolute path — that is what makes this a
    store and not another per-lane directory."""
    r = git(tree, "rev-parse", "--git-common-dir")
    if r.returncode != 0:
        raise Refused(f"{tree} is not a git worktree")
    d = r.stdout.strip()
    if not os.path.isabs(d):
        d = os.path.join(tree, d)
    return os.path.join(os.path.realpath(d), STORE)


def repo_root(tree):
    r = git(tree, "rev-parse", "--show-toplevel")
    return r.stdout.strip() if r.returncode == 0 else None


# The witness for a tree the shared table can reach. Every row hangs off
# `resources/board/`, and this is a module that directory has always held.
# `shared.py` would be the obvious marker and is the wrong one: a lane cut
# before this module landed still regenerates a `node_modules` and a graphify
# cache worth sharing, and 21 of the 31 lanes on this machine are such lanes.
MARKER = "resources/board/plan.py"


def main_worktree(tree):
    """The repo's MAIN worktree — the first one `git worktree list` names.

    `--show-toplevel` answers the worktree the path is IN, and on this machine
    the board is a LINKED worktree of this same repo on a branch of its own.
    So from the board it answers the board, from a lane it answers the lane,
    and the code checkout — the only tree that holds `resources/board/` — is
    named by neither. Every worktree of a repo can name the main one, which is
    why this is the resolution and `--show-toplevel` is not."""
    r = git(tree, "worktree", "list", "--porcelain")
    if r.returncode != 0:
        return None
    for line in r.stdout.splitlines():
        if line.startswith("worktree "):
            return os.path.realpath(line[len("worktree "):].strip())
    return None


def offers(tree):
    """Whether the shared table can ever be satisfied in this tree.

    Every row hangs off `resources/board/`, and a worktree of this repo on
    another branch holds none of it — the board is one. Surveying such a tree
    prints rows that are permanently `store-only`, and applying to it creates
    empty directories that satisfy nothing: measured on this machine, the board
    worktree grew `resources/board/obsidian/`, `pearde/graphify/` and
    `.pearde/graphify/` and shared not one byte."""
    return os.path.isfile(os.path.join(tree, MARKER))


def is_checkout(tree):
    """Whether this tree holds THIS module — what the label `checkout` means,
    and a stricter question than `offers`."""
    return os.path.isfile(os.path.join(tree, "resources", "board",
                                       os.path.basename(__file__)))


def ignored(tree, rel):
    """Does git ignore this path in this tree? `check-ignore` exits 0 when
    the path IS ignored, 1 when it is not, 128 on an error — and an error
    is not a yes."""
    return git(tree, "check-ignore", "-q", "--", rel).returncode == 0


def invisible(tree, rel):
    """Does git see nothing at this path? The gate every link actually
    passes, and NOT the same question as `ignored`.

    A pattern written `node_modules/` with the trailing slash matches a
    directory and only a directory. A symlink is not a directory, so the
    moment the real directory becomes a link git stops ignoring it and the
    lane grows an untracked entry on every `status` — measured, on this
    repo's own `resources/board/node_modules/`. `check-ignore` answers
    about the path as it is now and cannot see that coming; `status` after
    the fact is the only thing that can, which is why the link is written
    first and judged second."""
    r = git(tree, "status", "--porcelain", "--", rel)
    return r.returncode == 0 and not r.stdout.strip()


def ignore_hint(rel):
    """The .gitignore line that would let this path be a symlink — what a
    refusal owes the person reading it."""
    return (f"git would show the link — add `{rel}` to .gitignore, with no "
            "trailing slash, and run `pearde share apply` again")


def matched_pattern(r):
    """The pattern out of `check-ignore -v`, whose line is
    `<source>:<line>:<pattern>\\t<path>`. The empty string when it matched
    nothing."""
    if r.returncode != 0 or not r.stdout.strip():
        return ""
    field = r.stdout.splitlines()[0].split("\t")[0]
    return field.rsplit(":", 1)[-1].strip()


def refusal(tree, rel):
    """Why a symlink at `rel` would be visible to git here — the sentence a
    refusal owes the person reading it — or the empty string when it would
    not be.

    This is `invisible`'s question asked without writing anything.
    `invisible` links the path, reads `git status` and puts the tree back;
    a survey must write nothing, so it asks git about the ignore rules
    instead, and asks twice, because `check-ignore` answers about the path as
    it finds it on disk. A path that IS a directory is answered as one, so a
    match is read for the trailing slash that makes a pattern
    directory-only — `node_modules/` stops ignoring the path the moment the
    real directory becomes a link. A path that is not there is answered as a
    file, which is what a link is, so a miss is put again with the slash
    written on, and the pattern that then matches is the same defect. No
    pattern either way is the other refusal: nothing here ignores it at all."""
    r = git(tree, "check-ignore", "-v", "--", rel)
    pat = matched_pattern(r)
    if r.returncode == 0 and pat and not pat.endswith("/"):
        return ""                       # ignored as a link too — it can share
    if not pat:
        pat = matched_pattern(git(tree, "check-ignore", "-v", "--",
                                  rel.rstrip("/") + "/"))
    which = (f"`{pat}` ignores a directory and a symlink is not one — "
             if pat else "no .gitignore row here ignores it — ")
    return which + ignore_hint(rel)


def reachable(tree, rel):
    """Whether `link_one` would even try here. It skips a row whose top
    directory this tree does not hold — `pearde/graphify/cache` on a board
    spelled `.pearde/` — and a survey that judged such a row would report a
    refusal for a link nothing was ever going to write."""
    return os.path.lexists(os.path.join(tree, rel)) or \
        os.path.isdir(os.path.join(tree, rel.split("/")[0]))


def targets(tree):
    """Every (rel, kind, why, key) this tree offers — `rel` where it sits in
    the tree, `key` where it sits in the store. A `glob` row expands against
    what is on disk in the tree AND against what the store already holds, so
    a bundle no tree has fetched yet is still linked once one has."""
    out, store, seen_real = [], store_of(tree), set()
    for s in SHARED:
        if s.kind == "dir":
            # `.pearde` is a symlink onto `pearde` on an upgraded CHECKOUT, so
            # both spellings name ONE directory there and the second row would
            # report a duplicate — and report it wrong, because git reads a
            # path through a tracked symlink as tracked. The rows stay (a
            # board not yet upgraded has a real `.pearde/`, and in a lane both
            # spellings are real directories); the duplicate is dropped by
            # what the path actually resolves to, and where both survive they
            # share one `key` and so one copy in the store.
            real = os.path.realpath(os.path.join(tree, s.pattern))
            if real in seen_real:
                continue
            seen_real.add(real)
            out.append((s.pattern, "dir", s.why, s.key))
            continue
        seen = set()
        for base in (tree, store):
            for p in globlib.glob(os.path.join(base, s.pattern)):
                rel = os.path.relpath(p, base).replace(os.sep, "/")
                if rel not in seen:
                    seen.add(rel)
                    out.append((rel, "file", s.why, rel))
    return out


# ── the state of one path ─────────────────────────────────────────────────────

def state(tree, rel, key=None):
    """What `rel` is in `tree`, against the store copy at `key`. One of:

        linked      a symlink onto this store's copy — done
        stale       a symlink onto a RETIRED key of this same store
        foreign     a symlink somewhere else — left alone, never rewritten
        local       a real file or directory, not shared yet
        refused     git would show the link — .gitignore names it with a
                    trailing slash, or names it nowhere at all; no apply
                    will change that until a row is added
        store-only  the store has it, the tree does not
        absent      neither has it
        tracked     git would track it here — refused, never linked

    `refused` is the answer `apply` used to be the only thing that could
    reach: it writes the link, reads `git status`, puts the tree back and
    prints the reason. A survey must write nothing, so it reads the pattern
    instead — see `refusal`. A tree already `linked` is never re-judged.
    """
    store = store_of(tree)
    dst = os.path.join(store, key or rel)
    src = os.path.join(tree, rel)
    here = os.path.lexists(src)
    if here and os.path.islink(src):
        try:
            real = os.path.realpath(src)
        except OSError:
            return "foreign"
        if real == os.path.realpath(dst):
            return "linked"
        return "stale" if real.startswith(store + os.sep) else "foreign"
    if here and not ignored(tree, rel):
        return "tracked"
    if (here or os.path.exists(dst)) and reachable(tree, rel) \
            and refusal(tree, rel):
        return "refused"
    if here:
        return "local"
    return "store-only" if os.path.exists(dst) else "absent"


def bytes_of(path):
    if os.path.islink(path) or not os.path.exists(path):
        return 0
    if os.path.isfile(path):
        try:
            return os.path.getsize(path)
        except OSError:
            return 0
    n = 0
    for root, dirs, files in os.walk(path, followlinks=False):
        for f in files:
            p = os.path.join(root, f)
            if not os.path.islink(p):
                try:
                    n += os.path.getsize(p)
                except OSError:
                    pass
    return n


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0


# ── linking ───────────────────────────────────────────────────────────────────

def merge_into(src, dst):
    """Everything under `src` the store does not already hold. The store
    wins every collision — it is the copy every other tree is about to point
    at, and a lane's half-written cache entry must not overwrite it."""
    added = 0
    if os.path.isfile(src):
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            added += 1
        return added
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        out = dst if rel == os.curdir else os.path.join(dst, rel)
        os.makedirs(out, exist_ok=True)
        for f in files:
            a, b = os.path.join(root, f), os.path.join(out, f)
            if not os.path.exists(b):
                shutil.copy2(a, b)
                added += 1
    return added


def relative_link(src, dst):
    """The link `src` → `dst`, written relative so the store survives the
    repo being moved. Both are absolute on the way in."""
    return os.path.relpath(dst, os.path.dirname(src))


def link_one(tree, rel, kind, dry=False, key=None):
    """Make `tree/rel` a link onto the store copy at `key`. Returns
    (action, note).

    Actions: `linked` (already), `seeded` (this tree's copy became the
    store's), `merged` (its extra files were kept, then it was dropped),
    `attached` (linked onto a store copy it did not have), `created` (an
    empty store copy, so the next generator writes into the store),
    `refused` (git would track it, or would show the link), `foreign`
    (someone else's symlink)."""
    key = key or rel
    st = state(tree, rel, key)
    if st == "linked":
        return "linked", ""
    if st == "tracked":
        return "refused", "git tracks this path here"
    if st == "refused":
        return "refused", refusal(tree, rel)
    if st == "foreign":
        return "foreign", "already a symlink elsewhere — left alone"
    if not reachable(tree, rel):
        # A row whose top directory this tree does not hold. Linking it would
        # create that directory to hang the link in — `.pearde/` in a tree
        # spelled `pearde/`, and the other way round — which is inventing
        # dirt, not sharing anything. Measured: an empty untracked directory
        # that `git status` then reported forever.
        return "skipped", "no such tree here"

    store = store_of(tree)
    dst, src = os.path.join(store, key), os.path.join(tree, rel)
    if st == "stale":
        # Our own link, onto a key this module no longer keeps a copy at.
        # It is not the tree's work and never was — drop it and re-link.
        if dry:
            return "attached", f"re-linked off the retired {os.path.relpath(os.path.realpath(src), store)}"
        os.remove(src)
        st = "store-only" if os.path.exists(dst) else "absent"
    if st == "absent" and kind != "dir":
        # A directory nothing has made yet is worth pre-creating, so the next
        # generator writes into the store. A file is not: there is nothing to
        # point at and nothing will write through the link.
        return "skipped", "nothing to share yet"
    if dry:
        return {"local": "seeded" if not os.path.exists(dst) else "merged",
                "store-only": "attached",
                "absent": "created"}[st], ""

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    note, action, backup = "", "", None
    if st == "local":
        backup = dst + ".seeding"
        if not os.path.exists(dst):
            shutil.move(src, dst)           # the tree's copy IS the store's
            action = "seeded"
        else:
            added = merge_into(src, dst)
            shutil.move(src, backup)        # kept until the link is judged
            action = "merged"
            note = f"{added} file(s) the store did not have" if added else ""
    elif st == "store-only":
        action = "attached"
    else:
        os.makedirs(dst, exist_ok=True)
        action = "created"

    os.makedirs(os.path.dirname(src), exist_ok=True)
    if os.path.lexists(src):                # a race, or a stale link
        if os.path.islink(src):
            os.remove(src)
        else:
            raise Refused(f"{rel}: reappeared under me — run `share` again")
    os.symlink(relative_link(src, dst), src)

    # The invariant, judged after the fact because only `git status` can
    # answer it (see `invisible`). A link git would show is worse than the
    # duplication it saves, so the tree is put back exactly as it was —
    # its own copy where it had one, nothing at all where it had nothing.
    if not invisible(tree, rel):
        os.remove(src)
        if st == "local":
            if backup and os.path.exists(backup):
                shutil.move(backup, src)
            elif action == "seeded":
                shutil.move(dst, src)       # the store never held it before
        return "refused", ignore_hint(rel)
    if backup and os.path.exists(backup):
        shutil.rmtree(backup) if os.path.isdir(backup) else os.remove(backup)
    return action, note


def unlink_one(tree, rel, dry=False, key=None):
    """Put a real copy back where the link is. The store keeps its copy —
    `undo` is an escape hatch, not a teardown."""
    if state(tree, rel, key) != "linked":
        return "skipped", "not linked here"
    src = os.path.join(tree, rel)
    dst = os.path.realpath(src)
    if dry:
        return "unlinked", ""
    os.remove(src)
    if os.path.isdir(dst):
        shutil.copytree(dst, src)
    else:
        shutil.copy2(dst, src)
    return "unlinked", ""


# ── the trees a board covers ──────────────────────────────────────────────────

def find_repo(arg=None):
    """The code repo this call is about: the path given, else the repo the
    cwd is in. A board is not required — the store belongs to the repo, and
    a repo with no board still has a checkout worth sharing."""
    start = os.path.abspath(arg or os.getcwd())
    root = repo_root(start)
    if not root:
        raise Refused(f"not inside a git repo: {start}")
    return os.path.realpath(root)


def find_board_soft(arg=None):
    """The board, or None. `share` needs one only to enumerate lanes, so a
    repo without a board is answered rather than refused — and `die`'s
    message is swallowed with the exit, because "no board here" is not
    something this command has to say."""
    import contextlib
    import io
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            return planlib.find_board(arg)
    except SystemExit:
        return None


def find_checkout(arg=None):
    """The code checkout this call is about. `find_repo` answers the worktree
    the path is IN, and the board is a linked worktree of this same repo on a
    branch of its own — so from the board, and from a lane, that is a tree
    holding no `resources/board/` at all. The main worktree is the one that
    does, and every worktree of the repo can name it."""
    here = find_repo(arg)
    return main_worktree(here) or here


def root_of(board, repo=None):
    """The tree every label is relative to — the checkout, whether or not it
    is itself worth surveying. `trees` may drop it; the store and the labels
    still hang off it, so it is resolved separately and never read off
    `trees()[0]`."""
    return os.path.realpath(repo) if repo else find_checkout(board)


def trees(board, repo=None):
    """The checkout and every lane under the board, each a worktree root —
    and only those the shared table can reach, which `offers` decides. With no
    board there are no lanes, and the checkout alone is the answer. A lane
    whose directory is gone is skipped, not reported — `sweep` owns that."""
    import lanes as laneslib
    root = root_of(board, repo)
    out = [root] if offers(root) else []
    if not board:
        return out
    d = os.path.join(board, laneslib.LANES_DIR)
    if os.path.isdir(d):
        for slug in sorted(os.listdir(d)):
            p = os.path.join(d, slug)
            if os.path.isdir(p) and os.path.exists(os.path.join(p, ".git")) \
                    and offers(p):
                out.append(os.path.realpath(p))
    return out


def label(tree, root):
    """What a tree is called in the output. The checkout is `checkout`; a
    lane is its slug, because a lane's path is the board path plus a slug
    long enough to wrap a terminal twice and the slug is the only part that
    identifies it. A tree that is neither — a repo given by `--repo`,
    somewhere else entirely — keeps its path."""
    rel = os.path.relpath(tree, root)
    if rel == os.curdir:
        return "checkout"
    if rel.startswith(os.pardir):
        return tree
    parts = rel.split(os.sep)
    return parts[-1] if LANES_MARK in parts else rel


LANES_MARK = ".lanes"


# ── the command ───────────────────────────────────────────────────────────────

def survey(board, repo=None):
    """One row per (tree, target): its state and what it costs unshared."""
    rows, root = [], root_of(board, repo)
    for t in trees(board, repo):
        for rel, kind, why, key in targets(t):
            st = state(t, rel, key)
            note = refusal(t, rel) if st == "refused" else ""
            rows.append({"tree": label(t, root), "path": t, "rel": rel,
                         "key": key, "kind": kind, "state": st, "why": why,
                         "note": note,
                         "bytes": bytes_of(os.path.join(t, rel))
                         if st in ("local", "tracked") else 0})
    return rows


def apply_tree(tree, dry=False, undo=False, name=None):
    """Share (or un-share) every target in ONE worktree. The unit `lanes`
    calls on a fresh lane, and the unit `apply` loops."""
    out = []
    for rel, kind, why, key in targets(tree):
        try:
            if undo:
                action, note = unlink_one(tree, rel, dry, key)
            else:
                action, note = link_one(tree, rel, kind, dry, key)
        except (OSError, Refused) as e:
            action, note = "failed", str(e)
        out.append({"tree": name or tree, "rel": rel,
                    "action": action, "note": note})
    return out


def retire(store, dry=False):
    """Fold every store copy at a key this module no longer uses into the one
    that survives, then drop it. One shared object is one store path; a second
    path holding a second copy of it is the very duplication the store exists
    to remove, moved from the lanes into the store. Nothing is lost — the
    surviving copy wins every collision and the entries it does not have are
    copied over first."""
    out = []
    for old, new in RETIRED:
        a, b = os.path.join(store, old), os.path.join(store, new)
        if not os.path.isdir(a) or os.path.islink(a) or a == b:
            continue
        if dry:
            out.append({"tree": "store", "rel": old, "action": "retired",
                        "note": f"would fold into {new}"})
            continue
        added = merge_into(a, b) if os.path.isdir(b) else 0
        if not os.path.isdir(b):
            os.makedirs(os.path.dirname(b), exist_ok=True)
            shutil.move(a, b)
        else:
            shutil.rmtree(a)
        d = os.path.dirname(a)                  # the shell the key hung in
        while os.path.isdir(d) and not os.listdir(d) and d.startswith(store):
            os.rmdir(d)
            d = os.path.dirname(d)
        out.append({"tree": "store", "rel": old, "action": "retired",
                    "note": f"folded into {new}"
                            + (f" — {added} entry(ies) kept" if added else "")})
    return out


def apply(board, repo=None, dry=False, undo=False):
    ts, root = trees(board, repo), root_of(board, repo)
    out = [] if undo else retire(store_of(root), dry)
    for t in ts:
        out += apply_tree(t, dry, undo, name=label(t, root))
    return out


def cmd_share(argv):
    """one copy per machine of what every lane regenerates"""
    try:
        a = trlib.Args(argv, FLAGS, "share")
    except trlib.FlagRefused as e:
        print(f"pearde share: {e}", file=sys.stderr)
        return 2
    verb = a.pos[0] if a.pos and a.pos[0] in ("status", "apply", "undo") \
        else "status"
    rest = a.pos[1:] if (a.pos and a.pos[0] == verb) else a.pos

    # The repo is the subject; the board only names the lanes. `--repo` is
    # therefore resolved FIRST and the board is looked for inside it — a
    # board found by walking up from the cwd would otherwise hand this
    # call another repo's lanes, which is what it did once.
    try:
        if a.opt.get("repo"):
            repo = find_repo(a.opt["repo"])
            board = find_board_soft(a.opt.get("board") or repo)
            if board and not os.path.realpath(board).startswith(repo):
                board = None
        else:
            where = a.opt.get("board") or (rest[0] if rest else None)
            board = find_board_soft(where)
            # `find_checkout`, not `find_repo`: the board is a linked worktree
            # of this repo on its own branch, so `--show-toplevel` from it —
            # and from any lane — answers a tree that holds no `resources/`
            # at all, and the checkout was surveyed by no call that did not
            # pass `--repo`. `--repo` still means exactly the tree it names.
            repo = find_checkout(board or where)
    except Refused as e:
        print(f"pearde share: {e}", file=sys.stderr)
        return 1

    try:
        if verb == "status":
            rows = survey(board, repo)
            if "json" in a.flags:
                json.dump({"store": store_of(root_of(board, repo)),
                           "rows": rows}, sys.stdout, indent=1)
                print()
                return 0
            return print_status(board, repo, rows)
        rows = apply(board, repo, dry=a.dry, undo=(verb == "undo"))
        if "json" in a.flags:
            json.dump(rows, sys.stdout, indent=1)
            print()
        else:
            print_apply(rows, a.dry, verb)
        return 1 if any(r["action"] == "failed" for r in rows) else 0
    except Refused as e:
        print(f"pearde share: {e}", file=sys.stderr)
        return 1


DONE = {"linked", "seeded", "merged", "attached", "created", "unlinked"}


# Every state, in the order the summary reads them, with the words it uses.
# The summary is built from this tuple and nothing else, so it accounts for
# every row surveyed — a state left out of a hand-written line is a tree the
# count cannot see, which is how 27 refused lanes once read as `0 refused`.
WORDS = (("linked", "shared"),
         ("local", "not yet"),
         ("refused", "refused (git would show the link)"),
         ("tracked", "refused (git tracks them)"),
         ("stale", "linked to a retired store path"),
         ("foreign", "someone else's link"),
         ("store-only", "in the store only"),
         ("absent", "not here"))


def print_status(board, repo, rows):
    store = store_of(root_of(board, repo))
    counts = {}
    for r in rows:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    waste = sum(r["bytes"] for r in rows if r["state"] == "local")
    print(f"store: {store}"
          + ("" if os.path.isdir(store) else "  (not created yet)"))
    if os.path.isdir(store):
        print(f"held:  {human(bytes_of(store))} in one copy")
    by_tree = {}
    for r in rows:
        by_tree.setdefault(r["tree"], []).append(r)
    for tree, rs in by_tree.items():
        loose = [r for r in rs if r["state"] not in ("linked", "absent")]
        if not loose:
            continue
        print(f"\n{tree}")
        for r in sorted(loose, key=lambda x: -x["bytes"]):
            size = f"  {human(r['bytes'])}" if r["bytes"] else ""
            print(f"  {r['state']:<11} {r['rel']}{size}")
            if r.get("note"):
                print(f"  {'':<11} {r['note']}")
    seen = {k for k, _ in WORDS}
    for k in sorted(counts):
        if k not in seen:                       # a state added and not worded
            print(f"\nunaccounted state `{k}`: {counts[k]} row(s)")
    print("\n" + " · ".join(f"{counts.get(k, 0)} {w}" for k, w in WORDS))
    print(f"= {sum(counts.get(k, 0) for k, _ in WORDS)} "
          f"of {len(rows)} row(s) surveyed")
    if waste:
        print(f"duplicated on disk: {human(waste)} — `pearde share apply` "
              "leaves one copy")
    elif counts.get("local"):
        print("`pearde share apply` links them")
    return 0


def print_apply(rows, dry, verb):
    pre = "dry · " if dry else ""
    changed = [r for r in rows if r["action"] not in ("linked", "skipped")]
    for r in changed:
        note = f" — {r['note']}" if r["note"] else ""
        print(f"{pre}{r['action']:<9} {r['tree']}/{r['rel']}{note}")
    ok = sum(1 for r in rows if r["action"] in DONE)
    bad = [r for r in rows if r["action"] in ("failed", "refused")]
    word = "would be" if dry else "are"
    print(f"{pre}{ok} path(s) {word} "
          + ("real again" if verb == "undo" else "shared") + ".")
    for r in bad:
        print(f"{pre}{r['action']}: {r['tree']}/{r['rel']} — {r['note']}",
              file=sys.stderr)


cmd_share.flags = FLAGS         # what `pearde share --help` prints
COMMANDS = {"share": cmd_share}


if __name__ == "__main__":
    sys.exit(cmd_share(sys.argv[1:]))
