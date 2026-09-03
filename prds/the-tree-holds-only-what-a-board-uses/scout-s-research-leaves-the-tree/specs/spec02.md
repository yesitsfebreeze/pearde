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

- [ ] `.pearde/wiki/sources/scout/` holds both new notes, each opening with a `---` frontmatter fence carrying `type: source`
- [ ] `.pearde/wiki/sources/scout/attachments/` holds all seven files, byte-identical to their content in git history
- [ ] No file under `.pearde/wiki/` contains the string `resources/scout/findings.md` or `resources/scout/reading-list.md`
- [ ] Both new notes are named by a wikilink from at least one older note
- [ ] `python3 resources/knowledge.py --root .pearde/wiki doctor` prints `doctor: clean` after a `relink`, with no `no frontmatter` line and no note left out of the graph
- [ ] `python3 resources/knowledge.py --root .pearde/wiki query "which tool won recursive search over a source tree"` returns `scout-findings-index-2026-08` among its hits
- [ ] `git -C .pearde status --short` shows the new files and `git status --short` in the code repo shows none of them — the board repo commits its own

## Verify and Proof

```sh
set -e
B=.pearde
test -f $B/wiki/sources/scout/scout-findings-index-2026-08.md
test -f $B/wiki/sources/scout/scout-reading-list-2026-08.md
head -1 $B/wiki/sources/scout/scout-findings-index-2026-08.md | grep -qx -- '---'
head -1 $B/wiki/sources/scout/scout-reading-list-2026-08.md | grep -qx -- '---'
for f in _typos.toml deny.toml dependabot.yml quality.yml scout.yml 2026-08-25.tsv 2026-08-28.tsv; do
  test -s "$B/wiki/sources/scout/attachments/$f"
done
! grep -rn -e 'resources/scout/findings\.md' -e 'resources/scout/reading-list' $B/wiki
grep -rq 'scout-findings-index-2026-08' $B/wiki/sources/scout/260831-3e48.md
grep -rq 'scout-reading-list-2026-08' $B/wiki/sources/scout/260831-2cdf.md
python3 resources/knowledge.py --root $B/wiki relink > /dev/null
python3 resources/knowledge.py --root $B/wiki doctor | tee /tmp/spec02-doctor.txt | grep -q 'doctor: clean'
! grep -q 'no frontmatter' /tmp/spec02-doctor.txt
python3 resources/knowledge.py --root $B/wiki query "which tool won recursive search over a source tree" | grep -q 'scout-findings-index-2026-08'
git -C $B status --short | grep -q 'wiki/sources/scout'
! git status --short | grep -q 'wiki/sources/scout'
echo spec02 green
```
