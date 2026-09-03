---
complexity: 4
footprint:
  - resources/health.py
---

# spec01 — `health.py`'s git runner is a one-line call into `common.run_git`

`resources/health.py` already delegated `find_board`, its frontmatter
reader and its atomic write to `resources/common.py` before this PRD
started; the one primitive it still defined a second time was `_git`, a
`subprocess.run(["git", "-C", root] + args, ...)` wrapper returning stdout
on a zero exit and `None` on any failure (a bad path, git missing, or a
timeout).

## What already stands

`_git` is now:

```python
def _git(root, *args):
    return common.run_git(root, *args, timeout=30, check=True, default=None,
                            stdout=True)
```

`check=True` makes a non-zero exit a failure alongside the process-level
ones `run_git` always treats as failure; `default=None` returns `None` on
any of them, matching `_git`'s old catch-all; `stdout=True` returns the
raw (unstripped) stdout on success, matching the old `r.stdout`. The now-
unused `import subprocess` is removed — nothing else in the file calls it.

## What is left

Nothing in this file.

## Acceptance

- [x] `health.py` defines no `subprocess.run` of its own; `_git` is the
  one-line delegation above.
- [x] `health.head_commit` and `health.commits_behind` return the same
  values as before the edit, on a real repo, a bad commit id, and the
  literal string `"none"`.
- [x] `python3 resources/health.py score <board>` runs to completion.

## Verify and Proof

```sh
python3 -m py_compile resources/health.py
python3 -c "
import sys; sys.path.insert(0, 'resources')
import health
print(health.head_commit('.'))
print(health.commits_behind('.', 'none'))
print(health.commits_behind('.', 'not-a-commit'))
"
python3 .pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/the-top-level-resources-modules-delegate-to-common/probe/verify.py
```
