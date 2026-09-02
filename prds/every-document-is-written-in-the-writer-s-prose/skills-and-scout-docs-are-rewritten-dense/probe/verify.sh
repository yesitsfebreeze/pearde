#!/usr/bin/env bash
# Re-run every acceptance box of this PRD against the MERGED tree, never the
# lane alone. `collect` commits the lane's uncommitted files and then merges,
# so a gate run on either side by itself measures a tree nobody will have.
# `main` moved under this lane — it added a section to
# `resources/scout/findings.md` — and only the merged tree shows that.
#
#   LANE=<lane worktree> MAIN=<main ref> bash verify.sh
#   REF=main bash verify.sh          # the negative control
#
# It writes nothing into either checkout and moves no branch: the lane's
# uncommitted files become a temp commit through a temp index, that commit is
# merged with `git merge-tree --write-tree`, and the result is unpacked into a
# temp dir.
set -u

LANE=${LANE:-/Users/feb/dev/infra/pearde/pearde/.lanes/every-document-is-written-in-the-writer-s-prose-skills-and-scout-docs-are-rewritten-dense}
# The lane's fork point, pinned as a literal SHA. `main` cannot be the default:
# `collect` commits the merge BEFORE it runs the verify block, so by then
# `main` contains the lane and every diff against it is empty — the boxes
# then read 0 changed files and fail on work that is correct.
MAIN=${MAIN:-9889e78}
cd "$LANE" || exit 2

pass=0; fail=0
box() { local name=$1 want=$2 got=$3
  if [ "$got" = "$want" ]; then pass=$((pass+1)); echo "PASS  $name"
  else fail=$((fail+1)); echo "FAIL  $name (exit $got, wanted $want)"; fi
}

W=$(mktemp -d); M=$(mktemp -d); trap 'rm -rf "$W" "$M"' EXIT

REF=${REF:-}
if [ -z "$REF" ]; then
  GIT_INDEX_FILE="$W/idx" git read-tree HEAD || exit 2
  GIT_INDEX_FILE="$W/idx" git add -A -- references/skills resources/scout || exit 2
  t=$(GIT_INDEX_FILE="$W/idx" git write-tree)
  REF=$(git commit-tree "$t" -p HEAD -m "probe: the lane's working tree")
  what="$(git rev-parse --short HEAD) + uncommitted"
else
  what="$REF"
fi

TREE=$(git merge-tree --write-tree "$MAIN" "$REF" 2>/dev/null)
if [ -z "$TREE" ]; then echo "FAIL  the lane does not merge into $MAIN"; exit 1; fi
echo "merged tree $TREE  ($MAIN + $what)"
git archive "$TREE" | tar -x -C "$M"

