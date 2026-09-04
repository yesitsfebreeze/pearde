---
complexity: 6
footprint:
  - references/obsidian.md
  - references/knowledge.md
  - references/files.md
  - references/parts/statusline.md
  - references/skills/pearde-knowledge.md
---

# spec04 — the written contract says the project root and names three plugins

Six documentation files still carry the superseded contract — the vault
rooting at `.pearde/`, the vault directory living at `.pearde/.obsidian/`,
and two required plugins. `init.py` and `statusline.sh` have rooted at the
project since 2026-09-02, so these pages already disagreed with the code
before this PRD; with `unhide` added they are wrong on a second count. A
person reading `references/obsidian.md` today is told to root Obsidian at a
folder Obsidian cannot show.

**What already stands**: every row of the table below, corrected in the lane
and verified — no file under `references/` reads "roots at `.pearde`", "root
is `.pearde`", `.pearde/.obsidian`, "two required plugins" or "Two plugins"
(the acceptance grep returns nothing), and `unhide`, the pinned version and
the manifest-`id` note are in `references/obsidian.md` and
`references/files.md`.

Rebasing onto `install-fetches-nothing` (`session/s98669`), landed while this
PRD was blocked, conflicted in exactly these two files — that sibling
reworded the same "install.sh fetches the bundles" sentences this spec had
already corrected, to "`pearde vault` fetches" instead, since the fetch moved
out of `install.sh` entirely. The three-way merge kept both: this spec's
three-plugins/`unhide` content, reworded to the sibling's "`pearde vault`
fetches" phrasing. One sentence the merge did not touch was still stale for
the same reason — `doctor`'s vault-row fix in `references/obsidian.md` named
`install.sh --apply`, corrected here to name `pearde vault` alone.

**What is left**, each claim and where it sits:

| file | the claim to correct |
|---|---|
| `references/obsidian.md` | "The board is the vault: Obsidian roots at `.pearde/`"; the whole section "The root is `.pearde/`, never the repo root"; "Seeds `.pearde/.obsidian/`"; "Two plugins, seeded by `init`" and its table; the sentence saying `userIgnoreFilters` only adds ignores should stay — it is true and it is now the reason `unhide` is needed |
| `references/knowledge.md` line 19 | "The board's vault roots at `.pearde/`" |
| `references/files.md` line 50 | the `obsidian.md` row's "the two required plugins" |
| `references/files.md` line 175 | the `init.py` row: "seeds the Obsidian vault at the board (`.pearde/.obsidian/`… dataview + local-rest-api…)" — it is the project, three plugins, and `init` no longer registers unless asked |
| `references/files.md` line 177 | the preset row: "the two required plugins' settings" |
| `references/parts/statusline.md` line 52 | "whenever `.pearde/.obsidian/` exists" — `statusline.sh` reads `<project>/.obsidian` first and the board only as a fallback |
| `references/skills/pearde-knowledge.md` line 8 | "the folder is its own Obsidian vault" — it is a folder inside the project's vault |

`references/obsidian.md` also gains what the probe learned and no page holds:
that the bundle directory is the manifest `id` `unhide`; that the plugin
needs `Detect all file extensions`; that its default `showingRules` exclude
only `.git` and `.venv`, so `.pearde/.lanes/` must be excluded by hand or
enabling the plugin walks every lane checkout; and the plugin's own warning
that in an Obsidian Sync vault it can delete hidden files, with `protectSync`
on by default.

## Acceptance

- [x] No file under `references/` says the Obsidian vault roots at the board
      or at `.pearde/`.
- [x] No file under `references/` says the vault directory is
      `.pearde/.obsidian/`.
- [x] `references/obsidian.md` names three plugins with `unhide` among them,
      says the bundle directory is `unhide`, and names the pinned version.
- [x] `references/obsidian.md` records the `Detect all file extensions`
      precondition, the default `showingRules` and why `.lanes` must be
      excluded, and the Obsidian Sync warning.
- [x] The `init.py` and preset rows in `references/files.md` describe what
      those files now do, registration included.
- [x] `python3 resources/index.py check` and `bash resources/doctor.sh`
      report no new problem.

## Verify and Proof

```sh
grep -rn "roots at \`\.pearde\|root is \`\.pearde\|\.pearde/\.obsidian\|two required plugins\|Two plugins" references/ && echo BAD || echo "no stale claim"
grep -n "unhide" references/obsidian.md references/files.md
python3 resources/index.py check
bash resources/doctor.sh | grep -E "^  (index|vault) "
```
