---
complexity: 5
footprint:
  - resources/guard.py
---

# spec02 — guard reads state through the one reader

`resources/guard.py`'s `fm_state` — the only place the top-level guard hook
reads a PRD's frontmatter at all — stops carrying its own `STATE_RE` and
reads a proposed `prd.md`'s `state:` value through
`resources/common.py` `split_frontmatter` instead, the same call
`resources/board/prdfile.py` (spec03) now sits on. Depends on spec01
(`common.prd_shape`'s module, and `common._clean`'s fix, must exist first);
otherwise independent of spec03.

`common.py` is stdlib-only and lives beside `guard.py` in `resources/`, the
same tier of trust `pearde_path.py` already has there (guard.py imports it
unconditionally, no `try/except`) — the guard's own rule against depending
on shared code is stated as "the guard imports nothing from **the
planner**" (`resources/board/plan.py` and the module web behind it), not
against `common.py`, which is guard's sibling and carries no board-specific
deciding.

This spec's work already stands, built and verified in a scratch clone of
this repo's HEAD, and re-run against the harness this repo already commits
for the guard (`.pearde/prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh`)
with an identical pass/fail count to an unmodified clone. The diff below is
the whole of it.

```diff
--- a/resources/guard.py
+++ b/resources/guard.py
@@ -36,6 +36,7 @@ _D = os.path.dirname(os.path.abspath(__file__))
 sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                 else os.path.dirname(_D))
 import pearde_path  # noqa: E402 — @resources/pearde_path.py, the one rule
+import common  # noqa: E402 — @resources/common.py, the shared reader; stdlib-only, same tier as pearde_path
 try:
     import quiet  # noqa: E402 — @resources/board/quiet.py, stdlib-only; a broken module denies nothing
 except Exception:
@@ -106,7 +107,6 @@ SCAN = "python3 %s scan" % (pearde_path.script("plan.py") or "plan.py")
 # `resources/<dir>/<mod>.py` matches wherever a module lands: the directory
 # is a wildcard, so a file that moves stays recognised as one of ours.
 TOOLS = re.compile(r"\b(pearde|plan|guard)\.py\b|resources/\w+/\w+\.py")
-STATE_RE = re.compile(r"^state:[ \t]*(.*?)[ \t]*$", re.M)
 
 # A board walked by hand. `find … prd.md`, `grep -r state:`, `ls prds/*/prd.md`
 # — every spelling of the sweep step 1 stopped asking for.
@@ -514,12 +514,12 @@ def another_boards_write(inp, cwd):
 
 
 def fm_state(text):
-    """The `state:` value of a frontmatter block, or None."""
-    if not text.startswith("---"):
-        return None
-    end = text.find("\n---", 3)
-    m = STATE_RE.search(text[3:end] if end > 0 else "")
-    return m.group(1) if m else None
+    """The `state:` value of a frontmatter block, or None — read through
+    @resources/common.py `split_frontmatter`, the one reader every board
+    module now parses a `prd.md` through, so a malformed file reads the
+    same way here as it does to transitions, collect and plan."""
+    fm, _ = common.split_frontmatter(text)
+    return (fm or {}).get("state") or None
 
 
 def after_edit(path, tool, inp):
```

## Acceptance

- [ ] `resources/guard.py` defines no `STATE_RE` and no other frontmatter
      regex of its own — a `grep -E '^(KEY_RE|ITEM_RE|STATE_RE)\s*=\s*re\.compile'`
      over the file finds nothing.
- [ ] `guard.fm_state` returns the same value as before on every case the
      committed `the-skill-tree-is-guarded` harness exercises — that
      harness's pass/fail count on this file matches an unmodified clone,
      run with `PEARDE_ROOT` pointed at each in turn.
- [ ] `guard.fm_state` and `plan.parse_prd` agree that a `prd.md` with no
      `state:` key has no state — one fact, read through one primitive by
      both paths.

## Verify and Proof

```sh
python3 - <<'PY'
import sys
sys.path.insert(0, "resources")
import guard
assert guard.fm_state("---\nstate: open\n---\nbody") == "open"
assert guard.fm_state("---\nstate: open  # note\n---\nbody") == "open"
assert guard.fm_state("no fence") is None
assert guard.fm_state("---\nno-state: x\n---\n") is None
print("spec02: ok")
PY
bash .pearde/prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh
```
