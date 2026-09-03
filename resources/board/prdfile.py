#!/usr/bin/env python3
"""pearde prdfile — one PRD file: its frontmatter, its boxes, its typed numbers.

Cut out of plan.py; plan.py re-exports every name here, so every caller that
imports `plan` keeps working. Python 3 stdlib only.
"""
import collections
import datetime
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
# win: a cp1252 console cannot encode the box/greek glyphs this prints,
# and the trailing summary dies on UnicodeEncodeError. Force UTF-8 out.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import time
import urllib.error
import urllib.request

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import memos as memolib  # noqa: E402 — on the path by the rule
import questions as qlib  # noqa: E402 — the drill count, one reader with list
import render as renderlib  # noqa: E402 — on the path by the rule
import workflows as wflib  # noqa: E402 — on the path by the rule
from boards import (PASS_FILE, state_dir)  # noqa: E402,F401



# Frontmatter: match a key by name at any indentation, anywhere in the block.
# Scalars and simple `- item` lists. Names are unique within one file.
KEY_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")
ITEM_RE = re.compile(r"^\s*-\s+(.*?)\s*$")


def strip_comment(v):
    # `^` as well as `\s+`: a value that is ONLY a comment is an empty value.
    # `est:   # the weight, only when complexity is absent` — the template's
    # own line — parsed to the comment TEXT while the leading run of spaces was
    # eaten by KEY_RE, so every reader of `est` got a sentence where a duration
    # was meant. `hours()` read it as 0.0 in silence; `dur()` reports it, which
    # is how it was found. A `#` inside a word (`repo: a#b`) is still a `#`.
    return re.sub(r"(^|\s+)#.*$", "", v).strip().strip("\"'")


# ── the parse cache ──────────────────────────────────────────────────────────
# `scan` is step 1 of every pass, the status line and the view daemon, and
# each call re-read and re-parsed every prd.md and every spec's frontmatter.
# The cache holds (fm, title, body) keyed on abspath + mtime_ns + size and is
# persisted to <board>/.state/parse-cache.json by `scan` — machine-local,
# git-ignored, never a source of truth: anything short of a clean current-
# version file reads as an empty cache, and every call stats the file anyway,
# so an edit made outside pearde (an editor, `git checkout`) is a miss and is
# re-parsed on that call. Stdlib only.
CACHE_VERSION = 1
_PCACHE = {}          # abspath -> {"mtime": ns, "size": n, "fm", "title", "body"}
_PCACHE_LOADED = False
_PCACHE_DIRTY = False  # a miss since the last save: scan() rewrites the file


def parse_cache_path(board):
    return os.path.join(state_dir(board), "parse-cache.json")


def parse_cache_load(board):
    """Fill the module cache from disk. Never raises; anything short of a
    clean current-version file means an empty cache and a cold parse."""
    global _PCACHE, _PCACHE_LOADED
    if _PCACHE_LOADED:
        return
    _PCACHE_LOADED = True
    try:
        with open(parse_cache_path(board), encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return
    files = data.get("files") if isinstance(data, dict) else None
    if isinstance(data, dict) and data.get("version") == CACHE_VERSION \
            and isinstance(files, dict):
        _PCACHE = files


def parse_cache_save(board):
    """Merge the run's parses back to disk, atomically. Never raises: a cache
    that fails to save just costs the next call a cold parse. Entries whose
    file no longer exists are dropped, so deleting a PRD shrinks the cache."""
    try:
        keep = {}
        for apath, e in _PCACHE.items():
            try:
                st = os.stat(apath)
            except OSError:
                continue
            if st.st_mtime_ns == e.get("mtime") and st.st_size == e.get("size"):
                keep[apath] = e
        path = parse_cache_path(board)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"version": CACHE_VERSION, "files": keep}, f)
        os.replace(tmp, path)
    except OSError:
        pass


