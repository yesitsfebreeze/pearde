# a lane is declared at spec time and only a writer gets one — implementer, pass one

Verdict: DONE

spec01: 7/7 boxes ticked, each against output quoted below. The build stands
uncommitted in the lane
`/Users/feb/dev/infra/pearde/.pearde/.lanes/a-lane-is-declared-at-spec-time-and-only-a-writer-gets-one`,
six files, all six in the spec's `footprint:`. The checkout holds none of
them modified — `git -C /Users/feb/dev/infra/pearde status --short` is
`?? resources/board-name.sh` and nothing else — so collect merges the lane
with no `checkout --` needed on any footprint path.

## Baseline, recorded before the first edit

| root | `git status --short` |
|------|----------------------|
| lane | the six footprint files, ` M` each — the probe's pass-one code |
| checkout `/Users/feb/dev/infra/pearde` | `?? resources/board-name.sh` only |
| board `/Users/feb/dev/infra/pearde/.pearde` | 30+ PRD and `.state` files, none this PRD's but `prds/<this>/prd.md` |

Every `footprint:` path exists in the lane. No `@` or `@@` in the PRD body
dangles: `resources/board/{transitions,lanes,brief,init}.py` and
`.pearde/prds/every-worker-runs-in-its-own-worktree/prd.md` all resolve.

## Acceptance, box by box

| box | check run | output |
|-----|-----------|--------|
| `lane` in `FRONTMATTER_KEYS` | `grep -n` on `resources/board/init.py` | `92: "footprint", "origin", "from", "lane",` |
| `contract.md` documents `lane` + default | `git diff -- references/parts/contract.md` | row in the `prd.md` table (`analyst, at spec time` / `pearde claim` / `write \| read`, Optional) and in the defaults table (`` `write` — every PRD on the board today carries an implementer that edits ``) |
| `cut_lane` skips a `lane: read` PRD | verify block test 1 | `claim: p is \`lane: read\` — no worktree cut`, and `.lanes/p` absent |
| `cut_lane` unchanged when absent | verify block test 2 | `.lanes/p` present; progress line printed as before |
| `specced --lane`, refuses by name, both paths | verify block test 3 + the extra run below | refuse: `--lane \`bogus\` is not one of write\|read`, exit 1. Real run: `prd.md` carries `lane: read`. Dry run: previewed frontmatter carries `lane: read`, file byte-identical to before |
| `scores_of` returns `lane`, `route_report` forwards it | verify block test 4 + the extra run below | `scores_of(...) -> lane == "read"`; argv with a `lane:` line ends `['--blast','low','--lane','read']`, without one ends `['--blast','low']` |
| `claims.py check` reports no new problem | full-output diff, lane vs checkout | identical but for one unrelated line number (`prdfile.py:348` vs `:333`); 12 problems both sides, none naming `lane` |

### The verify block, run in the lane

The spec's block opens `cd /Users/feb/dev/infra/pearde` — the checkout. The
code is in the lane and the checkout is clean of it, so the block was run
with that `cd` pointed at the lane instead; nothing else in it resolves a
board, so no other substitution was needed. Output:

```
claim: p is `lane: read` — no worktree cut
▸ p: open → analyzing · done 0/1 · 0% · ... · as engineer
▸ p: open → analyzing · done 0/1 · 0% · ... · as engineer
spec01: ok
```

and its second line, `python3 resources/claims.py check . | grep -c
"contract.md.*lane" | grep -qx 0`, passed — the count is `0`.

### The two boxes the block does not reach

The block proves `--lane bogus` is refused and `scores_of` reads the key; it
does not reach the `--dry` half of box 5 or `route_report` in box 6. Both
were run separately, in the lane:

- **dry path** — `trlib.dry_line` spied on to capture the previewed
  frontmatter: `dry: previewed lane = read · file untouched`, and the
  `prd.md` bytes compared equal to the pre-run body. The real path writes
  `lane: read` into frontmatter. (`--dry` echoes no `dry · lane:` line, the
  way `--workflow` does; `--blast` echoes none either, and the spec names
  `--blast` as the path this follows. Left as is.)
- **`route_report`** — `COMMANDS["specced"]` swapped for a recorder:
  with `lane: read` in `## Scores` the argv is
  `['p','--as','engineer','--board',<tmp>,'--blast','low','--lane','read']`;
  with the line absent, `--lane` is not in the argv at all.

### The fixture proving the key's reader has teeth

`bad_keys` is what box 7 rides on, and a box that cannot fail is not a box.
In a `mktemp -d` copy of `resources/` and `references/`, with `lane` taken
back out of `FRONTMATTER_KEYS` and `contract.md` naming `` `lane: read` ``:

```
references/parts/contract.md:56: `lane:` — no frontmatter key of that name
```

With `lane` restored in the registry, the same tree greps `0` for the key.
Fixture removed; nothing was written under `prds/`.

