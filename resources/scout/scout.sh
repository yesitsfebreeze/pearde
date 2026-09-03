#!/usr/bin/env bash
# One door onto scout's four layers — discover, ask, curate, wire — that used
# to be four files with four `--help` texts and a distinction (daily
# measurement vs one-off ranker vs curated list vs passive gate) held in the
# head, not printed anywhere. `scout.sh <verb>` is now the whole surface;
# `toolscout.sh` stays only as a compat entry that execs `scout.sh tool`.
#
# Two axes on the discovery layer, because they answer different questions:
#   stars  — what the field already settled on. Safe, but you are late.
#   delta  — what it is settling on right now. Early, but half of it is hype.
#
# The stargazers API is restricted as of 2026-06-30, so there is no per-repo
# star timeline for a repo you do not own. Delta is computed the one way still
# open: snapshot star counts on every sweep, diff our own history. `delta`
# reports nothing until the second sweep and sharpens with every one after —
# and it measures the buckets in buckets.txt, not GitHub's global firehose.
#
# `scout.sh` with no verb prints the table below — REGISTRY is the one place
# the verb list, its one-line contract and its landing file are written, and
# `README.md`'s Commands table is generated from a run of this same table
# (`README.md` names the exact command; a diff between the two is a doctor
# finding, never a second copy typed by hand).
set -euo pipefail

# Repo descriptions are full of emoji and CJK; byte-wise collation keeps sort
# and awk from erroring out on sequences that are not valid in the user locale.
export LC_ALL=C

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
scout="$here"
snaps="$scout/snapshots"
buckets="$scout/buckets.txt"
per_bucket="${SCOUT_PER_BUCKET:-30}"
# One snapshot/day; keep enough to serve any `delta <days>` window callers
# actually use (README documents up to ~90) plus slack for gaps in the cron.
snap_keep="${SCOUT_SNAP_KEEP:-90}"

die() { echo "scout: $*" >&2; exit 1; }

# The single source of the verb list: verb (with its args), one-line
# contract, and the file a reader finds its record in — tab-separated, one
# row per verb, in the order `scout.sh` (no args) and README.md's Commands
# table both print them. Editing a verb's shape means editing this row and
# nothing else prints a stale one.
registry() {
	cat <<-'EOF'
	sweep	snapshot every bucket's star counts	snapshots/<date>.tsv
	delta [days]	what gained the most stars since ~N days ago	snapshots/ (diffed, no new write)
	trending [window]	GitHub's own trending feed, a discovery channel	none kept — pipe to a file to save it
	tool <query>	one-off dependency ranking: stars + what stars hide	none kept — pipe to a file to save it
	find <id> [query]	call one ranking page by id (was route.sh)	routes.md defines it; a settled pick goes in findings.md
	reading	check the curated reading list: mappings present, archived rows marked	reading-list.md
	quality	the passive quality gates and their templates	templates/
	EOF
}

cmd_list() {
	{ printf 'VERB\tCONTRACT\tLANDS IN\n'; registry; } | column -t -s $'\t'
}

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
	echo "record: $out  ($n buckets, $(wc -l < "$out" | tr -d ' ') rows)" >&2

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

# Portable day epoch: GNU `date -d`, else BSD `date -j -f`. Both forced to UTC
# midnight — an unforced BSD parse fills the missing time-of-day from *now*,
# which skews every day-count by however far into today the caller runs.
epoch_of() {
	local d="$1"
	date -u -d "$d 00:00:00" +%s 2>/dev/null \
		|| date -u -j -f "%Y-%m-%d %H:%M:%S" "$d 00:00:00" +%s
}

# Diff the newest snapshot against the most recent one at least N days older,
# and say which day it actually landed on — a gap in the cron otherwise reads
# as ordinary movement, just mislabeled with the wrong window.
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
		local cutoff f today candidates base_date actual_days tolerance
		today=$(date -u +%Y-%m-%d)
		cutoff=$(date -u -v-"${want_days}"d +%Y-%m-%d 2>/dev/null || date -u -d "$want_days days ago" +%Y-%m-%d)
		# Candidates exclude $newest itself — it is the diff's upper anchor,
		# never its own base, or a sparse history reports a false exact match
		# (today diffed against today, zero rows, no signal anything is wrong).
		candidates=$(echo "$files" | sed '$d')
		for f in $candidates; do
			[ "$(basename "$f" .tsv)" \< "$cutoff" ] && continue
			base="$f"; break
		done

		base_date=$(basename "$base" .tsv)
		actual_days=$(( ( $(epoch_of "$today") - $(epoch_of "$base_date") ) / 86400 ))
		tolerance=$(( want_days * 2 ))

		# The window doubled or worse: the reference day is not the one asked
		# for, and the worst reading of the table below is the plausible wrong
		# one. Name the gap and suppress the table rather than print it wrong.
		# Never narrow a legitimate long window — a young tree diffs against
		# its oldest snapshot and says so; only a window *stretched past
		# tolerance* is refused.
		if [ "$actual_days" -ge "$tolerance" ]; then
			echo "gap: no snapshot within 2× of ${want_days} days — run sweep first"
			return 0
		fi

		echo "delta ${want_days} · diffed against ${base_date} (${actual_days} days back, nearest to ${want_days})"
	fi

	# pipefail off for this one pipeline: `head -40` closes its end of the
	# pipe as soon as it has its 40 lines, `awk`/`sort` upstream then die of
	# SIGPIPE, and pipefail turns that ordinary truncation into a nonzero
	# pipeline status — which `set -e` then reads as a failure of the whole
	# function, skipping the `record:` line below on every diff over 40 rows.
	# Measured: a 2026-08-25 -> 2026-08-28 diff on this repo's own snapshots
	# exits 141 without it.
	set +o pipefail
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
	set -o pipefail

	echo "record: $base vs $newest — diffed in place, nothing new written to snapshots/" >&2
}


