#!/usr/bin/env bash
# probe — the union arithmetic, on a tree built at run time.
#
# Three git repos in a temp dir: two members and the master that names them.
# Every count is known by construction, so the assertions below are arithmetic
# rather than a reading of this machine. Also covers the case the four real
# boards do not: a member that is itself a master.
set -u
RAMP=${RAMP:-/Users/feb/dev/infra/pearde/resources/board/ramp.py}
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
fail=0
say() { if [ "$1" = 0 ]; then echo "PASS  $2"; else echo "FAIL  $2"; fail=1; fi; }

mkrepo() {                              # mkrepo <dir> <n .rs files>
  mkdir -p "$1/src" "$1/.pearde/prds"
  i=0; while [ "$i" -lt "$2" ]; do : > "$1/src/f$i.rs"; i=$((i+1)); done
  printf 'x\n' > "$1/README.md"
  git -C "$1" init -q 2>/dev/null
  git -C "$1" add -A 2>/dev/null
  printf -- '---\nname: %s\n---\n' "$(basename "$1")" > "$1/.pearde/settings.md"
}

mkrepo "$T/a" 30
mkrepo "$T/b" 12
mkrepo "$T/top" 1
{ printf -- '---\nname: top\nmembers:\n'
  printf -- '  - %s\n' "$T/a/.pearde" "$T/b/.pearde"
  printf -- '---\n'; } > "$T/top/.pearde/settings.md"

rust_of() { python3 "$RAMP" need --board "$1" 2>&1 | awk '$1=="rust"{print $2}'; }

A=$(rust_of "$T/a/.pearde"); B=$(rust_of "$T/b/.pearde")
O=$(rust_of "$T/top/.pearde")
[ "$A" = 30 ]; say $? "a alone counts its own 30 .rs (got ${A:-none})"
[ "$B" = 12 ]; say $? "b alone counts its own 12 .rs (got ${B:-none})"
[ "$O" = 43 ]; say $? "the master sums 30+12+1 = 43 (got ${O:-none})"

W=$(python3 "$RAMP" need --board "$T/top/.pearde" 2>&1 | awk '$1=="rust"{$1="";$2="";print}')
case "$W" in *a*) r=0;; *) r=1;; esac; say $r "the master's rust row credits member a"
case "$W" in *top*) r=0;; *) r=1;; esac; say $r "the master's rust row credits its own tree"

# a floor is applied to the sum, not per member: two members of 15 .md each
# clear writing's floor of 25 together and neither does alone
mkrepo "$T/c" 0; mkrepo "$T/d" 0; mkrepo "$T/mid" 0
i=0; while [ "$i" -lt 15 ]; do : > "$T/c/n$i.md"; : > "$T/d/n$i.md"; i=$((i+1)); done
git -C "$T/c" add -A 2>/dev/null; git -C "$T/d" add -A 2>/dev/null
{ printf -- '---\nname: mid\nmembers:\n'
  printf -- '  - %s\n' "$T/c/.pearde" "$T/d/.pearde"
  printf -- '---\n'; } > "$T/mid/.pearde/settings.md"
wr() { python3 "$RAMP" need --board "$1" 2>&1 | awk '$1=="writing"{print $2}'; }
[ -z "$(wr "$T/c/.pearde")" ]; say $? "c's .md alone stays under writing's floor"
[ -z "$(wr "$T/d/.pearde")" ]; say $? "d's .md alone stays under writing's floor"
MID=$(wr "$T/mid/.pearde")
[ -n "$MID" ] && [ "$MID" -ge 30 ]
say $? "the floor is applied to the sum, never per member: $MID over two members that each fall short"

# a member that is itself a master — its own board would measure the union,
# so the parent must see the grandchildren's trees, not the middle repo's
mkrepo "$T/root" 0
{ printf -- '---\nname: root\nmembers:\n  - %s\n---\n' "$T/top/.pearde"; } \
  > "$T/root/.pearde/settings.md"
R=$(rust_of "$T/root/.pearde")
[ "$R" = 43 ]; say $? "a master under a master reaches the grandchildren: 43 (got ${R:-none})"

# a cycle must not hang or recurse forever
mkrepo "$T/x" 4; mkrepo "$T/y" 4
printf -- '---\nname: x\nmembers:\n  - %s\n---\n' "$T/y/.pearde" > "$T/x/.pearde/settings.md"
printf -- '---\nname: y\nmembers:\n  - %s\n---\n' "$T/x/.pearde" > "$T/y/.pearde/settings.md"
# macOS ships no timeout(1); perl's alarm is the portable bound
if out=$(perl -e 'alarm 20; exec @ARGV' python3 "$RAMP" need --board "$T/x/.pearde" 2>&1); then
  n=$(printf '%s' "$out" | awk '$1=="rust"{print $2}')
  [ "$n" = 8 ]; say $? "a members cycle terminates and counts each repo once: 8 (got ${n:-none})"
else
  say 1 "a members cycle terminates (it did not)"
fi

exit $fail
