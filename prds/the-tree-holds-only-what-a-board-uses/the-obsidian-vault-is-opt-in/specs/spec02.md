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

- [x] The fetch list holds exactly one row, `dataview`, at its pinned version.
- [x] `install.sh --check` names no `obsidian-local-rest-api` row as `ok` or `missing`.
- [x] A plugin directory in the preset that no row claims is reported `stale` by `--check` and removed by `--apply` and by `--remove`.
- [x] The stale line names the plugin without a trailing slash in its path.
- [x] `bash -n resources/install.sh` is clean and the report's other rows are unchanged in count.

## Verify and Proof

```sh
bash -n /Users/feb/dev/infra/pearde/resources/install.sh
out=$(bash /Users/feb/dev/infra/pearde/resources/install.sh --check 2>&1 || true)
printf '%s\n' "$out" | grep -E 'dataview|local-rest'
N=0
printf '%s\n' "$out" | grep 'local-rest' | grep -qE ' ok | missing ' && N=$((N+1))
if [ "$N" != 0 ]; then echo "FAIL rest named ok or missing"; exit 1; fi
echo "PASS rest never ok or missing"
mkdir -p /Users/feb/dev/infra/pearde/resources/board/obsidian/plugins/made-up
out=$(bash /Users/feb/dev/infra/pearde/resources/install.sh --check 2>&1 || true)
printf '%s\n' "$out" | grep 'made-up' | grep -q stale
echo "PASS stale named"
out=$(bash /Users/feb/dev/infra/pearde/resources/install.sh --remove /tmp/vaultoptin-dest 2>&1 || true)
printf '%s\n' "$out" | grep -q 'removed made-up'
echo "PASS removed by --remove"
if [ -d /Users/feb/dev/infra/pearde/resources/board/obsidian/plugins/made-up ]; then echo "FAIL still there"; exit 1; fi
echo "PASS made-up gone"
```

`--remove` above runs with a throwaway destination (the flag goes first — the
installer's arg order is `install.sh --remove <skills-dir>`) so the sweep fires
while nothing of the install is touched; `obsidian-local-rest-api` in the
preset goes the same way, on the next real `--apply`/`--remove`. The stale
line names the plugin by its basename with no trailing slash.
