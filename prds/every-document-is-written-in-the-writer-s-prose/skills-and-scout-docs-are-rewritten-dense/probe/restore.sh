#!/usr/bin/env bash
# Put pass three's finished tree back into a lane that was reset.
# `probe/skills/` and `probe/scout/` hold whole files, not bodies — pass two
# lost four hours to `probe/bodies/`, which was a mid-pass snapshot.
#
#   bash restore.sh [lane]
set -eu
P=$(cd "$(dirname "$0")" && pwd)
L=${1:-/Users/feb/dev/infra/pearde/pearde/.lanes/every-document-is-written-in-the-writer-s-prose-skills-and-scout-docs-are-rewritten-dense}
cp "$P"/skills/*.md "$L"/references/skills/
cp "$P"/scout/*.md  "$L"/resources/scout/
cd "$L"
git diff --stat -- references/skills resources/scout | tail -1
python3 resources/prose.py check references/skills/*.md resources/scout/*.md && echo "scope green"
