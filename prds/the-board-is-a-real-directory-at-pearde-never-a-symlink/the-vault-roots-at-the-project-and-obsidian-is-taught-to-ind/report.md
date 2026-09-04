Verdict: DONE

# Report — the vault roots at the project and obsidian is taught to index the dotted board

The lane's rebase onto `session/s98669` (`install-fetches-nothing`) was left
mid-conflict — an interactive rebase stopped with 4 files unmerged
(`references/files.md`, `references/obsidian.md`, `resources/board/init.py`,
`resources/install.sh`). This pass resolved every conflict, finished the
rebase, found and fixed one stale reference the merge itself didn't touch,
and reran every spec's verify block against the result.

## Workflow implementer-continue

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | merge-blocking-branch | passed | `git rebase` (already in progress onto `4a94475`, the tip after `session/s98669` landed) — `git diff --name-only --diff-filter=U` named the 4 files above; each read whole with its conflict markers and the commit range that produced each side |
| 2 | reconcile-conflict-by-design-not-by-side | passed | Each hunk combined by design: `init.py`'s `OBSIDIAN_PLUGINS`/`OBSIDIAN_BUNDLES` merged (sibling's dict machinery + this PRD's `unhide` entry and tuple); `cmd_vault` merged (sibling's `ensure_bundles()` fetch kept, this PRD's dropped `unhide_board` call and unconditional `write_obsidian` kept); `cmd_init`'s missing-bundle message took the sibling's `pearde vault` wording, its new `repair_vault_relative` `else` branch kept; `install.sh` took the sibling's deletion of the fetch section outright (it now fetches nothing, matching `install-fetches-nothing`); `references/files.md` and `references/obsidian.md` rows combined this PRD's three-plugin/`unhide` content with the sibling's `pearde vault fetches` phrasing. `grep -rn` for the four conflict marker shapes over the repo returns nothing; `python3 -c "import ast; ast.parse(...)"` on `init.py` and `bash -n` on `install.sh` and `doctor.sh` all pass |
| 3 | rerun-probe-against-merge | passed | `python3 .pearde/prds/.../probe/vault_contract.py .` → 7/7 boxes pass (quoted below); `resources/invariants/*.sh` all PASS; `python3 resources/index.py check` shows only the two pre-existing findings (`resources/common.py` no row, `hotreload-test.js` not on disk) — confirmed via `git diff --name-only 4a94475 HEAD` that neither file is in this commit's footprint |
| 4 | update-stale-specs-and-probe | passed | Grepping `references/` and `resources/doctor.sh` for the moved machinery found one thing the rebase's auto-merge did not touch because it wasn't a textual conflict: `doctor.sh`'s vault-row fix for "unhide installed but not enabled/missing" and `references/obsidian.md`'s matching sentence both still named `install.sh --apply` to fetch the bundle — stale under `install-fetches-nothing`, which moved that fetch to `pearde vault`. Both reworded to name `pearde vault` alone and reverified live (see below) |

No workflow atomic itself misfired — every `## Do` step and `## Fails when` shape held. `### Edits` is empty.

## Spec01 — unhide is a declared dependency, pinned, seeded and enabled

All 8 acceptance boxes verified:

```
$ grep -n 'polyipseity/obsidian-unhide' resources/board/init.py
141:# lists — `unhide` is the id of polyipseity/obsidian-unhide, not its repo
152:    "unhide": ("polyipseity/obsidian-unhide", "3.1.0"),

$ python3 resources/pearde.py vault --dry /tmp/unhide-check-project   # bundle present
dry · would register /tmp/unhide-check-project with Obsidian
$ (with resources/board/obsidian/plugins/unhide moved aside)
dry · would register /tmp/unhide-check-project with Obsidian · would fetch unhide

$ ls resources/board/obsidian/plugins/unhide
data.json  main.js  manifest.json  styles.css

$ git status --porcelain resources/board/obsidian/plugins/ | grep -E 'main\.js|manifest\.json|styles\.css' && echo BAD || echo "bundles held out"
bundles held out
```

