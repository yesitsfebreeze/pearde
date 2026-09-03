#!/usr/bin/env bash
# Sweep GitHub for things worth reusing — not just libraries, but the reference
# lists, starters and written-down practice that get cloned across every field.
#
# Two axes, because they answer different questions:
#   stars  — what the field already settled on. Safe, but you are late.
#   delta  — what it is settling on right now. Early, but half of it is hype.
#
# The stargazers API is restricted as of 2026-06-30, so there is no per-repo
# star timeline for a repo you do not own. Delta is computed the one way still
# open: snapshot star counts on every sweep, diff our own history. `delta`
# reports nothing until the second sweep and sharpens with every one after —
# and it measures the buckets in buckets.txt, not GitHub's global firehose.
#
#   scout.sh sweep              take a snapshot of every bucket
#   scout.sh delta [days]       what gained the most stars since ~N days ago
#   scout.sh trending [window]  GitHub's own trending, as a discovery channel
#                               for buckets you never thought to define
#                               (window: daily | weekly | monthly)
#   scout.sh reading            check reading-list.md: every row needs a
#                               mapping column, and a row whose repo has gone
#                               ARCHIVED is marked stale in place
set -euo pipefail

# Repo descriptions are full of emoji and CJK; byte-wise collation keeps sort
# and awk from erroring out on sequences that are not valid in the user locale.
export LC_ALL=C

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scout="$root/scout"
snaps="$scout/snapshots"
buckets="$scout/buckets.txt"
per_bucket="${SCOUT_PER_BUCKET:-30}"
# One snapshot/day; keep enough to serve any `delta <days>` window callers
# actually use (README documents up to ~90) plus slack for gaps in the cron.
snap_keep="${SCOUT_SNAP_KEEP:-90}"

die() { echo "scout: $*" >&2; exit 1; }

