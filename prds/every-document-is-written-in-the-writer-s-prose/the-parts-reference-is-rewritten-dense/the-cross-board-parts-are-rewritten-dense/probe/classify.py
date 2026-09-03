#!/usr/bin/env python3
"""Split `prose.py`'s unbound-waste hits into the shape the rule targets and
the shape it catches by accident.

    classify.py <path>...   counts, then every hit under its class

The rule bans the vague-subject opener — `it is`, `this means`, `there are`
— where the pronoun opens a clause with no antecedent in reach. A hit sitting
mid-clause behind its own noun (`a board that is a worktree`) or behind a
preposition (`nothing of it is`) is a bound reading the same regex cannot
tell apart. The test is mechanical and stated, never a judgement per hit:

    subject   the hit opens the clause — start of a line, or straight after
              . ; : — ( or a comma
    bound     any other hit: a word runs ahead of it inside the clause

`subject` is the rule's real catch. `bound` is where a rewrite is forced to
reword correct English, and the count is what makes that cost visible.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD_ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 6))
for _r in (os.getcwd(), BOARD_ROOT):
    if os.path.isfile(os.path.join(_r, "resources", "prose.py")):
        sys.path.insert(0, os.path.join(_r, "resources"))
        break
else:
    sys.exit("classify.py: no resources/prose.py in the cwd or beside the probe")
import prose  # noqa: E402

OPENERS = set(".;:—(,")


def classify(text):
    body = "\n".join(prose.prose_lines(prose.strip_code(text)))
    out = []
    for word, off in prose.unbound_hits(text):
        before = body[:off].rstrip()
        kind = "subject" if not before or before[-1] in OPENERS else "bound"
        line = body[body.rfind("\n", 0, off) + 1:]
        line = line.split("\n")[0]
        out.append((kind, word, line.strip()))
    return out


def main(paths):
    tot = {"subject": 0, "bound": 0}
    rows = []
    for path in paths:
        c = classify(open(path).read())
        n = {"subject": 0, "bound": 0}
        for kind, _, _ in c:
            n[kind] += 1
            tot[kind] += 1
        rows.append((path, n["subject"], n["bound"]))
        for kind, word, line in c:
            print(f"  {kind:8} [{word}] {line}")
    print()
    print(f"{'file':34} {'subject':>8} {'bound':>6} {'total':>6}")
    for path, s, b in rows:
        print(f"{path:34} {s:8} {b:6} {s + b:6}")
    t = tot["subject"] + tot["bound"]
    print(f"{'TOTAL':34} {tot['subject']:8} {tot['bound']:6} {t:6}")
    if t:
        print(f"bound share: {tot['bound'] / t:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
