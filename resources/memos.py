#!/usr/bin/env python3
"""pearde memos — the board's decision records: read them, and check them.

    python3 memos.py check [board]      one problem per line; silent when clean
    python3 memos.py list  [board]      slug · kind · status · date · subject
    python3 memos.py add   <subject> [board] [--kind <kind>]
                                        slug it, write the memo from the template, print the path
    python3 memos.py verify [slug] [board]
                                        run every invariant's `verify:` command; non-zero = broken
    python3 memos.py index [board]      regenerate memos/README.md, the index by kind
    python3 memos.py retag [board]      rewrite every `tags:` from its own kind and status

A memo is `.pearde/memos/<slug>.md`. It is not a PRD: no state, never claimed,
never dispatched, invisible to the loop and to the progress line. It records
what was decided and what it beat. @references/memo.md is the format. This
file is its only reader, so the format has one home.

Python 3 stdlib only. @resources/board/plan.py and @resources/board/serve.py
import `scan` from here rather than growing a second frontmatter parser; the
parser, the board resolver and the record directory are @resources/common.py's.
"""
import datetime
import os
import re
import subprocess
import sys

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import common  # noqa: E402
from common import ISO_RE  # noqa: E402,F401 — @resources/workflows.py imports it from here

PROG = "memos"
REQUIRED = ("memo", "kind", "status", "subject", "date")
OPTIONAL = ("updated", "prds", "supersedes", "superseded_by", "verify",
            "tags")
KINDS = ("decision", "note", "invariant")
STATUSES = ("open", "decided", "superseded")
# The index groups in this order — invariants first, because they bind now;
# a kind outside the set lands under "Unsorted", where check() names it.
SECTIONS = (("invariant", "Invariants"), ("decision", "Decisions"),
            ("note", "Notes"))


def parse(path):
    """(frontmatter, title, body) of the file at `path`, in the board's
    dialect. frontmatter is None when the fence is missing or unterminated —
    the caller reports that, it is not a crash."""
    return common.parse_frontmatter(open(path, encoding="utf-8").read())


def find_board(arg):
    return common.find_board(arg, PROG)


def board_above(d):
    return common.board_above(d, PROG)


def collection(board):
    """The board's memos as a @resources/common.py `Collection`: at
    `.pearde/memos/` unless `memos:` in .pearde/settings.md points elsewhere
    — a repo whose decisions already live in another system mirrors that
    dir read-only instead of moving files another tool owns. External
    means foreign contract: the strict frontmatter gate applies only to
    the board's own memos/."""
    return common.Collection(board, "memos", "memos", REQUIRED, OPTIONAL,
                             "README.md", noun="memo")


def memos_dir(board):
    """(path, external) — what @resources/doctor.sh asks."""
    c = collection(board)
    return c.dir, c.external


def scan(board):
    """{slug: memo} for every .pearde/memos/*.md. Sorted by date descending, then
    slug — newest decision first, which is the order a reader wants."""
    out = collection(board).scan()
    for m in out.values():
        fm = m["fm"]
        m.update(kind=fm.get("kind", ""), status=fm.get("status", ""),
                 subject=fm.get("subject", ""), date=fm.get("date", ""))
    return dict(sorted(out.items(),
                       key=lambda kv: (str(kv[1]["date"]), kv[0]), reverse=True))


def board_prds(board):
    # A memo's `prds:` reference is a PRD name relative to the board's
    # `.pearde/prds/`, not to the board — so the walk starts there. Before the board
    # moved from `<repo>/prds` to `<repo>/.pearde` the two were the same
    # directory and this distinction did not exist.
    # relpath is OS-native (`\` on Windows); every `prds:` reference in a
    # memo is written `/`, the project's own convention — normalize so the
    # comparison in `check()` is not a silent path-separator mismatch.
    root = os.path.join(board, "prds")
    if not os.path.isdir(root):
        return set()
    return {os.path.relpath(r, root).replace(os.sep, "/")
            for r, ds, fs in os.walk(root)
            if "prd.md" in fs and r != root}


def _listed(v):
    return v if isinstance(v, list) else [v] if v else []


