---
complexity: 5
footprint:
  - resources/install.sh
---

# spec02 — the installer ships one bundle, and sweeps the one it dropped

`install.sh` fetched two pinned Obsidian bundles into the preset. One of them
— `obsidian-local-rest-api` — is dropped by this PRD, and a bundle the repo no
longer ships does not leave on its own: the preset is untracked, so git never
takes it away, and a machine that ran the old installer keeps several
megabytes that `install --check` happily reports as installed. The row goes,
and a sweep names any plugin directory in the preset that no `PLUGINS` row
claims — `stale` in report mode, removed on `--apply` and `--remove`.

**What stands** (built in this lane, uncommitted): the `PLUGINS` array holds
the `dataview` row alone; the header paragraph says one plugin and says why
the vault being opt-in makes a machine that never fetches it a supported
state; the sweep loop follows the fetch loop, stripping the trailing slash off
each glob match before naming it.

**What is left**: nothing in this file. **Read this before starting**: the
sibling PRD `install-fetches-nothing` is `specced` and its spec01 moves this
entire plugin block out of `install.sh` and behind `pearde vault`. Whichever
lands second applies the same two changes to wherever the fetch list then
lives — one `dataview` row and the stale sweep — rather than to this file by
name. The two are the same edit in two possible homes, never two edits.

## Acceptance

- [ ] The fetch list holds exactly one row, `dataview`, at its pinned version.
- [ ] `install.sh --check` names no `obsidian-local-rest-api` row as `ok` or `missing`.
- [ ] A plugin directory in the preset that no row claims is reported `stale` by `--check` and removed by `--apply` and by `--remove`.
- [ ] The stale line names the plugin without a trailing slash in its path.
- [ ] `bash -n resources/install.sh` is clean and the report's other rows are unchanged in count.

## Verify and Proof

```sh
bash -n <repo>/resources/install.sh
bash <repo>/resources/install.sh --check | grep -E 'dataview|rest'
mkdir -p <repo>/resources/board/obsidian/plugins/made-up
bash <repo>/resources/install.sh --check | grep 'made-up' | grep -q stale && echo "PASS stale named"
rmdir <repo>/resources/board/obsidian/plugins/made-up
```
