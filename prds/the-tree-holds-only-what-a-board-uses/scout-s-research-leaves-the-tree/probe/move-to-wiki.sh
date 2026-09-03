#!/usr/bin/env bash
# The spec02 move, run against a scratch copy of the board's wiki so nothing
# in the live board is touched. Proves: the two research indexes are accepted
# as source notes once they carry frontmatter, the configs and TSVs ride along
# unscanned under attachments/, the four citations resolve as wikilinks, and
# knowledge.py doctor goes clean afterwards.
#
#     bash probe/move-to-wiki.sh <lane-or-repo-root>
#
# Reads the departing files out of git history, so it runs before or after the
# deletions land.
set -euo pipefail
REPO="${1:?usage: move-to-wiki.sh <repo-root>}"
REF="${2:-HEAD}"
T=$(mktemp -d /tmp/scoutmove.XXXXXX)
cp -R "$REPO/.pearde/wiki" "$T/wiki" 2>/dev/null || cp -R /Users/feb/dev/infra/pearde/.pearde/wiki "$T/wiki"
W="$T/wiki"
mkdir -p "$W/sources/scout/attachments"
cd "$REPO"
{ printf -- '---\ntitle: scout-findings-index-2026-08\ndate: 2026-08-31\ntype: source\ntags: [source, scout, findings, archive]\nrelated:\n  - "[[260831-3e48]]"\n  - "[[260831-cbe9]]"\n---\n\n'
  git show "$REF:resources/scout/findings.md"; } > "$W/sources/scout/scout-findings-index-2026-08.md"
{ printf -- '---\ntitle: scout-reading-list-2026-08\ndate: 2026-08-31\ntype: source\ntags: [source, scout, reading-list, archive]\nrelated:\n  - "[[260831-2cdf]]"\n---\n\n'
  git show "$REF:resources/scout/reading-list.md"; } > "$W/sources/scout/scout-reading-list-2026-08.md"
for f in _typos.toml deny.toml dependabot.yml quality.yml scout.yml; do
  git show "$REF:resources/scout/templates/$f" > "$W/sources/scout/attachments/$f"
done
for f in 2026-08-25.tsv 2026-08-28.tsv; do
  git show "$REF:resources/scout/snapshots/$f" > "$W/sources/scout/attachments/$f"
done
python3 - "$W" <<'PY'
import pathlib, sys
W = pathlib.Path(sys.argv[1])
subs = [
 ("sources/scout/260831-2cdf.md",
  "Full table with per-tree mappings lives in `resources/scout/reading-list.md` — never copied here; the distilled takeaway is this note, the list is the citation.",
  "Full table with per-tree mappings is [[scout-reading-list-2026-08]] — the distilled takeaway is this note, the list is the citation."),
 ("sources/scout/260831-3e48.md",
  "Source: `resources/scout/findings.md` —",
  "Source: [[scout-findings-index-2026-08]] —"),
 ("sources/scout/260831-cbe9.md",
  "Source: `resources/scout/findings.md` rows",
  "Source: [[scout-findings-index-2026-08]] rows"),
 ("conclusions/scout/scout-feeds-knowledge-knowledge-feeds-the-rou.md",
  "2. **Scout's own indexes second** (`findings.md` for decided jobs, `reading-list.md` for mechanisms to steal): for a job the KB has not absorbed yet.",
  "2. **The archived indexes second** ([[scout-findings-index-2026-08]] for decided jobs, [[scout-reading-list-2026-08]] for mechanisms to steal): a job the KB has not absorbed yet."),
 ("conclusions/scout/scout-feeds-knowledge-knowledge-feeds-the-rou.md",
  "or a finding left only inside `findings.md` where no wikilink can reach it.",
  "or a finding left in the tool's own tree where no wikilink can reach it."),
]
for rel, old, new in subs:
    p = W / rel; t = p.read_text()
    assert old in t, f"anchor gone: {rel}"
    p.write_text(t.replace(old, new))
print("citations rewritten")
PY
python3 "$REPO/resources/knowledge.py" --root "$W" relink > /dev/null
python3 "$REPO/resources/knowledge.py" --root "$W" doctor
python3 "$REPO/resources/knowledge.py" --root "$W" query \
  "which tool won recursive search over a source tree" | grep -q 'scout-findings-index-2026-08' \
  && echo "query reaches the moved research"
echo "scratch wiki: $W"
