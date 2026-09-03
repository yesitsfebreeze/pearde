"""No table and no table row at <ref> is gone from the working tree: per file,
the table count and the row count may rise and may never fall.

What it does not prove: a row swapped for a different row of the same shape.
`probe/tokens.py` covers the backticked half of that, and the rest is read.

Two stricter keys were tried against the real rewrites and both false-positive,
because the rewrite tightens cells as well as prose:

    row keyed by its first cell   `more than 60 words in the fork` became
                                  `over 60 words in the fork` — same row
    table keyed by its header     `why it fits pearde` became `why it fits`,
                                  `why reject` became `why` — same table

`git diff | grep -c '^-|'` cannot back the constraint either: a re-worded row
shows as one removal and one addition, so the count is the number of rows
touched, never the number lost."""
import re, subprocess, sys

FENCE = re.compile(r"^\s*```")
SEP = re.compile(r"^\|[\s:|-]+\|$")


def tables(text):
    """Row counts, one per table, in file order. The header row counts."""
    out, cur, inside = [], 0, False
    for line in text.splitlines():
        if FENCE.match(line):
            inside = not inside
            continue
        s = line.strip()
        if inside or not s.startswith("|"):
            if cur:
                out.append(cur)
                cur = 0
            continue
        if not SEP.match(s):
            cur += 1
    if cur:
        out.append(cur)
    return out


ref = sys.argv[1]
bad = 0
for f in sys.argv[2:]:
    old = subprocess.run(["git", "show", f"{ref}:{f}"], capture_output=True, text=True).stdout
    was, now = tables(old), tables(open(f, encoding="utf-8").read())
    print(f"{f}: {len(was)} table(s) {sum(was)} rows -> {len(now)} table(s) {sum(now)} rows")
    if len(now) < len(was):
        bad = 1
        print(f"  {len(was) - len(now)} table(s) gone")
    if sum(now) < sum(was):
        bad = 1
        print(f"  {sum(was) - sum(now)} row(s) gone")
sys.exit(bad)
