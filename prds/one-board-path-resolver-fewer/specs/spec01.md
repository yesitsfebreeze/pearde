---
complexity: 4
footprint:
  - resources/statusline.sh
---

# spec01 — the status line checks the current name before the legacy one

`resources/statusline.sh`'s board-segment walk (`## board segment` block)
tests `$d/pearde/settings.md` before `$d/.pearde/settings.md` — the reverse
of `resources/common.py` and `resources/board/boards.py`, which both hold
`BOARD_DIR = ".pearde"` ahead of `LEGACY_BOARD_DIR = "pearde"` since the
2026-09-03 revert. The header comment above the walk (`A board is a pearde/
directory ... — .pearde/ on a board that never migrated out of the hidden
name`) describes the reverted 2026-09-02 direction too. Order only changes
the answer for the pathological case both directories are real (not one a
symlink to the other), but the comment is read by whoever next touches this
file, and it currently teaches the wrong history.

Confirmed by `probe/order-and-duplication.sh`, section "shell resolvers:
which name they test FIRST".

## Acceptance

- [x] The first board-name check in the walk tests `$d/.pearde/settings.md`; the second tests `$d/pearde/settings.md`.
  - `dot=97 legacy=104` — `test "$(cat /tmp/first_dot)" -lt "$(cat /tmp/first_legacy)"` passed.
- [x] The header comment names `.pearde/` as the current directory and `pearde/` as the legacy one it is read through a compat symlink for — not the reverse.
- [x] `resources/statusline.sh` still parses under `bash -n` and its board segment resolves the same path as before on a board carrying only `.pearde/` or only `pearde/` (no behavior change on any single-name board — this repo's own board included).
  - `bash -n` clean; `echo '{"model":{"display_name":"x"},"cwd":"<repo>"}' | bash resources/statusline.sh | grep -q 'pearde'` passed (board renders).

## Verify and Proof

```sh
cd "$REPO"
bash -n resources/statusline.sh
grep -n 'd/\.pearde/settings\.md' resources/statusline.sh | head -1 | cut -d: -f1 > /tmp/first_dot
grep -n 'd/pearde/settings\.md' resources/statusline.sh | head -1 | cut -d: -f1 > /tmp/first_legacy
# the dotted check's line number must be lower than the legacy check's
test "$(cat /tmp/first_dot)" -lt "$(cat /tmp/first_legacy)"
echo '{"model":{"display_name":"x"},"cwd":"'"$PWD"'"}' | bash resources/statusline.sh | grep -q 'pearde'
```