def check(board):
    """Every problem, one string each. Empty means the memos are clean.
    An external memo dir is another system's contract: only what is universal
    is checked — the file parses, the required five are present — and its own
    vocabulary (kinds, statuses, extra keys) is left alone."""
    coll = collection(board)
    memos, bad = scan(board), []
    if coll.external and not os.path.isdir(coll.dir):
        return [f"settings.md: `memos: …` points at {coll.dir}, which does not exist"]
    prds = board_prds(board)
    for slug in sorted(memos):
        m, at = memos[slug], f"{slug}.md"
        bad += coll.check_fence(m)
        if not m["parsed"]:
            continue
        fm = m["fm"]
        if coll.external:
            bad += coll.check_keys(m, closed=False)
            continue
        bad += coll.check_keys(m, slug_key="memo")
        if fm.get("kind") and fm["kind"] not in KINDS:
            bad.append(f"{at}: kind `{fm['kind']}` — the set is {'|'.join(KINDS)}")
        ver = fm.get("verify")
        if fm.get("kind") == "invariant":
            if not ver or isinstance(ver, list):
                bad.append(f"{at}: kind invariant with no `verify:` command — "
                           "an invariant nobody can run is a claim")
        elif "verify" in fm:
            bad.append(f"{at}: `verify:` on kind `{fm.get('kind')}` — "
                       "only an invariant carries a check")
        st = fm.get("status")
        if st and st not in STATUSES:
            bad.append(f"{at}: status `{st}` — the set is {'|'.join(STATUSES)}")
        want = memo_tags(m["kind"], m["status"])
        have = _listed(fm.get("tags"))
        if have != want:
            bad.append(f"{at}: `tags:` is {have or 'missing'}, derived from "
                       f"this memo's own kind and status it is {want} — "
                       "`memos.py retag` writes it")
        bad += coll.check_dates(m)
        sb = _listed(fm.get("superseded_by"))
        if st == "superseded" and not sb:
            bad.append(f"{at}: status superseded, naming nothing in its place")
        if sb and st != "superseded":
            bad.append(f"{at}: superseded_by is set, status is `{st}`")
        for k in ("supersedes", "superseded_by"):
            for name in _listed(fm.get(k)):
                if name not in memos:
                    bad.append(f"{at}: `{k}: {name}` names no memo")
        for name in _listed(fm.get("prds")):
            if name not in prds:
                bad.append(f"{at}: `prds: {name}` is not a PRD on this board")
    if not coll.external:
        idx = os.path.join(coll.dir, "README.md")
        have = (open(idx, encoding="utf-8").read()
                if os.path.isfile(idx) else None)
        if (memos or have is not None) and have != render_index(memos):
            bad.append("README.md: the kind index is stale — run `memo index`")
    return bad


def render_index(memos):
    """memos/README.md, the index by kind — generated, never edited, so it
    cannot go stale the way a maintained list does. Grouped by SECTIONS,
    newest first within each (scan's order). scan() skips README.md, so the
    index is not itself a memo."""
    lines = ["# Memos",
             "",
             "<!-- Generated by `memo index` and rewritten by `memo add`;",
             "     `memo check` fails on a stale index. Do not edit. -->"]
    known = {k for k, _ in SECTIONS}
    groups = list(SECTIONS) + [(None, "Unsorted")]
    for kind, heading in groups:
        rows = [m for m in memos.values()
                if (m["kind"] == kind if kind else m["kind"] not in known)]
        if not rows:
            continue
        lines += ["", f"## {heading}", ""]
        for m in rows:
            lines.append(f"- [{m['slug']}]({m['slug']}.md) — "
                         f"{m['status']} · {m['date']} — {m['subject']}")
    return "\n".join(lines) + "\n"


def write_index(board):
    """Regenerate the index and return its path. Refuses an external
    `memos:` dir — that mirror is read-only, nothing is written there."""
    coll = collection(board)
    if coll.external:
        print(f"memos: settings.md points `memos:` at {coll.dir} — another "
              "system's records, mirrored read-only; no index is written there",
              file=sys.stderr)
        sys.exit(1)
    return coll.write("README.md", render_index(scan(board)))


def binding(board, only=None):
    """[(slug, memo)] — every invariant that binds now, in slug order. `kind:
    invariant` and a status other than `superseded`; a superseded one records
    a rule that has been replaced and no longer holds anything to account.
    The one place that answers "which rules bind" — `verify` prints them and
    @resources/board/collect.py refuses on them, and two readers asking the
    same question ask it here."""
    memos = scan(board)
    return [(sl, m) for sl, m in memos.items()
            if m["kind"] == "invariant" and m["status"] != "superseded"
            and (not only or sl == only)]