Live `pearde vault` seeded `.pearde` boards show `unhide` in
`.obsidian/community-plugins.json`, `app.json` `showUnsupportedFiles: true`,
and `plugins/unhide/data.json`'s `showingRules` = `['+/', '-/\.git.../',
'-/\.venv.../', '-/\.obsidian.../', '-/\.lanes.../', '-/\.state.../',
'-/\.claims.../', '-/\.graphify.../', ...]`.

`python3 resources/index.py check` — no new problem (see step 3 note above).

## Spec02 — every vault-relative path names the board this project actually has

```
$ grep -rn '[^.a-zA-Z/-]pearde/' resources/board/knowledge/ && echo BAD || echo "preset clean"
preset clean
$ python3 -c "import json;print([f for f in json.load(open('resources/board/obsidian/app.json'))['userIgnoreFilters'] if f.startswith('pearde/')])"
[]
```

Probe box `Dataview sources resolve from the project root` and
`userIgnoreFilters resolve from the project root` both PASS (0 stale lines).
Manually verified the two "what is left" checks the spec named:
`retarget()` only rewrites the prefix after a quote/apostrophe/`[[`, so a
board renamed to `theboard/` came out with `Dashboard.md`'s
`FROM "theboard/wiki/board"` and, after `pearde vault`, `userIgnoreFilters`
rewritten to `theboard/...` — a bare-word `pearde/` in prose is untouched
because it never follows one of those three leads.

## Spec03 — the report and the commands state the project-rooted contract

```
$ bash -n resources/doctor.sh && echo OK
OK
$ grep -c 'pearde.py upgrade' resources/doctor.sh
0
```

All 6 `resources/invariants/*.sh` PASS. All three `vault` row arms
exercised live against a fixture (Obsidian's register faked under a scratch
`HOME`):
- registered + unhide present + enabled → `ok … unhide indexes .pearde inside it`
- registered + unhide bundle missing → `broken … fix: pearde.py vault <dir> — fetches the pinned unhide bundle and seeds it into the vault, the board keeps its name`
- registered + bundle present, not in `community-plugins.json` → `broken … unhide is installed but not enabled`

`pearde vault <dir>` ran to completion on the `.pearde` board this repo
itself has (`bash resources/doctor.sh` on the repo shows `vault ok … as
pearde`) — no rename, `.pearde` unchanged. `pearde init <dir>` (no `--vault`)
registers nothing; `pearde init <dir> --vault` is the one path that writes
the register.

## Spec04 — the written contract says the project root and names three plugins

```
$ grep -rn "roots at \`\.pearde\|root is \`\.pearde\|\.pearde/\.obsidian\|two required plugins\|Two plugins" references/ && echo BAD || echo "no stale claim"
no stale claim
$ python3 resources/index.py check   # only the two pre-existing, out-of-footprint findings
$ bash resources/doctor.sh | grep -E "^  (index|vault) "
index broken 3 problems   (pre-existing, not new — see step 3)
vault ok    /Users/feb/dev/infra/pearde/.obsidian · registered as pearde …
```

Found and fixed one stale claim the merge itself left standing (not caught
by the acceptance grep, since it doesn't match those five phrases):
`resources/doctor.sh`'s vault-row fix and `references/obsidian.md`'s
matching sentence named `install.sh --apply`, which fetches nothing since
`session/s98669` landed. Both now name `pearde vault` alone.

## Commits

- `0055a36` — the rebased, reconciled PRD commit (13 files, +329/-132)
- `cf4bbca` — the `install.sh --apply` → `pearde vault` correction in
  `doctor.sh` and `references/obsidian.md`

Both on
`lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`.
`git status --porcelain` in the lane is clean.

No footprint file was under the health floor (brief named none).
