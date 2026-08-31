---
complexity: 8
footprint:
  - resources/workflows.py
---

# spec01 — `workflows.py add` writes one slug from one body

Already stands: `add(board, slug, kind, subject, body, date)` in
`resources/workflows.py` — refuses (`ValueError`) a slug already in the
library by either kind, else writes `<slug>.md` with a closed frontmatter
(`atomic:`/`workflow:`, `subject`, `date`, `runs: 0`) and `body` verbatim
under it. A CLI door, `python3 resources/workflows.py add <slug>
<atomic|workflow> <subject> [board]` with the body on stdin, exists for the
same call outside `specced` — the door named in `@references/drill.md` and
`@references/workflow.md`'s "written by `specced`" note. Nothing left to
finish here; this spec is the seam a later `workflow add` skill handle calls
into.

## Acceptance

- [x] `add()` refuses a slug already in the library (either kind), raising
      before any file is touched
- [x] `add()` writes a workflow and an atomic each in the closed frontmatter
      shape, `runs: 0`, that `workflows.py check` accepts
- [x] the CLI `add` subcommand round-trips: writes the file, prints its path,
      and a second call for the same slug is refused, exit 1

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 -m py_compile resources/workflows.py
D=$(mktemp -d)/.pearde && mkdir -p "$D/workflows"
cat > "$D/settings.md" <<'SETTINGS'
---
language: English
---
SETTINGS
printf '# t — a probe atomic\n\n## Do\n\n1. Nothing.\n\n## Done when\n\n- Nothing.\n' | \
  python3 resources/workflows.py add probe-atomic atomic "a probe atomic" "$D"
test -f "$D/workflows/probe-atomic.md"
python3 resources/workflows.py check "$D"
printf 'again\n' | python3 resources/workflows.py add probe-atomic atomic "again" "$D" \
  2>/tmp/spec01.err && { echo "FAIL: duplicate slug should refuse"; exit 1; }
grep -q "already in the library" /tmp/spec01.err
echo spec01 ok
```
