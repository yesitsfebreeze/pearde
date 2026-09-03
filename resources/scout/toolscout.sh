#!/usr/bin/env bash
# Compat entry. The one-off dependency ranker moved to `scout.sh tool` — one
# door for all seven verbs instead of a fifth file — and this name execs it
# unchanged, so an old invocation, a cron line or an external reference never
# breaks. `toolscout.sh <query>` and `scout.sh tool <query>` are the same
# process by construction: this file's only job is to become that one.
#
# Usage:
#   toolscout.sh 'topic:rust language:rust'      # a GitHub search query
#   toolscout.sh 'pdf parsing' --limit 40
#
# Query syntax is GitHub's own: topic:, language:, stars:>N, pushed:>DATE.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$here/scout.sh" tool "$@"
