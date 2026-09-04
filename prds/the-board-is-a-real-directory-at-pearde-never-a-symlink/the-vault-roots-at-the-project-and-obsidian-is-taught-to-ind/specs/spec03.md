---
complexity: 10
footprint:
  - resources/doctor.sh
  - resources/board/init.py
---

# spec03 — the report and the commands state the project-rooted contract, and neither renames the board

`doctor`'s vault row read the board's dotted name as the failure and printed
`pearde upgrade` as its fix — a command that renames `.pearde/` to `pearde/`
and leaves a symlink behind, which is precisely the reversal the invariant
`the-board-directory-is-pearde-and-the-compat-symlink-is-gone` forbids. The
same rename sat at the top of `pearde vault`, which is the only command that
writes Obsidian's register: it refused every `.pearde` board outright, so on
this machine no project could be registered at all. Under the project-rooted
contract the dotted name is not the failure — a missing or disabled `unhide`
is — and registering is opt-in, so that no throwaway fixture board leaves a
dead vault in a person's Obsidian.

**Landed while this PRD was blocked**: `install-fetches-nothing`
(`session/s98669`) moved the bundle fetch out of `resources/install.sh` and
behind `pearde vault`, and added its own `ensure_bundles`/`copy_bundles` to
`cmd_vault`. Rebasing this spec's `cmd_vault` rewrite onto that meant
reconciling two independent rewrites of the same function rather than a
textual conflict: the sibling's fetch call is kept (`ensure_bundles()`, now
fetching `unhide` too since spec01 added it to `OBSIDIAN_BUNDLES`), the
`unhide_board` call this spec drops stays dropped, and `write_obsidian(d)`
runs unconditionally as this spec always intended — which already does
everything the sibling's separate `copy_bundles(dest)` branch did for an
existing `.obsidian/`, so that branch was not re-added to `cmd_vault` (the
function itself is untouched and unused there — a finding below, not fixed
here since it belongs to the sibling's footprint).

**What already stands** (rebuilt in the lane against the landed sibling):

- `doctor.sh`'s vault row drops the dot-segment arm and the `upgrade` fix.
  Its `ok` arm now reads `… — ▸vault opens the project, and unhide indexes
  .pearde inside it`; two new `broken` arms fire on a registered project
  whose vault has no `unhide` bundle, and on one where the bundle is there
  but `community-plugins.json` does not enable it. Both fixes now name only
  `pearde vault` — the one command left that fetches and seeds — and both
  say the board keeps its name. All three arms were exercised against a
  fixture project.
- `cmd_vault` no longer calls `unhide_board`. It also seeds unconditionally
  rather than only when `.obsidian/` is absent, so a vault created before
  `unhide` was pinned gains the plugin on the next run; `write_obsidian`
  overwrites nothing already in place. Verified directly: removing
  `.obsidian/plugins/unhide/` from an already-seeded fixture and re-running
  `pearde vault` restores it while `dataview`'s `main.js` is byte-identical
  before and after (`shasum` matched).
- `cmd_init` registers only when `--vault` is passed. Without it, `init`
  prints the one line saying the project is not registered and how to
  register it, and writes nothing into `obsidian.json`.

**What is left**: `upgrade` (`init.py`) still calls
`unhide_board`, and `unhide_board` is still in the file. That verb reverses
the invariant on a live board and is out of this PRD's contract — it is
reported as a finding, not fixed here. Decide whether `upgrade` should also
register, or whether `pearde vault` stays the only writer; the opt-in box
speaks about `init`.

## Acceptance

- [x] `resources/doctor.sh` contains no `pearde.py upgrade` in the vault
      row's fix, and no arm that reports the board's dotted name as broken.
- [x] On a registered project whose vault has `unhide` installed and enabled,
      the vault row is `ok` and its text names `unhide`.
- [x] With the `unhide` bundle removed from the vault, the row is `broken`
      and its fix names `pearde vault` — not a rename.
- [x] With the bundle present but `unhide` absent from
      `community-plugins.json`, the row is `broken` and says the plugin is
      installed but not enabled.
- [x] `pearde vault <project>` runs to completion on a `.pearde` board
      instead of refusing, and the board's directory name is unchanged
      afterwards.
- [x] `pearde vault` on a project whose vault predates `unhide` adds the
      plugin and rewrites no file that was already there.
- [x] `pearde init <dir>` writes no entry into Obsidian's register; `pearde
      init <dir> --vault` writes exactly one.
- [x] `bash resources/invariants/…/no-destructive-git…` and the rest of
      `resources/invariants/` are no worse than the recorded baseline.

## Verify and Proof

```sh
bash -n resources/doctor.sh
grep -c 'pearde.py upgrade' resources/doctor.sh   # expect 0 in the vault row
python3 .pearde/prds/the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind/probe/vault_contract.py .
for f in resources/invariants/*.sh; do printf '%-70s ' "$(basename $f)"; bash "$f" >/dev/null 2>&1 && echo PASS || echo FAIL; done
bash resources/doctor.sh | grep -A2 '^  vault'
```
