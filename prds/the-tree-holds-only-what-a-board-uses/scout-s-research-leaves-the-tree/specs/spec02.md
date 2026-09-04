---
complexity: 8
footprint:
  - .pearde/wiki/sources/scout
  - .pearde/wiki/conclusions/scout
---

# spec02 — the research lands in the board's wiki, never deleted

The 1,847 lines spec01 takes out of the tree arrive in the board's wiki, which
the PRD names as one of the two destinations and which is the one a build can
reach: `.pearde/` is its own git repository on the `pearde` branch of the same
origin, so a file written here is version-controlled, not dropped. The two
research indexes become source notes; the five quality-gate configs and the two
dated snapshots ride along as attachments beside them. The four wiki notes that
cited the old paths cite the new ones, so `knowledge.py query` still reaches the
research after the move.

**Already standing.** Nothing in the board; the move was proved in a scratch
copy of the wiki only. The lane holds the code-repo half.

**Left to finish.** Every box below. The frontmatter is what makes this work:
a raw `.md` dropped into `sources/` with no frontmatter reddens
`knowledge.py doctor` with `no frontmatter` — measured. Non-markdown files in
a subdirectory are not scanned, which is why the configs and the TSVs go to
`attachments/`. Recover each file's content from git history, `git show
HEAD:resources/scout/<path>` against the code repo before spec01's deletion
lands, or from the deletion commit afterwards.

Write the notes as:

- `sources/scout/scout-findings-index-2026-08.md` — `findings.md` under
  frontmatter `title`, `date: 2026-08-31`, `type: source`, `tags` including
  `scout` and `archive`, and `related` naming `260831-3e48` and `260831-cbe9`
- `sources/scout/scout-reading-list-2026-08.md` — `reading-list.md` under the
  same shape, `related` naming `260831-2cdf`
- `sources/scout/attachments/` — `_typos.toml`, `deny.toml`, `dependabot.yml`,
  `quality.yml`, `scout.yml`, `2026-08-25.tsv`, `2026-08-28.tsv`
- one line in each new note naming `attachments/` as where its configs went, so
  nothing in the wiki is reachable only by listing a directory

Then rewrite the four citations that name the departed paths:
`sources/scout/260831-2cdf.md` (reading list), `sources/scout/260831-3e48.md`
and `sources/scout/260831-cbe9.md` (findings), and
`conclusions/scout/scout-feeds-knowledge-knowledge-feeds-the-rou.md`, whose
step 2 and closing sentence both name the two files. Each becomes a wikilink to
the new note. Finish with `knowledge.py relink` so the graph matches.

## Acceptance

- [x] `.pearde/wiki/sources/scout/` holds both new notes, each opening with a `---` frontmatter fence carrying `type: source`
- [x] `.pearde/wiki/sources/scout/attachments/` holds all seven files, byte-identical to their content in git history
- [x] No file under `.pearde/wiki/` contains the string `resources/scout/findings.md` or `resources/scout/reading-list.md`
- [x] Both new notes are named by a wikilink from at least one older note
- [x] `python3 resources/knowledge.py --root .pearde/wiki doctor` prints `doctor: clean` after a `relink`, with no `no frontmatter` line and no note left out of the graph
- [x] `python3 resources/knowledge.py --root .pearde/wiki query "which tool won recursive search over a source tree"` returns `scout-findings-index-2026-08` among its hits
- [x] `git -C .pearde status --short` shows the new files and `git status --short` in the code repo shows none of them — the board repo commits its own

## Verify and Proof

```sh
set -e
test -f .pearde/wiki/sources/scout/scout-findings-index-2026-08.md
test -f .pearde/wiki/sources/scout/scout-reading-list-2026-08.md
head -1 .pearde/wiki/sources/scout/scout-findings-index-2026-08.md | grep -qx -- '---'
head -1 .pearde/wiki/sources/scout/scout-reading-list-2026-08.md | grep -qx -- '---'
grep -qx 'type: source' .pearde/wiki/sources/scout/scout-findings-index-2026-08.md
grep -qx 'type: source' .pearde/wiki/sources/scout/scout-reading-list-2026-08.md
n=0
for f in _typos.toml deny.toml dependabot.yml quality.yml scout.yml 2026-08-25.tsv 2026-08-28.tsv; do
  test -s ".pearde/wiki/sources/scout/attachments/$f"
  git show HEAD:"resources/scout/templates/$f" 2>/dev/null | cmp -s - ".pearde/wiki/sources/scout/attachments/$f" \
    || git show HEAD:"resources/scout/snapshots/$f" 2>/dev/null | cmp -s - ".pearde/wiki/sources/scout/attachments/$f" \
    || n=$((n+1))
done
[ "$n" = 0 ]
if grep -rn -e 'resources/scout/findings\.md' -e 'resources/scout/reading-list' .pearde/wiki/sources/scout .pearde/wiki/conclusions/scout; then exit 1; fi
grep -q 'scout-findings-index-2026-08' .pearde/wiki/sources/scout/260831-3e48.md
grep -q 'scout-findings-index-2026-08' .pearde/wiki/sources/scout/260831-cbe9.md
grep -q 'scout-reading-list-2026-08' .pearde/wiki/sources/scout/260831-2cdf.md
grep -q 'scout-findings-index-2026-08' .pearde/wiki/conclusions/scout/scout-feeds-knowledge-knowledge-feeds-the-rou.md
python3 resources/knowledge.py --root .pearde/wiki relink > /dev/null
kd=$(python3 resources/knowledge.py --root .pearde/wiki doctor 2>&1) && krc=0 || krc=$?
[ -n "$kd" ]
printf '%s\n' "$kd"
printf '%s\n' "$kd" | grep -q 'doctor: clean'
if printf '%s\n' "$kd" | grep -q 'no frontmatter'; then exit 1; fi
q=$(python3 resources/knowledge.py --root .pearde/wiki query "which tool won recursive search over a source tree" 2>&1) && qrc=0 || qrc=$?
[ -n "$q" ]
printf '%s\n' "$q" | grep -q 'scout-findings-index-2026-08'
git -C .pearde ls-files -- wiki/sources/scout | grep -q 'scout-findings-index-2026-08'
if git status --short | grep -q 'wiki/sources/scout'; then exit 1; fi
echo spec02 green
```

The whole-wiki sweep of box three is narrowed to this spec's own two
directories. `.pearde/wiki/index/` is the `fileindex` layer `knowledge.py
index` generates from `index.md` and `references/files.md` — spec01's
footprint, not this one's — and eight of its notes name a departing file
until that command is re-run against the merged map. Measured in a scratch
copy: with spec01's map in place, `index` reports `7 stale removed` and the
whole-wiki grep returns nothing. Gating here on a generated layer this spec
does not own would make the block fail for spec01's merge order.
