"""Swap a skill file's body, keeping its frontmatter byte-identical.

    splice.py <bodies-dir> <skill-file>...
"""
import sys, os

bodies, files = sys.argv[1], sys.argv[2:]
for f in files:
    name = os.path.basename(f)
    new = os.path.join(bodies, name)
    if not os.path.exists(new):
        continue
    text = open(f, encoding="utf-8").read()
    assert text.startswith("---\n"), f
    end = text.index("\n---\n", 3) + len("\n---\n")
    open(f, "w", encoding="utf-8").write(text[:end] + open(new, encoding="utf-8").read())
    print("spliced", f)
