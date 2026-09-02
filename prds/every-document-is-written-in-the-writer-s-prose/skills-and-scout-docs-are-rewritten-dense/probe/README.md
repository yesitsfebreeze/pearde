# probe — skills-and-scout-docs-are-rewritten-dense

| file | what it holds |
|---|---|
| `skills/` | the 19 finished `references/skills/*.md`, whole files |
| `scout/` | the 4 finished `resources/scout/*.md` |
| `bodies/` | pass one's mid-pass body snapshot — superseded by `skills/`, kept as the record |
| `frontmatter/pearde-scout-split.md` | pass two's proof that the longest description splits under 24 words a sentence |
| `restore.sh` | copy `skills/` and `scout/` back into a reset lane |
| `verify.sh` | every acceptance box, run on the merged tree; `REF=main` is the negative control |
| `hits.py` | each unbound-waste hit with its surrounding words |
| `split.py` | per file, unbound hits in the whole file against the body alone |
| `shape.py` | words per shape — frontmatter, prose, table, list, heading |
| `splice.py` | pass two's body-only splice; `restore.sh` replaces it |

`bash verify.sh` on the merged tree: `boxes 14/14`, exit 0. `REF=main bash
verify.sh` scores 9/14, and a mutation reddens each of the other five, so no
box here is a check that cannot fail.

The implementer pass fast-forwarded the lane's base from `3664de0` to `main`
and re-applied the rewrite with `git apply --3way`, which put `main`'s later
`findings.md` section inside the lane where its one unbound `it` could be
rewritten. `skills/` and `scout/` hold the files as they stand after that, so
`restore.sh` restores the rebased text, never the pre-rebase text.
