#!/usr/bin/env python3
"""Bench the parse-cache probe against the real board, read-only.

Usage: python3 bench.py [board]   (default: repo's .pearde)

Three numbers:
  cold  — full walk + parse of every prd.md and spec .md, empty cache
  warm  — same walk, cache from the cold run, nothing on disk touched
  edit  — warm cache, but one spec file was touched first: proves only
          that one file re-parses and the new content is what comes back

Writes nothing under .pearde/ — the cache file lives beside this script,
in the PRD's own probe/ dir, never under .pearde/prds/ (that would make it
a PRD directory) and never under the real .pearde/.state/ (outside this
PRD's footprint at analysis time).
"""
import os
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
for _ in range(6):
    if os.path.isfile(os.path.join(REPO, "resources", "board", "plan.py")):
        break
    REPO = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(REPO, "resources", "board"))
sys.path.insert(0, os.path.join(REPO, "resources"))
import plan as planlib  # noqa: E402
import parsecache  # noqa: E402

CACHE_PATH = os.path.join(HERE, "state", "parse-cache.json")


def walk_and_parse(board, cache, stats):
    """Everything real `_scan_one` + `spec_data` parse: every prd.md, every
    spec's frontmatter. Read-only — no write anywhere under `board`."""
    scan_root = planlib.prds_dir(board)
    n_prd = n_spec = 0
    for root, dirs, files in os.walk(scan_root):
        if "prd.md" in files and root != scan_root:
            parsecache.parse_prd_cached(
                os.path.join(root, "prd.md"), cache, planlib.parse_prd, stats)
            n_prd += 1
        sdir = os.path.join(root, "specs")
        if os.path.isdir(sdir) and root != sdir:
            for f in sorted(os.listdir(sdir)):
                if f.endswith(".md"):
                    parsecache.parse_prd_cached(
                        os.path.join(sdir, f), cache, planlib.parse_prd,
                        stats)
                    n_spec += 1
        dirs[:] = [d for d in dirs if d not in ("specs",)]
    return n_prd, n_spec


def run_edit_detection_probe():
    """A fixture board, built fresh under a runtime tempdir (never under
    .pearde/prds/, per the brief). Cold-parses it, warms the cache, edits
    ONE file, and asserts the reparse touches that file alone and returns
    the new content — the PRD's "never serve a stale answer" constraint."""
    tmp = tempfile.mkdtemp(prefix="parsecache-fixture-")
    cache_path = os.path.join(tmp, "cache.json")
    try:
        prds = os.path.join(tmp, "prds")
        for i in range(5):
            d = os.path.join(prds, f"prd-{i}")
            os.makedirs(os.path.join(d, "specs"), exist_ok=True)
            with open(os.path.join(d, "prd.md"), "w", encoding="utf-8") as f:
                f.write(f"---\nstate: open\npriority: {i}\n---\n\n# PRD {i}\n")
            with open(os.path.join(d, "specs", "spec01.md"), "w",
                      encoding="utf-8") as f:
                f.write("---\ncomplexity: 3\n---\n\n# spec\n")

        cache = {}
        walk_and_parse(tmp, cache, {})
        parsecache.save_cache(cache_path, cache)

        # untouched reload: everything should hit
        cache2 = parsecache.load_cache(cache_path)
        stats = {}
        walk_and_parse(tmp, cache2, stats)
        assert stats.get("miss", 0) == 0, f"expected no misses, got {stats}"
        assert stats.get("hit", 0) == 10, f"expected 10 hits, got {stats}"

        # edit exactly one file — content AND therefore size changes
        target = os.path.join(prds, "prd-2", "prd.md")
        with open(target, "w", encoding="utf-8") as f:
            f.write("---\nstate: open\npriority: 99\n---\n\n# PRD 2 edited\n")

        cache3 = parsecache.load_cache(cache_path)
        stats3 = {}
        walk_and_parse(tmp, cache3, stats3)
        assert stats3.get("miss", 0) == 1, (
            f"expected exactly 1 miss after 1 edit, got {stats3}")
        assert stats3.get("hit", 0) == 9, f"expected 9 hits, got {stats3}"
        fm, title, body = parsecache.parse_prd_cached(
            target, cache3, planlib.parse_prd)
        assert fm.get("priority") == "99", f"stale value served: {fm}"
        assert title == "PRD 2 edited", f"stale title served: {title!r}"
        print("edit-detection: pass (1 file changed -> exactly 1 reparse, "
              "new content served)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def timed(fn):
    t0 = time.perf_counter()
    r = fn()
    return r, (time.perf_counter() - t0) * 1000


def main():
    board = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, ".pearde")

    # cold: uncached, real parse_prd on every file
    stats_cold = {}
    cache_cold = {}
    (n_prd, n_spec), ms_cold = timed(
        lambda: walk_and_parse(board, cache_cold, stats_cold))
    print(f"cold : {ms_cold:7.2f} ms  ({n_prd} prd.md, {n_spec} specs, "
          f"hit={stats_cold.get('hit', 0)} miss={stats_cold.get('miss', 0)})")

    # simulate "next process": persist, reload fresh, parse again untouched
    parsecache.save_cache(CACHE_PATH, cache_cold)
    cache_warm = parsecache.load_cache(CACHE_PATH)
    stats_warm = {}
    _, ms_warm = timed(
        lambda: walk_and_parse(board, cache_warm, stats_warm))
    print(f"warm : {ms_warm:7.2f} ms  (hit={stats_warm.get('hit', 0)} "
          f"miss={stats_warm.get('miss', 0)})")
    os.remove(CACHE_PATH)

    # edit-detection, against a fixture board built fresh at run time —
    # never the real board's own prd.md, per the brief: fixtures live in a
    # directory made at run time, never under .pearde/prds/.
    run_edit_detection_probe()

    # corrupt-cache fallback: garbage on disk must not raise, must read as {}
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        f.write("{not json")
    got = parsecache.load_cache(CACHE_PATH)
    print(f"corrupt cache -> {got!r} (expect {{}})")

    # version-mismatch fallback
    import json
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump({"version": 999, "files": {"x": {}}}, f)
    got = parsecache.load_cache(CACHE_PATH)
    print(f"version mismatch -> {got!r} (expect {{}})")

    os.remove(CACHE_PATH)


if __name__ == "__main__":
    main()
