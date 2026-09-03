---
complexity: 9
footprint:
  - resources/board/prdfile.py
---

# spec03 — prdfile delegates its parse to the one reader

`resources/board/prdfile.py` `_parse_prd_uncached` — the function `parse_prd`
sits on top of with the mtime cache, and the one every PRD scan in
`transitions.py`, `collect.py` and `plan.py` reaches through — stops
carrying its own `KEY_RE`/`ITEM_RE` frontmatter loop and reads the fence
through `resources/common.py` `split_frontmatter` (spec01) instead. What
stays here, layered on top of the shared read, is what is PRD/spec-specific
and belongs nowhere else: dropping an empty `key:` list nothing filled
(kept only for `needs:`, whose absence and whose empty list both mean
"nothing owed"), and reading the title off the body's first `# ` line with
a template's `<placeholder>` brackets cut off it.

`KEY_RE`, `ITEM_RE` and `strip_comment` stay as names in this file — aliased
to `common`'s — because `plan.py` re-exports all three (`noqa: F401`) and
`resources/board/specs.py` `fm_lines` calls `plan.KEY_RE` directly; removing
the names outright would break that caller.

One behaviour changes deliberately, per the PRD's own `## Done when`: a
`prd.md` whose fence opens with `---` but never closes previously had its
visible `key: value` lines parsed leniently into `fm` anyway, with the body
emptied. Read through `common.split_frontmatter` it now reads as a fully
malformed file — `fm = {}`, the whole text as body — the same "no closed
fence" fact `common.prd_shape`'s `problems` names and `guard.fm_state`
(spec02) already returns `None` for. This is the four-modules-agree
behaviour the PRD asks for, not a regression: scanning the real board
(`plan.py scan` against `.pearde`) is byte-identical before and after,
because no PRD on it is actually malformed this way.

This spec's work already stands, built and verified in a scratch clone of
this repo's HEAD: `plan.py scan` against the live `.pearde` board is
byte-for-byte unchanged, and every module that imports `plan`
(`transitions.py`, `collect.py`, `specs.py`) still imports cleanly. The diff
below is the whole of it.

```diff
--- a/resources/board/prdfile.py
+++ b/resources/board/prdfile.py
@@ -30,6 +30,7 @@ _D = os.path.dirname(os.path.abspath(__file__))
 sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                 else os.path.dirname(_D))
 import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
+import common  # noqa: E402 — @resources/common.py, the one frontmatter reader
 import memos as memolib  # noqa: E402 — on the path by the rule
 import questions as qlib  # noqa: E402 — the drill count, one reader with list
 import render as renderlib  # noqa: E402 — on the path by the rule
@@ -37,21 +38,17 @@ import workflows as wflib  # noqa: E402 — on the path by the rule
 from boards import (PASS_FILE, state_dir)  # noqa: E402,F401
 
 
-
-# Frontmatter: match a key by name at any indentation, anywhere in the block.
-# Scalars and simple `- item` lists. Names are unique within one file.
-KEY_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")
-ITEM_RE = re.compile(r"^\s*-\s+(.*?)\s*$")
-
-
-def strip_comment(v):
-    # `^` as well as `\s+`: a value that is ONLY a comment is an empty value.
-    # `est:   # the weight, only when complexity is absent` — the template's
-    # own line — parsed to the comment TEXT while the leading run of spaces was
-    # eaten by KEY_RE, so every reader of `est` got a sentence where a duration
-    # was meant. `hours()` read it as 0.0 in silence; `dur()` reports it, which
-    # is how it was found. A `#` inside a word (`repo: a#b`) is still a `#`.
-    return re.sub(r"(^|\s+)#.*$", "", v).strip().strip("\"'")
+# Kept as names: `plan.py` re-exports `strip_comment`, `KEY_RE` and
+# `ITEM_RE` (noqa F401), and `resources/board/specs.py` `fm_lines` matches
+# `plan.KEY_RE` directly. All three are @resources/common.py's now — one
+# frontmatter regex and one comment fix, not a second copy of either.
+# `est:   # the weight, only when complexity is absent` — the template's own
+# line — is why the comment fix exists: the value is nothing but a trailing
+# note, not a sentence, and `hours()` must read it as absent, not as 0.0 in
+# silence.
+strip_comment = common._clean
+KEY_RE = common.KEY_RE
+ITEM_RE = common.ITEM_RE
 
 
 # ── the parse cache ──────────────────────────────────────────────────────────
