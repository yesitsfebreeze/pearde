"""Print each unbound-waste hit with its surrounding words.

    hits.py <file>...
"""
import importlib.util, sys, os
spec = importlib.util.spec_from_file_location("prose", os.path.join(os.getcwd(), "resources/prose.py"))
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8").read()
    body = "\n".join(p.prose_lines(p.strip_code(t)))
    for w, at in p.unbound_hits(t):
        print(f"{f}: …{body[max(0,at-60):at+40]}…".replace("\n", " "))
