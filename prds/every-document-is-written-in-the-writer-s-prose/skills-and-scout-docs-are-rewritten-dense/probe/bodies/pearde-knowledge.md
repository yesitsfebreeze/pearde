
Read @references/knowledge.md. The scope is `@@knowledge`. The tool is
`python3 @resources/knowledge.py <verb>` — every verb takes `--root`, the
default root is `.pearde/wiki/`, and the folder is its own Obsidian vault.

- `query` first. A question the KB answers costs nothing; one it does not
  prints `gap:` and goes to `enqueue` or a research pass.
- Write with `remember` and `conclude`, never by hand — the verbs carry the
  frontmatter the graph and the dashboard read; `conclude` refuses a lone
  source, per `min_sources_per_conclusion`.
- `relink` after writing, and `wiki` when the graph grew a community;
  `doctor` before calling a KB fact settled.
- Scout sweeps distill here; memo bodies wikilink in.
