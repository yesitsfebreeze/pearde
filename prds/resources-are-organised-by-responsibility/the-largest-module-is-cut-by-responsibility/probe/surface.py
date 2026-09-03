"""What the rest of the tree reads off `plan`.

Run: python3 surface.py <repo-root>
Walks every .py under resources/ that imports plan, and collects every
attribute read off the module object. That set is the contract the cut must
keep: whatever lands in a sibling module still has to answer to `plan.<name>`,
or a caller outside this PRD's footprint breaks.
"""
import ast, collections, os, sys

root = sys.argv[1] if len(sys.argv) > 1 else "."
res = os.path.join(root, "resources")

used = collections.defaultdict(set)   # name -> files that read it
for dirpath, dirnames, filenames in os.walk(res):
    dirnames[:] = [d for d in dirnames if d != "__pycache__"]
    for fn in filenames:
        if not fn.endswith(".py"):
            continue
        p = os.path.join(dirpath, fn)
        if os.path.abspath(p) == os.path.abspath(os.path.join(res, "board", "plan.py")):
            continue
        try:
            tree = ast.parse(open(p).read())
        except SyntaxError:
            continue
        alias = None
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    if a.name == "plan":
                        alias = a.asname or "plan"
            if isinstance(node, ast.ImportFrom) and node.module == "plan":
                for a in node.names:
                    used[a.name].add(os.path.relpath(p, root))
        if not alias:
            continue
        for node in ast.walk(tree):
            if (isinstance(node, ast.Attribute)
                    and isinstance(node.value, ast.Name)
                    and node.value.id == alias):
                used[node.attr].add(os.path.relpath(p, root))

print("plan's public surface: %d names read from %d files\n" % (
    len(used), len({f for s in used.values() for f in s})))
for name in sorted(used):
    print("%-24s %s" % (name, " ".join(sorted(used[name]))))