def run_invariants(board, only=None):
    """[(slug, cmd, exit, output)] — every binding invariant run, nothing
    printed. cwd is the repo root (the board's parent), so a command is
    written the way the PRD contract's `verify:` is, and stdout and stderr
    come back in one stream in the order a reader saw them.

    An invariant with no `verify:` command is exit 1 here, not a skip: the
    memo claims a rule binds and hands nothing that proves it, and a rule
    that cannot be checked is indistinguishable from one that is broken.
    `check` already refuses that memo, so this only fires on a board whose
    check is red.

    This is the runner both readers share. `verify` below is its printer;
    `collect` reads the exit codes to refuse a landing, and needs the whole
    output rather than the one tail line a person reads."""
    root = os.path.dirname(board)
    out = []
    for sl, m in binding(board, only):
        cmd = m["fm"].get("verify")
        if not cmd or isinstance(cmd, list):
            out.append((sl, cmd if isinstance(cmd, str) else "",
                        1, "BROKEN — no `verify:` command"))
            continue
        try:
            r = subprocess.run(cmd, shell=True, cwd=root,
                               capture_output=True, text=True)
        except OSError as e:                # a cwd that is gone, a dead shell
            out.append((sl, cmd, 127, str(e)))
            continue
        out.append((sl, cmd, r.returncode, r.stdout + r.stderr))
    return out


def verify(board, only=None):
    """Run every binding invariant's `verify:` command — status superseded no
    longer binds and is skipped. cwd is the repo root (the board's parent), so
    a command is written the way the PRD contract's `verify:` is. Prints one
    line per invariant; returns the broken slugs."""
    ran = run_invariants(board, only)
    broken = []
    for sl, _cmd, code, output in ran:
        if code == 0:
            print(f"{sl}: holds")
            continue
        tail = output.strip().splitlines()
        if tail and tail[-1].startswith("BROKEN"):
            print(f"{sl}: {tail[-1]}")
        else:
            why = f" — {tail[-1]}" if tail else ""
            print(f"{sl}: BROKEN (exit {code}){why}")
        broken.append(sl)
    if only and not ran:
        print(f"memos: `{only}` names no binding invariant", file=sys.stderr)
        sys.exit(2)
    if not only and not ran:
        print("no invariants on this board")
    return broken


def slug(subject):
    """The rule of @references/parts/handles.md: lowercase, spaces to
    hyphens — every run of anything else collapses to one hyphen."""
    return re.sub(r"[^a-z0-9]+", "-", subject.lower()).strip("-")


# --- tags: derived, never authored -------------------------------------------

# `tags:` is the one memo key nobody writes by hand. Obsidian's graph view
# colours by tag and cannot query a property, so the kind and status a memo
# already carries have to reach the graph as tags — and two fields that must
# agree are one field that can disagree, which is why this one is generated
# from the other two on every `add` and every `retag`, and why `check` calls
# a memo whose tags drift from its own kind and status a problem.
# The character set is Obsidian's: a tag ends at the first character outside
# it, so a value with a space would silently become a shorter tag.
TAG_SAFE = re.compile(r"[^A-Za-z0-9_/-]+")


def tag(value):
    """One frontmatter value as a tag body — lowercased, unsafe runs folded to
    `-`. Empty in, empty out; the caller drops it."""
    return TAG_SAFE.sub("-", str(value or "").strip().lower()).strip("-")


def memo_tags(kind, status):
    """The tags a memo carries: `memo`, then one axis per field the format
    gives it. Derived from the fields, so a tag cannot outlive the value it
    names."""
    out = ["memo"]
    for name, value in (("kind", kind), ("status", status)):
        body = tag(value)
        if body:
            out.append(f"{name}/{body}")
    return out


def retag_text(text, tags):
    """`text` with its `tags:` block rewritten to `tags`, written after
    `status:` when it has none. Returns (text, changed) —
    @resources/common.py `set_list_key`, bound to the memo's own key;
    @resources/workflows.py calls it too."""
    return common.set_list_key(text, "tags", tags, after="status")


