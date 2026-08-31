#!/usr/bin/env python3
"""Probe: apply the specific-rule table (and the prds/<name>/ pattern rule)
to the scoped prose files, then report every remaining bare `prds/`
occurrence for manual review. Run from the repo root
(/Users/feb/dev/infra/pearde), e.g.:

    python3 .pearde/prds/every-document-names-the-path-the-board-is-on/probe/migrate.py
    python3 .../migrate.py --apply

Specific rules run before the generic one; there IS no generic mechanical
rule for a bare `prds/` -- the PRD says each is read and decided by hand.
"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/feb/dev/infra/pearde")
SCOPE_FILE = Path("/tmp/scope_files.txt")

# Longest/most-specific first -- applied top to bottom, plain substring.
RULES = [
    ("prds/knowledge/", ".pearde/wiki/"),
    ("prds/.plan.json", ".pearde/.state/plan.json"),
    ("prds/.round.md", ".pearde/.state/round.md"),
    ("prds/.history.jsonl", ".pearde/.state/history.jsonl"),
    ("prds/.transitions.jsonl", ".pearde/.state/transitions.jsonl"),
    ("prds/.view.html", ".pearde/.state/view.html"),
    ("prds/memos/", ".pearde/memos/"),
    ("prds/workflows/", ".pearde/workflows/"),
    ("prds/settings.md", ".pearde/settings.md"),
    ("prds/vision.md", ".pearde/vision.md"),
]

# prds/<name>/ -> .pearde/prds/<name>/ -- applied after the literal rules
# above (which already consumed the special subpaths), so what is left
# matching this is a real PRD-dir reference.
PRD_NAME_RE = re.compile(r"prds/([A-Za-z0-9][\w.-]*)/")


def load_scope():
    return [ROOT / line.strip() for line in SCOPE_FILE.read_text().splitlines() if line.strip()]


def apply_specific(text):
    for old, new in RULES:
        text = text.replace(old, new)
    return text


def apply_prd_name_rule(text):
    return PRD_NAME_RE.sub(lambda m: f".pearde/prds/{m.group(1)}/", text)


def main():
    dry = "--apply" not in sys.argv
    files = load_scope()
    total_before = total_after = 0
    bare_report = []
    for f in files:
        if not f.exists():
            print(f"MISSING: {f}", file=sys.stderr)
            continue
        text = f.read_text()
        before = len(re.findall(r"prds/", text))
        total_before += before
        new_text = apply_prd_name_rule(apply_specific(text))
        after = len(re.findall(r"prds/", new_text))
        total_after += after
        if after:
            for m in re.finditer(r".{0,40}prds/.{0,40}", new_text):
                bare_report.append((str(f.relative_to(ROOT)), m.group(0)))
        if not dry and new_text != text:
            f.write_text(new_text)
    print(f"prds/ occurrences before: {total_before}")
    print(f"prds/ occurrences after specific+name rules: {total_after}")
    print(f"bare occurrences left for manual read: {len(bare_report)}")
    for fname, ctx in bare_report:
        print(f"  {fname}: ...{ctx}...")


if __name__ == "__main__":
    main()
