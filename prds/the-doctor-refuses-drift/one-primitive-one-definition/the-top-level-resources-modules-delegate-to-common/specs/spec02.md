---
complexity: 8
footprint:
  - resources/questions.py
---

# spec02 — `questions.py`'s board walk and section reader are one-line calls into `common.py`

`resources/questions.py` held two duplicates: `find_board`/`board_in`/
`board_above`/`board_scanned`, thin wrappers around `plan.find_board`'s own
helpers with only the `questions:` refusal prefix as this file's own
contribution — the same job `common.find_board(arg, prog)` already does
end to end; and `sections(body, pattern)`, its own `## <name>` line scanner
taking a compiled, `re.M`-anchored pattern (`Q_RE`, `A_RE`) and returning
the raw heading line paired with the body up to the next `## `.

## What already stands

```python
def find_board(arg):
    return common.find_board(arg, "questions")


def sections(body, name):
    """Every `## <name>` section — matched as a prefix with a word boundary,
    so `## Questions (pass 1, answered)` still matches `name="Questions"` —
    up to the next `##`: (heading text, its body)."""
    return common.section(body, name, all=True, prefix=True, word=True,
                            heading=True, ci=False)
```

`import common` is added; `import plan as planlib` stays — `parse()` still
reads `planlib.parse_prd` for the cached PRD read, outside either
primitive. Nothing else in the file called `board_in`, `board_above` or
`board_scanned`, so removing them drops no other caller; every call site
that passed `Q_RE`/`A_RE` now passes the string `"Questions"`/`"Answers"`,
and both compiled patterns (and `H2_RE`, `sections`'s own next-boundary
regex) are removed as unused.

Two differences between the old `sections` and `common.section`'s
`heading=True` shape, neither read past a substring or truthy check:
`common.section`'s heading text is the name only (`"Questions"`), not the
raw `"## Questions"` line the old reader returned — the two format
strings that interpolated `head` assuming the `## ` prefix (`` `{head}`
with nothing under it`` at both the questions- and answers-branch, and
`` `{head}` with no `## Questions` above it``) now spell it explicitly
(`` `## {head}` ``), so the printed message is unchanged; and the returned
body carries one fewer leading blank line when the heading is followed by
one (the same `_H2_RE` greedy-`\s*$` behaviour spec03 documents for
`workflows.py`), which no caller here reads past `.strip()` or a
`re.search`/`re.finditer` scan.

`probe/verify.py` runs both readers over every `## Questions`/`## Answers`
section in every live `prd.md` (222 files) and finds no divergence once
the raw prefix and leading-blank-line differences are normalised out of
both sides for the comparison — the check is honest about what it ignores
rather than silent about it.

## What is left

Nothing in this file.

## Acceptance

- [x] `questions.py` defines no `board_scanned`/`board_in`/`board_above`
  or line-scanning `## <name>` reader of its own; `find_board` and
  `sections` are the one-line delegations above.
- [x] `find_board` resolves the same board, from the board itself, from
  `None` (walking up from the cwd), and refuses the same way (`questions: `
  prefix, exit 1) on a path with no board, as it did before the edit.
- [x] `python3 resources/questions.py check <board>` and `... list <board>`
  print byte-identical output to the pre-edit implementation, verified
  against a copy of `resources/` with only `questions.py` reverted to the
  commit this lane started from.

## Verify and Proof

```sh
python3 -m py_compile resources/questions.py
# `check` exits 1 on the board's own three pre-existing question-pass
# problems, which this unit neither made nor fixes — capture its status
# so the block reads the output rather than dying on it.
out=$(python3 resources/questions.py check .pearde 2>&1) || true
printf '%s\n' "$out" | tail -3
python3 resources/questions.py list .pearde | wc -l
python3 .pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/the-top-level-resources-modules-delegate-to-common/probe/verify.py
```