def parse_prd(path):
    """(fm, title, body) for `path`, off the cache when its mtime+size still
    match. The returned fm is a fresh dict with fresh lists, so a caller that
    mutates it (`fm["state"] = …` in transitions/collect) cannot poison the
    cache — every key is copied one level, which is all fm ever holds."""
    try:
        apath = os.path.abspath(path)
        st = os.stat(apath)
    except OSError:
        return _parse_prd_uncached(path)
    e = _PCACHE.get(apath)
    if (e and e.get("mtime") == st.st_mtime_ns and e.get("size") == st.st_size):
        return ({k: list(v) if isinstance(v, list) else v
                 for k, v in e["fm"].items()},
                e["title"], e["body"])
    fm, title, body = _parse_prd_uncached(path)
    try:
        _PCACHE[apath] = {"mtime": st.st_mtime_ns, "size": st.st_size,
                          "fm": fm, "title": title, "body": body}
        global _PCACHE_DIRTY
        _PCACHE_DIRTY = True
    except OSError:
        pass
    return fm, title, body


def _parse_prd_uncached(path):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    fm, body_start = {}, 0
    if lines and lines[0].strip() == "---":
        i, cur_list = 1, None
        while i < len(lines) and lines[i].strip() != "---":
            line = lines[i]
            m = KEY_RE.match(line)
            item = ITEM_RE.match(line)
            if m:
                key, val = m.group(1), strip_comment(m.group(2))
                if val:
                    fm[key] = val
                    cur_list = None
                else:
                    fm[key] = []
                    cur_list = key
            elif item and cur_list is not None:
                v = strip_comment(item.group(1))
                if v:
                    fm[cur_list].append(v)
            i += 1
        body_start = i + 1
    body = "\n".join(lines[body_start:]).strip()
    title = None
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip().strip("<>").strip()
            break
    fm = {k: v for k, v in fm.items() if v != [] or k == "needs"}
    return fm, title, body


# Deliberately NOT `opens_an_unticked_box`, and deliberately left as it was
# when the gates widened. It answers a different question over a different
# population: the boxes under `## Acceptance` in `specs/*.md`, counted both
# ways to make a progress fraction, where `opens_an_unticked_box` reads the
# whole of `prd.md` to make a verdict. Its `[ xX]` capture is the fraction's
# alphabet — `[~]` is neither counted nor closed by it, because a struck box
# is a contract term withdrawn rather than a term met, and folding it into
# `closed/total` would move a bar that nothing was built behind. Matching it
# to the gates would be matching two rules that answer two questions.
#
# What it costs, said plainly because a reader meets it and not the argument
# above: a spec's Acceptance box spelled `+ [ ]`, `- []`, `1. [ ]` or with a
# tab after the marker is invisible to this pattern ENTIRELY — not in
# `closed`, not in `total`. So `closed == total` can be true while a contract
# term is still open, and the board offers the PRD at a clean n/n. That is
# survivable only because the `done` gates never read a spec at all
# (`done_boxes_are_ticked.rs` filters on `name == "prd.md"`), so no spec box
# in any spelling can make `collect` name a PRD a gate would refuse. An
# analyst writing `- [ ]` is what keeps the fraction honest.
BOX_RE = re.compile(r"^\s*[-*]\s+\[([ xX])\]", re.M)


def acceptance_of(text):
    """(closed, total) acceptance boxes in one spec's text.

    `## Acceptance` only. A box anywhere else in a spec is a note the analyst
    left itself, and counting it would make the number say something other
    than "how much of the contract is standing"."""
    closed = total = 0
    for sec in re.split(r"(?m)^##\s+", text)[1:]:
        head = sec.split("\n", 1)[0].strip().lower()
        if not head.startswith("acceptance"):
            continue
        for box in BOX_RE.findall(sec):
            total += 1
            closed += box.lower() == "x"
    return closed, total


def acceptance(prd):
    """(closed, total) over every spec of one PRD.

    This is the only thing on the board that moves while a worker works.
    Everything else — the state, the est, the report — is written at the
    transitions either side of it, so a plan that reads nothing else stands
    still for the whole of the run it is supposed to be showing."""
    sdir = os.path.join(prd["dir"], "specs")
    closed = total = 0
    for f in sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []:
        if not f.endswith(".md"):
            continue
        try:
            text = open(os.path.join(sdir, f), encoding="utf-8").read()
        except OSError:
            continue
        c, t = acceptance_of(text)
        closed, total = closed + c, total + t
    return closed, total


