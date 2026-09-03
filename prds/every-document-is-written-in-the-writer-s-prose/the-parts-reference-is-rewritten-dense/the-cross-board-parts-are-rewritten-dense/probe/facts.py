#!/usr/bin/env python3
"""The fact set of a markdown file, and the diff of one against a git ref.

A fact is anything a rewrite may not silently drop: an inline-code span, a
non-blank line inside a fence, an @path or @@keyword handle, and every cell
of every table row. Prose is not a fact — the rewrite is free there.

    facts.py show <path>            one fact per line
    facts.py diff <ref> <path>...   what the working tree lost against <ref>

`diff` exits 1 on any loss.
"""
import re, subprocess, sys, collections

CODE = re.compile(r"`([^`\n]+)`")
HANDLE = re.compile(r"@@?[A-Za-z0-9_./<>-]+")


def facts(text):
    out = []
    fence = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            if s:
                out.append(("fence", s))
            continue
        for m in CODE.finditer(line):
            out.append(("code", m.group(1).strip()))
        for m in HANDLE.finditer(CODE.sub(" ", line)):
            out.append(("handle", m.group(0)))
        if s.startswith("|") and s.endswith("|") and set(s) - set("|- :"):
            for cell in s.strip("|").split("|"):
                c = CODE.sub(lambda m: m.group(1), cell).strip()
                if c:
                    out.append(("cell", c))
    return out


def at_ref(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"],
                       capture_output=True, text=True)
    if r.returncode:
        return None
    return r.stdout


def main(argv):
    if len(argv) >= 2 and argv[0] == "show":
        for kind, f in facts(open(argv[1]).read()):
            print(f"{kind}\t{f}")
        return 0
    if len(argv) >= 3 and argv[0] == "diff":
        ref, lost_total = argv[1], 0
        for path in argv[2:]:
            old = at_ref(ref, path)
            if old is None:
                print(f"{path}: not at {ref}")
                continue
            was = collections.Counter(f for _, f in facts(old))
            now = collections.Counter(f for _, f in facts(open(path).read()))
            lost = was - now
            gained = sum((now - was).values())
            n = sum(lost.values())
            lost_total += n
            print(f"{path}: {sum(was.values())} -> {sum(now.values())} "
                  f"facts, {n} lost, {gained} new")
            for f, c in sorted(lost.items()):
                print(f"    lost x{c}: {f}")
        return 1 if lost_total else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