# --- spec01 · references/skills/ --------------------------------------------
( cd "$M" && python3 resources/prose.py check references/skills/*.md ) >/dev/null 2>&1
box "spec01.1 prose.py names no file in references/skills/" 0 $?

python3 - "$LANE" "$MAIN" "$M" <<'PY'
import glob, os, re, subprocess, sys
lane, main, merged = sys.argv[1:4]
bad = []
for path in sorted(glob.glob(os.path.join(merged, "references/skills/*.md"))):
    rel = os.path.relpath(path, merged)
    old = subprocess.run(["git", "-C", lane, "show", f"{main}:{rel}"],
                         capture_output=True, text=True).stdout
    new = open(path, encoding="utf-8").read()
    def field(t, k):
        for l in t.splitlines():
            if l.startswith(k + ": "):
                return l
        return ""
    if field(old, "name") != field(new, "name"):
        bad.append(f"{rel}: name: changed")
    do, dn = field(old, "description"), field(new, "description")
    if not dn:
        bad.append(f"{rel}: no description:")
    for pat, what in ((r'"[^"]*"', "trigger"), (r'`[^`]*`', "code span")):
        if re.findall(pat, do) != re.findall(pat, dn):
            bad.append(f"{rel}: {what} list changed")
for b in bad:
    print(b)
sys.exit(1 if bad else 0)
PY
box "spec01.2 every name: and every trigger phrase byte-identical to $MAIN" 0 $?

python3 - "$M" <<'PY'
import glob, os, sys
over = [f for f in sorted(glob.glob(os.path.join(sys.argv[1], "references/skills/*.md")))
        for l in open(f, encoding="utf-8")
        if l.startswith("description: ") and len(l.rstrip("\n")) - 13 > 1024]
for f in over:
    print(os.path.basename(f), "description over 1024 chars")
sys.exit(1 if over else 0)
PY
box "spec01.3 no description: exceeds 1024 characters" 0 $?

( cd "$M" && bash resources/doctor.sh 2>&1 ) | grep -qE '^  skills +ok +19 well-formed'
box "spec01.4 doctor reports 19 well-formed skills" 0 $?

ns=$(git diff --name-status "$MAIN" "$TREE" -- references/skills/ resources/scout/)
[ "$(echo "$ns" | grep -cE '^M')" -ge 18 ] && [ -z "$(echo "$ns" | grep -vE '^M')" ]
box "spec01.5 18+ files changed in scope and every line is M" 0 $?

# --- spec02 · resources/scout/ ----------------------------------------------
( cd "$M" && python3 resources/prose.py check resources/scout/*.md ) >/dev/null 2>&1
box "spec02.1 prose.py names no file in resources/scout/" 0 $?

[ "$( cd "$M" && bash resources/scout/route.sh list 2>/dev/null | wc -l | tr -d ' ' )" = 45 ]
box "spec02.2 route.sh list returns 45 routes" 0 $?

# A route id is the word after `### `, which is where `route.sh`'s own `ids()`
# reads it. The first spelling of this check matched `| \`<id>\`` — a table row
# `routes.md` has never held — so it diffed two empty lists and could not fail.
# The rule it asserts did not move: the id set, read the way `route.sh` reads it.
ids() { sed -n 's/^### \([a-z0-9-]*\) .*/\1/p' | sort; }
[ "$(git show "$MAIN:resources/scout/routes.md" | ids | wc -l | tr -d ' ')" -ge 45 ] &&
diff <(git show "$MAIN:resources/scout/routes.md" | ids) \
     <(ids < "$M/resources/scout/routes.md") >/dev/null
box "spec02.3 the route id set is unchanged" 0 $?

for f in findings.md reading-list.md README.md routes.md; do
  [ "$(git show "$MAIN:resources/scout/$f" | grep -cE '^\| ')" \
    = "$(grep -cE '^\| ' "$M/resources/scout/$f")" ]
  box "spec02.4 $f keeps every table row" 0 $?
done

# --- both -------------------------------------------------------------------
MM=$(mktemp -d); git archive "$MAIN" | tar -x -C "$MM"
diff <( cd "$MM" && python3 resources/index.py check 2>&1 | sort ) \
     <( cd "$M" && python3 resources/index.py check 2>&1 | sort ) >/dev/null
box "spec02.5 index.py check says exactly what it says on $MAIN" 0 $?
rm -rf "$MM"

python3 - "$LANE" "$MAIN" "$M" <<'PY'
import glob, os, re, subprocess, sys
lane, main, merged = sys.argv[1:4]
def words(t):
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = re.sub(r"`[^`]*`", "", t)
    return len(t.split())
old = new = 0
for path in sorted(glob.glob(os.path.join(merged, "references/skills/*.md"))
                   + glob.glob(os.path.join(merged, "resources/scout/*.md"))):
    rel = os.path.relpath(path, merged)
    old += words(subprocess.run(["git", "-C", lane, "show", f"{main}:{rel}"],
                                capture_output=True, text=True).stdout)
    new += words(open(path, encoding="utf-8").read())
print(f"scope words {old} -> {new}")
sys.exit(0 if new < old else 1)
PY
box "spec02.6 the scope's word count is below $MAIN" 0 $?

echo
echo "boxes $pass/$((pass+fail))"
[ "$fail" = 0 ]