# The states in which a worker holds the PRD and its acceptance boxes are the
# live record of the run. `analyzing` holds it too, but an analyst writes the
# boxes rather than closing them — its progress is the spec files appearing.
HOLDING_STATES = {"claimed", "blocked"}

CLAIM_TS_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?)?"
    r"(?:Z|[+-]\d{2}:?\d{2})?)")


def claim_of(fm):
    """`claim: <worker> <started>` → {"who", "since"}, or None.

    The timestamp is whatever ISO-ish thing the orchestrator wrote. The worker
    name is the rest. Neither is required — a claim with no timestamp still
    says who holds the PRD."""
    raw = fm.get("claim")
    if not raw or isinstance(raw, list):
        return None
    raw = str(raw).strip()
    m = CLAIM_TS_RE.search(raw)
    who = (raw[:m.start()] + raw[m.end():]).strip() if m else raw
    return {"who": who, "since": m.group(1) if m else ""}


def strip_list_marker(rest):
    """What follows one Markdown list marker at the front of `rest`, or `None`
    when `rest` does not open a list item.

    A port of `strip_list_marker` in
    `shared/shared/tests/done_boxes_are_ticked.rs`, whose body mitosys, model
    and realm adopted on 2026-08-28 (`@infra/gates-adopt-the-best-matcher`).
    Kept as its own function so it can be read beside the Rust it mirrors.

    The three bullets are Markdown's three. The ordered arm is GFM's: `digits
    > 9` is GFM's own bound on an ordered marker, and it is what keeps a year
    or a version number from being read as a list marker; `)` is admitted
    beside `.` because GFM admits both."""
    if rest[:1] in ("-", "*", "+"):
        return rest[1:]
    digits = len(rest) - len(rest.lstrip("0123456789"))
    if digits == 0 or digits > 9:
        return None
    rest = rest[digits:]
    return rest[1:] if rest[:1] in (".", ")") else None


def opens_an_unticked_box(line):
    """True when `line` opens an unticked checkbox: a list marker, then a
    bracket pair holding nothing but whitespace.

    The marker is any of Markdown's three bullets or an ordered marker, and
    the gap between marker and bracket is any run of spaces, because all of
    those render as the same open box in every viewer the board is read in.
    A reader matching one spelling only is one a stray `*`-bulleted box walks
    past, and a board file is prose, written by hand, in five repositories.

    A ticked box and a struck box are closures and do not match: their
    brackets are not empty. `- [~]` is a box whose bar the code did not
    clear, closed with a reason beside it — never work that is merely still
    owed.

    This body is the four gates' body, which is the point: `collect` naming a
    PRD a gate would reject is the defect `body_has_open_box` exists to
    remove, and it comes back the moment the two disagree about what a box
    is."""
    rest = strip_list_marker(line.lstrip())
    if rest is None:
        return False
    rest = rest.lstrip(" ")
    if not rest.startswith("["):
        return False
    rest = rest[1:]
    end = rest.find("]")
    return end >= 0 and not rest[:end].strip()


def body_has_open_box(prd):
    """True when `prd.md` itself still carries an unticked box.

    The specs are not the whole contract. All four trees' `done` gates read
    the boxes in `prd.md` over the whole file, under every heading — mitosys's
    was scoped under `## Acceptance` until 2026-08-28 and is not any more — so
    a PRD whose specs are all closed can still be one the gate refuses.
    Clearing what the gates clear is what `collect` has to do, because saying
    "collect" on a PRD a gate would reject is how a board manufactures the
    `done`-with-open-boxes defect it is trying to remove.

    The match is `opens_an_unticked_box`, the gates' own matcher, not a
    literal `- [ ]`: a `* [ ]` box is red to every tree's gate, and until
    2026-08-28 it was invisible here. `- [~]` stays a closure under it. This
    is the one place the marker set matters, which is why it is not
    `acceptance_of`'s `== "x"` test."""
    try:
        text = open(os.path.join(prd["dir"], "prd.md"), encoding="utf-8").read()
    except OSError:
        return False
    return any(opens_an_unticked_box(l) for l in text.splitlines())


