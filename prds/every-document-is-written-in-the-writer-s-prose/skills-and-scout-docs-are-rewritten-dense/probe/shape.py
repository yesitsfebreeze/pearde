"""How each file's words are shaped: frontmatter, prose, table, list, heading.

    shape.py <file>...   words per shape, and the share that is compressible prose
"""
import importlib.util, os, sys
spec = importlib.util.spec_from_file_location("prose", os.path.join(os.getcwd(), "resources/prose.py"))
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)

tot = {}
for f in sys.argv[1:]:
    text = p.strip_code(open(f, encoding="utf-8").read())
    kinds = {"frontmatter": 0, "prose": 0, "table": 0, "list": 0, "heading": 0}
    fm = text.startswith("---")
    seen = 0
    for line in text.splitlines():
        s = line.strip()
        if fm and s == "---":
            seen += 1
            continue
        n = len(s.split())
        if fm and seen < 2:
            kinds["frontmatter"] += n
        elif s.startswith("|"):
            kinds["table"] += n
        elif s.startswith("#"):
            kinds["heading"] += n
        elif s.startswith(("-", "*", ">")) or (s[:2].rstrip(".").isdigit() and s[:1].isdigit()):
            kinds["list"] += n
        else:
            kinds["prose"] += n
    for k, v in kinds.items():
        tot[k] = tot.get(k, 0) + v
    print(f"{f}: " + " ".join(f"{k}={v}" for k, v in kinds.items()))
print("TOTAL: " + " ".join(f"{k}={v}" for k, v in tot.items()))
print("prose share: %.0f%%" % (100 * tot["prose"] / sum(tot.values())))
