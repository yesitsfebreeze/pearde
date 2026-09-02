#!/usr/bin/env python3
"""Three clean-room defects in resources/prose.py, each reproduced in a temp
file with no repo content. Run from the repo root:

    python3 .pearde/prds/.../probe/prose_defects.py

Every case prints EXPECTED vs GOT. Exit 1 while any defect stands.
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
PROSE = os.path.join(ROOT, "resources", "prose.py")

CASES = [
    ("restrictive relative clause is not a vague subject",
     "# T\n\nAbsorb the conclusion that is canonical.\n", 0),
    ("object-position pronoun is bound, per prose.py's own docstring",
     "# T\n\nThe worker takes the lane it is given.\n", 0),
    ("frontmatter is counted as prose and dilutes the sentence mean",
     "---\nstate: open\norigin: requested\npriority: 55\ncomplexity: 30\n"
     "blast-radius: mid\nworkflow: probe-then-spec\nclaim: w 2026-01-01\n---\n"
     "\n# T\n\nA single very long sentence written deliberately to run far "
     "past the twenty word average that the density rule in the language file "
     "asks every document on this board to hold itself to without exception.\n",
     1),
]


def run(text):
    fd, path = tempfile.mkstemp(suffix=".md")
    os.write(fd, text.encode())
    os.close(fd)
    try:
        got = subprocess.run([sys.executable, PROSE, "check", path],
                             capture_output=True, text=True)
        return got.returncode, got.stdout.strip()
    finally:
        os.unlink(path)


def main():
    bad = 0
    for name, text, want in CASES:
        code, out = run(text)
        ok = code == want
        bad += 0 if ok else 1
        print(f"{'ok  ' if ok else 'FAIL'} {name}: want exit {want}, got {code}"
              + (f" — {out.split(': ', 1)[-1]}" if out else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