def standing(prd):
    """(fraction closed, closed, total, collect) for one PRD.

    `collect` is the whole point of reading the boxes: a PRD whose every
    acceptance box is closed while a worker still holds it is finished work
    waiting to be committed and set `done`. Until that happens every PRD
    behind it waits too, so it is the most valuable thing on the board.

    `frac`/`closed`/`total` stay the SPECS' numbers — they are the only thing
    that moves while a worker works, which is what the lane bar is drawn
    from. `collect` is the stricter question and answers from `prd.md` too;
    the two deliberately disagree, and `prds/memos/done-counts-which-boxes.md`
    is why."""
    closed, total = acceptance(prd)
    frac = (closed / total) if total else 0.0
    held = prd["state"] in HOLDING_STATES
    ready = bool(held and total and closed == total
                 and not body_has_open_box(prd))
    return frac, closed, total, ready


def hours(v):
    if not v or isinstance(v, list):
        return 0.0
    v = str(v).strip()
    m = re.match(r"^([\d.]+)\s*([mhd]?)$", v)
    if not m:
        return 0.0
    try:
        n = float(m.group(1))
    except ValueError:   # `..`, `1.2.3` — the shape matches, the number does not
        return 0.0
    unit = m.group(2)
    return n / 60 if unit == "m" else n * 8 if unit == "d" else n


# ── numbers a person typed ───────────────────────────────────────────────────
# Every weight on this board is hand-written: `complexity` on every spec by
# every analyst the board has ever dispatched, `priority` on every prd.md,
# `weight-default`, `gantt-day` and `claim-ttl` in settings.md. The population
# of writers is the population of workers, so the failure mode is a typo — and
# a bare `float()` over one of them turns that typo into a traceback in `scan`,
# step 1 of every pass, that names no PRD and stops every session on the
# board. Nothing here reads a number off a file a person wrote except through
# `num` and `dur`.
#
# A bad value reads as 0.0, which is what an UNSCORED value already reads as,
# and that is the whole of the decision: `compute_plan` and `weight_of` weigh
# an unscored PRD at the board average and `progress_terms` leaves it out of
# the average it computes, so a typo is weighed as "we do not know this one's
# size" rather than as free. What would be wrong is the SILENCE — a weight
# that quietly becomes 0 is a wrong number that looks like a real one, and it
# moves the PRD in the plan and in the progress percentage — so every bad
# value is said out loud, on stderr, naming the file a person has to open.
# Once per (file, key, value), never once per read: `complexity` is read by
# five functions in a pass and one typo is one problem.
_BAD_SEEN = set()
# a duration that is honestly zero — `0`, `0h`, `0.0m` — so `dur` does not
# report the one value `hours()` and a broken value agree on
ZERO_RE = re.compile(r"^0*\.?0*\s*[mhd]?$")


def bad_value(where, key, v):
    """Say once that a hand-written value is not a number. Never raises."""
    seen = (str(where), str(key), repr(v))
    if seen in _BAD_SEEN:
        return
    _BAD_SEEN.add(seen)
    print(f"plan: {where or '?'} — {key}: {v!r} is not a number, weighed as "
          f"unscored", file=sys.stderr)


def num(fm, key, where="", default=0):
    """A plain number off frontmatter — `complexity`, `priority`,
    `weight-default`. 0.0 when absent or empty, 0.0 AND a report when it is
    there and is not a number. Never raises."""
    v = fm.get(key, default)
    if v is None or v == "":
        return 0.0
    try:
        return float(v)
    except (TypeError, ValueError):
        bad_value(where, key, v)
        return 0.0


def dur(fm, key, where="", default=""):
    """A duration off frontmatter — `est`, `actual`, `gantt-day` — in hours.
    `hours()` reads the shapes; this names the file when a value is not one of
    them. 0.0 when absent or unreadable. Never raises."""
    v = fm.get(key, default)
    if v is None or v == "":
        return 0.0
    h = hours(v)
    if h == 0.0 and not ZERO_RE.match(str(v).strip()):
        bad_value(where, key, v)
    return h

# The states the loop moves work through. A board state outside LIVE_STATES is
# the user's own and terminal to the loop — the planner does not schedule it,
# and the view lists it as parked rather than folding it into `open`.
LIVE_STATES = {"open", "analyzing", "refine", "question", "specced",
               "claimed", "blocked", "failed"}

