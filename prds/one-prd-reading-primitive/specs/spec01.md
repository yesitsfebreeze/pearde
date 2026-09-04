---
complexity: 8
footprint:
  - resources/common.py
---

# spec01 — common.py gains the PRD reader

`resources/common.py` gains `prd_shape(dir_path)`: `(fm, title, body, specs,
children, problems)` for one PRD directory — the frontmatter of its
`prd.md`, every spec under `specs/` as `(name, fm, title, body)`, the
basenames of every immediate child directory holding its own `prd.md`, and
`problems` as one sentence per way the shape was short of whole (no closed
fence on `prd.md`, no closed fence on a spec, no `state:` key). It decides
nothing — no transition, no gate, no completeness call — only facts and
problems, the line the PRD's own `## Fails when` draws.

Alongside it, `_clean` (the comment-stripping used by `split_frontmatter`)
gains the same fix `resources/board/prdfile.py` `strip_comment` already
carried: a value that is *only* a trailing comment (`est:   # the weight,
only when complexity is absent`) now reads as absent everywhere
`common.split_frontmatter` is used, not only where `prdfile.py`'s own copy
ran.

This spec's work already stands, built and verified in a scratch clone
(`git clone --shared`) of this repo's HEAD; the diff below is the whole of
it, ready to apply to `resources/common.py`.

```diff
--- a/resources/common.py
+++ b/resources/common.py
@@ -9,6 +9,7 @@
     read_text(path)                the text, or "" when it cannot be read
     pop_flag(argv, name)           (value, rest) for one `--flag value`
     Collection                     a directory of `<slug>.md` records under the board
+    prd_shape(dir)                 one PRD's (fm, title, body, specs, children, problems)
 
 Stdlib only, and it imports nothing from @resources/board/: memos.py stands
 on this file and @resources/board/plan.py imports memos.py, so a link back
@@ -162,7 +163,15 @@ ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
 
 
 def _clean(v):
-    return re.sub(r"\s+#.*$", "", v).strip().strip("\"'")
+    # `^` as well as `\s+`: a value that is ONLY a comment (`est:   # the
+    # weight, only when complexity is absent` — a key's line whose value is
+    # nothing but a trailing note) already had its leading spaces eaten by
+    # the caller's key/value split, so the comment sits at position 0 of
+    # `v` with nothing before it to match `\s+#`. Left unanchored at the
+    # start, that reads as a value rather than an absent one — measured
+    # against @resources/board/prdfile.py `strip_comment`, the reader this
+    # unifies with, which carried the fix first.
+    return re.sub(r"(^|\s+)#.*$", "", v).strip().strip("\"'")
 
 
 def split_frontmatter(text, lists=True):
@@ -221,6 +230,52 @@ def read_text(path, errors="replace"):
         return ""
 
 
+# ── one PRD's shape ──────────────────────────────────────────────────────────
+
+def prd_shape(dir_path):
+    """One PRD directory read whole: (fm, title, body, specs, children,
+    problems).
+
+    specs is `[(name, fm, title, body), ...]` for every `<name>.md` directly
+    under `specs/`, name order. children is the sorted basenames of every
+    immediate subdirectory that itself holds a `prd.md` — a parked or
+    container child, never a grandchild. problems is every way the shape
+    was short of whole, as one sentence each: `prd.md`'s fence did not
+    close, it closed with no `state:` key, or a spec's fence did not close.
+
+    This is the reading four modules did four ways before: facts and
+    problems only, nothing here decides a transition, a gate or a spec's
+    completeness — that is `plan.dispatchable`'s and `specs.check_spec`'s,
+    unmoved. The board scan's mtime cache sits in front of this, keyed on
+    the file it reads; this is what a cache miss calls."""
+    path = os.path.join(dir_path, "prd.md")
+    fm, title, body = parse_frontmatter(read_text(path))
+    problems = []
+    if fm is None:
+        problems.append(f"{path}: no closed `---` frontmatter fence")
+        fm = {}
+    elif not fm.get("state"):
+        problems.append(f"{path}: no `state:` key")
+
+    specs = []
+    sdir = os.path.join(dir_path, "specs")
+    for f in sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []:
+        if not f.endswith(".md"):
+            continue
+        spath = os.path.join(sdir, f)
+        sfm, stitle, sbody = parse_frontmatter(read_text(spath))
+        if sfm is None:
+            problems.append(f"{spath}: no closed `---` frontmatter fence")
+            sfm = {}
+        specs.append((f[:-3], sfm, stitle, sbody))
+
+    children = sorted(
+        n for n in (os.listdir(dir_path) if os.path.isdir(dir_path) else [])
+        if os.path.isfile(os.path.join(dir_path, n, "prd.md")))
+
+    return fm, title, body, specs, children, problems
+
+
 def atomic_write(path, text):
     """Written beside, then renamed over: a reader sees the old file or the
     new one, never a partial."""
```

## Acceptance

- [x] `common.prd_shape` is defined, callable, and returns `(fm, title, body,
      specs, children, problems)` for a directory holding `prd.md`.
- [x] On a fixture whose `prd.md` has no `state:` key and whose one spec has
      no closed fence, `problems` names both, and `children`/`specs` still
      resolve for the parts of the shape that were well-formed.
- [x] `common.split_frontmatter("---\nest:   # a note\n---\n")` reads `est`
      as `[]` (absent), not as the comment text.

## Verify and Proof

```sh
python3 - <<'PY'
import sys, os, tempfile
sys.path.insert(0, "resources")
import common

d = tempfile.mkdtemp()
os.makedirs(os.path.join(d, "specs"))
open(os.path.join(d, "prd.md"), "w").write("---\nno-state-key: true\n---\n\n# T\n\nbody\n")
open(os.path.join(d, "specs", "spec01.md"), "w").write("not a fence at all")
os.makedirs(os.path.join(d, "child"))
open(os.path.join(d, "child", "prd.md"), "w").write("---\nstate: open\n---\n# C\n")

fm, title, body, specs, children, problems = common.prd_shape(d)
assert title == "T"
assert children == ["child"]
assert specs and specs[0][0] == "spec01"
assert any("no `state:` key" in p for p in problems)
assert any("no closed" in p for p in problems)

fm2, _ = common.split_frontmatter("---\nest:   # the weight, only when complexity is absent\n---\n")
assert fm2.get("est") == []
print("spec01: ok")
PY
# Last and bare, on this spec's own footprint file: the reader is defined
# here, in `common.py`, and not somewhere the import happened to find it.
if ! grep -q '^def prd_shape' resources/common.py; then exit 1; fi
```
