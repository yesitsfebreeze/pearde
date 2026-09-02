#!/usr/bin/env python3
"""Check that every roster persona is a sourced composite.

One row per check, `ok` or `FAIL`, then a tally line `<n> checks, <p> pass,
<f> fail`. Exit 1 on any failure.

The grammar it enforces, per `@references/personas/<id>.md`:

- `## Built from` exists once, with at least three bullets.
- Each bullet reads `- **<Name>** — <known for>. Trait: <trait>. Source: <src>.`
- That `<src>` names a year — a shape check, not a proof the artefact exists.
- Each `## How you work` bullet ends its final line with `[<Name>: <trait>]`.
- That `<Name>` is a person in `## Built from`, and that `<trait>` is that
  person's trait, character for character.
- The opening paragraph's first line carries the word `composite`.
- No third-person pronoun for the persona anywhere in the body.

Run: python3 .pearde/prds/the-four-personas-are-built-from-research/probe/check_personas.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PERSONAS = ROOT / "references" / "personas"
IDS = ["engineer", "designer", "mentor", "skeptic"]

BUILT = re.compile(
    r"^- \*\*(?P<name>[^*]+)\*\* — (?P<known>.+?)\. "
    r"Trait: (?P<trait>.+?)\. Source: (?P<source>.+?)\.\s*$"
)
MARK = re.compile(r"\[(?P<name>[^\[\]:]+): (?P<trait>[^\[\]]+)\]")
# Gendered singular pronouns only — a persona assumes no gender. Generic
# `they` for the user is correct prose and is not flagged.
YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
PRONOUN = re.compile(r"\b(he|she|him|her|his|hers|herself|himself)\b", re.I)

rows = []


def check(ok, label):
    rows.append((bool(ok), label))
    return bool(ok)


def sections(body):
    """{heading: [lines]} for one `## ` level."""
    out, cur = {}, None
    for line in body.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return out


def bullets(lines):
    """Group `- ` lines with their continuations."""
    out = []
    for line in lines:
        if line.startswith("- "):
            out.append([line])
        elif out and line.strip() and line.startswith("  "):
            out[-1].append(line)
    return out


def one(pid):
    path = PERSONAS / f"{pid}.md"
    if not check(path.is_file(), f"{pid}: file exists"):
        return
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if not check(len(parts) == 3 and parts[0] == "", f"{pid}: frontmatter parses"):
        return
    front, body = parts[1], parts[2]

    keys = [m for m in re.findall(r"^([a-z-]+):", front, re.M)]
    check(keys == ["name", "profession", "description"], f"{pid}: three frontmatter keys")

    opening = body.strip().splitlines()[0] if body.strip() else ""
    check("composite" in opening.lower(), f"{pid}: first line says composite")

    sec = sections(body)
    for head in ("How you work", "Voice", "Built from"):
        check(head in sec, f"{pid}: has `## {head}`")
    check(body.count("\n## Built from\n") == 1, f"{pid}: one `## Built from`")
    if "Built from" not in sec or "How you work" not in sec:
        return

    people = {}
    bf = bullets(sec["Built from"])
    check(len(bf) >= 3, f"{pid}: at least three practitioners ({len(bf)})")
    for b in bf:
        flat = " ".join(x.strip() for x in b)
        m = BUILT.match(flat)
        if not check(m, f"{pid}: Built-from bullet parses — {flat[:56]!r}"):
            continue
        people[m.group("name")] = m.group("trait")
        src = m.group("source")
        # A length bar passes a placeholder: `<the artefact>.` is 15
        # characters. A citation names the year of the artefact, which
        # no placeholder carries. It still proves only the shape of a
        # source, never that the artefact exists — see the report.
        check(bool(YEAR.search(src)),
              f"{pid}: {m.group('name')}'s source names a year — {src[:44]!r}")

    hw = bullets(sec["How you work"])
    check(3 <= len(hw) <= 6, f"{pid}: 3-6 `How you work` bullets ({len(hw)})")
    used = set()
    for b in hw:
        flat = " ".join(x.strip() for x in b)
        lead = flat[:44]
        # A bullet may carry more than one trace; every one of them is checked.
        marks = list(MARK.finditer(flat))
        if not check(marks, f"{pid}: bullet carries a trace — {lead!r}"):
            continue
        for m in marks:
            name, trait = m.group("name"), m.group("trait")
            used.add(name)
            if not check(name in people, f"{pid}: {name!r} is under Built from — {lead!r}"):
                continue
            check(people[name] == trait, f"{pid}: trait matches Built from — {lead!r}")

    orphan = sorted(set(people) - used)
    check(not orphan, f"{pid}: every practitioner backs a bullet — orphans {orphan}")

    bad = sorted({m.group(0) for m in PRONOUN.finditer(body)})
    check(not bad, f"{pid}: no third-person pronoun — found {bad}")


def index():
    path = PERSONAS / "INDEX.md"
    text = path.read_text(encoding="utf-8")
    check("written, not researched" not in text,
          "INDEX.md: no 'written, not researched' claim")
    check("Built from" in text, "INDEX.md: still documents `## Built from`")
    for pid in IDS:
        check(f"`{pid}`" in text, f"INDEX.md: roster row for `{pid}`")


for pid in IDS:
    one(pid)
index()

for ok, label in rows:
    print(f"{'ok  ' if ok else 'FAIL'} {label}")
npass = sum(1 for ok, _ in rows if ok)
print(f"{len(rows)} checks, {npass} pass, {len(rows) - npass} fail")
sys.exit(0 if npass == len(rows) else 1)
