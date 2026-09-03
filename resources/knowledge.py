#!/usr/bin/env python3
"""pearde knowledge — the research layer, whole. One tool, no dependency.

  knowledge.py query "<question>"  what the record already answers; a gap enqueues
  knowledge.py round [board]       what the round owes the KB, one line per tool
  knowledge.py remember <title>    a finding, body on stdin — one topic per file
  knowledge.py conclude <title>    synthesize from >=2 named sources
  knowledge.py enqueue <question>  a research question, priority-tagged
  knowledge.py relink [board]      resolve wikilinks, symmetrize `related:`
  knowledge.py board [board]       regenerate the board notes the vault renders
  knowledge.py index [board]       regenerate every folder's `_index.md`
  knowledge.py wiki [board]        the generated pages over the KB
  knowledge.py dashboard [board]   the numbers in Dashboard.md; --write the report
  knowledge.py doctor [board]      frontmatter, links, graph, pending — one per line
  knowledge.py harvest [board]     move a lane's stranded notes into the record

The loop: query first; a gap enqueues or researches; a finding is remembered;
a conclusion is concluded from >=2 sources; relink holds the graph together;
the dashboard and the wiki are what a person opens.

The folder is <board>/wiki/ — sources/, conclusions/, pending/, graphs/,
WORKFLOW.md, Dashboard.md — the self-contained Obsidian vault. The board is
the one above the cwd, found the way every other board tool finds it, so a
worker in a lane worktree reads and writes the live record rather than a stub
beside its own copy of this file (`default_root`). Every verb takes --root to
run on any other board's folder.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import common  # noqa: E402 — the board resolver, one copy
import memos as memos_lib  # noqa: E402 — the memos, read by their own reader

PROG = "knowledge"


def _plan():
    """@resources/board/plan.py, the one reader of a PRD — imported on
    demand, the way @resources/workflows.py `members` reaches it, since
    plan.py imports memos.py at its top and this file sits beside memos.
    The rule already put every directory under resources/ on the path, so
    the directory it sits in is never spelled here."""
    import plan  # noqa: E402
    return plan


# --- paths -----------------------------------------------------------------

def default_root(start=None):
    """The wiki of the board this call belongs to — the cwd's board first,
    the folder beside this file only when the climb finds none.

    The order is the whole point. A worker builds in a LANE, a git worktree
    at `<board>/.lanes/<slug>` materialised WITHOUT the board directory on
    purpose (@resources/board/lanes.py `create`: a tracked board copied into
    a worktree hands every command a stale board). The lane therefore holds
    a checkout of THIS file and no wiki beside it, so resolving
    script-relative answered `<lane>/pearde/wiki`, `Store.ensure` created
    it, and `query` reported `0 notes on record` against a record holding
    82 — silently, no error, once per worker. The gap it then enqueued
    landed in a directory `git worktree remove` deletes.

    Climbing from the cwd is how every other board tool answers the same
    question (@resources/common.py `board_above`, and @resources/board/plan.py
    says why discovery cannot be part of the climb). A lane's own board
    folder holds the shared graphify cache and nothing else, so it carries
    neither `settings.md` nor `prds/` and `is_board_dir` walks straight past
    it to the live board two levels up.

    The fallback is the checkout with no board above the cwd — a call from
    `/tmp`, a test fixture — where the folder beside this file is the only
    answer there is. `--root` still overrides both.
    """
    board = common.board_above(os.path.abspath(start or os.getcwd()), PROG)
    if board:
        return Path(board) / "wiki"
    repo = Path(__file__).resolve().parent.parent
    for name in common.BOARD_DIRS:
        if (repo / name / "wiki").is_dir():
            return repo / name / "wiki"
    return repo / common.BOARD_DIR / "wiki"


class Store:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()
        self.sources = self.root / "sources"
        self.absorbed = self.sources / ".absorbed"
        self.conclusions = self.root / "conclusions"
        self.pending = self.root / "pending"
        self.graphs = self.root / "graphs"
        self.graphify = self.root / ".graphify"
        self.graph_json = self.graphify / "graph.json"
        self.workflow_md = self.root / "WORKFLOW.md"
        # The dashboard sits at the BOARD's root, not the wiki's. The vault
        # roots at `.pearde/` (@references/obsidian.md), so the one page a
        # person opens is the first file they see on opening it — one folder
        # down was one folder to know about. Every Dataview source in it is
        # vault-relative (`wiki/board`, `memos`), so the move changes no
        # query: DQL `FROM` never reads from the file's own folder.
        self.board = self.root.parent
        self.dashboard_md = self.board / "Dashboard.md"
        self.report_md = self.board / "Dashboard.report.md"

    def ensure(self):
        for d in (self.sources, self.conclusions, self.pending,
                  self.graphs, self.graphify, self.absorbed):
            d.mkdir(parents=True, exist_ok=True)

    def workflow(self):
        """WORKFLOW.md frontmatter — the configuration, read on every call.
        Each key has a default and a coercion; a one-item list is its item
        first, so `key: [x]` and `key: x` read the same."""
        config = {key: default for key, (default, _) in CONFIG.items()}
        try:
            text = self.workflow_md.read_text(encoding="utf-8")
        except OSError:
            return config
        meta = parse_frontmatter(text)[0]
        for key, (_, coerce) in CONFIG.items():
            if key in meta:
                value = meta[key]
                if isinstance(value, list) and len(value) == 1:
                    value = value[0]
                config[key] = coerce(value)
        return config


def _csv(value):
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return value


def _flag(value):
    if isinstance(value, str):
        return value.strip().lower() in ("true", "yes", "1")
    return value


def _count(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 2


# key -> (default, coercion) — the whole of what WORKFLOW.md configures
CONFIG = {
    "active_focus": ([], _csv),
    "priority_tags": ([], _csv),
    "auto_enqueue": (True, _flag),
    "min_sources_per_conclusion": (2, _count),
    # days a tool's output may age before `round` calls it stale
    "stale_after_scout": (7, _count),
    "stale_after_graph": (3, _count),
    "stale_after_vault": (1, _count),
}


# --- frontmatter / note parsing ---------------------------------------------

FM_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


def parse_frontmatter(text):
    """Return (dict-of-keys, body). Lists stay lists; scalars stay strings;
    list items keep their quotes stripped but nothing else is coerced."""
    match = FM_RE.match(text)
    if not match:
        return {}, text
    meta, current_key, current_list = {}, None, None
    for line in match.group(1).split("\n"):
        if not line.strip() or line.strip().startswith("#"):
            continue
        item = re.match(r"^  - \"?(.+?)\"?\s*$", line)
        if item and current_key is not None:
            # `current_list` is None under a key that had a scalar value, so
            # an indented item there is a malformed file, not a list. Skip
            # the line: one stray dash in one note must not raise out of the
            # parser and take the whole verb down with it.
            if current_list is not None:
                current_list.append(item.group(1))
            continue
        pair = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if pair:
            key, value = pair.group(1), pair.group(2)
            if value == "":
                current_key, current_list = key, []
                meta[key] = current_list
            else:
                current_key, current_list = key, None
                if value.startswith("[") and value.endswith("]"):
                    inner = value[1:-1]
                    meta[key] = [v.strip().strip('"') for v in inner.split(",") if v.strip()] if inner.strip() else []
                else:
                    meta[key] = value.strip().strip('"')
        else:
            current_key, current_list = None, None
    return meta, text[match.end():]


class Note:
    def __init__(self, path):
        self.path = path
        raw = path.read_text(encoding="utf-8")
        self.meta, self.body = parse_frontmatter(raw)
        self.title = self.meta.get("title") or path.stem
        self.type = self.meta.get("type", "")
        self.tags = list(self.meta.get("tags", []))
        date = self.meta.get("date", "")
        try:
            self.date = dt.date.fromisoformat(str(date)[:10]) if date else None
        except ValueError:
            self.date = None


def load_notes(store, kinds=("sources", "conclusions")):
    notes = []
    bases = {"sources": store.sources, "conclusions": store.conclusions}
    for kind in kinds:
        base = bases[kind]
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if store.absorbed in path.parents:
                continue
            if path.name == "_index.md":
                continue
            note = Note(path)
            note.kind = kind  # sources / conclusions
            notes.append(note)
    return notes


# --- ids and slugs ----------------------------------------------------------

def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60] or "note"


def note_id(when=None):
    day = (when or dt.date.today()).strftime("%y%m%d")
    entropy = hashlib.sha1(str(dt.datetime.now(tz=dt.timezone.utc)).encode()).hexdigest()[:4]
    return f"{day}-{entropy}"


def note_maps(notes):
    """({stem: note}, {lowercased title: note}) — how a wikilink is looked
    up, built once per verb and handed to every lookup. Both `resolve_slug`
    and `build_graph` read these; a later note with the same title wins,
    as it did when each built its own."""
    by_stem = {n.path.stem: n for n in notes}
    by_title = {n.title.strip().lower(): n for n in notes}
    return by_stem, by_title


def resolve_slug(slug, by_stem, by_title):
    """Slug or wikilink target -> Path, or None. Wikilinks are shortest-path:
    any file whose stem or title matches."""
    slug = slug.strip().strip("[[]]")
    note = (by_stem.get(slug) or by_stem.get(Path(slug).stem)
            or by_title.get(slug.lower())
            or by_title.get(Path(slug).stem.lower()))
    return note.path if note else None


# --- verbs -------------------------------------------------------------------

def cmd_remember(store, args):
    store.ensure()
    when = dt.date.today()
    body = sys.stdin.read().strip()
    if not body:
        print("remember: body is empty — pipe the note in: echo \"...\" | knowledge.py remember <title>", file=sys.stderr)
        return 1
    slug = slugify(args.title)
    folder = store.sources
    if args.folder:
        folder = store.sources / args.folder.strip("/ ")
        if store.absorbed in folder.parents or folder == store.absorbed:
            print("remember: .absorbed is closed — a source is moved there by hand "
                  "once a conclusion lists it under `derived_from:`; no verb "
                  "writes there", file=sys.stderr)
            return 1
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{note_id(when)}.md"
    # id collision: shift the entropy a second forward until free
    while target.exists():
        target = folder / f"{note_id(when)}{hashlib.sha1(target.name.encode()).hexdigest()[:1]}.md"
    related = [r.strip().strip("[[]]") for chunk in (args.related or []) for r in chunk.split(",") if r.strip()]
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    tags = sorted(set(tags + ["source"]))
    lines = [
        "---",
        f"title: {args.title}",
        f"date: {when.isoformat()}",
        "type: source",
        f"tags: [{', '.join(tags)}]",
    ]
    if args.provenance:
        lines.append(f"provenance: \"{args.provenance}\"")
    if related:
        lines.append("related:")
        lines += [f"  - \"[[{r}]]\"" for r in related]
    lines += ["---", "", f"# {args.title}", "", body, ""]
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"remembered: {target.relative_to(store.root)} · [[{target.stem}]]")
    return 0


def cmd_conclude(store, args):
    store.ensure()
    config = store.workflow()
    minimum = config["min_sources_per_conclusion"]
    when = dt.date.today()
    sources = [s.strip().strip("[[]]") for s in (args.sources or "").split(",") if s.strip()]
    by_stem, by_title = note_maps(load_notes(store))
    resolved, missing = [], []
    for slug in sources:
        path = resolve_slug(slug, by_stem, by_title)
        (resolved if path else missing).append((slug, path))
    if missing:
        print("conclude: unresolved source link(s):", file=sys.stderr)
        for slug, _ in missing:
            print(f"  {slug}", file=sys.stderr)
        return 1
    if len(sources) < minimum:
        print(f"conclude: {len(sources)} source(s) is a hunch, not a conclusion "
              f"— min_sources_per_conclusion={minimum}", file=sys.stderr)
        return 1
    slug = slugify(args.title)
    target = store.conclusions / f"{slug}.md"
    if target.exists() and not args.force:
        print(f"conclude: {target.relative_to(store.root)} exists — new wording is an edit, "
              "a second finding is a --force or a new title", file=sys.stderr)
        return 1
    body = sys.stdin.read().strip()
    if not body:
        print("conclude: body is empty — pipe the argument in", file=sys.stderr)
        return 1
    related = [r.strip().strip("[[]]") for chunk in (args.related or []) for r in chunk.split(",") if r.strip()]
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    tags = sorted(set(tags + ["conclusion"]))
    lines = [
        "---",
        f"title: {slug}",
        f"date: {when.isoformat()}",
        "type: conclusion",
        f"tags: [{ ', '.join(tags)}]",
        "sources:",
    ] + [f"  - \"[[{p.stem}]]\"" for _, p in resolved] + ([
        "related:",
    ] + [f"  - \"[[{r}]]\"" for r in related] if related else []) + [
        "derived_from: []",
        "---",
        "",
        f"# {args.title}",
        "",
        body,
        "",
    ]
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"concluded: {target.relative_to(store.root)} · [[{target.stem}]] "
          f"· {len(resolved)} source(s)")
    return 0


def cmd_enqueue(store, args):
    store.ensure()
    when = dt.date.today()
    question = " ".join(args.question).strip()
    if not question or question == '""':
        print("enqueue: empty question", file=sys.stderr)
        return 1
    dedupe_only = getattr(args, "_dedupe_only", False)
    existing = []
    if store.pending.exists():
        for path in store.pending.glob("*.md"):
            try:
                meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
            except OSError:
                continue
            if str(meta.get("question", "")).strip().lower() == question.lower():
                existing.append(path)
    if existing:
        print(f"enqueued: already pending — {existing[0].relative_to(store.root)}")
        return 0
    if dedupe_only:
        return 0
    target = store.pending / f"{note_id(when)}.md"
    lines = [
        "---",
        f"date: {when.isoformat()}",
        "type: pending",
        f"status: pending",
        f"priority: {args.priority}",
        # the graph colours by kind, and a kind it can see is a tag — the
        # `type:` beside it is a property, which the graph view cannot query
        "tags: [pending]",
    ]
    if args.requested_by:
        lines.append(f"requested_by: \"{args.requested_by}\"")
    lines += [
        f"question: \"{question}\"",
        "---",
        "",
        f"# {question}",
        "",
    ]
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"enqueued: {target.relative_to(store.root)} · priority {args.priority}")
    return 0


def score_note(note, terms, focus, priority_tags):
    score = 0
    haystacks = [(note.title.lower(), 3), (note.body.lower(), 1)]
    tag_text = " ".join(note.tags).lower()
    haystacks.append((tag_text, 2))
    for term in terms:
        for text, weight in haystacks:
            if term in text:
                score += weight
    matched_focus = [f for f in focus if f.lower() in tag_text or f.lower() in note.title.lower()]
    if matched_focus:
        score += 2 * len(matched_focus)
    matched_priority = [t for t in priority_tags if t.lower() in tag_text]
    if matched_priority:
        score += 3 * len(matched_priority)
    if note.date:
        age_days = (dt.date.today() - note.date).days
        if age_days <= 14:
            score += 1
    return score


def _gap(store, config, question, no_enqueue):
    """What a gap does to the queue: enqueued when the configuration says
    so; with --no-enqueue only deduped, so an already-pending question is
    still named and nothing is written."""
    if config["auto_enqueue"] and not no_enqueue:
        cmd_enqueue(store, argparse.Namespace(
            question=[question], priority="med", requested_by="query gap"))
    elif no_enqueue:
        cmd_enqueue(store, argparse.Namespace(
            question=[question], priority="med", requested_by="query gap",
            _dedupe_only=True))


def cmd_query(store, args):
    config = store.workflow()
    question = " ".join(args.question).strip()
    terms = [t for t in re.split(r"\W+", question.lower()) if len(t) > 2]
    notes = load_notes(store)
    scores = sorted(((score_note(n, terms, config["active_focus"], config["priority_tags"]), n)
                     for n in notes), key=lambda pair: pair[0], reverse=True)
    hits = [(s, n) for s, n in scores if s > 0]
    strong = [(s, n) for s, n in hits if s >= 4]
    print(f"query: {len(hits)} hit(s), {len(strong)} strong · {len(notes)} notes on record")
    for score, note in hits[:args.limit]:
        marker = "@" if score >= 4 else " "
        links = list(WIKILINK_RE.findall(note.body))
        print(f"  {marker} {score:>2}  [[{note.path.stem}]] {note.kind:<9} {note.title[:70]}")
        if args.verbose:
            first = next((line.strip() for line in note.body.split("\n")
                          if line.strip() and not line.startswith("#")), "")
            print(f"        {first[:100]}")
            if links:
                print(f"        links: {', '.join(links[:6])}")
    if not hits:
        print("gap: nothing on record for this question")
        _gap(store, config, question, args.no_enqueue)
        return 2
    if len(strong) < 1:
        print("gap: thin — hits name the topic but no note answers it")
        _gap(store, config, question, args.no_enqueue)
        return 2
    return 0


def build_graph(store):
    """Nodes = notes. Edges: body wikilinks (resolved), `sources:` frontmatter,
    `related:` frontmatter, symmetrized. Provenance per edge says where it
    came from. Writes .graphify/graph.json. Returns (notes, edges)."""
    notes = load_notes(store)
    by_stem, by_title = note_maps(notes)

    def resolve(link):
        link = link.strip().strip("[[]]").strip()
        return by_stem.get(link) or by_title.get(link.lower()) \
            or next((n for t, n in by_title.items()
                     if t.startswith(link.lower()) or link.lower().startswith(t)), None)

    edges = {}

    def add_edge(src, dst, kind, provenance):
        if src.path == dst.path:
            return
        key = (src.path.stem, dst.path.stem)
        if key not in edges:
            edges[key] = {"from": src.path.stem, "to": dst.path.stem,
                          "type": kind, "provenance": provenance}
        elif provenance == "frontmatter" and edges[key]["provenance"] != "frontmatter":
            edges[key]["type"] = kind if kind == "derives" else edges[key]["type"]
            edges[key]["provenance"] = provenance

    for note in notes:
        for link in WIKILINK_RE.findall(note.body):
            target = resolve(link)
            if target:
                kind = "derives" if note.kind == "conclusions" else "links"
                add_edge(note, target, kind, "wikilink")
        for key, kind in (("sources", "derives"), ("related", "related")):
            for link in note.meta.get(key, []) or []:
                target = resolve(link)
                if target:
                    add_edge(note, target, kind, "frontmatter")

    # frontmatter `related:` is a symmetric claim; the reverse edge follows
    for edge in list(edges.values()):
        if edge["type"] == "related":
            back = (edge["to"], edge["from"])
            if back not in edges:
                edges[back] = {"from": edge["to"], "from_type": None,
                               "to": edge["from"], "type": "related",
                               "provenance": "frontmatter"}

    graph = {
        "nodes": [
            {
                "id": n.path.stem,
                "title": n.title,
                "kind": n.kind,
                "type": n.type,
                "tags": n.tags,
                "date": str(n.meta.get("date", "")),
                "path": str(n.path.relative_to(store.root)),
            }
            for n in notes
        ],
        "edges": sorted(edges.values(), key=lambda e: (e["from"], e["to"])),
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "note_count": len(notes),
        "edge_count": len(edges),
    }
    return notes, list(edges.values()), graph


def cmd_relink(store, args):
    store.ensure()
    notes, edges, graph = build_graph(store)
    store.graph_json.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    # symmetrize related: frontmatter, both directions, idempotently
    for note in notes:
        wanted = sorted({e["to"] if e["from"] == note.path.stem else e["from"]
                         for e in edges
                         if e["type"] == "related"
                         and note.path.stem in (e["from"], e["to"])})
        if not wanted:
            continue
        text = note.path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        listed = [str(r).strip("[[]]") for r in meta.get("related", []) or []]
        missing = [s for s in wanted if s not in listed]
        if not missing:
            continue
        # the block rewritten whole: the wanted set, then whatever was
        # listed and resolves to no note — kept, so `doctor` can still
        # name it as an unresolved link rather than have it vanish
        items = wanted + [s for s in listed if s not in wanted]
        text, _ = common.set_list_key(text, "related",
                                      [f'"[[{s}]]"' for s in items])
        note.path.write_text(text, encoding="utf-8")
        print(f"  related: {note.path.stem} + {', '.join(missing)}")
    print(f"relink: {graph['note_count']} nodes, {graph['edge_count']} edges "
          f"-> {store.graph_json}")
    orphan_stems = set()
    for edge in edges:
        orphan_stems.add(edge["from"])
        orphan_stems.add(edge["to"])
    orphans = [n for n in notes if n.path.stem not in orphan_stems]
    if orphans:
        print(f"  orphans ({len(orphans)}): " + ", ".join(o.path.stem for o in orphans))
    return 0


def cmd_wiki(store, args):
    """graphs/ — one hub page per connected component of >= 2 notes."""
    store.ensure()
    notes, edges, graph = build_graph(store)
    adjacency = {}
    for edge in edges:
        adjacency.setdefault(edge["from"], set()).add(edge["to"])
        adjacency.setdefault(edge["to"], set()).add(edge["from"])
    seen, components = set(), []
    for node in graph["nodes"]:
        if node["id"] in seen:
            continue
        stack, component = [node["id"]], set()
        while stack:
            current = stack.pop()
            if current in component:
                continue
            component.add(current)
            stack += [m for m in adjacency.get(current, ()) if m not in component]
        seen |= component
        if len(component) >= 2:
            components.append(sorted(component))
    components.sort(key=len, reverse=True)
    for index, component in enumerate(components, 1):
        hub = max(component, key=lambda cid: len(adjacency.get(cid, ())))
        member = {n["id"]: n for n in graph["nodes"] if n["id"] in component}
        lines = [
            "---",
            f"title: community-{index}-{slugify(hub)}",
            f"date: {dt.date.today().isoformat()}",
            "type: wiki",
            "tags: [graph]",
            "community:",
            f"  hub: \"[[{hub}]]\"",
            f"  size: {len(component)}",
            "---",
            "",
            f"# {member[hub]['title']}",
            "",
            f"{len(component)} notes travel together in this component. Hubs "
            f"first, then the rest.",
            "",
            "```dataview",
            "TABLE WITHOUT ID file.link AS Node, type, length(file.inlinks) AS In",
            f"WHERE file.path != this.file.path",
            "AND (",
        ]
        lines += [f'  file.name = "{cid}"' + (" OR" if cid != component[-1] else "")
                  for cid in component]
        lines += [")", "SORT length(file.inlinks) DESC", "```", ""]
        target_path = store.graphs / f"community-{index:02d}-{slugify(hub)}.md"
        target_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  {target_path.relative_to(store.root)} ({len(component)} notes, hub [[{hub}]])")
    # drop stale community pages
    keep = {f"community-{i:02d}-{slugify(max(c, key=lambda cid: len(adjacency.get(cid, ()))))}.md"
            for i, c in enumerate(components, 1)}
    for old in store.graphs.glob("community-*.md"):
        if old.name not in keep:
            old.unlink()
            print(f"  removed stale {old.relative_to(store.root)}")
    if not components:
        print("wiki: no component of two or more linked notes — the graph is thin")
    return 0


def cmd_board(store, args):
    """board/ — one generated note per PRD, the board as a linkable graph.

    Reads the board beside the KB (the parent of the KB folder) through its
    own readers — @resources/board/plan.py `scan` for every prd.md's
    frontmatter (state, origin, priority, complexity, blast-radius, needs,
    from, workflow, footprint), @resources/memos.py `scan` for the memos.
    Writes <KB>/board/<slug>.md per PRD — frontmatter carries the state
    fields as Dataview fields, the body carries the wikilinks: needs, fed-by
    (the computed reverse), derived-from, children, the memos that mention
    the PRD, the workflow it runs on. Stale pages for PRDs that left the
    board are removed. Regenerable: edit prd.md, run board again.
    """
    store.ensure()
    board_root = store.root.parent                # <board> — the KB's parent
    prds = board_root / "prds"                     # <board>/prds, the PRD tree
    vault_root = board_root.parent                 # the Obsidian vault: the
                                                   # PROJECT, so a vault-relative
                                                   # path starts with the board

    def scalar(value):
        # prd.md frontmatter carries trailing comments — "open  # open|..." —
        # so cut on the first " #", and treat the empty-list marker as empty
        text = str(value or "").split("#")[0].strip()
        return "" if text in ("[]", '""', "''") else text

    def listed(value):
        return value if isinstance(value, list) else [value] if value else []

    prds_found = {}          # PRD path-as-slug ("parent/child" for nested) -> fields
    for slug, prd in _plan().scan(str(board_root)).items():
        if prd["board"] is not None:      # a member's PRD is its own board's
            continue
        meta = prd["fm"]
        prds_found[slug] = {
            "title": prd["title"],
            "state": scalar(meta.get("state")),
            "origin": scalar(meta.get("origin")),
            "priority": scalar(meta.get("priority")),
            "complexity": scalar(meta.get("complexity")),
            "blast": scalar(meta.get("blast-radius")),
            "needs": [scalar(n) for n in listed(meta.get("needs")) if scalar(n)],
            "from": scalar(meta.get("from")),
            "workflow": scalar(meta.get("workflow")),
            "footprint": [scalar(f) for f in listed(meta.get("footprint")) if scalar(f)],
            "text": prd["body"],
        }
    memos = {}
    for slug, m in memos_lib.scan(str(board_root)).items():
        memos[slug] = {
            "subject": str(m["subject"]).strip() or slug,
            "kind": str(m["kind"]).strip(),
            "status": str(m["status"]).strip(),
            "cites": [str(p).strip() for p in listed(m["fm"].get("prds"))],
            # the raw file, frontmatter and all: a PRD named in the subject
            # line still counts as mentioned
            "text": common.read_text(m["path"]),
        }
    board_dir = store.root / "board"
    board_dir.mkdir(parents=True, exist_ok=True)
    # a memo belongs to a PRD when it names the PRD in its `prds:` frontmatter,
    # or the memo body cites the PRD dir name, or the PRD body cites the memo slug
    memo_hits_by_prd = {}
    for name, prd in prds_found.items():
        leaf = name.split("/")[-1]
        memo_hits_by_prd[name] = sorted(
            slug for slug, memo in memos.items()
            if leaf in memo["cites"] or leaf in memo["text"]
            or slug in prd["text"])
    flat = {name.split("/")[-1]: f"wiki/board/{name}"
            for name in prds_found}
    # A memo's wikilinks are not all knowledge: they also point at other memos
    # and at headings. Only a link that resolves to a note under sources/ or
    # conclusions/ belongs under ## Knowledge — the rest are decisions, and
    # already listed as such. Built once, not per PRD.
    kb_names = {}
    for note in load_notes(store, ("sources", "conclusions")):
        kb_names[note.path.stem] = note.path.stem
        kb_names[note.title.strip().lower()] = note.path.stem
    written, removed = [], []
    for name, prd in prds_found.items():
        name_parts = (name, name.split("/")[-1])
        fed_by = sorted(other for other, p in prds_found.items()
                        if any(part in p["needs"] for part in name_parts)
                        or any(other == n.split("/")[0] and n.split("/")[-1] == name.split("/")[-1]
                               for n in p["needs"]))
        children = sorted(other for other, p in prds_found.items()
                          if p["from"] in name_parts)
        # The properties above are what a Dataview query reads; the tags
        # below are what the graph view can see, and they are the same three
        # axes, not a second opinion — `tag_axes` derives them from the very
        # fields written on the next lines, so a PRD whose state changed and
        # whose note was regenerated cannot carry a stale tag. Three axes and
        # not four: `workflow:` is already a wikilink, so the graph draws that
        # edge to the workflow's own note, and a tag beside it would be a
        # weaker second copy of an edge that is already there.
        state = prd["state"] or "unknown"
        origin = prd["origin"] or "requested"
        blast = prd["blast"] or "low"
        lines = [
            "---",
            f"title: {name}",
            "type: prd",
            f"state: {state}",
            f"origin: {origin}",
            f"priority: {prd['priority'] or 0}",
            f"complexity: {prd['complexity'] or 0}",
            f"blast: {blast}",
            f"tags: [{', '.join(prd_tags(state, origin, blast))}]",
        ]
        if prd["from"]:
            lines.append(f'from: "[[{flat.get(prd["from"], prd["from"])}]]"')
        if prd["needs"]:
            lines.append("needs:")
            for n in prd["needs"]:
                lines.append(f'  - "[[{flat.get(n, n)}]]"')
        if prd["workflow"]:
            lines.append(f'workflow: "[[{prd["workflow"]}]]"')
        lines += [
            "---", "",
            f"# {prd['title']}", "",
            f"`state: {prd['state'] or 'unknown'} · origin: {prd['origin'] or 'requested'}"
            f" · priority {prd['priority'] or 0} · complexity {prd['complexity'] or 0}"
            f" · blast {prd['blast'] or '—'}`", "",
        ]
        if fed_by:
            lines += ["## Fed by (needs this one)", ""]
            lines += [f"- [[{flat.get(n, n)}]]" for n in fed_by] + [""]
        if prd["needs"]:
            lines += ["## Needs (gates this one behind)", ""]
            lines += [f"- [[{flat.get(n, n)}]]" for n in prd["needs"]] + [""]
        if prd["from"]:
            lines += [f"Derived from [[{flat.get(prd['from'], prd['from'])}]].", ""]
        if children:
            lines += ["## Children (derived from this)", ""]
            lines += [f"- [[{flat.get(c, c)}]]" for c in children] + [""]
        if prd["workflow"]:
            lines += [f"Runs on: [[{prd['workflow']}]]", ""]
        if prd["footprint"]:
            lines += ["## Footprint", ""]
            lines += [f"- `{f}`" for f in prd["footprint"]] + [""]
        specs = sorted(((prd_dir / "specs").glob("spec*.md"))
                       if (prd_dir := prds / name).exists() else [])
        if specs:
            lines += ["## Specs", ""]
            # [[.pearde/prds/…/spec]] — the vault-relative path, and the vault
            # is the project, so it carries the board folder in front
            lines += [f"- [[{s.relative_to(vault_root).with_suffix('')}]]"
                      for s in specs] + [""]
        if memo_hits_by_prd[name]:
            lines += ["## Decisions", ""]
            lines += [f"- [[{slug}]] — {memos[slug]['subject']}"
                      for slug in memo_hits_by_prd[name]] + [""]
        # the knowledge under the decisions: conclusions the citing memos stand on
        conclusions = sorted({kb
                              for slug in memo_hits_by_prd[name]
                              for link in WIKILINK_RE.findall(memos[slug]["text"])
                              if (kb := kb_names.get(link.strip())
                                  or kb_names.get(link.strip().lower()))})
        if conclusions:
            lines += ["## Knowledge", ""]
            lines += [f"- [[{c}]]" for c in conclusions] + [""]
        target = board_dir / f"{name}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines), encoding="utf-8")
        written.append(name)
    for old in sorted(board_dir.rglob("*.md")):
        if old.relative_to(board_dir).as_posix()[:-3] not in prds_found:
            old.unlink()
            removed.append(old.stem)
    print(f"board: {len(written)} PRD note(s), {len(memos)} memos scanned"
          + (f" · {len(removed)} stale removed" if removed else ""))
    return 0


# --- tags -------------------------------------------------------------------

# What a tag may hold: Obsidian reads a tag up to the first character outside
# this set, so a value carrying a space or a dot would silently become a
# shorter tag than the one written. Slugged, never dropped.
TAG_SAFE = re.compile(r"[^A-Za-z0-9_/-]+")


def tag(value):
    """One frontmatter value as a tag body — lowercased, unsafe runs folded to
    `-`. Empty in, empty out; the caller drops it."""
    return TAG_SAFE.sub("-", str(value or "").strip().lower()).strip("-")


def prd_tags(state, origin, blast):
    """The tags a generated PRD note carries: its kind, then one per axis the
    contract gives it. Derived from the fields on every regeneration, so the
    tag cannot outlive the value it names."""
    out = ["prd"]
    for name, value in (("state", state), ("origin", origin), ("blast", blast)):
        body = tag(value)
        if body:
            out.append(f"{name}/{body}")
    return out


# --- the map as notes -------------------------------------------------------

# what a path's first segments say the file is. A row ending in `/` names a
# place rather than a file, and keeps its own kind.
KINDS = {
    "references/skills": "skill",
    "references/templates": "template",
    "references/personas": "persona",
    "references/parts": "part",
    "references/agents": "agent",
    "resources/invariants": "invariant",
}
# a folder whose files are one family — the family is the area, not each file
FAMILIES = {"templates", "personas", "agents", "invariants"}


def index_kind(path):
    """reference · resource · skill · template · persona · part · agent ·
    invariant · entry · place — derived from the path, never stored."""
    if path.endswith("/"):
        return "place"
    head = "/".join(path.split("/")[:2])
    if head in KINDS:
        return KINDS[head]
    top = path.split("/")[0]
    if top in ("references", "resources"):
        return top[:-1]        # reference, resource
    return "entry"             # SKILL.md, README.md, index.md, .gitignore


def index_area(path):
    """The subject a file belongs to — `graph`, `board`, `knowledge`, …

    The keyword answers what to read; the area answers where a file sits, and
    a file with no keyword still has one. Derived from the path so it never
    drifts from the tree.
    """
    parts = path.rstrip("/").split("/")
    if len(parts) == 1:
        return "root"
    if parts[0] == "resources":
        if len(parts) > 3 and parts[1] == "board":
            return parts[2]                     # knowledge, obsidian, adapters
        if len(parts) > 2:
            return parts[1]                     # board, scout, graph, invariants
        return index_stem(parts[-1])            # resources/knowledge.py -> knowledge
    if parts[1] in FAMILIES:
        return parts[1]
    return index_stem(parts[-1])                # parts/board.md -> board


def index_stem(name):
    """The subject in a file name — `pearde-graph.md` and `graph.md` and
    `graph.sh` are all `graph`; a `.doc.md` is its template's subject."""
    stem = name.split(".")[0]
    return stem[7:] if stem.startswith("pearde-") else stem