## Workflow add-a-contract-key

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | ok — PRD body, `specs/spec01.md`, every `@` pointer opened, `git status --short` recorded in all three roots before the first edit |
| 2 | `settle-the-key-in-the-contract` | ok — one row in `contract.md`'s `prd.md` table, one in the defaults table, no sentence about the key's meaning in a second file. `grep -n lane references/parts/contract.md` reads both rows and nothing else |
| 3 | `teach-the-reader` | ok — `specs.py` owns the flag and is the only parser; `transitions.cut_lane` the only reader of the frontmatter key. Temp fixture above exits non-zero and names the key. No new `doctor.sh` row — see Edits |
| 4 | `sweep-for-other-copies` | ok — 5 greps, 20 hits, 13 inside the footprint and already carrying the key, 7 outside and none needing correction |
| 5 | `run-the-repo-gate` | ok — no new `broken` row, no new `index check` line traceable to the footprint |

No back-edge was taken.

### Edits

Two replacements for `add-a-contract-key`'s atomics, from what this run hit.

**`teach-the-reader`, step 3, item 5.** It reads

> 5. Add or extend the row in `resources/doctor.sh` so the check has a place a
>    person reads it.

and for a key joining a registry it demands a row that must not be written:
`resources/claims.py` reads `FRONTMATTER_KEYS` by name through
`_registry(root, "FRONTMATTER_KEYS")`, and `doctor.sh`'s `claims` row
already runs it, so a key added to that tuple is covered the moment it lands.
A second row would be a second reader of one check. Replacement:

> 5. Add or extend the row in `resources/doctor.sh` so the check has a place a
>    person reads it — unless the key joined a registry a `doctor` row already
>    reads (`FRONTMATTER_KEYS` and `SETTING_KEYS` are both read by the
>    `claims` row). Then the row exists; say in the report which one it is
>    and that no second row was added.

**`teach-the-reader`, step 3, `## Fails when`.** The table is a header with
no rows, and this shape belongs in it:

> | seen | means | do |
> |------|-------|----|
> | the fixture with a bad value passes the check silently | the check reads the key by a pattern the fixture does not match — `claims.py`'s `KEY_RE` wants the key inside backticks **and** followed by a colon, so `` `lane` `` in a table cell is invisible to it | write the fixture in the exact shape the reader's regex matches, confirm it fails, then confirm the real tree is silent. A fixture that never fails proves the key is unread, not that it is right |

## Sweep — the greps and their hits

Run in the lane, over `*.md`, `*.py`, `*.sh`:

| grep | hits | inside footprint | outside |
|------|------|------------------|---------|
| `scores_of` | 2 | 2 — `collect.py:345` def, `:390` caller, both on the 3-tuple | 0 |
| `FRONTMATTER_KEYS` | 3 | 1 — `init.py:90` | 2 — `claims.py:174` and `references/parts/doctor.md:76` name the registry, not its members; neither needs the key |
| `--blast` | 7 | 4 — `specs.py:4,877`, `collect.py:347,393` | 3 — `README.md:50`, `references/parts/states.md:11`, `references/parts/solo.md:10`, each naming the command generally, none enumerating its flag set |
| `## Scores` | 4 | 2 — `workers.md:209` (the one template, now carrying `lane: read`), `collect.py:346` | 2 — `loop.md:136`, `workers.md:330`, prose about the block, not its shape |
| `lane: read` | 4 | 4 — `workers.md:196,216`, `transitions.py:488,497` | 0 |

20 before, 13 already correct inside the footprint, 7 named out of scope,
0 corrections owed. The `## Scores` template lives in exactly one file.

## The gate

`python3 resources/index.py check` — exit 1 in both roots, as at baseline.
The lane prints 27 lines to the checkout's 17; every one of the extra ten is
`references/files.md lists @docs/... — no such directory`, because a
`lanes.create` worktree carries no `docs/` tree. Pre-existing and
lane-shaped, not this PRD's. Neither root prints a line naming a footprint
file.

`bash resources/doctor.sh` — exit 1 in both. Broken rows, identical sets:
`index`, `claims` (3 drifted names), `origin` (40 derived · 1 with no
`from:`), `memos` (45 memos · 1 problem), `knowledge`, `questions`. All
pre-existing; none moved. The lane adds two `off` rows — `guard` (not wired
in the lane's sibling `.claude/`) and `vault` (no `.obsidian` beside a lane)
— both absent-not-wrong, and both artefacts of where a worktree sits.

`python3 resources/grammar.py check` — exit 0 in both roots.

## Findings outside scope

- `references/files.md` lists `@resources/board/purge.py` and
  `references/parts/handles.md:74` documents `pearde purge`; neither the file
  nor the verb exists. `index check` and `claims check` both print it in the
  clean checkout. Not in this footprint.
- `capabilities.md` names `zzdead`, no such verb, and `be` is a verb with no
  row. Same, pre-existing in the clean checkout.
