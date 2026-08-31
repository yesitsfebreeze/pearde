#!/usr/bin/env python3
"""Apply the specific-rule table (plus the found extras: `.claims/`,
`report.md`, `view.user.css`/`.js`, bare `prds/knowledge`) and the generic
`prds/<name>/` pattern (identifiers, `<placeholder>`/`{placeholder}` tokens,
and `*`/`**` globs) across the scoped files, EXCEPT `resources/guard.py` and
`resources/doctor.sh`, which are hand-edited because some of their `prds/`
text describes board-detection code that has not itself been migrated (see
report). Run from the repo root:

    python3 .../probe/apply.py            # dry run, prints before/after counts
    python3 .../probe/apply.py --apply    # writes the files
"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/feb/dev/infra/pearde")
SCOPE_FILE = Path("/tmp/scope_files.txt")
HAND_EDITED = {"resources/guard.py", "resources/doctor.sh"}

# Literal rules, longest/most-specific first. Order matters only in that a
# rule with a trailing slash must run before any bare variant of the same
# name (so the bare rule doesn't eat the slash-suffixed occurrences first).
RULES = [
    ("prds/knowledge/", ".pearde/wiki/"),
    ("prds/.plan.json", ".pearde/.state/plan.json"),
    ("prds/.round.md", ".pearde/.state/round.md"),
    ("prds/.history.jsonl", ".pearde/.state/history.jsonl"),
    ("prds/.transitions.jsonl", ".pearde/.state/transitions.jsonl"),
    ("prds/.view.html", ".pearde/.state/view.html"),
    ("prds/.claims/", ".pearde/.claims/"),          # extra: collect.py/transitions.py join this off `board` directly
    ("prds/memos/", ".pearde/memos/"),
    ("prds/workflows/", ".pearde/workflows/"),
    ("prds/settings.md", ".pearde/settings.md"),
    ("prds/vision.md", ".pearde/vision.md"),
    ("prds/report.md", ".pearde/report.md"),        # extra: serve.py
    ("prds/view.user.css", ".pearde/view.user.css"),  # extra: render.py
    ("prds/view.user.js", ".pearde/view.user.js"),    # extra: render.py
    ("prds/knowledge", ".pearde/wiki"),             # extra: bare, no trailing slash -- run after the slash rule above
]

NAME_TOKEN = r"(?:[A-Za-z0-9][\w.-]*|<[^>/]+>|\{[^}/]+\}|\*\*|\*)"
PRD_NAME_RE = re.compile(r"prds/(" + NAME_TOKEN + r")/")


def apply_specific(text):
    for old, new in RULES:
        text = text.replace(old, new)
    return text


def apply_prd_name_rule(text):
    return PRD_NAME_RE.sub(lambda m: f".pearde/prds/{m.group(1)}/", text)


def load_scope():
    return [ROOT / line.strip() for line in SCOPE_FILE.read_text().splitlines() if line.strip()]


def main():
    dry = "--apply" not in sys.argv
    files = load_scope()
    total_before = total_after = 0
    bare = []
    for f in files:
        rel = str(f.relative_to(ROOT))
        if rel in HAND_EDITED:
            continue
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
            for m in re.finditer(r".{0,30}prds/.{0,30}", new_text):
                bare.append((rel, m.group(0)))
        if not dry and new_text != text:
            f.write_text(new_text)
    print(f"[automated {len(files) - len(HAND_EDITED)} files] prds/ before: {total_before}  after: {total_after}")
    for rel, ctx in bare:
        print(f"  BARE {rel}: ...{ctx}...")


if __name__ == "__main__":
    main()