def index_slug(path):
    """One flat note name per path, reversible by eye: `references/graph.md`
    is `references-graph-md`."""
    return re.sub(r"[^A-Za-z0-9]+", "-", path.strip("/")).strip("-").lower()


def yaml_quote(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def cmd_index(store, args):
    """index/ — one generated note per row of the repo's manifest, the map as
    a queryable set of notes.

    Dataview reads markdown and nothing else: it cannot see `resources/*.py`
    or a `.sh`, and the vault holds markdown and images by design. So an index
    of the tree is markdown *about* the tree — one note per row of
    @references/files.md, carrying the row's prose as `title`, the path as
    `path`, a `kind` and an `area` read off the path, and every `@@<keyword>`
    from @index.md naming that file. The body links the real file when the
    real file is a note, and links the siblings that share its keyword, so
    the graph shows a subject as one cluster.

    @resources/index.py stays the only parser of either format — this reads it
    through `rows()`, `keywords()` and `scope_text()`, against the project the
    board sits in, so a board in a repo with no map indexes nothing and says
    so. Stale notes for rows that left the manifest are removed, exactly as
    `board` does. Regenerable: edit the manifest, run index again.
    """
    store.ensure()
    board_root = store.root.parent                 # <board> — the KB's parent
    project = board_root.parent                    # the vault root, and the repo
    if not ((project / "index.md").is_file()
            and (project / "references" / "files.md").is_file()):
        print(f"index: no map at {project} — index.md and references/files.md "
              "are what this reads; nothing indexed")
        return 0
    import index as index_map   # noqa: E402 — the one reader of the format,
                                # on the path by the rule, wherever it sits

    rows = index_map.rows(str(project))
    scopes = index_map.keywords(str(project))
    scope_says = index_map.scope_text(str(project))

    # a keyword names files; a keyword naming a directory names everything
    # under it, the same way a manifest row covers a tree
    keywords_of = {path: set() for path in rows}
    for keyword, anchors in scopes.items():
        for anchor in anchors:
            if anchor.endswith("/"):
                for path in rows:
                    if path.startswith(anchor):
                        keywords_of[path].add(keyword)
            elif anchor in keywords_of:
                keywords_of[anchor].add(keyword)

    slugs, taken = {}, {}
    for path in rows:
        slug = index_slug(path)
        while slug in taken:
            slug += "-2"
        taken[slug] = path
        slugs[path] = slug
    # the vault is the project, so the note's own address carries the
    # board's real name in front, whatever the board is called
    link = {path: f"{board_root.name}/wiki/index/{slug}"
            for path, slug in slugs.items()}

    index_dir = store.root / "index"
    index_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for path, says in sorted(rows.items()):
        keywords = sorted(keywords_of[path])
        exists = (project / path).exists()
        lines = [
            "---",
            f"title: {yaml_quote(says or path)}",
            "type: fileindex",
            f"path: {path}",
            f"kind: {index_kind(path)}",
            f"area: {index_area(path)}",
            f"ext: {path.rsplit('.', 1)[-1] if '.' in path.rsplit('/', 1)[-1] else 'dir'}",
            f"keywords: [{', '.join(keywords)}]",
            f"present: {str(exists).lower()}",
            "---", "",
            f"# {path}", "",
        ]
        if says:
            lines += [says, ""]
        if path.endswith("/"):
            lines += [f"A place, not a file — every path under `{path}`.", ""]
        elif path.endswith(".md"):
            # a note in this vault: the link opens the real file
            lines += [f"→ [[{path[:-3]}|{path}]]", ""]
        else:
            lines += [f"→ `{path}` — not a note; Dataview cannot read it, "
                      "which is why this page exists.", ""]
        if keywords:
            lines += ["## Keywords", ""]
            lines += [f"- `@@{k}` — {scope_says.get(k, '')}".rstrip(" —")
                      for k in keywords] + [""]
            for keyword in keywords:
                siblings = sorted(p for p in rows
                                  if p != path and keyword in keywords_of[p])
                if not siblings:
                    continue
                lines += [f"## Same scope — `@@{keyword}`", ""]
                lines += [f"- [[{link[s]}|{s}]]" for s in siblings] + [""]
        else:
            lines += ["## Keywords", "",
                      "None. No `@@` scope in @index.md names this file — it "
                      "is reachable by path only.", ""]
        target = index_dir / f"{slugs[path]}.md"
        target.write_text("\n".join(lines), encoding="utf-8")
        written.append(path)

    keep = {f"{slug}.md" for slug in slugs.values()}
    removed = []
    for old in sorted(index_dir.rglob("*.md")):
        if old.relative_to(index_dir).as_posix() not in keep:
            old.unlink()
            removed.append(old.stem)
    orphan_keywords = sorted(k for k in scopes
                             if not any(k in v for v in keywords_of.values()))
    unkeyworded = sum(1 for path in rows if not keywords_of[path])
    print(f"index: {len(written)} file note(s), {len(scopes)} keyword(s)"
          + (f" · {unkeyworded} with no keyword" if unkeyworded else "")
          + (f" · {len(removed)} stale removed" if removed else "")
          + (f" · keyword(s) naming no row: {', '.join(orphan_keywords)}"
             if orphan_keywords else ""))
    return 0


def cmd_dashboard(store, args):
    """Rewrite Dashboard.md's numbers only — a human edits the queries; this
    prints the plain report. --write regenerates the report file."""
    notes, edges, graph = build_graph(store)
    today = dt.date.today()
    conclusions = [n for n in notes if n.kind == "conclusions"]
    sources = [n for n in notes if n.kind == "sources"]
    pending = []
    for path in sorted(store.pending.glob("*.md")):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        pending.append((path, meta))
    in_edges = {}
    out_edges = {}
    for edge in edges:
        out_edges.setdefault(edge["from"], 0)
        out_edges[edge["from"]] += 1
        in_edges.setdefault(edge["to"], 0)
        in_edges[edge["to"]] += 1
    cited = {e["to"] for e in edges if e["type"] in ("derives", "links")}
    uncited = [n for n in sources if n.path.stem not in cited]
    orphans = [n for n in notes
               if n.path.stem not in in_edges and n.path.stem not in out_edges]
    hubs = sorted(in_edges.items(), key=lambda pair: pair[1], reverse=True)[:8]

    def line(name, value):
        return f"{name}: {value}"

    out = [
        f"# Knowledge report — {today.isoformat()}",
        "",
        line("notes on record", f"{len(notes)} ({len(conclusions)} conclusions, {len(sources)} sources)"),
        line("edges", f"{graph['edge_count']} ({len([e for e in edges if e['type'] == 'derives'])} derive from sources)"),
        line("pending queue", f"{len(pending)} question(s)" + (
            ", priorities: " + ", ".join(f"{m.get('priority', '?')}" for _, m in pending) if pending else "")),
    ]
    if hubs:
        out += ["", "## Hubs (most referenced)", ""]
        out += [f"- [[{stem}]] — {count} inbound" for stem, count in hubs]
    if orphans:
        out += ["", "## Orphans (no edges in either direction)", ""]
        out += [f"- [[{n.path.stem}]] — {n.title}" for n in orphans]
    if uncited:
        out += ["", "## Sources no conclusion stands on yet", ""]
        out += [f"- [[{n.path.stem}]] — {n.title}" for n in uncited]
    out += ["", "The live views are in the vault: open the folder in Obsidian, "
            "or read Dashboard.md's Dataview blocks."]
    report = "\n".join(out) + "\n"
    print(report)
    if args.write:
        store.report_md.write_text(report, encoding="utf-8")
        print(f"written: {store.report_md.relative_to(store.root)}")
    return 0


def cmd_doctor(store, args):
    problems = []
    config = store.workflow()
    if not store.workflow_md.exists():
        problems.append("WORKFLOW.md missing — the loop has no configuration")
    notes = load_notes(store)
    stems = set()
    for note in notes:
        stems.add(note.path.stem)
        if not note.meta:
            problems.append(f"{note.path.name}: no frontmatter")
        if note.kind == "conclusions":
            n_sources = len(note.meta.get("sources", []) or [])
            if n_sources < config["min_sources_per_conclusion"]:
                problems.append(f"{note.path.name}: {n_sources} source(s) — below "
                                f"min_sources_per_conclusion={config['min_sources_per_conclusion']}")
            if "derived_from" not in note.meta:
                problems.append(f"{note.path.name}: conclusion without derived_from:")
    # resolve every wikilink in every body
    titles = {n.title.strip().lower() for n in notes}
    stems = set()
    for note in notes:
        stems.add(note.path.stem)
    for note in notes:
        for link in WIKILINK_RE.findall(note.body + " " + " ".join(
                str(v) for v in (note.meta.get("related", []) or []) +
                (note.meta.get("sources", []) or []))):
            link = link.strip().strip("[[]]").strip()
            if link in stems:
                continue
            low = link.lower()
            if low in titles or any(t.startswith(low) or low.startswith(t) for t in titles):
                continue
            problems.append(f"{note.path.name}: unresolved wikilink [[{link}]]")
    if store.graph_json.exists():
        try:
            graph = json.loads(store.graph_json.read_text(encoding="utf-8"))
            disk = {n.path.stem for n in notes}
            graph_ids = {n["id"] for n in graph.get("nodes", [])}
            if graph_ids != disk:
                stale = (graph_ids - disk) | (disk - graph_ids)
                problems.append("graph.json is behind the files: " + ", ".join(sorted(stale)[:6]))
        except (OSError, json.JSONDecodeError) as error:
            problems.append(f"graph.json unreadable: {error}")
    else:
        problems.append("graph.json missing — run relink")
    stale_pending = []
    for path in store.pending.glob("*.md"):
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        date = str(meta.get("date", ""))[:10]
        try:
            age = (dt.date.today() - dt.date.fromisoformat(date)).days
            if age > 30:
                stale_pending.append(f"{path.name}: pending {age} days — a question enqueued "
                                     "and never needed again is deleted, not drained")
        except ValueError:
            pass
    problems += stale_pending
    if problems:
        for problem in problems:
            print(f"  ✗ {problem}")
        print(f"doctor: {len(problems)} problem(s)")
        return 1
    print(f"doctor: clean — {len(notes)} notes, graph in sync, pending honest")
    return 0


# --- harvest -----------------------------------------------------------------

def stub_wikis(store):
    """Every lane's leftover wiki under this board.

    Before `default_root` climbed to the board, a worker in a lane resolved
    the folder beside its own copy of this file and `Store.ensure` made it:
    `<board>/.lanes/<slug>/pearde/wiki/`. Measured on this board 2026-09-02,
    19 lanes held 29 notes that way — 5 of them `remember` findings, which
    `git worktree remove` deletes with the lane. This finds them; `harvest`
    moves them.

    A lane whose wiki IS the live one — a symlink, a board mounted there on
    purpose — is not a stub and is skipped by `resolve()`."""
    board = store.root.parent
    lanes = board / ".lanes"
    out = []
    if not lanes.is_dir():
        return out
    live = store.root.resolve()
    for lane in sorted(lanes.iterdir()):
        for name in common.BOARD_DIRS:
            w = lane / name / "wiki"
            if not w.is_dir():
                continue
            try:
                if w.resolve() == live:
                    continue
            except OSError:
                continue
            out.append(w)
            break
    return out


def note_key(path):
    """What makes two notes the same note. `enqueue` dedupes a pending note
    on its `question:` and nothing else, so harvesting must ask the same
    question or it re-queues every gap a lane already asked; a source or a
    conclusion is its `title:`. The filename is never the key — `note_id`
    is time entropy, so two lanes writing the same finding a second apart
    get two names."""
    try:
        meta, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
    except OSError:
        return None
    for key in ("question", "title"):
        v = str(meta.get(key, "")).strip().strip('"').lower()
        if v:
            return v
    return None


def cmd_harvest(store, args):
    """Move every note a lane's stub wiki holds into the live record."""
    store.ensure()
    stubs = stub_wikis(store)
    if not stubs:
        print("harvest: no lane holds a wiki of its own — nothing stranded")
        return 0
    folders = ("pending", "sources", "conclusions")
    have = {}
    for folder in folders:
        d = store.root / folder
        have[folder] = {k for k in
                        (note_key(p) for p in d.rglob("*.md")
                         if p.name != "_index.md" and store.absorbed not in p.parents)
                        if k}
    moved, skipped = [], []
    for stub in stubs:
        lane = stub.parent.parent.name
        for folder in folders:
            src_dir = stub / folder
            if not src_dir.is_dir():
                continue
            for src in sorted(src_dir.rglob("*.md")):
                if src.name == "_index.md":
                    continue
                key = note_key(src)
                if key and key in have[folder]:
                    skipped.append((lane, folder, src.name))
                    if not args.dry:
                        src.unlink()
                    continue
                rel = src.relative_to(src_dir)
                target = store.root / folder / rel
                while target.exists():
                    target = target.with_name(
                        f"{target.stem}{hashlib.sha1(target.name.encode()).hexdigest()[:1]}.md")
                moved.append((lane, folder, target.name))
                if key:
                    have[folder].add(key)
                if args.dry:
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                src.unlink()
        if args.dry:
            continue
        # the emptied stub goes, so the next `harvest` has nothing to find.
        # Only the wiki — `<lane>/pearde/graphify` is the shared cache, a
        # symlink into <git-common-dir>/pearde-shared, and deleting through
        # it would take every lane's cache with it.
        if not any(stub.rglob("*.md")):
            shutil.rmtree(stub, ignore_errors=True)
            parent = stub.parent
            try:
                if parent.is_dir() and not any(parent.iterdir()):
                    parent.rmdir()
            except OSError:
                pass
    pre = "dry · " if args.dry else ""
    for lane, folder, name in moved:
        print(f"{pre}moved   {folder}/{name} <- {lane}")
    for lane, folder, name in skipped:
        print(f"{pre}already on record  {folder}/{name} <- {lane}")
    print(f"{pre}harvest: {len(moved)} note(s) recovered, {len(skipped)} "
          f"already on record, from {len(stubs)} lane wiki(s)")
    return 0


# --- the round --------------------------------------------------------------

# How many days a tool's output may age before the round is told to run it
# again. A sweep is a daily measurement whose delta only sharpens (scout's
# README), the corpus map goes stale on the commits the round itself lands,
# and the board notes are the vault's whole read layer — so the graph and the
# vault are re-run more often than the sweep, which costs a GitHub call per
# bucket. Knobs, not laws: WORKFLOW.md overrides each by name.
STALE_AFTER = {"scout": 7, "graph": 3, "vault": 1}


def _age_days(path):
    """Whole days since `path` was last written, or None when it is absent."""
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return None
    return int((dt.datetime.now().timestamp() - mtime) // 86400)


def _newest(directory, pattern="*"):
    """The most recently written entry matching `pattern`, or None."""
    try:
        entries = list(Path(directory).glob(pattern))
    except OSError:
        return None
    return max(entries, key=lambda p: p.stat().st_mtime, default=None)


def stale_rows(store):
    """[(days_over, tool, state, command)] — three `stat` calls and no note
    read, so the loop can print this on every pass without paying for the
    record. `days_over` is negative when the tool is current, 10**6 when it
    has never run, and the list is unsorted: callers rank it.
    """
    config = store.workflow()
    rows = []

    def row(name, age, what, command):
        limit = config.get(f"stale_after_{name}", STALE_AFTER[name])
        if age is None:
            rows.append((10 ** 6, name, f"{what} — never run", command))
        elif age > limit:
            rows.append((age - limit,
                         name, f"{what} — {age}d old, stale past {limit}d",
                         command))
        else:
            rows.append((-1, name, f"{what} — {age}d old", command))

    # scout: the sweep's own snapshots, wherever the tool keeps them.
    scout_sh = pearde_path.script("scout.sh")
    snap = _newest(Path(scout_sh).parent / "snapshots", "*.tsv") if scout_sh else None
    row("scout", _age_days(snap) if snap else None,
        "the sweep", "pearde scout sweep && pearde scout delta 7")

    # graph: graphify's corpus map, at the board's root beside this wiki.
    row("graph", _age_days(store.board / "graphify" / "graph.json"),
        "the corpus map", "pearde graph update")

    # vault: the board notes Dataview renders, and the note graph over them.
    row("vault", _age_days(store.root / "board"),
        "the board notes", "pearde knowledge board && pearde knowledge relink")
    return rows


def cmd_round(store, args):
    """What the round owes the KB — one line per tool, worst first.

    The read direction of the knowledge layer already ran every pass:
    `query` before a fork goes to the user. The WRITE direction never did.
    Nothing scheduled a sweep, nothing re-extracted the corpus after a
    collect landed, nothing regenerated the board notes the vault renders —
    so three tools sat beside the loop rather than in it, each waiting for a
    person to remember it existed. This verb is the one page that says which
    of them is behind and the exact command that clears it; `pearde next`
    prints the same rows as step 7, so a pass cannot run without seeing them.

    Reads only. Every row is a suggestion with a command, never a gate: a
    board with no ollama, no `gh` and no network still scans, still
    dispatches, and simply carries three rows saying so.
    """
    rows = stale_rows(store)
    notes = load_notes(store)
    pending = sorted(store.pending.glob("*.md"))
    sources = sum(1 for n in notes if n.kind == "sources")
    conclusions = sum(1 for n in notes if n.kind == "conclusions")
    stale = [r for r in rows if r[0] >= 0]
    print(f"knowledge: {len(notes)} notes ({conclusions} conclusions, "
          f"{sources} sources) · {len(pending)} pending · "
          + (f"{len(stale)} of {len(rows)} tools stale" if stale
             else "every tool current"))
    for over, name, state, command in sorted(rows, key=lambda r: -r[0]):
        print(f"  {'stale' if over >= 0 else 'ok   '} {name:<6} {state}")
        if over >= 0:
            print(f"         {command}")
    # A question standing in `pending/` is the KB asking the round for work,
    # the mirror of the round asking the KB at step 7. Naming the oldest ones
    # is what makes the queue a thing that drains rather than a thing that
    # grows: `research it, or delete it` is the whole rule.
    if pending:
        print(f"  pending — {len(pending)} question(s), oldest first;"
              " research one or delete it")
        for path in sorted(pending, key=lambda p: p.stat().st_mtime)[:3]:
            meta, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
            print(f"    {path.stem} · {meta.get('question', path.stem)}"
                  f" · {meta.get('priority', 'med')}")
    return 0


# --- CLI ----------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="knowledge.py",
        description="pearde knowledge — the research layer, whole.",
        epilog="The loop: query · enqueue · remember · conclude · relink · dashboard · doctor.\n"
           "The generated notes: board (one per PRD) · index (one per file in the map) · wiki.",
    )
    parser.add_argument("--root", help="KB folder (default: <repo>/pearde/wiki)")
    sub = parser.add_subparsers(dest="verb")

    p = sub.add_parser("remember", help="capture a finding as a source note (body on stdin)")
    p.add_argument("title")
    p.add_argument("--folder", help="subfolder of sources/ (e.g. scout)")
    p.add_argument("--tags", help="comma-separated")
    p.add_argument("--related", nargs="*", help="slugs, space- or comma-separated")
    p.add_argument("--provenance", help="where the finding came from — sweep, URL, route id")

    p = sub.add_parser("conclude", help="write a conclusion from >=2 sources (body on stdin)")
    p.add_argument("title")
    p.add_argument("--sources", required=True, help="comma-separated source slugs")
    p.add_argument("--tags", help="comma-separated")
    p.add_argument("--related", nargs="*", help="slugs, space- or comma-separated")
    p.add_argument("--force", action="store_true", help="overwrite an existing conclusion")

    p = sub.add_parser("enqueue", help="queue a research question")
    p.add_argument("question", nargs="+")
    p.add_argument("--priority", default="med", choices=["low", "med", "high"])
    p.add_argument("--requested-by", dest="requested_by")

    p = sub.add_parser("query", help="ask the KB; prints the gap when the answer is not on record")
    p.add_argument("question", nargs="+")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--no-enqueue", action="store_true",
                   help="report the gap without auto-enqueuing it")

    p = sub.add_parser("relink", help="rebuild the link graph (.graphify/graph.json), symmetrize related:")
    p = sub.add_parser("board", help="regenerate board/ — one linkable note per PRD with its needs, fed-by, memos")
    p = sub.add_parser("index", help="regenerate index/ — one note per file in the manifest, with its keywords")
    p = sub.add_parser("wiki", help="regenerate graphs/ community pages from the graph")
    p = sub.add_parser("dashboard", help="print the plain report; --write saves Dashboard.report.md")
    p.add_argument("--write", action="store_true")
    p = sub.add_parser("doctor", help="frontmatter, wikilinks, graph sync, pending age")
    p = sub.add_parser("harvest", help="move notes stranded in a lane's stub wiki into the record")
    p.add_argument("--dry", action="store_true", help="report what would move, move nothing")
    p = sub.add_parser("round", help="what the round owes the KB — one line per tool, worst first")

    args = parser.parse_args(argv)
    if not args.verb:
        parser.print_help()
        return 0
    store = Store(args.root or default_root())
    verbs = {
        "remember": cmd_remember,
        "conclude": cmd_conclude,
        "enqueue": cmd_enqueue,
        "query": cmd_query,
        "relink": cmd_relink,
        "board": cmd_board,
        "index": cmd_index,
        "wiki": cmd_wiki,
        "dashboard": cmd_dashboard,
        "doctor": cmd_doctor,
        "harvest": cmd_harvest,
        "round": cmd_round,
    }
    return verbs[args.verb](store, args)


if __name__ == "__main__":
    sys.exit(main())