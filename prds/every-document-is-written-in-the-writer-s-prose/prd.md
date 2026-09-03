---
state: done
origin: requested
priority: 55
complexity: 0
blast-radius:
actual: 48.21h
commit: 7a162c2
---

# every document is written in the writer's prose

When this is done, every tracked `.md` file in this repo is written in the
`writer` persona's prose — @references/personas/writer.md, Vera Lindqvist —
and @references/language.md states the rules a rewrite is checked against, so
the standard is a file and not a memory.

The tree is 117 tracked `.md` files, ~89k words at the time of writing. The
target is the same facts in materially fewer words: every rule, command,
state, key, path, table row and refusal text survives verbatim. This is a
rewrite of prose, never of contract.

## The rules the rewrite applies

@references/language.md already carries the shape rules — structure over
prose, one idea per sentence, imperative, no hedging, no meta, no legacy. This
PRD adds the density rules under them, from the persona:

| rule | test |
|---|---|
| Lead with the answer | the first line of a file or section is the finding, command or state — never the approach to it |
| Every heading summarises what is beneath it | headings alone read as the argument |
| Cut twice | half the words, then half of what is left, with no fact lost |
| A fact set is a table, a sequence a numbered list | a paragraph survives only where the content is an argument |
| About twenty words a sentence, on average | measured per file |
| No unbound `it`, `this`, `that`, `there` | each is deleted or names its noun |
| Reference describes, never teaches | instruction and explanation become a link |
| No preamble, no recap, no closer | the file opens on content and ends when the content ends |
| Emphasis earns its place | bold and italic only where a reader needed it, never both |

## What must not change

- Every `@<path>` and `@@<keyword>` still resolves — `resources/index.py check`
  is silent afterwards.
- Every command line, flag list, refusal string, frontmatter key, state name
  and settings key is character-identical. A rewrite that changes a refusal
  string changes behaviour.
- Every table row survives as a row. Cutting words never means cutting a fact.
- The README's exemption in @references/language.md — a human reader, a
  sentence may carry two ideas — stays, and the README is rewritten under it.
- No file is renamed, moved, split or merged. The rewrite is content only.
- @references/personas/*.md and @references/templates/*.md keep their
  prescribed shapes; their bodies are rewritten, their formats are not.

## Files

| file | change |
|---|---|
| `references/language.md` | a `## Density` section holding the nine rules above, and the persona named as their source |
| every other tracked `.md` | rewritten against those rules |
| `resources/prose.py` | the checker — word count per file, mean sentence length, unbound waste words, banned openers and closers; `check` exits 1 on a violation |
| `references/files.md` | the `resources/prose.py` row |
| `index.md` | `@@language`'s scope gains the checker |

## Verify

- `python3 resources/prose.py check` exits 0 across the tree, and exits 1 on a
  file with a planted preamble.
- `python3 resources/prose.py stat` prints before/after word counts; the tree
  total is at least 30% below the 88,734 words it starts at.
- `python3 resources/index.py check` silent.
- `python3 resources/pearde.py doctor` no worse than before the rewrite.
- `git diff --stat` shows no file renamed and none deleted.
- Spot check, named in the report: three files where a fact was at risk —
  @references/parts/handles.md, @references/parts/states.md,
  @references/settings.md — every row, key and command present after.

## Children

| child | contract | needs |
|---|---|---|
| `a-density-checker-and-the-root-docs-are-rewritten` | resources/prose.py` checks word count, mean sentence length, unbound waste words and banned openers/closers per file; `references/language.md` carries the `## Density` section; `references/files.md`, `index.md`, `README.md` and `SKILL.md` are rewritten dense | — |
| `the-parts-reference-is-rewritten-dense` | every file under `references/parts/` (28 files, 34,815 words) rewritten dense, every fact intact | a-density-checker-and-the-root-docs-are-rewritten |
| `the-loose-reference-files-are-rewritten-dense` | every loose file under `references/` except `language.md` and `files.md` (15 files, 16,857 words) rewritten dense | a-density-checker-and-the-root-docs-are-rewritten |
| `templates-personas-and-agents-are-rewritten-dense` | references/templates/`, `references/personas/` and `references/agents/` rewritten dense, prescribed shapes kept | a-density-checker-and-the-root-docs-are-rewritten |
| `skills-and-scout-docs-are-rewritten-dense` | references/skills/` and `resources/scout/` docs rewritten dense (includes the one file over the sentence-length target) | a-density-checker-and-the-root-docs-are-rewritten |
| `example-and-knowledge-fixtures-are-rewritten-dense` | resources/board/example/**` and `resources/board/knowledge/**` rewritten dense, checked against any harness reading them verbatim | a-density-checker-and-the-root-docs-are-rewritten |

## Report

container: every child done — pearde collect closes it

children: every-document-is-written-in-the-writer-s-prose/the-loose-reference-files-are-rewritten-dense, every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense, every-document-is-written-in-the-writer-s-prose/the-standard-is-held-to-its-own-standard, every-document-is-written-in-the-writer-s-prose/templates-personas-and-agents-are-rewritten-dense, every-document-is-written-in-the-writer-s-prose/a-density-checker-and-the-root-docs-are-rewritten, every-document-is-written-in-the-writer-s-prose/the-parts-reference-is-rewritten-dense, every-document-is-written-in-the-writer-s-prose/example-and-knowledge-fixtures-are-rewritten-dense
