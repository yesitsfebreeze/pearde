#!/usr/bin/env bash
# the-worker-parts-are-rewritten-dense — pass one's probe, kept for pass two.
#
# The build was the rewrite itself: the seven parts under references/parts/
# rewritten dense in the lane worktree, uncommitted. This script is what
# bounded it — the fact audit that says no backticked token, no @ link, no
# table row and no heading present at HEAD went missing in the rewrite.
# Naive by design: it reports near-misses (a link that gained a trailing
# character, a code span that moved across a line break) so a person looks,
# rather than passing silently. Three such were reported and all three were
# the same word still on the page, re-wrapped.
#
#   bash <this> [<repo root, default $PWD>]
set -u
ROOT="${1:-$PWD}"
cd "$ROOT" || exit 1
for f in workers workflows personas consult health grammar memos; do
  python3 - "references/parts/$f.md" <<'PY'
import re, subprocess, sys
p = sys.argv[1]
old = subprocess.run(['git', 'show', 'HEAD:' + p], capture_output=True, text=True).stdout
new = open(p).read()
toks  = lambda s: set(re.findall(r'`[^`\n]+`', s))
links = lambda s: set(re.findall(r'@[\w./-]+', s))
rows  = lambda s: len([l for l in s.splitlines() if l.strip().startswith('|')])
heads = lambda s: [l for l in s.splitlines() if l.startswith('#')]
mt = toks(old) - toks(new)
ml = links(old) - links(new)
mh = [h for h in heads(old) if h not in heads(new)]
print(f"{p}: words {len(old.split())}->{len(new.split())} "
      f"rows {rows(old)}->{rows(new)} heads {len(heads(old))}->{len(heads(new))} "
      f"backticks {new.count('`')}")
if mt: print("  look at tokens:", sorted(mt))
if ml: print("  look at links:", sorted(ml))
if mh: print("  look at headings:", mh)
PY
done
