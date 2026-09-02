#!/usr/bin/env python3
"""Check density — word count, mean sentence length, unbound waste words and
banned openers/closers, per file. The only reader of @references/language.md's
`## Density` section.

    prose.py stat [ref]        word count per tracked `.md` file and the tree
                                total; a `ref` (a commit-ish) diffs each file's
                                count there against the working tree — before,
                                then after
    prose.py check [path...]   one line per violation, silent and exit 0 when
                                clean; every tracked `.md` file when no path is
                                given

A fact set is a table, a sequence a list — neither carries sentences of its
own, so a heading, a table row, a bullet and a blockquote marker are read as
structure, never as prose. `stat`'s word count excludes fenced and inline
code; `check`'s sentence count excludes them too.

Four checks, from the four mechanical rules in `## Density`:

    mean sentence length     over MEAN_SENTENCE_MAX words average — the
                              `~twenty words a sentence, on average` rule
    unbound waste word       `it`, `this`, `that` or `there` immediately
                              followed by a linking verb or nothing — the
                              vague-subject shape (`it is`, `this means`,
                              `there are`) the rule bans, never the bound one
                              (`this file`, `read it`)
    banned opener             the file's first prose line opens on a listed
                              preamble phrase
    banned closer              the file's last prose line closes on a listed
                              recap phrase

The five rules that are not mechanical here — lead with the answer, a heading
summarises what is beneath it, cut twice, a fact set is a table, reference
describes never teaches, emphasis earns its place — read as argument, not as
a pattern a regex can hold, and are a person's to judge.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

MEAN_SENTENCE_MAX = 24  # "about twenty words a sentence, on average"

WASTE_RE = re.compile(r"\b(it|this|that|there)\b", re.I)
# Bound when the next word names a noun ("this file") or the pronoun sits in
# object position ("read it"); unbound when what follows is a linking verb or
# nothing at all — the vague-subject shape the rule bans.
UNBOUND_FOLLOW = {"is", "are", "was", "were", "'s", "means", "should",
                  "would", "could", "can", "will", "must", "seems", "looks"}

BANNED_OPENERS = (
    "this document", "this section", "this file", "in this section",
    "as mentioned", "note that", "it is worth noting", "it should be noted",
    "as we can see", "let's take a look", "let's start",
)
BANNED_CLOSERS = (
    "in conclusion", "to summarize", "to sum up", "in summary",
    "that's all", "and that's it", "as we have seen", "hopefully this helps",
)


def strip_code(text):
    text = FENCE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return text


def prose_lines(text):
    """Paragraph-shaped lines — not a heading, table row, bullet or
    blockquote, none of which carries a sentence of its own."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "|", "-", "*", ">")):
            continue
        out.append(s)
    return out


def sentences(text):
    out = []
    for line in prose_lines(strip_code(text)):
        out += [p for p in SENT_SPLIT.split(line) if p.strip()]
    return out


def word_count(text):
    return len(strip_code(text).split())


def mean_sentence_length(text):
    lens = [len(s.split()) for s in sentences(text)]
    return sum(lens) / len(lens) if lens else 0.0


def unbound_hits(text):
    """A pronoun bound to an object position ("read it", "do it") or
    followed by its own noun ("this file") is never flagged — only the
    vague-subject shape, where a linking verb follows with no noun between.
    Scanned over prose lines only — a table cell or a heading is structure,
    never a sentence with a subject to bind."""
    body = "\n".join(prose_lines(strip_code(text)))
    hits = []
    for m in WASTE_RE.finditer(body):
        rest = body[m.end():].lstrip(" \t")
        nxt = rest.split(None, 1)[0].strip(".,;:!?()\"'").lower() if rest else ""
        if nxt in UNBOUND_FOLLOW:
            hits.append((m.group(1).lower(), m.start()))
    return hits


def banned_phrase(text, phrases, at_end):
    lines = prose_lines(strip_code(text))
    if not lines:
        return None
    low = (lines[-1] if at_end else lines[0]).lower()
    return next((p for p in phrases if p in low), None)


def tracked_md():
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "*.md"],
        capture_output=True, text=True, check=True).stdout
    return [p for p in out.splitlines() if p]


def stat(argv):
    ref = argv[0] if argv else None
    total_after = 0
    total_before = 0
    for f in sorted(tracked_md()):
        after = word_count(open(os.path.join(ROOT, f), encoding="utf-8").read())
        total_after += after
        if ref:
            got = subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{f}"],
                                  capture_output=True, text=True)
            before = word_count(got.stdout) if got.returncode == 0 else 0
            total_before += before
            print(f"{f}: {before} -> {after}")
        else:
            print(f"{f}: {after}")
    if ref:
        pct = (100 * (total_before - total_after) / total_before) if total_before else 0.0
        print(f"total: {total_before} -> {total_after} ({pct:.1f}% cut)")
    else:
        print(f"total: {total_after}")
    return 0


def check(argv):
    files = argv or tracked_md()
    problems = []
    for f in files:
        p = f if os.path.isabs(f) else os.path.join(ROOT, f)
        rel = os.path.relpath(p, ROOT)
        if not os.path.isfile(p):
            problems.append(f"{rel}: not on disk")
            continue
        text = open(p, encoding="utf-8", errors="replace").read()
        m = mean_sentence_length(text)
        if m > MEAN_SENTENCE_MAX:
            problems.append(
                f"{rel}: mean sentence length {m:.1f} words, over {MEAN_SENTENCE_MAX}")
        hits = unbound_hits(text)
        if hits:
            words = ", ".join(sorted({w for w, _ in hits}))
            problems.append(f"{rel}: {len(hits)} unbound waste word(s) ({words})")
        opener = banned_phrase(text, BANNED_OPENERS, at_end=False)
        if opener:
            problems.append(f'{rel}: banned opener — "{opener}"')
        closer = banned_phrase(text, BANNED_CLOSERS, at_end=True)
        if closer:
            problems.append(f'{rel}: banned closer — "{closer}"')
    if problems:
        print("\n".join(problems))
    return 1 if problems else 0


def main(argv):
    cmd = argv[1] if len(argv) > 1 else None
    if cmd == "stat":
        return stat(argv[2:])
    if cmd == "check":
        return check(argv[2:])
    print(__doc__.strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
