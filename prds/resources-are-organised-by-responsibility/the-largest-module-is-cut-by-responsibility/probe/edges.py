"""Name every cross-section read in plan.py, and say which ones are cycles.

Run: python3 edges.py <path-to-plan.py>
The section map says a pair reads each other; this says WHICH name does it and
from which line, and whether the read happens at import time (a real cycle a
module split cannot survive) or inside a function body (a late read, which two
modules can hold either side of).
"""
import ast, collections, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else "resources/board/plan.py"
src = open(path).read()
lines = src.splitlines()
marks = [(i + 1, re.sub(r"\s*─+\s*$", "", l[5:]).strip())
         for i, l in enumerate(lines) if l.startswith("# ── ")]
bounds = []
for n, (ln, name) in enumerate(marks):
    end = marks[n + 1][0] - 1 if n + 1 < len(marks) else len(lines)
    bounds.append((name, ln, end))
if marks and marks[0][0] > 1:
    bounds.insert(0, ("<preamble>", 1, marks[0][0] - 1))
tree = ast.parse(src)


def sect_of(ln):
    for name, a, b in bounds:
        if a <= ln <= b:
            return name
    return "?"


owner = {}
for node in tree.body:
    ns = []
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        ns = [node.name]
    elif isinstance(node, ast.Assign):
        ns = [t.id for t in node.targets if isinstance(t, ast.Name)]
    for nm in ns:
        owner[nm] = sect_of(node.lineno)

# a read is "at import time" when no enclosing FunctionDef/ClassDef holds it
deferred = set()
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        for sub in ast.walk(node):
            deferred.add(id(sub))

edges = collections.defaultdict(list)
for node in tree.body:
    home = sect_of(node.lineno)
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
            o = owner.get(sub.id)
            if o and o != home:
                when = "deferred" if id(sub) in deferred else "IMPORT-TIME"
                edges[(home, o)].append((sub.id, sub.lineno, when))

pairs = set(edges)
print("cross-section reads, cycles marked\n")
for (f, t), hits in sorted(edges.items()):
    cyc = " ** CYCLE **" if (t, f) in pairs else ""
    hard = [h for h in hits if h[2] == "IMPORT-TIME"]
    names = sorted({h[0] for h in hits})
    print("%s -> %s  (%d reads)%s" % (f, t, len(hits), cyc))
    print("   names: " + ", ".join(names))
    if hard:
        print("   IMPORT-TIME: " + ", ".join(
            "%s:%d" % (h[0], h[1]) for h in sorted(set(hard))))
    print()

print("=== cycles: %d pair(s)" % (sum(1 for p in pairs if (p[1], p[0]) in pairs) // 2))