# Layer three, "curate": the mechanism-mapped reading list — repos worth
# reading, never just installing. The verb is the check over that list, not a
# dump of it: every data row needs a non-empty mapping
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
	echo "record: $list" >&2

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

	echo >&2
	echo "record: none kept — a live scrape of github.com/trending, pipe to a file to save it" >&2
}

# The one-off dependency ranker — moved here from toolscout.sh, which now
# execs `scout.sh tool "$@"`. Same flags, same payload, same jq pipeline, so
# `toolscout.sh <query>` and `scout.sh tool <query>` are byte-identical.
cmd_tool() {
	local limit=25
	local args=()
	while [ $# -gt 0 ]; do
		case "$1" in
			--limit) limit="$2"; shift 2 ;;
			*) args+=("$1"); shift ;;
		esac
	done

	if [ ${#args[@]} -eq 0 ]; then
		die "usage: scout.sh tool '<github search query>' [--limit N]"
	fi

	local query="${args[*]}"
	local now
	now="$(date -u +%s)"

	# GitHub caps search results at 100/page; sort=stars gives the popularity
	# axis, every other axis is computed below from the same payload.
	gh api -X GET search/repositories \
		-f q="$query" -f sort=stars -f order=desc -F per_page="$limit" \
		--jq '.items[] | {
			name: .full_name,
			stars: .stargazers_count,
			pushed: .pushed_at,
			issues: .open_issues_count,
			license: (.license.spdx_id // "NONE"),
			archived: .archived,
			lang: (.language // "-"),
			desc: (.description // "")
		}' |
	jq -rs --argjson now "$now" '
		def days(t): (($now - (t | fromdateiso8601)) / 86400) | floor;
		def flag(r):
			if r.archived then "ARCHIVED"
			elif days(r.pushed) > 365 then "stale"
			elif days(r.pushed) > 90 then "slow"
			else "active" end;
		["REPO","STARS","LAST PUSH","STATE","ISSUES","LICENSE","LANG"],
		(.[] | [
			.name,
			(.stars | tostring),
			"\(days(.pushed))d ago",
			flag(.),
			(.issues | tostring),
			.license,
			.lang
		])
		| @tsv
	' | column -t -s "$(printf '\t')"

	echo
	echo "query: $query   (stars rank; 'STATE' is what stars do not tell you)"
	echo "record: none kept — pipe to a file to save this ranking"
}

# Layer two, "ask": call one ranking page from routes.md by id. This is
# `route.sh` under scout's own door — the id space, `list` and `check`
# subcommands are unchanged, `route.sh` itself still holds the list and reads
# routes.md; this only forwards and, on an actual route run, names where the
# answer belongs once it is decided.
cmd_find() {
	set +e
	"$scout/route.sh" "$@"
	local rc=$?
	set -e
	case "${1:-}" in
		''|-h|--help|list|check) : ;;
		*) echo "record: routes.md defines the route just run; a settled pick's row goes in findings.md" >&2 ;;
	esac
	return "$rc"
}

# Layer four, "wire": the passive quality-gate templates a tree copies in.
cmd_quality() {
	local tdir="$scout/templates"
	[ -d "$tdir" ] || die "no templates at $tdir"
	{
		printf 'FILE\tGATE\n'
		for f in "$tdir"/*; do
			local b g
			b="$(basename "$f")"
			case "$b" in
				_typos.toml)     g="typos — deliberate-spelling allowlist" ;;
				deny.toml)       g="cargo-deny — RustSec advisories hard-gated" ;;
				dependabot.yml)  g="dependency updates" ;;
				quality.yml)     g="typos + gitleaks + cargo-deny + cargo-machete, weekly in CI" ;;
				scout.yml)       g="the sweep, run in CI instead of a local cron" ;;
				*)               g="-" ;;
			esac
			printf '%s\t%s\n' "$b" "$g"
		done
	} | column -t -s $'\t'
	echo >&2
	echo "record: $tdir — copy these into a tree to wire the gates" >&2
}

case "${1:-}" in
	sweep)     shift; cmd_sweep "$@" ;;
	delta)     shift; cmd_delta "$@" ;;
	trending)  shift; cmd_trending "$@" ;;
	tool)      shift; cmd_tool "$@" ;;
	find)      shift; cmd_find "$@" ;;
	reading)   shift; cmd_reading "$@" ;;
	quality)   shift; cmd_quality "$@" ;;
	''|-h|--help) cmd_list ;;
	*)         die "unknown verb '$1' — 'scout.sh' with no argument lists them" ;;
esac
