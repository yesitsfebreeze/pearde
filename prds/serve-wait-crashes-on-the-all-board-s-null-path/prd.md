---
state: deferred
origin: derived
from: the-board-is-a-real-directory-at-pearde-never-a-symlink
priority: 65
complexity: 0
blast-radius:
---

# serve wait crashes on the all board's null path

The user did not ask for this. It has been reported in four consecutive pass
files as *"`serve.py` registers the virtual `all` board with `path: null`"* and
each time it was worked around rather than fixed. Measured on 2026-09-03 in
`resources/board/serve.py`, the cause is exact and the crash site is one line.

**The `all` row is always there.** `serve.py:1143` appends
`{"name": alllib.KEY, "path": None, "seq": ALL.seq, …}` to the `/status`
payload unconditionally — it is the merged page over the watched boards, not a
board, so it has no path and correctly should not have one.

**Two readers of that payload, one of them safe.** `cmd_reap`'s liveness check
(`serve.py:1984`) reads `os.path.isdir(b.get("path") or "")` and carries a
comment saying why:

    `b.get("path", "")` returns that None — the default is only for a MISSING
    key — and `os.path.isdir(None)` raises TypeError, which took the whole
    reap down with a traceback.

**`cmd_wait` was never given the same treatment.** `serve.py:1839` still reads

    name = next((b["name"] for b in st["boards"]
                 if os.path.abspath(b["path"]) == os.path.abspath(board)), None)

`os.path.abspath(None)` raises `TypeError`. The generator hits the `all` row
and the call dies with a traceback instead of returning its documented exit
codes — the docstring one line above promises *"timeout ran out quietly, 2 = no
daemon"*, and neither is reachable once the `all` row is reached.

**Why it matters more than a stray traceback.** `pearde view wait` is the
dispatcher's own parking command (`references/parts/loop.md`, step 8). The
command a run parks on cannot raise.

`machine.boards()` is the third reader and is the model to copy: it skips the
row explicitly — `if not b.get("path"): skipped.append((b["name"], "no path —
the merged page, not a board"))`.

## Done means

- `cmd_wait` skips a watch-set row carrying no path instead of raising, and
  `pearde serve wait <board>` returns its documented exit codes with the `all`
  row present. A test proves it against a payload containing that row.
- Every reader of `st["boards"]` gets the path off one helper that returns the
  real boards, so a fourth reader cannot reintroduce this. `pearde index scope
  serve` names them; the three known are `serve.py:1839`, `serve.py:1984` and
  `machine.py:336`.
- The helper's contract is written down where the `all` row is registered
  (`serve.py:1143`): this row has no path, and no caller may assume one.
- No caller uses `b.get("path", "")` — the default fires only on a missing key,
  never on a null value, and that distinction is what produced both crashes.

## Related

`two-board-aliases-for-one-directory-fan-a-run-out-twice` fixes the *other*
defect on the very same line, `serve.py:1839`'s `os.path.abspath`, which does
not resolve symlinks. One line, two bugs, two PRDs: whichever lands second
rebases onto the first. Do not fold them — the null-path crash and the symlink
collapse have different tests and different done-means.
