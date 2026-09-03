#!/bin/bash
# pearde update — check every install of this repo and bring it current.
#
#   update.sh --all           check every install found and bring it current
#   update.sh --dry           say what it would do, write nothing
#   update.sh --local         this repo's project skills directory only
#   update.sh --global        the machine-wide skills directory only
#
# `--all` is the default and never has to be typed.
#
# An install is five symlinks per skill (@references/install.md), so updating
# one is never a copy: the links already point at this working tree and the
# content is current the moment the tree is. What goes stale is the *set* —
# a skill added since the install has no folder, one renamed leaves a folder
# pointing at nothing, and either is silent. This visits the places a skill
# folder can live, reads each through `install.sh <dir>` — the one reader of
# where a link points — reports it ok / off / stale / broken the way doctor
# does, and re-applies the links where an install is already present.
#
# It never creates an install that is not there. A directory with no pearde in
# it reads `off` and carries the one command that would install it — because
# putting skills somewhere the user did not ask for them is how a machine ends
# up with two, and only one of them in force.
#
# Two global directories is the case worth naming. `CLAUDE_CONFIG_DIR` moves
# an agent's whole configuration, so `$CLAUDE_CONFIG_DIR/skills` and
# `~/.claude/skills` can both hold a complete install while only the first is
# read. Both are checked and both are labelled, because an install that is
# present and inert looks exactly like one that works.
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="$(cd "$DIR/.." && pwd -P)"
SKILLS="$ROOT/references/skills"
INSTALL="$DIR/install.sh"

MODE=all; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --all)    MODE=all ;;
    --dry)    DRY=1 ;;
    --local)  MODE=local ;;
    --global) MODE=global ;;
    -h|--help) awk 'NR>1 && /^#/ {sub(/^# ?/,""); print; next} NR>1 {exit}' "$0"; exit 0 ;;
    *) echo "update: unknown argument \`$1\` — --all, --dry, --local, --global" >&2; exit 2 ;;
  esac
  shift
done

BROKEN=0; STALE=0
row() { printf '  %-11s %-7s %s\n' "$1" "$2" "$3"; [ "$2" = broken ] && BROKEN=1; return 0; }
fix() { printf '  %-11s %-7s fix: %s\n' "" "" "$1"; }
note() { printf '  %-11s %-7s %s\n' "" "" "$1"; }

echo "pearde update — $ROOT"
echo