def question_counts(prd):
    """(questions, answers) in one PRD's body — the numbers step 2 asks for.

    A question is a `**Qn**` line under `## Questions`; an answer is the same
    line under `## Answers`. Counting them here is what stops a pass opening
    every `question` PRD to find out whether it is still asking."""
    out = {}
    for sec in re.split(r"(?m)^##\s+", prd.get("body") or "")[1:]:
        head, _, rest = sec.partition("\n")
        head = head.strip().lower()
        if head.startswith(("questions", "answers")):
            out[head[:1]] = len(re.findall(r"(?m)^\s*(?:\*\*Q|[-*]\s)", rest))
    return out.get("q", 0), out.get("a", 0)


# One line of a pass, written back. `**Q1** *(answered 2026-08-28 14:22)*
# — <the decision>`: the id says which fork, the stamp says when it was
# settled, and everything after the dash is the decision itself. The stamp is
# optional — passes answered before the view wrote one still read, they only
# lose their place in a date order.
ANSWER_LINE_RE = re.compile(
    r"^\s*\*\*(Q?\d+[a-z]?)\*\*\s*"
    r"(?:\*?\(answered\s+([^)]*)\)\*?\s*)?[\u2014\u2013:-]*\s*(.*)$")


def drill_questions(board):
    """[(rel, qid, title, out)] \u2014 the drill, as data.

    The unanswered questions `questions.unanswered` counts, each marked `out`
    when the pass file's `## Asked` already lists it \u2014 by title, normalized,
    because that file holds the words the pass put to the user and drill.md
    sends a question there precisely so it is never re-put. Two entry points,
    one reader: `cmd_scan`'s drill section prints the list, and
    transitions.py `gate_claim` counts the ones still unput and refuses when
    two or more stand \u2014 @references/drill.md \u00a7 The board's own frontier."""
    un = qlib.unanswered(board)
    if not un:
        return un
    try:
        text = open(os.path.join(board, PASS_FILE), encoding="utf-8").read()
    except OSError:
        text = ""
    asked = re.sub(r"\s+", " ",
                   "\n".join(_h2_sections(text, "Asked"))).lower().strip()
    out = []
    for rel, qid, title in un:
        normed = re.sub(r"\s+", " ", title.lower()).strip()
        out.append((rel, qid, title,
                    bool(title) and normed in asked))
    return out

# `### Q1: the fork` — the question's own title, so an answer can be read
# without opening the PRD it came out of.
QUESTION_HEAD_RE = re.compile(r"(?m)^###\s+(Q?\d+[a-z]?)\s*[:.\u2014\u2013-]?\s*(.*)$")


def _h2_sections(body, name):
    """Every `## <name>` section's text. A pass can be asked twice — a second
    `## Questions` pass is a second section, not a replacement."""
    out = []
    for m in re.finditer(r"(?m)^##\s+" + name + r"\b[^\n]*$", body or ""):
        rest = body[m.end():]
        nxt = re.search(r"(?m)^##\s+", rest)
        out.append(rest[:nxt.start()] if nxt else rest)
    return out


def _qid(raw):
    q = raw.upper()
    return q if q.startswith("Q") else "Q" + q


def answers_of(prd):
    """Every answer written back into one PRD, in the order the file has them.

    The asks view moves an answered question out of the inbox and into the
    answered panel, and it needs the answer itself to do it — the question it
    settles, the decision, and when it was made. Reading it out of the file is
    what makes a redraw, a reload and a second reader agree: the PRD is the
    record, this is only how it is read."""
    body = prd.get("body") or ""
    titles = {}
    for sec in _h2_sections(body, "Questions"):
        for m in QUESTION_HEAD_RE.finditer(sec):
            titles.setdefault(_qid(m.group(1)), m.group(2).strip())
    out, cur = [], None
    for sec in _h2_sections(body, "Answers"):
        cur = None
        for line in sec.splitlines():
            m = ANSWER_LINE_RE.match(line)
            if m:
                qid = _qid(m.group(1))
                cur = {"id": qid, "date": (m.group(2) or "").strip(),
                       "text": m.group(3).strip(),
                       "question": titles.get(qid, "")}
                out.append(cur)
            elif cur is not None and line.strip():
                # a decision that runs over one line stays one answer
                cur["text"] = (cur["text"] + " " + line.strip()).strip()
    return out
