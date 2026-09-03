---
complexity: 8
footprint:
  - resources/workflows.py
---

# spec03 — `workflows.py`'s board walk and section reader are one-line calls into `common.py`

`resources/workflows.py` held two duplicates: `find_board`, a `try`/`except`
around `memos.find_board` that rewrote the `memos:` prefix on the failure
to `workflows:` — indirection through `memos.py` rather than the shared
file this PRD points callers at directly — and `section(body, name)`, its
own line-scanning `## <name>` reader, matched case-sensitively.

## What already stands

```python
def find_board(arg):
    """@resources/common.py resolves the board; only the prefix on the
    failure is ours, so the error names the command that was run."""
    return common.find_board(arg, "workflows")


def section(body, name):
    """The lines under `## <name>`, up to the next `##`. None when absent."""
    return common.section(body, name, lines=True, ci=False)
```

`common.section(..., lines=True, ci=False)` matches the old function's
case-sensitive, whole-line heading match and its "stop at the next `## `"
body, but its own `## ` regex ends the match with a greedy `\s*$` that
swallows one more newline than a plain line scan would when a blank line
follows the heading — so a body that used to come back with one leading
(and sometimes trailing) empty line now comes back without it. `brief`
already trims blank lines off both ends of `section(..., "Use when")`
before printing it (`while body and not body[0].strip(): body.pop(0)`, and
the same at the end) for exactly this reason on the old shape, so the
trim is now a no-op rather than the thing doing the work — the printed
page is unchanged either way. `check()`'s `if not section(body, s):`
existence test and `steps()`'s table-row scan (which already skips a blank
line — `_cells("")` matches nothing) are unaffected by the count or
position of blank lines in the list.

`import common` is added; `import memos` and `from memos import ISO_RE,
parse` stay — `parse` still reads every workflow file's frontmatter and
`ISO_RE` still validates `date:`/`updated:`, outside this primitive.

## What is left

Nothing in this file.

## Acceptance

- [x] `workflows.py` defines no line-scanning `## <name>` reader or
  `memos.find_board` wrapper of its own; both are the one-line delegations
  above.
- [x] `workflows.py check <board>` reports the same library state as
  before the edit (`7 workflows · 23 atomics · the library checks out`).
- [x] For every workflow and atomic in the live library, `section(body,
  name)` for `Do`, `Done when`, `Use when` and `Steps` is truthy exactly
  when it was truthy before the edit (120 checks across 30 files).
- [x] `workflows.py brief probe-then-spec <board>` prints the same page as
  before the edit.

## Verify and Proof

```sh
python3 -m py_compile resources/workflows.py
python3 resources/workflows.py check .pearde
python3 resources/workflows.py brief probe-then-spec .pearde
python3 .pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/the-top-level-resources-modules-delegate-to-common/probe/verify.py
```