def retag(board):
    """Rewrite every memo's `tags:` from its own kind and status. Returns the
    slugs it changed. An external memos dir is another system's contract and
    is left alone — the same exemption `check` makes."""
    coll = collection(board)
    if coll.external or not os.path.isdir(coll.dir):
        return []
    changed = []
    for slug_, m in scan(board).items():
        if not m["parsed"]:
            continue
        text = open(m["path"], encoding="utf-8").read()
        out, did = retag_text(text, memo_tags(m["kind"], m["status"]))
        if did:
            common.atomic_write(m["path"], out)
            changed.append(slug_)
    return sorted(changed)


def add(board, subject, kind="decision"):
    """Write `<memos>/<slug>.md` from @references/templates/memo.md and
    return its path. Line-based: `memo:`, `kind:`, `subject:`, `date:` and
    the title line are filled in; every other template line is kept — the
    reader fills the sections, @references/templates/memo.doc.md says how. An invariant gets a
    bare `verify:` line, which fails `check` until the command is written and
    run — an invariant is filed proven, never on faith. The `tags:` block is
    derived from the kind and status just written, the same lines `retag`
    would produce. Rewrites the index.
    Exits 2 on a subject that slugs to nothing or a kind outside the set, 1
    on a path that exists or a `memos:` dir that is another system's — that
    dir is mirrored read-only, nothing is written there."""
    if kind not in KINDS:
        print(f"memos: kind `{kind}` — the set is {'|'.join(KINDS)}",
              file=sys.stderr)
        sys.exit(2)
    subject = subject.strip()
    sl = slug(subject)
    if not sl:
        print(f"memos: `{subject}` slugs to nothing", file=sys.stderr)
        sys.exit(2)
    coll = collection(board)
    if coll.external:
        print(f"memos: settings.md points `memos:` at {coll.dir} — another "
              "system's records, mirrored read-only; write the memo there",
              file=sys.stderr)
        sys.exit(1)
    path = os.path.join(coll.dir, sl + ".md")
    if os.path.exists(path):
        print(f"memos: {path} exists", file=sys.stderr)
        sys.exit(1)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tpl = open(os.path.join(root, "references", "templates", "memo.md"),
               encoding="utf-8").read()
    today = datetime.date.today().isoformat()
    out = []
    for line in tpl.splitlines():
        if line.startswith("memo: <slug>"):
            line = f"memo: {sl}"
        elif line.startswith("kind: ") and kind != "decision":
            line = f"kind: {kind}"
        elif line.startswith("subject: "):
            line = f"subject: {subject}"
        elif line.startswith("date: "):
            line = f"date: {today}"
            if kind == "invariant":
                line += "\nverify: "
        elif line.startswith("# <slug> — "):
            line = f"# {sl} — {subject}"
        out.append(line)
    text = "\n".join(out) + "\n"
    fm, _, _ = common.parse_frontmatter(text)
    text, _ = retag_text(text, memo_tags(fm.get("kind"), fm.get("status")))
    coll.write(sl + ".md", text)
    write_index(board)
    return path


def main(argv):
    try:
        kind, args = common.pop_flag(argv[1:], "--kind")
    except ValueError:
        print("memos: --kind needs a value", file=sys.stderr)
        return 2
    if kind is None:
        kind = "decision"
    cmd = args[0] if args else "check"
    if cmd == "add":
        if len(args) < 2 or not args[1].strip():
            print("memos: add <subject> [board] [--kind <kind>]",
                  file=sys.stderr)
            return 2
        board = find_board(args[2] if len(args) > 2 else None)
        print(add(board, args[1], kind))
        return 0
    if cmd == "verify":
        # verify [slug] [board] — a slug never contains a path separator and
        # is never a directory on disk, which is how the two are told apart.
        only, at = None, None
        for a in args[1:]:
            if os.sep in a or a in (".", "..") or os.path.isdir(a):
                at = a
            else:
                only = a
        return 1 if verify(find_board(at), only) else 0
    board = find_board(args[1] if len(args) > 1 else None)
    if cmd == "check":
        bad = check(board)
        if bad:
            print("\n".join(bad))
        return 1 if bad else 0
    if cmd == "index":
        print(write_index(board))
        return 0
    if cmd == "retag":
        done = retag(board)
        print(f"retag: {len(done)} memo(s) rewritten"
              + (" — " + ", ".join(done) if done else " (all current)"))
        return 0
    if cmd == "list":
        for m in scan(board).values():
            print(f"{m['slug']:24} {m['kind']:9} {m['status']:11} "
                  f"{m['date']:11} {m['subject']}")
        return 0
    print(__doc__.strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
