#!/usr/bin/env python3
"""ramp — what this repo needs to be worked on, and what the machine is
missing before the first pass.

    ramp [<board>] [--board <path>] [--json]  the gate — happy, or the gap and the ask
    ramp have [<board>]                       every skill this machine already offers this repo
    ramp need [<board>]                       the jobs the tree and the board ask for
    ramp gap [<board>]                        need minus have, loudest signal first
    ramp find <job> [<job>…]                  candidates for one job, off scout's routes
    ramp happy [<n>] [<board>]                record the happiness value — 0 reopens the gate

The gate is loop step 0 and it is read off one key: `happiness:` in
`.pearde/settings.md`, `0` when the file does not carry it. Non-zero is a
person saying the toolbox is good enough, and the gate prints one line and
gets out of the way. Zero means it has never been settled — or was reopened —
and the pass owes the user a proposal before it touches a PRD.

Three lists, and the third is the only one anybody acts on:

    need    a job the tree or the board asks for — a `Cargo.toml` asks for
            rust, forty markdown files ask for writing, a board full of Vue
            PRDs asks for Vue before a dependency does
    have    every skill this machine offers this repo — the project's own
            `.claude/skills/`, the config dir's, the user's, and the skills
            inside installed plugins; a flat set of `skill-*.md` files counts
            the same as a folder holding a `SKILL.md`
    gap     a need no installed skill's name or description answers

Nothing here installs anything. `find` ranks candidates and prints the exact
`npx skills add` line for each; the user picks, per
@references/parts/ramp.md. A ramp that installed on its own would be a sweep
writing to the machine, and the machine is not the board's to write.

Discovery is scout's — `resources/scout/route.sh skills` and `skillrepo`.
This module holds the fit: what the repo asks for, what is already answered,
and what to put to a person. Python 3 stdlib only.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edit as editlib          # noqa: E402
import plan as planlib          # noqa: E402

FLAGS = planlib.Flags(("board",), ("json",))
ROUTE = os.path.join(os.path.dirname(HERE), "scout", "route.sh")

# One row per job this tool can recognise. `marks` are tracked paths — a
# fnmatch pattern against the repo-relative path; `deps` are substrings looked
# for inside a manifest the tree already has; `words` are what an installed
# skill has to mention to count as an answer, and what `find` searches for.
# The table is the knob: a job nothing in the tree marks never reaches a gap.
JOBS = (
    ("rust",      ("Cargo.toml", "*.rs"),                   (),
     ("rust", "cargo", "clippy")),
    ("python",    ("pyproject.toml", "requirements*.txt", "*.py"), (),
     ("python", "pytest", "mypy")),
    ("typescript", ("tsconfig.json", "*.ts", "*.tsx"),      (),
     ("typescript",)),
    ("node",      ("package.json",),                        (),
     ("node", "npm", "javascript")),
    ("vue",       (),                          ("\"vue\"", "\"nuxt\""),
     ("vue", "nuxt")),
    ("react",     (),                          ("\"react\"",),
     ("react",)),
    ("next",      (),                          ("\"next\"",),
     ("next.js", "nextjs")),
    ("svelte",    (),                          ("\"svelte\"",),
     ("svelte",)),
    ("tailwind",  (),                          ("tailwindcss",),
     ("tailwind",)),
    ("php",       ("composer.json", "*.php"),               (),
     ("php", "laravel", "symfony", "shopware")),
    ("go",        ("go.mod", "*.go"),                       (),
     ("golang", "go module")),
    ("docker",    ("Dockerfile", "docker-compose*.y*ml", "compose.y*ml"), (),
     ("docker", "container")),
    # `workflow` and `ci` on their own are somebody else's word — this board
    # calls its own routes workflows. The keywords stay specific enough that
    # a PRD title cannot raise a job the tree never marked.
    ("ci",        (".github/workflows/*.y*ml",),            (),
     ("github actions", "pipeline", "continuous integration")),
    ("terraform", ("*.tf",),                                (),
     ("terraform", "opentofu")),
    ("sql",       ("*.sql", "migrations/*"),                (),
     ("sql", "database", "migration")),
    ("testing",   ("*_test.py", "*.test.ts", "*.spec.ts"),
     ("vitest", "jest", "playwright", "cypress", "pytest"),
     ("test", "tdd", "coverage")),
    ("writing",   ("*.md",),                                (),
     ("writing", "documentation", "docs", "prose", "editing")),
    ("shell",     ("*.sh",),                                (),
     ("shell", "bash", "posix")),
)

# A job whose markers are everywhere in every repo needs more than one hit
# before it is a signal. Below the floor the job is not asked for at all.
FLOOR = {"writing": 25, "shell": 5, "python": 3, "typescript": 3,
         "sql": 3, "testing": 2}

MANIFESTS = ("package.json", "composer.json", "Cargo.toml", "pyproject.toml")


# ── the tree, read once ───────────────────────────────────────────────────────

def repo_of(board):
    """The code repo a board sits in — its parent, which is where every
    marker below is looked for."""
    return os.path.dirname(os.path.abspath(board))


def tracked(repo):
    """Every tracked path, repo-relative. git is the filter: a vendored
    `node_modules` is not the repo asking for node. Falls back to a walk that
    skips the usual heavy directories where git cannot answer."""
    try:
        r = subprocess.run(["git", "-C", repo, "ls-files"],
                           capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.splitlines()
    except (OSError, subprocess.TimeoutExpired):
        pass
    skip = {".git", "node_modules", "target", "dist", "build", "venv",
            ".venv", "__pycache__"}
    out = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in files:
            out.append(os.path.relpath(os.path.join(root, f), repo))
    return out


def manifest_text(repo, paths):
    """The manifests' contents, concatenated and lowercased — where a `deps`
    substring is looked for. Only files git already listed are opened."""
    text = []
    for p in paths:
        if os.path.basename(p) in MANIFESTS:
            try:
                text.append(open(os.path.join(repo, p),
                                 encoding="utf-8", errors="replace").read())
            except OSError:
                pass
    return "\n".join(text).lower()


def board_words(board):
    """What the board itself is about: every PRD's title line, lowercased. A
    board full of Vue PRDs asks for Vue before a `package.json` does."""
    out = []
    prds = os.path.join(board, "prds")
    for root, dirs, files in os.walk(prds):
        if "archive" in root.split(os.sep):
            continue
        dirs[:] = [d for d in dirs if d != "archive"]
        if "prd.md" not in files:
            continue
        try:
            for line in open(os.path.join(root, "prd.md"),
                             encoding="utf-8", errors="replace"):
                if line.startswith("# "):
                    out.append(line[2:].strip().lower())
                    break
        except OSError:
            pass
    return out


def needs(board):
    """[(job, count, why)] — every job the tree or the board asks for, over
    its floor, loudest first."""
    import fnmatch
    repo = repo_of(board)
    paths = tracked(repo)
    lowered = [p.lower() for p in paths]
    deps = manifest_text(repo, paths)
    titles = board_words(board)
    rows = []
    for job, marks, dep_words, words in JOBS:
        hits, why = 0, []
        for pat in marks:
            n = sum(1 for p in lowered
                    if fnmatch.fnmatch(p, pat.lower())
                    or fnmatch.fnmatch(os.path.basename(p), pat.lower()))
            if n:
                hits += n
                why.append(f"{pat}×{n}")
        for d in dep_words:
            if d.lower() in deps:
                hits += 5
                why.append(f"dep {d.strip(chr(34))}")
        n = sum(1 for t in titles if any(w in t for w in words))
        if n:
            hits += n * 2
            why.append(f"{n} PRD{'s' if n > 1 else ''}")
        if hits >= FLOOR.get(job, 1):
            rows.append((job, hits, ", ".join(why)))
    rows.sort(key=lambda r: -r[1])
    return rows


# ── the machine, read once ────────────────────────────────────────────────────

def skill_dirs(board):
    """[(where, path)] — every place this agent discovers skills, project
    first. `CLAUDE_CONFIG_DIR` is honoured because the live install follows
    it; a path that is not there is dropped, not reported."""
    repo = repo_of(board)
    home = os.path.expanduser("~")
    cfg = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(home, ".claude")
    cand = [("project", os.path.join(repo, ".claude", "skills")),
            ("config", os.path.join(cfg, "skills")),
            ("user", os.path.join(home, ".claude", "skills"))]
    seen, out = set(), []
    for where, p in cand:
        rp = os.path.realpath(p)
        if os.path.isdir(p) and rp not in seen:
            seen.add(rp)
            out.append((where, p))
    return out


def frontmatter(path):
    """(name, description) off a SKILL.md — the two keys that say what a
    skill answers. A file with no frontmatter reads as its own first line."""
    try:
        text = open(path, encoding="utf-8", errors="replace").read(8000)
    except OSError:
        return "", ""
    name = desc = ""
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    body = m.group(1) if m else ""
    for key in ("name", "description"):
        km = re.search(rf"^{key}:\s*(.+?)$", body, re.M)
        if km:
            v = km.group(1).strip().strip("|>").strip()
            if key == "name":
                name = v
            else:
                desc = v
    if not desc:
        desc = " ".join(text.split())[:300]
    return name, desc


def installed(board):
    """[(where, name, text)] — every skill on offer, its searchable text
    lowercased. Three shapes count: a folder holding a `SKILL.md`, a flat set
    of `skill-*.md` files, and the skills inside an installed plugin."""
    import glob
    rows, seen = [], set()

    def add(where, name, text):
        # One skill, once. The same name reached twice — a config dir and the
        # user's dir holding it, a plugin cached under both — is one offer.
        if name in seen:
            return
        seen.add(name)
        rows.append((where, name, text))

    for where, root in skill_dirs(board):
        for entry in sorted(os.listdir(root)):
            d = os.path.join(root, entry)
            if not os.path.isdir(d):
                continue
            sk = os.path.join(d, "SKILL.md")
            if os.path.isfile(sk):
                name, desc = frontmatter(sk)
                add(where, name or entry, f"{name} {entry} {desc}".lower())
                continue
            flat = sorted(glob.glob(os.path.join(d, "skill-*.md")))
            for f in flat:
                nm = os.path.basename(f)[6:-3]
                _, desc = frontmatter(f)
                add(where, f"{entry}/{nm}", f"{entry} {nm} {desc}".lower())
    home = os.path.expanduser("~")
    cfg = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(home, ".claude")
    for base in {os.path.join(cfg, "plugins", "cache"),
                 os.path.join(home, ".claude", "plugins", "cache")}:
        for sk in glob.glob(os.path.join(base, "*", "*", "*", "skills",
                                         "*", "SKILL.md")):
            name, desc = frontmatter(sk)
            plug = sk.split(os.sep)[-4]
            add("plugin", name or plug, f"{name} {plug} {desc}".lower())
    return rows


def covers(text, words):
    """Whether one skill's text answers one job. A short word is matched on
    its boundaries — `go` must not be answered by `google`."""
    for w in words:
        if len(w) <= 4:
            if re.search(rf"\b{re.escape(w)}\b", text):
                return True
        elif w in text:
            return True
    return False


def gap(board):
    """[(job, count, why, covered_by)] for every need, `covered_by` empty
    where nothing answers it."""
    have = installed(board)
    words = {job: ws for job, _, _, ws in JOBS}
    out = []
    for job, hits, why in needs(board):
        by = [n for _, n, t in have if covers(t, words[job])]
        out.append((job, hits, why, by))
    return out


# ── the sources, through scout ────────────────────────────────────────────────

def route(rid, query, rows=8):
    """One scout route, as lines. A route that dies returns nothing — the
    proposal is thinner, never wrong."""
    if not os.path.isfile(ROUTE):
        return []
    env = dict(os.environ, SCOUT_N=str(rows))
    # `skills` reads one page per row past the name match, and the gate calls
    # it once per word — so it stays shallow here. The route on its own does
    # not, and an explicit SCOUT_DEPTH still wins.
    env.setdefault("SCOUT_DEPTH", "20")
    try:
        r = subprocess.run(["bash", ROUTE, rid, query], capture_output=True,
                           text=True, timeout=90, env=env)
    except (OSError, subprocess.TimeoutExpired):
        return []
    return [l for l in r.stdout.splitlines() if l.strip()] if r.returncode == 0 else []


def candidates(job, words, rows=6):
    """[(axis, score, source, name)] for one job, over two axes — scout's own
    rule, and the reason a pick here is not a star count. `skills` ranks one
    skill by installs; `gh` ranks a whole repository by stars, so its rows
    are a source to enumerate rather than a skill to install. Neither is a
    verdict: the user picks, per @references/parts/ramp.md."""
    seen, out = set(), []
    for w in words:
        for line in route("skills", w, rows * 3):
            parts = line.split("\t")
            if len(parts) < 3 or (parts[1], parts[2]) in seen:
                continue
            seen.add((parts[1], parts[2]))
            try:
                out.append(("installs", int(parts[0]), parts[1], parts[2]))
            except ValueError:
                pass
    if len(out) < rows:
        w = words[0]
        for line in route("gh", f"{w} skills in:name,description stars:>50",
                          rows * 2)[1:]:          # the first row is the header
            parts = line.split()
            if len(parts) < 2 or "/" not in parts[0] or (parts[0], "*") in seen:
                continue
            seen.add((parts[0], "*"))
            try:
                out.append(("stars", int(parts[1]), parts[0], "*"))
            except ValueError:
                pass
    out.sort(key=lambda r: (r[0] != "installs", -r[1]))
    return out[:rows]


def install_line(source, name):
    """What a person runs to take one candidate. A whole repository is listed
    before it is installed — `-l` prints its skills and writes nothing."""
    return (f"npx skills add {source} -l" if name == "*"
            else f"npx skills add {source} -s {name}")


# ── the gate ──────────────────────────────────────────────────────────────────

def happiness(board):
    try:
        return int(str(planlib.board_settings(board).get("happiness", 0)).strip())
    except ValueError:
        return 0


def write_ask(board, proposals):
    """The forks the dispatcher puts, in `.pearde/.state/ask.md`'s own shape —
    one `## Q<n> ramp <question>` with its answers under it. One fork per
    gap job, so a person answers each job once and never the whole toolbox."""
    state = os.path.join(board, ".state")
    os.makedirs(state, exist_ok=True)
    out = ["# ramp", ""]
    for i, (job, why, cands) in enumerate(proposals, 1):
        out.append(f"## Q{i} ramp Install a skill for {job}?")
        out.append("")
        out.append(f"The tree asks for {job} ({why}) and no installed skill "
                   f"mentions it. Which of these goes in, if any?")
        out.append("")
        for axis, n, src, name in cands:
            shown = src if name == "*" else name
            out.append(f"- **{shown}** — `{install_line(src, name)}` "
                       f"· {n:,} {axis} · {src}")
        out.append("- **none** — the gap is real and we work without it")
        out.append("")
    out.append("## Q%d ramp Happy with the toolbox?" % (len(proposals) + 1))
    out.append("")
    out.append("Once the picks above are in, is this repo tooled well enough "
               "to start? A yes writes `happiness:` and the gate stops asking.")
    out.append("")
    out.append("- **yes** — `pearde ramp happy 1`, and passes run from here")
    out.append("- **not yet** — leave it at 0; the next pass proposes again")
    out.append("")
    path = os.path.join(state, "ask.md")
    editlib.write_atomic(path, "\n".join(out))
    return path


def cmd_have(board, as_json=False):
    rows = installed(board)
    if as_json:
        json.dump([{"where": w, "name": n} for w, n, _ in rows],
                  sys.stdout, indent=1)
        print()
        return 0
    for where, name, _ in rows:
        print(f"{where:<8} {name}")
    print(f"have: {len(rows)} skills over "
          f"{len(skill_dirs(board))} directories")
    return 0


def cmd_need(board, as_json=False):
    rows = needs(board)
    if as_json:
        json.dump([{"job": j, "signal": h, "why": w} for j, h, w in rows],
                  sys.stdout, indent=1)
        print()
        return 0
    for job, hits, why in rows:
        print(f"{job:<12} {hits:>5}  {why}")
    print(f"need: {len(rows)} jobs")
    return 0


def cmd_gap(board, as_json=False):
    rows = gap(board)
    missing = [r for r in rows if not r[3]]
    if as_json:
        json.dump([{"job": j, "signal": h, "why": w, "covered_by": by}
                   for j, h, w, by in rows], sys.stdout, indent=1)
        print()
        return 0
    for job, hits, why, by in rows:
        mark = "GAP " if not by else "ok  "
        cover = "" if not by else f"· {', '.join(by[:3])}"
        print(f"{mark}{job:<12} {hits:>5}  {why} {cover}".rstrip())
    print(f"gap: {len(missing)} of {len(rows)} jobs unanswered")
    return 1 if missing else 0


def cmd_find(jobs, rows=6):
    words = {job: ws for job, _, _, ws in JOBS}
    for job in jobs:
        ws = words.get(job, (job,))
        cands = candidates(job, ws, rows)
        print(f"# {job}")
        if not cands:
            print("  nothing — both routes answered nothing for "
                  f"{', '.join(ws)}")
        for axis, n, src, name in cands:
            shown = src if name == "*" else name
            print(f"  {n:>9,} {axis:<8} {shown:<30} {install_line(src, name)}")
    return 0


def cmd_happy(board, value):
    path = os.path.join(board, "settings.md")
    if not os.path.isfile(path):
        print("ramp: no settings.md — run `pearde init` first", file=sys.stderr)
        return 2
    editlib.set_key(path, "happiness", value)
    if value == 0:
        print("happiness 0 — the ramp gate is open again; the next pass proposes")
    else:
        print(f"happiness {value} — the ramp gate is closed; passes start at step 1")
    return 0


def cmd_gate(board, as_json=False):
    """Loop step 0. Prints one line when the toolbox is settled, and writes
    the ask when it is not."""
    h = happiness(board)
    if h > 0:
        print(f"ramp: happy {h} — skipped (`pearde ramp happy 0` reopens it)")
        return 0
    rows = gap(board)
    missing = [r for r in rows if not r[3]]
    if not missing:
        print(f"ramp: no gap — {len(rows)} jobs answered by installed skills; "
              f"`pearde ramp happy 1` closes the gate")
        return 0
    proposals = []
    for job, hits, why, _ in missing[:5]:
        ws = [w for j, _, _, w in JOBS if j == job][0]
        cands = candidates(job, ws)
        if cands:
            proposals.append((job, why, cands))
    for job, _, why, _ in missing:
        print(f"GAP {job:<12} {why}")
    gaps = f"{len(missing)} gap{'s' if len(missing) != 1 else ''}"
    if not proposals:
        print(f"ramp: {gaps}, no candidates — the routes answered nothing; "
              f"`pearde ramp happy 1` closes the gate anyway")
        return 0
    path = write_ask(board, proposals)
    print(f"ramp: {gaps}, {len(proposals)} with candidates → "
          f"{os.path.relpath(path)} · hand back ASK")
    return 1


def cmd_ramp(argv, board=None):
    """the toolbox gate — what this repo needs, and what is missing"""
    import transitions as translib
    verbs = {"have", "need", "gap", "find", "happy"}
    verb = argv[0] if argv and argv[0] in verbs else ""
    rest = argv[1:] if verb else argv
    if verb == "find":
        if not rest:
            print("ramp find: name a job — `pearde ramp gap` lists them",
                  file=sys.stderr)
            return 2
        return cmd_find(rest)
    try:
        a = translib.Args(rest, FLAGS, "ramp")
    except translib.FlagRefused as e:
        print(f"pearde ramp: {e}", file=sys.stderr)
        return 2
    pos = list(a.pos)
    value = None
    if verb == "happy" and pos and re.fullmatch(r"\d+", pos[0]):
        value = int(pos.pop(0))
    board = planlib.find_board(a.opt.get("board") or (pos[0] if pos else board))
    as_json = "json" in a.flags
    if verb == "have":
        return cmd_have(board, as_json)
    if verb == "need":
        return cmd_need(board, as_json)
    if verb == "gap":
        return cmd_gap(board, as_json)
    if verb == "happy":
        if value is None:
            print(f"happiness {happiness(board)}")
            return 0
        return cmd_happy(board, value)
    return cmd_gate(board, as_json)


cmd_ramp.flags = FLAGS          # what `pearde ramp --help` prints
COMMANDS = {"ramp": cmd_ramp}


if __name__ == "__main__":
    sys.exit(cmd_ramp(sys.argv[1:]) or 0)
