#!/usr/bin/env bash
# no-colour-group-in-the-vault-preset-is-a-path-query — the verify command of
# the memo of the same name. Run from the repo root:
#
#     bash resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not. Two checks, and
# the second is the one that bites:
#
#   1. the preset  — every `colorGroups` query in
#                    resources/board/obsidian/graph.json is a `tag:` query
#   2. the board   — every tag those groups name is carried by at least one
#                    note under the board
#
# A colour group that matches nothing is not an error Obsidian reports: the
# graph draws grey and looks like a layout choice. That is how the path-keyed
# groups died unnoticed when the board moved to `.pearde/wiki/`, and check 2
# catches the same break in its tag-shaped form — a writer that stops emitting
# a kind's tag leaves a group matching nothing.
set -u
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root" || exit 1

python3 - "$root" <<'PY'
import glob, json, os, re, subprocess, sys

root = sys.argv[1]
preset = os.path.join(root, "resources", "board", "obsidian", "graph.json")
try:
    groups = json.load(open(preset, encoding="utf-8")).get("colorGroups") or []
except (OSError, ValueError) as e:
    print(f"BROKEN: {preset} unreadable — {e}")
    sys.exit(1)
if not groups:
    print(f"BROKEN: {preset} declares no colour groups")
    sys.exit(1)

bad = [g.get("query", "") for g in groups
       if not str(g.get("query", "")).startswith("tag:#")]
if bad:
    print("BROKEN: colour group(s) not keyed on a tag — " + ", ".join(bad))
    sys.exit(1)

# The board of this repo, `.pearde/` first and the legacy `pearde/` after it.
# Rooted at the CHECKOUT, never at `root`: a lane is a worktree of this repo
# and holds an empty `.pearde/` of its own, so a script spelling the board
# beside itself reads that empty directory and reports BROKEN on a tree where
# nothing is wrong. `--git-common-dir` is the one `.git` every worktree shares.
common = subprocess.run(["git", "-C", root, "rev-parse", "--git-common-dir"],
                        capture_output=True, text=True)
checkout = (os.path.dirname(os.path.realpath(common.stdout.strip()))
            if common.returncode == 0 and common.stdout.strip() else root)
board = next((p for p in (os.path.join(checkout, ".pearde"),
                          os.path.join(checkout, "pearde"))
              if os.path.isdir(os.path.join(p, "prds"))), None)
if board is None:
    print(f"BROKEN: no board at {checkout}/.pearde — "
          "the second check has nothing to read")
    sys.exit(1)

# `[ \\t]` and not `\\s`: a block list writes `tags:` alone on its line, and
# `\\s*` would swallow the newline and read the first `- item` as an inline
# value — the whole block then reads as one malformed tag.
TAGS_RE = re.compile(r"^tags:[ \\t]*(.*)$", re.M)
carried = set()
for path in glob.glob(os.path.join(board, "**", "*.md"), recursive=True):
    try:
        head = open(path, encoding="utf-8").read(2000)
    except OSError:
        continue
    if not head.startswith("---"):
        continue
    fence = head.find("\n---", 3)
    front = head[:fence if fence > 0 else len(head)]
    m = TAGS_RE.search(front)
    if not m:
        continue
    inline = m.group(1).strip()
    if inline.startswith("["):
        carried.update(t.strip() for t in inline.strip("[]").split(","))
    else:
        for line in front[m.end():].splitlines()[1:]:
            item = line.strip()
            if not item.startswith("- "):
                break
            carried.add(item[2:].strip())

dead = [g["query"] for g in groups
        if g["query"][len("tag:#"):] not in carried]
if dead:
    print("BROKEN: colour group(s) no note carries — " + ", ".join(dead))
    sys.exit(1)
print(f"{len(groups)} colour groups, all tag queries, all carried")
PY
