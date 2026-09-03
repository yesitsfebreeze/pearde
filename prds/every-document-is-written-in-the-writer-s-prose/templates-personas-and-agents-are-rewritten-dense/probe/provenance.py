#!/usr/bin/env python3
"""A persona's two provenance lists still match, and its shape is intact.

A `## How you work` bullet closes with `[<Name>: <trait>]`; the matching
`## Built from` bullet repeats that trait character for character. A rewrite
that touches one copy and not the other breaks the file's own rule, and no
other check on this board reads it.

    provenance.py <persona.md>...      one line per file, exit 1 on a break
"""
import re
import sys

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
BRACKET = re.compile(r"^\s*\[([^:\]]+):\s*([^\]]+)\]\s*$", re.M)
BULLET = re.compile(r"^\s*- \*\*([^*]+)\*\* — .*?\. Trait: (.+?)\. Source: (.+)$", re.M)
REQUIRED = ("## How you work", "## Voice", "## Built from")
KEYS = ("name", "profession", "description")


def check(path):
    text = open(path, encoding="utf-8").read()
    bad = []

    fm = FM.match(text)
    if not fm:
        bad.append("no frontmatter")
    else:
        keys = tuple(l.split(":", 1)[0].strip()
                     for l in fm.group(1).splitlines() if ":" in l)
        if keys != KEYS:
            bad.append(f"frontmatter keys {keys}, want {KEYS}")

    for h in REQUIRED:
        if f"\n{h}\n" not in text:
            bad.append(f"no `{h}`")
    if any(f"\n{h}\n" not in text for h in REQUIRED):
        return bad

    how, built = text.split("## Built from", 1)
    brackets = BRACKET.findall(how)
    bullets = BULLET.findall(built)
    if not bullets:
        bad.append("no `## Built from` bullet in the prescribed shape")

    b_traits = {t.strip() for _, t, _ in bullets}
    h_traits = {t.strip() for _, t in brackets}
    for t in sorted(h_traits - b_traits):
        bad.append(f"trait in `## How you work` with no `## Built from` bullet: {t!r}")
    for t in sorted(b_traits - h_traits):
        bad.append(f"trait in `## Built from` backing no behaviour: {t!r}")

    names = {n.strip() for n, _, _ in bullets}
    for n in sorted({n.strip() for n, _ in brackets} - names):
        bad.append(f"bracket names nobody under `## Built from`: {n!r}")

    n_bullets = len(re.findall(r"^- \*\*", how, re.M))
    if not 3 <= n_bullets <= 6:
        bad.append(f"`## How you work` has {n_bullets} bullets, want 3-6")
    return bad


def main(argv):
    broken = 0
    for p in argv:
        bad = check(p)
        if bad:
            broken += 1
            print(f"{p}: {len(bad)} problem(s)")
            for b in bad:
                print(f"    {b}")
        else:
            print(f"{p}: provenance and shape ok")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