# ── the tree itself ──────────────────────────────────────────────────────────
# Every install reads through links into this working tree, so the tree is the
# thing that is actually out of date or not. Reported, never pulled: a pull
# with local work in the way fails halfway and leaves an install half-current.
if git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  BRANCH=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null)
  DIRTY=$(git -C "$ROOT" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  UP=$(git -C "$ROOT" rev-parse --abbrev-ref '@{u}' 2>/dev/null)
  if [ -n "$UP" ]; then
    git -C "$ROOT" fetch --quiet 2>/dev/null
    read -r BEHIND AHEAD <<<"$(git -C "$ROOT" rev-list --left-right --count "$UP...HEAD" 2>/dev/null)"
    STATE="$BRANCH · ${DIRTY} uncommitted · ${AHEAD:-0} ahead, ${BEHIND:-0} behind $UP"
    if [ "${BEHIND:-0}" -gt 0 ]; then
      row tree off "$STATE"
      fix "git -C $ROOT pull — every install reads through links into this tree"
    else
      row tree ok "$STATE"
    fi
  else
    row tree ok "$BRANCH · ${DIRTY} uncommitted · no upstream"
  fi
else
  row tree ok "not a git checkout — nothing to pull"
fi

WANT=$(ls "$SKILLS"/*.md 2>/dev/null | wc -l | tr -d ' ')

# check_dir <label> <dir> <aside>
#   Reports one skills directory and, when pearde is already installed in it,
#   re-applies the links so a skill added since lands as a folder.
check_dir() {
  local label="$1" dir="$2" aside="$3"
  [ -n "$aside" ] && aside=" · $aside"
  if [ -z "$dir" ]; then
    row "$label" off "no skills directory for this scope$aside"
    return 0
  fi
  if [ ! -d "$dir" ]; then
    row "$label" off "$dir does not exist$aside"
    fix "mkdir -p $dir && bash $INSTALL --apply $dir"
    return 0
  fi
  if [ ! -e "$dir/pearde/SKILL.md" ]; then
    row "$label" off "$dir holds no pearde$aside"
    fix "bash $INSTALL --apply $dir"
    return 0
  fi
  # `install.sh <dir>` in report mode is the one reader of what a link points
  # at — readlink against the source it should name, per link — so the verdict
  # here is parsed from its rows, never re-derived from a walk of our own. A
  # walk testing `-e` reads a link into some other checkout as fine.
  local out=""
  [ "$DRY" = 1 ] || out=$(bash "$INSTALL" --apply "$dir" 2>&1)
  local rep name st _rest have=0 absent=0 wrong=0 copies=0
  rep=$(bash "$INSTALL" "$dir" 2>&1)
  while read -r name st _rest; do
    [ -n "$name" ] && [ -f "$SKILLS/$name.md" ] || continue   # the agent rows report here too
    case "$st" in
      ok|self)  have=$((have + 1)) ;;
      copy)     copies=$((copies + 1)) ;;
      missing)  if [ -d "$dir/$name" ]; then wrong=$((wrong + 1)); else absent=$((absent + 1)); fi ;;
    esac
  done <<<"$rep"
  # every pearde folder no skill file claims — install.sh never looks at those
  local stale="" f
  for f in "$dir"/pearde "$dir"/pearde-*; do
    [ -d "$f" ] && [ ! -f "$SKILLS/$(basename "$f").md" ] && stale="$stale $(basename "$f")"
  done
  if [ "$copies" -gt 0 ]; then
    row "$label" broken "$dir · $copies skill folder(s) hold a real SKILL.md, not a link$aside"
    fix "reconcile by hand — the ! lines of: bash $INSTALL $dir"
  elif [ "$wrong" -gt 0 ]; then
    row "$label" broken "$dir · $wrong skill folder(s) link somewhere other than this tree$aside"
    fix "bash $INSTALL --apply $dir"
  elif [ "$absent" -gt 0 ]; then
    row "$label" stale "$dir · $have of $WANT skills · $absent without a folder$aside"
    fix "bash $INSTALL --apply $dir"
    STALE=1
  else
    row "$label" ok "$dir · $have of $WANT skills$aside"
    [ "$DRY" = 1 ] && note "dry · would run: bash $INSTALL --apply $dir"
  fi
  [ -n "$stale" ] && note "stale, no skill file claims them:$stale — remove by hand"
  echo "$out" | grep -E '✓|!' | while IFS= read -r l; do
    [ -n "$l" ] && printf '  %-11s %-7s %s\n' "" "" "$(echo "$l" | sed 's/^ *//')"
  done
  return 0
}

# ── local: this repo's own project skills directory ──────────────────────────
# A project skills directory is `<repo>/.claude/skills`, and it is per-repo by
# design — skills that exist here and nowhere else. This repo's, not the
# cwd's: the script is the install it checks, wherever the shell stands.
if [ "$MODE" = all ] || [ "$MODE" = local ]; then
  check_dir local "$ROOT/.claude/skills" "$(basename "$ROOT")"
fi

# ── global: the machine-wide one, and the one that is not in force ───────────
if [ "$MODE" = all ] || [ "$MODE" = global ]; then
  CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  check_dir global "$CFG/skills" \
    "$([ -n "${CLAUDE_CONFIG_DIR:-}" ] && echo "CLAUDE_CONFIG_DIR — in force" \
       || echo "default location")"
  if [ -n "${CLAUDE_CONFIG_DIR:-}" ] && [ "$CFG" != "$HOME/.claude" ] \
     && [ -d "$HOME/.claude/skills" ]; then
    check_dir global-alt "$HOME/.claude/skills" \
      "NOT in force — CLAUDE_CONFIG_DIR points elsewhere"
  fi
fi

echo
if [ "$BROKEN" = 1 ]; then
  echo "pearde: an install is broken — the fix line under it is the whole repair."
  exit 1
fi
if [ "$STALE" = 1 ]; then
  echo "pearde: an install is behind — \`pearde update\` without --dry re-links it."
  exit 0
fi
echo "pearde: every install found is current. \`pearde upgrade [<dir>]\` brings a *board* up to this layout."