@@ -140,36 +137,24 @@ def parse_prd(path):
 
 
 def _parse_prd_uncached(path):
+    """(fm, title, body) — the frontmatter read through
+    @resources/common.py `split_frontmatter`, the one reader every board
+    module now shares; what stays here is what a PRD/spec file means beyond
+    that: an empty `key:` block that no `- item` ever filled reads as
+    absent (kept only for `needs`, whose absence and whose empty list are
+    both "nothing owed"), and the title is the body's first `# ` line with
+    a template's `<placeholder>` angle brackets cut off it."""
     text = open(path, encoding="utf-8").read()
-    lines = text.splitlines()
-    fm, body_start = {}, 0
-    if lines and lines[0].strip() == "---":
-        i, cur_list = 1, None
-        while i < len(lines) and lines[i].strip() != "---":
-            line = lines[i]
-            m = KEY_RE.match(line)
-            item = ITEM_RE.match(line)
-            if m:
-                key, val = m.group(1), strip_comment(m.group(2))
-                if val:
-                    fm[key] = val
-                    cur_list = None
-                else:
-                    fm[key] = []
-                    cur_list = key
-            elif item and cur_list is not None:
-                v = strip_comment(item.group(1))
-                if v:
-                    fm[cur_list].append(v)
-            i += 1
-        body_start = i + 1
-    body = "\n".join(lines[body_start:]).strip()
+    fm, body_start = common.split_frontmatter(text)
+    if fm is None:
+        fm, body_start = {}, 0
+    fm = {k: v for k, v in fm.items() if v != [] or k == "needs"}
+    body = "\n".join(text.splitlines()[body_start:]).strip()
     title = None
     for line in body.splitlines():
         if line.startswith("# "):
             title = line[2:].strip().strip("<>").strip()
             break
-    fm = {k: v for k, v in fm.items() if v != [] or k == "needs"}
     return fm, title, body
```

## Acceptance

- [ ] `resources/board/prdfile.py` defines no `KEY_RE`/`ITEM_RE` regex of
      its own — both are `common.KEY_RE`/`common.ITEM_RE` by alias.
- [ ] `plan.py`, `transitions.py`, `collect.py` and `specs.py` all import
      cleanly, and `plan.KEY_RE` (`specs.py` `fm_lines`'s dependency) still
      resolves.
- [ ] `python3 resources/board/plan.py scan .pearde` against this repo's own
      live board prints byte-identical output before and after the change.
- [ ] A `prd.md` whose fence opens and never closes now parses to
      `fm == {}` and the whole file as `body` — the same "no closed fence"
      fact `common.prd_shape` and `guard.fm_state` (spec02) already report,
      not the old lenient partial parse.

## Verify and Proof

```sh
python3 -c "
import sys; sys.path.insert(0, 'resources'); sys.path.insert(0, 'resources/board')
import plan as planlib, specs, transitions, collect  # noqa: F401
print('imports ok, plan.KEY_RE =', planlib.KEY_RE)
"
python3 resources/board/plan.py scan .pearde | tail -3
# compared against a scan taken before this spec's edit landed — the pass
# writing this box quotes both counts side by side, not just this one run.
python3 - <<'PY'
import sys, tempfile, os
sys.path.insert(0, "resources"); sys.path.insert(0, "resources/board")
import plan as planlib
d = tempfile.mkdtemp(); p = os.path.join(d, "prd.md")
open(p, "w").write("---\nstate: open\nno closing fence\n# T\nbody\n")
fm, title, body = planlib._parse_prd_uncached(p)
assert fm == {}, fm
print("spec03: ok")
PY
```
