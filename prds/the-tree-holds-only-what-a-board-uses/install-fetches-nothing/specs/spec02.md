---
complexity: 4
footprint:
  - references/files.md
  - references/obsidian.md
  - resources/board/shared.py
  - resources/update.sh
---

# spec02 — every claim that the install fetches, corrected, and the harness

Four files told a reader the installer downloads the Obsidian bundles. Once
spec01 lands they are wrong, and a wrong claim about where a download happens
is the kind that costs a person an afternoon: they run the installer on a
machine with no network, see no plugin, and go looking in the wrong file.

- `references/obsidian.md` — "pinned bundles fetched by `install.sh --apply`"
  becomes `pearde vault`, and says the thing worth knowing about it: it is the
  one command in the repo that reaches the network, and it fetches only what
  the preset does not already hold at the pin.
- `references/files.md` — two rows. The `@resources/board/obsidian/` row said
  `install.sh` fetches the bundles; the `@resources/board/init.py` row said the
  preset was one "the install fetched" and named "a bundle the install never
  fetched". Both now name `vault`.
- `resources/board/shared.py` — the three `Share(...)` rows for the bundle
  globs describe them as "pinned by `install --apply`". They are pinned by
  `pearde vault`. The rows themselves are unchanged; only the description is.
- `resources/update.sh` — the row filter carries `# agents and plugins report
  too`, explaining why a name with no skill file is skipped. `install.sh` emits
  no plugin row any more, so the comment names a row that cannot appear.

The harness is the other half. `probe/verify.sh` is seven checks: the
installer names no fetch and no bundle file; `--apply` exits 0 with every route
to the network cut and prints no fetch line; `ensure_bundles` brings a missing
bundle in at the pin and fetches nothing on a second run; `copy_bundles` fills
an empty vault and leaves an installed plugin alone; and no file in the tree
still claims the install fetches. It pins its own denominator — a run that
reports fewer than seven checks fails rather than going quietly green — and
counts a network-less run of checks 4 and 5 as skipped, never as passed.

It writes nothing into the tree under test: the fetch checks repoint
`initlib.OBSIDIAN_PRESET` at a temp directory, because the real preset's
`main.js`, `manifest.json` and `styles.css` are shared-store symlinks in a lane
and writing a real file over one detaches that lane from the store.

**Already standing:** the four corrections are in the lane, and
`probe/verify.sh` is written and runs `7 passed, 0 failed` against it. Against
the unpatched checkout it exits 1 with six failures, including check 7 naming
the two `references/files.md` rows — so the check demonstrably fails on the
tree it is meant to catch.

**Left to finish:** land the four corrections with spec01, and keep the harness
where `doctor --harnesses` finds it (`<prd>/probe/verify.sh`).

## Acceptance

- [x] no file under `references/`, no `index.md`, no `README.md`, and neither `init.py` nor `shared.py` claims the install fetches the plugin bundles
- [x] `references/obsidian.md` names `pearde vault` as the fetch and says it is the one command that reaches the network
- [x] the `@resources/board/obsidian/` and `@resources/board/init.py` rows of `references/files.md` both name `vault`, not the install
- [x] the three bundle `Share` rows in `shared.py` say "pinned by `pearde vault`"
- [x] `resources/update.sh` no longer says the installer emits plugin rows
- [x] `probe/verify.sh` exists, is executable, runs seven checks and ends `7 passed, 0 failed` on the patched tree
- [x] `probe/verify.sh` exits non-zero against a tree where the installer still fetches
- [x] `python3 resources/index.py check` reports no problem this PRD introduced

## Verify and Proof

```sh
if grep -rniE 'install[^\n]{0,40}fetch|fetch[^\n]{0,30}install --apply' \
     references index.md README.md resources/board/init.py resources/board/shared.py \
     | grep -vi 'git .*fetch'; then
  echo "a file still claims the install fetches"; exit 1
fi
if ! grep -q 'pinned by `pearde vault`' resources/board/shared.py; then
  echo "shared.py still credits the installer"; exit 1
fi
if grep -q 'agents and plugins report too' resources/update.sh; then
  echo "update.sh still names a plugin row"; exit 1
fi
H=""
for B in .pearde pearde ../..; do
  P="$B/prds/the-tree-holds-only-what-a-board-uses/install-fetches-nothing/probe/verify.sh"
  if [ -f "$P" ]; then H="$P"; break; fi
done
if [ -z "$H" ]; then echo "the harness is not reachable from $PWD"; exit 1; fi
test -x "$H"
PEARDE_ROOT="$PWD" bash "$H" > "$PWD/.spec02.out" 2>&1
tail -2 "$PWD/.spec02.out"
grep -qE '^7 passed, 0 failed' "$PWD/.spec02.out"
rm -f "$PWD/.spec02.out"
R=$(mktemp -d); mkdir -p "$R/resources"
printf '#!/bin/bash\ncurl -fsSL https://example.invalid/main.js\n' > "$R/resources/install.sh"
if PEARDE_ROOT="$R" bash "$H" > "$R/red.txt" 2>&1; then
  echo "the harness went green on a tree whose installer fetches"; rm -rf "$R"; exit 1
fi
rm -rf "$R"
python3 resources/index.py check > "$PWD/.spec02.idx" 2>&1 || true
if grep -qiE 'install\.sh|obsidian|update\.sh' "$PWD/.spec02.idx"; then
  echo "index.py check names a file this PRD touched"; cat "$PWD/.spec02.idx"; rm -f "$PWD/.spec02.idx"; exit 1
fi
rm -f "$PWD/.spec02.idx"
echo "spec02 green"
```
