#!/usr/bin/env python3
"""No fact lost — the tokens a dense rewrite must carry over from a ref.

    facts.py <ref> <path.md>...   one line per token in <ref>:<path> that the
                                  working tree's <path> no longer holds;
                                  silent and exit 0 when none is lost

A fact is a token a rewrite may not drop: an inline-code span, a fenced block
line, an `@path` or `@@keyword` reference, a table row's cells, a heading's
text. Prose is not a fact — the rewrite exists to cut prose.
"""
import re
import subprocess
import sys

FENCE = re.compile(r"```(.*?)```", re.S)
INLINE = re.compile(r"`([^`\n]+)`")
REF = re.compile(r"@@?[A-Za-z0-9_./-]+")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def tokens(text):
    """The fact set of one markdown document, by kind."""
    out = set()
    for body in FENCE.findall(text):
        for line in body.splitlines():
            if norm(line):
                out.add(("fence", norm(line)))
    for span in INLINE.findall(text):
        out.add(("code", norm(span)))
    for ref in REF.findall(text):
        out.add(("ref", ref))
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and set(s) - set("|-: "):
            for cell in s.strip("|").split("|"):
                c = norm(INLINE.sub(r"\1", cell))
                if c:
                    out.add(("cell", c))
        elif s.startswith("#"):
            out.add(("head", norm(s.lstrip("# "))))
    return out


def at_ref(ref, path):
    got = subprocess.run(["git", "show", f"{ref}:{path}"],
                         capture_output=True, text=True)
    if got.returncode != 0:
        print(f"{path}: not at {ref}", file=sys.stderr)
        return None
    return got.stdout


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    ref, paths = argv[1], argv[2:]
    lost_total = 0
    for path in paths:
        before = at_ref(ref, path)
        if before is None:
            lost_total += 1
            continue
        try:
            after = open(path, encoding="utf-8").read()
        except OSError:
            print(f"{path}: not on disk")
            lost_total += 1
            continue
        was, now = tokens(before), tokens(after)
        lost = sorted(was - now)
        # A cell or heading whose exact text moved into a code span or a
        # sentence still stands; only a token absent from the whole new text
        # in any form is lost.
        flat = norm(INLINE.sub(r"\1", after))
        lost = [(k, v) for k, v in lost if v not in flat]
        for kind, val in lost:
            print(f"{path}: lost {kind} — {val}")
        lost_total += len(lost)
    return 1 if lost_total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
