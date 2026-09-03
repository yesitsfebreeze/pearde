#!/usr/bin/env python3
"""Measure the cuttable surface of a set of `.md` files.

Splits every file's words into fenced code, table rows, frontmatter,
headings, bullet text and paragraph prose — the last two are the only
words a density rewrite can touch, and a table row is a fact that must
survive as a row.

    surface.py <file>...
"""
import re
import sys

FENCE = re.compile(r"^\s*```")


def measure(path):
    text = open(path, encoding="utf-8").read()
    buckets = dict(code=0, front=0, table=0, head=0, bullet=0, prose=0)
    in_fence = in_front = False
    for i, line in enumerate(text.splitlines()):
        s = line.strip()
        n = len(s.split())
        if s == "---" and i == 0:
            in_front = True
            continue
        if in_front:
            if s == "---":
                in_front = False
            else:
                buckets["front"] += n
            continue
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            buckets["code"] += n
        elif s.startswith("|"):
            buckets["table"] += n
        elif s.startswith("#"):
            buckets["head"] += n
        elif s.startswith(("-", "*", ">")) or re.match(r"^\d+\.", s):
            buckets["bullet"] += n
        else:
            buckets["prose"] += n
    return buckets


def main(argv):
    tot = dict(code=0, front=0, table=0, head=0, bullet=0, prose=0)
    print(f"{'file':52} {'all':>5} {'code':>5} {'front':>5} {'table':>5} "
          f"{'head':>5} {'bullet':>6} {'prose':>6} {'cuttable':>8}")
    for p in argv:
        b = measure(p)
        for k in b:
            tot[k] += b[k]
        a = sum(b.values())
        cut = b["bullet"] + b["prose"]
        print(f"{p[-52:]:52} {a:5} {b['code']:5} {b['front']:5} {b['table']:5} "
              f"{b['head']:5} {b['bullet']:6} {b['prose']:6} "
              f"{cut:6} {100*cut/a if a else 0:4.0f}%")
    a = sum(tot.values())
    cut = tot["bullet"] + tot["prose"]
    print(f"{'TOTAL':52} {a:5} {tot['code']:5} {tot['front']:5} {tot['table']:5} "
          f"{tot['head']:5} {tot['bullet']:6} {tot['prose']:6} "
          f"{cut:6} {100*cut/a if a else 0:4.0f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
