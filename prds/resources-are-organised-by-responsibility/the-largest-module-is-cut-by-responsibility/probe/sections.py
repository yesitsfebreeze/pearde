"""Map plan.py's sections: what each defines, and what it uses from the others.

Run: python3 sections.py <path-to-plan.py>
Prints one block per `# ── <name> ──` section — its line span, its top-level
names, and the sections it reads names out of. That cross-section table is the
thing the cut is decided on: a section nobody reads from can leave alone; a
pair that read each other cannot be separated without a facade.
"""
import ast, collections, sys, re

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


owner = {}          # top-level name -> section
defines = collections.defaultdict(list)
for node in tree.body:
    names = []
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        names = [node.name]
    elif isinstance(node, ast.Assign):
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        names = [node.target.id]
    for nm in names:
        owner[nm] = sect_of(node.lineno)
        defines[sect_of(node.lineno)].append(nm)

uses = collections.defaultdict(collections.Counter)
for node in tree.body:
    home = sect_of(node.lineno)
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
            o = owner.get(sub.id)
            if o and o != home:
                uses[home][o] += 1

print("%s — %d lines, %d sections\n" % (path, len(lines), len(bounds)))
for name, a, b in bounds:
    ds = defines.get(name, [])
    print("── %s  [%d-%d] %d lines · %d names" % (name, a, b, b - a + 1, len(ds)))
    if ds:
        print("   defines: " + ", ".join(ds))
    if uses[name]:
        print("   reads:   " + ", ".join("%s(%d)" % (k, v)
                                         for k, v in uses[name].most_common()))
    print()

print("\n=== cross-section edges (from -> to: count)")
for f in uses:
    for t, c in uses[f].most_common():
        print("%-45s -> %-45s %d" % (f, t, c))
