#!/usr/bin/env python3
"""Pass-two probe: does the mtime parse cache get warm `scan` under 40 ms?

Reuses parsecache (mechanism proved in pass one) and now simulates the REAL
wiring: plan.parse_prd replaced by a cached wrapper for every call plan.py
makes during cmd_scan — _scan_one's prd.md parse AND spec_data's spec parse,
plus questions.py's own parse of every prd.md. Prints one number per run.
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
for _ in range(6):
    if os.path.isfile(os.path.join(REPO, "resources", "board", "plan.py")):
        break
    REPO = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(REPO, "resources", "board"))
sys.path.insert(0, os.path.join(REPO, "resources"))
import plan as planlib      # noqa: E402
import parsecache           # noqa: E402
import questions as qlib    # noqa: E402

CACHE = os.path.join(HERE, "state", "attempt-cache.json")


def wire(cache):
    """Replace both parsers with the cached one, exactly as the real change
    would: parse_prd on plan (prd.md + specs) and parse on questions."""
    orig_plan, orig_q = planlib.parse_prd, qlib.parse

    def cached_plan(path):
        return parsecache.parse_prd_cached(path, cache, orig_plan)

    def cached_q(path):
        fm, title, body = parsecache.parse_prd_cached(
            path, cache, orig_plan)
        return fm, body

    planlib.parse_prd = cached_plan
    qlib.parse = cached_q


def run_once():
    t0 = time.perf_counter()
    planlib.cmd_scan(os.path.join(REPO, ".pearde"))
    return (time.perf_counter() - t0) * 1000


def main():
    runs = sys.argv[1] if len(sys.argv) > 1 else "5"
    runs = int(runs)

    cache = {}
    wire(cache)
    ms_cold = run_once()
    print(f"cold (in-proc cache fills): {ms_cold:7.1f} ms")

    # persist, reload from disk, run again — the "next process" warm case
    parsecache.save_cache(CACHE, cache)
    for i in range(runs):
        cache = parsecache.load_cache(CACHE)
        wire(cache)
        ms = run_once()
        print(f"warm run {i + 1}                    : {ms:7.1f} ms")
    os.remove(CACHE)


if __name__ == "__main__":
    main()
