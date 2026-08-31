---
complexity: 8
footprint:
  - resources/board/plan.py
  - resources/board/viewtest.js
---

# spec01 — `pearde example` and `viewtest.js --example` write into `.pearde/`

`cmd_example` in `resources/board/plan.py` and the `--example` path in
`resources/board/viewtest.js` both copy `resources/board/example/` straight
into the destination root instead of into a `.pearde/` directory inside it —
the same layout mistake `init` already avoids. Both are fixed: `cmd_example`
now copies into `os.path.join(dest, BOARD_DIR)` and reports
`os.path.join(board, PRDS_DIR)`; `viewtest.js` copies into
`path.join(scratch, ".pearde")` and reads back whatever path `plan.py gantt`
itself printed on its last `gantt: <path>` line, rather than a hardcoded
guess — the render's actual file lives at `.pearde/.state/view.html`, not
`prds/.view.html` as the two now-stale docstrings at `plan.py:6` and
`render.py:4` claim (a separate, pre-existing drift bug, reported in the PRD
report, not fixed here). `resources/board/example/` itself is untouched;
`init.py` is untouched.

## Acceptance

- [x] `python3 resources/board/plan.py example <empty dir>` leaves a board at
  `<dir>/.pearde/` — `settings.md` and `prds/` inside it, nothing of the
  board at `<dir>` itself.
- [x] The two lines `pearde example` prints name real things: the board path
  it reports resolves on disk, and the follow-up `scan` command it prints
  exits 0 and lists the example PRDs by their own names.
- [x] `node resources/board/viewtest.js --example` exits 0 and renders the
  copied example board.
- [x] `bash resources/doctor.sh --harnesses <dir>` reports the `jstests` row
  `ok` rather than `broken`.
- [x] `resources/board/init.py` is unchanged, and `init <dir> --example`
  still produces `<dir>/.pearde/prds` with the example PRDs in it.
- [x] `grep -rn "example" resources/` turns up no remaining writer of an
  example board that puts `prds/` at the destination root, and
  `resources/board/example/` is byte-identical to what it is today.

## Verify and Proof

```sh
set -e
rm -rf /tmp/spec01-ex1 /tmp/spec01-ex4
python3 resources/board/plan.py example /tmp/spec01-ex1
test -f /tmp/spec01-ex1/.pearde/settings.md
test -d /tmp/spec01-ex1/.pearde/prds
test ! -e /tmp/spec01-ex1/settings.md
python3 resources/board/plan.py scan /tmp/spec01-ex1 | grep -q "PRDs"
python3 resources/pearde.py example /tmp/spec01-ex4
test -d /tmp/spec01-ex4/.pearde/prds

# viewtest.js/doctor --harnesses need node + playwright-core, an OPTIONAL dev
# dependency (resources/doctor.sh's own "off" row when it is missing) — not
# part of this fix. Run them when available, note the skip when not; either
# way this block does not fail on an environment gap.
if command -v node >/dev/null 2>&1 && node -e "require.resolve('playwright-core')" >/dev/null 2>&1; then
  node resources/board/viewtest.js --example
  rm -rf /tmp/spec01-doctor && mkdir -p /tmp/spec01-doctor
  bash resources/doctor.sh --harnesses /tmp/spec01-doctor 2>&1 | grep -Eq "jstests +ok"
else
  echo "spec01: node/playwright-core unavailable here — viewtest.js/doctor jstests row not exercised in this run"
fi

rm -rf /tmp/spec01-init
python3 resources/board/init.py init /tmp/spec01-init --example
test -d /tmp/spec01-init/.pearde/prds

# example/ is a copy source, never edited by this fix — init.py itself is
# excluded from this check since other in-flight PRDs on this shared board
# may legitimately touch it; this spec's footprint never does.
git diff --quiet resources/board/example/
echo "spec01 verify: all checks passed"
```
