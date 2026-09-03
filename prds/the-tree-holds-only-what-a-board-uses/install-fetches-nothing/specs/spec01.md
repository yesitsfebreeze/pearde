---
complexity: 8
footprint:
  - resources/install.sh
  - resources/board/init.py
---

# spec01 — the fetch leaves the installer and lands behind `pearde vault`

`install.sh` is links and nothing else — five symlinks per skill, no copies —
and it carried a `curl` loop that downloaded two Obsidian plugin bundles from
GitHub releases into `resources/board/obsidian/plugins/`. A person installing
the skills on a machine with no network watched that fail and got a `!` line
and exit 1 from an installer that had, in fact, built every link it was asked
for. A person who never opens Obsidian paid for two bundles they will never
read. And `install.sh --remove` deleted those bundles, which is the installer
throwing away a several-megabyte download that is not part of any install.

The whole plugin block leaves `install.sh` — the header paragraph, the
`PLUGIN_DIR`/`PLUGINS` table, the fetch loop and the `--remove` arm that
deleted `main.js`, `manifest.json` and `styles.css`. Nothing replaces it: the
installer reaches no network in any mode, and `--remove` cannot delete a bundle
it no longer names.

The fetch lands in `resources/board/init.py`, behind `pearde vault` — the one
verb whose whole point is "I want this vault". Four new names:

- `OBSIDIAN_BUNDLES` — `name -> (github repo, release tag)`, the pins that used
  to sit in the shell table (`dataview 0.5.68`,
  `obsidian-local-rest-api 5.1.0`), plus `BUNDLE_FILES` and `BUNDLE_TIMEOUT`.
- `bundle_state(name)` — `ok` / `stale` / `missing` for the preset's copy,
  judged against the pin. An unreadable manifest is `stale`, not `ok`: a
  half-written bundle is not one to copy into somebody's vault.
- `fetch_bundle(name)` — one bundle, over `urllib.request`, each file landing
  as `<f>.part` and renamed, so an interrupted fetch leaves nothing
  `bundle_state` would read as good. A 404 on `styles.css` is not a failure —
  plenty of plugins ship none. Returns the failure line or `None`.
- `ensure_bundles(names)` — fetch everything the preset does not already hold
  at its pin; returns `(fetched, failed)` and never raises. A vault without
  dataview renders no view, which is worth saying out loud, but it is not
  worth refusing to register the vault over.
- `copy_bundles(dest)` — put every preset bundle a vault does not already have
  into it, leaving an installed plugin directory alone. This is what makes
  `pearde vault` actually repair the case the old wiring could not: a vault
  seeded before the bundles arrived.

`cmd_vault` calls `ensure_bundles()` before anything is copied anywhere, prints
what it fetched and one line per bundle it could not get, and — when the vault
is already there — calls `copy_bundles` on it. `--dry` names the bundles it
would fetch. Every console line that used to send a person to
`pearde install --apply <skills-dir>` for a missing bundle now sends them to
`pearde vault`: `cmd_init`'s no-bundle line, `cmd_upgrade`'s vault line, and
the two comments in `write_obsidian`.

**Already standing:** all of it is in the lane
(`.pearde/.lanes/the-tree-holds-only-what-a-board-uses-install-fetches-nothing`),
uncommitted. `install.sh` is 47 lines shorter and holds no URL; `init.py` holds
the five functions above and the pins. The harness at
`.pearde/prds/the-tree-holds-only-what-a-board-uses/install-fetches-nothing/probe/verify.sh`
runs `7 passed, 0 failed` against that lane and `6 failed` against the
unpatched checkout.

**Left to finish:** land it. One thing to watch while landing: the preset's
`main.js`, `manifest.json` and `styles.css` are shared-store symlinks per lane
(`resources/board/shared.py`), and a fetch writing a real file over one detaches
that lane from the store until `pearde share apply` runs again. The harness
never writes through the real preset for exactly this reason; a person who runs
`pearde vault` inside a lane should re-run `pearde share apply` after it.

## Acceptance

- [x] `resources/install.sh` matches no `curl`, no `wget` and no `http` URL
- [x] `resources/install.sh` names no `main.js`, `manifest.json` or `styles.css`, so `--remove` deletes no bundle
- [x] `bash resources/install.sh --apply <scratch-dir>` exits 0 with every route to the network cut, and prints no fetch line
- [x] `init.py` defines `OBSIDIAN_BUNDLES` with both pins, and `bundle_state`, `fetch_bundle`, `ensure_bundles`, `copy_bundles`
- [x] `ensure_bundles` brings a missing bundle in at its pinned version and fetches nothing on a second run
- [x] `copy_bundles` fills a vault that has no plugin directory and leaves an installed one untouched
- [x] `cmd_vault` calls `ensure_bundles` before it copies or registers anything, and `--dry` names what it would fetch
- [x] no console line in `init.py` sends a person to `install --apply` for a missing bundle

## Verify and Proof

```sh
if grep -qE 'curl|wget|https?://' resources/install.sh; then
  echo "install.sh still names a fetch"; exit 1
fi
if grep -qE 'main\.js|manifest\.json|styles\.css' resources/install.sh; then
  echo "install.sh still names a bundle file"; exit 1
fi
if grep -n 'install --apply' resources/board/init.py | grep -qi 'bundle\|fetch'; then
  echo "init.py still sends a person to the installer for a bundle"; exit 1
fi
python3 - <<'PY'
import importlib.util, os, sys
s = importlib.util.spec_from_file_location(
    "initlib", os.path.join("resources", "board", "init.py"))
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
bad = []
for n in ("bundle_state", "fetch_bundle", "ensure_bundles", "copy_bundles"):
    if not callable(getattr(m, n, None)):
        bad.append(f"init.py has no {n}")
pins = getattr(m, "OBSIDIAN_BUNDLES", {})
if pins.get("dataview", (None, None))[1] != "0.5.68":
    bad.append(f"dataview is not pinned at 0.5.68: {pins.get('dataview')}")
if pins.get("obsidian-local-rest-api", (None, None))[1] != "5.1.0":
    bad.append(f"local-rest-api is not pinned at 5.1.0: {pins.get('obsidian-local-rest-api')}")
src = open(os.path.join("resources", "board", "init.py"), encoding="utf-8").read()
if "ensure_bundles()" not in src.split("def cmd_vault", 1)[-1]:
    bad.append("cmd_vault does not call ensure_bundles")
for b in bad:
    print("  FAIL " + b)
print(f"{len(bad)} problem(s)")
sys.exit(1 if bad else 0)
PY
SK="$(mktemp -d)"
env http_proxy=http://127.0.0.1:1 https_proxy=http://127.0.0.1:1 \
    ALL_PROXY=http://127.0.0.1:1 bash resources/install.sh --apply "$SK" > "$SK/out.txt" 2>&1
if grep -qi 'could not fetch' "$SK/out.txt"; then
  echo "the offline install reported a fetch"; rm -rf "$SK"; exit 1
fi
rm -rf "$SK"
echo "spec01 green"
```
