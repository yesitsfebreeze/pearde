---
complexity: 8
footprint:
  - resources/board/init.py
  - references/archive.md
  - references/settings.md
  - references/parts/contract.md
---

# spec02 — one registry says which keys are real

`init.py`'s `DEFAULTS` is six pairs — the keys `pearde init` prints into a new
`settings.md`. The board honours twenty-three: `claim-ttl`, `harnesses`,
`gate`, `context-budget`, `machine-ceiling` and the rest each read at a
default held by their one reader, and several (`transitions-per-pass`) are
read by a worker rather than by any module here. So there is no set in this
repo that answers "is this a real key", and a check against `DEFAULTS` alone
calls seventeen live keys drift.

Add `SETTING_KEYS` and `FRONTMATTER_KEYS` beside `DEFAULTS`, `DEFAULTS` being
the printed subset of the first. spec01 reads both by regex rather than by
import — `init.py` writes files, and a checker must not run one.

Then mark the three places this repo names a key or a command on purpose that
does not exist, so the row is honest rather than merely loud:
`references/archive.md`'s rejected `pearde archive`, `references/settings.md`'s
paragraph explaining that there is deliberately no `persona:` key, and
`references/parts/contract.md`'s `time:` nesting example.

The build for this stands at `probe/row-and-registry.diff`.

## Acceptance

- [x] `resources/board/init.py` holds `SETTING_KEYS`, a tuple of every settings key `references/settings.md` documents, and `DEFAULTS`'s six names are a subset of it
- [x] `resources/board/init.py` holds `FRONTMATTER_KEYS`, a tuple covering `references/parts/contract.md`'s `prd.md` and `specNN.md` tables and the `vision.md` keys `board.md` names
- [x] What `pearde init` writes into a new `settings.md` is unchanged — `DEFAULTS` is still its only source
- [x] `python3 resources/claims.py keys` prints both tuples and no key documented in `references/settings.md` is missing from the settings half
- [x] `references/archive.md`, `references/settings.md` and `references/parts/contract.md` each carry `<!-- claims: ignore -->` on the one line that names something on purpose that does not exist, and nowhere else
- [x] With spec01 landed, `claims check` reports exactly the misses that are real drift: `commits:` in `references/parts/commits.md`, `done-counts-which-boxes` in `resources/board/mapfile.py` and `resources/board/prdfile.py`, and the command names `pearde report`, `pearde once` and `pearde master`

## Verify and Proof

```sh
python3 -c "import sys;sys.path.insert(0,'resources/board');import init;
d={k for k,_ in init.DEFAULTS};assert d<=set(init.SETTING_KEYS),d-set(init.SETTING_KEYS);
print(len(init.SETTING_KEYS),'settings',len(init.FRONTMATTER_KEYS),'frontmatter')"
python3 resources/claims.py check || true
grep -c 'claims: ignore' references/archive.md references/settings.md references/parts/contract.md
```
