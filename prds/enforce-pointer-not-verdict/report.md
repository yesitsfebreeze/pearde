Verdict: SPECCED

## Build

Read the PRD (its body is the docs page `docs/content/docs/improvements/
health-pointer-verdict.mdx`, which is still on disk — no recovery from
6839a9b needed). Ran `python3 resources/knowledge.py query` against the
contract; 104 broad hits, none a real match — no gap enqueued. Ran
`python3 resources/workflows.py list` and followed `probe-then-spec` (open
PRD, contract to specs from a build).

Built and proved the fix in the lane
`.pearde/.lanes/enforce-pointer-not-verdict` (the `repo:` this brief names):

- `resources/health.py`'s `list_ranking` now prints, per unhealthy file,
  its score, its worst axis **and its note's path** — the anchor a pointer
  needs. A file scoring under the floor whose note is missing from disk is
  named as missing its note (`no note at <path> — pearde health score
  writes one`), never named bare.
- `references/health.md`, `references/parts/health.md` and
  `references/parts/workers.md` now say once, beside the `<health>`
  placeholder and in health.md's "Handed to a worker" section, that the
  score never reorders the plan (`plan.py` reads no health key at all —
  verified: `plan.py scan` on a two-PRD fixture board is byte-identical
  under `health-floor: 1` and `health-floor: 100`).
- The "pointer, never a verdict" statement now stands fully in one place,
  `references/health.md`; `references/templates/grammar.md` and
  `references/skills/pearde-health.md` were trimmed from restating it to
  citing it.

Probe: `.pearde/prds/enforce-pointer-not-verdict/probe/
check_pointer_not_verdict.sh` — builds a throwaway board+repo, proves the
note-path line, the missing-note guard and the byte-identical plan across
floors. All three pass against the lane (`REPO=<lane>`); left in the tree,
uncommitted, uses no path under `.pearde/prds/`.

`resources/board/brief.py`'s `read_blocks()` still returns no `bad` entries
— the edited `<health>` row in `workers.md` parses sound.
`resources/index.py check` prints the same two pre-existing lines
before and after (`resources/common.py` no manifest row,
`hotreload-test.js` not on disk) — inherited, not this PRD's.
`resources/health.py check` prints only a pre-existing `stale:` note.

## Finding — `docs/` is untracked and out of scope

`docs/content/docs/health/index.mdx` and two sibling `docs/` pages restate
the same "worst first on one page — so a monolith is named before a worker
meets it" phrasing and the pointer-not-verdict rule a fourth time.
`git ls-files docs/` returns nothing — the whole tree (a Next.js/fumadocs
site, `node_modules` included) is untracked, outside the manifest, outside
every doctor row and outside any footprint the board's tools recognize.
Left alone; not edited, not spec'd — a wrong claim/duplicate found outside
this PRD's own mechanism, reported rather than fixed, per the contract.

## Scores

complexity: 15
blast-radius: mid
workflow: probe-then-spec
