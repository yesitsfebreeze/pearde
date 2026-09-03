#!/usr/bin/env bash
# The guard `one-verb-set` promised: the seven-verb table `scout.sh` (no
# argument) prints, from its own `registry`, and the "## Commands" table in
# README.md must be the same rows — column for column — or the two have
# drifted back into the two truths this PRD existed to remove. Silent and
# exit 0 when they agree; one line per mismatch otherwise, doctor-style.
#
# Not a `scout.sh` verb: this checks `scout.sh`'s own claim about itself, so
# it cannot live inside the thing making the claim, and it is not wired into
# the repo's top-level doctor.sh either — `resources/scout/` links out to
# nothing past `@@scout` (@references/files.md), so nothing outside it may
# link in past that same door, this script included; run it by hand or from
# a scout-owned CI step (`templates/scout.yml`), not from `doctor.sh`.
#
#   resources/scout/check.sh
set -euo pipefail
export LC_ALL=C
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# scout.sh's own table, minus its header row, one tab-joined row per verb.
live="$("$here/scout.sh" | tail -n +2 | sed -E 's/  +/\t/g')"

# README.md's Commands table: the header row named exactly, every `| a | b |
# c |` line after it up to the next one that is not a table row, backticks
# stripped so `` `sweep` `` reads the same as scout.sh's bare `sweep`.
readme="$(awk '
	/^\| verb \| contract \| lands in \|$/ { f = 1; next }
	f && /^\|---/ { next }
	f && /^\|/ { print; next }
	f { exit }
' "$here/README.md" | sed -E 's/^\| *//; s/ *\|$//; s/ *\| */\t/g; s/`([^`]*)`/\1/g')"

bad=0
n=$(printf '%s\n' "$live"   | grep -c .)
m=$(printf '%s\n' "$readme" | grep -c .)
if [ "$n" != "$m" ]; then
	echo "scout/check: scout.sh lists $n verbs, README.md's Commands table holds $m rows"
	bad=1
fi

i=1
while [ "$i" -le "$n" ] && [ "$i" -le "$m" ]; do
	a="$(printf '%s\n' "$live"   | sed -n "${i}p")"
	b="$(printf '%s\n' "$readme" | sed -n "${i}p")"
	if [ "$a" != "$b" ]; then
		echo "scout/check: row $i differs"
		echo "  scout.sh:   $a"
		echo "  README.md:  $b"
		bad=1
	fi
	i=$((i + 1))
done

exit "$bad"
