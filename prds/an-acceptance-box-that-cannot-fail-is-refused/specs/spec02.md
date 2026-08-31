---
complexity: 10
footprint:
  - resources/board/specs.py
---

# spec02 — the refusal message is actionable and the gate survives a real check run

A refusal a worker cannot act on is no better than a silent pass. The call
site already stands in `check_spec` (`resources/board/specs.py`, the
`verify block <N> cannot fail — <why>` append near line 531): this spec
records that the message names the block position and the shape that made
it unable to fail, not just the fact of the refusal, and that the whole
gate — walker plus call site — survives being exercised the way `specced`
itself is: `--check`, refusing, writing nothing to disk. Nothing further is
to be built; this closes out the second half of the report's "What is left".

## Acceptance

- [x] the refusal message for a guarded block names which block (`verify
  block <N>`) — a spec with two `sh` blocks, one live and one guarded,
  produces a message pointing at the guarded one's number, not the live
  one's
- [x] the refusal message states the shape, not just "cannot fail" bare —
  quoting or naming the guard pattern (e.g. the trailing always-0 command,
  or the `!` inversion) so a worker reading it knows what to change
- [x] running the gate end to end — build a spec file in a fixture
  directory made at run time, call `check_spec` on it — refuses the
  guarded version and writes nothing, then accepts the same file after its
  last statement is replaced with a live one, matching how `specced`
  itself is invoked (never against a real PRD under `.pearde/prds/`)
- [x] the probe's gate fixture (the `check_spec` round-trip in
  `probe/verify.sh`) still passes against the code as it stands now, not
  just as it stood when the walker was first built

## Verify and Proof

```sh
bash .pearde/prds/an-acceptance-box-that-cannot-fail-is-refused/probe/verify.sh
python3 - resources/board/specs.py <<'PYEND'
import importlib.util, os, sys, tempfile
s = importlib.util.spec_from_file_location("specs", sys.argv[1])
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
F = chr(96) * 3
head = ("---\ncomplexity: 5\nfootprint:\n  - resources/board/specs.py\n---\n"
        "# spec02 - fixture\n\n## Acceptance\n\n"
        "- [ ] a check that can fail\n\n## Verify and Proof\n\n")
live = F + "sh\npython3 -c 'import sys; sys.exit(1)'\n" + F + "\n\n"
dead = F + "sh\ngrep -q p resources/board/specs.py || true\necho done\n" + F
fixed = F + ("sh\ngrep -q p resources/board/specs.py || true\n"
             "python3 -c 'import sys; sys.exit(1)'\n") + F
d = tempfile.mkdtemp()
p = os.path.join(d, "spec02.md")
text = head + live + dead + "\n"
open(p, "w", encoding="utf-8").write(text)
before = sorted(os.listdir(d))
fm, _b, _c = m.plan.parse_prd(p)
bad, _w, _f = m.check_spec(p, fm, text, {}, [])
msgs = [t for _ln, t in bad if "cannot fail" in t]
wrong = []
if len(msgs) != 1:
    wrong.append("expected one refusal, got %d" % len(msgs))
if not all(t.startswith("verify block 2") for t in msgs):
    wrong.append("the refusal does not name the guarded block's number")
if not all("|| true" in t for t in msgs):
    wrong.append("the refusal does not name the guard shape")
if sorted(os.listdir(d)) != before:
    wrong.append("the gate wrote to the fixture directory")
bad2, _w, _f = m.check_spec(p, fm, head + live + fixed + "\n", {}, [])
if any("cannot fail" in t for _ln, t in bad2):
    wrong.append("the repaired block is still refused")
for t in msgs:
    print("  " + t)
print("spec02: 5 checks over resources/board/specs.py, %d wrong" % len(wrong))
for w in wrong:
    print("  " + w)
raise SystemExit(1 if wrong else 0)
PYEND
```
