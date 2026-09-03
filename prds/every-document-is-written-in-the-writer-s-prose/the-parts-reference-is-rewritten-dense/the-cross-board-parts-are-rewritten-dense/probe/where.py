#!/usr/bin/env python3
"""Where each unbound waste word sits, which `prose.py check` counts but
never locates.

    where.py <path>...    the sentence around every hit, in file order

Reuses `prose.py`'s own `prose_lines`, `strip_code` and `unbound_hits`, so a
hit printed here is the same hit the checker counts — the tool is a locator,
never a second opinion.
"""
import os, sys

# The tree being checked is the cwd, never the probe's own repo — the probe
# sits on the board and the rewrite happens in a lane, so importing the
# checker beside the probe would grade one tree with another's rules.
HERE = os.path.dirname(os.path.abspath(__file__))
BOARD_ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 6))
for root in (os.getcwd(), BOARD_ROOT):
    if os.path.isfile(os.path.join(root, "resources", "prose.py")):
        sys.path.insert(0, os.path.join(root, "resources"))
        break
else:
    sys.exit("where.py: no resources/prose.py in the cwd or beside the probe")
import prose  # noqa: E402


def located(text):
    """Each hit as (waste word, the prose line holding it)."""
    lines = prose.prose_lines(prose.strip_code(text))
    body = "\n".join(lines)
    starts, at = [], 0
    for ln in lines:
        starts.append(at)
        at += len(ln) + 1
    out = []
    for word, off in prose.unbound_hits(text):
        i = max(j for j, s in enumerate(starts) if s <= off)
        out.append((word, lines[i]))
    return out


def main(paths):
    total = 0
    for path in paths:
        hits = located(open(path).read())
        total += len(hits)
        print(f"== {path}: {len(hits)}")
        for word, line in hits:
            print(f"  [{word}] {line}")
    print(f"total {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
