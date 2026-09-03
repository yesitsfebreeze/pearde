---
complexity: 3
footprint:
  - references/parts/board.md
  - references/parts/commits.md
  - references/parts/guard.md
---

# spec01 — *Where the board is* reads the dotted order, and the pages that copy it agree

`references/parts/board.md` is the page every other reader is pointed at for
the board's location. It argued the undotted layout: the board at `pearde/`,
`.pearde` a compatibility symlink beside it, and a paragraph of Obsidian
reasoning as the justification. The memo
`the-board-directory-is-pearde-and-the-compat-symlink-is-gone` settled the
opposite, so the page and the two pages spelling board paths in prose —
`commits.md` and `guard.md` — are rewritten to it.

**Stands.** All three files are rewritten in the lane. *Where the board is*
opens on the real dotted directory, gives the four-step order with `.pearde/`
first and `pearde/` as the legacy name, cites the memo, and hands the vault
question to `@references/obsidian.md` rather than answering it. `commits.md`
and `guard.md` spell every board path `.pearde/…`. `prose.py check` is clean on
`board.md`; `commits.md` carries three waste words that are its own at `HEAD`
and are not this spec's to clear.

**Left.** Nothing but the checks below.

## Acceptance

- [x] `references/parts/board.md` names no vault root — the sentence deciding
      where Obsidian opens is `@references/obsidian.md`'s, and this page cites
      it instead of restating it. The vault contract is being settled by
      `the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`, so a
      claim here would go stale the day it lands.
- [x] The numbered order in *Where the board is* reads `.pearde/` at step 1,
      `pearde/` at step 2 and `.pearde/` at step 4, matching
      `boards.py BOARD_DIRS` and its `board_named` fallback.
- [x] `references/parts/board.md` says `pearde upgrade` leaves no symlink
      behind, and names the memo that decided it.
- [x] `commits.md` and `guard.md` hold no bare `pearde/` at all, and every one
      left in `board.md` is introduced as the legacy name or as what `pearde
      upgrade` moves.
- [x] `python3 resources/prose.py check references/parts/board.md` prints
      nothing.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
python3 resources/prose.py check references/parts/board.md
# commits.md and guard.md spell no board path undotted at all
for f in references/parts/commits.md references/parts/guard.md; do
  grep -nE '(^|[^./a-zA-Z_-])pearde/' "$f" && { echo "FAIL $f"; exit 1; }
done
# in board.md every bare `pearde/` is introduced as the legacy name or as what
# `upgrade` moves — a line asserting it as the board's own name fails here
grep -nE '(^|[^./a-zA-Z_-])pearde/' references/parts/board.md \
  | grep -vE 'legacy|upgrade' && { echo "FAIL board.md"; exit 1; }
# the order, and the memo
grep -q '1\. `<project>/\.pearde/`' references/parts/board.md || exit 1
grep -q '4\. and when none does, `<project>/\.pearde/`' references/parts/board.md || exit 1
grep -q 'the-board-directory-is-pearde-and-the-compat-symlink-is-gone' references/parts/board.md || exit 1
grep -q 'leaves no link behind' references/parts/board.md || exit 1
# the page defers the vault rather than deciding it
grep -q "@references/obsidian.md's" references/parts/board.md || exit 1
echo "spec01 ok"
```
