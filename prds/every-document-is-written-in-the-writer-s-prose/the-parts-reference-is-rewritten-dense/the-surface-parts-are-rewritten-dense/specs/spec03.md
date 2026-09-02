---
complexity: 6
footprint:
  - references/parts/order.md
---

# spec03 — `references/parts/order.md` rewritten dense

The three axes, the pressure order and the calibration prose are cut for
density, and the long calibration paragraph splits where the argument turns.
Already stands, done in the lane: 1,069 → 1,046 words, `check` green, 8
unbound pronouns to none.

`one-predicate-for-dispatchable` names a **two-line** needle for this file —
`` every child `done` — a parked`` and `   child holds its parent`. Its `has()`
helper runs `grep -F` on that needle, and `grep -F` reads a multi-line pattern
as one pattern **per line**, so the assertion passes when *either* half appears
anywhere in the file. Measured, not assumed: re-wrapping the clause leaves the
harness at `ok` and its totals unmoved.

The original wrap is restored anyway, and the box below asserts the exact
two-line string the harness's author meant. The box is deliberately stricter
than the harness — a re-wrap that the harness waves through fails here.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/order.md` exits `0`
- [x] the word count is at or below the count at `HEAD`
- [x] the exact two-line string is intact, wrap and three-space indent included — stricter than the harness's `grep -F`
- [x] `The axis is` `` `.pearde/vision.md` `` is intact and `vision.py` is still absent

## Verify and Proof

```sh
M=references/parts/order.md

python3 resources/prose.py check "$M"

python3 resources/prose.py stat HEAD | grep "^$M:" \
  | awk '{ exit ($4+0 <= $2+0) ? 0 : 1 }'

python3 - "$M" <<'PY'
import sys
t = open(sys.argv[1]).read()
pin = "every child `done` — a parked\n   child holds its parent"
assert pin in t, "lost the two-line dispatchable pin"
assert "The axis is `.pearde/vision.md`" in t, "lost the vision.md pin"
assert "vision.py" not in t, "vision.py came back"
print("spec03: two-line pin, vision pin intact; vision.py absent")
PY
```
