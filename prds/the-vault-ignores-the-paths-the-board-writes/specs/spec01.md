---
complexity: 5
footprint:
  - resources/board/obsidian/app.json
  - .obsidian/app.json
---

# spec01 — the two Obsidian ignore lists name only paths that exist, and agree

Both `userIgnoreFilters` lists name only paths that exist under the current
layout, and the template and the live file are byte-identical.

## Acceptance

- [x] `resources/board/obsidian/app.json`'s `userIgnoreFilters` is exactly:
      `.claude/`, `.pearde/graphify/`, `.pearde/.state/`, `.pearde/.claims/`,
      `.pearde/wiki/.graphify/`, `.pearde/wiki/Dashboard.report.md`,
      `.pearde/wiki/graphs/`, `.pearde/wiki/pending/`,
      `.pearde/wiki/sources/.absorbed/`, `resources/board/state/`
- [x] `.obsidian/app.json` (this repo's own root vault) has the identical list
- [x] every entry, minus the trailing `/`, exists as a real path under the
      code repo root right now — all ten, with no exception
- [x] no entry names `prds/.plan.json`, `prds/knowledge/…`, `graphify-out/`,
      or any other path from a superseded layout
- [x] none of the ignored paths appears in the vault's index. Checked against
      the running app rather than by eye: `obsidian.json` registers
      `/Users/feb/dev/infra/pearde` as an open vault, and its own IndexedDB
      index holds `resources/board/knowledge/` but zero hits for
      `resources/board/state`, `.pearde/` or `.claude/` — a non-dot sibling
      indexed while the ignored non-dot path is not, which is the filter
      biting

## Verify and Proof

```sh
python3 - <<'PY'
import json, os, sys
want = [".claude/", ".pearde/graphify/", ".pearde/.state/", ".pearde/.claims/",
        ".pearde/wiki/.graphify/", ".pearde/wiki/Dashboard.report.md",
        ".pearde/wiki/graphs/", ".pearde/wiki/pending/",
        ".pearde/wiki/sources/.absorbed/", "resources/board/state/"]
tpl  = json.load(open("resources/board/obsidian/app.json"))["userIgnoreFilters"]
live = json.load(open(".obsidian/app.json"))["userIgnoreFilters"]
bad = []
if tpl  != want: bad.append(f"template list is {tpl}")
if live != want: bad.append(f"live list is {live}")
for p in want:
    if not os.path.exists(p.rstrip("/")): bad.append(f"{p} does not exist")
for b in bad: print("FAIL", b)
print("OK  10 entries, both files, all present" if not bad else "FAILED")
sys.exit(1 if bad else 0)
PY
```
