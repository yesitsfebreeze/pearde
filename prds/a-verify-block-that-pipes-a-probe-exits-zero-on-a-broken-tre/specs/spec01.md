---
complexity: 8
footprint:
  - resources/board/collect.py
---

# spec01 — the block is an argument, never bash's stdin

`collect.run` hands the verify block to `bash -e -o pipefail` on **stdin**
(`subprocess.run(..., input=script)`). Bash reads a stdin script statement by
statement, so the first command in the block that reads stdin with no file
operand and no redirect — a bare `cat`, `grep PAT`, `sort`, `wc`, a `python3 -`
— consumes the **rest of the block**. Every statement after it never runs, and
bash exits with the status of the last statement it did reach, which is a 0.
collect records that as green.

Measured, on a broken tree, under `-e -o pipefail`:

    bash -c 'echo "3 passed, 2 failed"' | tail -1
    cat
    bash -c 'echo "3 passed, 2 failed"' | grep -q '0 failed'
    echo reached-the-end

exit 0 — and the two lines after `cat` come back on **stdout**, printed by
`cat`, rather than run. The assertion never executed. Passing the same block
as an argument with stdin closed gives exit 1.

The board already carries hand-written `</dev/null` on four probe calls in
`upgrade-leaves-the-memo-index-stale/specs/spec01.md`, which is this trap
being worked around one call at a time instead of closed once.

**Already standing:** the change is in the lane
(`resources/board/collect.py`, `run()`): when `script` is not None the block
goes in as `+ ["-c", script]` with `stdin=subprocess.DEVNULL`, and the no-script
branch closes stdin too. The sibling harness
`a-verify-block-must-not-destroy-the-checkout-it-runs-in/probe/verify.sh` runs
24 passed, 0 failed against the patched lane.

**Left to finish:** land it, and keep the comment that says why stdin is closed.

## Acceptance

- [x] `collect.run` passes the script as a `-c` argument, not as `input=`
- [x] `collect.run` closes stdin on both branches — with a script and without
- [x] a block whose assertion sits behind a bare `cat` exits non-zero on a broken tree
- [x] the same block still exits 0 on a tree that is not broken
- [x] `a-verify-block-must-not-destroy-the-checkout-it-runs-in/probe/verify.sh` still ends `0 failed`

## Verify and Proof

```sh
T=$(mktemp -d)
cat > "$T/t.py" <<'PY'
import sys
sys.path.insert(0, "resources/board")
import collect
BROKEN = ("bash -c 'echo \"3 passed, 2 failed\"' | tail -1\n"
          "cat\n"
          "bash -c 'echo \"3 passed, 2 failed\"' | grep -q '0 failed'\n"
          "echo reached-the-end\n")
CLEAN = BROKEN.replace("2 failed", "0 failed")
bad = []
c, o = collect.run(["bash", "-e", "-o", "pipefail"], ".", BROKEN)
if c == 0:
    bad.append(f"broken tree went green: exit {c} out={o!r}")
if "grep -q" in o:
    bad.append("the block was echoed, not run — still on stdin")
c2, o2 = collect.run(["bash", "-e", "-o", "pipefail"], ".", CLEAN)
if c2 != 0:
    bad.append(f"clean tree went red: exit {c2} out={o2!r}")
src = open("resources/board/collect.py", encoding="utf-8").read()
if "input=script" in src:
    bad.append("collect.run still feeds the block on stdin")
if src.count("stdin=subprocess.DEVNULL") < 2:
    bad.append("stdin is not closed on both branches of run()")
for b in bad:
    print("  FAIL " + b)
print(f"{len(bad)} problem(s)")
sys.exit(1 if bad else 0)
PY
python3 "$T/t.py"
rm -rf "$T"
PEARDE_TREE="$PWD" bash .pearde/prds/a-verify-block-must-not-destroy-the-checkout-it-runs-in/probe/verify.sh </dev/null > "$PWD/.guard.out" 2>&1
tail -1 "$PWD/.guard.out"
grep -qE '^[0-9]+ passed, 0 failed$' "$PWD/.guard.out"
rm -f "$PWD/.guard.out"
echo "spec01 green"
```
