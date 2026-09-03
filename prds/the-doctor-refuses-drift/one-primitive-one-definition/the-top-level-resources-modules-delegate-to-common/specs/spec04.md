---
complexity: 12
footprint:
  - resources/knowledge.py
---

# spec04 — `knowledge.py`'s frontmatter reader delegates its fence-and-key parsing to `common.split_frontmatter`, keeping only its own wiki-only extensions

`resources/knowledge.py` held a full second `parse_frontmatter`: its own
`---` fence match, its own `key:`/`  - item` line scanner, its own quote
stripping — plus two behaviours `common.py`'s dialect does not have: an
inline `key: [a, b]` shorthand for a one-line list, and treating a
malformed indented dash under a key that already got a scalar as "skip the
line" rather than silently turning the scalar into a list.

## What already stands

```python
def parse_frontmatter(text):
    fm, start = common.split_frontmatter(text, lists=True)
    if fm is None:
        return {}, text
    for key, value in list(fm.items()):
        if (isinstance(value, str) and value.startswith("[")
                and not value.startswith("[[") and value.endswith("]")):
            inner = value[1:-1]
            fm[key] = ([v.strip().strip('"') for v in inner.split(",") if v.strip()]
                       if inner.strip() else [])
    return fm, "\n".join(text.splitlines()[start:])
```

The fence, the `key:` and multi-line `- item` parsing and the quote
stripping now run once, in `common.split_frontmatter`. What is left of
knowledge.py's own dialect is the loop above: any value `common.py` read
as the literal string `[a, b]` is re-read as a list, the way a hand-typed
`tags: [memo, kind/decision]` line reads in the wiki today. A doubled
bracket (`[[a wikilink]]`, quoted or not — `common.py`'s own quote-
stripping already ran) is left a string on purpose: 109 of the corpus's
587 notes hold a `from:` or `workflow:` field shaped exactly that way, one
wikilink standing for one cross-reference, never a list of one.

The one case this drops from the old reader's own behaviour: a value
`common.split_frontmatter` reads as a fresh top-level key because its
`KEY_RE` allows leading whitespace, where the old reader's column-0-
anchored `pair` regex silently discarded the same indented line as
neither a list item nor a key. `probe/verify.py` runs both readers over
every note under `.pearde/wiki/` (a frozen copy of the pre-delegation
function is inlined there for the comparison) and finds exactly one file
where this fires: `wiki/graphs/community-01-260831-2cdf.md`, a generated
graph note with `community:` opened as an empty list and `hub:`/`size:`
indented under it as a nested mapping neither reader treats as YAML — the
new reader reads the two as extra top-level keys instead of dropping them,
strictly more read, nothing lost. No other file in the corpus diverges.

The now-unused `FM_RE` is removed; `WIKILINK_RE` (a different job — link
extraction inside a note's body, not its frontmatter) stays.

## What is left

If a future note relies on the quote-escapes-brackets precedence for a
value that is not itself a wikilink (a hand-typed `"[a, b]"` meant to stay
a string) — no note in the current corpus does — that value now reads as
a list; nobody has asked for that escape hatch since it was never
observed in use, so this spec does not build it.

## Acceptance

- [x] `knowledge.py` defines no fence/key/list line-scanner of its own;
  `parse_frontmatter` delegates the fence-and-key parsing to
  `common.split_frontmatter` and keeps only the bracket-list re-read above.
- [x] Every note under `.pearde/wiki/` (587 files) parses to the same
  `(meta, body)` as the pre-delegation reader, except the one named,
  generated-note case, which reads strictly more keys, never fewer or
  wrong ones.
- [x] `python3 resources/knowledge.py query "<anything>"` and `doctor.sh`'s
  `knowledge` row behave the same as before the edit (the row's own
  `graph.json is behind the files` finding is pre-existing and unrelated).

## Verify and Proof

```sh
python3 -m py_compile resources/knowledge.py
python3 .pearde/prds/the-doctor-refuses-drift/one-primitive-one-definition/the-top-level-resources-modules-delegate-to-common/probe/verify.py
python3 resources/knowledge.py query "one primitive one definition" .pearde | head -3
```
