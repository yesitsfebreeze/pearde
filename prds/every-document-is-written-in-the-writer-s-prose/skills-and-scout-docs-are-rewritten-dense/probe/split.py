"""Per file: unbound hits in the whole file vs in the body alone, with context."""
import importlib.util, sys, os
spec = importlib.util.spec_from_file_location("prose", os.path.join(os.getcwd(), "resources/prose.py"))
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
def ctx(t):
    body = "\n".join(p.prose_lines(p.strip_code(t)))
    return [f"…{body[max(0,at-55):at+35]}…".replace("\n"," ") for w, at in p.unbound_hits(t)]
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8").read()
    b = t.split("\n---\n", 1)[1] if t.startswith("---\n") else t
    full, body = ctx(t), ctx(b)
    fm = len(full) - len(body)
    ml_f, ml_b = p.mean_sentence_length(t), p.mean_sentence_length(b)
    if full or ml_f > 24:
        print(f"{f}: {len(full)} hits ({fm} frontmatter, {len(body)} body) · mean {ml_f:.1f} full / {ml_b:.1f} body")
        for c in body: print("   body", c)
