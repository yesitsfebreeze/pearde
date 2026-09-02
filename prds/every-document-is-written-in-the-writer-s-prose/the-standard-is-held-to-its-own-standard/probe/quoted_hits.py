#!/usr/bin/env python3
"""How many prose.py unbound-waste hits sit inside a double-quoted span —
the shape of a document quoting the bad prose it bans."""
import os, subprocess, sys
ROOT = os.environ.get("PEARDE_ROOT", os.getcwd())
sys.path.insert(0, os.path.join(ROOT, "resources"))
import prose

files = subprocess.run(["git", "-C", ROOT, "ls-files", "*.md"],
                       capture_output=True, text=True, check=True).stdout.split()
tot = quoted = 0
per = []
for rel in files:
    text = open(os.path.join(ROOT, rel)).read()
    body = "\n".join(prose.prose_lines(prose.strip_code(text)))
    hits = prose.unbound_hits(text)
    if not hits:
        continue
    q = 0
    for _, pos in hits:
        # inside a "..." span on the same line?
        ls = body.rfind("\n", 0, pos) + 1
        le = body.find("\n", pos)
        le = len(body) if le < 0 else le
        # count quotes from start of the paragraph-ish window
        if body.count('"', ls, pos) % 2 == 1 or body.count('"', 0, pos) % 2 == 1:
            q += 1
    tot += len(hits); quoted += q
    per.append((rel, len(hits), q))
for rel, n, q in sorted(per, key=lambda r: -r[2])[:10]:
    print(f"{rel}: {n} hits, {q} inside a quoted span")
print(f"total: {tot} hits, {quoted} inside a quoted span, {len(per)} files")
