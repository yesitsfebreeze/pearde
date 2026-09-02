---
complexity: 8
footprint:
  - resources/board/shared.py
---

# spec03 — one graphify cache in the store, not one per spelling

`SHARED` lists the cache twice, once as `pearde/graphify/cache` and once as
`.pearde/graphify/cache`, and `targets()` drops the duplicate by comparing what
the two resolve to. That test holds only in the code checkout, where `.pearde` is
a symlink onto `pearde`. In a lane both are real directories, both rows fire, and
the store grows two caches that never share an entry.

Measured on this repo: 29 of 30 trees carry both, and
`<git-common-dir>/pearde-shared/` holds `pearde/graphify/cache` at 24 MB beside
`.pearde/graphify/cache` at 2.6 MB. One copy per machine, twice — which is the
duplication this PRD exists to remove, moved from the lanes into the store.

What already stands: both rows are still needed, because a board not yet upgraded
has a real `.pearde/`. What is left is that they must reach one store path.

The two spellings name one board, so they name one store entry. Point both rows
at a single store key, and merge the entries the second copy already holds into
the first before the second is dropped, so no cached extraction is refetched.

## Acceptance

- [x] Both board spellings link onto one store path, in a lane as well as in the checkout.
- [x] The store holds exactly one graphify cache directory after `share apply`.
- [x] The entries already under the second store copy are merged into the surviving one before it goes; no entry is lost.
- [x] A tree that has only `.pearde/` still gets a working link, and a tree that has only `pearde/` still gets one.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
python3 resources/pearde.py share apply
python3 -c "
import os, subprocess
d = subprocess.run(['git','rev-parse','--git-common-dir'],
                   capture_output=True, text=True).stdout.strip()
store = os.path.join(os.path.realpath(d), 'pearde-shared')
a = os.path.join(store, 'pearde/graphify/cache')
b = os.path.join(store, '.pearde/graphify/cache')
both = [p for p in (a, b) if os.path.isdir(p) and not os.path.islink(p)]
assert len(both) < 2, f'store holds two caches: {both}'
print('ok: one cache in the store')
"
```
