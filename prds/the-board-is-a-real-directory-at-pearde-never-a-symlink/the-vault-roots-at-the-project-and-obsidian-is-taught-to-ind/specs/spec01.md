---
complexity: 10
footprint:
  - resources/board/init.py
  - resources/board/obsidian/community-plugins.json
  - resources/board/obsidian/app.json
  - resources/board/obsidian/plugins/unhide/data.json
---

# spec01 — unhide is a declared dependency, pinned, seeded and enabled

The board is `.pearde/`, and Obsidian skips every path holding a dot-segment
before it reads a single setting. From a vault at the project root the whole
board is therefore invisible, and `userIgnoreFilters` cannot help — that
setting only adds ignores. `polyipseity/obsidian-unhide` is the one mechanism
that makes the dotted board indexable, so it becomes the third plugin the
vault requires, fetched at a pinned version beside dataview and the REST API,
seeded into every board's vault, and named when its bundle is not there.

**Landed while this PRD was blocked**: `install-fetches-nothing`
(`session/s98669`) moved every bundle fetch out of `resources/install.sh` —
that script now only links skill folders — and behind `pearde vault`
instead, through `resources/board/init.py`'s `OBSIDIAN_BUNDLES` /
`ensure_bundles` / `fetch_bundle`. `install.sh` carrying `unhide`'s pin, and
`vault_contract.py` reading it out of `install.sh`, are both stale under that
landed contract. This pass rebased onto it: `unhide` moved into
`OBSIDIAN_BUNDLES` beside the other two plugins, `install.sh` was left
exactly as `install-fetches-nothing` shipped it, and the probe now reads the
pin out of `init.py`.

**What already stands** (rebuilt in the lane against the landed sibling):

- `OBSIDIAN_PLUGINS` in `resources/board/init.py` is `("dataview",
  "obsidian-local-rest-api", "unhide")` and `OBSIDIAN_BUNDLES["unhide"]` is
  `("polyipseity/obsidian-unhide", "3.1.0")` — the release publishes
  `main.js`, `manifest.json` and `styles.css` as assets under a bare `3.1.0`
  tag, which is exactly what `fetch_bundle` expects, so it needed no change
  beyond the one dict entry.
- `pearde vault` calls `ensure_bundles()` before it seeds, so `--dry` and a
  missing-network run both name `unhide` when the preset does not hold it,
  and `write_obsidian` copies whatever `ensure_bundles` left into a new or an
  already-configured board's vault, naming it in `missing` when the fetch
  never got it.
- `community-plugins.json` lists `unhide`, so the plugin is enabled on the
  vault's first open rather than sitting installed and inert.
- `app.json` sets `showUnsupportedFiles` to `true` — the plugin's README makes
  `Files & links > Detect all file extensions` a precondition for it to work
  at all.
- `plugins/unhide/data.json` ships `showingRules`, `"+/"` first and then the
  exclusions. The default rules exclude only `.git` and `.venv`; on a pearde
  project that leaves `.pearde/.lanes/` — one full checkout per lane — for
  Obsidian to walk on enable, which the README names as the freeze case. The
  shipped rules exclude `.lanes`, `.state`, `.claims`, `.graphify`,
  `.obsidian`, the three cache directories and `node_modules` at any depth.

**What is left**: none — the bundle directory name is already the plugin's
manifest `id` (`unhide`), not the repo name (`obsidian-unhide`); the
`.gitignore` rules hold `main.js`/`manifest.json`/`styles.css` out of the tree
while `plugins/unhide/data.json` stays tracked; and `references/files.md`'s
directory row for `@resources/board/obsidian/` already covers the new file.

## Acceptance

- [x] `resources/board/init.py`'s `OBSIDIAN_BUNDLES` pins
      `polyipseity/obsidian-unhide` at an exact version, and `pearde vault`
      fetches `main.js`, `manifest.json` and `styles.css` into
      `resources/board/obsidian/plugins/unhide/`.
- [x] `pearde vault --dry` names the unhide bundle as missing rather than
      passing silently when it has not been fetched.
- [x] `OBSIDIAN_PLUGINS` names `unhide`, and a board made by `pearde init`
      has `.obsidian/plugins/unhide/main.js` in it.
- [x] `.obsidian/community-plugins.json` in that board lists `unhide`.
- [x] `.obsidian/app.json` in that board has `showUnsupportedFiles` true.
- [x] `.obsidian/plugins/unhide/data.json` in that board carries
      `showingRules` whose first rule includes hidden files and which exclude
      `.lanes`, `.state`, `.claims`, `.graphify` and `.git`.
- [x] `git status` on the repo shows no `main.js`, `manifest.json` or
      `styles.css` under `resources/board/obsidian/plugins/`.
- [x] `python3 resources/index.py check` reports no new problem.

## Verify and Proof

```sh
grep -n 'polyipseity/obsidian-unhide' resources/board/init.py
python3 resources/pearde.py vault --dry /tmp/unhide-check-project
ls resources/board/obsidian/plugins/unhide
git status --porcelain resources/board/obsidian/plugins/ | grep -E 'main\.js|manifest\.json|styles\.css' && echo BAD || echo "bundles held out"
python3 .pearde/prds/the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind/probe/vault_contract.py .
python3 resources/index.py check
```
