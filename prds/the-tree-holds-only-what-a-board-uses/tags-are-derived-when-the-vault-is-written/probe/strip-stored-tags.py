#!/usr/bin/env python3
"""Strip the `tags:` block from every authored memo and workflow on a board.

    python3 strip-stored-tags.py <board>          # e.g. .pearde

Pass one of this PRD deleted the `retag` verbs; this is the one-shot that
takes the values they used to write out of the 67 authored records, so
`memos.py check` and `workflows.py check` stop calling `tags:` a key that is
not theirs. Line-based on purpose: the block is `tags:` followed by `  - `
items, and nothing else in a memo's frontmatter has that shape.

Idempotent — a file with no `tags:` block is left byte-identical. Prints the
count it changed.
"""
import glob
import os
import sys


def strip(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end < 0:
        return False
    front, rest = text[:end], text[end:]
    out, in_block = [], False
    for line in front.split("\n"):
        if line.startswith("tags:"):
            in_block = True
            continue
        if in_block:
            if line.startswith("  - "):
                continue
            in_block = False
        out.append(line)
    new = "\n".join(out) + rest
    if new == text:
        return False
    open(path, "w", encoding="utf-8").write(new)
    return True


def main(argv):
    board = argv[1] if len(argv) > 1 else ".pearde"
    n = 0
    for sub in ("memos", "workflows"):
        for path in sorted(glob.glob(os.path.join(board, sub, "*.md"))):
            if os.path.basename(path) == "README.md":
                continue
            n += strip(path)
    print(f"stripped `tags:` from {n} authored record(s) under {board}/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
