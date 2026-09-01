#!/usr/bin/env python3
"""Probe: a parse cache for `plan.parse_prd`, keyed on (path, mtime, size).

Pass one for scan-parses-the-board-once-and-caches-it-by-mtime. Proves the
mechanism against the real board (read-only) before it moves into
resources/board/plan.py. Not wired into the tree — the implementer's spec
does that.

Design matches the PRD's constraints:
  - cache is a single JSON file, machine-local, never a source of truth
  - keyed on path + mtime_ns + size; a mismatch on either is a cache miss
  - missing/corrupt/unreadable/version-mismatched cache -> empty dict,
    silently, never raises
  - stdlib only
"""
import json
import os

CACHE_VERSION = 1


def load_cache(path):
    """{abspath: {"mtime": ns, "size": n, "fm": {}, "title": s, "body": s}}
    or {} on anything short of a clean, current-version file. Never raises."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict) or data.get("version") != CACHE_VERSION:
        return {}
    files = data.get("files")
    return files if isinstance(files, dict) else {}


def save_cache(path, files):
    """Atomic write (tmp + rename) so a crash mid-write never leaves a
    corrupt file for the next reader — load_cache would silently discard it
    anyway, but a torn write is still worth not producing. Never raises: a
    cache that fails to save just costs the next call a cold parse."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"version": CACHE_VERSION, "files": files}, f)
        os.replace(tmp, path)
    except OSError:
        pass


def parse_prd_cached(path, cache, parse_prd, stats=None):
    """(fm, title, body) for `path`, off `cache` when its mtime+size still
    match, off `parse_prd` (plan.py's real parser) otherwise — and either way
    `cache` is left holding the current, correct entry.

    `stats`, when passed, is a dict this bumps `hit`/`miss` on, so a bench
    can report the split without instrumenting the caller."""
    apath = os.path.abspath(path)
    try:
        st = os.stat(apath)
    except OSError:
        # the file the tree walk just found is gone by the time we stat it —
        # let the real parser hit the same race and handle it the same way
        # it always has.
        return parse_prd(path)
    entry = cache.get(apath)
    if (entry and entry.get("mtime") == st.st_mtime_ns
            and entry.get("size") == st.st_size):
        if stats is not None:
            stats["hit"] = stats.get("hit", 0) + 1
        return entry["fm"], entry["title"], entry["body"]
    if stats is not None:
        stats["miss"] = stats.get("miss", 0) + 1
    fm, title, body = parse_prd(path)
    cache[apath] = {"mtime": st.st_mtime_ns, "size": st.st_size,
                     "fm": fm, "title": title, "body": body}
    return fm, title, body
