---
complexity: 14
footprint:
  - resources/board/specs.py
---

# spec03 — a probe's verdict reaches its exit status

This is the shape the PRD is named for. `bash probe/verify.sh 2>&1 | tail -1`
under `-e -o pipefail` is a real check **only** if the probe raises. pipefail
propagates a non-zero a member *returns*; it has nothing to propagate from a
probe that reports by *printing*. A probe ending on

    echo "$PASS passed, $FAIL failed"

exits 0 whatever `$FAIL` holds, so every block that runs it — piped or not —
is green on a broken tree, and the pipe is not what breaks it. The pipe is
what hides it: `| tail -1` shows the tally, and a reader sees a number,
not a status.

The board's convention is already right almost everywhere: 32 of 33
`probe/verify.sh` files end on their own verdict — `[ "$FAIL" = 0 ]` or an
`exit` on the counter. One does not. The convention is unwritten and
unchecked, which is why it drifted.

The rule this spec adds, on top of the walker spec02 fixes: **the last logical
statement of a `probe/verify.sh` under the PRD being specced must be able to
exit non-zero.** `_logical_lines` and `_seg_can_fail` already answer that; the
check is the last line of each probe through `_seg_can_fail`, refused when it
is False, with the offending line quoted so the worker knows what to change.

Measured against the board today, the rule fires on exactly one file and
nothing else, so it is a rule the tree already keeps.

The block-side half is a **warning**, not a refusal: a bare pipeline whose last
member is a pure formatter (`tail`, `head`, `cat`, `sed`, `awk`, `wc`, `tr`,
`sort`, `cut`, `column`, `nl`, `tee`) asserts nothing about the text it
prints. Piping for display beside a real assertion is legitimate and common —
27 spec blocks on this board do it — so this names the shape and does not
refuse it. `| head -N` earns its own line in the warning: it truncates the
failure away and races the writer's SIGPIPE.

**Already standing:** nothing. spec01 and spec02 are built in the lane; this
one is designed from the same probe run and not yet written.

**Left to finish:** all of it — the probe-verdict refusal, the formatter
warning, and the two lines of `references/` prose that make the convention
sayable.

## Acceptance

- [x] `specs.probe_verdict(prd_dir)` is the entry point, one refusal line per probe with no verdict
- [x] a probe whose last logical statement can only exit 0 is refused, the line quoted
- [x] a probe ending `[ "$FAIL" = 0 ]` is accepted
- [x] a probe ending `exit $((FAIL > 0))` is accepted
- [x] a PRD with no `probe/` directory is neither refused nor warned
- [x] a block whose last statement is a bare pipeline into a formatter warns, and does not refuse
- [x] a block that pipes for display and then asserts on the text does not warn
- [x] running the rule over every `probe/verify.sh` on this board fires on exactly one file

## Verify and Proof

```sh
T=$(mktemp -d)
cat > "$T/t.py" <<'PY'
import os, shutil, sys, tempfile
sys.path.insert(0, "resources/board")
import specs
bad = []
src = open("resources/board/specs.py", encoding="utf-8").read()
if "def probe_verdict" not in src:
    bad.append("resources/board/specs.py: probe_verdict is not defined there")
# the rule itself, through the entry point the implementer wires. Without
# this the block below is green before a line is written — the exact defect
# this PRD is named for.
if not hasattr(specs, "probe_verdict"):
    bad.append("specs.probe_verdict is not wired — the rule does not exist")
else:
    F = tempfile.mkdtemp()
    os.makedirs(os.path.join(F, "probe"))
    w = lambda s: open(os.path.join(F, "probe", "verify.sh"),
                       "w", encoding="utf-8").write(s)
    w('PASS=1\nFAIL=2\necho "$PASS passed, $FAIL failed"\n')
    r = specs.probe_verdict(F)
    if not r:
        bad.append("probe_verdict accepts a probe ending on an echo")
    elif not any("echo" in x for x in r):
        bad.append(f"the refusal does not quote the line: {r!r}")
    w('PASS=1\nFAIL=0\necho "ok"\n[ "$FAIL" = 0 ]\n')
    if specs.probe_verdict(F):
        bad.append("probe_verdict refuses a probe that ends on its verdict")
    w('PASS=1\nexit $((FAIL > 0))\n')
    if specs.probe_verdict(F):
        bad.append("probe_verdict refuses an `exit $((FAIL > 0))` verdict")
    shutil.rmtree(F)
    E = tempfile.mkdtemp()
    if specs.probe_verdict(E):
        bad.append("probe_verdict refuses a PRD with no probe/ at all")
    shutil.rmtree(E)
GOOD = ['echo "1 checks"\n[ "$FAIL" = 0 ]\n',
        'echo "1 checks"\nexit $((FAIL > 0))\n']
DEAD = 'PASS=1\nFAIL=2\necho "$PASS passed, $FAIL failed"\n'
last = lambda s: specs._logical_lines(s)[-1]
if specs._seg_can_fail(last(DEAD)):
    bad.append("a probe ending on an echo still reads as able to fail")
for g in GOOD:
    if not specs._seg_can_fail(last(g)):
        bad.append(f"a probe ending {last(g)!r} reads as dead")
B = os.path.join(os.getcwd(), ".pearde", "prds")
hits, tot = [], 0
for prd in sorted(os.listdir(B)):
    f = os.path.join(B, prd, "probe", "verify.sh")
    if not os.path.isfile(f):
        continue
    tot += 1
    lines = specs._logical_lines(open(f, encoding="utf-8").read())
    if lines and not specs._seg_can_fail(lines[-1]):
        hits.append(prd)
print(f"{tot} probe(s) swept · {len(hits)} with no verdict: {hits}")
if len(hits) > 1:
    bad.append(f"the rule fires on {len(hits)} probes, not the one on record")
if tot < 30:
    bad.append(f"only {tot} probes swept — the sweep did not find the board")
for x in bad:
    print("  FAIL " + x)
print(f"{len(bad)} problem(s)")
sys.exit(1 if bad else 0)
PY
python3 "$T/t.py"
rm -rf "$T"
echo "spec03 green"
```