cmd_sweep() {
	[ -f "$buckets" ] || die "no bucket file at $buckets"
	mkdir -p "$snaps"
	local out="$snaps/$(date -u +%Y-%m-%d).tsv"
	: > "$out"

	local n=0
	while IFS=$'\t' read -r name query; do
		case "$name" in ''|\#*) continue ;; esac
		[ -n "${query:-}" ] || continue
		printf '  %-14s %s\n' "$name" "$query" >&2

		# One search call per bucket. Authenticated search allows 30/min, so
		# even a large bucket file stays inside the limit without throttling.
		gh api -X GET search/repositories \
			-f q="$query" -f sort=stars -f order=desc -F per_page="$per_bucket" \
			--jq '.items[] | [
				.full_name, (.stargazers_count|tostring), .pushed_at,
				(.archived|tostring), (.license.spdx_id // "NONE"),
				(.language // "-"), ((.description // "") | gsub("\t";" "))
			] | @tsv' |
			sed "s/^/$name\t/" >> "$out" || die "search failed for bucket '$name'"
		n=$((n + 1))
	done < "$buckets"

	echo >&2
	echo "snapshot: $out  ($n buckets, $(wc -l < "$out" | tr -d ' ') rows)" >&2

	# Cap: keep only the snap_keep most recent snapshots so snapshots/ does
	# not grow unbounded — one ~700-line TSV per sweep, forever, otherwise.
	local all total over extra
	all=$(ls -1 "$snaps"/*.tsv 2>/dev/null | sort)
	total=$(echo "$all" | grep -c .)
	over=$((total - snap_keep))
	extra=""
	[ "$over" -gt 0 ] && extra=$(echo "$all" | head -n "$over")
	if [ -n "$extra" ]; then
		echo "$extra" | while IFS= read -r f; do rm -f "$f"; done
		echo "pruned $(echo "$extra" | wc -l | tr -d ' ') snapshot(s) older than the $snap_keep kept" >&2
	fi

	cmd_delta 0 2>/dev/null || echo "run again tomorrow for a delta" >&2
}

# Diff the newest snapshot against the most recent one at least N days older.
cmd_delta() {
	local want_days="${1:-7}"
	local files
	files=$(ls -1 "$snaps"/*.tsv 2>/dev/null | sort) || true
	[ -n "$files" ] || die "no snapshots yet — run 'scout.sh sweep' first"

	local newest base
	newest=$(echo "$files" | tail -1)
	base=$(echo "$files" | sed '$d' | tail -1)   # BSD head has no `-n -1`
	[ -n "${base:-}" ] || { echo "only one snapshot so far — nothing to diff" >&2; return 1; }

	# Prefer the oldest snapshot still inside the requested window, so `delta 30`
	# measures a month of movement rather than yesterday's noise.
	if [ "$want_days" -gt 0 ]; then
		local cutoff f
		cutoff=$(date -u -v-"${want_days}"d +%Y-%m-%d 2>/dev/null || date -u -d "$want_days days ago" +%Y-%m-%d)
		for f in $files; do
			[ "$(basename "$f" .tsv)" \< "$cutoff" ] && continue
			base="$f"; break
		done
	fi

	echo "# $(basename "$base" .tsv) -> $(basename "$newest" .tsv)" >&2
	awk -F'\t' -v OFS='\t' '
		NR==FNR { old[$2] = $3; next }
		{
			if (!($2 in old)) { gain = "NEW"; pct = "-" }
			else {
				d = $3 - old[$2]
				if (d <= 0) next
				gain = "+" d
				pct = old[$2] > 0 ? sprintf("%.1f%%", d * 100 / old[$2]) : "-"
			}
			key = ($2 in old) ? $3 - old[$2] : 999999999
			print key, $1, $2, $3, gain, pct, substr($8, 1, 60)
		}
	' "$base" "$newest" |
		sort -t$'\t' -k1,1nr | cut -f2- |
		{ printf 'BUCKET\tREPO\tSTARS\tGAIN\tRATE\tWHAT\n'; cat; } |
		head -40 | column -t -s $'\t'
}


# Check pass over reading-list.md: every data row needs a non-empty mapping
# (its last column, "what to steal") and its repo's live state, resolved
# through the same signal toolscout.sh reads (archived, last push) — a row
# whose repo has gone ARCHIVED is marked `<!-- stale: archived YYYY-MM-DD -->`
# in place, never deleted; the curated judgement in the row stands.
#
# Guard against the network: a row's repo is looked up in the *newest*
# snapshot first (already-fetched archived/pushed_at, free), and `gh api` is
# called per repo only when no snapshot row names it — sweep's buckets are
# topic searches, not this list's specific repos, so most rows still miss
# the snapshot and pay one REST call each (5000/hr authenticated, no
# per-item rate wait like the search endpoint sweep uses).
cmd_reading() {
	local list="$scout/reading-list.md"
	[ -f "$list" ] || die "no reading list at $list"

	local newest=""
	newest=$(ls -1 "$snaps"/*.tsv 2>/dev/null | sort | tail -1) || true

	local tmp bare="" checked=0 marked=0 today
	tmp="$(mktemp)"
	today="$(date -u +%Y-%m-%d)"

	while IFS= read -r line || [ -n "$line" ]; do
		case "$line" in
			'| ['*)
				local n mapping repo
				# The link *text* is not always `owner/repo` (a display name
				# like `[cargo-mutants](...)` is common) — the URL is the only
				# reliable source for the full name.
				# `|| true`: the script runs under `pipefail`, and a row that
				# links anywhere but GitHub makes `grep` exit 1 — which would
				# abort the whole check mid-file, silently, with no output and
				# a status indistinguishable from a bare row. No match here is
				# a normal row, not an error.
				repo=$(printf '%s' "$line" | grep -oE 'github\.com/[^)]+' | head -1 | sed 's#github\.com/##' || true)
				n=$(awk -F'|' '{print NF}' <<<"$line")
				mapping=$(awk -F'|' -v n="$n" '{v=$(n-1); gsub(/^[ \t]+|[ \t]+$/,"",v); print v}' <<<"$line")

				if [ -z "$mapping" ]; then
					# A row that links somewhere other than GitHub parses to
					# no `owner/repo`, and an unnamed row is a check that
					# does not name the row it failed on — fall back to the
					# link text, which every row has.
					local label="$repo"
					[ -n "$label" ] || label=$(printf '%s' "$line" | sed -E 's#^\| *\[([^]]*)\].*#\1#')
					bare="$bare  $label\n"
				fi

				if [ -n "$repo" ] && [ "${line#*"<!-- stale:"}" = "$line" ]; then
					checked=$((checked + 1))
					local archived="" pushed="" hit resp
					if [ -n "$newest" ]; then
						hit=$(awk -F'\t' -v want="$repo" '$2==want{print; exit}' "$newest")
						if [ -n "$hit" ]; then
							archived=$(cut -f5 <<<"$hit")
							pushed=$(cut -f4 <<<"$hit")
						fi
					fi
					if [ -z "$archived" ]; then
						resp=$(gh api "repos/$repo" --jq '{archived, pushed_at}' 2>/dev/null) || resp=""
						if [ -n "$resp" ]; then
							archived=$(jq -r '.archived' <<<"$resp")
							pushed=$(jq -r '.pushed_at' <<<"$resp")
						fi
					fi
					if [ "$archived" = "true" ]; then
						local asof="${pushed%%T*}"
						[ -n "$asof" ] || asof="$today"
						# Insert right after the repo link, inside the same
						# cell — the row stays one line, the comment shows in
						# the raw file, and the table does not break.
						line=$(printf '%s' "$line" | sed -E "s#(\]\([^)]+\))#\1 <!-- stale: archived $asof -->#")
						marked=$((marked + 1))
					fi
				fi
				;;
		esac
		printf '%s\n' "$line" >> "$tmp"
	done < "$list"

	# Write back only when a row was actually marked. `mv` from a `mktemp`
	# file carries that file's 0600 mode and its inode onto the list on
	# every run — a check that found nothing to say would leave the list
	# owner-readable only, and the bare-row run is contracted to fail
	# *without modifying the file*. `cat >` keeps the list's own mode.
	if [ "$marked" -gt 0 ]; then
		cat "$tmp" > "$list"
	fi
	rm -f "$tmp"
	echo "reading: $checked repo(s) checked against state, $marked marked stale" >&2

	if [ -n "$bare" ]; then
		echo "reading: bare row(s) — no mapping column ('what to steal'):" >&2
		printf '%b' "$bare" >&2
		return 1
	fi
}

cmd_trending() {
	local window="${1:-weekly}"
	local html
	html=$(curl -sfL -A "Mozilla/5.0" "https://github.com/trending?since=$window") \
		|| die "could not reach github.com/trending"

	# Repo names and star gains appear once per row in document order, so the
	# two extractions line up by position. A scraped page with no API behind
	# it — a mismatch is a layout change, and dies loudly.
	local names gains
	names=$(echo "$html" | grep -oE 'href="/[^"/]+/[^"/]+" data-view-component="true" class="Link"' \
		| sed -E 's|href="/||; s|" data.*||')
	gains=$(echo "$html" | grep -oE '[0-9,]+ stars (today|this week|this month)' | sed -E 's/ stars.*//')

	[ "$(echo "$names" | wc -l)" -eq "$(echo "$gains" | wc -l)" ] \
		|| die "trending layout changed — name/gain rows no longer align"

	{ printf 'REPO\tGAIN (%s)\n' "$window"; paste <(echo "$names") <(echo "$gains"); } \
		| column -t -s $'\t'
}

case "${1:-}" in
	sweep)    shift; cmd_sweep "$@" ;;
	delta)    shift; cmd_delta "$@" ;;
	reading)  shift; cmd_reading "$@" ;;
	trending) shift; cmd_trending "$@" ;;
	*)        awk 'NR>1 && /^#/ {sub(/^# ?/,""); print; next} NR>1 {exit}' \
	              "${BASH_SOURCE[0]}" >&2; exit 2 ;;
esac
