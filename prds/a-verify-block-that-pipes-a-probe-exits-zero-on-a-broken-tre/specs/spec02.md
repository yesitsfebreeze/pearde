---
complexity: 10
footprint:
  - resources/board/specs.py
---

# spec02 — the cannot-fail walker reads what the block actually says

`_cannot_fail_why` is the one gate between a dead verify block and a green
PRD, and its tokeniser mis-reads two shapes that nearly every block on this
board contains. Both mis-reads fail in the permissive direction: the walker
concludes "something here can go red" about text it never parsed.

**`$((` read as `$(`.** `_seg_can_fail` decides a bare assignment is fallible
when it holds a command substitution, testing `re.search(r"\$\(|`", s)`. That
pattern matches the arithmetic expansion `$((N+1))`, which runs no command and
can leave no status. So the counter idiom

    N=0
    bash probe.sh | tail -1 | grep -qE '0 fail$' || N=$((N+1))
    echo "$N problem(s)"

is accepted: the walker thinks `N=$((N+1))` can abort. It cannot. The block
ends on an `echo`, every fallible command sits behind `||`, and it is green on
a broken tree — measured, exit 0, printing `1 problem(s)`.

**`2>&1` split at the `&`.** `_segments` treats an unquoted `&` at depth 0 as
a list boundary without looking at what precedes it, so `bash probe.sh 2>&1 |
tail -1` is parsed as two statements — `bash probe.sh 2>` and a pipeline whose
first member is the word `1`. The walker's whole analysis of any block using
`2>&1` is an analysis of text the block does not contain.

**Already standing:** both fixes are in the lane. `_seg_can_fail` now tests
`r"\$\((?!\()|`"`; `_segments` keeps the `&` in `cur` when the segment so far
ends in `>` or `<`, and when the `&` is itself opening `&>`. The counter idiom
above is now refused with the fallback named, and `_segments` returns one
statement for `bash p.sh 2>&1 | tail -1`, two for `a && b`, two for `a & b`.

**Left to finish:** land it. Re-run the census below: no verify block standing
on this board is newly refused by either fix, so this is a correction with no
migration behind it.

## Acceptance

- [x] `_seg_can_fail("N=$((N+1))")` is False and `_seg_can_fail("N=$(cmd)")` is True
- [x] `_cannot_fail_why` refuses the counter block above, naming the `||` fallback
- [x] `_segments("bash p.sh 2>&1 | tail -1")` yields one statement, two pipeline members
- [x] `_segments` still splits `a && b`, `a & b` and `a; b` into two
- [x] `cmd >&2` and `cmd &>out.txt` stay one segment
- [x] no verify block already on the board is refused by the patched walker

## Verify and Proof

```sh
T=$(mktemp -d)
cat > "$T/t.py" <<'PY'
import os, re, sys
sys.path.insert(0, "resources/board")
import specs
bad = []
src = open("resources/board/specs.py", encoding="utf-8").read()
if "$\\((?!\\()" not in src:
    bad.append("resources/board/specs.py: the $(( guard is not in the source")
if specs._seg_can_fail("N=$((N+1))"):
    bad.append("$(( still read as a command substitution")
if not specs._seg_can_fail("N=$(cmd)"):
    bad.append("a real command substitution stopped counting")
COUNTER = ("N=0\n"
           "bash probe.sh | tail -1 | grep -qE '0 fail$' || N=$((N+1))\n"
           'echo "$N problem(s)"\n')
why = specs._cannot_fail_why(COUNTER)
if not why:
    bad.append("the counter block is still accepted")
elif "fallback" not in why:
    bad.append(f"the refusal does not name the fallback: {why!r}")
cases = [("bash p.sh 2>&1 | tail -1", 2, ["", "|"]),
         ("a && b", 2, ["", "&&"]),
         ("a & b", 2, ["", "&"]),
         ("a; b", 2, ["", ";"]),
         ("cmd >&2", 1, [""]),
         ("cmd &>out.txt", 1, [""])]
for line, n, ops in cases:
    got = specs._segments(line)
    if len(got) != n or [o for o, _ in got] != ops:
        bad.append(f"_segments({line!r}) -> {got!r}")
B = os.path.join(os.getcwd(), ".pearde", "prds")
refused = []
for prd in sorted(os.listdir(B)):
    sd = os.path.join(B, prd, "specs")
    if not os.path.isdir(sd):
        continue
    for f in sorted(os.listdir(sd)):
        if not f.endswith(".md"):
            continue
        t = open(os.path.join(sd, f), encoding="utf-8").read()
        m = re.search(r"^## Verify and Proof\s*$(.*?)(?=^## |\Z)", t,
                      re.M | re.S)
        if not m:
            continue
        b = re.search(r"^```[a-z]*\s*$(.*?)^```\s*$", m.group(1), re.M | re.S)
        if b and specs._cannot_fail_why(b.group(1)):
            refused.append(f"{prd}/specs/{f}")
if refused:
    bad.append(f"{len(refused)} standing block(s) newly refused: "
               f"{refused[:3]}")
print(f"checked {len(cases) + 4} shapes")
for x in bad:
    print("  FAIL " + x)
print(f"{len(bad)} problem(s)")
sys.exit(1 if bad else 0)
PY
python3 "$T/t.py"
rm -rf "$T"
echo "spec02 green"
```
